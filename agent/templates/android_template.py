from __future__ import annotations

from dataclasses import dataclass
import re


class AndroidTemplateError(ValueError):
    """Raised when an Android project specification is invalid."""


@dataclass(frozen=True)
class AndroidProjectSpec:
    """Portable metadata used to select a safe Android starter template."""

    project_name: str
    package_name: str
    mode: str = "offline"
    min_sdk: int = 24
    target_sdk: int = 35
    accessibility_required: bool = True

    def __post_init__(self) -> None:
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_ ]{1,49}", self.project_name.strip()):
            raise AndroidTemplateError("project_name must be 2-50 characters")
        if not re.fullmatch(r"[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*){1,4}", self.package_name):
            raise AndroidTemplateError("package_name must be a valid Android-style package")
        if self.mode not in {"offline", "online", "hybrid"}:
            raise AndroidTemplateError("mode must be offline, online, or hybrid")
        if not 21 <= self.min_sdk <= self.target_sdk <= 36:
            raise AndroidTemplateError("SDK values must satisfy 21 <= min_sdk <= target_sdk <= 36")


class AndroidTemplateCatalog:
    """Selects deterministic starter templates without pretending they are final apps."""

    SUPPORTED_MODES = ("offline", "online", "hybrid")
    SUPPORTED_FAMILIES = (
        "general",
        "form",
        "database",
        "content",
        "utility",
        "api_client",
    )

    def choose(self, *, mode: str, family: str = "general") -> str:
        if mode not in self.SUPPORTED_MODES:
            raise AndroidTemplateError(f"Unsupported mode: {mode}")
        if family not in self.SUPPORTED_FAMILIES:
            raise AndroidTemplateError(f"Unsupported app family: {family}")
        return f"android-{mode}-{family}"

    def describe(self, template_id: str) -> dict[str, str]:
        parts = template_id.split("-", 2)
        if len(parts) != 3 or parts[0] != "android":
            raise AndroidTemplateError("Invalid Android template id")
        mode, family = parts[1], parts[2]
        self.choose(mode=mode, family=family)
        return {
            "template_id": template_id,
            "mode": mode,
            "family": family,
            "status": "starter-template",
            "note": "Template selection is not evidence of build or functional correctness.",
        }
