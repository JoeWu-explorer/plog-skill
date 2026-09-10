"""Render an agent-authored photo story as one portable, offline HTML album."""
from __future__ import annotations

import argparse
import base64
import html
import io
import json
import math
import os
from pathlib import Path
import re
import tempfile
from typing import Any

from PIL import Image
from photo_files import PhotoError, _decode, sha256

MAX_PAGES = 50
MAX_HTML_BYTES = 64 * 1024 * 1024


class AlbumError(ValueError):
    pass


def _text(value: Any, name: str, *, required: bool = False) -> str:
    if not isinstance(value, str) or (required and not value.strip()):
        raise AlbumError(f'{name} must be {"nonempty " if required else ""}text.')
    if len(value) > 10000:
        raise AlbumError(f'{name} is too long (maximum 10000 characters).')
    return value


def validate_design(value: Any) -> dict[str, Any]:
    """Require an authored design, rather than silently reusing a sample's look."""
    if not isinstance(value, dict):
        raise AlbumError('Add design to the story: choose this book’s appearance from its photos and story first.')
    required = {'rationale', 'palette', 'material', 'typeface', 'title_box',
                'subtitle_box', 'photo_box', 'title_size', 'title_align',
                'page_margin', 'turn_ms', 'hold_seconds'}
    if set(value) != required:
        raise AlbumError('design fields must be: ' + ', '.join(sorted(required)))
    _text(value['rationale'], 'design.rationale', required=True)
    palette = value['palette']
    colors = {'cover', 'cover_text', 'paper', 'ink', 'accent', 'stage', 'stage_edge'}
    if not isinstance(palette, dict) or set(palette) != colors:
        raise AlbumError('design.palette must define: ' + ', '.join(sorted(colors)))
    for name, color in palette.items():
        if not isinstance(color, str) or not re.fullmatch(r'#[0-9a-fA-F]{6}', color):
            raise AlbumError(f'design.palette.{name} must be a six-digit hex color.')
    def luminance(color: str) -> float:
        channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in channels]
        return sum(v * weight for v, weight in zip(linear, (.2126, .7152, .0722)))
    for foreground, background in [('cover_text', 'cover'), ('ink', 'paper')]:
        lo, hi = sorted([luminance(palette[foreground]), luminance(palette[background])])
        if (hi + .05) / (lo + .05) < 4.5:
            raise AlbumError(f'design.palette.{foreground}/{background} needs at least 4.5:1 contrast.')
    for name, options in [('material', ('cloth', 'paper', 'smooth')),
                          ('typeface', ('serif', 'sans', 'handwritten')),
                          ('title_align', ('left', 'center'))]:
        if value[name] not in options:
            raise AlbumError(f'design.{name} must be one of {options}.')
    for name in ('title_box', 'subtitle_box', 'photo_box'):
        box = value[name]
        if name == 'photo_box' and box is None:
            continue
        if not isinstance(box, list) or len(box) != 4 or any(type(n) not in (int, float) or not math.isfinite(n) for n in box):
            raise AlbumError(f'design.{name} must be [x, y, width, height].')
        x, y, width, height = box
        if x < 0 or y < 0 or width <= 0 or height <= 0 or x + width > 600 or y + height > 700:
            raise AlbumError(f'design.{name} must fit within the 600 × 700 cover design area.')
    for name, lo, hi in [('title_size', 24, 96), ('page_margin', 0, 60),
                         ('turn_ms', 500, 2000), ('hold_seconds', 2, 8)]:
        number = value[name]
        if type(number) not in (int, float) or not math.isfinite(number) or not lo <= number <= hi:
            raise AlbumError(f'design.{name} must be between {lo} and {hi}.')
    return value


def read_story(path: Path) -> dict[str, Any]:
    """Resolve only explicit local photo paths, relative to the story file."""
    story = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(story, dict) or story.get('schema_version') != 1:
        raise AlbumError('The story must be an object with schema_version: 1.')
    _text(story.get('title'), 'title', required=True)
    for name in ('subtitle', 'intro', 'ending', 'intro_title', 'ending_title'):
        _text(story.get(name, ''), name)
    validate_design(story.get('design'))
    pages = story.get('pages')
    if not isinstance(pages, list) or not 2 <= len(pages) <= MAX_PAGES:
        raise AlbumError(f'An album needs 2–{MAX_PAGES} photos.')
    cover = story.get('cover', 0)
    if type(cover) is not int or not 0 <= cover < len(pages):
        raise AlbumError('cover must be a zero-based index of a photo in pages.')
    if story.get('reading', 'book') not in ('book', 'scroll', 'pages'):
        raise AlbumError('reading must be book (legacy scroll/pages files are also accepted).')
    for index, page in enumerate(pages):
        if not isinstance(page, dict):
            raise AlbumError(f'pages[{index}] must be an object.')
        for name in ('image', 'title', 'alt'):
            _text(page.get(name), f'pages[{index}].{name}', required=True)
        for name in ('text', 'chapter'):
            _text(page.get(name, ''), f'pages[{index}].{name}')
        raw = page['image']
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', raw) or raw.startswith('//'):
            raise AlbumError('Use local photo paths; remote URLs are not fetched.')
        source = Path(raw).expanduser()
        page['source'] = (path.parent / source).resolve()
        if not page['source'].is_file():
            raise AlbumError(f'Photo {index + 1} is missing; restore it before exporting.')
    return story


def _photo(source: Path) -> tuple[str, int, int]:
    before = sha256(source)
    clean, _ = _decode(source)
    clean.thumbnail((2400, 2400), Image.Resampling.LANCZOS)
    output = io.BytesIO()
    clean.save(output, format='WEBP', quality=92, method=4)
    if before != sha256(source):
        raise AlbumError('A photo changed during export; export again from stable files.')
    return base64.b64encode(output.getvalue()).decode('ascii'), *clean.size


def render_story(story: dict[str, Any]) -> str:
    esc = html.escape
    images: dict[Path, tuple[str, int, int]] = {}
    sections = []
    navigation = []
    total = 0
    for index, page in enumerate(story['pages']):
        source = page['source']
        if source not in images:
            images[source] = _photo(source)
        data, width, height = images[source]
        total += len(data)
        if total > MAX_HTML_BYTES:
            raise AlbumError('Album exceeds 64 MiB; split the story into smaller albums.')
        number = index + 1
        chapter = f'<p class="chapter">{esc(page["chapter"])}</p>' if page.get('chapter') else ''
        sections.append(
            f'<section class="spread" id="photo-{number}" aria-labelledby="title-{number}">'
            f'<figure><img src="data:image/webp;base64,{data}" width="{width}" height="{height}" '
            f'alt="{esc(page["alt"], quote=True)}" loading="lazy" decoding="async"></figure>'
            f'<div class="story">{chapter}<h2 id="title-{number}">{esc(page["title"])}</h2>'
            f'<p class="prose">{esc(page.get("text", ""))}</p>'
            f'<span class="folio">{number:02d} / {len(story["pages"]):02d}</span></div></section>'
        )
        navigation.append(f'<a href="#photo-{number}"><span>{number:02d}</span>{esc(page["title"])}</a>')
    cover_page = story['pages'][story.get('cover', 0)]
    data, width, height = images[cover_page['source']]
    values = {
        'TITLE': esc(story['title']),
        'SUBTITLE': esc(story.get('subtitle', '')),
        'INTRO': esc(story.get('intro', '')),
        'ENDING': esc(story.get('ending', '')),
        'COUNT': str(len(story['pages'])),
        'COVER': f'<img src="data:image/webp;base64,{data}" width="{width}" height="{height}" alt="{esc(cover_page["alt"], quote=True)}" fetchpriority="high">',
        'CONTENTS': ''.join(navigation),
        'PAGES': '\n'.join(sections),
        'READING': 'book',
        'DESIGN': esc(json.dumps({key: value for key, value in validate_design(story.get('design')).items()
                                 if key != 'rationale'}, ensure_ascii=False), quote=True),
        'INTROTITLE': esc(story.get('intro_title', '序言'), quote=True),
        'ENDINGTITLE': esc(story.get('ending_title', '结语'), quote=True),
    }
    template = (Path(__file__).resolve().parents[1] / 'assets' / 'album.html.txt').read_text(encoding='utf-8')
    # One substitution pass: captions containing template-like text stay literal.
    return re.sub(r'\{\{([A-Z]+)\}\}', lambda match: values[match[1]], template)


def export_album(story_path: Path, destination: Path) -> dict[str, Any]:
    story_path, destination = Path(story_path), Path(destination)
    if destination.suffix.lower() != '.html':
        raise AlbumError('Choose an output filename ending in .html.')
    if destination.exists() or destination.is_symlink():
        raise AlbumError('Output already exists; choose a new filename to preserve earlier versions.')
    story = read_story(story_path)
    rendered = render_story(story).encode('utf-8')
    if len(rendered) > MAX_HTML_BYTES:
        raise AlbumError('Album exceeds 64 MiB; split the story into smaller albums.')
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.album-', dir=destination.parent)
    staged = Path(temporary)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(rendered)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(staged, destination)
    except BaseException:
        try:
            if destination.samefile(staged):
                destination.unlink()
        except FileNotFoundError:
            pass
        raise
    finally:
        staged.unlink(missing_ok=True)
    return {'html': str(destination.resolve()), 'photos': len(story['pages']), 'bytes': len(rendered), 'sha256': sha256(destination)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('story', type=Path, help='Agent-authored JSON story; image paths are relative to this file')
    parser.add_argument('--output', type=Path, required=True, help='New standalone .html file')
    args = parser.parse_args()
    try:
        print(json.dumps(export_album(args.story, args.output), ensure_ascii=False))
    except (AlbumError, PhotoError, OSError, ValueError) as exc:
        parser.exit(1, f'{exc}\n')


if __name__ == '__main__':
    main()
