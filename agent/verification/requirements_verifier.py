from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from agent.android.feature_generator import GeneratedAndroidFeatures
from agent.planning import ProjectPlan


@dataclass(frozen=True)
class RequirementsVerificationReport:
    """Evidence that the generated project still matches the approved plan."""

    status: str
    required_capabilities: tuple[str, ...]
    generated_capabilities: tuple[str, ...]
    missing_capabilities: tuple[str, ...]
    missing_files: tuple[str, ...]
    unresolved_questions: tuple[str, ...]
    reasons: tuple[str, ...]

    @property
    def passed(self) -> bool:
        return self.status == "VERIFIED"


class RequirementsVerifier:
    """Verify approved requirements against actual generated project evidence."""

    def verify(
        self,
        plan: ProjectPlan,
        features: GeneratedAndroidFeatures,
        project_root: str | Path,
    ) -> RequirementsVerificationReport:
        if not isinstance(plan, ProjectPlan):
            raise TypeError("plan must be a ProjectPlan")
        if not isinstance(features, GeneratedAndroidFeatures):
            raise TypeError("features must be GeneratedAndroidFeatures")

        root = Path(project_root).resolve()
        required = _unique(plan.capabilities)
        generated = _unique(features.capabilities)
        missing = tuple(capability for capability in required if capability not in generated)
        missing_files = tuple(
            relative for relative in features.files if not (root / relative).is_file()
        )
        unresolved = tuple(plan.unresolved_questions)
        reasons: list[str] = []

        if missing:
            reasons.append("Generated capability metadata does not cover every approved capability.")
        if missing_files:
            reasons.append("Generated feature files are missing from the project output.")
        if unresolved:
            reasons.append("Approved generation cannot pass while requirements remain unresolved.")
        if not generated:
            reasons.append("Generation produced no capability evidence.")

        return RequirementsVerificationReport(
            status="VERIFIED" if not reasons else "FAILED",
            required_capabilities=required,
            generated_capabilities=generated,
            missing_capabilities=missing,
            missing_files=missing_files,
            unresolved_questions=unresolved,
            reasons=tuple(reasons),
        )


def _unique(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value))
