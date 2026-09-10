import json
import posixpath
import re
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from distribution import build, install, uninstall, agent_target, AGENTS, DistributionError, MANIFEST

ROOT = Path(__file__).resolve().parents[1]


class DistributionTests(unittest.TestCase):
    def test_legacy_package_upgrades_and_moves_without_touching_works(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            package = build(ROOT, root / 'new.zip')
            legacy = root / 'old.zip'
            with zipfile.ZipFile(package) as source, zipfile.ZipFile(legacy, 'w') as dest:
                for name in source.namelist():
                    value = source.read(name)
                    if name.endswith(MANIFEST):
                        manifest = json.loads(value)
                        manifest['name'] = 'photo-dialogue'
                        value = json.dumps(manifest).encode()
                    dest.writestr(name.replace('plog/', 'photo-dialogue/', 1), value)
            old = root / 'skills' / 'photo-dialogue'
            new = old.with_name('plog')
            work = root / 'work.png'
            work.write_bytes(b'preserve my work')
            install(legacy, old)
            with self.assertRaises(DistributionError):
                install(package, new)
            install(package, old, update=True)
            old.rename(new)
            self.assertEqual(json.loads((new / MANIFEST).read_text())['name'], 'plog')
            uninstall(new)
            self.assertEqual(work.read_bytes(), b'preserve my work')

    def test_package_name_mismatch_and_mixed_roots_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            package = build(ROOT, root / 'new.zip')
            for mode in ('manifest', 'root'):
                bad = root / (mode + '.zip')
                with zipfile.ZipFile(package) as source, zipfile.ZipFile(bad, 'w') as dest:
                    for name in source.namelist():
                        value = source.read(name)
                        if name.endswith(MANIFEST):
                            if mode == 'manifest':
                                manifest = json.loads(value)
                                manifest['name'] = 'photo-dialogue'
                                value = json.dumps(manifest).encode()
                            else:
                                name = name.replace('plog/', 'photo-dialogue/', 1)
                        dest.writestr(name, value)
                with self.assertRaises(DistributionError):
                    install(bad, root / 'plog')
                self.assertFalse((root / 'plog').exists())

    def test_packaged_markdown_references_resolve_inside_archive(self):
        with tempfile.TemporaryDirectory() as folder:
            package = build(ROOT, Path(folder) / 'candidate.zip')
            with zipfile.ZipFile(package) as archive:
                names = set(archive.namelist())
                for name in names:
                    if not name.endswith('.md'):
                        continue
                    for link in re.findall(r'\]\(([^)]+)\)', archive.read(name).decode()):
                        if '://' in link or link.startswith('#'):
                            continue
                        target = posixpath.normpath(posixpath.join(posixpath.dirname(name), link.split('#')[0]))
                        self.assertIn(target, names, f'{name}: {link}')

    def _legacy_install(self, root):
        package = build(ROOT, root / 'candidate.zip')
        target = root / 'skills' / 'plog'
        install(package, target)
        manifest_path = target / MANIFEST
        manifest = json.loads(manifest_path.read_text())
        for name in ('references/conversation.md', 'references/agents.md', 'scripts/image_backend.py', 'references/albums.md', 'scripts/album.py', 'assets/album.html.txt'):
            del manifest['files'][name]
            (target / name).unlink()
        manifest_path.write_text(json.dumps(manifest))
        return package, target

    def test_legacy_installation_upgrades_with_conversation_reference(self):
        with tempfile.TemporaryDirectory() as folder:
            package, target = self._legacy_install(Path(folder))
            install(package, target, update=True)
            self.assertEqual((target / 'references/conversation.md').read_bytes(), (ROOT / 'plog/references/conversation.md').read_bytes())
            uninstall(target)
            self.assertFalse(target.exists())

    def test_legacy_installation_still_protects_local_edits(self):
        with tempfile.TemporaryDirectory() as folder:
            package, target = self._legacy_install(Path(folder))
            source = target / 'SKILL.md'
            source.write_text('my local changes')
            with self.assertRaises(DistributionError):
                install(package, target, update=True)
            with self.assertRaises(DistributionError):
                uninstall(target)
            self.assertEqual(source.read_text(), 'my local changes')

    def test_unknown_legacy_manifest_does_not_allow_update_or_uninstall(self):
        with tempfile.TemporaryDirectory() as folder:
            package, target = self._legacy_install(Path(folder))
            manifest_path = target / MANIFEST
            manifest = json.loads(manifest_path.read_text())
            del manifest['files']['references/runtime.md']
            (target / 'references/runtime.md').unlink()
            manifest_path.write_text(json.dumps(manifest))
            with self.assertRaises(DistributionError):
                install(package, target, update=True)
            with self.assertRaises(DistributionError):
                uninstall(target)
            self.assertTrue((target / 'SKILL.md').exists())

    def test_clean_package_install_and_modified_file_protection(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            package = build(ROOT, root / 'candidate.zip')
            target = root / 'skills' / 'plog'
            install(package, target)
            self.assertTrue((target / 'SKILL.md').is_file())
            self.assertTrue((target / 'assets/album.html.txt').is_file())
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
            target = root / 'skills' / 'plog'
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
            target = root / 'plog'
            with self.assertRaises(DistributionError):
                install(package, target)
            self.assertFalse(target.exists())
            self.assertFalse((root / 'outside').exists())

    def test_private_files_inside_cache_or_named_like_manifest_are_protected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            package = build(ROOT, root / 'candidate.zip')
            target = root / 'plog'
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
            target = root / 'plog'
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
            backups = list(root.glob('.plog-backup-*'))
            self.assertEqual(len(backups), 1)
            self.assertEqual((backups[0] / 'plog' / 'SKILL.md').read_bytes(), original)

    def test_all_agent_profiles_install_same_complete_skill(self):
        import os
        import subprocess
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            package=build(ROOT,root/'candidate.zip')
            for agent in AGENTS:
                with self.subTest(agent=agent):
                    home=root/agent
                    env=dict(os.environ, HOME=str(home), OPENCLAW_STATE_DIR=str(home/'.openclaw'), HERMES_HOME=str(home/'.hermes'), CLAUDE_CONFIG_DIR=str(home/'.claude'), DSH_HOME=str(home/'.dsh'))
                    result=subprocess.run([sys.executable,str(ROOT/'scripts/distribution.py'),'install',str(package),'--agent',agent],env=env,capture_output=True,text=True)
                    self.assertEqual(result.returncode,0,result.stderr)
                    report=json.loads(result.stdout)
                    target=Path(report['installed'])
                    expected={'generic':'.agents','codex':'.agents','claude-code':'.claude','openclaw':'.openclaw','hermes':'.hermes','deepseek-harness':'.dsh'}[agent]
                    self.assertEqual(target,home/expected/'skills/plog')
                    self.assertTrue((target/'references/agents.md').is_file())
                    self.assertTrue((target/'scripts/image_backend.py').is_file())
                    self.assertEqual(report['host_discovery'],'unverified')
                    uninstall(target)

    def test_alpha3_installation_upgrades_with_backend(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder); package=build(ROOT,root/'candidate.zip'); target=root/'plog'
            install(package,target)
            manifest=json.loads((target/MANIFEST).read_text())
            for name in ('references/agents.md','scripts/image_backend.py','references/albums.md','scripts/album.py','assets/album.html.txt'):
                del manifest['files'][name]
                (target/name).unlink()
            (target/MANIFEST).write_text(json.dumps(manifest))
            install(package,target,update=True)
            self.assertTrue((target/'scripts/image_backend.py').is_file())
            uninstall(target)

    def test_alpha6_installation_upgrades_with_album_resources(self):
        from distribution import ALPHA6_PACKAGE_FILES
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            package = build(ROOT, root / 'new.zip')
            target = root / 'plog'
            install(package, target)
            manifest = json.loads((target / MANIFEST).read_text())
            for name in set(manifest['files']) - ALPHA6_PACKAGE_FILES:
                del manifest['files'][name]
                (target / name).unlink()
            (target / MANIFEST).write_text(json.dumps(manifest))
            install(package, target, update=True)
            self.assertTrue((target / 'scripts/album.py').is_file())
            self.assertTrue((target / 'assets/album.html.txt').is_file())
            uninstall(target)
