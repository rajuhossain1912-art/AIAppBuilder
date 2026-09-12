# AIAppBuilder Testing System Specification

## 1. Purpose

The Testing System defines how AIAppBuilder plans, executes, records, and evaluates tests for generated Android applications.

## 2. Core Principle

A test is considered passed only when actual evidence shows that the expected result occurred.

No test may be marked passed merely because code exists or because a build succeeded.

## 3. Testing Scope

The Testing System should support, when applicable:

- Unit testing
- Integration testing
- UI testing
- Functional testing
- Regression testing
- Accessibility testing
- Security testing
- Compatibility testing
- Offline testing
- Online testing
- Performance testing
- Artifact testing
- Error-path testing

## 4. Test Inputs

The system should use:

- Confirmed requirements
- Requirement IDs
- Approved plan
- Generated source
- Build result
- Review findings
- Known risks
- Previous failures
- Verification requirements

## 5. Test Lifecycle

The normal lifecycle is:

PLAN
→ PREPARE
→ EXECUTE
→ COLLECT EVIDENCE
→ ANALYZE
→ REPORT
→ FIX IF REQUIRED
→ RETEST

## 6. Requirement Traceability

Important requirements should map to one or more tests.

Example:

REQ-001
→ TEST-001
→ RESULT
→ EVIDENCE
→ VERIFIED

Untested important requirements must not be represented as fully verified.

## 7. Test States

Valid test states include:

- NOT_RUN
- QUEUED
- RUNNING
- PASSED
- FAILED
- BLOCKED
- SKIPPED
- CANCELLED
- NOT_APPLICABLE

## 8. Unit Tests

When unit tests are appropriate, they should verify isolated business logic and important edge cases.

The system should record:

- Test name
- Input
- Expected result
- Actual result
- Status
- Error information

## 9. Integration Tests

Integration tests should verify important interactions between components.

Examples include:

- UI and business logic
- Business logic and data storage
- Data layer and API
- Authentication
- Database operations
- Media processing
- External integrations

## 10. UI Tests

UI testing should verify important user workflows.

Examples:

- Application starts
- Navigation works
- Buttons operate
- Text fields work
- Forms validate input
- Dialogs behave correctly
- Loading states appear
- Error states are understandable
- Required results are displayed

## 11. Accessibility Testing

Accessibility is a required testing consideration.

When applicable, test:

- TalkBack navigation
- Focus order
- Focus stability
- Accessible names
- Buttons
- Text fields
- Dialogs
- Error announcements
- Loading announcements
- State announcements
- Text scaling
- Touch target sizes
- Non-color-only information

The system must distinguish automated accessibility checks from real device accessibility testing.

## 12. TalkBack Verification

If physical TalkBack testing is unavailable, the system must not claim that TalkBack behavior was fully verified.

The result should be recorded as appropriate:

- STATIC_CHECKED
- USER_CONFIRMED
- NOT_VERIFIED
- BLOCKED

## 13. Offline Testing

For offline-capable applications, tests should verify required functionality without network access when practical.

The system should identify:

- Features that work offline
- Features that require network access
- Behavior when network access disappears

## 14. Online Testing

For online applications, tests should verify:

- Successful network requests
- Invalid responses
- Server errors
- Timeouts
- Network loss
- Authentication failures
- Retry behavior
- Safe handling of remote data

## 15. Hybrid Testing

Hybrid applications should test both offline and online behavior.

The test report must clearly identify which features require network access.

## 16. Error-Path Testing

Important failure conditions should be tested.

Examples:

- Invalid input
- Missing permission
- Network unavailable
- Storage unavailable
- Authentication failure
- API failure
- Unsupported Android version
- Insufficient resources
- Corrupt input

## 17. Boundary Testing

Where relevant, test:

- Empty input
- Minimum input
- Maximum expected input
- Very large input
- Unexpected characters
- Duplicate data
- Missing data
- Invalid formats

## 18. Data Testing

When the application manages data, test:

- Create
- Read
- Update
- Delete
- Import
- Export
- Serialization
- Deserialization
- Migration
- Backup and restore when required

Data-loss risks should receive high priority.

## 19. Security Testing

When applicable, test for:

- Hard-coded secrets
- Excessive permissions
- Unsafe storage
- Insecure network communication
- Unsafe file handling
- Authentication problems
- Authorization problems
- Exported components
- WebView risks
- Sensitive logging
- Input validation

Security testing must follow the Security Policy.

## 20. Privacy Testing

When applicable, verify:

- Only necessary data is collected
- Data is stored appropriately
- External transmission is necessary
- Sensitive data is not unnecessarily exposed
- Privacy-related permissions are appropriate

## 21. Compatibility Testing

Where environments are available, test the approved Android compatibility range.

Consider:

- Android versions
- API levels
- CPU architectures
- Screen sizes
- Permissions
- Platform restrictions

Testing one Android environment must not be reported as testing every supported environment.

## 22. Performance Testing

When performance is important, test:

- Startup time
- Responsiveness
- Memory usage
- CPU usage
- Battery impact
- Network usage
- Large input processing
- Background work

The test environment should be recorded.

## 23. Resource Testing

The system should identify resource-related failures such as:

- Out of memory
- Storage exhaustion
- Excessive CPU use
- Network quota exhaustion
- Provider limits

Testing must not intentionally damage the user's device.

## 24. Regression Testing

After a fix, affected previous tests should be rerun.

Regression testing should confirm:

- Original defect is fixed
- Related functionality remains correct
- Existing features were not unnecessarily broken
- Accessibility has not regressed
- Security has not regressed

## 25. Test Selection

The system should select tests based on changed functionality and risk.

Not every change requires every possible test.

High-risk changes should receive broader testing.

## 26. Test Isolation

Tests should avoid corrupting real user or client data.

Where practical, use:

- Test data
- Temporary environments
- Isolated databases
- Test accounts
- Controlled network conditions

## 27. Test Data Privacy

Test data must not unnecessarily contain:

- Passwords
- API keys
- Private keys
- Payment credentials
- Real confidential client information

Sensitive data must not be copied into ordinary test reports.

## 28. Test Execution Evidence

A test result should preserve evidence such as:

- Test output
- Logs
- Screenshots when available
- Runtime observations
- Tool results
- Artifact information
- User confirmation when applicable

Evidence must not be altered to hide failure.

## 29. Test Failure

When a test fails:

1. Record the actual failure.
2. Identify the affected requirement.
3. Capture evidence.
4. Analyze the likely cause.
5. Create or update a fix plan.
6. Apply an authorized fix.
7. Rebuild when required.
8. Rerun the affected tests.

## 30. Blocked Test

A test must be marked BLOCKED when a required environment, tool, service, device, permission, or dependency is unavailable.

The system must not convert BLOCKED into PASSED.

## 31. Skipped Test

A test may be SKIPPED only for a documented reason.

Skipped tests must remain visible in the test report.

## 32. Test Timeout

Tests must have reasonable execution limits.

A timeout must be recorded as a failure or blocked state according to the actual cause.

The system must not run indefinitely.

## 33. Retry Protection

Retries must be bounded.

A deterministic failure must not trigger an endless retry loop.

## 34. Test Environment

When available, record:

- Operating system
- Android version
- API level
- Device or emulator
- Java version
- Gradle version
- Build tools
- Network condition

Unknown information must be recorded as unknown.

## 35. Test Result Record

Each test result should contain:

- Test ID
- Project ID
- Requirement ID
- Test name
- Test type
- Source version
- Build ID
- Environment
- Expected result
- Actual result
- Status
- Evidence
- Error information
- Date and time

## 36. Test Report

A test report should contain:

- Project
- Source version
- Build
- Test summary
- Passed tests
- Failed tests
- Blocked tests
- Skipped tests
- Important evidence
- Known limitations
- Regression results

## 37. Test Quality Gate

Before declaring testing complete, verify:

- Required tests were identified.
- Required tests were executed when possible.
- Results are recorded.
- Failures are investigated.
- Important requirements have traceability.
- Accessibility was considered.
- Security was considered.
- Offline/online behavior was tested where applicable.
- Regression testing was performed where required.
- Limitations were recorded.

## 38. No False Test Success

The system must never claim:

- Test passed without execution evidence
- Accessibility passed without appropriate evidence
- Offline behavior passed without appropriate testing
- Online behavior passed when the required service was unavailable
- Security passed without appropriate checks
- Compatibility passed across environments that were not tested

## 39. Integration With Verification

Testing results must be passed to the Verification Engine.

The Verification Engine remains responsible for determining whether the available evidence is sufficient for final verification.

## 40. Integration With Build

Testing should normally operate on a known build or source state.

The test record must identify the relevant build/source version.

## 41. Integration With Review

Release-blocking review findings should result in appropriate tests when testing can demonstrate that the issue was resolved.

## 42. Integration With Delivery

Testing must be completed to the level required by the approved release plan before final delivery.

Successful testing alone does not automatically authorize delivery.

## 43. Test History

Test history should be retained as part of project history.

Historical test results must not be silently rewritten.

## 44. Reproducibility

Where practical, tests should be repeatable using the documented:

- Source version
- Build version
- Test configuration
- Environment

Environmental differences should be recorded.

## 45. User Confirmation

When automated testing is unavailable, user confirmation may provide evidence for selected real-world behaviors.

It must be explicitly recorded as:

USER_CONFIRMED

It must not be falsely represented as automated testing.

## 46. Cost and Permission Protection

Testing must not automatically:

- Purchase services
- Enable paid infrastructure
- Increase quotas
- Create paid accounts
- Grant new permissions

without appropriate authorization.

## 47. Accessibility of Test Reports

Test reports should be accessible to users of assistive technologies.

Important results must be available as readable text and must not depend only on visual presentation.

## 48. Final Rule

The Testing System exists to produce reliable evidence about application behavior.

Its fundamental process is:

REQUIREMENTS
→ TEST PLAN
→ EXECUTE
→ COLLECT EVIDENCE
→ ANALYZE
→ FIX
→ RETEST
→ REPORT
→ VERIFICATION

A test result is valid only when it accurately represents what was actually tested.
