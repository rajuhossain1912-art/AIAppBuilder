# AIAppBuilder — Project Structure and File Placement Rules

## Purpose

This document defines the canonical repository structure for AIAppBuilder.

The agent MUST determine the correct location for every new file before creating it. It MUST NOT create files or folders arbitrarily.

## Canonical Structure

```text
AIAppBuilder/
├── README.md
├── ARCHITECTURE.md
├── PROJECT_STRUCTURE.md
├── LICENSE
├── .gitignore
│
├── .github/
│   └── workflows/
│
├── config/
│   ├── policy/
│   ├── providers/
│   ├── security/
│   └── quotas/
│
├── agent/
│   ├── orchestrator/
│   ├── requirements/
│   ├── planning/
│   ├── research/
│   ├── generation/
│   ├── review/
│   ├── verification/
│   └── delivery/
│
├── memory/
│   ├── passport/
│   ├── audit/
│   ├── lessons/
│   └── backups/
│
├── knowledge/
│   ├── android/
│   ├── accessibility/
│   ├── kotlin/
│   ├── compose/
│   ├── testing/
│   ├── security/
│   ├── lessons-learned/
│   └── project-patterns/
│
├── templates/
│   ├── basic-android/
│   ├── offline-app/
│   ├── online-api-app/
│   ├── hybrid-app/
│   ├── tts-app/
│   ├── media-app/
│   ├── accessibility-first-app/
│   └── database-app/
│
├── projects/
│   └── <project-id>/
│       ├── passport/
│       ├── source/
│       ├── tests/
│       ├── build/
│       ├── artifacts/
│       └── reports/
│
├── tools/
│   ├── build/
│   ├── test/
│   ├── security/
│   └── maintenance/
│
└── docs/
    ├── decisions/
    ├── guides/
    └── operations/
