import hashlib
import json
from pathlib import Path
import sys
import tempfile
import time
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from host_session import run_case


class HostSessionTests(unittest.TestCase):
    def host(self, root, *, delete_skill=False, hold_pipe=False):
        skill = root / 'skill'
        skill.mkdir()
        (skill / 'SKILL.md').write_text('test skill')
        (skill / 'INSTALL-MANIFEST.json').write_text(json.dumps({'files': {'SKILL.md': hashlib.sha256(b'test skill').hexdigest()}}))
        executable = root / 'fake-codex'
        executable.write_text(f'''#!{sys.executable}
import json,sys,pathlib,subprocess
if {hold_pipe!r}:subprocess.Popen([sys.executable,'-c','import time; time.sleep(7)'])

def send(value):
 print(json.dumps(value),flush=True)
for line in sys.stdin:
 request=json.loads(line);method=request.get('method')
 if method=='initialize':send({{'id':request['id'],'result':{{'userAgent':'controlled-test'}}}})
 elif method=='thread/start':send({{'id':request['id'],'result':{{'thread':{{'id':'thread-test'}},'model':'test-double'}}}})
 elif method=='turn/start':
  send({{'method':'item/completed','params':{{'item':{{'type':'imageGeneration','id':'image-test','savedPath':None,'result':'','status':'completed'}}}}}})
  send({{'method':'item/completed','params':{{'item':{{'type':'agentMessage','text':'Test output, not a real image.'}}}}}})
  if {delete_skill!r}:pathlib.Path({str(skill / 'SKILL.md')!r}).unlink()
  send({{'id':request['id'],'result':{{'turn':{{'id':'turn-test'}}}}}})
  send({{'method':'turn/completed','params':{{'turn':{{'status':'completed'}}}}}})
''')
        executable.chmod(0o700)
        return executable, {'skill_path': str(skill), 'prompts': ['Controlled protocol test.']}

    def test_events_before_rpc_response_are_counted_and_delivered(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            host, case = self.host(root)
            result = run_case(host, case, root / 'evidence', timeout=5)
            self.assertEqual(result['status'], 'completed')
            self.assertEqual(len(result['image_calls']), 1)
            self.assertEqual(result['messages'], ['Test output, not a real image.'])

    def test_removed_candidate_file_keeps_evidence_and_marks_run_incomplete(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            host, case = self.host(root, delete_skill=True)
            result = run_case(host, case, root / 'evidence', timeout=5)
            self.assertEqual(result['status'], 'incomplete')
            self.assertFalse(result['installed_candidate_unchanged'])
            saved = json.loads((root / 'evidence/result.json').read_text())
            self.assertEqual(saved['status'], 'incomplete')
            self.assertTrue((root / 'evidence/events.jsonl').is_file())

    def test_descendant_holding_stdout_does_not_block_evidence_save(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            host, case = self.host(root, hold_pipe=True)
            started = time.monotonic()
            result = run_case(host, case, root / 'evidence', timeout=3)
            self.assertEqual(result['status'], 'completed')
            self.assertLess(time.monotonic() - started, 4)
            self.assertTrue((root / 'evidence/result.json').is_file())
