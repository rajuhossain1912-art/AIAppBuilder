from __future__ import annotations

from dataclasses import dataclass

from agent.requirements import RequirementSet

from .android_template import AndroidProjectSpec, AndroidTemplateCatalog


@dataclass(frozen=True)
class TemplateDecision:
    spec: AndroidProjectSpec
    template_id: str
    confidence: str
    reasons: tuple[str, ...]


class AppIntentClassifier:
    """Conservative classifier used only for starter-template selection."""

    FAMILY_HINTS = {
        "database": ("database", "inventory", "stock", "record", "customer list"),
        "form": ("form", "registration", "survey", "application", "input"),
        "content": ("news", "article", "blog", "ebook", "content", "reader"),
        "utility": ("calculator", "converter", "timer", "note", "utility", "tool"),
        "api_client": ("api", "server", "cloud", "login", "sync", "online"),
    }

    def classify(self, requirements: RequirementSet, *, project_name: str, package_name: str) -> TemplateDecision:
        text = requirements.normalized_request.casefold()
        scores = {family: sum(1 for hint in hints if hint in text) for family, hints in self.FAMILY_HINTS.items()}
        family = max(scores, key=scores.get) if max(scores.values()) else "general"

        has_offline = any("offline" in item.casefold() for item in requirements.compatibility)
        has_online = any("online" in item.casefold() for item in requirements.compatibility)
        mode = "hybrid" if has_offline and has_online else "online" if has_online else "offline"
        reasons = tuple(f"{family} hint: {hint}" for hint in self.FAMILY_HINTS.get(family, ()) if hint in text)
        confidence = "medium" if reasons else "low"
        spec = AndroidProjectSpec(
            project_name=project_name,
            package_name=package_name,
            mode=mode,
            accessibility_required=True,
        )
        template_id = AndroidTemplateCatalog().choose(mode=mode, family=family)
        return TemplateDecision(spec, template_id, confidence, reasons)
