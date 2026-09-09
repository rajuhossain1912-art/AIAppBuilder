# AIAppBuilder Agent Orchestrator Specification

## 1. Purpose

The Agent Orchestrator is the central coordination component of AIAppBuilder.

Its responsibility is to control the application's complete development lifecycle while enforcing security, privacy, approval, accessibility, resource, and verification requirements.

The Orchestrator is a coordinator and decision-control layer. It must not bypass security policies or grant itself additional privileges.

---

## 2. Core Development Lifecycle

The standard lifecycle is:

RECEIVED
→ UNDERSTANDING
→ AWAITING_CONFIRMATION
→ PLANNING
→ RESEARCHING
→ GENERATING
→ REVIEWING
→ BUILDING
→ TESTING
→ FIXING
→ VERIFYING
→ DELIVERING
→ COMPLETED

Failures must transition to an appropriate recoverable failure state while preserving diagnostic information.

---

## 3. Main Responsibilities

The Orchestrator must:

- Receive user requirements.
- Preserve the original user request.
- Coordinate requirement analysis.
- Coordinate requirement clarification.
- Create and maintain project state.
- Coordinate planning.
- Trigger research when necessary.
- Coordinate project generation.
- Coordinate code review.
- Coordinate builds.
- Coordinate tests.
- Coordinate error analysis.
- Coordinate fixes.
- Coordinate verification.
- Coordinate artifact delivery.
- Record important activities.
- Enforce security policies.
- Enforce approval boundaries.
- Protect project isolation.
- Respect resource and quota limits.
- Recover safely from failures.
- Prevent uncontrolled retry loops.
- Report the actual state of work honestly.

---

## 4. User Language Handling

The Orchestrator must accept:

- Bangla
- Banglish
- English
- Mixed Bangla-English
- Informal language
- Incomplete sentences
- Typographical errors
- Voice-to-text errors
- Naturally written user requirements

The system should normalize unclear language into a structured requirement without changing the user's intended meaning.

When the intended meaning is materially uncertain, the Orchestrator must request clarification before substantial implementation.

---

## 5. Requirement Preservation

The original user request must be preserved.

The system should maintain:

- Original request
- Normalized request
- Structured requirements
- Assumptions
- Clarifications
- User approvals
- Rejected suggestions
- Final confirmed requirements

The normalized requirement must never silently replace the original request.

---

## 6. Planning Gate

Before substantial generation begins, the Orchestrator should create a plan containing:

- Project goal
- Functional requirements
- Non-functional requirements
- Accessibility requirements
- Security requirements
- Privacy requirements
- Compatibility requirements
- Technical approach
- Required components
- Research requirements
- Build requirements
- Test requirements
- Delivery requirements
- Known risks
- Unresolved questions

The plan should be presented to the user when the task is materially complex or when user approval is required.

---

## 7. Approval Model

The Orchestrator must distinguish between:

### Automatically Allowed Actions

Examples include:

- Parsing requirements
- Creating internal plans
- Reading project files within authorized scope
- Running approved local/project checks
- Building an authorized project
- Running authorized tests
- Reviewing generated code
- Recording audit information

### Actions Requiring User Approval

Examples include:

- Spending money
- Enabling paid services
- Creating billing accounts
- Adding payment methods
- Accessing private external data without prior authorization
- Creating external accounts
- Granting new external permissions
- Destructive deletion
- Public production deployment
- Any materially security-sensitive action outside the approved scope

The Orchestrator must never bypass an approval requirement.

---

## 8. Privilege Boundary

The Orchestrator must operate only with privileges already granted to it.

It must not:

- Grant itself new permissions.
- Create hidden credentials.
- Circumvent access controls.
- Disable security policies.
- Modify its own security boundary without authorized approval.
- Obtain private account access through unauthorized means.

If a required capability is unavailable, the Orchestrator must report the limitation.

---

## 9. Project Isolation

Every project must have an independent project identity.

The Orchestrator must ensure that:

- Project A cannot accidentally overwrite Project B.
- Project-specific secrets are not copied between projects.
- Project-specific private information is not added to global knowledge.
- Files are created inside the correct project.
- Project state remains associated with the correct project.

---

## 10. File Placement

Before creating or modifying a file, the Orchestrator must:

1. Identify the purpose of the file.
2. Check the canonical repository structure.
3. Check whether the file already exists.
4. Determine whether an update is more appropriate than creating a duplicate.
5. Confirm the target project when project-specific.
6. Avoid arbitrary file locations.

The canonical repository structure is defined by `PROJECT_STRUCTURE.md`.

---

## 11. State Management

The Orchestrator must maintain explicit state.

A state record should contain, when applicable:

- Project ID
- Current lifecycle state
- Previous state
- Timestamp
- Current task
- Completed tasks
- Pending tasks
- Blocked tasks
- Errors
- Retry count
- Required approvals
- Received approvals
- Last successful operation
- Last verified result

State transitions must be recorded.

---

## 12. State Transition Rules

The Orchestrator must not skip important lifecycle stages without a justified reason.

Examples:

- A project should not be marked COMPLETED merely because code was generated.
- A project should not be marked DELIVERING if the required artifact was never produced.
- A build failure must not be reported as a successful build.
- An untested feature must not be reported as fully verified.
- A blocked operation must remain visibly blocked.

---

## 13. Research Coordination

The Orchestrator should trigger research when:

- Information may be outdated.
- A technical decision depends on current documentation.
- A dependency requires verification.
- An API behavior is uncertain.
- Compatibility information is uncertain.
- A security-sensitive implementation requires authoritative information.

Research should prioritize official and primary sources.

Research results should be passed to the appropriate planning or implementation component.

---

## 14. Generation Coordination

The Orchestrator should provide the generation component with:

- Confirmed requirements
- Technical plan
- Architecture decisions
- Relevant research
- Security requirements
- Accessibility requirements
- Compatibility requirements
- Project structure rules
- Existing project state

Generated code must remain inside the authorized project scope.

---

## 15. Review Gate

Before building, generated or modified code should pass a review stage.

The review should consider:

- Correctness
- Security
- Privacy
- Accessibility
- Maintainability
- Compatibility
- Resource usage
- Dependency usage
- Project requirements
- Unnecessary changes

Important unresolved problems should block delivery.

---

## 16. Build Coordination

The Orchestrator must initiate builds only for the intended project and configuration.

It must capture:

- Build start
- Build result
- Build logs
- Error information
- Artifact information
- Build duration when available

A successful build must be based on actual build evidence.

---

## 17. Test Coordination

The Orchestrator should run appropriate tests based on the project.

Possible checks include:

- Compilation
- Unit tests
- Integration tests
- UI tests
- Accessibility checks
- Security checks
- Compatibility checks
- Resource checks

Testing requirements should be proportional to the application.

---

## 18. Error Recovery

When an operation fails:

1. Capture the real error.
2. Preserve the diagnostic information.
3. Determine the affected component.
4. Analyze the likely cause.
5. Research when necessary.
6. Apply the smallest appropriate fix.
7. Rebuild or retest.
8. Verify the result.
9. Record the outcome.

The Orchestrator must not hide errors.

---

## 19. Retry Protection

Retries must be bounded.

The Orchestrator must maintain a retry counter for recoverable operations.

A practical initial retry range may be approximately 5–10 attempts depending on the operation.

If repeated attempts fail:

- Stop the loop.
- Preserve diagnostics.
- Report the actual problem.
- Request user input when appropriate.

The system must prevent infinite automated retry loops.

---

## 20. Preservation of Working Features

The Orchestrator must prefer minimal changes.

Before a significant modification, it should identify affected functionality when practical.

After a fix, it should verify that unrelated working functionality has not been unnecessarily broken.

---

## 21. Accessibility Gate

Accessibility must be considered throughout the lifecycle rather than only at final delivery.

For Android applications, the Orchestrator should coordinate checks for:

- TalkBack compatibility
- Accessibility labels
- Focus order
- Focus stability
- Touch target usability
- Text readability
- Error discoverability
- Accessible custom controls
- Non-color-only communication
- Non-position-only communication

Accessibility defects must be treated as real defects.

---

## 22. Security Gate

Before delivery, the Orchestrator should coordinate security checks for:

- Secrets
- Permissions
- Network security
- Data handling
- Authentication
- Storage
- Dependencies
- Exported components
- Debug configuration
- Release configuration

Security policy is defined by `config/policy/SECURITY_POLICY.md`.

---

## 23. Resource and Quota Gate

Before potentially expensive operations, the Orchestrator should check available resources and quotas when that information is available.

It must not silently:

- Spend money
- Enable paid services
- Increase billing
- Bypass provider limits

If a free resource is unavailable, the Orchestrator should stop the affected operation and explain the limitation.

---

## 24. Audit Coordination

Important events should be recorded.

Examples include:

- Requirement received
- Requirement changed
- Approval received
- Plan created
- Research performed
- File created
- File modified
- Build started
- Build succeeded
- Build failed
- Test started
- Test failed
- Fix applied
- Verification completed
- Artifact created
- Delivery completed
- Operation blocked

Audit records must not contain secrets.

---

## 25. Memory Coordination

The Orchestrator must ensure that important project history is stored durably.

It should preserve:

- Project identity
- Requirements
- Decisions
- Approvals
- Research findings
- File changes
- Build results
- Test results
- Errors
- Fixes
- Releases
- Known limitations
- User feedback

The system must not rely only on temporary AI conversation context.

---

## 26. Delivery Gate

Before delivery, the Orchestrator must determine:

- Was the requested functionality implemented?
- Was the project successfully built?
- Were relevant tests completed?
- Were important errors resolved?
- Was accessibility reviewed?
- Was security reviewed?
- Was the requested artifact actually produced?
- Are there known limitations?

Only verified results may be described as verified.

---

## 27. Honest Reporting

The Orchestrator must clearly distinguish between:

- Planned
- In progress
- Generated
- Built
- Tested
- Partially tested
- Verified
- Blocked
- Failed
- Delivered

It must never claim that an action occurred when it did not.

---

## 28. Safe Stop

The Orchestrator must safely stop when:

- Required permission is missing.
- Required approval is missing.
- A security policy would be violated.
- Required resources are unavailable.
- A critical dependency cannot be verified.
- Repeated recovery attempts fail.
- The requested operation exceeds authorized capabilities.

A safe stop must preserve the project state and diagnostics.

---

## 29. Recovery

After an interruption, the Orchestrator should be able to recover from durable project state.

It should determine:

- Last known state
- Last completed action
- Pending action
- Last known error
- Required approvals
- Last successful build
- Last verified result

The system should continue only when the recovered state is sufficiently trustworthy.

---

## 30. Modularity

The Orchestrator must communicate with specialized components through clear interfaces.

Potential components include:

- Requirements Engine
- Planning Engine
- Research Engine
- Generation Engine
- Review Engine
- Build Engine
- Test Engine
- Verification Engine
- Memory Manager
- Audit Manager
- Provider Manager
- Quota Manager
- Delivery Manager

The Orchestrator should coordinate these components rather than duplicating all their responsibilities.

---

## 31. No Hidden Actions

The Orchestrator must not perform materially important actions secretly.

Important external actions, security-sensitive actions, destructive actions, and paid actions must be visible through appropriate approval and audit mechanisms.

---

## 32. Final Orchestration Rule

The Orchestrator exists to turn a user idea into a verified software result through controlled stages.

The required principle is:

Understand
→ Confirm when necessary
→ Plan
→ Research
→ Generate
→ Review
→ Build
→ Test
→ Fix
→ Verify
→ Deliver
→ Record
→ Learn from verified outcomes

Safety, security, accessibility, privacy, correctness, and honest reporting must remain active throughout the entire lifecycle.
