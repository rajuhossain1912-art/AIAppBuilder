from __future__ import annotations

from typing import Optional

from .state_model import (
    LifecycleState,
    OrchestratorState,
    OrchestratorStateManager,
    StateTransitionError,
)
from .state_store import OrchestratorStateStore, StateStoreError


class OrchestratorError(RuntimeError):
    """Base error for orchestrator coordination failures."""


class Orchestrator:
    """Central lifecycle coordinator for one AIAppBuilder project."""

    def __init__(
        self,
        project_id: str,
        state_path: str,
    ) -> None:
        self.project_id = project_id
        self.state_manager = OrchestratorStateManager(project_id)
        self.state_store = OrchestratorStateStore(state_path)

    @property
    def state(self) -> OrchestratorState:
        return self.state_manager.state

    @property
    def current_state(self) -> LifecycleState:
        return self.state_manager.current_state

    def start(self) -> OrchestratorState:
        """Start or restore the project lifecycle."""
        try:
            restored_state = self.state_store.load()
        except StateStoreError:
            restored_state = None

        if restored_state is not None:
            if restored_state.project_id != self.project_id:
                raise OrchestratorError(
                    "Stored state belongs to a different project"
                )

            self.state_manager.state = restored_state
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

    def _persist(self) -> None:
        try:
            self.state_store.save(self.state_manager.state)
        except StateStoreError as exc:
            raise OrchestratorError(
                "Unable to persist orchestrator state"
            ) from exc
