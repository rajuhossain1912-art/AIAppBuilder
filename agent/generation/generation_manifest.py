from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class GenerationManifestError(ValueError):
    """Raised when a generation manifest is invalid."""


@dataclass
class GenerationManifest:
    """Traceable plan for files created or modified by one generation session."""

    project_id: str
    session_id: str
    requirement_ids: list[str] = field(default_factory=list)
    files_to_create: list[str] = field(default_factory=list)
    files_to_modify: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    tests: list[str] = field(default_factory=list)
    expected_artifacts: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        for name in ("project_id", "session_id"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise GenerationManifestError(f"{name} must not be empty")
            setattr(self, name, value.strip())

        for name in (
            "requirement_ids", "files_to_create", "files_to_modify",
            "dependencies", "tests", "expected_artifacts",
        ):
            values = getattr(self, name)
            if not isinstance(values, list) or not all(isinstance(v, str) and v.strip() for v in values):
                raise GenerationManifestError(f"{name} must contain non-empty strings")
            setattr(self, name, self._unique(values))

    @staticmethod
    def _unique(values: list[str]) -> list[str]:
        result: list[str] = []
        for value in values:
            value = value.strip()
            if value not in result:
                result.append(value)
        return result

    def add_file(self, path: str, *, modify: bool = False) -> None:
        if not isinstance(path, str) or not path.strip():
            raise GenerationManifestError("file path must not be empty")
        path = path.strip()
        target = self.files_to_modify if modify else self.files_to_create
        if path not in target:
            target.append(path)

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "session_id": self.session_id,
            "requirement_ids": list(self.requirement_ids),
            "files_to_create": list(self.files_to_create),
            "files_to_modify": list(self.files_to_modify),
            "dependencies": list(self.dependencies),
            "tests": list(self.tests),
            "expected_artifacts": list(self.expected_artifacts),
        }
