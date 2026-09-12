from __future__ import annotations

from dataclasses import dataclass

from agent.planning import PlanningEngine, ProjectPlan
from agent.requirements import RequirementEngine, RequirementSet


@dataclass
class IntakeResult:
    requirements: RequirementSet
    plan: ProjectPlan
    needs_user_confirmation: bool


class AgentPipeline:
    """Deterministic intake/planning bridge used before consequential generation."""

    def __init__(self) -> None:
        self.requirements_engine = RequirementEngine()
        self.planning_engine = PlanningEngine()

    def intake(self, user_request: str) -> IntakeResult:
        requirements = self.requirements_engine.analyze(user_request)
        plan = self.planning_engine.create_plan(requirements)
        return IntakeResult(
            requirements=requirements,
            plan=plan,
            needs_user_confirmation=bool(
                requirements.unresolved_questions or requirements.assumptions
            ),
        )
