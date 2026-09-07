"""Optional provider-neutral image edit/vision transport; no implicit network calls."""
from __future__ import annotations

import argparse
import base64
import binascii
from dataclasses import dataclass
import io
import json
import os
from pathlib import Path
import tempfile
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
import uuid

from photo_files import PhotoError, export_png, prepare, sha256, verify_png

MAX_IMAGE = 32 * 1024 * 1024
MAX_RESPONSE = 64 * 1024 * 1024


class BackendError(ValueError):
    pass


@dataclass(frozen=True)
class Endpoint:
    base_url: str
    model: str
    key: str


def endpoint(kind: str) -> Endpoint:
    prefix = 'PD_' + kind.upper()
    url, model, key = (os.environ.get(prefix + suffix, '').strip()
                       for suffix in ('_BASE_URL', '_MODEL', '_API_KEY'))
    if not url or not model:
        raise BackendError(f'Set {prefix}_BASE_URL and {prefix}_MODEL for the selected provider.')
    parsed = urlsplit(url)
    local = parsed.hostname in ('localhost', '127.0.0.1', '::1')
    if (parsed.scheme != 'https' and not (parsed.scheme == 'http' and local)) or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise BackendError(f'{prefix}_BASE_URL must be HTTPS (or loopback HTTP), without credentials, query or fragment.')
    if not key and not local:
        raise BackendError(f'Set {prefix}_API_KEY in the process environment; keep it outside the skill.')
    if any('\r' in value or '\n' in value for value in (url, model, key)):
        raise BackendError('Provider settings must be single-line values.')
    return Endpoint(url.rstrip('/'), model, key)


def doctor() -> dict[str, Any]:
    result: dict[str, Any] = {'network_calls': 0, 'native_tools': 'inspect_in_agent', 'backends': {}}
    for kind in ('image', 'vision'):
        try:
            config = endpoint(kind)
            result['backends'][kind] = {'status': 'configured_not_tested', 'service': config.base_url, 'model': config.model}
        except (BackendError, ValueError):
            result['backends'][kind] = {'status': 'missing_or_invalid', 'required': [f'PD_{kind.upper()}_{suffix}' for suffix in ('BASE_URL', 'MODEL', 'API_KEY')]}
    return result


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        raise BackendError('Provider redirected the request; verify the configured endpoint before trying again.')


def post(config: Endpoint, route: str, body: bytes, content_type: str, timeout: int) -> dict[str, Any]:
    headers = {'Content-Type': content_type, 'Accept': 'application/json'}
    if config.key:
        headers['Authorization'] = 'Bearer ' + config.key
    request = Request(config.base_url + route, data=body, headers=headers, method='POST')
    try:
        # One request, no retries, no redirects carrying credentials or images elsewhere.
        with build_opener(NoRedirect()).open(request, timeout=timeout) as response:
            raw = response.read(MAX_RESPONSE + 1)
        if len(raw) > MAX_RESPONSE:
            raise BackendError('Provider response exceeds the size limit.')
        value = json.loads(raw)
        if not isinstance(value, dict):
            raise BackendError('Provider returned an unsupported response.')
        return value
    except HTTPError as exc:
        raise BackendError(f'Provider returned HTTP {exc.code}; no retry was made.') from None
    except (URLError, TimeoutError, OSError):
        raise BackendError('Provider request failed or timed out; result may be unknown. No retry was made.') from None
    except (ValueError, UnicodeError) as exc:
        if isinstance(exc, BackendError):
            raise
        raise BackendError('Provider returned invalid JSON.') from None


def prompt_text(path: Path) -> str:
    if path.stat().st_size > 100_000:
        raise BackendError('Prompt file exceeds 100 KB.')
    value = path.read_text(encoding='utf-8')
    if not value.strip():
        raise BackendError('Prompt must not be empty.')
    return value


def clean_bytes(path: Path, workspace: Path) -> bytes:
    with prepare(path, workspace) as clean:
        if clean.stat().st_size > MAX_IMAGE:
            raise BackendError('Prepared image exceeds 32 MiB; explicitly choose a smaller copy.')
        return clean.read_bytes()


def edit(source: Path, prompt: str, output: Path, *, send: bool, timeout: int = 180) -> dict[str, Any]:
    if not send:
        raise BackendError('Sending requires --send after current image, service and purpose are authorized.')
    config = endpoint('image')
    if output.exists() or output.is_symlink() or output.resolve() == source.resolve():
        raise BackendError('Choose a new candidate path; existing files and the source are preserved.')
    before = sha256(source)
    with tempfile.TemporaryDirectory(prefix='.plog-api-', dir=output.parent) as directory:
        root = Path(directory)
        pixels = clean_bytes(source, root)
        boundary = 'plog-' + uuid.uuid4().hex
        body = io.BytesIO()
        for name, value in (('model', config.model), ('prompt', prompt), ('n', '1')):
            body.write(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
            body.write(value.encode('utf-8') + b'\r\n')
        body.write(f'--{boundary}\r\nContent-Disposition: form-data; name="image"; filename="source.png"\r\nContent-Type: image/png\r\n\r\n'.encode())
        body.write(pixels + f'\r\n--{boundary}--\r\n'.encode())
        response = post(config, '/images/edits', body.getvalue(), 'multipart/form-data; boundary=' + boundary, timeout)
        try:
            rows = response['data']
            if not isinstance(rows, list) or len(rows) != 1 or not isinstance(rows[0]['b64_json'], str):
                raise ValueError
            decoded = base64.b64decode(rows[0]['b64_json'], validate=True)
            if not decoded or len(decoded) > MAX_IMAGE:
                raise ValueError
        except (KeyError, TypeError, ValueError, binascii.Error):
            raise BackendError('Expected one base64 image in data[0].b64_json; URL-only responses are not downloaded.') from None
        if sha256(source) != before:
            raise BackendError('Source changed during generation; candidate was not published.')
        raw = root / 'response.png'
        raw.write_bytes(decoded)
        export_png(raw, output, source=source)
    return {'status': 'candidate_needs_visual_review', 'path': str(output.resolve()), **verify_png(output)}


def analyze(images: list[Path], prompt: str, *, send: bool, workspace: Path, timeout: int = 180) -> dict[str, Any]:
    if not send:
        raise BackendError('Sending requires --send after current images, vision service and purpose are authorized.')
    if not 1 <= len(images) <= 3:
        raise BackendError('Analyze one image, or compare source, selected version and candidate (up to three).')
    config = endpoint('vision')
    content: list[dict[str, Any]] = [{'type': 'text', 'text': prompt}]
    total = 0
    with tempfile.TemporaryDirectory(prefix='.plog-vision-', dir=workspace) as directory:
        for index, path in enumerate(images):
            pixels = clean_bytes(path, Path(directory))
            total += len(pixels)
            if total > MAX_IMAGE:
                raise BackendError('Combined prepared images exceed 32 MiB.')
            content.extend([{'type': 'text', 'text': f'Image {index + 1}'}, {'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,' + base64.b64encode(pixels).decode('ascii')}}])
        body = json.dumps({'model': config.model, 'messages': [{'role': 'user', 'content': content}]}, ensure_ascii=False).encode('utf-8')
        response = post(config, '/chat/completions', body, 'application/json', timeout)
    try:
        observation = response['choices'][0]['message']['content']
        if not isinstance(observation, str) or not observation.strip():
            raise ValueError
    except (KeyError, TypeError, ValueError, IndexError):
        raise BackendError('Vision provider returned no usable observation.') from None
    return {'status': 'observation_not_acceptance', 'observation': observation}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='operation', required=True)
    commands.add_parser('doctor')
    for name in ('edit', 'analyze'):
        sub = commands.add_parser(name)
        sub.add_argument('--prompt-file', type=Path, required=True)
        sub.add_argument('--send', action='store_true')
        sub.add_argument('--timeout', type=int, default=180)
        if name == 'edit':
            sub.add_argument('--image', type=Path, required=True)
            sub.add_argument('--output', type=Path, required=True)
        else:
            sub.add_argument('--images', type=Path, nargs='+', required=True)
            sub.add_argument('--workspace', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.operation == 'doctor':
            result = doctor()
        else:
            if not 1 <= args.timeout <= 600:
                raise BackendError('Timeout must be between 1 and 600 seconds.')
            prompt = prompt_text(args.prompt_file)
            if args.operation == 'edit':
                result = edit(args.image, prompt, args.output, send=args.send, timeout=args.timeout)
            else:
                result = analyze(args.images, prompt, send=args.send, workspace=args.workspace, timeout=args.timeout)
        print(json.dumps(result, ensure_ascii=False))
    except BackendError as exc:
        parser.exit(1, f'{exc}\n')
    except (PhotoError, OSError, ValueError):
        # Provider responses, credentials and private prompt/path details stay out of errors.
        parser.exit(1, 'Image operation failed. Check settings, supported response format, input and output; no automatic retry.\n')


if __name__ == '__main__':
    main()
