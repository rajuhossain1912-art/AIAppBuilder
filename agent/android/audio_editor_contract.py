from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AudioEditorContract:
    """Minimum truthful contract before audio_editor can be marked implemented."""

    requires_real_media_processing: bool = True
    requires_accessible_transport_controls: bool = True
    requires_trim_and_split: bool = True
    requires_export: bool = True
    requires_talkback_verification: bool = True

    def is_ready(self, *, media_processing: bool, controls: bool, editing: bool, export: bool, accessibility: bool) -> bool:
        return all((media_processing, controls, editing, export, accessibility))
