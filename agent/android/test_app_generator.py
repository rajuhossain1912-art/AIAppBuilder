from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from agent.android import AndroidAppGenerator
from agent.android.app_generator import AndroidAppGenerationError
from agent.planning import PlanningEngine
from agent.requirements import RequirementEngine


class AndroidAppGeneratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.requirements = RequirementEngine()
        self.planning = PlanningEngine()
        self.generator = AndroidAppGenerator()

    def _plan(self, request: str):
        requirements = self.requirements.analyze(request)
        return self.planning.create_plan(requirements)

    def test_requires_explicit_approval(self) -> None:
        plan = self._plan("Create a calculator app that works fully offline.")
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(AndroidAppGenerationError):
                self.generator.generate(plan, directory)

    def test_generates_project_and_features_after_approval(self) -> None:
        plan = self._plan("Create an accessible calculator app that works fully offline.")
        with tempfile.TemporaryDirectory() as directory:
            result = self.generator.generate(plan, directory, approved=True)
            package_path = "/".join(result.intent.spec.package_name.split("."))
            activity = Path(directory) / "app" / "src" / "main" / "java" / package_path / "MainActivity.java"
            self.assertTrue(activity.is_file())
            self.assertEqual(result.intent.family, "utility")
            self.assertEqual(result.features.family, "utility")
            source = activity.read_text(encoding="utf-8")
            self.assertIn("Double.parseDouble", source)
            self.assertIn("setContentDescription", source)


if __name__ == "__main__":
    unittest.main()
