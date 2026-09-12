from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from agent.build import BuildEngine, BuildResult
from agent.delivery import DeliveryEngine, DeliveryGate, DeliveryResult
from agent.pipeline import AgentPipeline, IntakeResult
from agent.review import ReviewEngine, ReviewReport
from agent.security import PrivacyGuard
from agent.test import TestEngine, TestResult
from agent.verification import (
    AndroidAccessibilityVerifier,
    AndroidCompletenessVerifier,
    AndroidCompatibilityVerifier,
    VerificationExecutor,
    VerificationReport,
)

from .orchestrator import Orchestrator
from .state_model import LifecycleState


@dataclass(frozen=True)
class OrchestratedIntake:
    intake: IntakeResult
    orchestrator: Orchestrator


@dataclass(frozen=True)
class ReleaseCycleResult:
    review: ReviewReport
    build: BuildResult
    test: TestResult
    verification: VerificationReport
    delivery: DeliveryResult
    retries: int

    @property
    def delivered(self) -> bool:
        return self.delivery.status == "READY"


class PipelineOrchestrator:
    """Bind intake, generation, review, build, test, verification and delivery."""

    def __init__(self, project_id: str, state_path: str | Path) -> None:
        self.orchestrator = Orchestrator(project_id, str(state_path))
        self.pipeline = AgentPipeline()
        self.review_engine = ReviewEngine()
        self.build_engine = BuildEngine()
        self.test_engine = TestEngine()
        self.verification_executor = VerificationExecutor()
        self.accessibility_verifier = AndroidAccessibilityVerifier()
        self.completeness_verifier = AndroidCompletenessVerifier()
        self.compatibility_verifier = AndroidCompatibilityVerifier()
        self.privacy_guard = PrivacyGuard()
        self.delivery_engine = DeliveryEngine()

    def intake(self, user_request: str) -> OrchestratedIntake:
        self.orchestrator.start()
        self.orchestrator.set_task("client_intake")
        self.orchestrator.transition_to(LifecycleState.UNDERSTANDING)
        result = self.pipeline.intake(user_request)
        self.orchestrator.complete_task("client_intake")
        if result.needs_user_confirmation:
            self.orchestrator.request_approval("requirements_and_plan")
            self.orchestrator.transition_to(LifecycleState.AWAITING_CONFIRMATION)
        else:
            self.orchestrator.transition_to(LifecycleState.PLANNING)
            self.orchestrator.record_success("requirements_and_plan_ready")
        return OrchestratedIntake(intake=result, orchestrator=self.orchestrator)

    def approve_and_generate(self, result: OrchestratedIntake, output_root: str | Path):
        if result.orchestrator is not self.orchestrator:
            raise ValueError("result belongs to a different orchestrator")
        if result.intake.needs_user_confirmation:
            raise ValueError("Clarifying questions must be resolved before generation")
        self.orchestrator.receive_approval("requirements_and_plan")
        self.orchestrator.transition_to(LifecycleState.GENERATING)
        self.orchestrator.set_task("android_generation")
        try:
            generated = self.pipeline.generate_android(result.intake, output_root, approved=True)
        except Exception as exc:
            self.orchestrator.record_error(str(exc))
            self.orchestrator.transition_to(LifecycleState.FIXING)
            raise
        self.orchestrator.complete_task("android_generation")
        self.orchestrator.record_success("android_source_generated")
        self.orchestrator.transition_to(LifecycleState.REVIEWING)
        return generated

    @staticmethod
    def _android_source_path(root: Path, review_paths: Sequence[str]) -> Path | None:
        for relative in review_paths:
            candidate = root / relative
            if candidate.suffix == ".java" and candidate.is_file():
                return candidate
        java_files = sorted((root / "app").rglob("*.java")) if (root / "app").is_dir() else []
        return java_files[0] if java_files else None

    def execute_release_cycle(
        self,
        project_root: str | Path,
        review_paths: Sequence[str],
        build_command: Sequence[str],
        test_command: Sequence[str],
        artifact_path: str | Path,
        authorized: bool = False,
        max_retries: int = 2,
        fix_callback: Callable[[str, int], None] | None = None,
    ) -> ReleaseCycleResult:
        """Run REVIEW -> BUILD -> TEST -> VERIFY -> FIX/RETRY -> DELIVERY."""
        if max_retries < 0 or max_retries > 5:
            raise ValueError("max_retries must be between 0 and 5")
        root = Path(project_root).resolve()
        artifact = Path(artifact_path).resolve()
        retries = 0

        self.orchestrator.set_task("review")
        review = self.review_engine.review_paths(self.orchestrator.state.project_id, root, review_paths)
        while review.blocking:
            if retries >= max_retries:
                self.orchestrator.record_error("Release blocked by unresolved review findings.")
                self.orchestrator.transition_to(LifecycleState.FIXING)
                raise RuntimeError("Release blocked by unresolved review findings")
            retries += 1
            self.orchestrator.record_error("Release-blocking review findings require fixing.")
            self.orchestrator.increment_retry()
            self.orchestrator.transition_to(LifecycleState.FIXING)
            if fix_callback:
                fix_callback("REVIEW", retries)
            self.orchestrator.transition_to(LifecycleState.REVIEWING)
            review = self.review_engine.review_paths(self.orchestrator.state.project_id, root, review_paths)
        self.orchestrator.complete_task("review")
        self.orchestrator.record_success("review_passed")

        source_path = self._android_source_path(root, review_paths)
        build: BuildResult
        test: TestResult
        verification: VerificationReport
        accessibility_ok = compatibility_ok = completeness_ok = False
        privacy_ok = False

        while True:
            self.orchestrator.transition_to(LifecycleState.BUILDING)
            self.orchestrator.set_task("build")
            build = self.build_engine.run(root, build_command)
            if not build.success:
                if retries >= max_retries:
                    self.orchestrator.record_error(build.stderr or "Build failed")
                    self.orchestrator.transition_to(LifecycleState.FIXING)
                    raise RuntimeError("Build failed and retry limit was reached")
                retries += 1
                self.orchestrator.increment_retry()
                self.orchestrator.record_error(build.stderr or "Build failed")
                self.orchestrator.transition_to(LifecycleState.FIXING)
                if fix_callback:
                    fix_callback("BUILD", retries)
                continue
            self.orchestrator.complete_task("build")
            self.orchestrator.record_success("build_succeeded")

            self.orchestrator.transition_to(LifecycleState.TESTING)
            self.orchestrator.set_task("test")
            test = self.test_engine.run(root, test_command)
            if not test.success:
                if retries >= max_retries:
                    self.orchestrator.record_error(test.stderr or "Tests failed")
                    self.orchestrator.transition_to(LifecycleState.FIXING)
                    raise RuntimeError("Tests failed and retry limit was reached")
                retries += 1
                self.orchestrator.increment_retry()
                self.orchestrator.record_error(test.stderr or "Tests failed")
                self.orchestrator.transition_to(LifecycleState.FIXING)
                if fix_callback:
                    fix_callback("TEST", retries)
                continue
            self.orchestrator.complete_task("test")
            self.orchestrator.record_success("tests_passed")

            self.orchestrator.transition_to(LifecycleState.VERIFYING)
            self.orchestrator.set_task("verification")
            verification = self.verification_executor.hash_artifact(self.orchestrator.state.project_id, artifact)
            accessibility_ok = False
            if source_path is not None:
                accessibility_ok = self.accessibility_verifier.verify_source(
                    self.orchestrator.state.project_id, source_path
                ).final_status == "VERIFIED"
            compatibility_ok = self.compatibility_verifier.verify_project(
                self.orchestrator.state.project_id, root
            ).final_status == "VERIFIED"
            completeness_ok = self.completeness_verifier.verify_project(
                self.orchestrator.state.project_id, root
            ).status == "VERIFIED"
            privacy_report = self.privacy_guard.inspect_source(root, review_paths)
            privacy_ok = privacy_report.passed

            if (
                verification.final_status == "VERIFIED"
                and accessibility_ok
                and compatibility_ok
                and completeness_ok
                and privacy_ok
            ):
                self.orchestrator.complete_task("verification")
                self.orchestrator.record_verified_result("artifact_sha256")
                break

            if retries >= max_retries:
                self.orchestrator.record_error("Verification gates failed and retry limit was reached.")
                self.orchestrator.transition_to(LifecycleState.FIXING)
                raise RuntimeError("Verification failed and retry limit was reached")
            retries += 1
            self.orchestrator.increment_retry()
            self.orchestrator.record_error("Verification gates failed; release requires another fix/retry cycle.")
            self.orchestrator.transition_to(LifecycleState.FIXING)
            if fix_callback:
                fix_callback("VERIFY", retries)

        gate = DeliveryGate(
            requirements_verified=True,
            build_succeeded=build.success,
            tests_passed=test.success,
            review_blockers_resolved=not review.blocking,
            security_ok=not any(f.category == "SECURITY" and f.severity in {"CRITICAL", "HIGH"} for f in review.findings),
            privacy_ok=privacy_ok,
            accessibility_ok=accessibility_ok,
            compatibility_ok=compatibility_ok and completeness_ok,
            artifact_verified=verification.final_status == "VERIFIED",
            authorized=authorized,
        )
        self.orchestrator.transition_to(LifecycleState.DELIVERING)
        self.orchestrator.set_task("delivery")
        delivery = self.delivery_engine.prepare(
            gate,
            artifact,
            project_id=self.orchestrator.state.project_id,
            evidence={
                "review": "PASSED",
                "build": "PASSED",
                "tests": "PASSED",
                "artifact_verification": verification.final_status,
                "accessibility": accessibility_ok,
                "compatibility": compatibility_ok,
                "completeness": completeness_ok,
                "privacy": privacy_ok,
                "authorized": authorized,
            },
        )
        if delivery.status != "READY":
            self.orchestrator.record_error("Delivery gate blocked release.")
            self.orchestrator.transition_to(LifecycleState.FIXING)
            raise RuntimeError("Delivery blocked: " + "; ".join(delivery.reasons))
        self.orchestrator.complete_task("delivery")
        self.orchestrator.record_success("delivery_ready")
        self.orchestrator.transition_to(LifecycleState.COMPLETED)
        return ReleaseCycleResult(review, build, test, verification, delivery, retries)
