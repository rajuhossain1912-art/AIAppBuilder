from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from agent.security.privacy_guard import PrivacyDecision, PrivacyGuard


class PrivacyGuardTests(unittest.TestCase):
    def test_unnecessary_disclosure_is_denied(self):
        guard = PrivacyGuard()
        decision = guard.decide_disclosure(
            data_category="client data",
            purpose="analytics",
            recipient="external service",
            necessary=False,
            user_approved=True,
        )
        self.assertEqual(decision, PrivacyDecision.DENY)

    def test_necessary_disclosure_requires_approval(self):
        guard = PrivacyGuard()
        decision = guard.decide_disclosure(
            data_category="project data",
            purpose="approved API operation",
            recipient="approved service",
            necessary=True,
            user_approved=False,
        )
        self.assertEqual(decision, PrivacyDecision.REQUIRE_APPROVAL)

    def test_approved_necessary_disclosure_is_allowed(self):
        guard = PrivacyGuard()
        decision = guard.decide_disclosure(
            data_category="project data",
            purpose="approved API operation",
            recipient="approved service",
            necessary=True,
            user_approved=True,
        )
        self.assertEqual(decision, PrivacyDecision.ALLOW)

    def test_sensitive_data_with_network_egress_is_blocked(self):
        guard = PrivacyGuard()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "MainActivity.java"
            source.write_text(
                """
                String phoneNumber = getPhoneNumber();
                HttpURLConnection connection = (HttpURLConnection) url.openConnection();
                """,
                encoding="utf-8",
            )
            report = guard.inspect_source(root, ["MainActivity.java"])
        self.assertFalse(report.passed)
        self.assertEqual(report.status, "BLOCKED")

    def test_local_source_without_disclosure_risk_passes(self):
        guard = PrivacyGuard()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "MainActivity.java"
            source.write_text(
                """
                TextView title = new TextView(this);
                title.setText("Hello");
                """,
                encoding="utf-8",
            )
            report = guard.inspect_source(root, ["MainActivity.java"])
        self.assertTrue(report.passed)
        self.assertEqual(report.status, "VERIFIED")


if __name__ == "__main__":
    unittest.main()
