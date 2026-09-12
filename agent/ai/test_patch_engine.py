from __future__ import annotations

import json
from pathlib import Path

import pytest

from agent.ai.patch_engine import (
    ConstrainedPatchApplier,
    PatchValidationError,
    parse_patch_response,
)


def test_parse_strict_patch_response() -> None:
    patches = parse_patch_response(json.dumps({"patches": [{"path": "app/src/Main.java", "content": "class Main {}", "reason": "fix"}]}))
    assert patches[0].path == "app/src/Main.java"
    assert patches[0].content == "class Main {}"


def test_rejects_traversal_and_protected_paths() -> None:
    with pytest.raises(PatchValidationError):
        parse_patch_response(json.dumps({"patches": [{"path": "../secret.txt", "content": "x"}]}))
    with pytest.raises(PatchValidationError):
        parse_patch_response(json.dumps({"patches": [{"path": ".github/workflows/build.yml", "content": "x"}]}))


def test_rejects_non_json_and_unsupported_extension() -> None:
    with pytest.raises(PatchValidationError):
        parse_patch_response("```json {\"patches\": []}```")
    with pytest.raises(PatchValidationError):
        parse_patch_response(json.dumps({"patches": [{"path": "run.sh", "content": "rm -rf /"}]}))


def test_applier_isolates_root_and_records_hashes(tmp_path: Path) -> None:
    root = tmp_path / "generated"
    root.mkdir()
    target = root / "app" / "src" / "Main.java"
    target.parent.mkdir(parents=True)
    target.write_text("old", encoding="utf-8")
    patches = parse_patch_response(json.dumps({"patches": [{"path": "app/src/Main.java", "content": "new"}]}))
    applied = ConstrainedPatchApplier(root).apply(patches)
    assert target.read_text(encoding="utf-8") == "new"
    assert applied[0].before_sha256
    assert applied[0].after_sha256
    assert applied[0].before_sha256 != applied[0].after_sha256
