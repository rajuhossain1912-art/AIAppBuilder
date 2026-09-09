# AIAppBuilder Generation Engine Specification

## 1. Purpose

The Generation Engine converts an approved implementation plan into an actual software project or controlled modifications to an existing project.

It must generate code, configuration, resources, tests, documentation, and other required project files according to the confirmed requirements and approved plan.

The Generation Engine must not silently change confirmed requirements.

---

## 2. Core Principle

Generation must be:

- Requirement-driven
- Plan-driven
- Security-aware
- Accessibility-aware
- Compatibility-aware
- Testable
- Maintainable
- Reproducible
- Project-isolated
- Conservative with existing working functionality

The engine must prefer correct and understandable implementation over unnecessary complexity.

---

## 3. Required Inputs

The Generation Engine should receive:

- Original user request
- Confirmed requirements
- Requirement identifiers
- User approvals
- Technical plan
- Architecture
- Technology decisions
- Research findings
- File plan
- Security requirements
- Privacy requirements
- Accessibility requirements
- Compatibility requirements
- Performance requirements
- Testing requirements
- Project structure rules
- Existing project state when applicable

---

## 4. Generation Boundary

The Generation Engine may create or modify files only within the authorized project scope.

It must not:

- Modify unrelated projects.
- Access unrelated private data.
- Create hidden files outside the approved scope.
- Create arbitrary repository structures.
- Bypass security policies.
- Grant itself new permissions.
- Create unauthorized credentials.
- Enable paid services without approval.

---

## 5. New Project Generation

For a new project, the engine should generate the project foundation first.

Typical order:

1. Project configuration
2. Build configuration
3. Application manifest
4. Source structure
5. Core models
6. Data layer
7. Business logic
8. UI
9. Accessibility implementation
10. Integrations
11. Error handling
12. Tests
13. Documentation
14. Security configuration
15. Build configuration verification

The actual order may change according to the approved plan.

---

## 6. Existing Project Generation

When modifying an existing project, the engine must first understand the existing project.

It should identify:

- Existing files
- Existing architecture
- Existing dependencies
- Existing features
- Existing build configuration
- Existing tests
- Existing accessibility behavior
- Existing security controls

The engine must prefer modifying the appropriate existing file rather than creating unnecessary duplicates.

Existing working functionality must be preserved unless the user explicitly requests a change.

---

## 7. File Placement

Every generated file must have a planned destination.

The engine must follow:

`PROJECT_STRUCTURE.md`

Before creating a file, it should verify:

- Target path
- File purpose
- Whether the file already exists
- Whether an existing file should be modified
- Project ownership
- Dependencies

The engine must not create arbitrary folders or files.

---

## 8. Generation Manifest

Before substantial generation, the engine should maintain a generation manifest.

The manifest should identify:

- Project ID
- Generation session ID
- Requirement IDs
- Planned files
- Existing files to modify
- New files
- Dependencies
- Generated tests
- Expected artifacts

The manifest should make generation traceable.

---

## 9. Requirement Traceability

Generated implementation must remain connected to requirement IDs.

Example:

REQ-001
→ PLAN-001
→ GEN-001
→ File(s)
→ TEST-001
→ VERIFICATION-001

Important requirements must not disappear during generation.

---

## 10. Code Generation Principles

Generated code should be:

- Clear
- Consistent
- Maintainable
- Modular where appropriate
- Properly named
- Properly structured
- Documented when useful
- Free from unnecessary duplication
- Free from unnecessary dependencies

The engine should not generate excessively complicated code for simple requirements.

---

## 11. Language Selection

The Generation Engine must use the programming language and framework approved by the Planning Engine.

For Android projects, it should prefer the project's established language and architecture unless the approved plan explicitly specifies otherwise.

It must not introduce a different framework merely for convenience.

---

## 12. Dependency Handling

A dependency may be introduced only when justified by the plan or a verified technical requirement.

Before adding a dependency, the engine should consider:

- Purpose
- Version
- License
- Security
- Compatibility
- Maintenance
- Resource impact
- Existing alternatives

Unnecessary dependencies must not be added.

---

## 13. Dependency Reproducibility

Generated projects should use reproducible dependency declarations whenever practical.

The engine should avoid:

- Unpinned unstable dependencies when unnecessary
- Unverified repositories
- Unknown binary sources
- Unnecessary dynamic versions

Dependency changes must be recorded.

---

## 14. Android Generation

For Android applications, generation should consider:

- Minimum SDK
- Target SDK
- Compile SDK
- Gradle version
- Java/Kotlin version
- AndroidX compatibility
- Manifest configuration
- Runtime permissions
- Storage behavior
- Background restrictions
- Device compatibility

The implementation must follow the approved compatibility plan.

---

## 15. Accessibility-First Generation

Accessibility must be implemented as part of the application rather than added after the UI is complete.

For Android applications, generated interfaces should consider:

- TalkBack
- Accessibility labels
- Semantic information
- Logical focus order
- Stable focus behavior
- Accessible buttons
- Accessible text fields
- Accessible dialogs
- State announcements
- Error announcements
- Loading announcements
- Touch target size
- Text scaling
- Contrast
- Non-color-only communication

Custom UI components must provide appropriate accessibility behavior.

---

## 16. Accessibility Regression Protection

When modifying an existing accessible application, the engine should identify accessibility-sensitive code before changing it.

After changes, accessibility-related tests or verification must be included when applicable.

The engine must not knowingly remove existing accessibility behavior without explicit approval.

---

## 17. Security-First Generation

Generated code must follow:

`config/policy/SECURITY_POLICY.md`

The engine should prevent:

- Hard-coded secrets
- Exposed API keys
- Insecure storage
- Unnecessary permissions
- Unsafe network communication
- Unsafe file handling
- Unvalidated sensitive input
- Insecure exported components
- Debug-only security weaknesses in release configuration

---

## 18. Secrets

The Generation Engine must never place real secrets directly into source code.

It should use appropriate configuration or secret-management mechanisms supported by the project environment.

If a secret is required but unavailable, generation should clearly identify the missing configuration instead of inventing one.

---

## 19. Privacy-Aware Generation

Generated applications should collect and transmit only information required by confirmed requirements.

The engine should avoid unnecessary:

- Analytics
- Tracking
- Personal data collection
- Device information collection
- External transmission

Privacy-sensitive behavior should be documented and testable.

---

## 20. Network Generation

For online applications, generated network code should include appropriate:

- Request handling
- Response handling
- Timeout behavior
- Error handling
- Connectivity failure handling
- Authentication handling
- Secure transport
- Data validation

For hybrid applications, offline fallback behavior should follow the approved plan.

---

## 21. Offline Generation

For offline applications, generated code must not accidentally introduce unnecessary network dependencies.

The engine should consider:

- Local storage
- Local processing
- Device resources
- Offline error handling
- Backup requirements
- Application size

If a requested feature cannot operate offline, the engine must identify the limitation.

---

## 22. Input Validation

Generated applications should validate user input at appropriate boundaries.

Validation should consider:

- Missing values
- Invalid formats
- Excessive input
- Unexpected values
- Malformed data
- Security-sensitive input

Validation errors should be understandable and accessible.

---

## 23. Error Handling

Generated applications must handle expected failures.

Examples:

- Network unavailable
- Permission denied
- Invalid input
- Storage unavailable
- Authentication failure
- API failure
- Resource exhaustion
- Unsupported device behavior

Errors should not be silently swallowed.

User-facing errors should be understandable and accessible.

---

## 24. Logging

Logging should be useful for diagnosis without exposing sensitive information.

The engine must avoid logging:

- Passwords
- Authentication tokens
- API secrets
- Sensitive personal information
- Private project information

Release builds should follow the project's approved logging policy.

---

## 25. Resource Efficiency

Generated applications should avoid unnecessary:

- CPU usage
- RAM usage
- Battery usage
- Storage usage
- Network requests
- Background work

Large inputs should be handled safely.

Resource-intensive features should follow the approved performance plan.

---

## 26. UI Generation

Generated UI must follow the approved design requirements.

The engine should ensure:

- Consistent navigation
- Clear hierarchy
- Predictable interactions
- Responsive layouts
- Appropriate text scaling
- Accessible controls
- Clear feedback

The engine must not copy another application's protected branding or proprietary visual assets.

---

## 27. Original Design

When the user requests an application similar to an existing application, the engine may implement common functional concepts but must create an original implementation.

It must avoid unauthorized copying of:

- Source code
- Logos
- Trademarks
- Copyrighted images
- Copyrighted sounds
- Proprietary assets
- Protected branding

Licensing concerns identified by the Research Engine must be respected.

---

## 28. Localization

When multiple languages are required, generated text should use an appropriate localization structure rather than unnecessarily hard-coding user-facing strings.

The engine should preserve:

- Bangla
- English
- Other approved languages

according to the project requirements.

---

## 29. User Language

The agent must understand user instructions regardless of whether they are written in:

- Bangla
- Banglish
- English
- Mixed language

The generated application's language behavior must follow the confirmed requirements.

---

## 30. Code Review Preparation

Generated code must be structured so that the Review Engine can inspect:

- Changed files
- New files
- Dependencies
- Requirement mapping
- Security-sensitive code
- Accessibility-sensitive code
- Potential regressions

Generation should produce enough metadata for later review.

---

## 31. Test Generation

The Generation Engine should generate appropriate tests alongside implementation when practical.

Possible tests include:

- Unit tests
- Integration tests
- UI tests
- Accessibility tests
- Data tests
- Error-handling tests
- Security checks

Tests should map to requirement IDs.

---

## 32. Build Configuration

Generated build configuration must be consistent with the approved plan.

The engine should verify:

- Plugin versions
- SDK versions
- Dependency declarations
- Build variants
- Manifest configuration
- Resource configuration
- Required repositories

It must avoid unnecessary changes to working build configuration.

---

## 33. Generated Documentation

When appropriate, the engine should generate or update:

- README
- Setup instructions
- Configuration instructions
- Architecture notes
- API usage information
- Build instructions
- Testing instructions
- Known limitations

Documentation must describe the actual implementation rather than planned features that were never implemented.

---

## 34. Incremental Generation

For large projects, generation should be incremental.

The engine should:

1. Generate a controlled group of files.
2. Validate the group.
3. Continue only when the result is acceptable.
4. Record progress.
5. Recover safely after interruption.

This reduces the risk of large uncontrolled changes.

---

## 35. Generation Checkpoints

Important generation stages should create checkpoints.

A checkpoint may record:

- Generation session
- Completed files
- Pending files
- Current requirement
- Current phase
- Build status
- Test status
- Errors
- Recovery information

---

## 36. Safe Modification

Before modifying an existing file, the engine should determine:

- Why it must change
- Which requirements require the change
- Which existing behavior may be affected
- Whether a smaller change is possible

The engine should prefer the smallest change that correctly satisfies the requirement.

---

## 37. No Blind Replacement

The engine must not replace an entire existing project or major source file simply because doing so is easier.

Large replacements require a clear technical reason and should be treated as higher-risk changes.

---

## 38. Failure Handling

If generation fails:

1. Preserve the error.
2. Record the affected file or operation.
3. Stop unsafe cascading changes.
4. Analyze the cause.
5. Request research when necessary.
6. Apply a controlled fix.
7. Revalidate.
8. Continue only when safe.

---

## 39. No False Success

The Generation Engine must never claim:

- A file was created when it was not.
- A feature was implemented when it was not.
- A build succeeded when it did not.
- A test passed when it was not run.
- A bug was fixed when it was not verified.

Actual evidence must determine status.

---

## 40. Project Isolation

Every generated artifact must belong to the correct project.

The engine must prevent:

- Cross-project source leakage
- Cross-project secrets
- Cross-project private requirements
- Accidental file overwrites
- Incorrect project references

---

## 41. Client Project Protection

When generating an application for another person or organization, the engine must keep client-specific information isolated.

Client requirements and private data must not become shared global knowledge unless they have been appropriately sanitized and are safe to reuse.

---

## 42. Cost Control

Generation must respect the approved cost constraints.

It must not:

- Enable paid APIs automatically
- Create paid infrastructure
- Increase billing limits
- Purchase services
- Subscribe to services

without the required authorization.

---

## 43. Free-First Implementation

When the confirmed requirement is "free," generation should prefer:

1. Built-in platform features
2. Existing project capabilities
3. Compatible open-source solutions
4. Verified free services
5. Paid services only after explicit approval

The engine must clearly identify any unavoidable paid dependency.

---

## 44. Compatibility Protection

Generated code should avoid unnecessary device-specific behavior.

For Android applications, compatibility should be considered across the approved Android range.

The engine should prefer broadly supported APIs when practical.

---

## 45. Performance and Processor Safety

The generated application must not intentionally perform unnecessary heavy processing.

For resource-intensive operations, the engine should consider:

- Background execution
- Memory limits
- CPU usage
- Battery impact
- Large-file handling
- Cancellation
- Progress feedback

The application should avoid behavior that can unnecessarily overload the user's device.

---

## 46. Verification Handoff

After generation, the engine should provide the Verification Engine with:

- Generated files
- Modified files
- Requirement mapping
- Test results when available
- Build configuration
- Known limitations
- Known errors
- Security-sensitive changes
- Accessibility-sensitive changes

Generation is not verification.

---

## 47. Generation Quality Gate

Before declaring generation complete, verify:

- Required files were created.
- Existing files were modified only when necessary.
- File locations follow project structure.
- Requirements remain traceable.
- Dependencies are justified.
- Security requirements are followed.
- Accessibility requirements are implemented.
- Privacy requirements are respected.
- Compatibility requirements are considered.
- Tests exist where appropriate.
- No secrets were embedded.
- No unauthorized paid services were introduced.
- Known errors are recorded.
- Documentation reflects actual implementation.

---

## 48. Final Rule

The Generation Engine exists to transform an approved plan into controlled, maintainable, testable software.

Its fundamental process is:

APPROVED REQUIREMENTS
→ APPROVED PLAN
→ CONTROLLED GENERATION
→ FILE VALIDATION
→ TEST PREPARATION
→ REVIEW HANDOFF
→ VERIFICATION

Generation must never be treated as proof that the application is correct.

Only successful review, testing, and verification can establish that the requested application is ready for delivery.
