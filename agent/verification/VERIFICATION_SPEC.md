# AIAppBuilder Verification Engine Specification

## 1. Purpose

The Verification Engine determines whether an implemented application actually works according to the confirmed requirements, approved plan, generated implementation, review findings, and available test evidence.

Verification is evidence-based.

The engine must never declare success merely because code exists, a build command was requested, or a previous stage reported success.

---

## 2. Core Principle

The Verification Engine must verify actual results.

It must distinguish between:

- IMPLEMENTED
- BUILT
- TESTED
- VERIFIED
- NOT_VERIFIED
- FAILED
- BLOCKED

These statuses must never be treated as interchangeable.

---

## 3. Required Inputs

The Verification Engine should receive:

- Confirmed requirements
- Requirement IDs
- Approved plan
- Research findings
- Generated files
- Modified files
- Review findings
- Build configuration
- Test definitions
- Test results
- Expected behavior
- Known limitations
- Previous verification results

---

## 4. Verification Lifecycle

The normal verification flow is:

REQUIREMENTS
→ IMPLEMENTATION
→ REVIEW
→ BUILD
→ TEST
→ RESULT_COLLECTION
→ REQUIREMENT_VERIFICATION
→ SECURITY_VERIFICATION
→ ACCESSIBILITY_VERIFICATION
→ COMPATIBILITY_VERIFICATION
→ ARTIFACT_VERIFICATION
→ FINAL_STATUS

If a required stage cannot be performed:

→ BLOCKED

The engine must explain why verification is blocked.

---

## 5. Evidence Principle

Every important verification result should be supported by evidence.

Possible evidence includes:

- Successful build output
- Test output
- Test logs
- Static analysis results
- Security scan results
- Accessibility test results
- Compatibility results
- Generated artifact
- File inspection
- Runtime behavior
- User-confirmed behavior when appropriate

A claim without sufficient evidence must not be marked verified.

---

## 6. Requirement Verification

For each requirement, determine:

- VERIFIED
- PARTIALLY_VERIFIED
- NOT_VERIFIED
- FAILED
- BLOCKED
- NOT_APPLICABLE

The engine must map each important requirement to verification evidence.

Example:

REQ-001
→ Implementation
→ TEST-001
→ Evidence
→ VERIFIED

---

## 7. Build Verification

When a build is required, verify:

- Build command
- Build environment
- Build variant
- Build result
- Build errors
- Build warnings when relevant
- Generated artifacts

The engine must distinguish:

- BUILD_NOT_ATTEMPTED
- BUILD_RUNNING
- BUILD_SUCCEEDED
- BUILD_FAILED
- BUILD_BLOCKED

A build must not be marked successful without actual successful build evidence.

---

## 8. Build Reproducibility

When practical, verification should determine whether the project can be built consistently using the documented configuration.

Important build dependencies should be recorded.

If reproducibility cannot be established, the limitation must be reported.

---

## 9. Test Execution

Tests should be executed according to the approved testing plan when the required tools and environment are available.

Test status must be one of:

- TEST_PASSED
- TEST_FAILED
- TEST_NOT_RUN
- TEST_BLOCKED
- TEST_NOT_APPLICABLE

The engine must never infer TEST_PASSED from the absence of an error message.

---

## 10. Unit Test Verification

When unit tests exist, verify:

- Tests were actually executed
- Results are available
- Failures are recorded
- Important requirements have appropriate coverage when practical

Passing unit tests do not automatically prove complete application correctness.

---

## 11. Integration Verification

For applications with multiple components, verify important interactions such as:

- UI to business logic
- Business logic to data layer
- Data layer to API
- Storage operations
- Authentication
- Media processing
- External integrations

The exact scope depends on the application.

---

## 12. UI Verification

Verify important user workflows.

Examples:

- Application starts
- Navigation works
- Required controls operate
- Forms accept valid input
- Invalid input is handled
- Loading states work
- Error states work
- Required results appear
- Important actions complete successfully

---

## 13. Accessibility Verification

When accessibility is a confirmed requirement, verification must include accessibility behavior.

Consider:

- TalkBack access
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
- Touch targets
- Non-color-only information

Visual correctness alone is insufficient for accessibility verification.

---

## 14. Accessibility Acceptance

An accessibility requirement should only be marked VERIFIED when there is sufficient evidence that the intended accessible behavior works.

If direct device testing is unavailable, the result must be marked appropriately:

- NOT_VERIFIED
- BLOCKED
- STATICALLY_VERIFIED

The engine must not pretend that a real TalkBack test occurred when it did not.

---

## 15. Security Verification

Verify important security requirements including, when applicable:

- No hard-coded secrets
- Appropriate permissions
- Secure storage
- Secure network communication
- Safe file handling
- Authentication
- Authorization
- Exported component configuration
- WebView security
- Sensitive logging
- Input validation

Security verification must follow:

`config/policy/SECURITY_POLICY.md`

---

## 16. Secret Verification

The engine should verify that source files and generated artifacts do not expose obvious:

- API keys
- Passwords
- Tokens
- Private keys
- Authentication credentials

If a possible secret is detected, verification should be blocked or failed according to severity.

Sensitive values must not be reproduced unnecessarily in reports.

---

## 17. Privacy Verification

Verify that:

- Required data collection is implemented correctly.
- Unnecessary data is not collected.
- Data is transmitted only where required.
- Storage follows the approved plan.
- Deletion behavior works where required.
- External services receive only necessary information.

---

## 18. Compatibility Verification

When practical, verify the application against the approved compatibility target.

Consider:

- Android versions
- API levels
- CPU architectures
- Screen sizes
- Storage behavior
- Permissions
- Platform restrictions

If only one environment can be tested, the report must not claim that every supported environment was verified.

---

## 19. Performance Verification

When performance is important, verify:

- Startup behavior
- CPU usage when relevant
- Memory usage when relevant
- Battery impact when relevant
- Network usage
- Large input handling
- Background processing

Performance results must include the tested environment when relevant.

---

## 20. Large Input Verification

For applications handling large text, files, images, audio, or other data, verify:

- Application remains responsive
- Memory usage remains reasonable
- Processing completes or fails safely
- Cancellation works when required
- Errors are handled
- Data is not unnecessarily lost

---

## 21. Offline Verification

For offline applications, verify required features without network access where practical.

For hybrid applications, verify both:

- Offline behavior
- Online behavior

An application must not be marked fully offline-capable if a required feature silently depends on network access.

---

## 22. Network Verification

For network-enabled features, verify:

- Requests are made correctly
- Responses are handled correctly
- Invalid responses are handled
- Network failure is handled
- Timeouts are handled
- Authentication failures are handled
- Sensitive data is protected

---

## 23. Error Verification

Important failure paths should be tested.

Examples:

- Invalid input
- Network unavailable
- Permission denied
- Storage unavailable
- Authentication failure
- API failure
- Unsupported environment
- Resource exhaustion

The expected behavior must be defined before the test is considered successful.

---

## 24. Data Verification

Verify important data operations:

- Create
- Read
- Update
- Delete
- Import
- Export
- Serialization
- Deserialization
- Migration
- Backup when required

Data-loss risks must receive high priority.

---

## 25. Artifact Verification

When an APK, AAB, or other artifact is generated, verify:

- Artifact exists
- Expected artifact type
- Expected build variant
- Artifact is associated with the correct project
- Artifact corresponds to the verified source state
- Artifact is not corrupted when the available tools permit checking

The engine must not report an artifact as delivered if it was not actually produced.

---

## 26. Artifact Identity

Verification should record, when available:

- Artifact name
- Version
- Version code
- Build variant
- Commit or source identifier
- Checksum or equivalent identifier

This helps connect the delivered artifact to the verified project state.

---

## 27. Regression Verification

After fixes, verify that:

- The original defect is resolved.
- Related requirements still work.
- Existing working features remain functional.
- Accessibility has not regressed.
- Security has not regressed.
- Build behavior remains valid.

---

## 28. Review Finding Verification

Every release-blocking review finding should have a corresponding verification result.

Example:

REVIEW-001
→ FIX-001
→ TEST-001
→ VERIFIED

An issue must not be considered resolved merely because the corresponding code changed.

---

## 29. Verification Environment

The verification record should identify relevant environment information.

Examples:

- Operating system
- Android version
- API level
- Device or emulator
- Build tools
- Runtime version
- Network condition

If an environment detail is unknown, record it as unknown rather than inventing it.

---

## 30. Verification Limitations

Verification must clearly state what could not be tested.

Examples:

- No physical device available
- No emulator available
- External API unavailable
- Required permission unavailable
- Required service unavailable
- Test environment unavailable
- Build tool unavailable

Limitations must not be hidden.

---

## 31. User Confirmation

User confirmation may be used as evidence for behavior that requires real-world user interaction when automated verification is unavailable.

The report must identify it as:

USER_CONFIRMED

It must not be represented as an automated test.

---

## 32. Verification Result Format

Each verification record should contain:

- Verification ID
- Project ID
- Requirement ID
- Test or evidence ID
- Environment
- Action
- Expected result
- Actual result
- Status
- Evidence
- Limitations
- Date and time

---

## 33. Verification Status

The overall verification status should be one of:

- VERIFIED
- VERIFIED_WITH_WARNINGS
- FAILED
- BLOCKED
- INCOMPLETE

### VERIFIED

Required verification evidence is sufficient and no known blocking issue remains.

### VERIFIED_WITH_WARNINGS

Required verification passed, but non-blocking limitations or warnings remain.

### FAILED

One or more required verification checks failed.

### BLOCKED

Required verification could not be performed.

### INCOMPLETE

Some required verification has not yet been completed.

---

## 34. Release Gate

Final delivery should normally require:

- Required MUST_HAVE requirements verified
- Required build verified
- Required tests passed
- Release-blocking review findings resolved
- Critical security issues resolved
- Required accessibility checks passed
- Required compatibility checks completed or explicitly accepted
- Artifact verified

---

## 35. No False Verification

The Verification Engine must never claim:

- Build succeeded without build evidence.
- Test passed without test evidence.
- Accessibility verified without appropriate evidence.
- Security verified without appropriate checks.
- Compatibility verified without testing or sufficient evidence.
- Artifact exists without confirming its existence.
- Feature works merely because code exists.

---

## 36. No Silent Exceptions

A failed or blocked verification must not be silently converted into success.

Exceptions require:

- Clear documentation
- Reason
- Risk
- Appropriate authorization
- Affected requirement

---

## 37. Automatic Reverification

When a verified component is modified, affected verification should be considered stale until rerun or otherwise re-established.

The engine should identify which requirements and tests are affected by a change.

---

## 38. Verification History

Each verification session should record:

- Verification ID
- Project ID
- Source version
- Artifact version
- Date and time
- Environment
- Results
- Failures
- Warnings
- Limitations
- Final status

Verification history must not be silently deleted.

---

## 39. Project Isolation

Verification records and artifacts must remain associated with the correct project.

The engine must not expose:

- Private source code
- Credentials
- Client information
- Private test data
- Confidential verification reports

to unrelated projects or unauthorized external parties.

---

## 40. Cost and Permission Protection

Verification must not automatically:

- Purchase services
- Enable paid APIs
- Increase quotas
- Create paid infrastructure
- Grant new permissions

without appropriate authorization.

---

## 41. Evidence Integrity

Verification evidence should be preserved when practical.

Evidence should allow a reviewer to determine:

- What was tested
- How it was tested
- Where it was tested
- What result occurred
- When it occurred

The engine must not modify evidence to make a failed result appear successful.

---

## 42. Final Verification Report

The final report should contain:

- Project
- Source version
- Artifact
- Requirement status
- Build status
- Test status
- Security status
- Accessibility status
- Compatibility status
- Performance status when applicable
- Review status
- Remaining warnings
- Limitations
- Final verification status

---

## 43. Handoff to Delivery Engine

Only after verification is complete should the result be passed to the Delivery Engine.

The handoff should contain:

- Verified project state
- Verified artifact
- Verification report
- Requirement traceability
- Remaining warnings
- Accepted limitations
- Delivery authorization status

---

## 44. Verification Quality Gate

Before declaring verification complete, verify:

- Requirements were checked.
- Build result is evidenced.
- Tests were actually run when required.
- Test results are recorded.
- Security was checked.
- Accessibility was checked.
- Compatibility was considered.
- Important errors were tested.
- Review findings were rechecked.
- Artifact was verified.
- Limitations were recorded.
- No false success was reported.

---

## 45. Final Rule

The Verification Engine exists to answer:

"Did the implemented software actually satisfy the confirmed requirements, and do we have enough evidence to prove it?"

Its fundamental process is:

IMPLEMENTATION
→ BUILD
→ TEST
→ COLLECT EVIDENCE
→ VERIFY REQUIREMENTS
→ VERIFY SECURITY
→ VERIFY ACCESSIBILITY
→ VERIFY COMPATIBILITY
→ VERIFY ARTIFACT
→ REPORT
→ HAND OFF

Verification is the evidence boundary between "we built it" and "we have demonstrated that it works."
