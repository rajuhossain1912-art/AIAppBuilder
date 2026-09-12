# AIAppBuilder Quota Protection Policy

## Purpose

This document defines how AIAppBuilder must monitor, protect, and respond to provider, build, storage, network, and other resource quotas.

The system must prevent unexpected costs, uncontrolled resource consumption, and false claims about availability or free usage.

## Core Rules

AIAppBuilder must:

1. Prefer free and approved resources when technically suitable.
2. Never silently use a paid resource.
3. Never assume that a service provides unlimited free usage.
4. Check available quota information when technically possible.
5. Stop when an important quota limit prevents safe continuation.
6. Never bypass provider limits or usage restrictions.
7. Avoid unnecessary resource consumption.
8. Record important quota-related failures and decisions.
9. Require user approval before an action that may create a financial obligation.
10. Report actual quota limitations honestly.

## Quota Categories

The system may need to monitor:

- AI model usage
- API request limits
- Build minutes
- GitHub Actions usage
- Storage capacity
- Network usage
- Provider rate limits
- Artifact storage
- Database limits
- Cloud-function or compute limits
- Other provider-specific resource limits

## Quota States

Where information is available, a resource may be classified as:

- AVAILABLE
- LIMITED
- NEAR_LIMIT
- EXHAUSTED
- UNKNOWN
- BLOCKED

UNKNOWN must not be treated as unlimited.

## Pre-Operation Check

Before a potentially resource-intensive operation, AIAppBuilder should determine when technically possible:

- Required resource
- Expected consumption
- Available quota
- Remaining quota
- Whether the operation may incur a charge
- Whether an approved free alternative exists

If the required information cannot be verified, the system should use conservative assumptions.

## Paid Usage Protection

AIAppBuilder must never:

- Enable billing automatically.
- Add a payment method automatically.
- Purchase credits automatically.
- Upgrade a plan automatically.
- Continue into paid usage silently.
- Bypass a provider's payment restriction.

If an operation may cause a financial charge, explicit user approval is required.

## Free Quota Exhaustion

When a free quota is exhausted:

1. Stop the affected operation.
2. Record the actual limitation.
3. Inform the user.
4. Check for an approved free alternative when appropriate.
5. Continue only if the alternative is safe and authorized.
6. Require approval if continuation may introduce cost or materially different permissions.

The system must not claim that the operation will continue for free when this has not been verified.

## Rate Limits

When a provider imposes request or rate limits, AIAppBuilder should:

- Respect the documented limit.
- Avoid unnecessary repeated requests.
- Use bounded retries.
- Apply appropriate delays when technically suitable.
- Stop when continued retries are not justified.

The system must not attempt to evade rate limits.

## Build Resource Protection

Build operations may consume significant resources.

The build system should:

- Avoid unnecessary rebuilds.
- Reuse valid results when appropriate.
- Stop repeated failing builds after a bounded number of attempts.
- Record build failures.
- Avoid infinite build loops.
- Prefer minimal fixes before rebuilding.

A build must not be repeated indefinitely merely because a previous attempt failed.

## AI Usage Protection

AI model usage should be controlled to avoid unnecessary consumption.

The system should:

- Send only information required for the operation.
- Avoid unnecessary duplicate prompts.
- Reuse verified context when appropriate.
- Limit uncontrolled retry loops.
- Prefer smaller suitable operations when possible.
- Stop when required provider access is unavailable.

The system must not claim that AI usage is free or unlimited unless verified.

## Storage Protection

AIAppBuilder should monitor storage where provider information is available.

The system should:

- Avoid unnecessary duplicate artifacts.
- Remove temporary data when safe and authorized.
- Preserve required project history.
- Protect important backups.
- Avoid deleting important history merely to recover space.

Storage cleanup must not silently destroy required project information.

## Network Protection

Network operations should be minimized when practical.

The system should:

- Avoid unnecessary downloads.
- Avoid repeated retrieval of identical resources.
- Prefer cached verified information when appropriate.
- Avoid uncontrolled polling.
- Respect provider and service limits.

Large or repeated network operations should be justified by the task.

## Quota Uncertainty

If quota information is unavailable or unreliable:

- Do not assume unlimited availability.
- Do not assume that usage is free.
- Do not assume that billing is disabled.
- Avoid unnecessary resource-intensive operations.
- Ask for user approval when financial risk may exist.

Uncertainty must result in conservative behavior.

## Alternative Providers

If a quota is exhausted, AIAppBuilder may consider an alternative provider only when:

- The provider is approved.
- The alternative is technically suitable.
- Privacy conditions are acceptable.
- Required permissions are acceptable.
- No unexpected cost is introduced.
- The switch is allowed by provider and security policies.

A switch to a paid provider requires explicit user approval.

## Provider Records

Important quota events should record, when available:

- Provider
- Resource category
- Operation
- Timestamp
- Quota state
- Relevant limit information
- Result
- Whether user approval was required
- Error or limitation information

Secrets and credentials must never be recorded.

## Resource-Intensive Operations

Operations that may require additional protection include:

- Large builds
- Repeated builds
- Large test suites
- Large artifact uploads
- Extensive AI requests
- Large research operations
- Large file transfers
- Bulk provider operations

The system should estimate or check resource requirements when practical.

## Retry Protection

Retries must be bounded.

A failed operation must not automatically retry forever.

Before retrying, AIAppBuilder should determine whether:

- The failure is temporary.
- The retry is likely to succeed.
- The provider allows another request.
- The retry may consume significant quota.
- The retry may cause a charge.

If repeated failures provide no reasonable path to success, the operation must stop.

## User Approval

Explicit approval should be requested before:

- Paid usage
- Plan upgrades
- Credit purchases
- Billing activation
- Resource expansion that may cost money
- Continuing after a free quota is exhausted when cost is possible
- Switching to a materially different provider with new permissions or privacy implications

Approval must be specific enough to understand the relevant consequence.

## Honest Reporting

AIAppBuilder must clearly distinguish between:

- Quota verified
- Quota unavailable
- Quota limited
- Quota exhausted
- Paid access available
- Paid access authorized
- Operation blocked
- Operation completed

The system must never invent quota values or claim successful usage without evidence.

## Policy Interaction

This policy must work together with:

- Provider Policy
- Security Policy
- Secure Storage Policy
- Resource Policy
- Approval Policy
- Privacy Policy

When policies conflict, the more restrictive security, privacy, cost, or authorization requirement should apply unless the user explicitly and validly approves a permitted alternative.

## Final Rule

AIAppBuilder must never spend money, bypass quotas, assume unlimited free usage, or consume resources without appropriate authorization and evidence.

When quota, cost, or availability is uncertain, the system must choose the safer option and stop for confirmation when necessary.
