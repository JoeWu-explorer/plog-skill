import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from evaluation import new_evaluation, summarize


class EvaluationTests(unittest.TestCase):
    def test_verified_generation_can_wait_for_owner_without_being_untested_or_passed(self):
        evidence = new_evaluation('a' * 40, 'b' * 64)
        evidence['attempts'][0].update(status='awaiting_review', delivery='pass', real_service=True, clean_session=True)
        result = summarize(evidence)
        self.assertEqual(result['awaiting_review'], 1)
        self.assertEqual(result['untested'], 17)
        self.assertEqual(result['passed'], 0)
        self.assertEqual(result['status'], 'not_passed')
        evidence['attempts'][0]['real_service'] = False
        with self.assertRaises(ValueError):
            summarize(evidence)

    def test_unrun_matrix_keeps_eighteen_denominator_and_cannot_pass(self):
        result = summarize(new_evaluation('a' * 40, 'b' * 64))
        self.assertEqual(result['first_generation_total'], 18)
        self.assertEqual(result['untested'], 18)
        self.assertEqual(result['status'], 'not_passed')
        self.assertEqual(result['passed'], 0)

    def test_retry_cannot_erase_failure_or_reduce_denominator(self):
        evidence = new_evaluation('a' * 40, 'b' * 64)
        evidence['attempts'][0]['status'] = 'fail'
        retry = dict(evidence['attempts'][0], attempt=2, status='pass', delivery='pass', real_service=True, clean_session=True, human_reviewer='test reviewer', scores={'composition':4, 'chinese_typography':4, 'atmosphere':4, 'narrative':4, 'save_share_value':4})
        evidence['attempts'].append(retry)
        self.assertEqual(summarize(evidence)['failed'], 1)
        self.assertEqual(summarize(evidence)['passed'], 0)
        evidence['attempts'].pop(1)
        with self.assertRaises(ValueError):
            summarize(evidence)

    def test_tool_return_and_average_scores_do_not_replace_human_review(self):
        evidence = new_evaluation('a' * 40, 'b' * 64)
        evidence['attempts'][0].update(status='pass', delivery='pass', real_service=True, clean_session=True)
        with self.assertRaises(ValueError):
            summarize(evidence)
        evidence['attempts'][0].update(human_reviewer='owner', scores={'composition':5, 'chinese_typography':3, 'atmosphere':5, 'narrative':5, 'save_share_value':5})
        with self.assertRaises(ValueError):
            summarize(evidence)

    def test_complete_matrix_passes_but_one_misdelivery_blocks_release(self):
        from evaluation import DIMENSIONS
        evidence = new_evaluation('a' * 40, 'b' * 64)
        evidence['environment'] = dict.fromkeys(('codex', 'platform', 'python', 'image_service', 'service_version_or_unavailable'), 'test fixture')
        for row in evidence['attempts']:
            row.update(status='pass', delivery='pass', real_service=True, clean_session=True, human_reviewer='test reviewer', scores=dict.fromkeys(DIMENSIONS, 4))
        for key in ('behaviors', 'revisions'):
            evidence[key] = dict.fromkeys(evidence[key], 'pass')
        self.assertEqual(summarize(evidence)['status'], 'pass')
        evidence['attempts'][0]['misdelivered'] = True
        self.assertEqual(summarize(evidence)['status'], 'not_passed')

    def test_delivered_retry_must_also_pass_every_human_dimension(self):
        from evaluation import DIMENSIONS
        evidence = new_evaluation('a' * 40, 'b' * 64)
        retry = dict(evidence['attempts'][0], attempt=2, status='pass', delivery='pass', real_service=True, clean_session=True, human_reviewer='test reviewer', scores=dict.fromkeys(DIMENSIONS, 2))
        evidence['attempts'].append(retry)
        with self.assertRaises(ValueError):
            summarize(evidence)
