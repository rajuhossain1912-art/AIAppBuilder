from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AudioEditorPlan:
    """Platform-safe plan for an accessible local audio editor."""

    operations: tuple[str, ...] = (
        "pick_audio",
        "preview",
        "trim",
        "split",
        "volume",
        "export",
    )
    accessibility_requirements: tuple[str, ...] = (
        "talkback_labels",
        "logical_focus_order",
        "status_announcements",
        "clear_error_messages",
    )


SUPPORTED_AUDIO_MIME_TYPES = (
    "audio/*",
    "audio/mpeg",
    "audio/wav",
    "audio/ogg",
    "audio/mp4",
)
