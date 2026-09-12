from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from agent.orchestrator.pipeline_orchestrator import PipelineOrchestrator
from agent.orchestrator.state_model import LifecycleState


class ReleaseCycleTests(unittest.TestCase):
    def _android_fixture(self, root: Path) -> None:
        (root / "app/src/main").mkdir(parents=True)
        (root / "settings.gradle").write_text('rootProject.name = "Fixture"\ninclude(":app")\n', encoding="utf-8")
        (root / "build.gradle").write_text('plugins { id "com.android.application" version "8.7.3" apply false }\n', encoding="utf-8")
        (root / "app/build.gradle").write_text(
            'plugins { id "com.android.application" }\n'
            'android { namespace "com.example.fixture"; compileSdk 35; defaultConfig { '
            'applicationId "com.example.fixture"; minSdk 23; targetSdk 35 } }\n',
            encoding="utf-8",
        )
        (root / "app/src/main/AndroidManifest.xml").write_text(
            '<manifest xmlns:android="http://schemas.android.com/apk/res/android">\n'
            '  <application><activity android:name=".MainActivity" android:exported="true" /></application>\n'
            '</manifest>\n',
            encoding="utf-8",
        )
        source = root / "app/src/main/Main.java"
        source.write_text(
            'import android.widget.Button;\n'
            'class Main { Button button; void label() { button.setContentDescription("Action"); } }\n',
            encoding="utf-8",
        )
        (root / "requirements_verification.json").write_text(
            json.dumps({
                "status": "VERIFIED",
                "required_capabilities": ["general"],
                "generated_capabilities": ["general"],
                "implemented_capabilities": ["general"],
                "unsupported_capabilities": [],
                "missing_capabilities": [],
                "missing_files": [],
                "unresolved_questions": [],
                "reasons": [],
            }),
            encoding="utf-8",
        )

    def _start_review(self, runner: PipelineOrchestrator) -> None:
        runner.orchestrator.start()
        runner.orchestrator.transition_to(LifecycleState.UNDERSTANDING)
        runner.orchestrator.transition_to(LifecycleState.PLANNING)
        runner.orchestrator.transition_to(LifecycleState.GENERATING)
        runner.orchestrator.transition_to(LifecycleState.REVIEWING)

    def test_review_build_test_verify_delivery_cycle(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self._android_fixture(root)
            artifact = root / "app-debug.apk"
            build = [
                "python",
                "-c",
                "from pathlib import Path; Path('app-debug.apk').write_bytes(b'ci-artifact')",
            ]
            test = [
                "python",
                "-c",
                "from pathlib import Path; assert Path('app/src/main/Main.java').is_file()",
            ]

            runner = PipelineOrchestrator("release-test", root / "state.json")
            self._start_review(runner)

            result = runner.execute_release_cycle(
                project_root=root,
                review_paths=["app/src/main/Main.java"],
                build_command=build,
                test_command=test,
                artifact_path=artifact,
                authorized=True,
            )

            self.assertTrue(result.delivered)
            self.assertEqual(result.verification.final_status, "VERIFIED")
            self.assertEqual(result.delivery.status, "READY")
            self.assertTrue(result.delivery.manifest)
            self.assertEqual(runner.orchestrator.current_state, LifecycleState.COMPLETED)
            self.assertEqual(result.retries, 0)

    def test_build_failure_uses_fix_callback_and_retries_to_delivery(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self._android_fixture(root)
            artifact = root / "app-debug.apk"
            build = [
                "python",
                "-c",
                "from pathlib import Path; marker=Path('build-fixed'); assert marker.is_file(), 'intentional first-attempt build failure'; Path('app-debug.apk').write_bytes(b'ci-artifact')",
            ]
            test = [
                "python",
                "-c",
                "from pathlib import Path; assert Path('app/src/main/Main.java').is_file()",
            ]
            runner = PipelineOrchestrator("release-retry-test", root / "state.json")
            self._start_review(runner)
            callbacks: list[tuple[str, int]] = []

            def fix(stage: str, attempt: int) -> None:
                callbacks.append((stage, attempt))
                if stage == "BUILD":
                    (root / "build-fixed").write_text("fixed", encoding="utf-8")

            result = runner.execute_release_cycle(
                project_root=root,
                review_paths=["app/src/main/Main.java"],
                build_command=build,
                test_command=test,
                artifact_path=artifact,
                authorized=True,
                max_retries=2,
                fix_callback=fix,
            )

            self.assertTrue(result.delivered)
            self.assertEqual(result.retries, 1)
            self.assertEqual(callbacks, [("BUILD", 1)])
            self.assertEqual(runner.orchestrator.current_state, LifecycleState.COMPLETED)
            self.assertEqual(runner.orchestrator.state.retry_count, 1)

    def test_release_is_blocked_without_verified_requirements_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self._android_fixture(root)
            (root / "requirements_verification.json").unlink()
            artifact = root / "app-debug.apk"
            build = [
                "python",
                "-c",
                "from pathlib import Path; Path('app-debug.apk').write_bytes(b'ci-artifact')",
            ]
            test = [
                "python",
                "-c",
                "from pathlib import Path; assert Path('app/src/main/Main.java').is_file()",
            ]
            runner = PipelineOrchestrator("release-test", root / "state.json")
            self._start_review(runner)
            with self.assertRaises(RuntimeError):
                runner.execute_release_cycle(
                    project_root=root,
                    review_paths=["app/src/main/Main.java"],
                    build_command=build,
                    test_command=test,
                    artifact_path=artifact,
                    authorized=True,
                    max_retries=0,
                )


if __name__ == "__main__":
    unittest.main()
