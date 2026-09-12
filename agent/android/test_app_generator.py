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

    def test_generates_composable_real_capabilities(self) -> None:
        plan = self._plan(
            "Create an accessible app for education, sports, profile, business, news, text content, image, video and online services."
        )
        with tempfile.TemporaryDirectory() as directory:
            result = self.generator.generate(plan, directory, approved=True)
            self.assertTrue(result.features.implemented_capabilities)
            self.assertFalse(result.features.unsupported_capabilities)
            source = next(
                (Path(directory) / relative).read_text(encoding="utf-8")
                for relative in result.features.files
                if relative.endswith("MainActivity.java")
            )
            self.assertIn("Choose image", source)
            self.assertIn("Choose video", source)
            self.assertIn("Open online service", source)
            self.assertIn("Save content", source)
            self.assertIn("setContentDescription", source)

    def test_global_accessibility_gate_rejects_unlabeled_interactive_source(self) -> None:
        class InaccessibleGenerator:
            def generate(self, project_root, intent):
                activity = Path(project_root) / "app" / "src" / "main" / "java" / Path(*intent.spec.package_name.split(".")) / "MainActivity.java"
                activity.parent.mkdir(parents=True, exist_ok=True)
                activity.write_text(
                    "import android.widget.Button;\nButton action = new Button(this);\n",
                    encoding="utf-8",
                )
                from agent.android.feature_generator import GeneratedAndroidFeatures
                return GeneratedAndroidFeatures(
                    files=(str(activity.relative_to(project_root)),),
                    family=intent.family,
                    capabilities=intent.capabilities,
                    implemented_capabilities=intent.capabilities,
                )

        plan = self._plan("Create an accessible calculator app that works fully offline.")
        generator = AndroidAppGenerator(feature_generator=InaccessibleGenerator())
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(AndroidAppGenerationError):
                generator.generate(plan, directory, approved=True)

    def test_rejects_generation_when_requested_capability_is_not_implemented(self) -> None:
        plan = self._plan("Create an accessibility utility app with screen reader tools and offline accessibility service features.")
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(AndroidAppGenerationError):
                self.generator.generate(plan, directory, approved=True)

    def test_performance_preflight_rejects_blocking_source(self) -> None:
        class BlockingGenerator:
            def generate(self, project_root, intent):
                activity = Path(project_root) / "app" / "src" / "main" / "java" / Path(*intent.spec.package_name.split(".")) / "MainActivity.java"
                activity.parent.mkdir(parents=True, exist_ok=True)
                activity.write_text("Thread.sleep(5000);", encoding="utf-8")
                from agent.android.feature_generator import GeneratedAndroidFeatures
                return GeneratedAndroidFeatures(files=(str(activity.relative_to(project_root)),), family=intent.family)

        plan = self._plan("Create an accessible calculator app that works fully offline.")
        generator = AndroidAppGenerator(feature_generator=BlockingGenerator())
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(AndroidAppGenerationError):
                generator.generate(plan, directory, approved=True)

    def test_rejects_generation_with_invalid_plan(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(TypeError):
                self.generator.generate(None, directory, approved=True)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
