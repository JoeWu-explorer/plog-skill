"""Transport contract tests use an in-process server, never a paid image provider."""
import base64
from contextlib import contextmanager
from email.parser import BytesParser
from email.policy import default
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

from PIL import Image, PngImagePlugin

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'plog/scripts'))
from image_backend import BackendError, analyze, doctor, edit, endpoint, post
from photo_files import PhotoError, sha256, verify_png
from revision_record import append, delivery


@contextmanager
def provider():
    requests = []
    state = {'status': 200, 'response': {}}
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            body = self.rfile.read(int(self.headers['Content-Length']))
            requests.append((self.path, dict(self.headers), body))
            self.send_response(state['status'])
            if state['status'] == 302:
                self.send_header('Location', '/redirected')
            self.end_headers()
            self.wfile.write(json.dumps(state['response']).encode())
        def log_message(self, *args):
            pass
    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    thread = threading.Thread(target=lambda: server.serve_forever(poll_interval=0.01), daemon=True)
    thread.start()
    try:
        yield f'http://127.0.0.1:{server.server_port}/v1', requests, state
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def png_bytes(metadata=False):
    stream = io.BytesIO()
    # Synthetic landscape fixture; no human photo or personal data.
    image = Image.new('RGB', (40, 30), '#79bad0')
    info = PngImagePlugin.PngInfo()
    if metadata:
        info.add_text('private', 'location-device-marker')
    image.save(stream, format='PNG', pnginfo=info)
    return stream.getvalue()


class ImageBackendTests(unittest.TestCase):
    def test_doctor_is_offline_does_not_claim_service_works_or_expose_key(self):
        env = {'PD_IMAGE_BASE_URL': 'https://images.example/v1', 'PD_IMAGE_MODEL': 'editor', 'PD_IMAGE_API_KEY': 'private-test-key'}
        with patch.dict(os.environ, env, clear=True), patch('image_backend.post') as request:
            result = doctor()
            self.assertEqual(result['network_calls'], 0)
            self.assertEqual(result['backends']['image']['status'], 'configured_not_tested')
            self.assertEqual(result['backends']['vision']['status'], 'missing_or_invalid')
            self.assertNotIn('private-test-key', json.dumps(result))
            request.assert_not_called()

    def test_no_send_switch_never_contacts_service(self):
        with patch('image_backend.post') as request:
            with self.assertRaises(BackendError):
                edit(Path('missing.png'), 'test', Path('new.png'), send=False)
            with self.assertRaises(BackendError):
                analyze([Path('missing.png')], 'test', send=False, workspace=Path('.'))
            request.assert_not_called()

    def test_rejects_credentials_in_url_and_remote_http(self):
        for url in ('http://images.example/v1', 'https://user:secret@images.example/v1', 'https://images.example/v1?key=secret', 'https://images.example/v1#secret'):
            with self.subTest(url=url), patch.dict(os.environ, {'PD_IMAGE_BASE_URL':url, 'PD_IMAGE_MODEL':'test', 'PD_IMAGE_API_KEY':'secret'}):
                with self.assertRaises(BackendError):
                    endpoint('image')

    def test_real_cli_edit_sends_clean_photo_and_only_writes_candidate(self):
        with tempfile.TemporaryDirectory() as folder, provider() as (url, calls, state):
            root = Path(folder)
            source = root / 'coast.png'
            source.write_bytes(png_bytes(metadata=True))
            original = sha256(source)
            prompt = root / 'prompt.txt'
            prompt.write_text('海边 Plog，保留海岸线。')
            output = root / 'candidate.png'
            state['response'] = {'data':[{'b64_json':base64.b64encode(png_bytes(metadata=True)).decode()}]}
            env = dict(os.environ, PD_IMAGE_BASE_URL=url, PD_IMAGE_MODEL='fixture-editor', PD_IMAGE_API_KEY='fixture-key')
            result = subprocess.run([sys.executable, str(ROOT/'plog/scripts/image_backend.py'), 'edit', '--image', str(source), '--prompt-file', str(prompt), '--output', str(output), '--send'], env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['status'], 'candidate_needs_visual_review')
            self.assertEqual(sha256(source), original)
            verify_png(output)
            self.assertFalse((root/'revision.json').exists())
            self.assertEqual(len(calls), 1)
            route, headers, body = calls[0]
            self.assertEqual(route, '/v1/images/edits')
            self.assertEqual(headers['Authorization'], 'Bearer fixture-key')
            message = BytesParser(policy=default).parsebytes(('Content-Type: '+headers['Content-Type']+'\r\n\r\n').encode()+body)
            parts = {part.get_param('name', header='content-disposition'):part.get_payload(decode=True) for part in message.iter_parts()}
            self.assertEqual(parts['prompt'].decode(), prompt.read_text())
            self.assertEqual(parts['n'], b'1')
            self.assertEqual(parts['model'], b'fixture-editor')
            with Image.open(io.BytesIO(parts['image'])) as image:
                self.assertFalse(image.info)
            self.assertNotIn(b'location-device-marker', body)
            self.assertFalse(list(root.glob('.plog-*')))

    def test_vision_compares_images_together_without_treating_text_as_acceptance(self):
        with tempfile.TemporaryDirectory() as folder, provider() as (url, calls, state):
            root = Path(folder)
            source = root/'street.png'; source.write_bytes(png_bytes(metadata=True))
            state['response'] = {'choices':[{'message':{'content':'Image 2 has an altered roof; uncertain signage.'}}]}
            with patch.dict(os.environ, {'PD_VISION_BASE_URL':url, 'PD_VISION_MODEL':'fixture-vision', 'PD_VISION_API_KEY':''}):
                result = analyze([source, source, source], 'Compare source, base, candidate.', send=True, workspace=root)
            self.assertEqual(result['status'], 'observation_not_acceptance')
            self.assertIn('altered roof', result['observation'])
            payload = json.loads(calls[0][2])
            self.assertEqual(calls[0][0], '/v1/chat/completions')
            images = [part for part in payload['messages'][0]['content'] if part['type']=='image_url']
            self.assertEqual(len(images), 3)
            for part in images:
                with Image.open(io.BytesIO(base64.b64decode(part['image_url']['url'].split(',')[1]))) as image:
                    self.assertFalse(image.info)
            self.assertFalse(list(root.glob('.plog-*')))

    def test_http_failures_and_redirects_are_not_retried_or_logged(self):
        with provider() as (url, calls, state), patch.dict(os.environ, {'PD_IMAGE_BASE_URL':url, 'PD_IMAGE_MODEL':'test', 'PD_IMAGE_API_KEY':''}):
            for status in (429, 500, 302):
                state.update(status=status, response={'error':'private-key-and-prompt'})
                with self.assertRaises(BackendError) as error:
                    post(endpoint('image'), '/images/edits', b'x', 'application/json', 1)
                self.assertNotIn('private-key-and-prompt', str(error.exception))
            self.assertEqual(len(calls), 3)
            self.assertTrue(all(call[0]=='/v1/images/edits' for call in calls))

    def test_existing_output_and_bad_provider_result_preserve_files(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder); source=root/'pet.png'; source.write_bytes(png_bytes())
            output=root/'candidate.png'; output.write_bytes(b'keep')
            with patch.dict(os.environ, {'PD_IMAGE_BASE_URL':'http://localhost/v1','PD_IMAGE_MODEL':'test','PD_IMAGE_API_KEY':''}), patch('image_backend.post') as request:
                with self.assertRaises(BackendError):
                    edit(source, 'caption', output, send=True)
                request.assert_not_called()
                self.assertEqual(output.read_bytes(), b'keep')
                output.unlink()
                for response in ({'data':[{'url':'https://example/image.png'}]}, {'data':[{'b64_json':'invalid'}]}, {'data':[{'b64_json':base64.b64encode(b'not an image').decode()}]}):
                    request.return_value=response
                    with self.assertRaises((BackendError, PhotoError)):
                        edit(source,'caption',output,send=True)
                    self.assertFalse(output.exists())
                self.assertFalse(list(root.glob('.plog-*')))

    def test_changed_source_during_generation_is_not_published(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder); source=root/'coast.png'; source.write_bytes(png_bytes())
            def changed(*args):
                Image.new('RGB',(20,20),'red').save(source)
                return {'data':[{'b64_json':base64.b64encode(png_bytes()).decode()}]}
            with patch.dict(os.environ, {'PD_IMAGE_BASE_URL':'http://localhost/v1','PD_IMAGE_MODEL':'test','PD_IMAGE_API_KEY':''}), patch('image_backend.post',side_effect=changed):
                with self.assertRaises(BackendError):
                    edit(source,'caption',root/'candidate.png',send=True)
                self.assertFalse((root/'candidate.png').exists())

    def test_timeout_is_one_request_and_keeps_output_absent(self):
        from image_backend import Endpoint
        with patch('image_backend.build_opener') as opener:
            opener.return_value.open.side_effect=TimeoutError('private request details')
            with self.assertRaises(BackendError) as error:
                post(Endpoint('http://localhost/v1','test','secret'),'/images/edits',b'private prompt','application/json',1)
            self.assertIn('unknown',str(error.exception))
            self.assertNotIn('private request details',str(error.exception))
            self.assertEqual(opener.return_value.open.call_count,1)

    def test_narrator_only_and_silent_plog_keep_independent_revisions(self):
        # This verifies the file model; it does not simulate visual acceptance.
        from revision_record import select, recover
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            for scene in ('landscape','street','still-life','pet'):
                source=root/(scene+'.png'); source.write_bytes(png_bytes())
                work=root/scene
                version={'change_target':'Plog caption','voice_elements':[{'text':'沿着海风慢慢走','kind':'narration','attribution':'narrator'}],'visual_intent':'preserve scene geometry'}
                original=sha256(source)
                append(work,source=source,source_sha256=original,candidate=source,version=version)
                silent=dict(version,change_target='remove caption',voice_elements=[])
                append(work,source=source,source_sha256=original,candidate=source,version=silent,parent_id='v001')
                self.assertEqual(select(work,'v001')['voice_elements'],version['voice_elements'])
                self.assertEqual(select(work)['voice_elements'],[])
                self.assertEqual(recover(work,source=source,version_id='v001')['version']['id'],'v001')
                self.assertTrue(Path(delivery(work)['image']).is_file())
                self.assertEqual(sha256(source),original)
