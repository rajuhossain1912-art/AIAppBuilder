# AIAppBuilder Provider Policy

## Purpose

This document defines the rules for external providers used by AIAppBuilder.

The provider system must remain provider-agnostic, secure, privacy-aware, quota-aware, and free-first.

## Provider Categories

AIAppBuilder may use provider abstractions for:

- AI model providers
- Git providers
- Build providers
- Storage providers
- Research providers

## Provider Selection

The system must:

1. Prefer an approved free option when technically suitable.
2. Never silently switch to a paid provider.
3. Never add a payment method automatically.
4. Never create a billing account automatically.
5. Require user approval before enabling paid services.
6. Record the provider selected for important operations.
7. Record relevant quota or availability information when available.

## Provider Independence

Core application logic must not depend permanently on one external provider.

Provider-specific implementations must remain behind defined interfaces or adapters.

Replacing one provider should not require unnecessary changes to unrelated components.

## Credentials

Provider credentials must:

- Never be hard-coded in source code.
- Never be committed to the repository.
- Never be written into generated project source.
- Be stored only through an approved secure mechanism.
- Be used only when the user has authorized the relevant provider.
- Never be exposed in logs, reports, error messages, or generated artifacts.

## Privacy

The provider system must minimize external data transmission.

Before sending project information to an external provider, the system should determine:

- What data is being sent.
- Why it is required.
- Whether the provider is authorized.
- Whether confidential information can be removed or minimized.
- Whether the operation requires user approval.

Private project information must not be sent to unrelated providers.

## Paid Services

Any action that may create a financial obligation requires explicit user approval.

Examples include:

- Enabling a paid API.
- Adding a payment method.
- Creating a billing account.
- Purchasing credits.
- Subscribing to a service.
- Exceeding a free quota when charges may occur.

If approval is not available, the operation must stop.

## Quota Protection

Before resource-intensive operations, the system should check available quotas when the provider exposes quota information.

The system must not claim unlimited free usage unless this has been verified.

If a free quota is exhausted and no approved free alternative exists, the system must stop and report the limitation.

## Provider Failure

When a provider fails, the system should:

1. Capture the actual error.
2. Determine whether the failure is temporary or permanent when possible.
3. Avoid uncontrolled retries.
4. Respect provider rate limits.
5. Use an approved alternative provider only when policy permits.
6. Require approval when switching would introduce cost, new permissions, or materially different privacy conditions.

## Provider Records

Important provider operations should record:

- Provider name
- Provider category
- Operation
- Date and time
- Success or failure
- Relevant quota information
- Approval status when applicable
- Error information when applicable

Sensitive credentials must never be recorded.

## Safety

AIAppBuilder must not use providers to create or facilitate:

- Malware
- Credential theft
- Spyware
- Unauthorized surveillance
- Fraud
- Unauthorized access
- Other intentionally harmful software

Provider access must never be used to bypass AIAppBuilder safety policies.

## Policy Changes

Provider policies must not be weakened automatically.

Changes affecting:

- Cost
- Privacy
- Security
- Permissions
- Provider trust
- Data handling

must be reviewed before becoming active.

## Default Rule

When provider safety, cost, privacy, authorization, or quota status is uncertain, AIAppBuilder must prefer the safer option and stop for user confirmation when necessary.
