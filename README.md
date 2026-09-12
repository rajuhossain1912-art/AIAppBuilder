# AIAppBuilder

A private AI-powered application development agent for creating safe, usable, and accessible Android applications from natural-language ideas and requirements.

## Purpose

AIAppBuilder is a personal development agent. It is intended for use by its owner to develop Android applications for personal projects and client work.

The intended client workflow is:

**Client request → requirement interview → structured specification → owner approval → architecture → source generation → build → test → fix → verify → APK delivery**

The agent must ask for missing information instead of inventing important requirements. It must not claim an app is complete merely because source code was generated.

## Client Order Intake

A client may describe an app in Bangla, Banglish, English, mixed language, or informal wording. The agent should:

1. Preserve the original request.
2. Normalize and structure the request.
3. Identify missing or ambiguous requirements.
4. Ask only the follow-up questions needed to make the specification actionable.
5. Collect app name, purpose, target users, essential features, online/offline needs, integrations, content/assets, authentication, data requirements, notifications, language, Android compatibility, accessibility needs, and other constraints when applicable.
6. Produce a clear client-order brief.
7. Show the understood specification and obtain owner approval before consequential generation.

For services such as YouTube or Facebook channel/page apps, the agent should request the relevant public channel/page links or identifiers, requested features, client-owned branding/content, and any approved API or integration requirements. It must not invent private endpoints or copy another product's proprietary implementation or design.

## Technology Stack

The development agent is primarily implemented in **Python**.

Generated Android applications currently use **Java** for the Android application source and **Gradle** for the Android build system.

The Android build baseline currently uses:

- Android Gradle Plugin (AGP) 8.7.3
- Gradle 8.9 in CI
- Java 17 for the Android build environment
- compileSdk 35
- targetSdk 35 by default
- configurable minSdk, with the current template supporting Android API 21+

GitHub is used as the source-control and cloud-CI environment for this private development project. GitHub Actions performs automated Python checks and cloud Android builds. The agent is designed to prefer dependency-light, stable Android APIs and to avoid paid infrastructure where technically possible.

This technology description is about the current AIAppBuilder implementation. Individual client applications may use additional Android libraries or services when their approved requirements genuinely need them.

## Core Workflow

1. Understand the user's application idea.
2. Extract functional and non-functional requirements.
3. Identify missing or ambiguous requirements.
4. Create an application plan and architecture.
5. Generate the Android project and source code.
6. Review the generated code.
7. Build the application.
8. Analyze build errors and attempt safe fixes based on actual error output.
9. Repeat build and verification when necessary.
10. Perform accessibility and functional checks.
11. Produce the final APK when the project successfully builds.
12. Clearly report any limitation that prevents completion.

## Accessibility Requirements

Accessibility is a core requirement of every generated application.

Generated applications should, whenever technically applicable:

- Support Android accessibility services and TalkBack.
- Provide meaningful accessible names for interactive controls.
- Provide useful content descriptions where appropriate.
- Maintain logical accessibility and focus order.
- Avoid inaccessible custom controls.
- Ensure important status and error messages can be discovered by screen readers.
- Avoid relying only on color, position, animation, or visual appearance to communicate information.
- Provide sufficiently large and usable touch targets.
- Keep text readable and controls understandable.
- Avoid unexpected focus changes.
- Test important workflows with accessibility considerations in mind.

The agent must treat accessibility problems as defects rather than optional improvements.

## Android Compatibility

Generated applications should prioritize broad Android compatibility.

The agent should avoid unnecessary device-specific or Android-version-specific behavior and should choose stable Android APIs whenever possible.

Compatibility decisions must be documented when a requested feature requires a particular Android version or device capability.

## Safety

The agent is intended to create legitimate software.

It must not intentionally create applications designed to:

- Harm people.
- Steal credentials or personal information.
- Install malware.
- Spy on users without proper authorization.
- Obtain unauthorized access to systems or accounts.
- Commit fraud or other illegal activity.

When a request clearly requires harmful or unauthorized functionality, the agent should refuse that part and explain the limitation.

## Privacy and Secrets

API keys, passwords, access tokens, private credentials, and other secrets must never be hard-coded into source files or committed to the repository.

Secrets must be handled through appropriate secure configuration mechanisms.

Client information should be retained only as necessary for the development workflow and should not be unnecessarily exposed in generated output.

## Reliability

The agent must not claim that an application is complete merely because source code was generated.

An application should be considered successfully completed only after the available build and verification process succeeds.

When a build fails, the agent should use the actual error output to diagnose the problem rather than guessing.

A successful build is necessary but is not, by itself, proof that every requested client feature is correct. Functional requirements and verification results must also be tracked.

## Private Use

AIAppBuilder is a private development tool.

It is not intended to provide direct access to clients or the general public.

Client requirements may be supplied to the agent by its owner for the purpose of developing applications.

## Development Principle

The primary development principle is:

**Understand → Plan → Generate → Build → Test → Fix → Verify → Deliver**

The agent should prefer correctness, accessibility, security, maintainability, and broad compatibility over simply generating code quickly.
