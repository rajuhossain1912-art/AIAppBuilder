# AIAppBuilder AI Interaction Specification

## 1. Purpose

The AI Interaction Layer defines how AIAppBuilder communicates with external AI providers and how AI-generated responses are received, normalized, validated, controlled, and passed to the appropriate agent stage.

It is responsible for AI interaction only.

It must not bypass:

- Orchestrator
- Approval Policy
- Provider Policy
- Provider Registry
- Quota Manager
- Resource Policy
- Privacy Policy
- Secure Storage Policy
- Audit Memory
- Project isolation
- Review and verification gates

The AI Interaction Layer must never be treated as an unrestricted autonomous authority.

---

## 2. Core Principles

The AI Interaction Layer must be:

- Provider-independent
- Free-first
- Privacy-aware
- Approval-aware
- Quota-aware
- Resource-aware
- Project-aware
- Security-aware
- Auditable
- Deterministic where possible
- Failure-safe
- Bounded
- Verifiable
- Honest about uncertainty

It must never assume that an AI provider is:

- Available
- Free
- Authorized
- Safe
- Correct
- Unlimited
- Suitable for the requested task

These properties must be checked separately.

---

## 3. Supported Input

The AI Interaction Layer may receive:

- Bangla
- Banglish
- English
- Mixed-language text
- Informal language
- Spelling errors
- Voice-to-text output
- Incomplete descriptions
- Structured requirements
- Research context
- Existing project context
- Error reports
- Review findings
- Test results
- User-approved instructions

The original user request must be preserved.

The AI Interaction Layer must not silently rewrite the user's original request.

---

## 4. Interaction Roles

AI interaction may support different controlled roles, including:

- Requirements interpretation
- Clarification assistance
- Planning assistance
- Research assistance
- Code generation assistance
- Code explanation
- Review assistance
- Error analysis
- Test analysis
- Verification assistance
- Documentation assistance
- Delivery explanation

Each interaction must have a declared purpose.

The system must not use an AI response for a different purpose without passing through the appropriate control layer.

---

## 5. AI Request Record

Every AI interaction should have a structured request record.

Recommended fields:

```text
request_id
timestamp
project_id
session_id
actor
stage
purpose
provider_id
model_id
input_classification
input_reference
privacy_classification
approval_reference
quota_reference
resource_reference
maximum_cost
maximum_tokens
maximum_retries
timeout
status
