"""Offline functional probes. Never installs packages or calls an image service."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import platform
import sys
import tempfile
from typing import Any


def check(workspace: Path) -> dict[str, Any]:
    report: dict[str, Any] = {'local': 'fail', 'python': platform.python_version(), 'platform': sys.platform, 'host_image_service': 'unverified', 'formats': {}, 'heif': 'unavailable'}
    if platform.python_implementation() != 'CPython' or not (3, 11) <= sys.version_info[:2] <= (3, 13) or sys.platform not in ('darwin', 'linux'):
        report['reason'] = 'Use CPython 3.11–3.13 on macOS/Linux in an isolated environment.'
        return report
    try:
        from PIL import Image, __version__ as pillow_version
        from photo_files import export_png, inspect_photo, prepare, verify_png
        report['pillow'] = pillow_version
        if int(pillow_version.split('.')[0]) != 12:
            report['reason'] = 'Install Pillow>=12,<13 from the runtime lock in an isolated environment.'
            return report
        with tempfile.TemporaryDirectory(prefix='.photo-check-', dir=workspace) as folder:
            root = Path(folder)
            for format_name in ('JPEG', 'PNG', 'WEBP'):
                source = root / format_name
                Image.new('RGB', (32, 16), 'blue').save(source, format=format_name)
                if inspect_photo(source)['size'] != [32, 16]:
                    raise ValueError('Codec returned incorrect dimensions.')
                output = export_png(source, root / (format_name + '.png'), source=source)
                verify_png(output)
                report['formats'][format_name] = 'pass'
            exif = Image.Exif()
            exif[274] = 6
            exif[271] = 'self-check device marker'
            oriented = root / 'oriented.jpg'
            Image.new('RGB', (32, 16)).save(oriented, exif=exif)
            with prepare(oriented, root) as derivative:
                if verify_png(derivative)['size'] != [16, 32]:
                    raise ValueError('EXIF orientation probe failed.')
            try:
                import pillow_heif
                pillow_heif.register_heif_opener()
                heif = root / 'probe.heic'
                Image.new('RGB', (32, 16), 'blue').save(heif, format='HEIF')
                if inspect_photo(heif)['size'] != [32, 16]:
                    raise ValueError('HEIF dimensions are incorrect.')
                export_png(heif, root / 'heif.png', source=heif)
                report['heif'] = 'pass'
                report['pillow_heif'] = pillow_heif.__version__
            except ImportError:
                report['heif'] = 'unavailable: optional extra not installed; provide JPEG/PNG/WebP'
            except Exception:
                report['heif'] = 'fail: optional codec probe failed; provide JPEG/PNG/WebP'
        report['local'] = 'pass'
    except ImportError:
        report['reason'] = 'Pillow missing. Install requirements.lock into the selected isolated environment.'
    except Exception as exc:
        report['reason'] = f'Local read/write or codec probe failed ({type(exc).__name__}); check directory permissions and locked dependencies.'
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, required=True, help='Existing private writable directory; probes are removed')
    args = parser.parse_args()
    result = check(args.workspace)
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result['local'] == 'pass' else 1)


if __name__ == '__main__':
    main()
