from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

from .interaction import AIInteraction
from .patch_engine import AppliedPatch, ConstrainedPatchApplier, parse_patch_response


@dataclass(frozen=True)
class FixResult:
    stage: str
    request_id: str
    applied: tuple[AppliedPatch, ...]


class AIFixAgent:
    """Turn bounded failure evidence into strictly constrained project patches."""

    def __init__(self, interaction: AIInteraction) -> None:
        self.interaction = interaction

    def fix(self, *, stage: str, project_root: str | Path, failure_evidence: str, allowed_paths: list[str]) -> FixResult:
        if not stage.strip():
            raise ValueError("stage must not be empty")
        if not failure_evidence.strip():
            raise ValueError("failure_evidence must not be empty")
        prompt = json.dumps({
            "task": "produce a minimal safe fix for the generated Android project",
            "stage": stage,
            "failure_evidence": failure_evidence,
            "allowed_paths": allowed_paths,
            "contract": {"output": "JSON object with only patches array", "patch": "path, content, optional reason", "no_markdown": True, "no_secrets": True, "only_allowed_paths": True},
        }, ensure_ascii=False)
        response = self.interaction.request(purpose=f"FIX_{stage}", prompt=prompt)
        patches = parse_patch_response(response.text)
        allowed = {Path(path).as_posix() for path in allowed_paths}
        unexpected = [patch.path for patch in patches if patch.path not in allowed]
        if unexpected:
            raise ValueError("AI proposed a file outside the allowed fix set: " + ", ".join(unexpected))
        applied = ConstrainedPatchApplier(project_root).apply(patches)
        return FixResult(stage=stage, request_id=response.request_id, applied=tuple(applied))
