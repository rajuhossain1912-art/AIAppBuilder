from __future__ import annotations

from dataclasses import dataclass

from agent.client import ClientOrderBrief, ClientOrderIntake
from agent.planning import PlanningEngine, ProjectPlan
from agent.requirements import RequirementSet


@dataclass
class IntakeResult:
    requirements: RequirementSet
    plan: ProjectPlan
    needs_user_confirmation: bool
    client_brief: ClientOrderBrief | None = None


class AgentPipeline:
    """Conservative intake/planning bridge used before consequential generation."""

    def __init__(self) -> None:
        self.client_intake = ClientOrderIntake()
        self.planning_engine = PlanningEngine()

    def intake(self, user_request: str) -> IntakeResult:
        brief = self.client_intake.start(user_request)
        plan = self.planning_engine.create_plan(brief.requirements)
        return IntakeResult(
            requirements=brief.requirements,
            plan=plan,
            needs_user_confirmation=not brief.ready_for_approval,
            client_brief=brief,
        )
