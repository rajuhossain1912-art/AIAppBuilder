from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from agent.passport import ProjectPassport, ProjectPassportStore


class ProjectPassportTest(unittest.TestCase):
    def test_round_trip_json_preserves_verified_state(self) -> None:
        passport = ProjectPassport(
            project_id="demo-001",
            project_name="Accessible Calculator",
            package_name="com.aiappbuilder.accessiblecalculator",
            created_at="2026-09-12T00:00:00+00:00",
            updated_at="2026-09-12T01:00:00+00:00",
            source_revision="abc123",
            generated_revision="def456",
            current_state="VERIFYING",
            approved=True,
            requirements_summary="Accessible offline calculator",
            plan_summary="Generate, review, build, test, verify",
            build_provider="github-actions",
            build_reference="run-123",
            build_status="VERIFIED",
            test_status="VERIFIED",
            accessibility_status="VERIFIED",
            performance_status="VERIFIED",
            verification_status="VERIFIED",
            delivery_status="NOT_VERIFIED",
            artifact_sha256="a" * 64,
            completed_operations=["generation", "build", "test"],
            recovery_notes=["Restore from source revision abc123"],
            audit_log=[
                {
                    "timestamp": "2026-09-12T01:00:00+00:00",
                    "state": "VERIFYING",
                    "current_task": "verification",
                }
            ],
        )

        restored = ProjectPassport.from_json(passport.to_json())
        self.assertEqual(restored.to_dict(), passport.to_dict())

    def test_store_round_trip(self) -> None:
        passport = ProjectPassport(
            project_id="demo-002",
            project_name="Test App",
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "project-passport.json"
            store = ProjectPassportStore(path)
            store.save(passport)
            restored = store.load()
            self.assertEqual(restored.project_id, "demo-002")
            self.assertEqual(restored.project_name, "Test App")
            self.assertEqual(restored.schema_version, 2)

    def test_schema_v1_migrates_to_schema_v2(self) -> None:
        restored = ProjectPassport.from_dict(
            {
                "schema_version": 1,
                "project_id": "legacy",
                "project_name": "Legacy App",
            }
        )
        self.assertEqual(restored.schema_version, 2)
        self.assertEqual(restored.audit_log, [])

    def test_invalid_schema_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ProjectPassport.from_dict(
                {
                    "schema_version": 99,
                    "project_id": "demo",
                    "project_name": "Demo",
                }
            )

    def test_invalid_audit_entry_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ProjectPassport.from_dict(
                {
                    "schema_version": 2,
                    "project_id": "demo",
                    "project_name": "Demo",
                    "audit_log": ["not-an-object"],
                }
            )


if __name__ == "__main__":
    unittest.main()
