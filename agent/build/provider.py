from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class ProviderStatus(str, Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class BuildProviderInfo:
    provider_id: str
    display_name: str
    priority: int
    status: ProviderStatus = ProviderStatus.UNKNOWN
    supports_android: bool = False
    supports_source_storage: bool = False


class BuildProvider(Protocol):
    """Provider contract used to keep build infrastructure replaceable."""

    @property
    def info(self) -> BuildProviderInfo:
        ...

    def health_check(self) -> ProviderStatus:
        ...

    def build(self, project_reference: str) -> str:
        """Start a build and return a provider-specific build reference."""
        ...


class ProviderRegistry:
    """Selects the highest-priority healthy provider without hard-coding GitHub."""

    def __init__(self, providers: list[BuildProvider] | None = None) -> None:
        self._providers = list(providers or [])

    def register(self, provider: BuildProvider) -> None:
        self._providers.append(provider)

    def providers(self) -> tuple[BuildProvider, ...]:
        return tuple(sorted(self._providers, key=lambda item: item.info.priority))

    def select(self, android_only: bool = True) -> BuildProvider:
        candidates = self.providers()
        for provider in candidates:
            if android_only and not provider.info.supports_android:
                continue
            status = provider.health_check()
            if status == ProviderStatus.AVAILABLE:
                return provider
        raise RuntimeError("No healthy build provider is currently available")
