# AIAppBuilder Orchestrator State Model

## Purpose

This document defines the durable state model used by the AIAppBuilder Orchestrator.

The state model must allow the system to:

- Know exactly where a project is in its lifecycle.
- Preserve the previous state.
- Recover after interruption.
- Prevent invalid lifecycle transitions.
- Track approvals, errors, retries, and verified results.
- Report the actual project status honestly.

The state model must work together with `ORCHESTRATOR_SPEC.md`, approval policies, quota policies, security policies, project memory, audit records, build systems, testing systems, and delivery systems.

## Lifecycle States

The standard lifecycle states are:

```text
RECEIVED
UNDERSTANDING
AWAITING_CONFIRMATION
PLANNING
RESEARCHING
GENERATING
REVIEWING
BUILDING
TESTING
FIXING
VERIFYING
DELIVERING
COMPLETED
