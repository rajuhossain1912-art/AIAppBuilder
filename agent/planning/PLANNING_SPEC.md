# AIAppBuilder Planning Engine Specification

## 1. Purpose

The Planning Engine converts confirmed and structured requirements into a practical, technically justified, testable software development plan.

It must determine how the requested application should be built without silently changing confirmed requirements.

The Planning Engine must work under the security, privacy, accessibility, compatibility, and approval rules defined by AIAppBuilder.

---

## 2. Input

The Planning Engine receives:

- Confirmed requirements
- Original user request
- Requirement identifiers
- User approvals
- Project constraints
- Existing project information
- Existing architecture
- Existing source code information
- Research findings
- Security requirements
- Accessibility requirements
- Compatibility requirements
- Budget and resource constraints
- Delivery requirements

The Planning Engine must not treat unconfirmed assumptions as confirmed requirements.

---

## 3. Planning Principles

The Planning Engine must:

- Preserve confirmed user requirements.
- Prefer simple and maintainable solutions.
- Minimize unnecessary dependencies.
- Minimize unnecessary permissions.
- Consider security from the beginning.
- Consider accessibility from the beginning.
- Consider compatibility from the beginning.
- Consider resource usage.
- Prefer free solutions when the user requires a free solution.
- Identify technical limitations honestly.
- Avoid unnecessary architectural complexity.
- Protect existing working functionality in existing projects.

---

## 4. Planning Lifecycle

The standard planning flow is:

REQUIREMENTS_RECEIVED
→ REQUIREMENTS_VALIDATED
→ EXISTING_PROJECT_ANALYZED
→ TECHNICAL_OPTIONS_IDENTIFIED
→ RESEARCH_REQUIREMENTS_IDENTIFIED
→ ARCHITECTURE_SELECTED
→ COMPONENTS_DEFINED
→ DATA_FLOW_DEFINED
→ FILE_PLAN_DEFINED
→ IMPLEMENTATION_PLAN_DEFINED
→ TEST_PLAN_DEFINED
→ SECURITY_PLAN_DEFINED
→ ACCESSIBILITY_PLAN_DEFINED
→ BUILD_PLAN_DEFINED
→ DELIVERY_PLAN_DEFINED
→ PLAN_READY

If important information is missing, the plan may enter:

REQUIRES_CLARIFICATION

If required technical information is uncertain:

REQUIRES_RESEARCH

---

## 5. Existing Project Analysis

Before planning changes to an existing project, the Planning Engine should determine:

- Existing architecture
- Existing modules
- Existing source files
- Existing dependencies
- Existing build configuration
- Existing working features
- Existing tests
- Existing accessibility implementation
- Existing security controls
- Existing known problems

The plan must avoid replacing working components unnecessarily.

---

## 6. Architecture Selection

The Planning Engine must select an architecture appropriate to the application.

Possible approaches include:

- Simple single-module architecture
- Layered architecture
- MVVM
- Clean Architecture
- Modular architecture
- Other appropriate architecture

The engine must not select a complex architecture merely because it is considered advanced.

The selected architecture must be justified by project requirements.

---

## 7. Technology Selection

For each important technology choice, the plan should consider:

- Requirement fit
- Android compatibility
- Accessibility
- Security
- Performance
- Maintainability
- Dependency size
- License
- Availability
- Cost
- Offline capability
- Online requirements
- Long-term viability

If multiple technologies can satisfy the requirement, the engine should prefer the option that provides the best practical balance.

---

## 8. Offline, Online, and Hybrid Planning

The plan must explicitly define whether the application is:

- Offline
- Online
- Hybrid

For online applications, identify:

- Required APIs
- Network operations
- Authentication
- Data synchronization
- Error handling
- Offline fallback when applicable

For offline applications, identify:

- Local storage
- Local processing
- Device resource requirements
- Model or data size
- Backup considerations

For hybrid applications, clearly separate offline and online responsibilities.

---

## 9. Component Planning

The plan should identify the major components required.

Possible components include:

- User interface
- Navigation
- View models
- Domain logic
- Data layer
- Local database
- Network layer
- API client
- Authentication
- Media processing
- File handling
- Accessibility layer
- Settings
- Logging
- Error handling
- Security components
- Testing components

Only necessary components should be included.

---

## 10. Data Flow

The Planning Engine should define how information moves through the application.

For example:

User Input
→ Validation
→ Business Logic
→ Local or Remote Data Layer
→ Processing
→ Result
→ Accessible UI

For sensitive data, the plan must identify:

- Where it originates
- Where it is processed
- Where it is stored
- Where it is transmitted
- When it is deleted

---

## 11. File Plan

Before implementation, the Planning Engine should produce a file plan.

The plan should identify:

- File path
- File purpose
- Component
- Dependencies
- Whether the file is new or existing
- Whether the file will be created or modified

File placement must follow:

`PROJECT_STRUCTURE.md`

The engine must not create duplicate files when an appropriate existing file already exists.

---

## 12. Implementation Order

The plan should divide implementation into logical phases.

A typical order is:

1. Project foundation
2. Build configuration
3. Core models
4. Data layer
5. Business logic
6. UI
7. Accessibility
8. Integrations
9. Error handling
10. Security hardening
11. Testing
12. Build
13. Verification
14. Delivery

The order may change when project requirements justify a different sequence.

---

## 13. Dependency Planning

Every new dependency should have a reason.

The plan should record:

- Dependency name
- Purpose
- Version requirement when known
- License considerations
- Security considerations
- Compatibility considerations
- Alternative if available

Unnecessary dependencies should be avoided.

---

## 14. Android Compatibility Planning

For Android applications, the plan should define:

- Minimum supported Android version
- Target Android version
- Compile SDK requirement
- Supported CPU architectures when relevant
- Screen-size considerations
- Storage behavior
- Permission behavior
- Background behavior
- Compatibility risks

The plan should prioritize broad compatibility when technically practical.

---

## 15. Accessibility Planning

Accessibility must be planned as part of the core application.

The plan should consider:

- TalkBack
- Semantic labels
- Focus order
- Focus stability
- Accessible buttons
- Accessible text fields
- Accessible dialogs
- State announcements
- Error announcements
- Loading announcements
- Touch target size
- Contrast
- Text scaling
- Non-color-only information

Accessibility acceptance criteria must be connected to the test plan.

---

## 16. Security Planning

Security must be included before implementation.

The plan should address:

- Secrets
- Permissions
- Authentication
- Authorization
- Secure storage
- Network security
- Input validation
- File access
- Exported components
- WebView security
- Dependency risks
- Logging safety

The plan must follow:

`config/policy/SECURITY_POLICY.md`

---

## 17. Privacy Planning

The plan should define:

- Data collected
- Purpose of collection
- Storage location
- Retention period when applicable
- External transmission
- Third-party services
- Data deletion
- User control

Data that is not required should not be collected.

---

## 18. Performance Planning

The plan should identify important resource constraints.

Consider:

- CPU usage
- RAM usage
- Storage usage
- Battery usage
- Startup time
- Network usage
- Large input handling
- Background work

For low-resource devices, the plan should prefer resource-efficient approaches.

---

## 19. Error Handling Plan

The plan should define expected failure conditions.

Examples:

- Invalid user input
- Network unavailable
- API failure
- Permission denied
- Storage unavailable
- Insufficient device resources
- Authentication failure
- Dependency failure
- Build failure

Each important failure should have a predictable and understandable response.

---

## 20. Testing Plan

The Planning Engine must create a testing strategy appropriate to the application.

Possible test levels:

- Unit tests
- Integration tests
- UI tests
- Accessibility tests
- Security checks
- Compatibility checks
- Performance checks
- Build verification
- Manual verification

Tests should map back to requirements.

---

## 21. Requirement Traceability

The plan must preserve requirement identifiers.

Example:

REQ-001
→ PLAN-001
→ FILES
→ TEST-001
→ VERIFICATION-001

This allows the system to determine whether every important requirement was actually implemented and verified.

---

## 22. Risk Register

Important risks should be recorded.

Each risk should contain:

- Risk ID
- Description
- Probability
- Impact
- Mitigation
- Verification method

Examples:

- API unavailable
- Dependency abandoned
- Android compatibility problem
- Accessibility regression
- Resource exhaustion
- Free quota exhaustion
- Security vulnerability
- Licensing problem

---

## 23. Free-First Strategy

When the user requires a no-cost solution, the Planning Engine should prioritize:

1. Built-in platform capabilities
2. Open-source solutions with compatible licenses
3. Free services with verified limits
4. Existing project capabilities
5. Paid services only when explicitly approved

The engine must not silently introduce paid infrastructure.

---

## 24. Provider Independence

When an external service is required, the plan should avoid unnecessary lock-in.

Where practical, define an abstraction that allows the provider to be replaced later.

For example:

Application
→ Provider Interface
→ Provider A

and potentially:

Application
→ Provider Interface
→ Provider B

This is especially important when free quotas or provider availability may change.

---

## 25. Build Planning

The plan should define:

- Build system
- Java/Kotlin version when applicable
- Gradle requirements
- Build variants
- Required configuration
- Artifact location
- Build verification
- Error reporting

The plan must not assume that a build succeeded until actual build evidence exists.

---

## 26. Delivery Planning

The plan should define the expected deliverables.

Possible deliverables:

- Source code
- Debug APK
- Release APK
- Documentation
- Configuration instructions
- Test report
- Verification report

Only artifacts that are actually produced may be marked as delivered.

---

## 27. Change Impact Analysis

When a confirmed requirement changes, the Planning Engine should determine:

- Affected architecture
- Affected files
- Affected dependencies
- Affected tests
- Affected accessibility behavior
- Affected security behavior
- Affected delivery artifacts

The engine should minimize unnecessary changes.

---

## 28. Rollback Planning

For significant changes, the plan should identify a safe recovery point when practical.

A rollback strategy should consider:

- Previous working state
- Changed files
- Build artifact
- Database or data migration
- Configuration changes

---

## 29. Plan Quality Gate

Before passing the plan to the Generation Engine, verify:

- Requirements preserved
- Existing project analyzed when applicable
- Architecture justified
- Technology choices justified
- File locations identified
- Dependencies reviewed
- Accessibility planned
- Security planned
- Privacy planned
- Compatibility planned
- Performance considered
- Testing planned
- Risks identified
- Delivery defined
- Requirement traceability established

If a critical item cannot be determined, the plan must identify it instead of pretending it is resolved.

---

## 30. No Silent Requirement Changes

The Planning Engine must never:

- Remove a MUST_HAVE requirement silently.
- Change a confirmed requirement without recording it.
- Turn a suggestion into a requirement.
- Hide a technical limitation.
- Claim an unavailable capability is available.

Conflicts must be reported and resolved through the appropriate approval process.

---

## 31. Handoff to Generation Engine

The final planning package should contain:

- Confirmed requirements
- Architecture
- Technology choices
- Component plan
- Data flow
- File plan
- Implementation order
- Dependencies
- Security plan
- Accessibility plan
- Privacy plan
- Compatibility plan
- Performance plan
- Error handling plan
- Testing plan
- Risk register
- Build plan
- Delivery plan
- Traceability map
- Required approvals
- Open issues

The Generation Engine must use this package as its implementation boundary.

---

## 32. Final Rule

The Planning Engine exists to answer:

"How can the confirmed user requirements be implemented correctly, safely, accessibly, maintainably, and verifiably?"

Its fundamental process is:

REQUIREMENTS
→ ANALYZE
→ RESEARCH
→ ARCHITECT
→ PLAN
→ TRACE
→ TEST
→ VERIFY
→ HAND OFF

A plan is not complete merely because it describes how to write code. It is complete when it provides a reliable path from confirmed requirements to a tested and verifiable software result.
