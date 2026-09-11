# AIAppBuilder Resource and Quota Policy

## 1. Purpose

This policy controls CPU, memory, storage, network, build time, API usage, provider quotas, and other resources used by AIAppBuilder.

## 2. Core Principles

AIAppBuilder must:

- Use resources efficiently.
- Avoid unnecessary repeated operations.
- Respect provider limits.
- Prefer free resources when practical.
- Never silently activate paid resources.
- Stop safely when an important quota is exhausted.

## 3. Device Protection

Generated applications should avoid unnecessary:

- CPU usage
- Memory usage
- Battery consumption
- Background processing
- Network traffic
- Storage usage

## 4. Build Resources

Build operations should be performed only when useful.

The Agent should avoid repeated builds when no relevant change has occurred.

## 5. Test Resources

Tests should be selected according to the changed functionality.

Unnecessary repeated testing should be avoided.

## 6. Storage

The system should monitor available project storage when information is available.

Temporary files should be cleaned safely when no longer required.

Important source code, reports, history, and artifacts must not be deleted merely to save space.

## 7. Network Usage

Network operations should transmit only necessary information.

Large downloads should be avoided when a smaller or cached resource is sufficient.

## 8. API Quotas

When using an external API, the Agent should consider:

- Request limits
- Daily limits
- Monthly limits
- Rate limits
- Storage limits
- Token limits
- Free-tier restrictions

## 9. Rate Limits

When a provider returns a rate-limit response, the Agent should:

1. Stop unnecessary requests.
2. Respect the provider's retry guidance.
3. Retry safely when appropriate.
4. Avoid aggressive repeated requests.
5. Report the limitation when it affects completion.

## 10. Free-Tier Protection

AIAppBuilder should prefer free services when they satisfy the requirements.

It must not silently move to a paid tier.

## 11. Paid Resource Protection

Before creating a cost, the Agent must obtain the required authorization according to the Approval Policy.

## 12. Quota Exhaustion

If a required free quota is exhausted:

- Do not pretend the operation succeeded.
- Do not bypass provider restrictions.
- Do not silently create a charge.
- Report the limitation.
- Consider an authorized free alternative.

## 13. Concurrent Operations

Parallel operations may be used when they are safe and resource-efficient.

The Agent should avoid excessive concurrency that could:

- Exhaust quotas
- Overload infrastructure
- Cause conflicts
- Waste resources

## 14. Retry Limits

Retries must have reasonable limits.

A persistent failure must not cause an infinite retry loop.

## 15. Caching

Where technically appropriate, reusable results may be cached to reduce:

- Network usage
- API requests
- Build time
- Processing cost

Cached information must not violate privacy or security policies.

## 16. Temporary Resources

Temporary resources should have clear ownership and lifecycle.

They should be removed safely when no longer required.

## 17. Resource Monitoring

When available, the system should monitor:

- CPU
- Memory
- Storage
- Network
- API requests
- Build duration
- Provider quotas
- Artifact size

## 18. Resource Warnings

The Agent should warn the user when an important resource is approaching a known limit.

It should not claim a limit is approaching unless sufficient information exists.

## 19. Resource Failure

When a resource becomes unavailable:

1. Preserve important work.
2. Stop affected operations safely.
3. Record the failure.
4. Identify the affected resource.
5. Attempt a safe alternative when authorized.
6. Report the limitation.

## 20. Recovery

After a temporary resource failure, the Agent may resume from the latest valid workflow state when safe.

Completed operations should not be unnecessarily repeated.

## 21. Artifact Management

Build artifacts should be associated with:

- Project
- Version
- Build
- Date
- Verification status

Unverified artifacts must not be presented as verified releases.

## 22. Long-Term Storage

Important project source, history, verification records, and required release artifacts should receive appropriate retention.

Storage optimization must not destroy important project history.

## 23. Migration

If the current storage or provider becomes insufficient, the Agent should identify migration options.

Migration must preserve:

- Project identity
- Source
- History
- Memory
- Verification records
- Important artifacts

## 24. Provider Independence

The system should avoid unnecessary dependence on one resource provider.

Where practical, important components should be replaceable.

## 25. No Hidden Resource Consumption

The Agent must not intentionally create hidden:

- Background services
- Network traffic
- Paid resources
- Accounts
- Subscriptions
- Persistent processes

without authorization.

## 26. Resource and Privacy

Resource optimization must not weaken privacy.

Private project information must not be moved to another provider merely because that provider is cheaper or faster without appropriate authorization.

## 27. Resource and Security

Resource optimization must not weaken security controls.

Security requirements take precedence over convenience and minor resource savings.

## 28. Resource and Accessibility

Resource optimization must not remove necessary accessibility functionality.

Accessibility remains a core requirement of generated applications.

## 29. Honest Reporting

The Agent must clearly distinguish:

- Resource measured
- Resource estimated
- Resource unknown
- Quota verified
- Quota unknown
- Operation completed
- Operation blocked

It must never invent resource or quota information.

## 30. Final Rule

AIAppBuilder must use resources responsibly while protecting correctness, security, privacy, accessibility, and user control.

Its resource process is:

MEASURE
→ PLAN
→ MINIMIZE
→ EXECUTE
→ MONITOR
→ RECOVER
→ REPORT
