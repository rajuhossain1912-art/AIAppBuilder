from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from agent.entrypoint import main


class EntrypointTests(unittest.TestCase):
    def test_intake_persists_request_and_returns_structured_result(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            state_root = Path(temp) / "state"
            work_root = Path(temp) / "work"
            with patch("builtins.print") as printer:
                code = main(
                    [
                        "--project-id",
                        "test-project",
                        "--state-root",
                        str(state_root),
                        "--work-root",
                        str(work_root),
                        "intake",
                        "Create an accessible offline notes app",
                    ]
                )
            self.assertEqual(code, 0)
            pending = state_root / "test-project" / "pending_request.txt"
            self.assertEqual(pending.read_text(encoding="utf-8"), "Create an accessible offline notes app")
            payload = json.loads(printer.call_args.args[0])
            self.assertEqual(payload["project_id"], "test-project")
            self.assertIn("normalized_request", payload)

    def test_generate_requires_explicit_approval(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            with patch("builtins.print") as printer:
                code = main(
                    [
                        "--project-id",
                        "test-project",
                        "--state-root",
                        str(Path(temp) / "state"),
                        "generate",
                    ]
                )
            self.assertEqual(code, 2)
            self.assertIn("explicit approval", printer.call_args.args[0])

    def test_status_is_resumable(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            state_root = Path(temp) / "state"
            with patch("builtins.print"):
                self.assertEqual(
                    main(
                        [
                            "--project-id",
                            "test-project",
                            "--state-root",
                            str(state_root),
                            "intake",
                            "Create an accessible offline notes app",
                        ]
                    ),
                    0,
                )
            with patch("builtins.print") as printer:
                self.assertEqual(
                    main(
                        [
                            "--project-id",
                            "test-project",
                            "--state-root",
                            str(state_root),
                            "status",
                            "--json",
                        ]
                    ),
                    0,
                )
            payload = json.loads(printer.call_args.args[0])
            self.assertEqual(payload["project_id"], "test-project")
            self.assertEqual(payload["current_state"], "PLANNING")


if __name__ == "__main__":
    unittest.main()
