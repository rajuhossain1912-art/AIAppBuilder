# Provider Failover and Recovery

AIAppBuilder must not treat one source host or build service as a permanent dependency.

## Provider roles

- Primary source/build provider: GitHub and GitHub Actions while available.
- Future source providers: GitLab, Bitbucket, Gitea/Forgejo, or another compatible provider after an explicit integration is implemented and tested.
- Future build providers: any compatible cloud build service that is actually implemented and verified. No unverified provider is treated as a working fallback.

## Selection rules

1. Prefer the highest-priority healthy provider that supports the requested Android build.
2. If the primary provider is unavailable, select the next healthy provider.
3. If no provider is healthy, stop and report that the build cannot currently be executed.
4. Never claim an APK was built or verified when the provider did not return a successful build result.

## Important limitation

Provider failover does not remove the need for network access to cloud services. If the internet is unavailable, online AI, web research, remote repositories, and cloud builds cannot be performed. Local deterministic work may continue when a suitable local runtime exists.

## Backup and recovery

A future recovery bundle should preserve the project identity, Project Passport, source revision, generated project metadata, test/verification results, artifact checksums, and restore instructions. Secrets and credentials must never be stored in the recovery bundle.

## Current verified state

GitHub Actions is currently the only verified cloud Android build provider in this project. The provider abstraction is now in place so additional providers can be added without rewriting the core build orchestration.
