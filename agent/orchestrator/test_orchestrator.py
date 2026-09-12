from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from agent.orchestrator import LifecycleState, Orchestrator, OrchestratorError


class OrchestratorTest(unittest.TestCase):
    def test_new_project_persists_and_restores_state_and_passport(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state_path = root / "state.json"
            passport_path = root / "project_passport.json"
            first = Orchestrator("project-1", str(state_path))
            first.start()
            first.transition_to(LifecycleState.UNDERSTANDING)
            first.request_approval("generate_android")
            first.receive_approval("generate_android")
            first.record_success("requirements_ready")

            self.assertTrue(passport_path.is_file())
            passport = json.loads(passport_path.read_text(encoding="utf-8"))
            self.assertEqual(passport["project_id"], "project-1")
            self.assertEqual(passport["current_state"], "UNDERSTANDING")
            self.assertFalse(passport["approved"])
            self.assertGreaterEqual(len(passport["audit_log"]), 1)

            first.request_approval("requirements_and_plan")
            first.receive_approval("requirements_and_plan")
            passport = json.loads(passport_path.read_text(encoding="utf-8"))
            self.assertTrue(passport["approved"])
            self.assertIn("requirements_ready", passport["completed_operations"])
            self.assertTrue(any(entry["state"] == "UNDERSTANDING" for entry in passport["audit_log"]))

            second = Orchestrator("project-1", str(state_path))
            restored = second.start()

            self.assertEqual(restored.current_state, LifecycleState.UNDERSTANDING)
            self.assertIn("generate_android", restored.required_approvals)
            self.assertIn("generate_android", restored.received_approvals)
            self.assertEqual(restored.last_successful_operation, "requirements_ready")

    def test_verified_lifecycle_metadata_is_persisted_to_passport(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            orchestrator = Orchestrator("project-metadata", str(root / "state.json"))
            orchestrator.start()
            orchestrator.complete_task("build")
            orchestrator.complete_task("test")
            orchestrator.complete_task("verification")
            orchestrator.record_verified_result("a" * 64)

            passport = json.loads(
                (root / "project_passport.json").read_text(encoding="utf-8")
            )
            self.assertEqual(passport["build_status"], "VERIFIED")
            self.assertEqual(passport["test_status"], "VERIFIED")
            self.assertEqual(passport["verification_status"], "VERIFIED")
            self.assertEqual(passport["accessibility_status"], "VERIFIED")
            self.assertEqual(passport["artifact_sha256"], "a" * 64)
            self.assertEqual(passport["generated_revision"], "artifact:" + "a" * 64)
            self.assertTrue(passport["audit_log"])
            self.assertEqual(passport["audit_log"][-1]["last_verified_result"], "a" * 64)

    def test_invalid_transition_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            orchestrator = Orchestrator("project-2", str(Path(temp_dir) / "state.json"))
            orchestrator.start()
            with self.assertRaises(OrchestratorError):
                orchestrator.transition_to(LifecycleState.COMPLETED)

    def test_mismatched_project_state_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "state.json"
            first = Orchestrator("project-a", str(state_path))
            first.start()

            second = Orchestrator("project-b", str(state_path))
            with self.assertRaises(OrchestratorError):
                second.start()


if __name__ == "__main__":
    unittest.main()
