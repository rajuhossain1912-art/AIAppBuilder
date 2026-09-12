from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import os
import re
from datetime import datetime, timezone

from agent.orchestrator import OrchestratedIntake, PipelineOrchestrator

DEFAULT_STATE_ROOT = Path("memory/runtime")
DEFAULT_WORK_ROOT = Path(".agent-work")
_PROJECT_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")


def _validate_project_id(project_id: str) -> str:
    """Reject path traversal and ambiguous project identifiers before filesystem use."""
    if not isinstance(project_id, str) or not _PROJECT_ID_RE.fullmatch(project_id):
        raise ValueError(
            "project_id must be 1-64 characters and contain only letters, numbers, hyphen, or underscore"
        )
    return project_id


def _persistent_client_data_allowed() -> bool:
    return os.getenv("AIAPPBUILDER_ALLOW_PERSISTENT_CLIENT_DATA", "false").strip().lower() == "true"


def _require_private_persistence() -> None:
    if not _persistent_client_data_allowed():
        raise RuntimeError(
            "Persistent client data is disabled. Set AIAPPBUILDER_ALLOW_PERSISTENT_CLIENT_DATA=true only in a private, controlled runtime."
        )


def _write_intake_record(state_dir: Path, result, original_request: str) -> None:
    """Persist the normalized intake needed for deterministic resume, not a re-run of AI intake."""
    _require_private_persistence()
    requirements = result.intake.requirements
    brief = result.intake.client_brief
    record = {
        "schema_version": 1,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "project_id": result.orchestrator.project_id,
        "request_sha256": hashlib.sha256(original_request.encode("utf-8")).hexdigest(),
        "original_request": requirements.original_request,
        "normalized_request": requirements.normalized_request,
        "questions": list(brief.questions) if brief else [],
        "needs_user_confirmation": result.intake.needs_user_confirmation,
        "plan": {
            "build_required": result.intake.plan.build_required,
            "test_required": result.intake.plan.test_required,
        },
    }
    (state_dir / "intake_record.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aiappbuilder", description="AIAppBuilder user-facing project agent entrypoint.")
    parser.add_argument("--project-id", default="default-project")
    parser.add_argument("--state-root", default=str(DEFAULT_STATE_ROOT))
    parser.add_argument("--work-root", default=str(DEFAULT_WORK_ROOT))
    sub = parser.add_subparsers(dest="command", required=True)

    intake = sub.add_parser("intake", help="Review and structure an app request.")
    intake.add_argument("request")
    status = sub.add_parser("status", help="Show persisted lifecycle state.")
    status.add_argument("--json", action="store_true", dest="as_json")
    generate = sub.add_parser("generate", help="Generate Android source from the last approved intake.")
    generate.add_argument("--approve", action="store_true")
    release = sub.add_parser("release", help="Run REVIEW -> BUILD -> TEST -> VERIFY -> FIX/RETRY -> DELIVERY.")
    release.add_argument("--approve", action="store_true")
    release.add_argument("--max-retries", type=int, default=2)
    return parser


def _agent(args: argparse.Namespace) -> tuple[PipelineOrchestrator, Path]:
    project_id = _validate_project_id(args.project_id)
    state_root = Path(args.state_root).resolve()
    work_root = Path(args.work_root).resolve()
    state_dir = state_root / project_id
    work_dir = work_root / project_id
    state_dir.mkdir(parents=True, exist_ok=True)
    work_dir.mkdir(parents=True, exist_ok=True)
    return PipelineOrchestrator(project_id, state_dir / "orchestrator_state.json"), state_dir


def _print_intake(result) -> None:
    brief = result.intake.client_brief
    payload = {
        "project_id": result.orchestrator.project_id,
        "original_request": result.intake.requirements.original_request,
        "normalized_request": result.intake.requirements.normalized_request,
        "questions": list(brief.questions) if brief else [],
        "needs_user_confirmation": result.intake.needs_user_confirmation,
        "plan": {"build_required": result.intake.plan.build_required, "test_required": result.intake.plan.test_required},
        "lifecycle_state": result.orchestrator.current_state.value,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def _review_paths(project_root: Path) -> list[str]:
    """Review generated source/config/evidence, excluding build caches and generated README text."""
    paths: list[str] = []
    for path in sorted(project_root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(project_root)
        if any(part in {"build", ".gradle"} for part in relative.parts):
            continue
        if relative.name == "README.generated.md":
            continue
        paths.append(relative.as_posix())
    return paths


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        agent, state_dir = _agent(args)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 2

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
        try:
            result = agent.intake(args.request)
            _write_intake_record(state_dir, result, args.request)
            (state_dir / "pending_request.txt").write_text(args.request, encoding="utf-8")
        except RuntimeError as exc:
            print(f"ERROR: {exc}")
            return 2
        _print_intake(result)
        return 0

    if args.command == "generate":
        if not args.approve:
            print("ERROR: explicit approval is required; use --approve after reviewing the intake.")
            return 2
        agent.orchestrator.start()
        intake_record = state_dir / "intake_record.json"
        if not intake_record.is_file():
            print("ERROR: no persisted intake record exists. Run 'intake' first in a private, controlled runtime.")
            return 2
        try:
            record = json.loads(intake_record.read_text(encoding="utf-8"))
            if record.get("project_id") != args.project_id:
                print("ERROR: intake record belongs to a different project.")
                return 2
            if record.get("needs_user_confirmation"):
                print("ERROR: clarification questions remain. Resolve them and run 'intake' again.")
                return 2
            request = str(record.get("original_request", "")).strip()
            if not request:
                print("ERROR: persisted intake record has no original request.")
                return 2
        except (OSError, json.JSONDecodeError, TypeError) as exc:
            print(f"ERROR: invalid intake record: {exc}")
            return 2
        # The orchestrator's persisted state is authoritative; the original request is
        # retained only as an audit input. Generation is never silently re-intaked.
        intake_result = agent.pipeline.intake(request)
        result = OrchestratedIntake(intake=intake_result, orchestrator=agent.orchestrator)
        output_root = Path(args.work_root).resolve() / args.project_id
        output_root.mkdir(parents=True, exist_ok=True)
        generated = agent.approve_and_generate(result, output_root)
        print(json.dumps({
            "status": "GENERATED", "project_id": args.project_id,
            "project_root": str(generated.project.root), "files": list(generated.features.files),
            "lifecycle_state": agent.orchestrator.current_state.value,
        }, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    if args.command == "release":
        if not args.approve:
            print("ERROR: explicit approval is required before release execution.")
            return 2
        if args.max_retries < 0 or args.max_retries > 5:
            print("ERROR: --max-retries must be between 0 and 5.")
            return 2
        agent.orchestrator.start()
        project_root = (Path(args.work_root).resolve() / args.project_id).resolve()
        artifact = project_root / "app" / "build" / "outputs" / "apk" / "debug" / "app-debug.apk"
        if not project_root.is_dir():
            print("ERROR: generated project does not exist. Run 'generate --approve' first.")
            return 2
        try:
            result = agent.execute_release_cycle(
                project_root=project_root,
                review_paths=_review_paths(project_root),
                build_command=["gradle", "--no-daemon", ":app:assembleDebug"],
                test_command=["gradle", "--no-daemon", ":app:test"],
                artifact_path=artifact,
                authorized=True,
                max_retries=args.max_retries,
            )
        except Exception as exc:
            print(f"ERROR: release cycle failed: {exc}")
            return 1
        print(json.dumps({
            "status": "DELIVERED", "project_id": args.project_id,
            "lifecycle_state": agent.orchestrator.current_state.value, "retries": result.retries,
            "artifact": str(result.delivery.artifact_path), "sha256": result.delivery.checksum_sha256,
            "delivery_manifest": result.delivery.manifest,
            "recovery_manifest": str(project_root / "recovery_manifest.json"),
        }, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
