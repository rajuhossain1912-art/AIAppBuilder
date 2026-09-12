from __future__ import annotations

from dataclasses import dataclass, field

from .capability_catalog import CapabilityMatch, classify_capabilities


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
    capabilities: list[CapabilityMatch] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not isinstance(self.original_request, str) or not self.original_request.strip():
            raise ValueError("original_request must not be empty")
        self.original_request = self.original_request.strip()
        if not self.normalized_request:
            self.normalized_request = self.original_request


class RequirementEngine:
    """First-pass requirement intake for a general-purpose app builder.

    Capability classification is compositional: an app can combine news,
    audio, video, business, education and other capabilities. It is not a
    fixed template registry, and unmatched ideas are preserved as general.
    """

    ACCESSIBILITY_HINTS = (
        "talkback", "accessibility", "accessible", "screen reader", "blind", "visually impaired"
    )
    OFFLINE_HINTS = ("offline", "without internet", "no internet")
    ONLINE_HINTS = ("online", "internet", "api", "server", "cloud")

    def analyze(self, request: str) -> RequirementSet:
        result = RequirementSet(original_request=request)
        text = request.strip()
        lowered = text.casefold()
        result.normalized_request = " ".join(text.split())
        result.capabilities = classify_capabilities(text)

        if any(hint in lowered for hint in self.ACCESSIBILITY_HINTS):
            result.accessibility.append("Support accessible interaction and screen-reader workflows.")
        if any(hint in lowered for hint in self.OFFLINE_HINTS):
            result.compatibility.append("Offline operation is required for at least part of the application.")
        if any(hint in lowered for hint in self.ONLINE_HINTS):
            result.compatibility.append("Online/network functionality is required for at least part of the application.")

        labels = ", ".join(match.label for match in result.capabilities)
        result.functional.append(f"Compose the requested app from detected capabilities: {labels}.")
        return result
