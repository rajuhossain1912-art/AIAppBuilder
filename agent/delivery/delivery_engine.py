from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone


@dataclass
class DeliveryGate:
    requirements_verified: bool = False
    build_succeeded: bool = False
    tests_passed: bool = False
    review_blockers_resolved: bool = False
    security_ok: bool = False
    accessibility_ok: bool = False
    compatibility_ok: bool = False
    artifact_verified: bool = False
    authorized: bool = False

    @property
    def ready(self) -> bool:
        return all((
            self.requirements_verified, self.build_succeeded, self.tests_passed,
            self.review_blockers_resolved, self.security_ok,
            self.accessibility_ok, self.compatibility_ok,
            self.artifact_verified, self.authorized,
        ))


@dataclass
class DeliveryResult:
    status: str
    artifact: str | None = None
    checksum_sha256: str | None = None
    reasons: list[str] = field(default_factory=list)
    manifest: str | None = None


class DeliveryEngine:
    """Allows delivery only after every required gate is explicitly satisfied."""

    def prepare(
        self,
        gate: DeliveryGate,
        artifact_path: str | Path | None = None,
        project_id: str | None = None,
        evidence: dict[str, object] | None = None,
    ) -> DeliveryResult:
        reasons: list[str] = []
        checks = {
            "requirements_verified": "Requirements are not verified.",
            "build_succeeded": "Build has not been confirmed successful.",
            "tests_passed": "Required tests have not passed.",
            "review_blockers_resolved": "Release-blocking review findings remain.",
            "security_ok": "Security verification is incomplete.",
            "accessibility_ok": "Accessibility verification is incomplete.",
            "compatibility_ok": "Compatibility verification is incomplete.",
            "artifact_verified": "Artifact verification is incomplete.",
            "authorized": "Delivery authorization has not been granted.",
        }
        for name, message in checks.items():
            if not getattr(gate, name):
                reasons.append(message)

        if artifact_path is not None:
            target = Path(artifact_path)
            if not target.is_file():
                reasons.append("The claimed delivery artifact does not exist.")
            elif gate.ready:
                digest = hashlib.sha256(target.read_bytes()).hexdigest()
                manifest_path = target.with_suffix(target.suffix + ".delivery.json")
                manifest_data = {
                    "project_id": project_id,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "artifact": str(target),
                    "sha256": digest,
                    "gate": gate.__dict__,
                    "evidence": evidence or {},
                }
                manifest_path.write_text(
                    json.dumps(manifest_data, ensure_ascii=False, indent=2, sort_keys=True),
                    encoding="utf-8",
                )
                return DeliveryResult(
                    status="READY", artifact=str(target),
                    checksum_sha256=digest, manifest=str(manifest_path),
                )

        return DeliveryResult(status="BLOCKED", reasons=reasons)
