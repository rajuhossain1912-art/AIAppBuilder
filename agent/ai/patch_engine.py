from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import hashlib
import json
import os
from typing import Any


class PatchValidationError(ValueError):
    """Raised when an AI-proposed patch violates safety constraints."""


@dataclass(frozen=True)
class FilePatch:
    path: str
    content: str
    reason: str = ""


@dataclass(frozen=True)
class AppliedPatch:
    path: str
    before_sha256: str | None
    after_sha256: str


_ALLOWED_SUFFIXES = {
    ".java", ".kt", ".xml", ".gradle", ".kts", ".properties", ".json",
    ".txt", ".md", ".html", ".css", ".js", ".yaml", ".yml",
}
_BLOCKED_PARTS = {
    ".git", ".github", "secrets", "credentials", "gradle-wrapper.jar",
}


def _safe_relative_path(value: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise PatchValidationError("patch path must be a non-empty string")
    raw = value.replace("\\", "/")
    candidate = Path(raw)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise PatchValidationError("patch path must stay inside the generated project")
    if any(part.casefold() in _BLOCKED_PARTS for part in candidate.parts):
        raise PatchValidationError("patch path targets a protected location")
    if candidate.suffix.casefold() not in _ALLOWED_SUFFIXES:
        raise PatchValidationError(f"unsupported patch file type: {candidate.suffix}")
    return candidate


def parse_patch_response(text: str) -> list[FilePatch]:
    """Parse only the strict JSON patch contract; markdown/fenced output is rejected."""
    try:
        payload: Any = json.loads(text)
    except json.JSONDecodeError as exc:
        raise PatchValidationError("AI fix response must be valid JSON") from exc
    if not isinstance(payload, dict) or set(payload) != {"patches"}:
        raise PatchValidationError("AI fix response must contain only a patches array")
    patches = payload["patches"]
    if not isinstance(patches, list) or not patches:
        raise PatchValidationError("patches must be a non-empty array")
    result: list[FilePatch] = []
    seen: set[str] = set()
    for item in patches:
        if not isinstance(item, dict) or not {"path", "content"}.issubset(item):
            raise PatchValidationError("each patch requires path and content")
        path = _safe_relative_path(item["path"])
        key = path.as_posix()
        if key in seen:
            raise PatchValidationError(f"duplicate patch path: {key}")
        seen.add(key)
        content = item["content"]
        if not isinstance(content, str):
            raise PatchValidationError("patch content must be text")
        reason = item.get("reason", "")
        if not isinstance(reason, str):
            raise PatchValidationError("patch reason must be text")
        result.append(FilePatch(key, content, reason))
    return result


class ConstrainedPatchApplier:
    """Apply AI patches only inside one generated project root and record hashes."""

    def __init__(self, project_root: str | Path) -> None:
        self.root = Path(project_root).resolve()

    def apply(self, patches: list[FilePatch]) -> list[AppliedPatch]:
        if not self.root.is_dir():
            raise PatchValidationError("generated project root does not exist")
        applied: list[AppliedPatch] = []
        for patch in patches:
            relative = _safe_relative_path(patch.path)
            target = (self.root / relative).resolve()
            try:
                target.relative_to(self.root)
            except ValueError as exc:
                raise PatchValidationError("patch escaped generated project root") from exc
            before = target.read_bytes() if target.is_file() else None
            before_sha = hashlib.sha256(before).hexdigest() if before is not None else None
            target.parent.mkdir(parents=True, exist_ok=True)
            temp = target.with_name(target.name + ".aiappbuilder.tmp")
            temp.write_text(patch.content, encoding="utf-8")
            os.replace(temp, target)
            after_sha = hashlib.sha256(target.read_bytes()).hexdigest()
            applied.append(AppliedPatch(relative.as_posix(), before_sha, after_sha))
        return applied
