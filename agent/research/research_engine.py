from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


CONFIDENCE = {"HIGH", "MEDIUM", "LOW", "UNKNOWN"}


class ResearchError(ValueError):
    """Raised when a research record is invalid."""


@dataclass
class ResearchRecord:
    research_id: str
    question: str
    reason: str = ""
    date: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    sources: list[str] = field(default_factory=list)
    findings: list[str] = field(default_factory=list)
    confidence: str = "UNKNOWN"
    limitations: list[str] = field(default_factory=list)
    decision_impact: Optional[str] = None

    def __post_init__(self) -> None:
        for name in ("research_id", "question"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ResearchError(f"{name} must not be empty")
            setattr(self, name, value.strip())
        if self.confidence not in CONFIDENCE:
            raise ResearchError(f"Invalid confidence: {self.confidence}")

    def add_source(self, source: str) -> None:
        self._add_unique(self.sources, source)

    def add_finding(self, finding: str) -> None:
        self._add_unique(self.findings, finding)

    def add_limitation(self, limitation: str) -> None:
        self._add_unique(self.limitations, limitation)

    @staticmethod
    def _add_unique(items: list[str], value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ResearchError("record value must not be empty")
        value = value.strip()
        if value not in items:
            items.append(value)

    def to_dict(self) -> dict:
        return {
            "research_id": self.research_id,
            "question": self.question,
            "reason": self.reason,
            "date": self.date,
            "sources": list(self.sources),
            "findings": list(self.findings),
            "confidence": self.confidence,
            "limitations": list(self.limitations),
            "decision_impact": self.decision_impact,
        }


class ResearchEngine:
    """Creates evidence records; it does not invent external facts."""

    def create_record(self, research_id: str, question: str, reason: str = "") -> ResearchRecord:
        return ResearchRecord(research_id=research_id, question=question, reason=reason)

    def add_verified_finding(
        self,
        record: ResearchRecord,
        finding: str,
        source: str,
        confidence: str = "MEDIUM",
    ) -> ResearchRecord:
        if not isinstance(record, ResearchRecord):
            raise TypeError("record must be a ResearchRecord")
        if confidence not in CONFIDENCE:
            raise ResearchError(f"Invalid confidence: {confidence}")
        record.add_source(source)
        record.add_finding(finding)
        record.confidence = confidence
        return record
