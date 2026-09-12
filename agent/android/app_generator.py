from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

from agent.android.app_spec_builder import AndroidBuildIntent, AndroidBuildIntentBuilder
from agent.android.feature_generator import AndroidFeatureGenerator, GeneratedAndroidFeatures
from agent.android.project_generator import AndroidProjectGenerator, GeneratedAndroidProject
from agent.planning import ProjectPlan
from agent.quality import PerformancePolicy
from agent.verification import AndroidAccessibilityVerifier, VerificationStatus
from agent.verification.requirements_verifier import RequirementsVerifier


class AndroidAppGenerationError(ValueError):
    """Raised when an Android app cannot be generated safely."""


@dataclass(frozen=True)
class GeneratedAndroidApp:
    intent: AndroidBuildIntent
    project: GeneratedAndroidProject
    features: GeneratedAndroidFeatures


class AndroidAppGenerator:
    """Connect planning, approval and mandatory pre-build quality gates."""

    def __init__(
        self,
        intent_builder: AndroidBuildIntentBuilder | None = None,
        project_generator: AndroidProjectGenerator | None = None,
        feature_generator: AndroidFeatureGenerator | None = None,
        performance_policy: PerformancePolicy | None = None,
        accessibility_verifier: AndroidAccessibilityVerifier | None = None,
        requirements_verifier: RequirementsVerifier | None = None,
    ) -> None:
        self.intent_builder = intent_builder or AndroidBuildIntentBuilder()
        self.project_generator = project_generator or AndroidProjectGenerator()
        self.feature_generator = feature_generator or AndroidFeatureGenerator()
        self.performance_policy = performance_policy or PerformancePolicy()
        self.accessibility_verifier = accessibility_verifier or AndroidAccessibilityVerifier()
        self.requirements_verifier = requirements_verifier or RequirementsVerifier()

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

        for relative in features.files:
            source_path = project.root / relative
            try:
                source = source_path.read_text(encoding="utf-8")
                self.performance_policy.require_clean(source)
            except (OSError, UnicodeDecodeError, ValueError) as exc:
                raise AndroidAppGenerationError(
                    f"Generated app failed performance preflight: {exc}"
                ) from exc

        source_paths = [project.root / relative for relative in features.files]
        java_sources = [path for path in source_paths if path.suffix == ".java"]
        if not java_sources:
            raise AndroidAppGenerationError(
                "Generated Android app has no Java source available for mandatory accessibility verification."
            )

        accessibility_reports = [
            self.accessibility_verifier.verify_source(
                project_id=intent.spec.package_name,
                source_path=source_path,
                required=True,
            )
            for source_path in java_sources
        ]
        failed = [
            report for report in accessibility_reports
            if report.final_status != VerificationStatus.VERIFIED
        ]
        if failed:
            details = "; ".join(
                evidence.detail
                for report in failed
                for evidence in report.evidence
                if evidence.status in {VerificationStatus.FAILED, VerificationStatus.BLOCKED}
            )
            raise AndroidAppGenerationError(
                "Generated Android app failed the mandatory global accessibility gate. "
                + (details or "Accessibility evidence is insufficient.")
            )

        requirements = self.requirements_verifier.verify(
            plan,
            features,
            project.root,
        )
        if not requirements.passed:
            reasons = "; ".join(requirements.reasons)
            raise AndroidAppGenerationError(
                "Generated Android app failed the approved-requirements gate. "
                + (reasons or "Required capabilities are not fully implemented.")
            )

        evidence_path = project.root / "requirements_verification.json"
        evidence_path.write_text(
            json.dumps(
                {
                    "status": requirements.status,
                    "required_capabilities": list(requirements.required_capabilities),
                    "generated_capabilities": list(requirements.generated_capabilities),
                    "implemented_capabilities": list(requirements.implemented_capabilities),
                    "unsupported_capabilities": list(requirements.unsupported_capabilities),
                    "missing_capabilities": list(requirements.missing_capabilities),
                    "missing_files": list(requirements.missing_files),
                    "unresolved_questions": list(requirements.unresolved_questions),
                    "reasons": list(requirements.reasons),
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )

        return GeneratedAndroidApp(intent=intent, project=project, features=features)
