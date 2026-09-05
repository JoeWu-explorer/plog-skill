"""Local image I/O only. Visual verification belongs to the invoking agent."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import io
import json
import os
from pathlib import Path
import tempfile
from typing import Any, Iterator
import warnings

from PIL import Image, ImageCms, ImageOps, UnidentifiedImageError


class PhotoError(ValueError):
    pass


def sha256(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def _decode(path: Path) -> tuple[Image.Image, str]:
    if path.suffix.lower() in {'.heic', '.heif'}:
        try:
            from pillow_heif import register_heif_opener
            register_heif_opener()
        except ImportError as exc:
            raise PhotoError('HEIF unavailable; install the optional locked extra or provide JPEG/PNG/WebP.') from exc
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', Image.DecompressionBombWarning)
            with Image.open(path) as original:
                format_name = original.format or ''
                if format_name not in {'JPEG', 'PNG', 'WEBP', 'HEIF'}:
                    raise PhotoError('Unsupported format; provide static JPEG, PNG or WebP (HEIF is optional).')
                if getattr(original, 'n_frames', 1) != 1 or getattr(original, 'is_animated', False):
                    raise PhotoError('Animated or multi-page input is unsupported; provide a static photo.')
                original.load()
                oriented = ImageOps.exif_transpose(original)
                alpha = oriented.convert('RGBA').getchannel('A') if 'A' in oriented.getbands() or 'transparency' in oriented.info else None
                profile = original.info.get('icc_profile')
                if profile:
                    try:
                        converted = ImageCms.profileToProfile(oriented, ImageCms.ImageCmsProfile(io.BytesIO(profile)), ImageCms.createProfile('sRGB'), outputMode='RGB')
                    except (OSError, ValueError, ImageCms.PyCMSError) as exc:
                        raise PhotoError('Embedded color profile cannot be safely converted to sRGB.') from exc
                else:
                    if oriented.mode not in {'RGB', 'RGBA', 'L', 'LA', 'P', '1'}:
                        raise PhotoError('Color space needs a valid profile; provide an sRGB photo.')
                    converted = oriented.convert('RGB')
                if converted is None:
                    raise PhotoError('Color conversion returned no image.')
                if alpha is not None:
                    converted.putalpha(alpha)
                # Pixel-only copy strips all source metadata, including text chunks.
                clean = Image.frombytes(converted.mode, converted.size, converted.tobytes())
                return clean, format_name
    except (UnidentifiedImageError, OSError, SyntaxError, Image.DecompressionBombError, Image.DecompressionBombWarning) as exc:
        raise PhotoError('Photo cannot be safely decoded; provide a valid supported static photo.') from exc


def inspect_photo(path: Path) -> dict[str, Any]:
    image, format_name = _decode(Path(path))
    return {'format': format_name, 'size': list(image.size), 'mode': image.mode, 'sha256': sha256(Path(path))}


def verify_png(path: Path) -> dict[str, Any]:
    try:
        with Image.open(path) as image:
            image.load()
            if image.format != 'PNG' or getattr(image, 'n_frames', 1) != 1:
                raise PhotoError('Delivery must be a static PNG.')
            if image.info or image.getexif():
                raise PhotoError('Delivery contains metadata; export a clean PNG first.')
            if image.mode not in {'RGB', 'RGBA'}:
                raise PhotoError('Delivery must use RGB or RGBA pixels.')
            return {'size': list(image.size), 'mode': image.mode, 'sha256': sha256(path)}
    except (OSError, SyntaxError, Image.DecompressionBombError) as exc:
        raise PhotoError('Delivery PNG is damaged or unreadable.') from exc


def export_png(candidate: Path, destination: Path, *, source: Path) -> Path:
    """Publish a clean PNG without replacing any existing file or the source."""
    candidate, destination, source = Path(candidate), Path(destination), Path(source)
    if destination.resolve() == source.resolve():
        raise PhotoError('Source Photo cannot be overwritten.')
    before = sha256(source)
    image, _ = _decode(candidate)
    fd, temporary = tempfile.mkstemp(prefix='.photo-', suffix='.png', dir=destination.parent)
    staged = Path(temporary)
    try:
        with os.fdopen(fd, 'wb') as stream:
            image.save(stream, format='PNG')
            stream.flush()
            os.fsync(stream.fileno())
        verify_png(staged)
        if sha256(source) != before:
            raise PhotoError('Source Photo changed during export.')
        os.link(staged, destination)  # exclusive publication, also rejects dangling symlinks
        return destination
    finally:
        staged.unlink(missing_ok=True)


@contextmanager
def prepare(source: Path, workspace: Path) -> Iterator[Path]:
    """Own and clean only the temporary derivative created by this operation."""
    with tempfile.TemporaryDirectory(prefix='.photo-', dir=workspace) as temporary:
        derivative = export_png(source, Path(temporary) / 'prepared.png', source=source)
        yield derivative


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['inspect', 'prepare', 'export', 'verify'])
    parser.add_argument('path', type=Path)
    parser.add_argument('--destination', type=Path)
    parser.add_argument('--source', type=Path)
    args = parser.parse_args()
    try:
        if args.operation == 'inspect':
            result = inspect_photo(args.path)
        elif args.operation == 'verify':
            result = verify_png(args.path)
        else:
            if args.destination is None or (args.operation == 'export' and args.source is None):
                parser.error('prepare/export require --destination; export also requires --source')
            output = export_png(args.path, args.destination, source=args.source or args.path)
            result = {'path': str(output.resolve()), **verify_png(output)}
        print(json.dumps(result, ensure_ascii=False))
    except (PhotoError, OSError) as exc:
        parser.exit(1, f'{exc}\n')


if __name__ == '__main__':
    main()
