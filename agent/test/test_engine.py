from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import subprocess
from typing import Sequence


@dataclass
class TestResult:
    success: bool
    command: list[str]
    return_code: int | None
    stdout: str = ""
    stderr: str = ""


@dataclass
class TestReport:
    results: list[TestResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return bool(self.results) and all(result.success for result in self.results)


class TestEngine:
    """Executes explicitly selected project tests and records actual results."""

    def run(self, project_root: str | Path, command: Sequence[str], timeout_seconds: int = 900) -> TestResult:
        root = Path(project_root).resolve()
        if not root.is_dir():
            raise ValueError("project_root must be an existing directory")
        if not command or not all(isinstance(item, str) and item for item in command):
            raise ValueError("command must contain non-empty strings")
        try:
            completed = subprocess.run(
                list(command), cwd=root, capture_output=True, text=True,
                timeout=timeout_seconds, check=False,
            )
            return TestResult(
                success=completed.returncode == 0,
                command=list(command), return_code=completed.returncode,
                stdout=completed.stdout, stderr=completed.stderr,
            )
        except subprocess.TimeoutExpired as exc:
            return TestResult(
                success=False, command=list(command), return_code=None,
                stdout=exc.stdout or "", stderr=(exc.stderr or "") + "\nTest timed out.",
            )
        except OSError as exc:
            return TestResult(
                success=False, command=list(command), return_code=None,
                stderr=f"Unable to execute test command: {exc}",
            )
