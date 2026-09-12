from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from agent.orchestrator import LifecycleState
from agent.orchestrator.pipeline_orchestrator import PipelineOrchestrator


class PipelineOrchestratorTest(unittest.TestCase):
    def test_complete_offline_request_reaches_reviewing_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "state.json"
            output = Path(temp_dir) / "calculator"
            runner = PipelineOrchestrator("e2e-orchestrated", state_path)
            result = runner.intake("Create an accessible offline calculator app for Android.")

            self.assertFalse(result.intake.needs_user_confirmation)
            generated = runner.approve_and_generate(result, output)

            self.assertTrue((generated.project.root / "settings.gradle").is_file())
            self.assertEqual(runner.orchestrator.current_state, LifecycleState.REVIEWING)
            self.assertIn("android_source_generated", runner.orchestrator.state.last_successful_operation)

    def test_unclear_request_waits_for_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            runner = PipelineOrchestrator("unclear", Path(temp_dir) / "state.json")
            result = runner.intake("Make me an app")
            self.assertTrue(result.intake.needs_user_confirmation)
            self.assertEqual(
                runner.orchestrator.current_state,
                LifecycleState.AWAITING_CONFIRMATION,
            )


if __name__ == "__main__":
    unittest.main()
