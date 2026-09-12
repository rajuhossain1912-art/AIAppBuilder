import tempfile
import unittest
from pathlib import Path

from agent.verification import AndroidAccessibilityVerifier, VerificationStatus


class AndroidAccessibilityVerifierTests(unittest.TestCase):
    def test_accessible_interactive_source_is_statistically_verified(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "MainActivity.java"
            source.write_text(
                "Button button = new Button(this);\nbutton.setContentDescription(\"Calculate\");\n",
                encoding="utf-8",
            )
            report = AndroidAccessibilityVerifier().verify_source("demo", source)
            self.assertEqual(report.final_status, VerificationStatus.VERIFIED)

    def test_interactive_source_without_label_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "MainActivity.java"
            source.write_text("Button button = new Button(this);\n", encoding="utf-8")
            report = AndroidAccessibilityVerifier().verify_source("demo", source)
            self.assertEqual(report.final_status, VerificationStatus.FAILED)

    def test_missing_source_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "missing.java"
            report = AndroidAccessibilityVerifier().verify_source("demo", source)
            self.assertEqual(report.final_status, VerificationStatus.FAILED)


if __name__ == "__main__":
    unittest.main()
