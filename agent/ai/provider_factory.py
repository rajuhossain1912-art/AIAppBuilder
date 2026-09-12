from __future__ import annotations

import os

from .http_provider import HTTPAIProvider
from .mock_provider import MockAIProvider


def create_ai_provider(*, allow_mock: bool = False):
    """Create the configured production provider, or an explicit test mock.

    Production use fails closed when no external provider is configured. The
    mock is available only when the caller explicitly opts into it.
    """
    provider_name = os.getenv("AIAPPBUILDER_AI_PROVIDER", "http").strip().lower()
    if provider_name == "mock":
        if not allow_mock:
            raise RuntimeError("Mock AI provider is disabled for production use")
        return MockAIProvider()
    if provider_name == "http":
        return HTTPAIProvider()
    raise RuntimeError(f"Unsupported AI provider: {provider_name}")
