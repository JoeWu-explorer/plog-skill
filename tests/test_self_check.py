import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'photo-dialogue' / 'scripts'))
from self_check import check


class SelfCheckTests(unittest.TestCase):
    def test_real_codec_probe_does_not_claim_host_generation_permission(self):
        with tempfile.TemporaryDirectory() as folder:
            report = check(Path(folder))
            self.assertEqual(report['local'], 'pass')
            self.assertEqual(report['host_image_service'], 'unverified')
            self.assertEqual(set(report['formats']), {'JPEG', 'PNG', 'WEBP'})
            self.assertEqual(list(Path(folder).iterdir()), [])

    def test_unwritable_or_missing_directory_reports_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            result = check(Path(folder) / 'missing')
            self.assertEqual(result['local'], 'fail')
            self.assertEqual(result['host_image_service'], 'unverified')
