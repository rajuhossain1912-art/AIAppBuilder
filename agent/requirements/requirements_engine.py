from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RequirementSet:
    """Preserves the original request and its structured interpretation."""

    original_request: str
    normalized_request: str = ""
    functional: list[str] = field(default_factory=list)
    non_functional: list[str] = field(default_factory=list)
    accessibility: list[str] = field(default_factory=list)
    security: list[str] = field(default_factory=list)
    privacy: list[str] = field(default_factory=list)
    compatibility: list[str] = field(default_factory=list)
    unresolved_questions: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not isinstance(self.original_request, str) or not self.original_request.strip():
            raise ValueError("original_request must not be empty")
        self.original_request = self.original_request.strip()
        if not self.normalized_request:
            self.normalized_request = self.original_request


class RequirementEngine:
    """Safe first-pass requirement intake.

    This component deliberately does not pretend to understand unstated
    requirements. It preserves the user's wording and only extracts
    high-confidence structural hints from it.
    """

    ACCESSIBILITY_HINTS = (
        "talkback",
        "accessibility",
        "accessible",
        "screen reader",
        "blind",
        "visually impaired",
    )
    OFFLINE_HINTS = ("offline", "without internet", "no internet")
    ONLINE_HINTS = ("online", "internet", "api", "server", "cloud")

    def analyze(self, request: str) -> RequirementSet:
        result = RequirementSet(original_request=request)
        text = request.strip()
        lowered = text.casefold()
        result.normalized_request = " ".join(text.split())

        if any(hint in lowered for hint in self.ACCESSIBILITY_HINTS):
            result.accessibility.append("Support accessible interaction and screen-reader workflows.")

        if any(hint in lowered for hint in self.OFFLINE_HINTS):
            result.compatibility.append("Offline operation is required for at least part of the application.")

        if any(hint in lowered for hint in self.ONLINE_HINTS):
            result.compatibility.append("Online/network functionality is required for at least part of the application.")

        if not result.functional:
            result.functional.append("Implement the functionality explicitly requested by the user.")

        return result
