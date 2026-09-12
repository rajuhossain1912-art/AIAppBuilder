from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from agent.android.app_spec_builder import AndroidBuildIntent
from agent.android.capability_composer import AndroidCapabilityComposer


class AndroidFeatureGenerationError(ValueError):
    """Raised when a feature cannot be generated safely."""


@dataclass(frozen=True)
class GeneratedAndroidFeatures:
    files: tuple[str, ...]
    family: str
    capabilities: tuple[str, ...] = ()
    implemented_capabilities: tuple[str, ...] = ()
    unsupported_capabilities: tuple[str, ...] = ()


class AndroidFeatureGenerator:
    """Generate Android features by composing all requested capabilities."""

    def __init__(self, composer: AndroidCapabilityComposer | None = None) -> None:
        self.composer = composer or AndroidCapabilityComposer()

    def generate(self, project_root: str | Path, intent: AndroidBuildIntent) -> GeneratedAndroidFeatures:
        if not isinstance(intent, AndroidBuildIntent):
            raise TypeError("intent must be an AndroidBuildIntent")
        root = Path(project_root).resolve()
        if not root.is_dir():
            raise AndroidFeatureGenerationError("project_root must be an existing directory")

        package_path = Path(*intent.spec.package_name.split("."))
        activity = root / "app" / "src" / "main" / "java" / package_path / "MainActivity.java"
        if not activity.is_file():
            raise AndroidFeatureGenerationError("generated Android project is missing MainActivity.java")

        composed = self.composer.compose(intent)
        activity.write_text(composed.source, encoding="utf-8")
        return GeneratedAndroidFeatures(
            files=(str(activity.relative_to(root)),),
            family=intent.family,
            capabilities=composed.capabilities,
            implemented_capabilities=composed.implemented_capabilities,
            unsupported_capabilities=composed.unsupported_capabilities,
        )
