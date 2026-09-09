# AIAppBuilder Review Engine Specification

## 1. Purpose

The Review Engine evaluates generated or modified software before verification and delivery.

Its purpose is to identify defects, regressions, security risks, accessibility problems, compatibility problems, requirement mismatches, unnecessary changes, and other issues that could prevent safe delivery.

The Review Engine must provide evidence-based findings and must never claim that software is correct without sufficient verification.

---

## 2. Core Principle

The Review Engine must review the actual project state against:

- Confirmed requirements
- Approved plan
- Research findings
- Project structure
- Security policy
- Accessibility requirements
- Compatibility requirements
- Testing requirements

Review must be independent from the assumption that generated code is correct.

---

## 3. Required Inputs

The Review Engine should receive:

- Original user request
- Confirmed requirements
- Requirement IDs
- Approved technical plan
- Research findings
- Generated files
- Modified files
- Existing project state
- Build configuration
- Test results when available
- Security policy
- Accessibility requirements
- Known limitations
- Previous review findings

---

## 4. Review Scope

The Review Engine should inspect, when applicable:

- Source code
- Project structure
- Build files
- Dependencies
- Manifest
- Resources
- UI
- Accessibility behavior
- Network code
- Data handling
- Security-sensitive code
- Privacy-sensitive code
- Tests
- Documentation
- Configuration
- Generated artifacts

---

## 5. Requirement Compliance

For each important requirement, determine:

- IMPLEMENTED
- PARTIALLY_IMPLEMENTED
- NOT_IMPLEMENTED
- NOT_VERIFIED
- BLOCKED
- NOT_APPLICABLE

Each finding should reference the relevant requirement ID whenever possible.

The engine must not mark a requirement as implemented merely because code appears related to it.

---

## 6. Requirement Traceability

The Review Engine should maintain:

Requirement
→ Plan
→ Implementation
→ Review
→ Test
→ Verification

Missing links should be reported.

Example:

REQ-001
→ PLAN-001
→ File: MainActivity
→ REVIEW-001
→ TEST-001
→ VERIFICATION-001

---

## 7. Code Quality Review

Review generated code for:

- Correctness
- Readability
- Maintainability
- Duplication
- Unnecessary complexity
- Naming
- Error handling
- Resource management
- Lifecycle handling
- Threading
- State management
- Potential crashes

The engine should distinguish stylistic issues from functional defects.

---

## 8. Build Configuration Review

Inspect:

- Gradle configuration
- Plugins
- SDK versions
- Java/Kotlin configuration
- Dependencies
- Repositories
- Build variants
- Manifest
- Resource configuration

Identify:

- Invalid configuration
- Version conflicts
- Unnecessary dependencies
- Unsafe repositories
- Compatibility risks
- Build-breaking changes

---

## 9. Dependency Review

For every newly added dependency, check when possible:

- Purpose
- Version
- License
- Maintenance
- Compatibility
- Security
- Resource impact
- Whether an existing dependency could already provide the required functionality

Unnecessary dependencies should be reported.

---

## 10. Security Review

Review against:

`config/policy/SECURITY_POLICY.md`

Look for:

- Hard-coded secrets
- Exposed API keys
- Unsafe storage
- Excessive permissions
- Insecure network communication
- Unsafe file handling
- Unsafe WebView configuration
- Improper authentication
- Improper authorization
- Exported component risks
- Injection risks
- Unsafe logging
- Sensitive information exposure

Security issues should receive high priority when appropriate.

---

## 11. Secret Detection

The Review Engine should detect possible:

- API keys
- Access tokens
- Passwords
- Private keys
- Authentication credentials
- Cloud credentials

Possible secrets must be reported without unnecessarily exposing their complete value.

The engine must never reproduce sensitive credentials in review output.

---

## 12. Privacy Review

Check whether the application:

- Collects unnecessary personal information
- Sends unnecessary information externally
- Stores unnecessary data
- Uses unnecessary analytics
- Uses unnecessary tracking
- Shares data with external services without appropriate authorization

Privacy issues should be mapped to requirements when possible.

---

## 13. Accessibility Review

Accessibility must be treated as a release-critical quality area when the project requires accessibility.

Review:

- TalkBack compatibility
- Accessible names
- Semantic information
- Focus order
- Focus stability
- Button accessibility
- Text-field accessibility
- Dialog accessibility
- Error announcements
- Loading announcements
- State announcements
- Touch target size
- Text scaling
- Contrast
- Non-color-only communication

The engine should identify both code-level and workflow-level accessibility problems.

---

## 14. Accessibility Regression Review

When an existing accessible feature is modified, compare the expected behavior before and after the change when evidence is available.

Potential regressions include:

- Controls no longer reachable
- Focus unexpectedly moving
- Labels disappearing
- Buttons becoming inaccessible
- Dialogs becoming difficult to operate
- Important information no longer announced

Accessibility regressions must not be ignored merely because visual UI still works.

---

## 15. Compatibility Review

Review against the approved compatibility target.

Consider:

- Android versions
- API levels
- Device architectures
- Screen sizes
- Storage behavior
- Permissions
- Platform restrictions
- Dependency compatibility
- Runtime behavior

The engine should avoid declaring universal compatibility without evidence.

---

## 16. Performance Review

Check for unnecessary:

- CPU usage
- RAM usage
- Battery usage
- Storage usage
- Network requests
- Background work
- Repeated expensive operations
- Memory leaks

Resource-intensive operations should be reviewed especially carefully for lower-resource devices.

---

## 17. Large Input Review

When the application handles large text, files, images, audio, or other data, review:

- Memory usage
- Processing strategy
- UI responsiveness
- Background processing
- Cancellation
- Error handling
- Storage requirements

The application should not unnecessarily crash or freeze because of large user input.

---

## 18. Network Review

For network-enabled applications, review:

- Secure transport
- Request validation
- Response validation
- Timeouts
- Retry behavior
- Error handling
- Authentication
- Connectivity failures
- Sensitive data transmission

The application must not assume that network connectivity always exists.

---

## 19. Offline Review

For offline or hybrid applications, verify that offline functionality matches the approved plan.

Look for:

- Accidental network dependency
- Missing offline fallback
- Incorrect local storage
- Data synchronization problems
- Unclear offline error behavior

---

## 20. UI Review

Review:

- Navigation
- Layout
- Responsive behavior
- Text visibility
- User feedback
- Loading states
- Error states
- Empty states
- Accessibility
- Consistency

The Review Engine must distinguish functional UI problems from subjective design preferences.

---

## 21. Copyright and Originality Review

Review whether generated assets or implementation unnecessarily copy protected material.

Potential concerns:

- Logos
- Trademarks
- Copyrighted images
- Copyrighted sounds
- Proprietary code
- Proprietary branding
- Unverified third-party assets

If licensing cannot be verified, report the uncertainty.

---

## 22. Data Review

Review:

- Data models
- Storage
- Serialization
- Validation
- Migration
- Import
- Export
- Backup
- Deletion

Data loss risks should receive appropriate severity.

---

## 23. Error Handling Review

Check whether expected errors are handled.

Examples:

- Invalid input
- Network failure
- Permission denial
- Storage failure
- API failure
- Authentication failure
- Unsupported device behavior
- Resource exhaustion

Errors should not silently disappear.

---

## 24. Logging Review

Check that logs do not expose:

- Passwords
- Tokens
- API keys
- Personal information
- Private project information
- Sensitive application data

Diagnostic logging should remain useful without creating privacy or security risks.

---

## 25. Test Review

Review whether tests cover important requirements.

Possible test categories:

- Unit
- Integration
- UI
- Accessibility
- Security
- Compatibility
- Performance
- Error handling

Missing tests for important requirements should be reported.

---

## 26. Test Result Integrity

The Review Engine must distinguish:

- TEST_PASSED
- TEST_FAILED
- TEST_NOT_RUN
- TEST_BLOCKED
- TEST_NOT_APPLICABLE

A test must never be marked passed unless evidence shows that it actually passed.

---

## 27. Change Scope Review

For modifications to an existing project, review:

- Files changed
- Lines or areas changed
- Dependencies changed
- Configuration changed
- Existing functionality affected

Unnecessary changes should be reported because they increase regression risk.

---

## 28. Regression Review

Check whether changes could break existing functionality.

Potential regressions include:

- Existing UI behavior
- Existing accessibility
- Existing APIs
- Existing storage
- Existing navigation
- Existing tests
- Existing build behavior

Regression risk should be explicitly recorded.

---

## 29. Risk Classification

Each finding should have a severity:

- CRITICAL
- HIGH
- MEDIUM
- LOW
- INFORMATIONAL

### CRITICAL

Issues that can cause severe security, data-loss, safety, or fundamental application failure.

### HIGH

Major functional, security, accessibility, or compatibility problems.

### MEDIUM

Important problems that should normally be fixed before final delivery.

### LOW

Minor defects or maintainability concerns.

### INFORMATIONAL

Observations that do not currently block delivery.

---

## 30. Review Finding Format

Each finding should contain:

- Finding ID
- Severity
- Category
- Requirement ID when applicable
- File
- Location when available
- Problem
- Evidence
- Impact
- Recommended action
- Verification requirement

Example:

REVIEW-001

Severity:
HIGH

Category:
ACCESSIBILITY

Requirement:
REQ-005

Problem:
The primary action is not accessible through TalkBack.

Impact:
A visually impaired user cannot complete the required workflow.

Recommended action:
Provide an accessible semantic label and verify TalkBack focus behavior.

---

## 31. False Positive Control

The Review Engine must avoid reporting speculative problems as confirmed defects.

If evidence is insufficient, classify the finding as:

- NEEDS_VERIFICATION
- POSSIBLE_RISK
- INFORMATIONAL

The engine must explain what evidence is missing.

---

## 32. Automatic Fixes

The Review Engine may recommend fixes.

It may apply an automatic fix only when:

- The change is low-risk.
- The intended behavior is unambiguous.
- The change is within the approved plan.
- No security-sensitive authorization is being bypassed.
- Existing functionality is unlikely to regress.

High-risk changes should be passed back to the appropriate planning or approval process.

---

## 33. No Silent Requirement Changes

The Review Engine must never solve a review finding by silently changing a confirmed requirement.

If the implementation conflicts with the requirement, report the conflict.

---

## 34. No False Approval

The Review Engine must never say:

- "Everything is correct"
- "Ready for release"
- "All tests passed"

unless sufficient evidence actually supports the statement.

---

## 35. Review Gates

The Review Engine should provide a gate status:

- PASS
- PASS_WITH_WARNINGS
- FAIL
- BLOCKED

### PASS

No known release-blocking issues remain.

### PASS_WITH_WARNINGS

No known release-blocking issue remains, but lower-priority findings exist.

### FAIL

One or more important issues must be fixed.

### BLOCKED

Review cannot continue because required evidence, files, tools, or permissions are unavailable.

---

## 36. Security Gate

A known unresolved CRITICAL security issue should normally block approval.

A HIGH security issue should normally require resolution or explicit authorized exception before delivery.

---

## 37. Accessibility Gate

When accessibility is a confirmed core requirement, a severe accessibility failure should normally block final delivery.

The Review Engine must not treat accessibility as optional merely because the application functions visually.

---

## 38. Requirement Gate

A MUST_HAVE requirement that is not implemented or verified should normally block final delivery.

---

## 39. Build Gate

If the project is expected to build, an unresolved build failure should normally block delivery.

The engine must distinguish:

- Build not attempted
- Build failed
- Build succeeded
- Build blocked

---

## 40. Review Handoff

When findings require changes, the Review Engine should return them to the appropriate stage:

- Requirements issue → Requirements Engine
- Technical planning issue → Planning Engine
- Missing research → Research Engine
- Implementation issue → Generation Engine
- Verification issue → Verification Engine

This prevents the wrong component from attempting to solve the wrong problem.

---

## 41. Review History

Each review should record:

- Review ID
- Project ID
- Date and time
- Reviewed version or commit
- Requirements version
- Plan version
- Findings
- Gate result
- Fix status
- Remaining risks

Review history must not be silently deleted.

---

## 42. Re-Review

After fixes, the affected area must be reviewed again.

The engine should verify:

- Original finding resolved
- No new regression introduced
- Related tests updated
- Requirement still satisfied

A previously failed review must not automatically become passed merely because code changed.

---

## 43. Project Isolation

Review data must remain associated with the correct project.

The engine must not expose:

- Client source code
- Private requirements
- Credentials
- Private review findings
- Confidential project information

to unrelated projects or external parties.

---

## 44. Cost and Permission Protection

Review must not automatically:

- Purchase services
- Enable paid APIs
- Increase quotas
- Create paid infrastructure
- Grant new permissions

without appropriate authorization.

---

## 45. Review Quality Gate

Before completing a review, verify:

- Requirements were checked.
- Plan was checked.
- Generated changes were inspected.
- Security was reviewed.
- Privacy was reviewed.
- Accessibility was reviewed.
- Compatibility was reviewed.
- Performance was considered.
- Dependencies were reviewed.
- Tests were reviewed.
- Regressions were considered.
- Findings have severity.
- Evidence is recorded.
- Gate status is justified.
- No false success was reported.

---

## 46. Final Rule

The Review Engine exists to find problems before they become delivered problems.

Its fundamental process is:

REQUIREMENTS
→ PLAN
→ IMPLEMENTATION
→ INSPECT
→ TEST EVIDENCE
→ IDENTIFY RISKS
→ CLASSIFY FINDINGS
→ FIX OR ESCALATE
→ RE-REVIEW
→ APPROVE OR BLOCK

Review is not a substitute for testing.

Testing is not a substitute for review.

Only combined evidence from requirements, planning, implementation, review, testing, and verification can support final delivery.
