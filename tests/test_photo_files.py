import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'photo-dialogue' / 'scripts'))
from photo_files import inspect_photo, prepare, export_png, verify_png, PhotoError


class PhotoFilesTests(unittest.TestCase):
    def test_oriented_source_is_unchanged_and_export_has_no_private_metadata(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / 'camera.jpg'
            exif = Image.Exif()
            exif[274] = 6
            exif[271] = 'Private camera'
            Image.new('RGB', (40, 20), 'red').save(source, exif=exif)
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            self.assertEqual(inspect_photo(source)['size'], [20, 40])
            with prepare(source, root) as prepared:
                self.assertEqual(verify_png(prepared)['size'], [20, 40])
                output = export_png(prepared, root / 'result.png', source=source)
                self.assertEqual(verify_png(output)['size'], [20, 40])
            self.assertFalse(prepared.exists())
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), digest)
            with Image.open(output) as image:
                self.assertFalse(image.info)
                self.assertFalse(image.getexif())

    def test_supported_formats_and_alpha_round_trip(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for fmt in ('JPEG', 'PNG', 'WEBP'):
                with self.subTest(format=fmt):
                    source = root / fmt
                    Image.new('RGB', (32, 24), 'blue').save(source, format=fmt)
                    output = export_png(source, root / (fmt + '.png'), source=source)
                    self.assertEqual(verify_png(output)['size'], [32, 24])
            source = root / 'transparent.png'
            Image.new('RGBA', (8, 8), (0, 20, 30, 40)).save(source)
            output = export_png(source, root / 'alpha.png', source=source)
            with Image.open(output) as image:
                self.assertEqual(image.getpixel((0, 0)), (0, 20, 30, 40))

    def test_animation_corruption_and_unsupported_input_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for fmt in ('PNG', 'WEBP', 'TIFF'):
                source = root / fmt
                Image.new('RGB', (8, 8), 'red').save(source, format=fmt, save_all=True, append_images=[Image.new('RGB', (8, 8), 'blue')])
                with self.assertRaises(PhotoError):
                    inspect_photo(source)
            corrupt = root / 'broken.png'
            corrupt.write_bytes(b'not an image')
            with self.assertRaises(PhotoError):
                inspect_photo(corrupt)

    def test_existing_output_and_source_are_never_replaced(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / 'source.png'
            Image.new('RGB', (8, 8), 'red').save(source)
            original = source.read_bytes()
            with self.assertRaises(PhotoError):
                export_png(source, source, source=source)
            alias = root / 'alias.png'
            alias.symlink_to(source)
            with self.assertRaises(PhotoError):
                export_png(source, alias, source=source)
            output = root / 'existing.png'
            output.write_bytes(b'keep me')
            with self.assertRaises(FileExistsError):
                export_png(source, output, source=source)
            self.assertEqual(output.read_bytes(), b'keep me')
            self.assertEqual(source.read_bytes(), original)
            self.assertFalse(list(root.glob('.photo-*')))

    def test_invalid_profile_is_not_silently_discarded(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'profile.png'
            Image.new('RGB', (8, 8)).save(source, icc_profile=b'invalid')
            with self.assertRaises(PhotoError):
                inspect_photo(source)

    def test_interrupted_publication_does_not_delete_a_replacement_file(self):
        import os
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / 'source.png'
            Image.new('RGB', (8, 8)).save(source)
            output = root / 'output.png'
            real_link = os.link
            def replaced_then_interrupted(src, dst):
                real_link(src, dst)
                Path(dst).unlink()
                Path(dst).write_bytes(b'user replacement')
                raise KeyboardInterrupt('interrupted after another writer replaced the link')
            with patch('os.link', side_effect=replaced_then_interrupted):
                with self.assertRaises(KeyboardInterrupt):
                    export_png(source, output, source=source)
            self.assertEqual(output.read_bytes(), b'user replacement')
            self.assertFalse(list(root.glob('.photo-*')))
