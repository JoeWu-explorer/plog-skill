"""Build an allowlisted skill; install/update/uninstall with local-edit protection."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
import shutil
import tempfile
from typing import Any
import zipfile

RUNTIME_FILES = (
    'SKILL.md', 'agents/openai.yaml',
    'references/art-direction.md', 'references/people-and-privacy.md',
    'references/revisions.md', 'references/runtime.md', 'references/conversation.md', 'references/agents.md',
    'schemas/revision-record.schema.json',
    # Text-suffixed HTML template also fits the Red Skill source-file allowlist.
    'references/albums.md', 'scripts/album.py', 'assets/album.html.txt',
    'scripts/photo_files.py', 'scripts/revision_record.py', 'scripts/self_check.py', 'scripts/image_backend.py',
    'requirements.txt', 'requirements.lock', 'requirements-heif.txt', 'requirements-heif.lock',
    'notices/Pillow.txt', 'notices/pillow-heif.txt',
)
PACKAGE_FILES = (*RUNTIME_FILES, 'LICENSE', 'THIRD_PARTY_NOTICES.md')
# Preserve exact historical layouts for safe upgrades, never arbitrary subsets.
ALPHA6_PACKAGE_FILES = frozenset(PACKAGE_FILES) - {'references/albums.md', 'scripts/album.py', 'assets/album.html.txt'}
ALPHA3_PACKAGE_FILES = ALPHA6_PACKAGE_FILES - {'references/agents.md', 'scripts/image_backend.py'}
LEGACY_PACKAGE_FILES = ALPHA3_PACKAGE_FILES - {'references/conversation.md'}
MANIFEST = 'INSTALL-MANIFEST.json'
SKILL_NAMES = ('plog', 'photo-dialogue')
AGENTS = ('generic', 'codex', 'claude-code', 'openclaw', 'hermes', 'deepseek-harness')


def agent_target(agent: str) -> Path:
    """Resolve one explicit host profile; never install into other agents implicitly."""
    home = Path.home()
    roots = {
        'generic': home / '.agents' / 'skills',
        'codex': home / '.agents' / 'skills',
        'claude-code': Path(os.environ.get('CLAUDE_CONFIG_DIR', str(home / '.claude'))) / 'skills',
        'openclaw': Path(os.environ.get('OPENCLAW_STATE_DIR', str(home / '.openclaw'))) / 'skills',
        'hermes': Path(os.environ.get('HERMES_HOME', str(home / '.hermes'))) / 'skills',
        'deepseek-harness': Path(os.environ.get('DSH_HOME', str(home / '.dsh'))) / 'skills',
    }
    if agent not in roots:
        raise DistributionError('Unknown agent; use --target for a custom discovery directory.')
    return roots[agent].expanduser().absolute() / 'plog'


class DistributionError(ValueError):
    pass


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build(repository: Path, destination: Path) -> Path:
    data: dict[str, bytes] = {}
    for name in PACKAGE_FILES:
        source = repository / name if name in ('LICENSE', 'THIRD_PARTY_NOTICES.md') else repository / 'plog' / name
        if source.is_symlink() or not source.is_file():
            raise DistributionError(f'Missing or symbolic package input: {name}')
        data[name] = source.read_bytes()
        if b'/Users/' in data[name] or b'/home/' in data[name]:
            raise DistributionError(f'Developer absolute path in package input: {name}')
    manifest = {'schema_version': 1, 'name': 'plog', 'files': {name: _digest(value) for name, value in data.items()}}
    data[MANIFEST] = (json.dumps(manifest, sort_keys=True, indent=2) + '\n').encode()
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, value in sorted(data.items()):
            info = zipfile.ZipInfo('plog/' + name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, value)
    return destination


def _payload(package: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(package) as archive:
        names = archive.namelist()
        prefix = names[0].split('/')[0] if names else ''
        if prefix not in SKILL_NAMES:
            raise DistributionError('Unknown skill package root.')
        expected = {prefix + '/' + name for name in (*PACKAGE_FILES, MANIFEST)}
        if len(names) != len(expected) or set(names) != expected:
            raise DistributionError('Package violates the exact allowlist.')
        if any(info.file_size > 2_000_000 or (info.external_attr >> 16) & 0o170000 == 0o120000 for info in archive.infolist()):
            raise DistributionError('Package contains oversized or symbolic entries.')
        data = {name.removeprefix(prefix + '/'): archive.read(name) for name in names}
    manifest = json.loads(data[MANIFEST])
    if not isinstance(manifest, dict) or manifest.get('schema_version') != 1 or manifest.get('name') != prefix or manifest.get('files') != {name: _digest(data[name]) for name in PACKAGE_FILES}:
        raise DistributionError('Package integrity manifest does not match.')
    return data


def _unchanged(target: Path) -> None:
    if target.name not in SKILL_NAMES or target.is_symlink() or not target.is_dir():
        raise DistributionError('Select the exact plog (or legacy photo-dialogue) installation directory.')
    try:
        if any(path.is_symlink() for path in target.rglob('*')):
            raise DistributionError('Installation contains symbolic links; preserve it and resolve manually.')
        manifest: dict[str, Any] = json.loads((target / MANIFEST).read_text())
        if not isinstance(manifest, dict) or not isinstance(manifest.get('files'), dict):
            raise DistributionError('Invalid installation manifest.')
        expected = manifest['files']
        if manifest.get('name') not in SKILL_NAMES or manifest.get('schema_version') != 1 or set(expected) not in (set(PACKAGE_FILES), ALPHA6_PACKAGE_FILES, ALPHA3_PACKAGE_FILES, LEGACY_PACKAGE_FILES):
            raise DistributionError('Unknown installation manifest.')
        actual = {}
        for path in target.rglob('*'):
            if not path.is_file():
                continue
            relative = path.relative_to(target).as_posix()
            cache = re.fullmatch(r'scripts/__pycache__/(photo_files|revision_record|self_check|image_backend|album)\.cpython-3(11|12|13)(\.opt-[12])?\.pyc', relative)
            if relative != MANIFEST and cache is None:
                actual[relative] = _digest(path.read_bytes())
        if actual != expected:
            raise DistributionError('Local files were added, removed or modified; preserve them before update/uninstall.')
    except (OSError, KeyError, ValueError, TypeError) as exc:
        raise DistributionError('Installation unrecognized or locally modified; nothing removed.') from exc


def install(package: Path, target: Path, *, update: bool = False) -> None:
    if target.name not in SKILL_NAMES or target.is_symlink():
        raise DistributionError('Target must be the exact plog (or legacy photo-dialogue) skill directory, not a symlink.')
    default = Path.home() / '.agents' / 'skills' / 'plog'
    if target.name == 'plog' and (target.parent / 'photo-dialogue').exists():
        raise DistributionError('Legacy sibling installation exists; migrate it before installing plog.')
    legacy = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'skills' / 'photo-dialogue'
    if target == default and legacy.exists() and legacy.resolve() != target.resolve():
        raise DistributionError('Legacy installation exists; select one discovery location before installing.')
    data = _payload(package)
    existed = target.exists()
    if existed:
        if not update:
            raise DistributionError('Installation exists; use update after checking local changes.')
        _unchanged(target)
    elif update:
        raise DistributionError('No existing installation to update.')
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.photo-install-', dir=target.parent) as temporary:
        staging = Path(temporary) / 'new'
        staging.mkdir()
        for name, value in data.items():
            output = staging / name
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(value)
        backup_root: Path | None = None
        backup: Path | None = None
        if existed:
            _unchanged(target)  # staging may have taken time; protect intervening edits
            backup_root = Path(tempfile.mkdtemp(prefix=f'.{target.name}-backup-', dir=target.parent))
            backup = backup_root / target.name
            target.rename(backup)
        try:
            if backup is not None:
                _unchanged(backup)
            staging.rename(target)
        except BaseException:
            if backup is not None:
                try:
                    backup.rename(target)
                except BaseException as restore_error:
                    raise DistributionError(f'Update and rollback failed. Previous installation preserved at {backup}') from restore_error
                if backup_root is not None:
                    backup_root.rmdir()
            raise
        if backup_root is not None:
            shutil.rmtree(backup_root)


def uninstall(target: Path) -> None:
    _unchanged(target)
    shutil.rmtree(target)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='operation', required=True)
    pack = commands.add_parser('build')
    pack.add_argument('destination', type=Path)
    pack.add_argument('--repository', type=Path, default=Path(__file__).resolve().parents[1])
    for name in ('install', 'update'):
        sub = commands.add_parser(name)
        sub.add_argument('package', type=Path)
        destination = sub.add_mutually_exclusive_group()
        destination.add_argument('--target', type=Path, help='Exact skill directory for custom profiles or sandboxes')
        destination.add_argument('--agent', choices=AGENTS, default='generic', help='Resolve the selected agent discovery directory')
    remove = commands.add_parser('uninstall')
    remove.add_argument('--target', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.operation == 'build':
            result = build(args.repository, args.destination)
            print(json.dumps({'package': str(result), 'sha256': _digest(result.read_bytes())}))
        elif args.operation == 'uninstall':
            uninstall(args.target)
            print('Specified skill removed; independent works retained.')
        else:
            target = args.target.expanduser().absolute() if args.target is not None else agent_target(args.agent)
            install(args.package, target, update=args.operation == 'update')
            print(json.dumps({'installed': str(target), 'host_discovery': 'unverified', 'image_service': 'unverified'}, ensure_ascii=False))
    except (DistributionError, OSError, ValueError, zipfile.BadZipFile) as exc:
        parser.exit(1, f'{exc}\n')


if __name__ == '__main__':
    main()
