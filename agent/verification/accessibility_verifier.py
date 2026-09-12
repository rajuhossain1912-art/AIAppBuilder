from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from .verification_executor import (
    VerificationEvidence,
    VerificationReport,
    VerificationStatus,
)


@dataclass(frozen=True)
class AccessibilityCheckResult:
    passed: bool
    detail: str


class AndroidAccessibilityVerifier:
    """Performs conservative static checks for basic TalkBack-friendly Android source."""

    _interactive = re.compile(r"\b(Button|EditText|ImageButton|CheckBox|Switch|RadioButton)\b")

    def verify_source(
        self,
        project_id: str,
        source_path: str | Path,
        required: bool = True,
    ) -> VerificationReport:
        report = VerificationReport(project_id=project_id)
        target = Path(source_path)
        if not target.is_file():
            report.evidence.append(
                VerificationEvidence(
                    evidence_id="ACCESSIBILITY-001",
                    check="ANDROID_SOURCE_EXISTS",
                    status=VerificationStatus.FAILED if required else VerificationStatus.BLOCKED,
                    detail="Android source file does not exist.",
                    source=str(target),
                )
            )
            return report

        source = target.read_text(encoding="utf-8")
        interactive_count = len(self._interactive.findall(source))
        content_description_count = source.count("setContentDescription") + source.count("android:contentDescription")

        if interactive_count == 0:
            report.evidence.append(
                VerificationEvidence(
                    evidence_id="ACCESSIBILITY-002",
                    check="INTERACTIVE_CONTROLS",
                    status=VerificationStatus.STATICALLY_VERIFIED,
                    detail="No standard interactive Android controls were detected; no control-label failure can be inferred from this check.",
                    source=str(target),
                )
            )
        elif content_description_count > 0:
            report.evidence.append(
                VerificationEvidence(
                    evidence_id="ACCESSIBILITY-003",
                    check="ACCESSIBLE_LABELING",
                    status=VerificationStatus.STATICALLY_VERIFIED,
                    detail="Interactive controls and at least one explicit content description were detected. Static checks cannot prove complete TalkBack behavior.",
                    source=str(target),
                )
            )
        else:
            report.evidence.append(
                VerificationEvidence(
                    evidence_id="ACCESSIBILITY-003",
                    check="ACCESSIBLE_LABELING",
                    status=VerificationStatus.FAILED if required else VerificationStatus.NOT_VERIFIED,
                    detail="Interactive controls were detected without an explicit content description in the generated source.",
                    source=str(target),
                )
            )
        return report
