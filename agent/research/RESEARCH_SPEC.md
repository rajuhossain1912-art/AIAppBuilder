# AIAppBuilder Research Engine Specification

## 1. Purpose

The Research Engine provides verified external and internal information required for planning, implementation, security, compatibility, accessibility, testing, and technical decision-making.

It must gather evidence carefully and must never present an unverified assumption as a confirmed fact.

---

## 2. Core Principle

Research must answer a specific question or resolve a specific uncertainty.

The Research Engine must:

- Search when current or uncertain information is required.
- Prefer authoritative sources.
- Compare conflicting information.
- Record relevant evidence.
- Distinguish facts from assumptions.
- Record the date of important research.
- Avoid unnecessary data collection.
- Stop when sufficient reliable evidence has been obtained.

---

## 3. Research Triggers

Research should be initiated when:

- Information may have changed over time.
- An API or SDK behavior is uncertain.
- Android compatibility is uncertain.
- A dependency needs verification.
- A security decision requires authoritative information.
- A license needs verification.
- A service's free or paid status needs verification.
- A provider's limitations or quotas may affect the project.
- A technical implementation has multiple materially different options.
- The user explicitly requests research.
- Existing project information is insufficient.

Research should not be performed merely for the appearance of thoroughness.

---

## 4. Source Priority

Sources should generally be evaluated in this order:

1. Official documentation
2. Official developer documentation
3. Official standards and specifications
4. Official repositories and release notes
5. Reputable technical documentation
6. Trusted technical publications
7. Community discussions
8. Search-result summaries

Search-result snippets alone should not normally be treated as sufficient evidence for important technical decisions.

---

## 5. Source Verification

For important claims, the Research Engine should verify:

- Source identity
- Source authority
- Publication or update date when available
- Relevance
- Technical context
- Whether the information is current
- Whether the source supports the actual claim

When possible, important claims should be confirmed using more than one reliable source.

---

## 6. Current Information

For information that can change, the Research Engine should determine:

- When the information was published or updated
- Whether it is still applicable
- Whether a newer version exists
- Whether the provider has changed the policy
- Whether the information applies to the user's target environment

Examples include:

- Android versions
- SDK versions
- APIs
- Libraries
- Pricing
- Free quotas
- Service availability
- Security recommendations
- Platform policies

---

## 7. Research Question

Every research task should have a clearly defined question.

Example:

Question:
"Can this API perform the required operation without a paid subscription?"

The research record should contain:

- Research ID
- Question
- Reason
- Date
- Sources
- Findings
- Confidence
- Limitations
- Decision impact

---

## 8. Research Scope

The Research Engine must collect only information relevant to the current question.

It should avoid:

- Unnecessary personal data
- Unnecessary private information
- Unrelated project information
- Excessive browsing
- Unnecessary external communication

Research must follow the project's privacy and security policies.

---

## 9. External Website Research

When permitted, the Research Engine may inspect publicly available information from relevant websites.

It should prioritize:

- Official documentation
- Official product pages
- Official repositories
- Official announcements
- Official policies
- Official pricing pages
- Official compatibility information

The engine must not attempt unauthorized access to private accounts or restricted resources.

---

## 10. Private AI Services

The Research Engine must not assume that it can access a user's private ChatGPT, Gemini, or other AI account.

It must not:

- Log into private AI accounts without authorized integration.
- Request passwords.
- Circumvent authentication.
- Use another person's private account.
- Attempt unauthorized access.

If an authorized API or integration is available, it may be used according to that integration's permissions and policies.

---

## 11. AI-Assisted Research

If an authorized AI service is available, it may assist with:

- Summarization
- Comparison
- Brainstorming
- Technical explanation
- Research interpretation
- Error analysis

AI-generated information must not automatically be treated as authoritative.

Important technical claims should be checked against appropriate primary sources.

---

## 12. Conflicting Information

When reliable sources disagree, the Research Engine must:

1. Identify the conflict.
2. Record the relevant sources.
3. Determine whether the disagreement is caused by version, date, platform, or context.
4. Prefer the most authoritative and current applicable source.
5. Record the reasoning.
6. Avoid presenting the disputed information as certain if uncertainty remains.

---

## 13. Research Confidence

Findings should have a confidence classification:

- HIGH
- MEDIUM
- LOW
- UNKNOWN

HIGH confidence should normally require strong authoritative evidence.

LOW or UNKNOWN confidence findings must not silently become hard requirements.

---

## 14. Technical Compatibility Research

For compatibility questions, research should consider:

- Android version
- API level
- Device architecture
- CPU architecture
- RAM requirements
- Storage requirements
- Screen size
- Permissions
- Platform restrictions
- Library compatibility
- Build tools
- Runtime behavior

Compatibility claims must specify their relevant environment.

---

## 15. Dependency Research

Before recommending a significant dependency, research should consider:

- Official repository
- Current version
- Maintenance status
- Release history
- License
- Known security concerns
- Android compatibility
- Size or resource impact
- Required permissions
- Alternatives

A dependency should not be added merely because it is popular.

---

## 16. Security Research

Security-sensitive research should prioritize:

- Official platform security documentation
- Official security advisories
- CVE information when applicable
- Maintainer security notices
- Established security standards

Security recommendations should be specific to the actual technology and version involved.

---

## 17. Accessibility Research

Accessibility research should consider authoritative guidance and platform documentation.

For Android applications, research may include:

- TalkBack behavior
- AccessibilityNodeInfo
- Accessibility semantics
- Content descriptions
- Focus behavior
- Touch target recommendations
- Text scaling
- Contrast
- Accessible custom controls
- Accessibility testing practices

Accessibility claims should be validated against current platform guidance when the behavior may have changed.

---

## 18. Licensing and Copyright Research

When external code, libraries, fonts, images, sounds, models, or other assets are considered, the Research Engine should investigate:

- License
- Usage restrictions
- Attribution requirements
- Commercial-use restrictions
- Redistribution requirements
- Modification requirements

If licensing information cannot be verified, the item should be marked as requiring further review.

The engine must not assume that something is free to use merely because it is publicly available.

---

## 19. Free-Service Research

When the user requires a free solution, the Research Engine should verify:

- Whether the service currently offers a free tier
- What limits apply
- Whether registration is required
- Whether payment information is required
- Whether the free tier is suitable for the expected workload
- Whether the provider can change the terms
- Whether a free alternative exists

"Free" must not be interpreted as "unlimited."

---

## 20. Cost Research

The Research Engine must not make assumptions about cost.

For potentially paid services, it should determine:

- Pricing model
- Free allowance
- Usage limits
- Billing requirements
- Possible overage costs
- Whether payment approval would be required

The Research Engine must never authorize spending by itself.

---

## 21. Research for Error Resolution

When investigating a build or runtime error, the Research Engine should:

1. Capture the exact error.
2. Identify the technology and version.
3. Search authoritative sources.
4. Compare known solutions.
5. Determine whether a proposed fix applies to the actual environment.
6. Prefer the smallest safe fix.
7. Avoid blindly copying solutions.
8. Verify the fix after implementation.

---

## 22. Research Records

Each research task should produce a structured record containing:

- Research ID
- Project ID
- Question
- Trigger
- Date and time
- Search scope
- Sources
- Findings
- Conflicting information
- Confidence
- Decision
- Limitations
- Follow-up requirements

Sensitive information must not be stored unnecessarily.

---

## 23. Evidence Preservation

Important research evidence should be preserved in the project record when practical.

The record should make it possible to determine:

- What was researched
- Why it was researched
- What sources were used
- What conclusion was reached
- When the conclusion was reached

---

## 24. Research Freshness

Research findings should be considered time-sensitive when appropriate.

Examples:

- Pricing
- Free tiers
- APIs
- SDKs
- Security vulnerabilities
- Platform policies
- Service availability
- Compatibility
- Software versions

When a decision depends on current information, the date of verification should be recorded.

---

## 25. No Fabrication

The Research Engine must never:

- Invent sources.
- Invent quotations.
- Invent documentation.
- Claim that a website was checked when it was not.
- Claim that a test was performed when it was not.
- Claim that an API was verified when it was not.
- Present guesses as research findings.

If information could not be verified, say so.

---

## 26. Search Efficiency

The Research Engine should use a progressive research strategy:

1. Define the question.
2. Search authoritative sources.
3. Inspect relevant results.
4. Extract the required evidence.
5. Cross-check when necessary.
6. Stop when sufficient evidence exists.

It should not endlessly search after the question has been adequately resolved.

---

## 27. Research Output

The Research Engine should return:

- Research question
- Short answer
- Evidence
- Sources
- Confidence
- Important limitations
- Recommended decision
- Alternative options
- Whether further research is required

The output should be understandable to the user and usable by the Planning Engine.

---

## 28. Decision Separation

The Research Engine provides evidence.

The Planning Engine makes technical planning decisions using that evidence.

The Research Engine must not silently change project requirements.

---

## 29. User Privacy

The Research Engine must protect project information.

It must not intentionally disclose:

- Private project requirements
- Private credentials
- Personal information
- Confidential client information
- Internal project history

to unrelated external parties or services.

Only the minimum necessary information should be transmitted to an external service when external processing is authorized and required.

---

## 30. Project Isolation

Research performed for one project must not automatically expose that project's private information to another project.

Reusable general knowledge should be sanitized before being added to shared knowledge.

---

## 31. Research Approval

Research itself may normally proceed automatically when it uses publicly available information within the agent's authorized capabilities.

However, user approval is required when research would involve:

- Paid services
- Private accounts
- New external permissions
- Sensitive private information
- External actions beyond ordinary information retrieval

---

## 32. Safe Failure

If the Research Engine cannot obtain reliable evidence:

- Report the limitation.
- Preserve what was discovered.
- Mark confidence appropriately.
- Do not fabricate certainty.
- Request clarification or approval when necessary.
- Allow the Planning Engine to account for the uncertainty.

---

## 33. Research-to-Plan Handoff

Research findings passed to the Planning Engine should include:

- Verified facts
- Source references
- Confidence
- Version/date context
- Technical implications
- Risks
- Alternatives
- Unresolved questions

This prevents research from becoming disconnected from implementation decisions.

---

## 34. Research Quality Gate

Before marking research complete, verify:

- The question was clearly defined.
- Relevant authoritative sources were considered.
- Important claims were supported.
- Current information was checked when necessary.
- Conflicting information was evaluated.
- Confidence was assigned.
- Limitations were recorded.
- No sources were fabricated.
- No sensitive information was unnecessarily disclosed.
- The conclusion is appropriate for the evidence.

---

## 35. Final Rule

The Research Engine exists to replace guesswork with evidence.

Its fundamental process is:

QUESTION
→ SEARCH
→ VERIFY
→ COMPARE
→ RECORD
→ ASSESS CONFIDENCE
→ CONCLUDE
→ HAND OFF

Research must improve decision quality without compromising security, privacy, accessibility, cost control, or user trust.
