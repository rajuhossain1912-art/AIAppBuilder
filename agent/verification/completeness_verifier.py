from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


class CompletenessStatus:
    VERIFIED = "VERIFIED"
    BLOCKED = "BLOCKED"
    NOT_VERIFIED = "NOT_VERIFIED"


@dataclass(frozen=True)
class CompletenessFinding:
    path: str
    message: str


@dataclass
class CompletenessReport:
    project_id: str
    findings: list[CompletenessFinding] = field(default_factory=list)

    @property
    def status(self) -> str:
        return CompletenessStatus.BLOCKED if self.findings else CompletenessStatus.VERIFIED


# Generated apps must never reach delivery while they still contain known
# placeholder language that admits the requested functionality is missing.
_PLACEHOLDER_MARKERS = (
    "requires an approved endpoint",
    "endpoint was invented",
    "requested features must be specified",
    "project shell ready",
    "ready for verified project-specific content",
    "implementation requires",
    "not implemented",
    "placeholder",
)


class AndroidCompletenessVerifier:
    """Rejects generated Android source that still contains explicit placeholders."""

    def verify_project(self, project_id: str, root: str | Path) -> CompletenessReport:
        project_root = Path(root).resolve()
        report = CompletenessReport(project_id=project_id)
        if not project_root.is_dir():
            report.findings.append(
                CompletenessFinding(".", "Android project directory does not exist.")
            )
            return report

        for path in sorted(project_root.rglob("*.java")):
            try:
                text = path.read_text(encoding="utf-8").casefold()
            except (OSError, UnicodeDecodeError):
                report.findings.append(
                    CompletenessFinding(str(path.relative_to(project_root)), "Source could not be read.")
                )
                continue
            for marker in _PLACEHOLDER_MARKERS:
                if marker in text:
                    report.findings.append(
                        CompletenessFinding(
                            str(path.relative_to(project_root)),
                            f"Known placeholder marker remains: {marker}",
                        )
                    )
                    break
        return report
