# AIAppBuilder Architecture Specification

## 1. Vision

AIAppBuilder is a private, cloud-first AI software development agent designed to transform natural-language app ideas into safe, usable, accessible Android applications.

The system should support Bangla, Banglish, English, mixed-language, informal, incomplete, and imperfect user requirements.

The core development principle is:

Understand → Plan → Research → Generate → Review → Build → Test → Fix → Verify → Deliver

The system must prioritize correctness, accessibility, security, privacy, reliability, maintainability, resource efficiency, and honest reporting.

---

## 2. Operating Model

AIAppBuilder should operate as an end-to-end development agent rather than only a code generator.

A project may progress through:

1. Requirement understanding
2. Requirement cleaning and restatement
3. User confirmation when necessary
4. Technical planning
5. Research
6. Architecture decisions
7. Project generation
8. Code review
9. Build
10. Testing
11. Error analysis
12. Fixing
13. Rebuilding
14. Verification
15. Artifact generation
16. Delivery
17. Learning and documentation

The agent must never claim that an application is complete merely because source code was generated.

---

## 3. Major Components

### 3.1 User Interaction Layer

The interaction layer must accept:

- Bangla
- Banglish
- English
- Mixed Bangla-English
- Informal language
- Incomplete requirements
- Ill-formed requirements
- Voice-derived or imperfect text

The system should clean and restate unclear requirements in understandable Bangla.

If a requirement is materially ambiguous, the agent must ask for confirmation before substantial implementation.

The user should be able to specify:

- App language
- Implementation technology
- UI preferences
- Accessibility requirements
- Offline/online behavior
- Required features
- Optional features

If the user does not specify implementation technology, the agent may recommend an appropriate technology and explain the reason.

---

### 3.2 Agent Orchestrator

The Agent Orchestrator controls the complete development lifecycle.

It should:

- Maintain project state
- Coordinate all agents/modules
- Enforce safety policies
- Track approvals
- Manage retries
- Detect failures
- Trigger research when needed
- Trigger builds and tests
- Prevent unauthorized actions
- Maintain audit history

The orchestrator must be state-aware and recoverable.

---

### 3.3 Requirements and Planning Engine

This component converts natural-language requirements into structured specifications.

It should identify:

- Functional requirements
- Non-functional requirements
- Accessibility requirements
- Security requirements
- Privacy requirements
- Compatibility requirements
- UI/UX requirements
- Performance requirements
- Resource constraints
- Build and delivery requirements

The planning engine should explain major technical decisions.

---

### 3.4 Research Engine

The research engine should investigate public and authorized information when technical knowledge is insufficient or potentially outdated.

Research should prioritize:

1. Official documentation
2. Primary sources
3. Reliable technical sources
4. Multiple-source comparison when appropriate

The agent must not blindly trust a single source.

Research results should be recorded with:

- Source
- Date
- Relevant finding
- Decision influenced by the finding
- Confidence or uncertainty where appropriate

---

### 3.5 Knowledge Base

The knowledge base should store verified and reusable technical knowledge.

Suggested structure:

knowledge/
├── android/
├── accessibility/
├── kotlin/
├── compose/
├── testing/
├── security/
├── lessons-learned/
└── project-patterns/

Suggested reusable templates:

- Basic Android App
- Offline App
- Online API App
- Hybrid App
- TTS App
- Media App
- Accessibility-first App
- Database App

Only verified lessons should become reusable knowledge.

---

### 3.6 Project Memory and Project Passport

Every project should have a durable Project Passport.

The Project Passport should track:

- Project name
- Project purpose
- User requirements
- Cleaned requirements
- User approvals
- Architecture decisions
- Reasons for major decisions
- Research findings
- Files created
- Files modified
- Builds
- Tests
- Errors
- Fixes
- APKs/artifacts
- Releases
- Rollbacks
- User feedback
- Known problems
- Important decisions
- Versions
- Current project state
- Last successful build

The system must not rely exclusively on model conversation context.

Important history should be stored durably.

Important memory should not be deleted without appropriate user approval.

---

## 4. Activity and Audit Log

The system should maintain an activity/audit log containing important events.

Each important event should include, when available:

- Timestamp
- Project
- Action
- Actor/component
- Input or reason
- Result
- Files affected
- Build/test status
- Error information
- Approval information

The audit system must help reconstruct what happened during development.

---

## 5. Code Generation and Project Engine

The Project Engine should create and maintain complete Android projects.

It should support appropriate technologies such as Kotlin and Jetpack Compose where suitable.

The engine must:

- Follow project architecture
- Preserve working functionality
- Avoid unnecessary changes
- Maintain consistent coding standards
- Keep configuration reproducible
- Avoid hard-coded secrets
- Generate maintainable code
- Respect Android compatibility requirements

Generated code should be reviewed before build execution.

---

## 6. UI/UX and Accessibility Engine

Accessibility is a core engineering requirement, not an optional feature.

Every generated application should consider:

- TalkBack compatibility
- Meaningful accessibility labels
- Correct content descriptions where appropriate
- Logical focus order
- Keyboard/focus accessibility where relevant
- Readable text
- Sufficient touch target sizes
- Status and error discoverability
- No color-only communication
- No position-only communication
- No animation-only communication
- Accessible custom controls
- Predictable focus behavior
- No unexpected focus changes

Accessibility defects must be treated as real defects.

UI/UX should be:

- Modern
- Simple
- Usable
- Consistent
- Appropriate for the application

Each application should have an independently designed visual system.

The agent must not intentionally clone another application's distinctive copyrighted or trademarked design.

---

## 7. Android Compatibility

Generated Android applications should target broad compatibility.

The preferred compatibility goal is:

Android 10 through current and future Android versions as technically possible.

The agent should avoid unnecessary device-specific behavior.

Compatibility problems discovered during testing should be recorded and fixed where technically possible.

---

## 8. Device Resource Protection

Generated applications should avoid unnecessary:

- CPU usage
- RAM usage
- Battery consumption
- Storage usage
- Network usage
- Thermal load

The system should prefer efficient implementations.

When practical, resource usage should be reviewed during verification.

---

## 9. Security Architecture

Security requirements include:

- No hard-coded secrets
- Secure credential handling
- Minimum necessary permissions
- Secure storage where appropriate
- Secure network communication
- Input validation
- Dependency review
- Security review before delivery
- Protection against unauthorized access

The system must not create:

- Malware
- Credential theft tools
- Spyware
- Unauthorized surveillance
- Fraud systems
- Unauthorized access mechanisms
- Other intentionally harmful software

Security policies must not be secretly weakened by the agent.

---

## 10. Privacy Architecture

User and project data must remain isolated.

The system must not:

- Share one user's project data with another user
- Leak secrets between projects
- Secretly export project data
- Put sensitive information into external prompts unnecessarily

Data should be classified where appropriate:

- Public
- Internal
- Confidential
- Highly Sensitive

The architecture should support:

- Data minimization
- Project isolation
- Encryption where appropriate
- Audit logging
- Export controls
- Deletion controls

No absolute zero-loss guarantee should be claimed.

Instead, the system should provide durable history, backups, recovery points, and migration support where practical.

---

## 11. Safety and Permission Model

AIAppBuilder should provide maximum useful autonomy within strict safety boundaries.

Routine low-risk actions may proceed automatically after appropriate project/session approval.

Explicit user approval is required before:

- Spending money
- Enabling paid services
- Adding payment methods
- Creating billing accounts
- Subscribing to paid services
- Using external/private data not clearly authorized
- Creating external accounts
- Granting external permissions
- Destructive deletion
- Public or production deployment
- Using credentials for external systems when authorization is not already established

The agent must never expand its own privileges.

---

## 12. Provider-Agnostic Architecture

AIAppBuilder should not depend permanently on a single provider.

Provider abstractions should exist for:

- AI model provider
- Git provider
- Build provider
- Storage provider
- Research provider

Potential providers may include GitHub, GitLab, Cloudflare, Firebase, Supabase, or other suitable services.

The system must never silently switch to a paid provider.

If a free quota is exhausted and no approved free alternative exists, the agent must stop and inform the user.

The agent must never claim unlimited free usage unless that is actually verified.

---

## 13. Quota and Resource Manager

The Resource and Quota Manager should monitor, where APIs allow:

- AI usage
- Build usage
- GitHub Actions usage
- Storage usage
- Provider quotas
- API availability
- Service limits

Before actions that may consume significant resources, the system should determine whether the operation is allowed.

No unauthorized spending is permitted.

---

## 14. End-to-End State Machine

The project lifecycle should use explicit states:

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

Failure states should preserve diagnostic information.

State transitions should be recorded in the audit history.

---

## 15. Build Engine

The Build Engine should:

- Build the generated project
- Capture real build logs
- Detect compilation failures
- Detect dependency problems
- Detect configuration errors
- Produce APK/AAB artifacts when possible
- Report exact failures

The agent must not claim a successful build without actual build evidence.

---

## 16. Test and Verification Engine

Verification should occur at multiple levels where practical:

- Source review
- Compilation
- Unit tests
- Integration tests
- UI tests
- Accessibility checks
- Compatibility checks
- Security checks
- Resource review
- Artifact verification

The final delivery decision should be based on evidence.

---

## 17. Build → Test → Fix Loop

When a build or test fails:

1. Capture the real error
2. Analyze the error
3. Research if necessary
4. Identify the likely root cause
5. Apply a minimal appropriate fix
6. Rebuild
7. Retest
8. Verify that existing working features were not unnecessarily broken

Retries must be bounded.

A practical initial retry limit may be approximately 5–10 attempts depending on the task.

Repeated failure should stop the loop and report the actual problem.

---

## 18. Failure Recovery

The system should create restore points before significant risky changes where practical.

If a change causes regression:

- Identify the affected change
- Preserve diagnostic information
- Roll back when appropriate
- Restore the last known-good state
- Re-plan the fix

The system should prefer safe incremental changes over large uncontrolled modifications.

---

## 19. Delivery

A completed project should provide, where technically possible:

- Source code
- Build result
- APK or other requested artifact
- Version information
- Build/test verification status
- Known limitations
- Important usage information

The agent must clearly distinguish:

- Generated
- Built
- Tested
- Verified
- Delivered

These states must not be falsely represented as equivalent.

---

## 20. Learning Loop

The learning process should follow:

Idea
→ Plan
→ Build
→ Test
→ Error
→ Research
→ Fix
→ Test
→ Success
→ Extract Lesson
→ Verify
→ Knowledge Base

Only verified lessons should be promoted into reusable knowledge.

Project-specific information must not automatically become global knowledge if it could expose private information.

---

## 21. Originality and Licensing

The agent should prefer:

- Original implementation
- Properly licensed dependencies
- Publicly documented APIs
- Attribution where required

The agent must not intentionally reproduce proprietary code without authorization.

Third-party licenses must be respected.

---

## 22. Implementation Order

The initial implementation should proceed in controlled stages:

1. Architecture and repository structure
2. Secure configuration and policy layer
3. Agent state and orchestration
4. Project Passport and audit/memory system
5. Provider abstraction and quota protection
6. AI interaction layer
7. Research engine
8. Android project generation
9. Cloud build integration
10. Test/fix/verification system
11. APK/artifact delivery
12. End-to-end testing and hardening

Each major stage should be verified before moving to the next stage.

---

## 23. Development Principles

AIAppBuilder must follow these principles:

- Safety before speed
- Evidence before claims
- Verification before delivery
- Accessibility from the beginning
- Security by design
- Privacy by design
- Minimal necessary permissions
- Preserve working functionality
- Avoid unnecessary resource consumption
- No unauthorized spending
- No hidden actions
- No hidden privilege escalation
- No deliberate deception
- No cross-project data leakage
- Durable project history
- Recoverable development
- Provider independence
- User control over important decisions

---

## 24. Current Architectural Goal

The first implementation goal is not to build every feature immediately.

The first goal is to establish a reliable foundation capable of:

1. Understanding requirements
2. Maintaining project memory
3. Planning work
4. Safely generating Android projects
5. Building them
6. Testing them
7. Fixing real errors
8. Verifying results
9. Delivering usable artifacts
10. Learning only from verified outcomes

The architecture should remain modular so that capabilities can be added without unnecessarily rewriting working components.
