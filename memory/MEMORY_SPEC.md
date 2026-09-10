# AIAppBuilder Memory and Long-Term History Specification

## 1. Purpose

The Memory System provides persistent, structured, searchable, and project-isolated memory for AIAppBuilder.

It must allow the agent to remember important decisions, actions, project history, lessons, approvals, verification results, and other authorized information over long periods.

The system must support reliable historical recall even after many months or years.

---

## 2. Core Principle

Memory must be:

- Persistent
- Structured
- Searchable
- Timestamped
- Project-aware
- Traceable
- Privacy-aware
- Security-aware
- Recoverable
- Auditable

Memory must not depend only on the current conversation context.

---

## 3. Long-Term Recall

The system should allow the agent to answer historical questions such as:

- What did you do on a particular date?
- What decision was made about a project?
- Which files were changed?
- Why was a decision made?
- Which requirements were approved?
- Which tests were performed?
- What problems were encountered?
- How was a previous problem solved?
- What happened during an earlier project version?

Historical answers must be based on stored evidence whenever available.

---

## 4. Date and Time

Important memory records should contain:

- Date
- Time
- Time zone
- Event type
- Project ID when applicable
- Actor
- Action
- Result

The system must not invent dates or times.

If exact time is unavailable, it should be recorded as unknown rather than guessed.

---

## 5. Memory Categories

The memory system should separate information into appropriate categories.

### Passport Memory

Stable project and system identity information.

Location:

`memory/passport/`

### Audit Memory

Historical actions and events.

Location:

`memory/audit/`

### Lessons Memory

Validated lessons learned from previous work.

Location:

`memory/lessons/`

### Backup Memory

Recovery and memory backup information.

Location:

`memory/backups/`

---

## 6. Project Isolation

Memory must be associated with the correct project.

Project-specific memory must not automatically become global memory.

Client-specific information must remain isolated from unrelated projects.

---

## 7. Global Knowledge vs Project Memory

The system must distinguish:

- Global knowledge
- General technical knowledge
- Project-specific knowledge
- Client-specific information
- Temporary session information
- Historical audit records

A project-specific decision must not automatically be treated as a universal rule.

---

## 8. Memory Importance

Memory should have importance levels such as:

- CRITICAL
- HIGH
- NORMAL
- LOW
- TEMPORARY

Critical and high-value records should receive stronger preservation and backup protection.

---

## 9. Memory Types

Possible memory record types include:

- USER_PREFERENCE
- PROJECT_DECISION
- REQUIREMENT
- APPROVAL
- ACTION
- FILE_CHANGE
- BUILD_RESULT
- TEST_RESULT
- REVIEW_RESULT
- VERIFICATION_RESULT
- DELIVERY_RESULT
- ERROR
- FIX
- LESSON
- CONFIGURATION
- LIMITATION
- SECURITY_EVENT
- ACCESSIBILITY_EVENT

---

## 10. Memory Record Structure

A memory record should contain, when applicable:

- Memory ID
- Project ID
- Memory type
- Importance
- Date
- Time
- Time zone
- Source
- Actor
- Summary
- Details
- Related requirement ID
- Related plan ID
- Related review ID
- Related verification ID
- Related delivery ID
- Related file
- Previous record
- Next record
- Confidence
- Privacy classification

---

## 11. Evidence-Based Memory

Important memory should retain a connection to its source.

Possible sources include:

- User instruction
- Approved plan
- Generated file
- Git commit
- Build result
- Test result
- Review report
- Verification report
- Delivery report

The agent should prefer evidence-backed memory over unsupported assumptions.

---

## 12. No Invented Memory

The agent must never invent:

- Past actions
- Past decisions
- Dates
- Times
- File changes
- Test results
- User approvals
- Project history

If a historical fact cannot be found, the agent should say that it could not verify it.

---

## 13. Memory Confidence

Memory records should support confidence levels such as:

- VERIFIED
- HIGH_CONFIDENCE
- MEDIUM_CONFIDENCE
- LOW_CONFIDENCE
- UNVERIFIED

Confidence must reflect evidence quality.

---

## 14. User Approval Memory

Important user approvals should be recorded.

Examples:

- Approval of a technical plan
- Approval of a feature
- Approval of a major change
- Approval of an external action
- Approval of a paid service
- Approval of public publication

The record should identify what was approved and when.

---

## 15. Action History

Important agent actions should be recorded.

Examples:

- Created file
- Modified file
- Deleted file
- Ran build
- Ran test
- Performed review
- Performed verification
- Created artifact
- Delivered artifact
- Encountered error
- Applied fix

Each important action should have a timestamp.

---

## 16. File History

For important project files, memory should be able to associate:

- File path
- File purpose
- Creation event
- Modification events
- Deletion event
- Relevant commit
- Related requirement
- Related project version

This enables historical questions about files.

---

## 17. Decision History

Important technical decisions should record:

- Decision ID
- Date
- Problem
- Options considered
- Decision
- Reason
- Evidence
- User approval when required
- Affected project
- Affected files

This prevents the agent from repeatedly reconsidering settled decisions without reason.

---

## 18. Requirement History

Requirements should preserve:

- Requirement ID
- Original requirement
- Clarifications
- Approval status
- Changes
- Date of change
- Reason for change
- Related implementation
- Verification result

Confirmed requirements must not be silently overwritten.

---

## 19. Project Version History

Important project versions should record:

- Project ID
- Version
- Commit
- Date
- Major changes
- Build result
- Verification result
- Delivery status

---

## 20. Error History

Important errors should be remembered.

Each error record should include:

- Error ID
- Date
- Project
- Error description
- Affected component
- Cause when known
- Fix
- Verification result
- Whether the issue can recur

This allows the agent to avoid repeating known mistakes.

---

## 21. Lesson Memory

Lessons should be created from validated experience rather than every temporary failure.

A lesson should contain:

- Lesson ID
- Problem
- Cause
- Solution
- Evidence
- Applicable conditions
- Date learned
- Project scope
- Confidence

Lessons must not be treated as universal if they apply only to one project or environment.

---

## 22. Learning Safety

The agent must not automatically convert arbitrary external information into trusted permanent knowledge.

New knowledge should be evaluated before becoming a high-confidence lesson.

Potentially unreliable information should remain marked as uncertain until verified.

---

## 23. External Information

The agent may use external information to improve its work when authorized and available.

However:

- External information must not automatically become permanent trusted memory.
- Sources should be recorded when practical.
- Conflicting information should be identified.
- Important technical claims should be verified when practical.

---

## 24. Memory Search

The system should support searching by:

- Date
- Date range
- Project
- Memory type
- Requirement ID
- File path
- Error ID
- Decision ID
- Keyword
- Event
- Version

The goal is reliable historical retrieval rather than approximate recollection.

---

## 25. Natural-Language Recall

The agent should understand historical questions written in:

- Bangla
- Banglish
- English
- Mixed language

Examples:

"এক বছর আগে এই project-এ কী করেছিলে?"

"গত মাসে কোন ফাইল পরিবর্তন করেছিলে?"

"এই সিদ্ধান্তটা কেন নিয়েছিলে?"

The system should translate the question into a structured memory search.

---

## 26. Date-Range Recall

For questions such as:

- Yesterday
- Last week
- Last month
- One year ago
- Between two dates

the system should resolve the date range using the correct time zone.

If the date range cannot be determined reliably, the agent must ask for clarification.

---

## 27. Memory Ranking

When multiple records match a query, results should be ranked using:

- Exact project match
- Exact date match
- Requirement relationship
- Evidence quality
- Confidence
- Importance
- Recency when relevant

The agent should prefer verified evidence over weak matches.

---

## 28. Memory Deduplication

The system should avoid unnecessary duplicate records.

If the same event is recorded more than once, it should be possible to identify the duplicates and preserve the strongest evidence.

Important historical information must not be lost during deduplication.

---

## 29. Memory Updates

Memory should normally be append-oriented for historical events.

Historical records should not be silently rewritten.

If a previous record was incorrect:

1. Preserve the original record.
2. Mark it as corrected.
3. Create a correction record.
4. Explain the reason for correction.
5. Link the records.

---

## 30. Memory Deletion

Historical memory must not be silently deleted.

If deletion is required by an authorized policy:

- Record the deletion event when appropriate.
- Identify the affected record.
- Preserve a minimal audit reference when legally and technically appropriate.

Sensitive information should be handled according to the applicable privacy policy.

---

## 31. Privacy Classification

Memory records should support privacy classifications such as:

- PUBLIC
- PROJECT_PRIVATE
- CLIENT_PRIVATE
- USER_PRIVATE
- SECURITY_SENSITIVE

The system must enforce appropriate access controls.

---

## 32. Sensitive Information

The memory system must avoid unnecessary storage of sensitive information.

It must not store:

- Passwords
- Private keys
- Authentication tokens
- API secrets
- Payment credentials

unless a specific secure mechanism explicitly requires temporary handling.

Secrets must never become ordinary searchable memory.

---

## 33. Information Minimization

The agent should remember enough information to perform its duties reliably without unnecessarily storing excessive personal or private information.

Memory quality is not measured by storing everything.

Useful, relevant, and authorized information should be prioritized.

---

## 34. No Cross-User Leakage

Memory belonging to one user or project must never be exposed to another unauthorized user or project.

Cross-project and cross-client leakage must be treated as a serious security issue.

---

## 35. Memory Encryption

Where supported by the storage system, sensitive memory should be protected using appropriate encryption at rest and in transit.

Encryption keys must not be stored as ordinary memory records.

---

## 36. Memory Integrity

The system should protect important memory records against accidental corruption.

Important records should have integrity information such as:

- Record hash
- Version
- Timestamp
- Source reference

when practical.

---

## 37. Memory Backup

Important memory should be backed up according to the backup policy.

Backups should preserve:

- Record identity
- Project association
- Timestamps
- Relationships
- Integrity information

Backups must also respect privacy and security requirements.

---

## 38. Memory Recovery

If the primary memory store becomes unavailable, the system should be able to recover from an available valid backup when supported.

Recovery should preserve historical ordering and record identity.

---

## 39. Memory Availability

The agent should distinguish between:

- Memory available
- Memory partially available
- Memory unavailable
- Memory corrupted
- Memory recovery required

It must not pretend to remember information when the memory source is unavailable.

---

## 40. One-Year and Long-Term Recall

The system should be designed so that historical records remain searchable for at least one year and preferably for the useful lifetime of the project, subject to storage and privacy policies.

A record must not expire merely because it is old unless an explicit retention policy requires it.

---

## 41. Audit Relationship

Memory and audit records should be connected.

The audit system records what happened.

Memory provides structured information that helps the agent understand and retrieve important historical context.

Neither should silently replace the other.

---

## 42. Learning Relationship

Validated lessons may be derived from audit and project history.

The process should be:

HISTORY
→ ANALYSIS
→ VALIDATION
→ LESSON
→ APPROVED KNOWLEDGE

The agent must not treat every historical event as a lesson.

---

## 43. Knowledge Relationship

Stable technical knowledge should be stored separately from project history.

Project experience may inform general knowledge only after appropriate validation and sanitization.

Private project information must not become public or global knowledge.

---

## 44. Memory and User Trust

The agent should be transparent about memory.

When asked what it remembers, it should provide relevant information without unnecessarily exposing unrelated private records.

It should distinguish:

- What is remembered
- What is verified
- What is uncertain
- What is unavailable

---

## 45. Memory Failure Handling

If a memory write fails:

1. Detect the failure.
2. Record the failure when possible.
3. Do not claim the information was permanently saved.
4. Retry safely when appropriate.
5. Report the limitation when important.

---

## 46. Memory Consistency

Related records should maintain consistent identifiers.

For example:

PROJECT
→ REQUIREMENT
→ PLAN
→ FILE CHANGE
→ REVIEW
→ VERIFICATION
→ DELIVERY

Historical links should remain intact.

---

## 47. Auditability

Important memory operations should be traceable:

- Memory created
- Memory updated
- Memory corrected
- Memory deleted
- Memory restored
- Memory searched when security policy requires logging

---

## 48. Memory Access Control

Only authorized components should be able to:

- Read memory
- Write memory
- Modify memory
- Delete memory
- Restore memory
- Export memory

Permissions should follow least privilege.

---

## 49. Export and Migration

The system should support safe migration or export of memory when the underlying infrastructure changes.

Migration should preserve:

- IDs
- Timestamps
- Relationships
- Project associations
- Evidence references
- Confidence
- Privacy classifications

This is important if the system later moves away from GitHub or another storage provider.

---

## 50. Provider Independence

Long-term memory must not be designed so that the entire system becomes permanently dependent on one provider.

The memory model should be portable where practical.

This allows migration to another storage system if:

- GitHub limits change
- Storage requirements increase
- Project popularity grows
- A different server becomes necessary
- Another database becomes more suitable

---

## 51. Storage Scaling

The system should support future migration from simple repository-based storage to a more scalable database or storage service.

The logical memory model should remain stable even if the physical storage backend changes.

---

## 52. Cost Protection

Memory storage should respect the user's cost requirements.

The system must not automatically create paid storage or infrastructure.

If the current free storage becomes insufficient, the agent should identify the limitation and present migration options rather than silently activating paid services.

---

## 53. Backup Provider Independence

Backups should not depend exclusively on the same storage location as the primary memory when practical.

A future backup strategy may use a separate authorized storage provider.

Any such provider must follow the project's privacy and security requirements.

---

## 54. Memory Health

The system should periodically be able to evaluate:

- Storage availability
- Backup status
- Integrity
- Searchability
- Corruption
- Missing records
- Failed writes
- Migration status

Memory health problems should be reported.

---

## 55. Memory Quality Gate

Before important memory is considered reliable, verify:

- Correct project association.
- Correct timestamp.
- Source or evidence identified.
- Appropriate confidence.
- Appropriate privacy classification.
- No secrets stored unnecessarily.
- Historical relationships preserved.
- No unsupported facts invented.

---

## 56. Historical Answer Quality Gate

Before answering an important historical question, the agent should:

1. Search relevant memory.
2. Prefer exact project matches.
3. Prefer evidence-backed records.
4. Check dates.
5. Check related records.
6. Identify uncertainty.
7. Answer only what the evidence supports.

---

## 57. Final Rule

The Memory System exists so that AIAppBuilder can remember important history reliably without pretending to remember information it does not have.

Its fundamental process is:

CAPTURE
→ TIMESTAMP
→ CLASSIFY
→ STORE
→ PROTECT
→ INDEX
→ SEARCH
→ VERIFY
→ RECALL

The agent must be able to say "I don't have verified information about that" rather than inventing a memory.
