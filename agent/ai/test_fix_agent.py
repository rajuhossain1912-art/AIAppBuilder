from __future__ import annotations

import json
from pathlib import Path

import pytest

from .fix_agent import AIFixAgent
from .interaction import AIInteraction


class FakeProvider:
    name = "fake"

    def __init__(self, response: str) -> None:
        self.response = response

    def complete(self, *, purpose: str, prompt: str) -> str:
        assert purpose == "FIX_BUILD"
        assert "failure_evidence" in prompt
        return self.response


def test_fix_agent_applies_only_allowlisted_file(tmp_path: Path) -> None:
    target = tmp_path / "app" / "src" / "MainActivity.java"
    target.parent.mkdir(parents=True)
    target.write_text("old", encoding="utf-8")
    response = json.dumps({"patches": [{"path": "app/src/MainActivity.java", "content": "new", "reason": "fix"}]})
    result = AIFixAgent(AIInteraction(FakeProvider(response))).fix(
        stage="BUILD", project_root=tmp_path, failure_evidence="compile error", allowed_paths=["app/src/MainActivity.java"]
    )
    assert target.read_text(encoding="utf-8") == "new"
    assert result.applied[0].before_sha256
    assert result.applied[0].after_sha256


def test_fix_agent_rejects_unapproved_path(tmp_path: Path) -> None:
    response = json.dumps({"patches": [{"path": "app/src/Other.java", "content": "x"}]})
    with pytest.raises(ValueError, match="outside the allowed fix set"):
        AIFixAgent(AIInteraction(FakeProvider(response))).fix(
            stage="BUILD", project_root=tmp_path, failure_evidence="error", allowed_paths=["app/src/MainActivity.java"]
        )
