import tempfile
import unittest
from pathlib import Path

from agent.verification.completeness_verifier import (
    AndroidCompletenessVerifier,
    CompletenessStatus,
)


class AndroidCompletenessVerifierTests(unittest.TestCase):
    def test_real_feature_source_is_verified(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "MainActivity.java"
            source.write_text(
                "Button add = button(\"Add\");\nadd.setOnClickListener(v -> calculate());\n",
                encoding="utf-8",
            )
            report = AndroidCompletenessVerifier().verify_project("demo", root)
            self.assertEqual(report.status, CompletenessStatus.VERIFIED)

    def test_placeholder_source_is_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "MainActivity.java"
            source.write_text(
                "TextView status = label(\"Project shell ready.\");\n",
                encoding="utf-8",
            )
            report = AndroidCompletenessVerifier().verify_project("demo", root)
            self.assertEqual(report.status, CompletenessStatus.BLOCKED)
            self.assertTrue(report.findings)

    def test_missing_project_is_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            missing = Path(temp) / "missing"
            report = AndroidCompletenessVerifier().verify_project("demo", missing)
            self.assertEqual(report.status, CompletenessStatus.BLOCKED)


if __name__ == "__main__":
    unittest.main()
