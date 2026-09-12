from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from agent.pipeline import AgentPipeline
from agent.review import ReviewEngine
from agent.verification import AndroidAccessibilityVerifier, AndroidCompletenessVerifier


class EndToEndPipelineTest(unittest.TestCase):
    """Prove the approved client request reaches a verified Android source tree."""

    def test_approved_offline_calculator_reaches_quality_gates(self) -> None:
        pipeline = AgentPipeline()
        intake = pipeline.intake(
            "Create an accessible offline calculator app for Android."
        )

        self.assertFalse(intake.needs_user_confirmation)
        self.assertEqual(intake.plan.build_required, True)
        self.assertEqual(intake.plan.test_required, True)

        with tempfile.TemporaryDirectory() as temp_dir:
            generated = pipeline.generate_android(
                intake,
                Path(temp_dir) / "calculator",
                approved=True,
            )
            root = generated.project.root
            main_activity = next(root.rglob("MainActivity.java"))

            accessibility = AndroidAccessibilityVerifier().verify_source(
                "e2e-calculator",
                main_activity,
                required=True,
            )
            self.assertTrue(accessibility.passed)

            completeness = AndroidCompletenessVerifier().verify_project(
                "e2e-calculator",
                root,
            )
            self.assertEqual(completeness.status, "VERIFIED")

            review = ReviewEngine().review_paths(
                "e2e-calculator",
                root,
                generated.features.files,
            )
            self.assertEqual(review.blocking, [])

            source = main_activity.read_text(encoding="utf-8")
            self.assertIn("Double.parseDouble", source)
            self.assertIn("setContentDescription", source)


if __name__ == "__main__":
    unittest.main()
