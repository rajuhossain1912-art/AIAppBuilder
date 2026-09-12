from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from agent.android.app_spec_builder import AndroidBuildIntent, AndroidBuildIntentBuilder
from agent.android.feature_generator import AndroidFeatureGenerator, GeneratedAndroidFeatures
from agent.android.project_generator import AndroidProjectGenerator, GeneratedAndroidProject
from agent.planning import ProjectPlan


class AndroidAppGenerationError(ValueError):
    """Raised when an Android app cannot be generated safely."""


@dataclass(frozen=True)
class GeneratedAndroidApp:
    intent: AndroidBuildIntent
    project: GeneratedAndroidProject
    features: GeneratedAndroidFeatures


class AndroidAppGenerator:
    """Connect planning, approval, Android mapping, project and feature generation."""

    def __init__(
        self,
        intent_builder: AndroidBuildIntentBuilder | None = None,
        project_generator: AndroidProjectGenerator | None = None,
        feature_generator: AndroidFeatureGenerator | None = None,
    ) -> None:
        self.intent_builder = intent_builder or AndroidBuildIntentBuilder()
        self.project_generator = project_generator or AndroidProjectGenerator()
        self.feature_generator = feature_generator or AndroidFeatureGenerator()

    def generate(
        self,
        plan: ProjectPlan,
        output_root: str | Path,
        approved: bool = False,
    ) -> GeneratedAndroidApp:
        if not isinstance(plan, ProjectPlan):
            raise TypeError("plan must be a ProjectPlan")
        if not approved:
            raise AndroidAppGenerationError(
                "Explicit approval is required before Android source generation."
            )

        intent = self.intent_builder.build(plan)
        output = Path(output_root).resolve()
        project = self.project_generator.generate(output, intent.spec)
        features = self.feature_generator.generate(project.root, intent)
        return GeneratedAndroidApp(intent=intent, project=project, features=features)
