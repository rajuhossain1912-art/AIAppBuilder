from __future__ import annotations

import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from .state_model import LifecycleState, OrchestratorState


class StateStoreError(RuntimeError):
    """Raised when orchestrator state cannot be safely stored or loaded."""


class OrchestratorStateStore:
    """Persists one project's orchestrator state as structured JSON."""

    def __init__(self, state_path: str | Path) -> None:
        path = Path(state_path)

        if not str(path).strip():
            raise ValueError("state_path must not be empty")

        self.path = path

    def save(self, state: OrchestratorState) -> None:
        """Atomically save the supplied state to disk."""
        self.path.parent.mkdir(parents=True, exist_ok=True)

        payload = self._serialize(state)

        try:
            with NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.path.parent,
                prefix=f".{self.path.name}.",
                suffix=".tmp",
                delete=False,
            ) as temporary_file:
                temporary_path = Path(temporary_file.name)
                json.dump(
                    payload,
                    temporary_file,
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
                temporary_file.write("\n")
                temporary_file.flush()
                os.fsync(temporary_file.fileno())

            os.replace(temporary_path, self.path)

        except OSError as exc:
            if "temporary_path" in locals():
                try:
                    temporary_path.unlink(missing_ok=True)
                except OSError:
                    pass

            raise StateStoreError(
                f"Unable to save orchestrator state: {self.path}"
            ) from exc

    def load(self) -> OrchestratorState:
        """Load and validate orchestrator state from disk."""
        if not self.path.exists():
            raise StateStoreError(
                f"Orchestrator state file does not exist: {self.path}"
            )

        try:
            with self.path.open("r", encoding="utf-8") as state_file:
                payload: Any = json.load(state_file)
        except (OSError, json.JSONDecodeError) as exc:
            raise StateStoreError(
                f"Unable to read orchestrator state: {self.path}"
            ) from exc

        return self._deserialize(payload)

    @staticmethod
    def _serialize(state: OrchestratorState) -> dict[str, Any]:
        return {
            "project_id": state.project_id,
            "current_state": state.current_state.value,
            "previous_state": (
                state.previous_state.value
                if state.previous_state is not None
                else None
            ),
            "timestamp": state.timestamp,
            "current_task": state.current_task,
            "completed_tasks": list(state.completed_tasks),
            "pending_tasks": list(state.pending_tasks),
            "blocked_tasks": list(state.blocked_tasks),
            "errors": list(state.errors),
            "retry_count": state.retry_count,
            "required_approvals": list(state.required_approvals),
            "received_approvals": list(state.received_approvals),
            "last_successful_operation": state.last_successful_operation,
            "last_verified_result": state.last_verified_result,
        }

    @staticmethod
    def _deserialize(payload: Any) -> OrchestratorState:
        if not isinstance(payload, dict):
            raise StateStoreError("Orchestrator state must be a JSON object")

        project_id = payload.get("project_id")
        current_state = payload.get("current_state")

        if not isinstance(project_id, str) or not project_id.strip():
            raise StateStoreError("State is missing a valid project_id")

        if not isinstance(current_state, str):
            raise StateStoreError("State is missing current_state")

        try:
            lifecycle_state = LifecycleState(current_state)
        except ValueError as exc:
            raise StateStoreError(
                f"Unknown lifecycle state: {current_state}"
            ) from exc

        previous_state_value = payload.get("previous_state")
        previous_state = None

        if previous_state_value is not None:
            try:
                previous_state = LifecycleState(previous_state_value)
            except ValueError as exc:
                raise StateStoreError(
                    f"Unknown previous lifecycle state: {previous_state_value}"
                ) from exc

        retry_count = payload.get("retry_count", 0)

        if not isinstance(retry_count, int) or retry_count < 0:
            raise StateStoreError("retry_count must be a non-negative integer")

        return OrchestratorState(
            project_id=project_id.strip(),
            current_state=lifecycle_state,
            previous_state=previous_state,
            timestamp=str(payload.get("timestamp", "")),
            current_task=payload.get("current_task"),
            completed_tasks=_string_list(payload.get("completed_tasks")),
            pending_tasks=_string_list(payload.get("pending_tasks")),
            blocked_tasks=_string_list(payload.get("blocked_tasks")),
            errors=_string_list(payload.get("errors")),
            retry_count=retry_count,
            required_approvals=_string_list(
                payload.get("required_approvals")
            ),
            received_approvals=_string_list(
                payload.get("received_approvals")
            ),
            last_successful_operation=payload.get(
                "last_successful_operation"
            ),
            last_verified_result=payload.get("last_verified_result"),
        )


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []

    if not isinstance(value, list):
        raise StateStoreError("Expected a JSON list")

    if not all(isinstance(item, str) for item in value):
        raise StateStoreError("State list values must all be strings")

    return list(value)
