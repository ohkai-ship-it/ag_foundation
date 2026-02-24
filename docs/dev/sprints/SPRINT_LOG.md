# Sprint Log — ag_foundation

This is the central log for all sprints. Each sprint gets a section below; we do **not** create per-sprint folders.

---

## Sprint 01 — Core runtime skeleton v0
**Dates:** 2026-03-02 → 2026-03-15  
**Goal:** Ship the minimal end-to-end runtime so `ag run "<prompt>"` produces a persisted `RunTrace` (truthful UX) in an isolated workspace.

### Targeted Backlog Items

| ID | Priority | Title | Status | PR |
|---:|:--:|---|:--:|---|
| AF-0004 | P0 | Sprint OS hygiene: sprint log + docs/dev pointers + handoff rules | Done | — |
| AF-0010 | P0 | Python project bootstrap (packaging + CLI stub + pytest) | Done | — |
| AF-0005 | P0 | Contracts: TaskSpec + RunTrace + Playbook schemas v0.1 | Not Started | — |
| AF-0006 | P0 | Workspace + storage baseline (sqlite + filesystem) | Not Started | — |
| AF-0007 | P0 | Core runtime skeleton v0 (interfaces + playbook + stub skills) | Not Started | — |
| AF-0008 | P0 | CLI v0: ag run + runs show --json, truthful labels, manual gate | Not Started | — |
| AF-0009 | P1 | Artifact registry v0 + ag artifacts list | Not Started | — |

### Sprint Notes
- Sprint plan: [SPRINT_PLAN_SPRINT01.md](SPRINT_PLAN_SPRINT01.md)
- Handoff outputs: [/docs/dev/handoff/](../handoff/)

---

## Sprint 00 — Project bootstrap (Docs + repo operating system)
**Dates:** 2026-02-01 → 2026-02-28  
**Goal:** Establish a clean documentation baseline and workflow.

### Completed Items

| ID | Priority | Title | Status |
|---:|:--:|---|:--:|
| AF-0001 | P0 | Kick-off: establish new docs/dev foundation | Done |
| AF-0002 | P0 | New cornerstone docs (IoT-in-space vision) | Done |
| AF-0003 | P0 | Core runtime skeleton (request + event driven) | Done (docs-only) |

### Sprint Notes
- Cornerstone docs authored: PROJECT_PLAN, ARCHITECTURE, CLI_REFERENCE, REVIEW_GUIDE
- ADRs created: ADR-0001 through ADR-0005
- Review entry: [2026-02-23-kickoff.md](../reviews/entries/2026-02-23-kickoff.md)

---

## Log Format

Each sprint section should include:
1. **Dates** and **Goal** (one sentence)
2. **Targeted Backlog Items** table with status and PR links
3. **Sprint Notes** with links to plan, report, and handoff outputs
