from __future__ import annotations

from pathlib import Path

from agent.android.feature_generator import GeneratedAndroidFeatures
from agent.planning import ProjectPlan
from agent.requirements.capability_catalog import classify_capabilities
from agent.verification.requirements_verifier import RequirementsVerifier


def test_music_and_keyboard_ideas_are_composable_capabilities() -> None:
    request = "Build a virtual guitar, tabla, flute and music keyboard, plus a Bangla typing keyboard."
    keys = {match.key for match in classify_capabilities(request)}
    assert {"instrument", "music", "typing_keyboard"}.issubset(keys)


def test_requirements_verifier_rejects_unimplemented_capability(tmp_path: Path) -> None:
    source = tmp_path / "MainActivity.java"
    source.write_text("class MainActivity {}", encoding="utf-8")
    plan = ProjectPlan(goal="virtual piano", capabilities=["instrument"])
    features = GeneratedAndroidFeatures(
        files=("MainActivity.java",),
        family="general",
        capabilities=("instrument",),
        implemented_capabilities=(),
        unsupported_capabilities=("instrument",),
    )
    report = RequirementsVerifier().verify(plan, features, tmp_path)
    assert not report.passed
    assert "instrument" in report.unsupported_capabilities
    assert report.reasons


def test_requirements_verifier_accepts_real_implemented_capability(tmp_path: Path) -> None:
    source = tmp_path / "MainActivity.java"
    source.write_text("class MainActivity {}", encoding="utf-8")
    plan = ProjectPlan(goal="calculator", capabilities=["calculator"])
    features = GeneratedAndroidFeatures(
        files=("MainActivity.java",),
        family="general",
        capabilities=("calculator",),
        implemented_capabilities=("calculator",),
    )
    report = RequirementsVerifier().verify(plan, features, tmp_path)
    assert report.passed
    assert report.reasons == ()
