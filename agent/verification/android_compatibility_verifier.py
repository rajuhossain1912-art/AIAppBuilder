from __future__ import annotations

from pathlib import Path

from .verification_executor import VerificationEvidence, VerificationReport, VerificationStatus


class AndroidCompatibilityVerifier:
    """Conservative static compatibility checks for generated Android projects."""

    def verify_project(self, project_id: str, root: str | Path) -> VerificationReport:
        project_root = Path(root).resolve()
        report = VerificationReport(project_id=project_id)
        required = (
            "settings.gradle",
            "build.gradle",
            "app/build.gradle",
            "app/src/main/AndroidManifest.xml",
        )
        missing = [name for name in required if not (project_root / name).is_file()]
        if missing:
            report.evidence.append(VerificationEvidence(
                evidence_id="COMPATIBILITY-001",
                check="ANDROID_PROJECT_STRUCTURE",
                status=VerificationStatus.FAILED,
                detail="Required Android project files are missing: " + ", ".join(missing),
                source=str(project_root),
            ))
            return report

        gradle = (project_root / "app/build.gradle").read_text(encoding="utf-8")
        manifest = (project_root / "app/src/main/AndroidManifest.xml").read_text(encoding="utf-8")
        checks = (
            ("COMPILE_SDK", "compileSdk" in gradle),
            ("MIN_SDK", "minSdk" in gradle),
            ("TARGET_SDK", "targetSdk" in gradle),
            ("APPLICATION_ID", "applicationId" in gradle),
            ("EXPORTED_LAUNCHER", 'android:exported="true"' in manifest),
        )
        failed = [name for name, ok in checks if not ok]
        if failed:
            report.evidence.append(VerificationEvidence(
                evidence_id="COMPATIBILITY-002",
                check="ANDROID_CONFIGURATION",
                status=VerificationStatus.FAILED,
                detail="Required compatibility configuration is missing: " + ", ".join(failed),
                source=str(project_root / "app/build.gradle"),
            ))
        else:
            report.evidence.append(VerificationEvidence(
                evidence_id="COMPATIBILITY-002",
                check="ANDROID_CONFIGURATION",
                status=VerificationStatus.STATICALLY_VERIFIED,
                detail="Android SDK, application ID, and launcher export configuration are present.",
                source=str(project_root),
            ))
        return report
