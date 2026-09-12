from __future__ import annotations

import argparse
import json
from pathlib import Path

from agent.orchestrator import LifecycleState, PipelineOrchestrator

DEFAULT_STATE_ROOT = Path("memory/runtime")
DEFAULT_WORK_ROOT = Path(".agent-work")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aiappbuilder",
        description="AIAppBuilder user-facing project agent entrypoint.",
    )
    parser.add_argument("--project-id", default="default-project")
    parser.add_argument("--state-root", default=str(DEFAULT_STATE_ROOT))
    parser.add_argument("--work-root", default=str(DEFAULT_WORK_ROOT))
    sub = parser.add_subparsers(dest="command", required=True)

    intake = sub.add_parser("intake", help="Review and structure an app request.")
    intake.add_argument("request")

    status = sub.add_parser("status", help="Show persisted lifecycle state.")
    status.add_argument("--json", action="store_true", dest="as_json")

    generate = sub.add_parser(
        "generate",
        help="Generate Android source from the last approved intake.",
    )
    generate.add_argument("--approve", action="store_true")

    return parser


def _agent(args: argparse.Namespace) -> tuple[PipelineOrchestrator, Path]:
    state_dir = Path(args.state_root) / args.project_id
    state_dir.mkdir(parents=True, exist_ok=True)
    return PipelineOrchestrator(args.project_id, state_dir / "orchestrator_state.json"), state_dir


def _print_intake(result) -> None:
    brief = result.intake.client_brief
    payload = {
        "project_id": result.orchestrator.project_id,
        "original_request": result.intake.requirements.original_request,
        "normalized_request": result.intake.requirements.normalized_request,
        "questions": list(brief.questions) if brief else [],
        "needs_user_confirmation": result.intake.needs_user_confirmation,
        "plan": {
            "build_required": result.intake.plan.build_required,
            "test_required": result.intake.plan.test_required,
        },
        "lifecycle_state": result.orchestrator.current_state.value,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    agent, state_dir = _agent(args)

    if args.command == "status":
        agent.orchestrator.start()
        payload = agent.orchestrator.snapshot()
        if args.as_json:
            print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        else:
            print(f"Project: {payload['project_id']}")
            print(f"State: {payload['current_state']}")
            print(f"Task: {payload['current_task'] or '-'}")
            print(f"Completed: {', '.join(payload['completed_tasks']) or '-'}")
            print(f"Blocked: {', '.join(payload['blocked_tasks']) or '-'}")
            print(f"Retries: {payload['retry_count']}")
        return 0

    if args.command == "intake":
        result = agent.intake(args.request)
        (state_dir / "pending_request.txt").write_text(args.request, encoding="utf-8")
        _print_intake(result)
        return 0

    if args.command == "generate":
        if not args.approve:
            print("ERROR: explicit approval is required; use --approve after reviewing the intake.")
            return 2

        agent.orchestrator.start()
        pending = state_dir / "pending_request.txt"
        if not pending.is_file():
            print("ERROR: no pending intake request exists. Run 'intake' first.")
            return 2

        request = pending.read_text(encoding="utf-8").strip()
        result = agent.intake(request)
        if result.intake.needs_user_confirmation:
            print("ERROR: clarification questions remain. Resolve them and run 'intake' again.")
            _print_intake(result)
            return 2

        output_root = Path(args.work_root) / args.project_id
        output_root.mkdir(parents=True, exist_ok=True)
        generated = agent.approve_and_generate(result, output_root)
        print(
            json.dumps(
                {
                    "status": "GENERATED",
                    "project_id": args.project_id,
                    "project_root": str(generated.project.root),
                    "files": list(generated.features.files),
                    "lifecycle_state": agent.orchestrator.current_state.value,
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
