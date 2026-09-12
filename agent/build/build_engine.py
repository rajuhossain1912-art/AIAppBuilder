from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
from typing import Sequence


class BuildError(ValueError):
    """Raised when a build request is unsafe or invalid."""


@dataclass
class BuildResult:
    success: bool
    command: list[str]
    return_code: int | None
    stdout: str = ""
    stderr: str = ""
    artifact_paths: list[str] | None = None


class BuildEngine:
    """Runs an explicitly approved build command inside an authorized project directory."""

    def run(self, project_root: str | Path, command: Sequence[str], timeout_seconds: int = 900) -> BuildResult:
        root = Path(project_root).resolve()
        if not root.is_dir():
            raise BuildError("project_root must be an existing directory")
        if not command or not all(isinstance(item, str) and item.strip() for item in command):
            raise BuildError("command must contain non-empty strings")
        if timeout_seconds <= 0 or timeout_seconds > 3600:
            raise BuildError("timeout_seconds must be between 1 and 3600")

        try:
            completed = subprocess.run(
                list(command), cwd=root, capture_output=True, text=True,
                timeout=timeout_seconds, check=False,
            )
        except subprocess.TimeoutExpired as exc:
            return BuildResult(
                success=False, command=list(command), return_code=None,
                stdout=exc.stdout or "", stderr=(exc.stderr or "") + "\nBuild timed out.",
            )
        except OSError as exc:
            return BuildResult(
                success=False, command=list(command), return_code=None,
                stderr=f"Unable to execute build command: {exc}",
            )

        return BuildResult(
            success=completed.returncode == 0,
            command=list(command), return_code=completed.returncode,
            stdout=completed.stdout, stderr=completed.stderr,
        )
