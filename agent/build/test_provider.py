import unittest

from agent.build.provider import (
    BuildProviderInfo,
    ProviderRegistry,
    ProviderStatus,
)


class FakeProvider:
    def __init__(self, provider_id: str, priority: int, status: ProviderStatus) -> None:
        self._info = BuildProviderInfo(
            provider_id=provider_id,
            display_name=provider_id,
            priority=priority,
            status=status,
            supports_android=True,
        )
        self.status = status

    @property
    def info(self) -> BuildProviderInfo:
        return self._info

    def health_check(self) -> ProviderStatus:
        return self.status

    def build(self, project_reference: str) -> str:
        return f"{self.info.provider_id}:{project_reference}"


class ProviderRegistryTests(unittest.TestCase):
    def test_selects_healthy_highest_priority_provider(self):
        registry = ProviderRegistry([
            FakeProvider("backup", 20, ProviderStatus.AVAILABLE),
            FakeProvider("primary", 10, ProviderStatus.AVAILABLE),
        ])
        self.assertEqual(registry.select().info.provider_id, "primary")

    def test_falls_back_when_primary_is_unavailable(self):
        registry = ProviderRegistry([
            FakeProvider("primary", 10, ProviderStatus.UNAVAILABLE),
            FakeProvider("backup", 20, ProviderStatus.AVAILABLE),
        ])
        self.assertEqual(registry.select().info.provider_id, "backup")

    def test_fails_honestly_when_no_provider_is_healthy(self):
        registry = ProviderRegistry([
            FakeProvider("primary", 10, ProviderStatus.UNAVAILABLE),
            FakeProvider("backup", 20, ProviderStatus.UNKNOWN),
        ])
        with self.assertRaises(RuntimeError):
            registry.select()


if __name__ == "__main__":
    unittest.main()
