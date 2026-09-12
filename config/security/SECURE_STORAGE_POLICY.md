# AIAppBuilder Secure Storage Policy

## Purpose

This document defines how AIAppBuilder must protect credentials, tokens, secrets, sensitive configuration, and other security-sensitive data.

The system must follow secure-by-default principles and must never store secrets in source code or generated project files.

## Core Rules

AIAppBuilder must:

1. Never hard-code secrets in source code.
2. Never commit credentials or private tokens to Git.
3. Never place secrets inside generated Android source files.
4. Never expose secrets in logs, reports, error messages, or artifacts.
5. Use the minimum required credential scope.
6. Use credentials only for authorized operations.
7. Avoid collecting credentials that are not required.
8. Never reveal stored credentials to the user through unsafe output.
9. Never copy credentials between unrelated projects.
10. Never silently create, rotate, or replace credentials.

## Secret Categories

Sensitive values may include:

- API keys
- Access tokens
- Refresh tokens
- OAuth credentials
- Private keys
- Signing keys
- Passwords
- Session credentials
- Provider credentials
- Repository credentials
- Cloud service credentials
- Encryption keys
- Other authentication secrets

All such values must be treated as sensitive unless explicitly classified otherwise.

## Repository Protection

The repository must never contain:

- Plain-text API keys
- Passwords
- Private access tokens
- Private cryptographic keys
- Authentication cookies
- Payment credentials
- Personal authentication data

Secret files must be excluded from version control where appropriate.

The `.gitignore` policy must support this protection.

## Environment Separation

Development, testing, and production credentials should remain separate.

A credential authorized for one environment must not automatically be reused in another environment.

Project-specific credentials must remain isolated from credentials belonging to other projects.

## Provider Authorization

Before using a credential, AIAppBuilder should verify when technically possible:

- Which provider it belongs to.
- Which operation it authorizes.
- Whether the user has authorized its use.
- Whether the credential is still valid.
- Whether the requested operation requires additional permissions.

The agent must not expand the scope of authorization by itself.

## Least Privilege

Credentials should have the smallest practical permission scope.

The system should prefer:

- Read-only access when write access is unnecessary.
- Project-specific access when available.
- Short-lived credentials when available.
- Limited-scope tokens instead of broad administrative credentials.

Broad privileges must not be requested merely for convenience.

## Credential Exposure Prevention

Credentials must not appear in:

- Console output
- Build logs
- Test reports
- Crash reports
- Audit records
- Generated documentation
- Screenshots
- APK metadata
- Source-code comments
- Commit messages

If a provider returns a secret in an error or response, the system should redact it before storing or displaying the information.

## Logging and Audit

Security-sensitive operations may be recorded in the audit system, but secret values must never be recorded.

An audit record may contain:

- Provider
- Operation
- Timestamp
- Project
- Result
- Authorization status
- Non-sensitive error information

It must not contain the credential itself.

## Generated Applications

AIAppBuilder must not embed private provider credentials directly inside generated Android applications.

If an application requires an external service, the architecture must determine an appropriate secure mechanism.

Client applications must not receive AIAppBuilder's private credentials merely because the application uses the same provider.

## Android Signing

Application signing credentials are sensitive.

Signing keys and keystores must:

- Never be committed to the repository.
- Never be included in generated source code.
- Never be printed in logs.
- Be handled through an approved secure mechanism.
- Require explicit authorization for signing operations where appropriate.

## Backup Protection

Backups containing secrets or sensitive configuration must receive protection appropriate to their sensitivity.

The system must not create an unprotected copy of a secret merely for backup convenience.

If secure backup is unavailable, the system must report the limitation rather than pretending that the data is safely backed up.

## Secret Rotation

Credential rotation must be controlled.

AIAppBuilder must not automatically rotate or revoke credentials unless:

- The operation is explicitly authorized, or
- An established security policy explicitly permits the action.

Before a potentially destructive credential operation, the system should preserve necessary non-secret diagnostic information.

## Credential Revocation

If a credential is suspected to be compromised, the system should:

1. Stop unnecessary use of the credential.
2. Record the security event without recording the secret.
3. Inform the user when appropriate.
4. Recommend or perform authorized revocation.
5. Require authorization before creating a replacement credential when necessary.
6. Verify the replacement before resuming dependent operations.

## Paid Services

Credentials must not be used to bypass payment restrictions, quotas, account limits, or provider policies.

A credential that could cause financial charges must be treated as high-risk.

AIAppBuilder must require explicit user approval before performing an operation that may create a financial obligation.

## Cross-Project Isolation

Credentials must never be shared between unrelated projects unless explicitly authorized and technically appropriate.

A project must not be able to access another project's private credentials through normal project operations.

## Failure Handling

If secure credential storage or retrieval is unavailable:

- Do not fall back to plain-text storage.
- Do not write the credential into source code.
- Do not commit the credential to Git.
- Do not expose the credential in an error message.
- Stop the dependent operation and report the actual limitation.

## Security Defaults

When the correct security handling is uncertain, AIAppBuilder must choose the safer option.

The system must prefer:

- No secret over an unnecessary secret.
- Least privilege over broad privilege.
- Isolation over sharing.
- Redaction over disclosure.
- Explicit approval over implicit authorization.
- Stopping safely over insecure continuation.

## Policy Changes

Changes to this policy must be reviewed before becoming active.

The agent must not weaken credential protection rules automatically.

Any change affecting:

- Secret storage
- Credential access
- Permission scope
- Project isolation
- Logging
- Encryption
- Backup protection

must receive appropriate review.

## Final Rule

No convenience, build requirement, provider requirement, or automation requirement justifies placing a sensitive credential in source code, generated application code, public repository content, logs, or other unsafe locations.
