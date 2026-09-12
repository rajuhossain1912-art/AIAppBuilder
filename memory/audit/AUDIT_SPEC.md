# AIAppBuilder Audit Memory Specification

## 1. Purpose

The Audit Memory system records important actions, decisions, state changes, approvals, failures, recoveries, and results performed within AIAppBuilder.

Audit records provide an evidence-based historical record of what happened.

The audit system must work with:

- Orchestrator State
- Project Passport
- Requirements
- Planning
- Research
- Generation
- Review
- Build
- Testing
- Verification
- Delivery
- Approval Policy
- Security Policy
- Privacy Policy
- Quota Policy
- Memory System

---

## 2. Core Principle

Audit records must answer:

- What happened?
- When did it happen?
- Which project was affected?
- Who or what performed the action?
- Why did it happen?
- What authorization existed?
- What was the result?
- What evidence supports the result?

The audit system must never invent historical events.

---

## 3. Audit Record Identity

Each audit record should have a unique Audit ID.

Recommended format:

```text
audit-YYYYMMDD-random-id
