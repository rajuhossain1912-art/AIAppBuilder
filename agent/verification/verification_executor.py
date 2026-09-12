from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import hashlib


class VerificationStatus:
    VERIFIED = "VERIFIED"
    STATICALLY_VERIFIED = "STATICALLY_VERIFIED"
    NOT_VERIFIED = "NOT_VERIFIED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"


@dataclass
class VerificationEvidence:
    evidence_id: str
    check: str
    status: str
    detail: str
    source: str | None = None


@dataclass
class VerificationReport:
    project_id: str
    evidence: list[VerificationEvidence] = field(default_factory=list)

    @property
    def final_status(self) -> str:
        if any(item.status == VerificationStatus.FAILED for item in self.evidence):
            return VerificationStatus.FAILED
        if any(item.status == VerificationStatus.BLOCKED for item in self.evidence):
            return VerificationStatus.BLOCKED
        if not self.evidence:
            return VerificationStatus.NOT_VERIFIED
        if all(item.status in {VerificationStatus.VERIFIED, VerificationStatus.STATICALLY_VERIFIED} for item in self.evidence):
            return VerificationStatus.VERIFIED
        return VerificationStatus.NOT_VERIFIED

    @property
    def passed(self) -> bool:
        """Backward-compatible boolean view of a fully verified report."""
        return self.final_status == VerificationStatus.VERIFIED


class VerificationExecutor:
    """Collects factual local evidence without upgrading static checks to runtime proof."""

    def verify_file_exists(self, project_id: str, path: str | Path) -> VerificationReport:
        report = VerificationReport(project_id=project_id)
        target = Path(path)
        if target.is_file():
            report.evidence.append(VerificationEvidence(
                evidence_id="EVIDENCE-001", check="FILE_EXISTS",
                status=VerificationStatus.STATICALLY_VERIFIED,
                detail="File exists and is readable as a filesystem object.", source=str(target),
            ))
        else:
            report.evidence.append(VerificationEvidence(
                evidence_id="EVIDENCE-001", check="FILE_EXISTS",
                status=VerificationStatus.FAILED,
                detail="Expected file does not exist.", source=str(target),
            ))
        return report

    def hash_artifact(self, project_id: str, path: str | Path) -> VerificationReport:
        report = VerificationReport(project_id=project_id)
        target = Path(path)
        if not target.is_file():
            report.evidence.append(VerificationEvidence(
                evidence_id="EVIDENCE-002", check="ARTIFACT_HASH",
                status=VerificationStatus.FAILED,
                detail="Artifact does not exist; checksum was not produced.", source=str(target),
            ))
            return report
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        report.evidence.append(VerificationEvidence(
            evidence_id="EVIDENCE-002", check="ARTIFACT_HASH",
            status=VerificationStatus.VERIFIED,
            detail=f"SHA-256: {digest}", source=str(target),
        ))
        return report
