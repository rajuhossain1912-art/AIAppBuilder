from __future__ import annotations

from dataclasses import asdict, dataclass
import json


@dataclass(frozen=True)
class RecoveryManifest:
    """Portable, secret-free metadata needed to recover a project."""

    project_id: str
    source_revision: str
    passport_revision: str
    generated_revision: str
    build_provider: str
    build_reference: str
    artifact_sha256: str
    restore_instructions: str

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, indent=2, sort_keys=True)


class RecoveryManifestBuilder:
    """Build a recovery record without ever accepting secret material."""

    def build(
        self,
        project_id: str,
        source_revision: str,
        passport_revision: str,
        generated_revision: str,
        build_provider: str,
        build_reference: str,
        artifact_sha256: str,
        restore_instructions: str,
    ) -> RecoveryManifest:
        values = {
            "project_id": project_id,
            "source_revision": source_revision,
            "passport_revision": passport_revision,
            "generated_revision": generated_revision,
            "build_provider": build_provider,
            "build_reference": build_reference,
            "artifact_sha256": artifact_sha256,
            "restore_instructions": restore_instructions,
        }
        if any(not isinstance(value, str) or not value.strip() for value in values.values()):
            raise ValueError("All recovery manifest fields must be non-empty strings")
        return RecoveryManifest(**values)
