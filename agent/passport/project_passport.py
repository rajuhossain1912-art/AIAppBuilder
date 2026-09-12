from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
from typing import Any


@dataclass
class ProjectPassport:
    """Authoritative, portable identity and state record for one project.

    The passport stores project metadata and verified lifecycle facts, but never
    stores secrets. It is deliberately JSON-compatible so it can survive
    provider migration and repository recovery.
    """

    schema_version: int = 2
    project_id: str = ""
    project_name: str = ""
    package_name: str = ""
    created_at: str = ""
    updated_at: str = ""
    source_revision: str = ""
    generated_revision: str = ""
    current_state: str = "RECEIVED"
    approved: bool = False
    requirements_summary: str = ""
    plan_summary: str = ""
    build_provider: str = ""
    build_reference: str = ""
    build_status: str = "NOT_VERIFIED"
    test_status: str = "NOT_VERIFIED"
    accessibility_status: str = "NOT_VERIFIED"
    performance_status: str = "NOT_VERIFIED"
    verification_status: str = "NOT_VERIFIED"
    delivery_status: str = "NOT_VERIFIED"
    artifact_sha256: str = ""
    completed_operations: list[str] = field(default_factory=list)
    blocked_operations: list[str] = field(default_factory=list)
    known_errors: list[str] = field(default_factory=list)
    recovery_notes: list[str] = field(default_factory=list)
    audit_log: list[dict[str, Any]] = field(default_factory=list)

    def validate(self) -> None:
        if self.schema_version != 2:
            raise ValueError("Unsupported Project Passport schema version")
        if not isinstance(self.project_id, str) or not self.project_id.strip():
            raise ValueError("project_id must not be empty")
        if not isinstance(self.project_name, str) or not self.project_name.strip():
            raise ValueError("project_name must not be empty")
        if not isinstance(self.current_state, str) or not self.current_state.strip():
            raise ValueError("current_state must not be empty")
        for field_name in (
            "completed_operations",
            "blocked_operations",
            "known_errors",
            "recovery_notes",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
                raise ValueError(f"{field_name} must be a list of strings")
        if not isinstance(self.audit_log, list):
            raise ValueError("audit_log must be a list")
        for entry in self.audit_log:
            if not isinstance(entry, dict):
                raise ValueError("audit_log entries must be objects")
            if not all(isinstance(key, str) for key in entry):
                raise ValueError("audit_log keys must be strings")

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2, sort_keys=True)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProjectPassport":
        if not isinstance(data, dict):
            raise ValueError("passport data must be an object")
        # Backward-compatible migration from schema v1.
        migrated = dict(data)
        if migrated.get("schema_version") == 1:
            migrated["schema_version"] = 2
            migrated.setdefault("audit_log", [])
        passport = cls(**migrated)
        passport.validate()
        return passport

    @classmethod
    def from_json(cls, text: str) -> "ProjectPassport":
        if not isinstance(text, str) or not text.strip():
            raise ValueError("passport JSON must not be empty")
        return cls.from_dict(json.loads(text))


class ProjectPassportStore:
    """Atomic-ish local JSON persistence for a Project Passport."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def save(self, passport: ProjectPassport) -> None:
        passport.validate()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(passport.to_json() + "\n", encoding="utf-8")
        temporary.replace(self.path)

    def load(self) -> ProjectPassport:
        if not self.path.is_file():
            raise FileNotFoundError(self.path)
        return ProjectPassport.from_json(self.path.read_text(encoding="utf-8"))
