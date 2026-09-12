from __future__ import annotations

from agent.android.audio_editor_spec import AudioEditorPlan, SUPPORTED_AUDIO_MIME_TYPES


def test_audio_editor_plan_contains_core_editing_operations() -> None:
    plan = AudioEditorPlan()
    assert {"pick_audio", "preview", "trim", "split", "volume", "export"}.issubset(plan.operations)


def test_audio_editor_plan_requires_accessibility_evidence() -> None:
    plan = AudioEditorPlan()
    assert "talkback_labels" in plan.accessibility_requirements
    assert "logical_focus_order" in plan.accessibility_requirements
    assert "status_announcements" in plan.accessibility_requirements
    assert "clear_error_messages" in plan.accessibility_requirements


def test_supported_audio_types_are_declared() -> None:
    assert "audio/*" in SUPPORTED_AUDIO_MIME_TYPES
    assert "audio/mpeg" in SUPPORTED_AUDIO_MIME_TYPES
    assert "audio/wav" in SUPPORTED_AUDIO_MIME_TYPES
