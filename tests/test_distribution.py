import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from distribution import build, install, uninstall, DistributionError

ROOT = Path(__file__).resolve().parents[1]


class DistributionTests(unittest.TestCase):
    def test_clean_package_install_and_modified_file_protection(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            package = build(ROOT, root / 'candidate.zip')
            target = root / 'skills' / 'photo-dialogue'
            install(package, target)
            self.assertTrue((target / 'SKILL.md').is_file())
            self.assertFalse((target / 'assets').exists())
            self.assertFalse((target / '.venv').exists())
            install(package, target, update=True)
            (target / 'SKILL.md').write_text('my local changes')
            with self.assertRaises(DistributionError):
                install(package, target, update=True)
            with self.assertRaises(DistributionError):
                uninstall(target)
            self.assertEqual((target / 'SKILL.md').read_text(), 'my local changes')

    def test_uninstall_preserves_independent_works_and_unknown_files(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            package = build(ROOT, root / 'candidate.zip')
            target = root / 'skills' / 'photo-dialogue'
            install(package, target)
            work = root / 'Pictures' / 'v001.png'
            work.parent.mkdir()
            work.write_bytes(b'private work')
            unknown = target / 'private.txt'
            unknown.write_text('keep')
            with self.assertRaises(DistributionError):
                uninstall(target)
            unknown.unlink()
            uninstall(target)
            self.assertFalse(target.exists())
            self.assertEqual(work.read_bytes(), b'private work')

    def test_archive_traversal_is_rejected_before_any_file_is_written(self):
        import zipfile
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            package = root / 'bad.zip'
            with zipfile.ZipFile(package, 'w') as archive:
                archive.writestr('../outside', 'bad')
            target = root / 'photo-dialogue'
            with self.assertRaises(DistributionError):
                install(package, target)
            self.assertFalse(target.exists())
            self.assertFalse((root / 'outside').exists())

    def test_private_files_inside_cache_or_named_like_manifest_are_protected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            package = build(ROOT, root / 'candidate.zip')
            target = root / 'photo-dialogue'
            install(package, target)
            for relative in ('scripts/__pycache__/private.txt', 'notes/INSTALL-MANIFEST.json'):
                path = target / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('private work')
                with self.assertRaises(DistributionError):
                    uninstall(target)
                self.assertTrue(path.exists())
                path.unlink()

    def test_failed_update_and_failed_rollback_preserve_recoverable_previous_install(self):
        import os
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            package = build(ROOT, root / 'candidate.zip')
            target = root / 'photo-dialogue'
            install(package, target)
            original = (target / 'SKILL.md').read_bytes()
            real_rename = os.rename
            calls = 0
            def failing_rename(src, dst, *args, **kwargs):
                nonlocal calls
                calls += 1
                if calls >= 2:
                    raise OSError('controlled publish and restore failure')
                return real_rename(src, dst, *args, **kwargs)
            with patch('os.rename', side_effect=failing_rename):
                with self.assertRaises((OSError, DistributionError)):
                    install(package, target, update=True)
            backups = list(root.glob('.photo-dialogue-backup-*'))
            self.assertEqual(len(backups), 1)
            self.assertEqual((backups[0] / 'photo-dialogue' / 'SKILL.md').read_bytes(), original)
