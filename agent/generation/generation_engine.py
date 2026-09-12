from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .generation_manifest import GenerationManifest, GenerationManifestError


class GenerationBoundaryError(RuntimeError):
    """Raised when generation attempts to leave the authorized project scope."""


class GenerationEngine:
    """Controlled file-generation primitives; AI content must pass through a manifest."""

    def validate_manifest(self, manifest: GenerationManifest) -> GenerationManifest:
        if not isinstance(manifest, GenerationManifest):
            raise TypeError("manifest must be a GenerationManifest")
        overlap = set(manifest.files_to_create) & set(manifest.files_to_modify)
        if overlap:
            raise GenerationManifestError(
                f"A file cannot be both created and modified: {sorted(overlap)}"
            )
        return manifest

    def validate_path(self, project_root: str | Path, relative_path: str) -> Path:
        root = Path(project_root).resolve()
        if not root.is_dir():
            raise GenerationBoundaryError("project_root must be an existing directory")
        if not isinstance(relative_path, str) or not relative_path.strip():
            raise GenerationBoundaryError("relative_path must not be empty")

        candidate = (root / relative_path).resolve()
        try:
            candidate.relative_to(root)
        except ValueError as exc:
            raise GenerationBoundaryError(
                "Generation path escapes the authorized project root"
            ) from exc
        return candidate

    def write_new_file(self, project_root: str | Path, relative_path: str, content: str) -> Path:
        target = self.validate_path(project_root, relative_path)
        if target.exists():
            raise GenerationBoundaryError("Refusing to overwrite an existing file as a new file")
        if not isinstance(content, str):
            raise TypeError("content must be a string")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def modify_existing_file(self, project_root: str | Path, relative_path: str, content: str) -> Path:
        target = self.validate_path(project_root, relative_path)
        if not target.is_file():
            raise GenerationBoundaryError("Refusing to modify a file that does not exist")
        if not isinstance(content, str):
            raise TypeError("content must be a string")
        target.write_text(content, encoding="utf-8")
        return target
