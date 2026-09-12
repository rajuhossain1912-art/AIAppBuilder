# PROJECT PASSPORT SPECIFICATION

## 1. Purpose

The Project Passport is the authoritative long-term identity and state record for one AIAppBuilder project.

It must preserve enough verified information to understand, recover, audit, continue, migrate, and deliver a project safely.

The passport must never be treated as a substitute for source code, build artifacts, audit records, or verification evidence.

---

## 2. Core Principles

The Project Passport must be:

- Persistent
- Project-specific
- Traceable
- Auditable
- Searchable
- Privacy-aware
- Security-aware
- Recoverable
- Version-aware
- Evidence-based
- Provider-independent
- Accessible
- Honest about uncertainty
- Safe against false success

No information may be invented merely to complete a passport field.

---

## 3. Project Identity

Every project must have:

- project_id
- project_name
- project_description
- project_type
- owner
- creation_date
- last_updated_date
- current_lifecycle_state
- current_project_version
- project_status

The project identity must remain stable throughout the project's lifetime.

---

## 4. Project ID

The project ID must be unique.

Recommended format:

`project-YYYYMMDD-short-name-random-id`

The ID must not contain secrets, passwords, API keys, payment information, or unnecessary personal information.

---

## 5. Project Scope

The passport must record:

- What the project is intended to do
- Main user/client purpose
- Supported platforms
- Important limitations
- Major functional boundaries
- Important non-goals

Scope changes must be recorded as decisions or requirement changes.

---

## 6. Ownership and Authority

The passport must identify the authorized project owner or controlling actor.

The agent must not assume authority that has not been granted.

The passport must distinguish:

- User instruction
- User approval
- Agent action
- External information
- Verified result

These must never be treated as equivalent.

---

## 7. Lifecycle State

The passport must track the current lifecycle state.

Allowed lifecycle states are:

`RECEIVED`

`UNDERSTANDING`

`AWAITING_CONFIRMATION`

`PLANNING`

`RESEARCHING`

`GENERATING`

`REVIEWING`

`BUILDING`

`TESTING`

`FIXING`

`VERIFYING`

`DELIVERING`

`COMPLETED`

Lifecycle state changes must be traceable.

---

## 8. Project Status

The project status must clearly indicate its operational condition.

Recommended statuses include:

- ACTIVE
- BLOCKED
- PAUSED
- COMPLETED
- FAILED
- ARCHIVED
- RECOVERING

The agent must not report a project as completed unless the required completion and verification conditions are satisfied.

---

## 9. Project Version

The passport must record the current project version.

Version changes must be traceable to the relevant change, decision, or release.

Schema versions must also be tracked so older passport records can be migrated safely.

---

## 10. Repository Reference

The passport may contain the repository reference required to locate the project.

Repository references must not contain secrets.

The passport must record enough information to identify the correct repository, branch, project location, and relevant revision when necessary.

---

## 11. Requirements

The passport must preserve important confirmed requirements.

Requirements may include:

- Functional requirements
- Accessibility requirements
- Security requirements
- Privacy requirements
- Performance requirements
- Compatibility requirements
- Offline/online requirements
- Client requirements
- Delivery requirements

Original user requirements must not be silently replaced by normalized requirements.

---

## 12. Approvals

Important approvals must be recorded.

Approval records must identify:

- What was approved
- Who approved it
- When it was approved
- What action the approval covers
- Whether the approval has expired or been superseded

Explicit approval is required for consequential actions such as:

- Spending money
- Using paid services
- Accessing private external data
- Using external accounts
- Destructive deletion
- Public production deployment
- Security-sensitive actions outside normal scope

---

## 13. Architecture Decisions

Important architecture decisions must be recorded with their reasons.

A decision should identify:

- Decision
- Reason
- Alternatives considered when relevant
- Approval if required
- Date
- Related project/version

Rejected important alternatives may also be recorded when useful.

---

## 14. Technology Information

The passport should record important technology choices, including when applicable:

- Android version range
- Minimum SDK
- Target SDK
- Kotlin
- Jetpack Compose
- Libraries
- APIs
- Build tools
- Storage technologies
- External services

Technology information must be kept current.

---

## 15. Accessibility Requirements

Accessibility is a first-class project requirement.

The passport must preserve important accessibility requirements such as:

- TalkBack compatibility
- Screen-reader labels
- Keyboard/accessibility navigation
- Focus order
- Touch target requirements
- Content descriptions
- Accessible error messages
- Non-visual workflows
- Android accessibility compatibility

Accessibility requirements must be considered during planning, generation, review, testing, and verification.

---

## 16. Security and Privacy Requirements

The passport must preserve important security and privacy requirements.

These may include:

- Data minimization
- Authentication requirements
- Authorization requirements
- Secure storage
- Network security
- Permission boundaries
- Client-data protection
- Secret protection
- Project isolation

Secrets must never be stored directly in the passport.

---

## 17. Provider Usage

The passport may record which AI or external providers were used.

Provider records should identify:

- Provider
- Model when relevant
- Purpose
- Date/time
- Project
- Result status

Provider usage must remain subject to provider policy, approval, privacy, quota, and security controls.

---

## 18. Research Findings

Important research findings may be recorded.

Each important finding should preserve:

- Source
- Date
- Topic
- Finding
- Confidence
- Relevance
- Related decision or requirement

External information must not automatically become trusted permanent knowledge.

Conflicting information must be identified and resolved or marked uncertain.

---

## 19. Files Created and Modified

The passport must maintain important file history.

It should record:

- Files created
- Files modified
- Important file paths
- Related purpose
- Relevant project/version
- Important change references

The agent must follow the canonical repository structure and must not create arbitrary duplicate locations.

---

## 20. Build History

Important builds must be recorded.

A build record should include:

- Build identifier
- Date/time
- Project version
- Build type
- Result
- Error reference when failed
- Verification status

A build succeeding technically does not automatically mean the application is correct.

---

## 21. Test History

Important test results must be recorded.

Test records may include:

- Test identifier
- Test type
- Date/time
- Result
- Failed tests
- Related build
- Related fix
- Verification status

Accessibility, security, functional, compatibility, and regression tests should be tracked when applicable.

---

## 22. Errors

Important errors must be preserved.

Each error should include enough information to understand:

- What happened
- When it happened
- Project/version
- Stage
- Related file or operation when known
- Whether it was resolved

Errors must not be silently deleted merely because a later build succeeds.

---

## 23. Fixes

Important fixes must be recorded.

A fix should be traceable to:

- Error
- File/change
- Date/time
- Project/version
- Test result
- Verification result when available

---

## 24. Artifacts

Important generated artifacts must be recorded.

Examples:

- APK
- AAB
- Source archive
- Test report
- Verification report
- Release package

The passport must distinguish an artifact existing from an artifact being verified.

---

## 25. Releases and Delivery

A release record should identify:

- Release version
- Date/time
- Artifact
- Verification status
- Delivery status
- Recipient or delivery target when appropriate

The agent must never claim delivery when delivery has not actually occurred.

---

## 26. Rollbacks

Important rollback actions must be recorded.

A rollback record should identify:

- What was rolled back
- Why
- From which version
- To which known-good version
- Date/time
- Result

The system should preserve the last known good state whenever possible.

---

## 27. User Feedback

Important user/client feedback must be preserved.

Feedback should be connected to the relevant project, requirement, version, issue, or decision whenever possible.

User feedback must not automatically override confirmed requirements without an appropriate change process.

---

## 28. Known Problems

Known unresolved problems must be recorded.

Each problem should contain:

- Description
- Severity when known
- Project/version
- Current status
- Workaround when available
- Related error/fix/test

Known problems must remain visible until resolved or explicitly accepted.

---

## 29. Important Decisions

Important project decisions must be preserved for long-term recall.

A decision should contain:

- Decision
- Reason
- Date/time
- Authority
- Related requirement
- Related project/version
- Consequences when important

---

## 30. Metadata

Metadata may contain additional structured information.

Metadata must not be used as an uncontrolled replacement for defined passport fields.

Metadata must not contain:

- Passwords
- API keys
- Access tokens
- Private keys
- Payment credentials
- Authentication secrets

Sensitive information must use the appropriate secure system.

---

## 31. Traceability

Important records must be traceable across the lifecycle.

The system should connect, when applicable:

Requirement → Plan → Research → Decision → File Change → Build → Test → Review → Verification → Artifact → Delivery

Traceability must support investigation and recovery.

---

## 32. Evidence and Confidence

Important claims must have an evidence or confidence level when appropriate.

Recommended confidence levels:

- VERIFIED
- HIGH_CONFIDENCE
- MEDIUM_CONFIDENCE
- LOW_CONFIDENCE
- UNVERIFIED

The agent must never convert an unverified claim into a verified result without evidence.

---

## 33. Timestamping

Important passport events must have reliable timestamps.

Where appropriate, timestamps should include:

- Date
- Time
- Time zone

Timestamps should use a consistent machine-readable format.

UTC ISO 8601 is recommended for stored timestamps.

---

## 34. Privacy Classification

Important records should have a privacy classification.

Recommended classifications:

- PUBLIC
- PROJECT_PRIVATE
- CLIENT_PRIVATE
- USER_PRIVATE
- SECURITY_SENSITIVE

Privacy classification must influence storage, access, export, backup, and migration behavior.

---

## 35. Secrets Protection

The Project Passport must never be a secret store.

Passwords, API keys, access tokens, private keys, authentication credentials, and payment credentials must not be stored in ordinary passport data.

Secrets must use an approved secure-storage mechanism.

---

## 36. Project Isolation

Data from one project must not accidentally appear in another project.

The system must use project identity when storing and retrieving project-specific information.

Cross-project reuse must be explicit, authorized, and safe.

---

## 37. Persistence

The passport must survive normal process termination and system interruption.

Persistent storage must be reliable and recoverable.

A successful in-memory update is not sufficient if the durable record was not saved.

---

## 38. Recovery

The system must support recovery after:

- App restart
- Agent interruption
- Build failure
- Network failure
- Provider failure
- Partial operation
- Storage failure

Recovery must use the last durable verified state rather than assumptions.

---

## 39. Migration

Passport data must be migratable between compatible schema versions.

Migration must:

- Preserve important information
- Avoid silent data loss
- Record migration version
- Validate the migrated result
- Fail safely when migration is impossible

---

## 40. Schema Evolution

The passport schema must have an explicit schema version.

Changes to the schema must be deliberate and documented.

Backward compatibility or migration must be considered before changing authoritative fields.

---

## 41. Consistency Rules

The passport must remain internally consistent.

Examples:

- A delivered artifact should reference a real artifact record.
- A completed project should have appropriate completion evidence.
- A verification result must correspond to an actual verification process.
- A rollback must reference a real prior state.
- A file record must use a valid project path.

Contradictory records must be detected and reported.

---

## 42. Auditability

Important passport changes must be auditable.

The passport records project state.

The Audit system records actions and events.

Neither system should silently replace the responsibility of the other.

---

## 43. Relationship to Memory

The Project Passport is part of the long-term project memory system.

The passport provides authoritative project identity and important project state.

Detailed historical events should remain in the appropriate memory or audit records.

---

## 44. One-Year Recall

The system must support project recall for at least one year.

Historical information should remain searchable by:

- Date
- Project
- Version
- Requirement
- Decision
- File
- Error
- Fix
- Build
- Test
- Release
- Keyword

The system must not invent historical information when records are unavailable.

---

## 45. Searchability

Project records should support searching in:

- Bangla
- Banglish
- English
- Mixed language

Search should support normal spelling variations where practical without changing authoritative stored records.

---

## 46. Data Integrity

Persistent passport data must be protected against accidental corruption.

The system should use:

- Validation
- Atomic writes where possible
- Version information
- Integrity checks when appropriate
- Safe recovery

A corrupted passport must not be treated as trustworthy without validation.

---

## 47. Backup

Important passport data must be backed up according to the project's backup policy.

Backups should preserve:

- Project identity
- Important history
- Schema version
- Integrity information

Backups must not expose protected secrets or private data.

---

## 48. Failure Handling

When passport operations fail, the agent must:

1. Stop unsafe continuation.
2. Preserve the last known good durable state.
3. Record the failure when possible.
4. Report the actual condition.
5. Retry only within approved limits.
6. Require recovery or user intervention when necessary.

---

## 49. Safety and Approval Boundary

The passport does not authorize actions.

Approval must come from the appropriate approval system.

The agent must not interpret the existence of a passport record as permission to:

- Spend money
- Access private accounts
- Access private data
- Delete important data
- Publish software
- Perform security-sensitive actions

---

## 50. No False Success

The passport must never contain a successful result merely because an operation was attempted.

Success requires appropriate evidence.

Examples:

- Build success requires an actual successful build.
- Test success requires actual test results.
- Verification success requires verification evidence.
- Delivery success requires actual delivery confirmation.

---

## 51. Authoritative Boundaries

The passport is authoritative for project identity and selected project state.

It is not authoritative for:

- Secrets
- Raw source code
- Complete audit history
- Complete test logs
- Complete build logs
- External provider truth
- User identity verification
- Payment records

Those belong to their designated systems.

---

## 52. Minimum Passport Record

A valid minimum passport must contain:

- project_id
- project_name
- project_description
- project_type
- owner
- creation_date
- last_updated_date
- current_lifecycle_state
- current_project_version
- project_status
- requirements
- approvals
- architecture_decisions
- files_created
- files_modified
- builds
- tests
- errors
- fixes
- artifacts
- releases
- known_problems
- important_decisions
- metadata

---

## 53. Validation

Before accepting a passport record, the system should validate:

- Required identity fields
- Valid project ID
- Valid lifecycle state
- Valid project status
- Valid version information
- Correct data types
- Required timestamps
- Project isolation
- Privacy classification where required
- No prohibited secrets

Invalid records must be rejected safely.

---

## 54. Implementation Boundary

The Project Passport model must remain separate from:

- Orchestrator state management
- Audit logging
- Secret storage
- Build execution
- Test execution
- Provider management
- Delivery execution

These systems may reference the passport but must not bypass their own policies.

---

## 55. Relationship to Orchestrator

The Orchestrator controls lifecycle execution.

The Project Passport preserves important durable project information.

Lifecycle transitions should be reflected consistently between the Orchestrator and Passport.

A passport must not independently authorize lifecycle actions.

---

## 56. Relationship to Audit

Audit records should provide detailed evidence of important actions.

The passport may reference important audit events.

The passport must not replace the audit log.

---

## 57. Relationship to Build and Test

Build and test systems must provide their own authoritative results.

The passport may store summaries and references.

The passport must not manufacture build or test results.

---

## 58. Relationship to Review and Verification

Review determines whether generated work satisfies relevant quality requirements.

Verification determines whether required claims and outputs are actually supported by evidence.

The passport may summarize these results but must not replace them.

---

## 59. Relationship to Delivery

Delivery must occur only after the required build, testing, review, verification, security, accessibility, and approval gates have passed.

The passport should preserve the final delivery state.

---

## 60. Project Completion

A project may be marked COMPLETED only when the required completion conditions are satisfied.

Depending on project type, this may include:

- Requirements confirmed
- Required generation completed
- Review completed
- Build succeeded
- Required tests passed
- Accessibility requirements checked
- Security requirements checked
- Verification completed
- Artifact created
- Delivery completed when required

---

## 61. Last Known Good State

The system should maintain enough information to identify the last known good project state.

This is critical for safe recovery and rollback.

A failed change must not automatically replace a previously verified good state.

---

## 62. Client and User Data

Client and user information must be minimized.

Only information required for project operation should be retained.

Private information must receive appropriate privacy classification and protection.

The agent must not expose one client's information to another project.

---

## 63. Provider Independence

The passport must remain usable even if an AI provider or external service becomes unavailable.

Provider-specific data must not make the project permanently dependent on one provider.

---

## 64. Cost Awareness

The passport may record important cost-related information.

Cost information must never be interpreted as authorization to spend money.

Paid actions require the appropriate approval.

---

## 65. Performance and Resource Awareness

The passport may record important resource limitations.

The agent should consider:

- CPU
- Memory
- Storage
- Network
- Build time
- API quotas

Resource limits must not be silently ignored.

---

## 66. Privacy During Export

Passport export must preserve privacy classifications.

Protected records must not be exported to public locations without authorization.

Secrets must never be exported as ordinary passport data.

---

## 67. Privacy During Migration

Migration must preserve privacy and security boundaries.

Protected data must not become public merely because the project was moved to another storage location.

---

## 68. Recovery Verification

After recovery or migration, the system should verify:

- Project identity
- Schema validity
- Data integrity
- Important references
- Lifecycle state
- Last known good state
- Required privacy boundaries

A recovered record must not be declared healthy without validation.

---

## 69. Change Management

Important changes to passport structure or meaning must be documented.

Changes should identify:

- What changed
- Why
- Schema version
- Migration requirement
- Compatibility impact

---

## 70. Implementation Quality Gate

The Project Passport implementation is acceptable only when:

- Required identity is persistent.
- Important project history is preserved.
- Lifecycle information is consistent.
- Requirements and approvals are traceable.
- Files and versions are traceable.
- Build/test/review/verification results are not fabricated.
- Privacy and security boundaries are respected.
- Recovery is possible.
- Schema evolution is manageable.
- Project isolation is preserved.
- One-year recall is supported.
- The implementation works with the Orchestrator, Memory, Audit, Build, Test, Verification, and Delivery systems.

---

## 71. Final Principle

The Project Passport exists to preserve the trustworthy identity and history of a project.

It must help AIAppBuilder remember what a project is, what was requested, what was approved, what was decided, what was changed, what succeeded, what failed, what was verified, what remains unresolved, and what must happen next.

When information is unknown, the system must say it is unknown.

When information is unverified, the system must say it is unverified.

When an operation failed, the system must say it failed.

When an action requires approval, the system must wait for approval.

The Project Passport must preserve truth, traceability, safety, privacy, recoverability, and user control above all else.
