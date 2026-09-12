from __future__ import annotations


class MockAIProvider:
    """Deterministic provider used for tests; never contacts an external service."""

    name = "mock"

    def complete(self, *, purpose: str, prompt: str) -> str:
        if not purpose.strip() or not prompt.strip():
            raise ValueError("purpose and prompt must not be empty")
        return f"MOCK:{purpose.strip()}:{prompt.strip()}"
