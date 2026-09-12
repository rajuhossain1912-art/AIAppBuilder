from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from agent.android import AndroidAppGenerator, GeneratedAndroidApp
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
        self.android_generator = AndroidAppGenerator()

    def intake(self, user_request: str) -> IntakeResult:
        brief = self.client_intake.start(user_request)
        plan = self.planning_engine.create_plan(brief.requirements)
        return IntakeResult(
            requirements=brief.requirements,
            plan=plan,
            needs_user_confirmation=not brief.ready_for_approval,
            client_brief=brief,
        )

    def generate_android(
        self,
        intake_result: IntakeResult,
        output_root: str | Path,
        approved: bool = False,
    ) -> GeneratedAndroidApp:
        """Generate Android source only after explicit approval."""
        if not isinstance(intake_result, IntakeResult):
            raise TypeError("intake_result must be an IntakeResult")
        return self.android_generator.generate(
            intake_result.plan,
            output_root,
            approved=approved,
        )
