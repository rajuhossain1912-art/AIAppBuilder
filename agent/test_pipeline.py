import unittest

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


if __name__ == "__main__":
    unittest.main()
