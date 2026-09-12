from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from agent.pipeline import AgentPipeline, IntakeResult

from .orchestrator import Orchestrator
from .state_model import LifecycleState


@dataclass(frozen=True)
class OrchestratedIntake:
    intake: IntakeResult
    orchestrator: Orchestrator


class PipelineOrchestrator:
    """Bind client intake to durable lifecycle state without bypassing approval."""

    def __init__(self, project_id: str, state_path: str | Path) -> None:
        self.orchestrator = Orchestrator(project_id, str(state_path))
        self.pipeline = AgentPipeline()

    def intake(self, user_request: str) -> OrchestratedIntake:
        self.orchestrator.start()
        self.orchestrator.set_task("client_intake")
        self.orchestrator.transition_to(LifecycleState.UNDERSTANDING)
        result = self.pipeline.intake(user_request)
        self.orchestrator.complete_task("client_intake")

        if result.needs_user_confirmation:
            self.orchestrator.request_approval("requirements_and_plan")
            self.orchestrator.transition_to(LifecycleState.AWAITING_CONFIRMATION)
        else:
            self.orchestrator.transition_to(LifecycleState.PLANNING)
            self.orchestrator.record_success("requirements_and_plan_ready")

        return OrchestratedIntake(intake=result, orchestrator=self.orchestrator)

    def approve_and_generate(
        self,
        result: OrchestratedIntake,
        output_root: str | Path,
    ):
        if result.orchestrator is not self.orchestrator:
            raise ValueError("result belongs to a different orchestrator")
        if result.intake.needs_user_confirmation:
            raise ValueError("Clarifying questions must be resolved before generation")

        self.orchestrator.receive_approval("requirements_and_plan")
        self.orchestrator.transition_to(LifecycleState.GENERATING)
        self.orchestrator.set_task("android_generation")
        try:
            generated = self.pipeline.generate_android(
                result.intake,
                output_root,
                approved=True,
            )
        except Exception as exc:
            self.orchestrator.record_error(str(exc))
            self.orchestrator.transition_to(LifecycleState.FIXING)
            raise

        self.orchestrator.complete_task("android_generation")
        self.orchestrator.record_success("android_source_generated")
        self.orchestrator.transition_to(LifecycleState.REVIEWING)
        return generated
