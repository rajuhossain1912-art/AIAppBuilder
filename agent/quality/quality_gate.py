from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class QualityGateResult:
    passed: bool
    reasons: tuple[str, ...]


class QualityGate:
    """Final safety gate: no delivery without explicit evidence."""

    def evaluate(
        self,
        *,
        build_passed: bool,
        tests_passed: bool,
        verification_passed: bool,
        approval_received: bool,
    ) -> QualityGateResult:
        reasons: list[str] = []
        if not approval_received:
            reasons.append("User approval is required before delivery")
        if not build_passed:
            reasons.append("A successful build is required")
        if not tests_passed:
            reasons.append("Passing tests are required")
        if not verification_passed:
            reasons.append("Verification evidence is required")
        return QualityGateResult(passed=not reasons, reasons=tuple(reasons))
