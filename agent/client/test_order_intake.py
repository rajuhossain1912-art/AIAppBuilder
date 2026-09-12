import unittest

from agent.client import ClientOrderIntake


class ClientOrderIntakeTests(unittest.TestCase):
    def setUp(self):
        self.intake = ClientOrderIntake()

    def test_short_request_gets_clarifying_questions(self):
        brief = self.intake.start("I need an app")
        self.assertFalse(brief.ready_for_approval)
        self.assertTrue(any("main purpose" in q.lower() for q in brief.questions))

    def test_youtube_request_asks_for_source(self):
        brief = self.intake.start("Create an app for my YouTube channel")
        self.assertTrue(any("channel/page/content source" in q.lower() for q in brief.questions))

    def test_api_request_asks_for_endpoint(self):
        brief = self.intake.start("Create an online app that reads data from an API")
        self.assertTrue(any("endpoint" in q.lower() for q in brief.questions))

    def test_original_request_is_preserved(self):
        brief = self.intake.start("  Make a calculator app  ")
        self.assertEqual(brief.requirements.original_request, "Make a calculator app")


if __name__ == "__main__":
    unittest.main()
