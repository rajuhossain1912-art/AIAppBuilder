from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class LifecycleState(str, Enum):
    RECEIVED = "RECEIVED"
    UNDERSTANDING = "UNDERSTANDING"
    AWAITING_CONFIRMATION = "AWAITING_CONFIRMATION"
    PLANNING = "PLANNING"
    RESEARCHING = "RESEARCHING"
    GENERATING = "GENERATING"
    REVIEWING = "REVIEWING"
    BUILDING = "BUILDING"
    TESTING = "TESTING"
    FIXING = "FIXING"
    VERIFYING = "VERIFYING"
    DELIVERING = "DELIVERING"
    COMPLETED = "COMPLETED"


class StateTransitionError(ValueError):
    """Raised when an invalid lifecycle transition is requested."""


@dataclass
class OrchestratorState:
    project_id: str
    current_state: LifecycleState = LifecycleState.RECEIVED
    previous_state: Optional[LifecycleState] = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    current_task: Optional[str] = None
    completed_tasks: list[str] = field(default_factory=list)
    pending_tasks: list[str] = field(default_factory=list)
    blocked_tasks: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    retry_count: int = 0
    required_approvals: list[str] = field(default_factory=list)
    received_approvals: list[str] = field(default_factory=list)
    last_successful_operation: Optional[str] = None
    last_verified_result: Optional[str] = None


ALLOWED_TRANSITIONS: dict[LifecycleState, set[LifecycleState]] = {
    LifecycleState.RECEIVED: {LifecycleState.UNDERSTANDING},
    LifecycleState.UNDERSTANDING: {
        LifecycleState.AWAITING_CONFIRMATION,
        LifecycleState.PLANNING,
    },
    LifecycleState.AWAITING_CONFIRMATION: {LifecycleState.PLANNING},
    LifecycleState.PLANNING: {
        LifecycleState.RESEARCHING,
        LifecycleState.GENERATING,
    },
    LifecycleState.RESEARCHING: {
        LifecycleState.GENERATING,
        LifecycleState.PLANNING,
    },
    LifecycleState.GENERATING: {LifecycleState.REVIEWING},
    LifecycleState.REVIEWING: {
        LifecycleState.BUILDING,
        LifecycleState.FIXING,
    },
    LifecycleState.BUILDING: {
        LifecycleState.TESTING,
        LifecycleState.FIXING,
    },
    LifecycleState.TESTING: {
        LifecycleState.VERIFYING,
        LifecycleState.FIXING,
    },
    LifecycleState.FIXING: {
        LifecycleState.BUILDING,
        LifecycleState.TESTING,
        LifecycleState.REVIEWING,
    },
    LifecycleState.VERIFYING: {
        LifecycleState.DELIVERING,
        LifecycleState.FIXING,
    },
    LifecycleState.DELIVERING: {LifecycleState.COMPLETED},
    LifecycleState.COMPLETED: set(),
}


class OrchestratorStateManager:
    """Controls valid lifecycle transitions for one project."""

    def __init__(self, project_id: str) -> None:
        if not isinstance(project_id, str) or not project_id.strip():
            raise ValueError("project_id must not be empty")

        self.state = OrchestratorState(project_id=project_id.strip())

    @property
    def current_state(self) -> LifecycleState:
        return self.state.current_state

    def can_transition_to(self, target: LifecycleState) -> bool:
        if not isinstance(target, LifecycleState):
            return False
        return target in ALLOWED_TRANSITIONS[self.state.current_state]

    def transition_to(self, target: LifecycleState) -> OrchestratorState:
        if not isinstance(target, LifecycleState):
            raise StateTransitionError("target must be a valid LifecycleState")

        if not self.can_transition_to(target):
            raise StateTransitionError(
                f"Invalid lifecycle transition: "
                f"{self.state.current_state.value} -> {target.value}"
            )

        self.state.previous_state = self.state.current_state
        self.state.current_state = target
        self.state.timestamp = datetime.now(timezone.utc).isoformat()
        return self.state

    def add_error(self, error: str) -> None:
        if isinstance(error, str) and error.strip():
            self.state.errors.append(error.strip())

    def increment_retry(self) -> int:
        self.state.retry_count += 1
        return self.state.retry_count

    def reset_retry(self) -> None:
        self.state.retry_count = 0

    def add_required_approval(self, approval: str) -> None:
        if isinstance(approval, str) and approval.strip():
            approval = approval.strip()
            if approval not in self.state.required_approvals:
                self.state.required_approvals.append(approval)

    def add_received_approval(self, approval: str) -> None:
        if isinstance(approval, str) and approval.strip():
            approval = approval.strip()
            if approval not in self.state.received_approvals:
                self.state.received_approvals.append(approval)

    def mark_success(self, operation: str) -> None:
        if not isinstance(operation, str) or not operation.strip():
            raise ValueError("operation must not be empty")
        self.state.last_successful_operation = operation.strip()

    def mark_verified(self, result: str) -> None:
        if not isinstance(result, str) or not result.strip():
            raise ValueError("result must not be empty")
        self.state.last_verified_result = result.strip()

    def set_current_task(self, task: Optional[str]) -> None:
        if task is not None and not isinstance(task, str):
            raise ValueError("task must be a string or None")
        self.state.current_task = task.strip() if task else None

    def add_completed_task(self, task: str) -> None:
        self._add_unique_task(self.state.completed_tasks, task)

    def add_pending_task(self, task: str) -> None:
        self._add_unique_task(self.state.pending_tasks, task)

    def add_blocked_task(self, task: str) -> None:
        self._add_unique_task(self.state.blocked_tasks, task)

    @staticmethod
    def _add_unique_task(items: list[str], task: str) -> None:
        if not isinstance(task, str) or not task.strip():
            raise ValueError("task must not be empty")
        task = task.strip()
        if task not in items:
            items.append(task)

    def snapshot(self) -> dict:
        return {
            "project_id": self.state.project_id,
            "current_state": self.state.current_state.value,
            "previous_state": (
                self.state.previous_state.value
                if self.state.previous_state
                else None
            ),
            "timestamp": self.state.timestamp,
            "current_task": self.state.current_task,
            "completed_tasks": list(self.state.completed_tasks),
            "pending_tasks": list(self.state.pending_tasks),
            "blocked_tasks": list(self.state.blocked_tasks),
            "errors": list(self.state.errors),
            "retry_count": self.state.retry_count,
            "required_approvals": list(self.state.required_approvals),
            "received_approvals": list(self.state.received_approvals),
            "last_successful_operation": self.state.last_successful_operation,
            "last_verified_result": self.state.last_verified_result,
        }
