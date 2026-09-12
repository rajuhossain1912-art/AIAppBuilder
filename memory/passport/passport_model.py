from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional


class ProjectPassportError(ValueError):
    """Base error for invalid project passport data."""


@dataclass
class ProjectPassport:
    """Authoritative identity and metadata record for one project."""

    project_id: str
    project_name: str
    project_description: str = ""
    project_type: str = ""
    owner: str = ""
    creation_date: str = ""
    last_updated_date: str = ""
    current_lifecycle_state: str = "RECEIVED"
    current_project_version: str = "0.1.0"
    repository_reference: Optional[str] = None
    project_status: str = "ACTIVE"

    requirements: list[str] = field(default_factory=list)
    approvals: list[str] = field(default_factory=list)
    architecture_decisions: list[str] = field(default_factory=list)
    research_findings: list[str] = field(default_factory=list)
    files_created: list[str] = field(default_factory=list)
    files_modified: list[str] = field(default_factory=list)
    builds: list[str] = field(default_factory=list)
    tests: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    fixes: list[str] = field(default_factory=list)
    artifacts: list[str] = field(default_factory=list)
    releases: list[str] = field(default_factory=list)
    rollbacks: list[str] = field(default_factory=list)
    user_feedback: list[str] = field(default_factory=list)
    known_problems: list[str] = field(default_factory=list)
    important_decisions: list[str] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.project_id.strip():
            raise ProjectPassportError("project_id is required")

        if not self.project_name.strip():
            raise ProjectPassportError("project_name is required")

        if not self.creation_date:
            self.creation_date = self._now()

        if not self.last_updated_date:
            self.last_updated_date = self.creation_date

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    def touch(self) -> None:
        """Update the passport modification timestamp."""
        self.last_updated_date = self._now()

    def add_requirement(self, requirement: str) -> None:
        self._add_unique(self.requirements, requirement)

    def add_approval(self, approval: str) -> None:
        self._add_unique(self.approvals, approval)

    def add_architecture_decision(self, decision: str) -> None:
        self._add_unique(self.architecture_decisions, decision)

    def add_research_finding(self, finding: str) -> None:
        self._add_unique(self.research_findings, finding)

    def add_file_created(self, path: str) -> None:
        self._add_unique(self.files_created, path)

    def add_file_modified(self, path: str) -> None:
        self._add_unique(self.files_modified, path)

    def add_build(self, result: str) -> None:
        self._add_unique(self.builds, result)

    def add_test(self, result: str) -> None:
        self._add_unique(self.tests, result)

    def add_error(self, error: str) -> None:
        self._add_unique(self.errors, error)

    def add_fix(self, fix: str) -> None:
        self._add_unique(self.fixes, fix)

    def add_artifact(self, artifact: str) -> None:
        self._add_unique(self.artifacts, artifact)

    def add_release(self, release: str) -> None:
        self._add_unique(self.releases, release)

    def add_rollback(self, rollback: str) -> None:
        self._add_unique(self.rollbacks, rollback)

    def add_user_feedback(self, feedback: str) -> None:
        self._add_unique(self.user_feedback, feedback)

    def add_known_problem(self, problem: str) -> None:
        self._add_unique(self.known_problems, problem)

    def add_important_decision(self, decision: str) -> None:
        self._add_unique(self.important_decisions, decision)

    def set_lifecycle_state(self, state: str) -> None:
        if not state.strip():
            raise ProjectPassportError("lifecycle state cannot be empty")
        self.current_lifecycle_state = state
        self.touch()

    def set_project_status(self, status: str) -> None:
        if not status.strip():
            raise ProjectPassportError("project status cannot be empty")
        self.project_status = status
        self.touch()

    def to_dict(self) -> Dict[str, Any]:
        """Return a serializable passport representation."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProjectPassport":
        """Create a passport from serialized data."""
        if not isinstance(data, dict):
            raise ProjectPassportError("passport data must be a dictionary")

        return cls(**data)

    @staticmethod
    def _add_unique(items: list[str], value: str) -> None:
        value = value.strip()

        if not value:
            raise ProjectPassportError("record value cannot be empty")

        if value not in items:
            items.append(value)
