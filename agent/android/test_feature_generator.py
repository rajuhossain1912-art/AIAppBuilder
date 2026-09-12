from pathlib import Path
import tempfile
import unittest

from agent.android.app_spec_builder import AndroidBuildIntentBuilder
from agent.android.feature_generator import AndroidFeatureGenerationError, AndroidFeatureGenerator
from agent.android.project_generator import AndroidProjectGenerator
from agent.planning import PlanningEngine
from agent.requirements import RequirementEngine


class AndroidFeatureGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.requirements = RequirementEngine()
        self.planning = PlanningEngine()
        self.intent_builder = AndroidBuildIntentBuilder()
        self.generator = AndroidFeatureGenerator()
        self.project_generator = AndroidProjectGenerator()

    def _intent(self, request):
        requirements = self.requirements.analyze(request)
        plan = self.planning.create_plan(requirements)
        return self.intent_builder.build(plan)

    def test_utility_generates_working_calculator_code(self):
        intent = self._intent("Create an accessible calculator app that works offline.")
        with tempfile.TemporaryDirectory() as tmp:
            self.project_generator.generate(tmp, intent.spec)
            result = self.generator.generate(tmp, intent)
            source = Path(tmp, result.files[0]).read_text(encoding="utf-8")
        self.assertEqual(result.family, "utility")
        self.assertIn("calculator", result.capabilities)
        self.assertIn("Double.parseDouble", source)
        self.assertIn("Result:", source)
        self.assertIn("setContentDescription", source)

    def test_form_generates_submit_validation(self):
        intent = self._intent("Create an accessible registration form app.")
        with tempfile.TemporaryDirectory() as tmp:
            self.project_generator.generate(tmp, intent.spec)
            result = self.generator.generate(tmp, intent)
            source = Path(tmp, result.files[0]).read_text(encoding="utf-8")
        self.assertEqual(result.family, "form")
        self.assertIn("forms_data", result.capabilities)
        self.assertIn("Name is required", source)
        self.assertIn("Saved:", source)

    def test_voice_video_news_request_is_composed(self):
        request = (
            "Create an accessible Bangla AI voice video maker with text to speech, "
            "images, video creation and an online news content screen."
        )
        intent = self._intent(request)
        expected = {"audio", "video", "image", "news", "text_content", "online_service"}
        self.assertTrue(expected.issubset(set(intent.capabilities)))
        with tempfile.TemporaryDirectory() as tmp:
            self.project_generator.generate(tmp, intent.spec)
            result = self.generator.generate(tmp, intent)
            source = Path(tmp, result.files[0]).read_text(encoding="utf-8")
        self.assertTrue(expected.issubset(set(result.capabilities)))
        self.assertIn("TextToSpeech", source)
        self.assertIn("Video capability", source)
        self.assertIn("Image capability", source)
        self.assertIn("News and newspaper capability", source)
        self.assertIn("Text and content capability", source)
        self.assertIn("Online service capability", source)

    def test_music_and_instrument_generate_real_tone_controls(self):
        request = "Create an accessible music app with guitar, harmonium, tabla, piano and notes."
        intent = self._intent(request)
        expected = {"music", "instrument"}
        self.assertTrue(expected.issubset(set(intent.capabilities)))
        with tempfile.TemporaryDirectory() as tmp:
            self.project_generator.generate(tmp, intent.spec)
            result = self.generator.generate(tmp, intent)
            source = Path(tmp, result.files[0]).read_text(encoding="utf-8")
        self.assertTrue(expected.issubset(set(result.capabilities)))
        self.assertTrue(expected.issubset(set(result.implemented_capabilities)))
        self.assertIn("AudioTrack", source)
        self.assertIn("playTone", source)
        self.assertIn("C4", source)
        self.assertIn("setContentDescription", source)

    def test_requires_existing_generated_project(self):
        intent = self._intent("Create a calculator app.")
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(AndroidFeatureGenerationError):
                self.generator.generate(Path(tmp) / "missing", intent)


if __name__ == "__main__":
    unittest.main()
