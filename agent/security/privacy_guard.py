from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable


class PrivacyDecision:
    ALLOW = "ALLOW"
    DENY = "DENY"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"


@dataclass(frozen=True)
class PrivacyReport:
    status: str
    reasons: tuple[str, ...] = ()
    inspected_files: tuple[str, ...] = ()
    findings: tuple[str, ...] = ()

    @property
    def passed(self) -> bool:
        return self.status == "VERIFIED"


# These patterns are deliberately conservative. They flag common direct data-exfiltration
# mechanisms without pretending that static analysis can prove runtime privacy by itself.
_EXTERNAL_EGRESS_PATTERNS = (
    re.compile(r"(?i)HttpURLConnection"),
    re.compile(r"(?i)\bOkHttpClient\b"),
    re.compile(r"(?i)\bRetrofit\b"),
    re.compile(r"(?i)\bWebSocket\b"),
    re.compile(r"(?i)\bURL\s*\("),
    re.compile(r"(?i)\bfetch\s*\("),
    re.compile(r"(?i)\baxios\b"),
    re.compile(r"(?i)\brequests\.(get|post|put|patch|delete)\b"),
)

_SENSITIVE_DATA_PATTERNS = (
    re.compile(r"(?i)password|passwd|secret|private[_ -]?key|access[_ -]?token|refresh[_ -]?token"),
    re.compile(r"(?i)national[_ -]?id|nid|passport|birth[_ -]?date|date[_ -]?of[_ -]?birth"),
    re.compile(r"(?i)phone[_ -]?number|email[_ -]?address|home[_ -]?address"),
    re.compile(r"(?i)health|medical|diagnos|pregnan|disability"),
)

_SECRET_LITERAL = re.compile(
    r"(?i)(api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*['\"][^'\"]{8,}['\"]"
)


class PrivacyGuard:
    """Conservative privacy gate: collect locally when possible, minimize disclosure, and block unapproved egress."""

    def inspect_source(self, project_root: str | Path, paths: Iterable[str]) -> PrivacyReport:
        root = Path(project_root).resolve()
        inspected: list[str] = []
        findings: list[str] = []
        reasons: list[str] = []

        for relative in paths:
            path = root / relative
            if not path.is_file():
                findings.append(f"Missing source file: {relative}")
                continue
            inspected.append(str(relative))
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                findings.append(f"Unable to inspect {relative}: {exc}")
                continue

            if _SECRET_LITERAL.search(text):
                findings.append(f"Possible hard-coded credential in {relative}; value omitted.")

            has_egress = any(pattern.search(text) for pattern in _EXTERNAL_EGRESS_PATTERNS)
            has_sensitive_terms = any(pattern.search(text) for pattern in _SENSITIVE_DATA_PATTERNS)
            if has_egress and has_sensitive_terms:
                findings.append(
                    f"Potential sensitive-data egress path detected in {relative}; explicit privacy policy evidence is required."
                )

        if findings:
            reasons.append("Privacy review found a disclosure risk that cannot be cleared by static inspection alone.")
            return PrivacyReport("BLOCKED", tuple(reasons), tuple(inspected), tuple(findings))

        return PrivacyReport("VERIFIED", (), tuple(inspected), ())

    def decide_disclosure(
        self,
        *,
        data_category: str,
        purpose: str,
        recipient: str | None,
        necessary: bool,
        user_approved: bool,
    ) -> str:
        """Return the minimum safe decision for an attempted disclosure.

        Data availability never implies permission to disclose it. Disclosure is denied
        when it is unnecessary; otherwise explicit approval is required for a recipient.
        """
        if not data_category.strip() or not purpose.strip():
            return PrivacyDecision.DENY
        if not necessary:
            return PrivacyDecision.DENY
        if not recipient:
            return PrivacyDecision.DENY
        if not user_approved:
            return PrivacyDecision.REQUIRE_APPROVAL
        return PrivacyDecision.ALLOW
