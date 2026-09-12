from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import re
from typing import Iterable


class ReviewStatus(str, Enum):
    IMPLEMENTED = "IMPLEMENTED"
    PARTIALLY_IMPLEMENTED = "PARTIALLY_IMPLEMENTED"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
    NOT_VERIFIED = "NOT_VERIFIED"
    BLOCKED = "BLOCKED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


@dataclass
class ReviewFinding:
    finding_id: str
    category: str
    severity: str
    message: str
    status: ReviewStatus = ReviewStatus.NOT_VERIFIED
    requirement_id: str | None = None
    path: str | None = None


@dataclass
class ReviewReport:
    project_id: str
    findings: list[ReviewFinding] = field(default_factory=list)

    @property
    def blocking(self) -> list[ReviewFinding]:
        return [f for f in self.findings if f.severity in {"CRITICAL", "HIGH"}]


_SECRET_PATTERNS = (
    re.compile(r"(?i)(api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)


class ReviewEngine:
    """Performs conservative static review; runtime claims require evidence."""

    def review_paths(self, project_id: str, root: str | Path, paths: Iterable[str]) -> ReviewReport:
        report = ReviewReport(project_id=project_id)
        for index, relative in enumerate(paths, start=1):
            path = Path(root) / relative
            if not path.is_file():
                report.findings.append(ReviewFinding(
                    finding_id=f"REVIEW-{index:03d}", category="STRUCTURE",
                    severity="HIGH", message="Planned file does not exist.",
                    status=ReviewStatus.NOT_IMPLEMENTED, path=str(relative),
                ))
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                report.findings.append(ReviewFinding(
                    finding_id=f"REVIEW-{index:03d}", category="FILE",
                    severity="HIGH", message=f"Unable to inspect file: {exc}",
                    status=ReviewStatus.BLOCKED, path=str(relative),
                ))
                continue
            for pattern in _SECRET_PATTERNS:
                if pattern.search(text):
                    report.findings.append(ReviewFinding(
                        finding_id=f"REVIEW-{len(report.findings)+1:03d}",
                        category="SECURITY", severity="CRITICAL",
                        message="Possible hard-coded credential detected; value intentionally omitted.",
                        status=ReviewStatus.BLOCKED, path=str(relative),
                    ))
                    break
        return report
