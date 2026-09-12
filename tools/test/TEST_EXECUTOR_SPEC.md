# AIAppBuilder Test Executor Specification

## 1. Purpose

The Test Executor performs authorized tests defined by the Testing System.

## 2. Execution Flow

PREPARE
→ VALIDATE
→ EXECUTE
→ COLLECT EVIDENCE
→ CLASSIFY RESULT
→ REPORT

## 3. Preconditions

Before execution verify:

- Correct project
- Correct source version
- Correct build
- Correct test configuration
- Required test tools
- Required environment
- Required permissions
- Required resources

## 4. Test Types

The executor may run:

- Unit tests
- Integration tests
- UI tests
- Functional tests
- Regression tests
- Accessibility tests
- Security tests
- Compatibility tests
- Offline tests
- Online tests
- Performance tests

## 5. Test Isolation

Tests should use isolated or controlled data when practical.

Real private user or client data must not be modified unnecessarily.

## 6. Execution Evidence

The executor must capture available:

- Test output
- Error output
- Logs
- Exit status
- Runtime result
- Environment information
- Evidence files

## 7. Result States

Valid states include:

- PASSED
- FAILED
- BLOCKED
- SKIPPED
- CANCELLED
- TIMEOUT
- NOT_RUN

## 8. No False Success

The executor must never mark a test as PASSED without actual execution evidence.

## 9. Failure Handling

When a test fails:

1. Preserve evidence.
2. Identify the failed test.
3. Identify the affected requirement.
4. Record the actual failure.
5. Return the failure to the appropriate workflow stage.

## 10. Blocked Tests

A test is BLOCKED when a required:

- Device
- Emulator
- Tool
- Service
- Permission
- Dependency
- Environment

is unavailable.

A blocked test must never be converted into a passed test.

## 11. Timeout

Every executable test should have a reasonable time limit.

A timeout must be recorded accurately.

The executor must not run indefinitely.

## 12. Retry

Retries must be bounded.

A deterministic failure must not cause an endless retry loop.

## 13. Regression

After an authorized fix, affected tests may be executed again.

The executor should identify the source/build version used for the retest.

## 14. Offline Tests

When an offline test is requested, the executor must actually test without network access when the environment permits.

If network isolation cannot be established, the result must not be reported as a confirmed offline test.

## 15. Online Tests

Online tests must record relevant network conditions when available.

External service failures must be distinguished from application failures when possible.

## 16. Accessibility Tests

Accessibility tests should identify whether they were:

- Automated
- Static
- Device-based
- User-confirmed

The executor must not claim a physical TalkBack test occurred unless it actually occurred.

## 17. Security Tests

Security testing must protect discovered sensitive values.

Secrets must not be copied into reports unnecessarily.

## 18. Environment Record

When available, record:

- Operating system
- Android version
- API level
- Device or emulator
- Build version
- Network state
- Relevant tool versions

Unknown information must remain unknown.

## 19. Resource Protection

Testing must respect:

- CPU
- Memory
- Storage
- Network
- Time
- Provider quotas

Testing must not intentionally damage the user's device.

## 20. Privacy Protection

Test execution must follow the Privacy Policy.

Private project information must not be unnecessarily transmitted to external services.

## 21. Cost Protection

The executor must not automatically activate paid services or increase quotas without required authorization.

## 22. Test Record

Each execution should record:

- Test ID
- Project ID
- Requirement ID
- Source version
- Build ID
- Test type
- Environment
- Start time
- End time
- Expected result
- Actual result
- Status
- Evidence
- Error information

## 23. Test Command Safety

The executor must execute only validated test operations.

Test input must not automatically become permission to execute unrelated destructive commands.

## 24. Cancellation

When cancellation is requested:

- Stop safely when possible.
- Preserve useful evidence.
- Record cancellation.
- Do not report success.

## 25. Integration

The Test Executor integrates with:

- Orchestrator
- Requirements
- Planning
- Generation
- Review
- Build System
- Verification Engine
- Delivery Engine
- Approval Policy
- Security Policy
- Privacy Policy
- Resource Policy

## 26. Verification Handoff

Test results must be passed to the Verification Engine with sufficient evidence and environment information.

## 27. Honest Reporting

The executor must distinguish:

- Executed
- Not executed
- Passed
- Failed
- Blocked
- Skipped
- Unknown

It must never invent test evidence.

## 28. Final Rule

The Test Executor exists to perform real tests and return accurate evidence.

Its process is:

TEST DEFINITION
→ VALIDATE
→ EXECUTE
→ CAPTURE EVIDENCE
→ RESULT
→ REPORT
→ VERIFICATION
