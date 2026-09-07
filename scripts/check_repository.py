"""Check runtime boundaries, local references, fixture integrity and asset inventory."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import tempfile

from distribution import build


def check(root: Path, *, release: bool = False) -> dict[str, int]:
    runtime = root / 'plog'
    references_checked = 0
    for document in runtime.rglob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)', document.read_text()):
            if '://' not in target and not target.startswith('#'):
                references_checked += 1
                resolved = (document.parent / target.split('#')[0]).resolve()
                if not resolved.is_relative_to(runtime.resolve()) or not resolved.is_file():
                    raise ValueError(f'Broken or external runtime reference in {document.name}: {target}')
    inventory = json.loads((root / 'docs/assets.json').read_text())
    found = {str(path.relative_to(root)) for folder in ('tests/fixtures', 'prototypes', 'examples') for path in (root / folder).rglob('*') if path.suffix.lower() in ('.png', '.jpg', '.jpeg', '.webp', '.heic', '.svg', '.gif')}
    if set(inventory) != found:
        raise ValueError('Every repository image must have an asset inventory entry; removed assets must be reconciled.')
    for path, asset in inventory.items():
        if hashlib.sha256((root / path).read_bytes()).hexdigest() != asset['sha256'] or not asset['source'] or not (root / asset['provenance']).is_file():
            raise ValueError(f'Changed or undocumented asset: {path}')
        if release and asset['license'] not in ('CC0-1.0', 'MIT', 'PROJECT-DISPLAY'):
            raise ValueError(f'Publication blocked by unresolved asset license: {path}')
    with tempfile.TemporaryDirectory() as temporary:
        build(root, Path(temporary) / 'skill.zip')
    return {'runtime_markdown_references': references_checked, 'inventoried_assets': len(inventory)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release', action='store_true', help='Also require every repository asset to have a cleared publication license')
    args = parser.parse_args()
    try:
        print(json.dumps(check(Path(__file__).resolve().parents[1], release=args.release)))
    except (OSError, ValueError) as exc:
        parser.exit(1, f'{exc}\n')


if __name__ == '__main__':
    main()
