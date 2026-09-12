from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PerformancePolicy:
    """Guardrails for responsive generated Android apps.

    The policy is intentionally conservative: generated apps must avoid obvious
    UI-thread blocking patterns and excessive repeated work. It does not claim
    runtime performance without runtime evidence.
    """

    max_source_file_bytes: int = 250_000
    max_repeated_ui_work: int = 20

    def validate_source(self, source: str) -> tuple[str, ...]:
        if not isinstance(source, str):
            raise TypeError("source must be a string")
        findings: list[str] = []
        if len(source.encode("utf-8")) > self.max_source_file_bytes:
            findings.append("Generated source file is unnecessarily large.")

        blocked = (
            ("Thread.sleep(", "Blocking sleep found in generated UI source."),
            ("SystemClock.sleep(", "Blocking system sleep found in generated UI source."),
            ("while (true)", "Unbounded UI loop found; generated apps must not spin indefinitely."),
            ("for (;;)" , "Unbounded loop found; generated apps must not spin indefinitely."),
        )
        for token, message in blocked:
            if token in source:
                findings.append(message)

        if source.count("setContentView(") > 1:
            findings.append("Multiple activity content resets detected; UI should be initialized once where possible.")
        return tuple(findings)

    def require_clean(self, source: str) -> None:
        findings = self.validate_source(source)
        if findings:
            raise ValueError("Performance policy failed: " + " | ".join(findings))
