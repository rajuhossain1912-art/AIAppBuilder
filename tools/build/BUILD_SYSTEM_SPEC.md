# AIAppBuilder Build System Specification

## 1. Purpose

The Build System converts an approved Android project source into reproducible, verifiable application artifacts.

It must support both offline-capable and online-dependent applications.

## 2. Core Principle

A build is successful only when real build evidence confirms success.

The system must never claim that an application was built when the build did not actually complete.

## 3. Supported Application Types

The Build System must be able to handle projects designed as:

- Offline applications
- Online applications
- Hybrid applications
- Local database applications
- API-based applications
- Media applications
- Accessibility-first applications
- TTS applications
- Other supported Android application architectures

The build process must not assume that every application requires network access at runtime.

## 4. Build Inputs

A build request should contain:

- Project ID
- Source version
- Build configuration
- Target variant
- Required Android compatibility information
- Dependency information
- Build environment information
- Required signing mode
- Relevant verification requirements

## 5. Source Integrity

Before building, the system should verify:

- Correct project
- Correct source version
- Required files present
- Required configuration present
- No unexpected project substitution
- No known unresolved release-blocking issue

## 6. Environment Detection

The Build System should determine the available build environment before execution.

It should identify, where available:

- Operating environment
- Java version
- Android SDK
- Build tools
- Gradle version
- Android Gradle Plugin version
- Available storage
- Available memory
- Network availability
- Required cached dependencies

The system must not claim that an environment is available without evidence.

## 7. Offline Build Capability

For projects that can build without network access, the system should support offline builds when all required dependencies are locally available.

Offline mode must not be forced when required dependencies are unavailable.

## 8. Online Build Capability

For projects requiring network access during build, the system may use authorized online dependency repositories and build services.

Network access during build must follow the Privacy Policy and Resource Policy.

## 9. Runtime Offline and Online Behavior

The Build System must distinguish:

- Offline build capability
- Online build dependency
- Offline runtime capability
- Online runtime capability

A project that requires internet at runtime must not be incorrectly described as fully offline.

A project capable of offline runtime operation must not be incorrectly described as online-only.

## 10. Build Variants

The system should support appropriate build variants such as:

- Debug
- Release
- Other project-defined variants

The selected variant must be recorded in the build result.

## 11. Dependency Resolution

The system should:

- Resolve required dependencies
- Detect missing dependencies
- Detect incompatible dependencies
- Record dependency failures
- Avoid unnecessary dependency additions

It must not silently replace a dependency with an unrelated one.

## 12. Dependency Reproducibility

Where practical, dependency versions should be explicitly controlled.

Build configuration should remain reproducible.

Unexpected dependency upgrades should not occur silently during a release build.

## 13. Build Configuration

The system should validate relevant:

- Gradle configuration
- Android configuration
- Manifest configuration
- SDK configuration
- Build variants
- Signing configuration
- Resource configuration

## 14. Compile Process

The Build System should:

1. Prepare the project.
2. Validate configuration.
3. Resolve dependencies.
4. Compile source.
5. Process resources.
6. Run required build tasks.
7. Generate the requested artifact.
8. Capture build output.
9. Report the actual result.

## 15. Build Logs

Each build should preserve useful logs containing:

- Build ID
- Project ID
- Source version
- Build variant
- Start time
- End time
- Tasks executed
- Warnings
- Errors
- Final result

Secrets must never be written into logs.

## 16. Error Detection

The system should distinguish among:

- Compilation error
- Dependency error
- Configuration error
- Resource error
- Manifest error
- Signing error
- Environment error
- Network error
- Storage/resource error
- Toolchain compatibility error
- Unknown error

## 17. Error Analysis

When a build fails, the system should identify:

- Actual error message
- Failing task
- Relevant file when available
- Likely root cause
- Confidence level when applicable

It must distinguish evidence from an unverified hypothesis.

## 18. Automatic Fix Loop

When authorized, the Agent may enter:

BUILD
→ ERROR
→ ANALYZE
→ RESEARCH IF NEEDED
→ FIX
→ BUILD AGAIN

The loop must be bounded.

## 19. Retry Protection

The system must not retry indefinitely.

Repeated failures should cause the build workflow to stop and report the actual problem.

Destructive operations must never be blindly retried.

## 20. Regression Protection

After a fix, the system should verify that the fix did not unnecessarily break previously working functionality.

Relevant tests should be rerun.

## 21. Resource Protection

Build operations should respect:

- CPU
- RAM
- Storage
- Network
- API quotas
- Build-service quotas
- Time limits

The system should avoid unnecessary repeated builds.

## 22. Free-First Operation

When the user requires a free workflow, the Build System should prefer available free build infrastructure.

It must not silently activate paid infrastructure.

## 23. Paid Build Services

A paid build service may be used only after the required approval has been obtained according to the Approval Policy.

The system must clearly identify a potential cost before activation.

## 24. Build Service Failure

If an external build service is unavailable, the system should:

1. Preserve the project state.
2. Preserve the failure evidence.
3. Determine whether another authorized build method exists.
4. Use an alternative only when permitted.
5. Report the limitation if no valid alternative exists.

## 25. Artifact Types

The Build System may produce:

- APK
- AAB
- Other project-requested build artifacts

Only actually generated artifacts may be marked as available.

## 26. Artifact Metadata

Each artifact should be associated with:

- Artifact ID
- Project ID
- Build ID
- Source version
- Variant
- Version name
- Version code when applicable
- Creation time
- File size
- Integrity identifier when available

## 27. Artifact Integrity

After generation, the system should verify that:

- The artifact exists
- The artifact is readable
- The artifact belongs to the correct project
- The artifact corresponds to the intended source
- The artifact was not unexpectedly modified

## 28. Signing

Signing must follow secure project configuration.

The system must never expose:

- Keystore passwords
- Private signing keys
- Signing credentials

Signing credentials must not be committed into source code.

## 29. Debug vs Release

The system must clearly distinguish debug artifacts from release artifacts.

A debug build must not automatically be presented as a production release.

## 30. Build Verification

A successful build is one verification input, not the entire application verification process.

Build success must be followed by the required testing and verification stages defined by the project.

## 31. Accessibility Build Requirements

When accessibility is a project requirement, the Build System must preserve all accessibility-related source and configuration.

A build optimization must not remove required accessibility functionality.

## 32. Android Compatibility

The Build System should support the project's declared Android compatibility range.

Where the project targets broad compatibility, the build configuration should avoid unnecessary restrictions that prevent supported Android versions from running.

## 33. Offline Application Verification

For an application declared offline-capable, the verification system should determine whether its required core functionality actually works without network access.

The Build System itself must not confuse successful compilation with offline functionality.

## 34. Online Application Verification

For an application requiring online services, the system should record the external services required for runtime operation.

Unavailable external services must not be represented as verified functionality.

## 35. Hybrid Application Verification

For hybrid applications, the system should distinguish:

- Features that work offline
- Features that require network access
- Behavior when network access is unavailable

## 36. Build Reproducibility

Where technically possible, rebuilding the same source version with the same configuration should produce an equivalent artifact.

Differences caused by external environments should be recorded when detected.

## 37. Build Cache

Caching may be used to reduce build time and resource usage.

Cached results must not be trusted blindly when source or configuration changes affect the result.

## 38. Clean Build

A clean build should be available when necessary to detect problems hidden by stale build outputs.

The system should not perform clean builds unnecessarily because they consume additional resources.

## 39. Build State

Build states should include:

- QUEUED
- PREPARING
- BUILDING
- SUCCEEDED
- FAILED
- CANCELLED
- BLOCKED
- RESOURCE_LIMITED

## 40. Build Cancellation

When technically possible, an active build should support cancellation.

Cancellation must preserve useful diagnostic information.

## 41. Interrupted Build

If a build is interrupted:

- Preserve the build record.
- Identify whether an artifact was actually produced.
- Do not mark the build successful without evidence.
- Allow safe resumption or retry.

## 42. Build History

Each build should record:

- Build ID
- Project ID
- Source version
- Variant
- Environment
- Start time
- End time
- Result
- Artifact IDs
- Error information
- Verification status

## 43. Last Known Good Build

The project should retain a reference to the latest verified successful build when available.

A failed build must not replace the last known good state.

## 44. Rollback Support

When practical, the system should be able to return to a previously verified source state.

Rollback must preserve audit history.

## 45. Build Security

The Build System should prevent:

- Unauthorized source changes
- Secret exposure
- Unauthorized artifact replacement
- Unexpected external uploads
- Unauthorized build destinations

## 46. Build Privacy

Private project information must remain isolated during build processing.

Build logs and artifacts must not unnecessarily expose private information.

## 47. Build-to-Delivery Relationship

The Delivery Engine may accept an artifact only when the artifact is linked to:

- Correct project
- Correct source version
- Successful build
- Required verification
- Required authorization

## 48. No False Success

The system must never report:

- Build succeeded without evidence
- APK exists when it does not
- AAB exists when it does not
- Artifact verified when it was not
- Offline capability when it was not tested
- Online functionality when the required service was unavailable

## 49. Build Report

The final build report should contain:

- Project
- Build ID
- Source version
- Variant
- Environment
- Build result
- Artifact list
- Errors
- Warnings
- Resource limitations
- Verification status
- Known limitations

## 50. Final Rule

The Build System exists to transform verified project source into real, traceable, reproducible application artifacts.

Its process is:

SOURCE
→ VALIDATE
→ PREPARE
→ RESOLVE DEPENDENCIES
→ BUILD
→ CAPTURE EVIDENCE
→ VERIFY ARTIFACT
→ TEST
→ REPORT
→ HAND OFF TO DELIVERY

A build is successful only when real evidence proves that the requested artifact was actually generated.
