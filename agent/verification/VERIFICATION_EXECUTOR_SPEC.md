# AIAppBuilder Verification Executor Specification

## 1. Purpose

The Verification Executor performs authorized verification checks and produces evidence for the Verification Engine.

## 2. Core Principle

Verification must be based on actual evidence.

The executor must never report a requirement as verified merely because source code exists or a previous stage reported success.

## 3. Execution Flow

PREPARE
→ VALIDATE
→ EXECUTE
→ COLLECT EVIDENCE
→ EVALUATE
→ REPORT

## 4. Preconditions

Before execution, verify:

- Correct project
- Correct source version
- Correct build
- Correct test results
- Required verification configuration
- Required tools
- Required environment
- Required authorization
- Required resources

## 5. Verification Scope

The executor may perform checks for:

- Requirements
- Build
- Tests
- Security
- Privacy
- Accessibility
- Compatibility
- Performance
- Offline behavior
- Online behavior
- Artifacts
- Regression
- Review findings

Only applicable checks should be executed.

## 6. Requirement Verification

For each required requirement, determine whether available implementation and evidence are sufficient.

Valid states include:

- VERIFIED
- PARTIALLY_VERIFIED
- NOT_VERIFIED
- FAILED
- BLOCKED
- NOT_APPLICABLE

## 7. Evidence Collection

The executor should collect available:

- Build evidence
- Test evidence
- Static analysis
- Security results
- Accessibility results
- Compatibility results
- Runtime results
- Artifact information
- User confirmation when appropriate

## 8. Evidence Integrity

Evidence must be preserved accurately.

The executor must not modify evidence to make an unsuccessful result appear successful.

## 9. Build Verification

When required, verify:

- Correct project
- Correct source
- Correct variant
- Actual build result
- Expected artifact
- Artifact integrity when supported

## 10. Test Verification

Verify that required tests:

- Were actually executed
- Used the intended source/build
- Produced a recorded result
- Have sufficient evidence

The executor must not infer a passed test from missing error output.

## 11. Security Verification

When applicable, check for:

- Hard-coded secrets
- Unsafe permissions
- Insecure storage
- Unsafe network communication
- Unsafe file handling
- Authentication problems
- Authorization problems
- Unsafe exported components
- WebView risks
- Sensitive logging

Security checks must follow the Security Policy.

## 12. Privacy Verification

When applicable, verify:

- Necessary data collection
- Appropriate storage
- Required external transmission
- Data minimization
- Appropriate deletion behavior
- Protection of private information

## 13. Accessibility Verification

When accessibility is required, verify available evidence for:

- Accessible names
- Focus behavior
- Navigation
- Buttons
- Text fields
- Dialogs
- Error announcements
- Loading announcements
- State announcements
- Text scaling
- Touch targets
- TalkBack behavior when directly testable

The executor must distinguish static checks from real device testing.

## 14. TalkBack Verification

The executor must never claim that TalkBack was tested on a physical or emulated device unless such testing actually occurred.

Possible results include:

- VERIFIED
- STATICALLY_VERIFIED
- USER_CONFIRMED
- NOT_VERIFIED
- BLOCKED

## 15. Compatibility Verification

When applicable, verify the tested environment against the approved compatibility target.

The executor must record the actual tested:

- Android version
- API level
- Device or emulator
- CPU architecture when relevant
- Screen configuration when relevant

Testing one environment must not be reported as verification of every environment.

## 16. Offline Verification

For offline-capable applications, verify required offline functionality when the environment allows network isolation.

If offline testing cannot actually be performed, report:

- NOT_VERIFIED
- BLOCKED

as appropriate.

## 17. Online Verification

For online functionality, verify:

- Network request behavior
- Response handling
- Authentication
- Timeout handling
- Network failure handling
- External service availability

External service failure must be distinguished from application failure when possible.

## 18. Hybrid Verification

For hybrid applications, separately verify:

- Offline features
- Online features
- Network transition behavior
- Failure behavior when connectivity is lost

## 19. Artifact Verification

When an artifact exists, verify:

- File exists
- Correct artifact type
- Correct project
- Correct source/build association
- Correct variant
- Readability
- Integrity when supported

## 20. Regression Verification

After an authorized fix, execute affected verification checks again.

The executor should identify:

- Previous result
- Changed source
- Retest result
- Remaining failures

## 21. Review Finding Verification

For release-blocking review findings, verify that:

- The finding is identified
- The intended fix exists
- Relevant tests were performed
- The original problem is no longer present when testable

Code modification alone is insufficient evidence.

## 22. Error Handling

If verification execution fails:

1. Preserve the evidence.
2. Record the failure.
3. Identify the affected verification.
4. Classify the failure.
5. Return the result to the Verification Engine.

## 23. Blocked Verification

A verification check must be BLOCKED when a required:

- Tool
- Device
- Emulator
- Service
- Permission
- Dependency
- Environment
- Artifact

is unavailable.

Blocked must never become verified without new evidence.

## 24. Timeout

Verification operations must have reasonable execution limits.

A timeout must be recorded accurately.

The executor must not run indefinitely.

## 25. Retry

Retries must be bounded.

A deterministic failure must not cause an endless retry loop.

## 26. Environment Record

When available, record:

- Operating system
- Android version
- API level
- Device or emulator
- Build identifier
- Test environment
- Network condition
- Relevant tool versions

Unknown information must remain unknown.

## 27. Resource Protection

Verification must respect:

- CPU
- Memory
- Storage
- Network
- Time
- Provider quotas

Verification must not intentionally damage the user's device.

## 28. Privacy Protection

Private project, client, and test information must not be unnecessarily transmitted or exposed.

Secrets must not be copied into verification reports.

## 29. Cost Protection

The executor must not automatically:

- Purchase services
- Enable paid APIs
- Increase quotas
- Create paid infrastructure

without required authorization.

## 30. Verification Record

Each execution should record:

- Verification ID
- Project ID
- Requirement ID
- Source version
- Build ID
- Test/evidence ID
- Verification type
- Environment
- Action
- Expected result
- Actual result
- Status
- Evidence
- Limitations
- Date and time

## 31. Honest Reporting

The executor must distinguish:

- VERIFIED
- NOT_VERIFIED
- FAILED
- BLOCKED
- INCOMPLETE
- UNKNOWN

It must never invent evidence.

## 32. No False Verification

The executor must never report:

- Requirement verified without evidence
- Security verified without appropriate checks
- Accessibility verified without appropriate evidence
- Offline behavior verified without offline testing
- Online behavior verified when the required service was unavailable
- Compatibility verified across untested environments
- Artifact verified without confirming the artifact

## 33. Verification Staleness

When source, configuration, build, or relevant behavior changes, affected previous verification results may become stale.

The executor should identify affected verification results and request re-verification when required.

## 34. Integration

The Verification Executor integrates with:

- Orchestrator
- Requirements
- Planning
- Research
- Generation
- Review
- Build System
- Test System
- Verification Engine
- Delivery Engine
- Approval Policy
- Security Policy
- Privacy Policy
- Resource Policy

## 35. Delivery Gate

The executor must provide sufficient verification evidence before an artifact is considered eligible for delivery.

Final delivery authorization remains governed by the Delivery and Approval processes.

## 36. Final Rule

The Verification Executor exists to perform real verification checks and return accurate evidence.

Its process is:

REQUIREMENT
→ CHECK
→ EVIDENCE
→ EVALUATE
→ RECORD
→ VERIFICATION ENGINE
→ FINAL STATUS

No evidence means no verified claim.
