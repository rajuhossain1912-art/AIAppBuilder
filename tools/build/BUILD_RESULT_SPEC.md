# AIAppBuilder Build Result Specification

## 1. Purpose

This specification defines the standard structure for recording and reporting Android build results.

## 2. Result Integrity

A build result must be based on actual execution evidence.

The system must never fabricate a successful result.

## 3. Required Information

Each build result should contain:

- Build ID
- Project ID
- Source version
- Build variant
- Execution mode
- Start time
- End time
- Final state
- Exit status
- Artifact information
- Verification status
- Error information when applicable

## 4. Result States

Valid result states include:

- SUCCEEDED
- FAILED
- CANCELLED
- TIMEOUT
- BLOCKED
- RESOURCE_LIMITED

## 5. Successful Result

A build may be marked SUCCEEDED only when:

- The build process completed successfully.
- The expected artifact exists.
- The artifact is readable.
- No release-blocking error remains.
- Required build evidence was captured.

## 6. Failed Result

A failed build must include the available:

- Failure category
- Failing task
- Error message
- Relevant file
- Diagnostic information
- Recovery recommendation

## 7. Artifact Record

Each generated artifact should record:

- Artifact ID
- Artifact type
- File name
- File size when available
- Build ID
- Source version
- Variant
- Integrity information when available
- Verification state

## 8. Verification

Build success must remain separate from application verification.

The result should clearly state whether post-build verification:

- PASSED
- FAILED
- PENDING
- NOT_RUN

## 9. Offline and Online

The result must record whether the build used:

- Offline mode
- Online mode

It must not confuse build mode with application runtime capability.

## 10. Environment

When available, record:

- Java version
- Gradle version
- Android SDK
- Build tools
- Android Gradle Plugin
- Operating environment

## 11. Resource Information

When available, record relevant:

- CPU limitations
- Memory limitations
- Storage limitations
- Network limitations
- Provider quota limitations
- Timeouts

## 12. Error Classification

Use the most appropriate category:

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

## 13. Last Known Good Build

A failed build must not replace the project's last known good build.

The system should preserve the reference to the latest verified successful build.

## 14. Auditability

The result must be traceable to:

- Project
- Source
- Build execution
- Artifact
- Verification
- Delivery when applicable

## 15. Privacy

Build results must not expose:

- Passwords
- API keys
- Access tokens
- Private keys
- Other secrets

Private project information should be minimized.

## 16. Honest Reporting

The system must clearly distinguish:

- Verified facts
- Estimated information
- Unknown information
- Successful operations
- Failed operations

Unknown information must not be invented.

## 17. Delivery Gate

An artifact should be eligible for delivery only when:

- Build succeeded
- Artifact exists
- Artifact integrity is acceptable
- Required verification passed
- Required approval exists

## 18. Final Rule

Every build result must provide an accurate, traceable, evidence-based record of what actually happened.

BUILD
→ RESULT
→ ARTIFACT
→ VERIFY
→ REPORT
