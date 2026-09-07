"""Minimal private version records; no generation, authorization, or visual verdicts."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import date
import fcntl
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Any, Iterator
import uuid
from urllib.parse import quote

from photo_files import publish_png, PublishedPNG, sha256, verify_png, PhotoError


class RecordError(ValueError):
    pass


def new_workspace() -> Path:
    return Path.home() / 'Pictures' / 'PhotoDialogue' / f'{date.today()}-{uuid.uuid4().hex[:12]}'


def _keys(value: Any, expected: set[str]) -> None:
    if not isinstance(value, dict) or set(value) != expected:
        raise RecordError('Record has missing or unexpected fields; use schema version 1.')


def _text(value: Any, limit: int = 2000) -> None:
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise RecordError('Expected nonempty bounded text.')


def _version_details(version: Any) -> None:
    _keys(version, {'change_target', 'voice_elements', 'visual_intent'})
    _text(version['change_target'], 500)
    _text(version['visual_intent'])
    voices = version['voice_elements']
    if not isinstance(voices, list) or len(voices) > 3:
        raise RecordError('At most three voice elements; use [] for deliberate silence.')
    for voice in voices:
        _keys(voice, {'text', 'kind', 'attribution'})
        _text(voice['text'])
        _text(voice['attribution'], 200)
        if voice['kind'] not in ('confirmed_quote', 'creative_dialogue', 'inner_voice', 'narration'):
            raise RecordError('Unknown voice kind.')


def _structure(record: Any, work: Path, *, files: bool = True) -> dict[str, Any]:
    _keys(record, {'schema_version', 'source', 'current_version', 'versions'})
    if type(record['schema_version']) is not int or record['schema_version'] != 1:
        raise RecordError('Unsupported schema version; recovery stopped.')
    _keys(record['source'], {'path', 'sha256'})
    _text(record['source']['path'], 4096)
    if not Path(record['source']['path']).is_absolute():
        raise RecordError('Source reference must be an absolute user-provided path.')
    digest = record['source']['sha256']
    if not isinstance(digest, str) or re.fullmatch('[0-9a-f]{64}', digest) is None:
        raise RecordError('Invalid source checksum.')
    versions = record['versions']
    if not isinstance(versions, list) or not versions:
        raise RecordError('Record must contain accepted versions.')
    seen: set[str] = set()
    for index, version in enumerate(versions, 1):
        _keys(version, {'id', 'output', 'parent_id', 'change_target', 'voice_elements', 'visual_intent'})
        expected_id = f'v{index:03d}'
        if version['id'] != expected_id or version['output'] != f'{expected_id}.png':
            raise RecordError('Invalid version order or output reference.')
        parent = version['parent_id']
        if (index == 1 and parent is not None) or (index > 1 and (not isinstance(parent, str) or parent not in seen)):
            raise RecordError('Invalid parent version.')
        _version_details({key: version[key] for key in ('change_target', 'voice_elements', 'visual_intent')})
        output = work / version['output']
        if output.is_symlink() or output.resolve().parent != work.resolve():
            raise RecordError('Output reference escapes the work directory.')
        if files:
            if not output.is_file():
                raise RecordError(f'Accepted version {expected_id} is missing; no substitute selected.')
            verify_png(output)
        seen.add(expected_id)
    if not isinstance(record['current_version'], str) or record['current_version'] not in seen:
        raise RecordError('Current version does not exist.')
    return record


def _load(work: Path) -> dict[str, Any]:
    record_path = work / 'revision.json'
    if record_path.is_symlink():
        raise RecordError('Revision Record must be a local regular file.')
    try:
        if record_path.stat().st_size > 2_000_000:
            raise RecordError('Revision Record is too large.')
        with record_path.open(encoding='utf-8') as stream:
            return _structure(json.load(stream), work)
    except (FileNotFoundError, json.JSONDecodeError, UnicodeError) as exc:
        raise RecordError('Record missing or invalid; PNGs remain usable. Provide source, selected image and context for precise editing.') from exc


def validate(work: Path) -> dict[str, Any]:
    return _load(Path(work))


def select(work: Path, version_id: str | None = None) -> dict[str, Any]:
    record = validate(work)
    chosen = version_id or record['current_version']
    for version in record['versions']:
        if version['id'] == chosen:
            return version
    raise RecordError('Requested version does not exist; no substitute selected.')


def delivery(work: Path, version_id: str | None = None) -> dict[str, str]:
    """Re-show a validated accepted PNG without reading the original or changing records."""
    version = select(work, version_id)
    image = str((Path(work) / version['output']).resolve())
    target = quote(image, safe='/: ')
    chosen = version['id']
    return {'version_id': chosen, 'image': image,
            'markdown': f'![{chosen} 预览](<{target}>)\n\n[下载 {chosen} PNG](<{target}>)'}


@contextmanager
def _locked(work: Path) -> Iterator[None]:
    if work.is_symlink():
        raise RecordError('Work directory must not be a symbolic link.')
    # Directory locking leaves no private diagnostic or stale lock files.
    fd = os.open(work, os.O_RDONLY)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        os.close(fd)


def _commit(work: Path, record: dict[str, Any]) -> None:
    fd, name = tempfile.mkstemp(prefix='.record-', dir=work)
    temporary = Path(name)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            json.dump(record, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, work / 'revision.json')
    finally:
        temporary.unlink(missing_ok=True)


def _check_source(record: dict[str, Any], source: Path) -> None:
    if not source.is_file() or sha256(source) != record['source']['sha256']:
        raise RecordError('Source missing or changed. Provide the correct original; no directories were searched.')


def recover(work: Path, *, source: Path, version_id: str | None = None) -> dict[str, Any]:
    """Read only the explicitly supplied original, never follow a record as authority."""
    work, source = Path(work), Path(source).resolve()
    with _locked(work):
        record = validate(work)
        _check_source(record, source)
        version = select(work, version_id)
        if record['source']['path'] != str(source):
            record['source']['path'] = str(source)
            _commit(work, record)
        return {'source': record['source'], 'version': version, 'image': str((work / version['output']).resolve())}


def append(work: Path, *, source: Path, source_sha256: str, candidate: Path, version: dict[str, Any], parent_id: str | None = None) -> dict[str, Any]:
    """Call only after Delivery Verification. Failed saves keep accepted versions intact."""
    work, source = Path(work), Path(source).resolve()
    _version_details(version)
    if not isinstance(source_sha256, str) or re.fullmatch('[0-9a-f]{64}', source_sha256) is None:
        raise RecordError('Provide the source SHA-256 captured before generation.')
    _check_source({'source': {'sha256': source_sha256}}, source)
    if not work.exists():
        work.mkdir(parents=True, mode=0o700)
    with _locked(work):
        record_path = work / 'revision.json'
        if record_path.exists() or record_path.is_symlink():
            record = validate(work)
            _check_source(record, source)
            parent = select(work, parent_id)['id']
        else:
            if any(work.iterdir()):
                raise RecordError('Existing nonempty directory has no record; choose a new work directory.')
            if parent_id is not None:
                raise RecordError('First version cannot have a parent.')
            parent = None
            record = {'schema_version': 1, 'source': {'path': str(source), 'sha256': source_sha256}, 'current_version': 'v001', 'versions': []}
        version_id = f"v{len(record['versions']) + 1:03d}"
        entry = {'id': version_id, 'output': version_id + '.png', 'parent_id': parent, **version}
        output = work / entry['output']
        saved: PublishedPNG | None = None
        try:
            saved = publish_png(candidate, output, source=source)
            if not saved.is_current():
                raise RecordError('Published PNG was replaced; no version accepted.')
            _check_source(record, source)
            record['versions'].append(entry)
            record['current_version'] = version_id
            record['source']['path'] = str(source)
            _structure(record, work)
            if not saved.is_current():
                raise RecordError('Published PNG was replaced; no version accepted.')
            _commit(work, record)
        except BaseException:
            if saved is not None:
                # The OS may publish the record before an interrupt is raised.
                # Remove only a candidate known not to be referenced on disk.
                try:
                    published = json.loads(record_path.read_text()) if record_path.exists() else {'versions': []}
                    registered = any(item.get('output') == entry['output'] for item in published['versions'])
                except (OSError, ValueError, KeyError, TypeError, AttributeError):
                    registered = True  # uncertain state: preserve the image for recovery
                if not registered:
                    try:
                        if saved.is_current():
                            output.unlink()
                    except OSError:
                        pass  # Missing or uncertain ownership: preserve state and original error.
            raise
        return entry


def export_text(work: Path, destination: Path, version_id: str | None = None) -> None:
    version = select(work, version_id)
    fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as stream:
        stream.write('\n'.join(v['text'] for v in version['voice_elements']) + '\n')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['validate', 'select', 'recover', 'append', 'export-text', 'delivery'])
    parser.add_argument('work', type=Path)
    parser.add_argument('--source', type=Path)
    parser.add_argument('--candidate', type=Path)
    parser.add_argument('--source-sha256', help='Source checksum captured by inspect before generation')
    parser.add_argument('--details', type=Path, help='Private JSON with change_target, voice_elements, visual_intent')
    parser.add_argument('--version')
    parser.add_argument('--destination', type=Path)
    args = parser.parse_args()
    try:
        result: Any
        if args.operation == 'validate':
            result = validate(args.work)
        elif args.operation == 'select':
            result = select(args.work, args.version)
        elif args.operation == 'delivery':
            result = delivery(args.work, args.version)
        elif args.operation == 'recover':
            if args.source is None:
                parser.error('recover requires --source explicitly supplied by the user')
            result = recover(args.work, source=args.source, version_id=args.version)
        elif args.operation == 'export-text':
            if args.destination is None:
                parser.error('export-text requires --destination')
            export_text(args.work, args.destination, args.version)
            result = {'saved': str(args.destination)}
        else:
            if args.source is None or args.candidate is None or args.details is None or args.source_sha256 is None:
                parser.error('append requires --source, --source-sha256, --candidate and --details; use only after visual verification')
            result = append(args.work, source=args.source, source_sha256=args.source_sha256, candidate=args.candidate, version=json.loads(args.details.read_text()), parent_id=args.version)
            result = {**result, 'delivery': delivery(args.work, result['id'])}
        print(json.dumps(result, ensure_ascii=False))
    except (RecordError, PhotoError, OSError, ValueError) as exc:
        parser.exit(1, f'{exc}\n')


if __name__ == '__main__':
    main()
