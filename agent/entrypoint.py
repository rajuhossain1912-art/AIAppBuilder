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
        description="AIAppBuilder project agent entrypoint.",
    )
    parser.add_argument("--project-id", default="default-project")
    parser.add_argument("--state-root", default=str(DEFAULT_STATE_ROOT))
    parser.add_argument("--work-root", default=str(DEFAULT_WORK_ROOT))
    sub = parser.add_subparsers(dest="command", required=True)

    intake = sub.add_parser("intake", help="Review and structure a new app request.")
    intake.add_argument("request")

    status = sub.add_parser("status", help="Show the persisted lifecycle state.")
    status.add_argument("--json", action="store_true", dest="as_json")

    generate = sub.add_parser(
        "generate",
        help="Generate Android source after explicit approval has been recorded.",
    )
    generate.add_argument("--approve", action="store_true")

    return parser


def _agent(args: argparse.Namespace) -> PipelineOrchestrator:
    state_dir = Path(args.state_root) / args.project_id
    state_dir.mkdir(parents=True, exist_ok=True)
    return PipelineOrchestrator(args.project_id, state_dir / "orchestrator_state.json")


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
    agent = _agent(args)

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
        _print_intake(result)
        return 0

    if args.command == "generate":
        if not args.approve:
            print("ERROR: explicit approval is required; use --approve after reviewing the intake.")
            return 2
        agent.orchestrator.start()
        if agent.orchestrator.current_state == LifecycleState.AWAITING_CONFIRMATION:
            print("ERROR: unresolved clarification questions remain; run intake again after resolving them.")
            return 2
        from agent.pipeline import AgentPipeline

        # Reconstruct a safe generation input from the persisted project state is
        # intentionally not supported yet: requirements must be supplied through
        # the intake command in the same execution context. This prevents the
        # agent from silently inventing requirements.
        print("ERROR: generation requires a fresh approved intake result in this execution context.")
        print("Use the GitHub Actions 'generate' workflow after the review/approval step.")
        return 2

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
