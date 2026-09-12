# AIAppBuilder Project Passport Specification

## 1. Purpose

The Project Passport is the authoritative identity and metadata record for an AIAppBuilder project.

It provides a stable reference for:

- Project identity
- Project ownership and scope
- Project lifecycle
- Requirements
- Architecture
- Technology
- Accessibility requirements
- Security and privacy requirements
- Provider usage
- Build and verification history
- Delivery status
- Project relationships
- Recovery and migration

The Project Passport must help the agent understand which project it is working on without relying only on the current conversation.

---

## 2. Core Principles

Every managed project must have a unique and stable project identity.

The passport must be:

- Persistent
- Structured
- Versioned
- Timestamped
- Project-specific
- Traceable
- Recoverable
- Privacy-aware
- Security-aware
- Migration-friendly
- Auditable

The passport must never contain unnecessary secrets.

The passport must represent known project facts and must not contain invented information.

---

## 3. Project Identity

Each project should have:

- Project ID
- Project name
- Project description
- Project type
- Owner
- Creation date
- Last updated date
- Current lifecycle state
- Current project version
- Repository reference when applicable
- Project status

The Project ID must remain stable for the lifetime of the project.

Project identity must not be silently changed because of a conversation reset, provider change, build failure, or migration.

---

## 4. Project ID

The Project ID must be unique.

Recommended format:

```text
project-YYYYMMDD-short-name-random-id
