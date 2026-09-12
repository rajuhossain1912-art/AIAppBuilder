from pathlib import Path
import tempfile
import unittest

from agent.android.app_spec_builder import AndroidBuildIntentBuilder
from agent.android.feature_generator import AndroidFeatureGenerator
from agent.android.project_generator import AndroidProjectGenerator
from agent.planning import PlanningEngine
from agent.requirements import RequirementEngine


class ImageEditorGeneratorTests(unittest.TestCase):
    def test_image_editor_is_generated_and_marked_implemented(self):
        requirements = RequirementEngine().analyze(
            "Create an accessible image editor with rotate, grayscale and export."
        )
        plan = PlanningEngine().create_plan(requirements)
        intent = AndroidBuildIntentBuilder().build(plan)
        self.assertIn("image_editor", intent.capabilities)

        with tempfile.TemporaryDirectory() as tmp:
            AndroidProjectGenerator().generate(tmp, intent.spec)
            result = AndroidFeatureGenerator().generate(tmp, intent)
            source = Path(tmp, result.files[0]).read_text(encoding="utf-8")

        self.assertIn("image_editor", result.implemented_capabilities)
        self.assertNotIn("image_editor", result.unsupported_capabilities)
        self.assertIn("BitmapFactory", source)
        self.assertIn("Rotate image 90 degrees", source)
        self.assertIn("Convert image to grayscale", source)
        self.assertIn("Export edited image", source)
        self.assertIn("setContentDescription", source)


if __name__ == "__main__":
    unittest.main()
