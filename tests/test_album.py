import base64
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'plog/scripts'))
from album import AlbumError, export_album, validate_design
from photo_files import PhotoError


class AlbumDOM(HTMLParser):
    def __init__(self, value):
        super().__init__()
        self.images = []
        self.ids = []
        self.tags = []
        self.feed(value)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        self.tags.append(tag)
        if tag == 'img':
            self.images.append(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])


class AlbumTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        photo = Image.new('RGB', (80, 40), '#456745')
        exif = Image.Exif()
        exif[274] = 6
        exif[315] = 'private camera owner'
        photo.save(self.root / 'first.jpg', exif=exif)
        Image.new('RGBA', (30, 60), (30, 80, 200, 128)).save(self.root / 'second.png')
        self.story = {
            'schema_version': 1, 'title': '几段日常', 'cover': 1,
            'design': json.loads((ROOT / 'examples/album/story.json').read_text())['design'],
            'pages': [
                {'image': 'first.jpg', 'title': '桌边', 'alt': '第一张照片', 'text': '看一会儿光'},
                {'image': 'second.png', 'title': '窗外', 'alt': '第二张照片', 'text': '留一页给风'}
            ]
        }
        self.manifest = self.root / 'story.json'

    def export(self, name='album.html'):
        self.manifest.write_text(json.dumps(self.story))
        return export_album(self.manifest, self.root / name)

    def test_standalone_order_orientation_metadata_and_source_preservation(self):
        originals = {p: p.read_bytes() for p in self.root.iterdir()}
        report = self.export()
        content = Path(report['html']).read_text()
        dom = AlbumDOM(content)
        self.assertEqual(report['photos'], 2)
        self.assertEqual([i for i in dom.ids if i.startswith('photo-')], ['photo-1', 'photo-2'])
        self.assertEqual(len(dom.images), 3)
        self.assertEqual(dom.images[0]['src'], dom.images[2]['src'])
        self.assertNotIn(str(self.root), content)
        self.assertNotIn('private camera owner', content)
        self.assertEqual((dom.images[1]['width'], dom.images[1]['height']), ('40', '80'))
        for attrs in dom.images:
            self.assertTrue(attrs['src'].startswith('data:image/webp;base64,'))
            decoded = Image.open(io.BytesIO(base64.b64decode(attrs['src'].split(',')[1])))
            self.assertFalse(decoded.getexif())
            self.assertFalse({'exif', 'xmp', 'icc_profile'} & decoded.info.keys())
        for path, original in originals.items():
            self.assertEqual(path.read_bytes(), original)
        self.assertEqual(list(self.root.glob('.album-*')), [])

    def test_untrusted_text_is_literal_and_not_template_or_script(self):
        self.story['title'] = '<script>alert(1)</script>{{PAGES}}'
        self.story['pages'][0]['alt'] = '\" onerror=\"alert(1)'
        self.story['pages'][0]['text'] = '</p><iframe src="https://example.com"></iframe>'
        report = self.export()
        content = Path(report['html']).read_text()
        dom = AlbumDOM(content)
        self.assertEqual(dom.tags.count('script'), 1)
        self.assertNotIn('iframe', dom.tags)
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;{{PAGES}}', content)
        self.assertEqual(dom.images[1]['alt'], '\" onerror=\"alert(1)')
        self.assertNotIn('onerror', dom.images[1])

    def test_missing_corrupt_animated_or_remote_image_leaves_no_album(self):
        (self.root / 'bad.jpg').write_text('not a photo')
        frames = [Image.new('RGB', (10, 10), color) for color in ('red', 'blue')]
        frames[0].save(self.root / 'animated.png', save_all=True, append_images=frames[1:])
        for bad in ('missing.jpg', 'bad.jpg', 'animated.png', 'https://example.com/photo.jpg'):
            with self.subTest(bad=bad):
                self.story['pages'][1]['image'] = bad
                with self.assertRaises((AlbumError, PhotoError)):
                    self.export()
                self.assertFalse((self.root / 'album.html').exists())
                self.assertEqual(list(self.root.glob('.album-*')), [])

    def test_existing_output_and_dangling_symlink_are_not_replaced(self):
        path = self.root / 'album.html'
        path.write_text('previous accepted album')
        with self.assertRaises(AlbumError):
            self.export()
        self.assertEqual(path.read_text(), 'previous accepted album')
        path.unlink()
        path.symlink_to(self.root / 'absent')
        with self.assertRaises(AlbumError):
            self.export()
        self.assertTrue(path.is_symlink())

    def test_invalid_story_and_revision_preservation(self):
        for key, bad in [('cover', -1), ('cover', True), ('pages', []), ('title', None), ('reading', 'invalid')]:
            old = self.story.get(key)
            self.story[key] = bad
            with self.subTest(key=key), self.assertRaises(AlbumError):
                self.export()
            if old is None:
                del self.story[key]
            else:
                self.story[key] = old
        self.export('v001.html')
        original = (self.root / 'v001.html').read_bytes()
        self.story['pages'].reverse()
        self.story['title'] = '另一个顺序'
        self.export('v002.html')
        self.assertEqual((self.root / 'v001.html').read_bytes(), original)
        self.assertNotEqual((self.root / 'v002.html').read_bytes(), original)

    def test_cli_from_another_working_directory(self):
        self.manifest.write_text(json.dumps(self.story))
        result = subprocess.run([sys.executable, str(ROOT / 'plog/scripts/album.py'), str(self.manifest), '--output', str(self.root / 'cli.html')], cwd='/', capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['photos'], 2)

    def test_missing_design_never_silently_uses_sample_look(self):
        del self.story['design']
        with self.assertRaisesRegex(AlbumError, 'Add design'):
            self.export()
        self.assertFalse((self.root / 'album.html').exists())

    def test_design_is_preserved_as_data_and_rationale_stays_private(self):
        self.story['design']['rationale'] = 'Private story context and decision notes'
        report = self.export()
        class DesignDOM(HTMLParser):
            def handle_starttag(self, tag, attributes):
                if tag == 'body':
                    self.design = json.loads(dict(attributes)['data-design'])
        parser = DesignDOM()
        content = Path(report['html']).read_text()
        parser.feed(content)
        expected = {k:v for k,v in self.story['design'].items() if k != 'rationale'}
        self.assertEqual(parser.design, expected)
        self.assertNotIn('Private story context', content)

    def test_invalid_design_stops_before_publishing(self):
        from copy import deepcopy
        original = deepcopy(self.story['design'])
        changes = [('material', 'url(https://example.com)'), ('turn_ms', float('nan')),
                   ('page_margin', True), ('photo_box', [-1, 50, 200, 300]),
                   ('title_box', [0, 0, 700, 100])]
        for field, value in changes:
            self.story['design'] = deepcopy(original)
            self.story['design'][field] = value
            with self.subTest(field=field), self.assertRaises(AlbumError):
                self.export()
            self.assertFalse((self.root / 'album.html').exists())
        for value in ['red; background:url(https://example.com)', original['palette']['cover']]:
            self.story['design'] = deepcopy(original)
            self.story['design']['palette']['cover_text'] = value
            with self.assertRaises(AlbumError):
                self.export()

    def test_another_book_can_choose_smooth_dark_cover_and_no_photo(self):
        self.story['design']['palette'].update(cover='#171922', cover_text='#f8ede0')
        self.story['design'].update(material='smooth', typeface='sans', photo_box=None, turn_ms=650)
        self.assertEqual(validate_design(self.story['design'])['material'], 'smooth')
        self.export()
