import unittest

from agent.recovery import RecoveryManifestBuilder


class RecoveryManifestTests(unittest.TestCase):
    def test_builds_portable_manifest(self):
        manifest = RecoveryManifestBuilder().build(
            project_id="demo",
            source_revision="abc123",
            passport_revision="passport-1",
            generated_revision="generated-1",
            build_provider="github-actions",
            build_reference="run-123",
            artifact_sha256="deadbeef",
            restore_instructions="Checkout the recorded source revision and rebuild.",
        )
        payload = manifest.to_json()
        self.assertIn("source_revision", payload)
        self.assertNotIn("token", payload.lower())
        self.assertNotIn("password", payload.lower())

    def test_rejects_empty_fields(self):
        with self.assertRaises(ValueError):
            RecoveryManifestBuilder().build(
                "demo", "", "passport", "generated", "provider", "run", "sha", "restore"
            )


if __name__ == "__main__":
    unittest.main()
