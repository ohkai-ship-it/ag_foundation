# Sprint Log — ag_foundation

> **⚠️ DEPRECATED (2026-03-03):** This log is archived. Sprint tracking now uses per-sprint folders under `/docs/new_dev/sprints/documentation/`. See `/docs/new_dev/sprints/INDEX_SPRINTS.md` for the canonical sprint index.

This is the central log for all sprints. Each sprint gets a section below; we do **not** create per-sprint folders.

---

## Sprint 03 — Observability & Truthful UX — COMPLETED
**Dates:** 2026-02-27 → 2026-02-28  
**Goal:** Strengthen workspace maturity, fix manual mode gating, and enforce observability + truthful UX.

### Targeted Backlog Items

| ID | Priority | Title | Status | Evidence |
|---:|:--:|---|:--:|---|
| AF-0027 | P0 | Default workspace policy (intuitive precedence) | Done | 5+ workspace policy tests |
| AF-0028 | P0 | Run ID truncation fix | Done | Full UUID in `ag runs list` |
| AF-0029 | P0 | RunTrace verification hardening | Done | 3 verifier consistency tests |
| AF-0030 | P0 | RunTrace metadata completeness (workspace_source) | Done | 2 workspace_source tests |
| AF-0031 | P0 | CLI truthfulness enforcement | Done | extract_labels tests |
| AF-0032 | P0 | Observability command expansion | Done | `ag runs stats` command |
| AF-0033 | P0 | Early .env loading + manual mode gate fix | Done | subprocess dotenv test |
| BUG-0006 | P1 | Manual mode .env loading defect | Fixed | AG_DEV from .env works |

### Sprint Summary
- **Tests:** 188 passed (was 178 before Sprint 03)
- **Coverage:** 76% overall, 100% run_trace, 100% task_spec, 93% config
- **New features:** `ag runs stats`, `workspace_source` metadata, verifier consistency
- **Review:** APPROVED — see [REVIEW_S03_FINDINGS.md](../reviews/entries/REVIEW_S03_2026-02-27/REVIEW_S03_FINDINGS.md)

### Sprint Notes
- Sprint plan: [SPRINT_03_PLAN.md](SPRINT_03_PLAN.md)
- Sprint report: [SPRINT_REPORT_SPRINT03.md](SPRINT_REPORT_SPRINT03.md)
- Completion note: [S03_COMPLETION_NOTE.md](S03_COMPLETION_NOTE.md)
- Workspace Resolution Order: `--workspace` → persisted default → `AG_WORKSPACE` → bootstrap 'default' → error

---

## Sprint 02 Hardening Extension — Storage, Coverage, Config, Workspace Policy
**Dates:** 2026-02-26  
**Goal:** Harden Sprint 02 deliverables after SQLite connection leak discovery (BUG-0004) and sign-off verification findings.

### Targeted Backlog Items

| ID | Priority | Title | Status | Evidence |
|---:|:--:|---|:--:|---|
| BUG-0004 | P1 | SQLite connections not closed → ResourceWarning | Fixed | pytest -W error passes |
| BUG-0005 | P0 | Implicit workspace creation on ag run | Fixed | 5 regression tests |
| AF-0021 | P1 | Storage lifecycle hardening (SQLite deterministic closure) | Done | 96% storage coverage |
| AF-0022 | P1 | Provider coverage hardening (≥95% target) | Done | 96% provider coverage |
| AF-0023 | P1 | Environment & configuration hardening | Done | 98% config coverage |
| AF-0024 | P1 | Workspace lifecycle correction (ag ws create/list) | Done | CLI tests |
| AF-0025 | P1 | Test discipline enforcement (Ruff + docs) | Done | ruff check passes |
| AF-0026 | P0 | Workspace selection policy enforcement | Done | 5 regression tests |

### Sprint Summary
- **Tests:** 174 passed (was 173 before hardening)
- **Coverage:** 90% overall, 96% storage, 96% providers, 98% config
- **Bugs fixed:** 2 (BUG-0004: SQLite leak, BUG-0005: implicit workspace)
- **Breaking change:** Workspace selection policy — `ag run` requires explicit `--workspace` or `AG_WORKSPACE`

### Sprint Notes
- Sprint report: [SPRINT_REPORT_SPRINT02_HARDENING.md](SPRINT_REPORT_SPRINT02_HARDENING.md)
- Sign-off findings: `/docs/dev/reviews/entries/REVIEW_S02_2026-02-26_SIGNOFF_FINDINGS.md`
- Bug reports: `/docs/dev/bugs/reports/` (BUG-0004, BUG-0005)
- Completion notes: `/docs/dev/backlog/completion/` (AF-0021 through AF-0026)

---

## Sprint 02 — Agent network v0 + LLM provider adapter (OpenAI first)
**Dates:** 2026-02-25 → 2026-02-26  
**Goal:** Extend the v0 runtime to multi-step delegation with provider abstraction and OpenAI as first real LLM provider.

### Targeted Backlog Items

| ID | Priority | Title | Status | Evidence |
|---:|:--:|---|:--:|---|
| AF-0014 | P1 | Resolve Recorder interface discrepancy (docs vs implementation) | Done | CONTRACT_INVENTORY updated |
| AF-0016 | P2 | Resolve ReasoningMode enum + Artifact semantics | Done | CONTRACT_INVENTORY fixed |
| AF-0018 | P1 | Provider abstraction + Claude/local stubs | Done | 34 tests |
| AF-0017 | P0 | OpenAI API integration (provider adapter) | Done | Mocked tests + integration marker |
| AF-0019 | P0 | Agent network playbook v0: delegation | Done | 23 tests |
| AF-0011 | P1 | CLI global options truly global | Done | 13 tests |

### Sprint Summary
- **Tests:** 173 passed (was 137 at Sprint 01 end)
- **Coverage:** 89% overall (was 88%)
- **CLI coverage:** 72% (was 64%, +8pp)
- **New modules:** `src/ag/providers/` (base, registry, stubs, openai)
- **New playbook:** `delegate_v0` with 6 steps (normalize→plan→execute×2→verify→finalize)
- **New models:** `Subtask`, `StepType.PLANNING`

### Sprint Notes
- Sprint plan: [SPRINT_PLAN_SPRINT02.md](SPRINT_PLAN_SPRINT02.md)
- Review evidence: `/docs/dev/reviews/entries/REVIEW_S01_2026-02-24/` (CONTRACT_INVENTORY, TEST_INVENTORY)
- Continuation prompt: `/docs/dev/prompts/continuation_prompt_sprint03_opus.md`

---

## Sprint 01 — Core runtime skeleton v0
**Dates:** 2026-03-02 → 2026-03-15  
**Goal:** Ship the minimal end-to-end runtime so `ag run "<prompt>"` produces a persisted `RunTrace` (truthful UX) in an isolated workspace.

### Targeted Backlog Items

| ID | Priority | Title | Status | PR |
|---:|:--:|---|:--:|---|
| AF-0004 | P0 | Sprint OS hygiene: sprint log + docs/dev pointers + handoff rules | Done | — |
| AF-0010 | P0 | Python project bootstrap (packaging + CLI stub + pytest) | Done | — |
| AF-0005 | P0 | Contracts: TaskSpec + RunTrace + Playbook schemas v0.1 | Done | feat/contracts |
| AF-0006 | P0 | Workspace + storage baseline (sqlite + filesystem) | Done | feat/storage-baseline |
| AF-0007 | P0 | Core runtime skeleton v0 (interfaces + playbook + stub skills) | Done | feat/runtime-skeleton |
| AF-0008 | P0 | CLI v0: ag run + runs show --json, truthful labels, manual gate | Done | feat/cli-v0 |
| AF-0009 | P1 | Artifact registry v0 + ag artifacts list | Done | feat/artifacts-v0 |

### Sprint Notes
- Sprint plan: [SPRINT_PLAN_SPRINT01.md](SPRINT_PLAN_SPRINT01.md)
- Sprint report: [SPRINT_REPORT_SPRINT01.md](SPRINT_REPORT_SPRINT01.md)
- Completion notes: [/docs/dev/backlog/completion/](../backlog/completion/)

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
3. **Sprint Notes** with links to plan, report, and completion notes
