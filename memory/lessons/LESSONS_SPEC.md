# AIAppBuilder Lessons Memory Specification

## 1. Purpose

The Lessons Memory system records verified lessons learned from completed work, failures, corrections, reviews, builds, tests, verification, research, and user feedback.

Lessons must help AIAppBuilder improve future decisions without inventing experience or changing approved policies silently.

The Lessons Memory system must work with:

- Orchestrator
- Project Passport
- Audit Memory
- Requirements
- Planning
- Research
- Generation
- Review
- Build
- Testing
- Verification
- Delivery
- Security Policy
- Privacy Policy
- Approval Policy
- Quota Policy
- Knowledge Base

---

## 2. Core Principles

Lessons must be:

- Evidence-based
- Traceable
- Project-aware
- Reusable when appropriate
- Clearly separated from facts
- Clearly separated from assumptions
- Clearly separated from permanent policy
- Correctable
- Searchable
- Privacy-aware
- Security-aware

AIAppBuilder must never create a lesson from an unverified assumption.

A lesson must not override an explicit user requirement, security rule, approval rule, privacy rule, or system policy.

---

## 3. Lesson Identity

Each lesson should have a unique Lesson ID.

Recommended format:

```text
lesson-YYYYMMDD-random-id
