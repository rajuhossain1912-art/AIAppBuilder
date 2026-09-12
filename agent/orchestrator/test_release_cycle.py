from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from agent.orchestrator.pipeline_orchestrator import PipelineOrchestrator
from agent.orchestrator.state_model import LifecycleState


class ReleaseCycleTests(unittest.TestCase):
    def test_review_build_test_verify_delivery_cycle(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "Main.java"
            source.write_text("class Main {}\n", encoding="utf-8")
            artifact = root / "app-debug.apk"

            build = [
                "python",
                "-c",
                "from pathlib import Path; Path('app-debug.apk').write_bytes(b'ci-artifact')",
            ]
            test = ["python", "-c", "assert Path('Main.java').is_file()"]

            state = root / "state.json"
            runner = PipelineOrchestrator("release-test", state)
            runner.orchestrator.start()
            runner.orchestrator.transition_to(LifecycleState.UNDERSTANDING)
            runner.orchestrator.transition_to(LifecycleState.PLANNING)
            runner.orchestrator.transition_to(LifecycleState.GENERATING)
            runner.orchestrator.transition_to(LifecycleState.REVIEWING)

            result = runner.execute_release_cycle(
                project_root=root,
                review_paths=["Main.java"],
                build_command=build,
                test_command=test,
                artifact_path=artifact,
                authorized=True,
            )

            self.assertTrue(result.delivered)
            self.assertEqual(result.verification.final_status, "VERIFIED")
            self.assertEqual(result.delivery.status, "READY")
            self.assertEqual(runner.orchestrator.current_state, LifecycleState.COMPLETED)
            self.assertEqual(result.retries, 0)


if __name__ == "__main__":
    unittest.main()
