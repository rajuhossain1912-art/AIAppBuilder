import tempfile
import unittest
from pathlib import Path

from agent.android.app_generator import AndroidAppGenerationError
from agent.pipeline import AgentPipeline


class AgentPipelineTests(unittest.TestCase):
    def setUp(self):
        self.pipeline = AgentPipeline()

    def test_client_questions_block_consequential_generation(self):
        result = self.pipeline.intake("I need an app")
        self.assertTrue(result.needs_user_confirmation)
        self.assertIsNotNone(result.client_brief)
        self.assertFalse(result.client_brief.ready_for_approval)
        self.assertTrue(result.client_brief.questions)

    def test_complete_enough_request_can_reach_planning(self):
        result = self.pipeline.intake(
            "Create a calculator app that works fully offline."
        )
        self.assertIsNotNone(result.client_brief)
        self.assertEqual(result.requirements.original_request, "Create a calculator app that works fully offline.")
        self.assertTrue(result.plan.build_required)
        self.assertTrue(result.needs_user_confirmation)

    def test_generation_requires_explicit_approval(self):
        result = self.pipeline.intake("Create a calculator app that works fully offline.")
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(AndroidAppGenerationError):
                self.pipeline.generate_android(result, directory)

    def test_generation_uses_pipeline_plan_after_approval(self):
        result = self.pipeline.intake("Create an accessible calculator app that works fully offline.")
        with tempfile.TemporaryDirectory() as directory:
            generated = self.pipeline.generate_android(result, directory, approved=True)
            package_path = "/".join(generated.intent.spec.package_name.split("."))
            activity = Path(directory) / "app" / "src" / "main" / "java" / package_path / "MainActivity.java"
            self.assertTrue(activity.is_file())
            self.assertEqual(generated.intent.family, "utility")


if __name__ == "__main__":
    unittest.main()
