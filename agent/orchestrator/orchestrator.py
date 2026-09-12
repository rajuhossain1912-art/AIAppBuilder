from __future__ import annotations

from datetime import datetime, timezone
import os
from pathlib import Path
from typing import Optional

from agent.passport import ProjectPassport, ProjectPassportStore

from .state_model import (
    LifecycleState,
    OrchestratorState,
    OrchestratorStateManager,
    StateTransitionError,
)
from .state_store import (
    OrchestratorStateStore,
    StateStoreError,
    StateStoreMissingError,
)


class OrchestratorError(RuntimeError):
    """Base error for orchestrator coordination failures."""


class Orchestrator:
    """Central lifecycle coordinator for one AIAppBuilder project."""

    def __init__(self, project_id: str, state_path: str) -> None:
        self.project_id = project_id
        self.state_manager = OrchestratorStateManager(project_id)
        self.state_store = OrchestratorStateStore(state_path)
        self.passport_store = ProjectPassportStore(
            Path(state_path).with_name("project_passport.json")
        )
        self._last_audit_signature: tuple | None = None

    @property
    def state(self) -> OrchestratorState:
        return self.state_manager.state

    @property
    def current_state(self) -> LifecycleState:
        return self.state_manager.current_state

    def start(self) -> OrchestratorState:
        """Start or restore lifecycle state and its portable Project Passport."""
        try:
            restored_state = self.state_store.load()
        except StateStoreMissingError:
            restored_state = None
        except StateStoreError as exc:
            raise OrchestratorError(
                "Unable to restore orchestrator state"
            ) from exc

        if restored_state is not None:
            if restored_state.project_id != self.project_id:
                raise OrchestratorError(
                    "Stored state belongs to a different project"
                )
            self.state_manager.state = restored_state
            try:
                self._sync_passport()
            except (OSError, ValueError) as exc:
                raise OrchestratorError(
                    "Unable to restore or update Project Passport"
                ) from exc
            return restored_state

        self._persist()
        return self.state

    def transition_to(self, target: LifecycleState) -> OrchestratorState:
        """Perform one validated lifecycle transition."""
        try:
            state = self.state_manager.transition_to(target)
        except StateTransitionError as exc:
            raise OrchestratorError(str(exc)) from exc

        self._persist()
        return state

    def set_task(self, task: Optional[str]) -> None:
        self.state_manager.set_current_task(task)
        self._persist()

    def complete_task(self, task: str) -> None:
        self.state_manager.add_completed_task(task)
        self._persist()

    def queue_task(self, task: str) -> None:
        self.state_manager.add_pending_task(task)
        self._persist()

    def block_task(self, task: str) -> None:
        self.state_manager.add_blocked_task(task)
        self._persist()

    def record_error(self, error: str) -> None:
        self.state_manager.add_error(error)
        self._persist()

    def request_approval(self, approval: str) -> None:
        self.state_manager.add_required_approval(approval)
        self._persist()

    def receive_approval(self, approval: str) -> None:
        self.state_manager.add_received_approval(approval)
        self._persist()

    def record_success(self, operation: str) -> None:
        self.state_manager.mark_success(operation)
        self._persist()

    def record_verified_result(self, result: str) -> None:
        self.state_manager.mark_verified(result)
        self._persist()

    def increment_retry(self) -> int:
        count = self.state_manager.increment_retry()
        self._persist()
        return count

    def reset_retry(self) -> None:
        self.state_manager.reset_retry()
        self._persist()

    def snapshot(self) -> dict:
        return self.state_manager.snapshot()

    def _audit_signature(self) -> tuple:
        state = self.state
        return (
            state.current_state.value,
            state.previous_state.value if state.previous_state else None,
            state.current_task,
            tuple(state.completed_tasks),
            tuple(state.pending_tasks),
            tuple(state.blocked_tasks),
            tuple(state.errors),
            state.retry_count,
            tuple(state.required_approvals),
            tuple(state.received_approvals),
            state.last_successful_operation,
            state.last_verified_result,
        )

    def _sync_passport(self) -> None:
        try:
            passport = self.passport_store.load()
        except FileNotFoundError:
            now = datetime.now(timezone.utc).isoformat()
            passport = ProjectPassport(
                project_id=self.project_id,
                project_name=self.project_id,
                created_at=now,
            )

        now = datetime.now(timezone.utc).isoformat()
        passport.project_id = self.project_id
        passport.project_name = passport.project_name or self.project_id
        passport.updated_at = now
        passport.current_state = self.state.current_state.value
        passport.approved = "requirements_and_plan" in self.state.received_approvals
        passport.completed_operations = list(self.state.completed_tasks)
        passport.blocked_operations = list(self.state.blocked_tasks)
        passport.known_errors = list(self.state.errors)
        passport.recovery_notes = [
            f"Lifecycle state persisted at {now}",
            f"Retry count: {self.state.retry_count}",
        ]

        completed = set(self.state.completed_tasks)
        if "build" in completed or "build_succeeded" in completed:
            passport.build_status = "VERIFIED"
        if "test" in completed or "tests_passed" in completed:
            passport.test_status = "VERIFIED"
        if "android_generation" in completed or "android_source_generated" in completed:
            passport.generated_revision = passport.generated_revision or os.environ.get(
                "GITHUB_SHA", "local-workspace"
            )
        if "requirements_and_plan_ready" in completed:
            passport.requirements_summary = "Requirements and plan prepared and recorded."
        if "review" in completed or "review_passed" in completed:
            passport.recovery_notes.append("Review completed without release-blocking findings.")

        if self.state.last_verified_result:
            passport.verification_status = "VERIFIED"
            passport.artifact_sha256 = self.state.last_verified_result
            passport.generated_revision = f"artifact:{self.state.last_verified_result}"
            passport.accessibility_status = "VERIFIED" if (
                "verification" in completed or "delivery" in completed
            ) else passport.accessibility_status

        if self.state.current_state == LifecycleState.COMPLETED:
            passport.delivery_status = "READY"
            passport.build_provider = (
                "GitHub Actions" if os.environ.get("GITHUB_ACTIONS") == "true" else "local"
            )
            passport.build_reference = os.environ.get(
                "GITHUB_RUN_ID", passport.build_reference or "local-workspace"
            )

        if os.environ.get("GITHUB_SHA"):
            passport.source_revision = os.environ["GITHUB_SHA"]

        signature = self._audit_signature()
        if signature != self._last_audit_signature:
            passport.audit_log.append(
                {
                    "timestamp": now,
                    "state": self.state.current_state.value,
                    "previous_state": (
                        self.state.previous_state.value
                        if self.state.previous_state else None
                    ),
                    "current_task": self.state.current_task,
                    "completed_operations": list(self.state.completed_tasks),
                    "blocked_operations": list(self.state.blocked_tasks),
                    "retry_count": self.state.retry_count,
                    "last_successful_operation": self.state.last_successful_operation,
                    "last_verified_result": self.state.last_verified_result,
                }
            )
            # Keep the passport portable and bounded while retaining the recent
            # lifecycle history needed for recovery and audit.
            passport.audit_log = passport.audit_log[-1000:]
            self._last_audit_signature = signature

        self.passport_store.save(passport)

    def _persist(self) -> None:
        try:
            self.state_store.save(self.state_manager.state)
            self._sync_passport()
        except (StateStoreError, OSError, ValueError) as exc:
            raise OrchestratorError(
                "Unable to persist orchestrator state or Project Passport"
            ) from exc
