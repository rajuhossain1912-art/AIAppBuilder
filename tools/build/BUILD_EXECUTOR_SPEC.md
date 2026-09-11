# AIAppBuilder Build Executor Specification

## 1. Purpose

The Build Executor performs authorized Android build operations defined by the Build System Specification.

## 2. Execution Flow

The executor follows:

VALIDATE
→ PREPARE
→ BUILD
→ CAPTURE RESULT
→ VERIFY ARTIFACT
→ REPORT

## 3. Preconditions

Before execution, verify:

- Correct project
- Correct source version
- Valid build configuration
- Required tools available
- Required dependencies available
- Required permissions available
- Required approval available
- Sufficient resources available

## 4. Execution Modes

The executor may support:

- Online build
- Offline build
- Debug build
- Release build
- Clean build
- Incremental build

The selected mode must be recorded.

## 5. Command Safety

Build commands must be generated from validated project configuration.

The executor must not execute arbitrary destructive commands merely because they appear in project input.

## 6. Working Directory

Every build must use an explicitly identified project working directory.

The executor must not accidentally build another project.

## 7. Dependency Preparation

Before compilation, the executor should verify required dependencies.

Missing dependencies must produce a clear failure rather than a false success.

## 8. Build Execution

The executor should:

1. Start the build.
2. Capture standard output.
3. Capture error output.
4. Monitor execution state.
5. Respect resource and time limits.
6. Detect completion.
7. Record the exit result.

## 9. Timeout

Build operations must have a defined execution limit.

A timeout must result in a recorded failure or resource-limited state.

The executor must not continue indefinitely.

## 10. Cancellation

When cancellation is requested and technically possible:

1. Stop the build safely.
2. Preserve useful logs.
3. Record cancellation.
4. Do not mark the build successful.

## 11. Exit Status

The executor must use actual execution evidence to determine success.

A successful process exit alone must not override other detected artifact or integrity failures.

## 12. Artifact Discovery

After a successful build, the executor should locate the expected artifact.

It must verify that the artifact actually exists before reporting success.

## 13. Artifact Validation

The executor should verify:

- File exists
- File is readable
- Expected artifact type
- Expected project association
- Expected build variant
- Expected source version when verifiable

## 14. Multiple Artifacts

If multiple artifacts are produced, each artifact must be recorded separately.

The executor must not confuse debug and release artifacts.

## 15. Build Logs

The executor must preserve relevant:

- Start time
- End time
- Commands or tasks
- Output
- Errors
- Exit status
- Artifact information

Secrets must never be intentionally recorded.

## 16. Failure Classification

Failures should be classified where possible as:

- SOURCE_ERROR
- CONFIG_ERROR
- DEPENDENCY_ERROR
- COMPILATION_ERROR
- RESOURCE_ERROR
- NETWORK_ERROR
- TOOLCHAIN_ERROR
- SIGNING_ERROR
- ARTIFACT_ERROR
- TIMEOUT
- CANCELLED
- UNKNOWN_ERROR

## 17. Retry

Retries must be controlled.

The executor must not repeatedly retry a deterministic failure without a meaningful change.

## 18. Clean Retry

A clean build may be attempted when stale outputs are a plausible cause and the operation is authorized.

It must not be used as a blind solution for every failure.

## 19. Security

The executor must protect:

- Signing credentials
- API keys
- Tokens
- Private keys
- Other secrets

Secrets must not be passed into logs unnecessarily.

## 20. Privacy

Build processing must respect the Privacy Policy.

Private project information must not be unnecessarily transmitted to external services.

## 21. Resource Limits

The executor must respect available:

- CPU
- Memory
- Storage
- Network
- Time
- Provider quotas

## 22. Offline Mode

When offline mode is requested, the executor must not silently require network access.

If required dependencies are unavailable locally, it must report the limitation.

## 23. Online Mode

Online builds may access authorized dependency repositories or services.

External access must follow privacy, security, resource, and approval policies.

## 24. Build Environment

The executor should record available build environment information when possible:

- Java
- Gradle
- Android SDK
- Build tools
- Android Gradle Plugin
- Operating environment

## 25. Reproducibility

The executor should use the recorded source version and build configuration.

Unexpected environmental differences should be recorded when detectable.

## 26. State Management

Execution states should include:

- QUEUED
- PREPARING
- RUNNING
- SUCCEEDED
- FAILED
- CANCELLED
- TIMEOUT
- BLOCKED
- RESOURCE_LIMITED

## 27. Recovery

If execution fails:

- Preserve source.
- Preserve logs.
- Preserve build state.
- Preserve the last known good build.
- Provide actionable diagnostic information.

## 28. No False Success

The executor must never report success when:

- The build failed
- The artifact does not exist
- The artifact cannot be read
- The wrong artifact was produced
- Required verification failed

## 29. Integration

The executor must integrate with:

- Orchestrator
- Planning
- Requirements
- Generation
- Verification
- Review
- Delivery
- Approval Policy
- Security Policy
- Privacy Policy
- Resource Policy

## 30. Final Rule

The Build Executor is responsible for performing real, authorized builds and returning evidence-based results.

It must prefer correctness over speed and must never fabricate a build result.
