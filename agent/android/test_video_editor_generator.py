from pathlib import Path
import tempfile
import unittest

from agent.android.app_spec_builder import AndroidBuildIntentBuilder
from agent.android.feature_generator import AndroidFeatureGenerator
from agent.android.project_generator import AndroidProjectGenerator
from agent.planning import PlanningEngine
from agent.requirements import RequirementEngine


class VideoEditorGeneratorTests(unittest.TestCase):
    def test_video_editor_is_generated_and_marked_implemented(self):
        requirements = RequirementEngine().analyze(
            "Create an accessible video editor with trim, split, preview and export."
        )
        plan = PlanningEngine().create_plan(requirements)
        intent = AndroidBuildIntentBuilder().build(plan)
        self.assertIn("video_editor", intent.capabilities)

        with tempfile.TemporaryDirectory() as tmp:
            AndroidProjectGenerator().generate(tmp, intent.spec)
            result = AndroidFeatureGenerator().generate(tmp, intent)
            source = Path(tmp, result.files[0]).read_text(encoding="utf-8")

        self.assertIn("video_editor", result.implemented_capabilities)
        self.assertNotIn("video_editor", result.unsupported_capabilities)
        self.assertIn("MediaExtractor", source)
        self.assertIn("MediaMuxer", source)
        self.assertIn("Trim and export video", source)
        self.assertIn("Split at end time", source)
        self.assertIn("Playing video preview", source)
        self.assertIn("Choose video", source)


if __name__ == "__main__":
    unittest.main()
