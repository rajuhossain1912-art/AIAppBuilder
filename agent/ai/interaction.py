from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Protocol
import uuid


@dataclass(frozen=True)
class AIResponse:
    request_id: str
    provider: str
    purpose: str
    text: str
    received_at: str
    metadata: dict[str, str] = field(default_factory=dict)


class AIProvider(Protocol):
    """Provider contract. Implementations must enforce their own authorization."""

    name: str

    def complete(self, *, purpose: str, prompt: str) -> str:
        ...


class AIInteraction:
    """Provider-independent interaction boundary with traceable request IDs."""

    def __init__(self, provider: AIProvider) -> None:
        self.provider = provider

    def request(self, *, purpose: str, prompt: str) -> AIResponse:
        if not isinstance(purpose, str) or not purpose.strip():
            raise ValueError("purpose must not be empty")
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("prompt must not be empty")
        provider_name = getattr(self.provider, "name", None)
        if not isinstance(provider_name, str) or not provider_name.strip():
            raise ValueError("provider must expose a non-empty name")

        text = self.provider.complete(purpose=purpose.strip(), prompt=prompt)
        if not isinstance(text, str):
            raise TypeError("AI provider must return text")

        return AIResponse(
            request_id=f"AI-{uuid.uuid4().hex}",
            provider=provider_name.strip(),
            purpose=purpose.strip(),
            text=text,
            received_at=datetime.now(timezone.utc).isoformat(),
        )
