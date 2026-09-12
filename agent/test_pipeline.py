import tempfile
import unittest
from pathlib import Path

from agent.android import AndroidAppGenerationError
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
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(AndroidAppGenerationError):
                self.pipeline.generate_android(result, directory, approved=True)

    def test_approved_request_reaches_android_generator(self):
        result = self.pipeline.intake("Create a calculator app that works fully offline.")
        self.assertIsNotNone(result.client_brief)
        self.assertEqual(
            result.requirements.original_request,
            "Create a calculator app that works fully offline.",
        )
        self.assertTrue(result.plan.build_required)
        self.assertFalse(result.needs_user_confirmation)
        with tempfile.TemporaryDirectory() as directory:
            generated = self.pipeline.generate_android(result, directory, approved=True)
            activity = Path(generated.project.root) / generated.features.files[0]
            self.assertTrue(activity.is_file())

    def test_generation_requires_approval_flag(self):
        result = self.pipeline.intake("Create a calculator app that works fully offline.")
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(AndroidAppGenerationError):
                self.pipeline.generate_android(result, directory)


if __name__ == "__main__":
    unittest.main()
