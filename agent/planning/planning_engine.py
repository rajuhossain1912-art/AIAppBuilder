from __future__ import annotations

from dataclasses import dataclass, field

from agent.requirements import RequirementSet


@dataclass
class ProjectPlan:
    """A traceable implementation plan derived from confirmed requirements."""

    goal: str
    functional_requirements: list[str] = field(default_factory=list)
    non_functional_requirements: list[str] = field(default_factory=list)
    accessibility_requirements: list[str] = field(default_factory=list)
    security_requirements: list[str] = field(default_factory=list)
    privacy_requirements: list[str] = field(default_factory=list)
    compatibility_requirements: list[str] = field(default_factory=list)
    capabilities: list[str] = field(default_factory=list)
    components: list[str] = field(default_factory=list)
    research_required: bool = False
    build_required: bool = True
    test_required: bool = True
    delivery_required: bool = True
    risks: list[str] = field(default_factory=list)
    unresolved_questions: list[str] = field(default_factory=list)


class PlanningEngine:
    """Builds a composable plan without reducing apps to fixed templates."""

    def create_plan(self, requirements: RequirementSet) -> ProjectPlan:
        if not isinstance(requirements, RequirementSet):
            raise TypeError("requirements must be a RequirementSet")

        capability_keys = [match.key for match in requirements.capabilities]
        components = [
            "requirements", "capability_analysis", "planning", "design_system",
            "generation", "review", "build", "test", "verification", "delivery",
        ]
        research_required = bool(requirements.unresolved_questions)
        risks = []
        if requirements.compatibility:
            risks.append("Compatibility requirements must be validated against the target Android range.")
        if requirements.accessibility:
            risks.append("Accessibility workflows must be tested with a screen reader where applicable.")
        if research_required:
            risks.append("Unresolved requirements must be clarified before substantial generation.")
        if any(match.key == "online_service" for match in requirements.capabilities):
            risks.append("Online features require validated public APIs or explicitly configured external services.")
        if any(match.key in {"video", "audio", "image"} for match in requirements.capabilities):
            risks.append("Media-generation features require a real supported backend; unavailable services must not be simulated as working.")

        return ProjectPlan(
            goal=requirements.normalized_request,
            functional_requirements=list(requirements.functional),
            non_functional_requirements=list(requirements.non_functional),
            accessibility_requirements=list(requirements.accessibility),
            security_requirements=list(requirements.security),
            privacy_requirements=list(requirements.privacy),
            compatibility_requirements=list(requirements.compatibility),
            capabilities=capability_keys,
            components=components,
            research_required=research_required,
            risks=risks,
            unresolved_questions=list(requirements.unresolved_questions),
        )
