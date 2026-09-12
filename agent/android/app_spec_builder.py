from __future__ import annotations

from dataclasses import dataclass
import re

from agent.planning import ProjectPlan
from agent.templates.android_template import AndroidProjectSpec


@dataclass(frozen=True)
class AndroidBuildIntent:
    """Validated Android implementation intent derived from a project plan."""

    spec: AndroidProjectSpec
    family: str
    rationale: tuple[str, ...]


class AndroidBuildIntentBuilder:
    """Converts a conservative project plan into deterministic Android metadata."""

    def build(self, plan: ProjectPlan) -> AndroidBuildIntent:
        if not isinstance(plan, ProjectPlan):
            raise TypeError("plan must be a ProjectPlan")

        name = self._project_name(plan.goal)
        package = self._package_name(name)
        mode = self._mode(plan)
        family = self._family(plan)

        rationale: list[str] = []
        if plan.accessibility_requirements:
            rationale.append("Accessibility requirements are carried into the Android specification.")
        if plan.security_requirements or plan.privacy_requirements:
            rationale.append("Security and privacy requirements remain mandatory implementation constraints.")
        if plan.research_required:
            rationale.append("Research is required before implementation when requirements remain unresolved.")

        return AndroidBuildIntent(
            spec=AndroidProjectSpec(
                project_name=name,
                package_name=package,
                mode=mode,
                accessibility_required=bool(plan.accessibility_requirements),
            ),
            family=family,
            rationale=tuple(rationale),
        )

    @staticmethod
    def _project_name(goal: str) -> str:
        words = re.findall(r"[A-Za-z0-9]+", goal or "")
        base = " ".join(words[:8]).strip() or "AI App"
        base = base.title()
        return base[:50].rstrip() if len(base) >= 2 else "AI App"

    @staticmethod
    def _package_name(project_name: str) -> str:
        words = re.findall(r"[a-z0-9]+", project_name.lower())
        suffix = "".join(words)[:30] or "app"
        return f"com.aiappbuilder.{suffix}"

    @staticmethod
    def _mode(plan: ProjectPlan) -> str:
        text = " ".join(
            plan.functional_requirements
            + plan.non_functional_requirements
            + plan.components
        ).lower()
        if any(token in text for token in ("api", "online", "web", "server", "cloud")):
            return "online"
        return "offline"

    @staticmethod
    def _family(plan: ProjectPlan) -> str:
        text = " ".join(plan.functional_requirements + [plan.goal]).lower()
        if any(token in text for token in ("form", "login", "register", "submit")):
            return "form"
        if any(token in text for token in ("database", "record", "inventory", "data")):
            return "database"
        if any(token in text for token in ("api", "server", "http")):
            return "api_client"
        if any(token in text for token in ("article", "news", "content", "blog")):
            return "content"
        if any(token in text for token in ("calculator", "converter", "utility", "tool")):
            return "utility"
        return "general"
