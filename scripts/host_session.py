"""Run an explicitly requested private Codex product test in an ephemeral session.

This is a development harness, never part of the installed skill. It preserves
actual host events and does not decide visual quality or human acceptance.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import queue
import subprocess
import threading
import time
from typing import Any


def run_case(codex: Path, case: dict[str, Any], destination: Path, *, timeout: int = 900) -> dict[str, Any]:
    repository = Path(__file__).resolve().parents[1]
    if destination.resolve().is_relative_to(repository):
        raise ValueError('Host evidence and private outputs must stay outside the repository.')
    for item in case.get('sources', []):
        if hashlib.sha256(Path(item['path']).read_bytes()).hexdigest() != item['sha256']:
            raise ValueError('Source changed since the test plan was fixed.')
    destination.mkdir(mode=0o700, parents=True, exist_ok=False)
    (destination / 'case.json').write_text(json.dumps(case, ensure_ascii=False, indent=2))
    messages: queue.Queue[dict[str, Any] | None] = queue.Queue()
    started = time.monotonic()
    result: dict[str, Any] = {'status': 'running', 'clean_session': True, 'image_calls': [], 'messages': [], 'tool_requests': [], 'turns': []}
    with (destination / 'host-stderr.txt').open('w') as errors, (destination / 'events.jsonl').open('w') as events:
        process = subprocess.Popen([str(codex), 'app-server', '--stdio'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=errors, text=True, bufsize=1)

        def reader() -> None:
            assert process.stdout is not None
            for line in process.stdout:
                try:
                    messages.put(json.loads(line))
                except json.JSONDecodeError:
                    continue
            messages.put(None)

        threading.Thread(target=reader, daemon=True).start()

        def send(value: dict[str, Any]) -> None:
            assert process.stdin is not None
            process.stdin.write(json.dumps(value, ensure_ascii=False) + '\n')
            process.stdin.flush()

        def receive() -> dict[str, Any]:
            remaining = timeout - (time.monotonic() - started)
            if remaining <= 0:
                raise TimeoutError('Target host test timed out; no automatic retry.')
            message = messages.get(timeout=remaining)
            if message is None:
                raise RuntimeError('Target host exited before completion.')
            # The savedPath is sufficient; never duplicate base64 image data in logs.
            item = message.get('params', {}).get('item', {})
            if item.get('type') == 'imageGeneration' and item.get('result'):
                item['result'] = '[image data omitted; see savedPath]'
            events.write(json.dumps(message, ensure_ascii=False) + '\n')
            events.flush()
            return message

        def response(number: int) -> dict[str, Any]:
            while True:
                message = receive()
                if message.get('id') == number:
                    if 'error' in message:
                        raise RuntimeError(str(message['error']))
                    return message['result']

        try:
            send({'id': 1, 'method': 'initialize', 'params': {'clientInfo': {'name': 'photo-dialogue-product-test', 'version': '1.0'}, 'capabilities': {'experimentalApi': True}}})
            result['host'] = response(1)
            send({'method': 'initialized', 'params': {}})
            params: dict[str, Any] = {'cwd': str(destination), 'ephemeral': True, 'sandbox': 'workspace-write', 'approvalPolicy': 'never'}
            if case.get('writable_roots'):
                params['config'] = {'sandbox_workspace_write.writable_roots': case['writable_roots']}
            if case.get('developer_instructions'):
                params['developerInstructions'] = case['developer_instructions']
            if case.get('dynamic_tools'):
                params['dynamicTools'] = case['dynamic_tools']
            send({'id': 2, 'method': 'thread/start', 'params': params})
            thread = response(2)
            result['thread_id'] = thread['thread']['id']
            result['model'] = thread.get('model')
            for index, prompt in enumerate(case['prompts']):
                inputs: list[dict[str, Any]] = [{'type': 'text', 'text': prompt.replace('{work}', str(destination / 'work')), 'text_elements': []}]
                if index == 0:
                    inputs += [{'type': 'localImage', 'path': source['path']} for source in case.get('sources', []) if source.get('attach', True)]
                send({'id': 10 + index, 'method': 'turn/start', 'params': {'threadId': result['thread_id'], 'input': inputs}})
                response(10 + index)
                while True:
                    message = receive()
                    method = message.get('method')
                    data = message.get('params', {})
                    if method == 'item/completed':
                        item = data['item']
                        if item['type'] == 'imageGeneration':
                            result['image_calls'].append(item)
                        elif item['type'] == 'agentMessage':
                            result['messages'].append(item.get('text', ''))
                    elif method == 'item/tool/call':
                        result['tool_requests'].append(data)
                        responses = case.get('tool_responses', [])
                        call_index = len(result['tool_requests']) - 1
                        answer = responses[min(call_index, len(responses) - 1)] if responses else {'contentItems': [{'type': 'inputText', 'text': 'Test adapter unavailable.'}], 'success': False}
                        send({'id': message['id'], 'result': answer})
                    elif 'id' in message and method:
                        # A test requiring user input is recorded, never silently answered.
                        result['tool_requests'].append(data)
                        raise RuntimeError('Host requested interactive input; inspect the private event log.')
                    elif method == 'turn/completed':
                        result['turns'].append(data['turn']['status'])
                        break
            result['status'] = 'completed' if all(turn == 'completed' for turn in result['turns']) else 'failed'
        except (TimeoutError, queue.Empty, RuntimeError, OSError) as exc:
            result['status'] = 'incomplete'
            result['error'] = str(exc)
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            result['elapsed_seconds'] = round(time.monotonic() - started, 2)
            result['cost'] = None
            result['quality'] = 'not assessed by harness'
            (destination / 'result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
            (destination / 'messages.md').write_text('\n\n'.join(result['messages']))
            for path in destination.glob('*'):
                if path.is_file():
                    os.chmod(path, 0o600)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codex', type=Path, required=True)
    parser.add_argument('--case', type=Path, required=True, help='Explicit private test plan with source hashes and user prompts')
    parser.add_argument('--destination', type=Path, required=True)
    args = parser.parse_args()
    try:
        result = run_case(args.codex, json.loads(args.case.read_text()), args.destination)
        print(json.dumps({key: result[key] for key in ('status', 'elapsed_seconds', 'quality')}, ensure_ascii=False))
    except (OSError, ValueError) as exc:
        parser.exit(1, f'{exc}\n')


if __name__ == '__main__':
    main()
