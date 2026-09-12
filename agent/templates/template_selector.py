from __future__ import annotations

from agent.requirements.requirements_engine import RequirementSet

from .android_template import AndroidTemplateCatalog


class TemplateSelector:
    """Selects a conservative Android starter from explicit requirements."""

    def __init__(self, catalog: AndroidTemplateCatalog | None = None) -> None:
        self.catalog = catalog or AndroidTemplateCatalog()

    def select(self, requirements: RequirementSet) -> dict[str, str | bool]:
        if not isinstance(requirements, RequirementSet):
            raise TypeError("requirements must be a RequirementSet")

        joined = " ".join(requirements.functional).casefold()
        compatibility = " ".join(requirements.compatibility).casefold()

        if "api" in joined or "server" in joined or "cloud" in joined:
            family = "api_client"
        elif "database" in joined or "storage" in joined or "inventory" in joined:
            family = "database"
        elif "form" in joined or "registration" in joined:
            family = "form"
        elif "content" in joined or "article" in joined:
            family = "content"
        else:
            family = "general"

        has_offline = "offline" in compatibility
        has_online = "online" in compatibility
        mode = "hybrid" if has_offline and has_online else "online" if has_online else "offline"

        template_id = self.catalog.choose(mode=mode, family=family)
        return {
            "template_id": template_id,
            "mode": mode,
            "family": family,
            "accessibility_required": bool(requirements.accessibility),
            "requires_clarification": bool(requirements.unresolved_questions),
        }
