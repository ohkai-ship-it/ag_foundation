# Sprint Plan — Sprint 01 — Core runtime skeleton v0
# Version number: v0.3

## Metadata
- **Sprint:** Sprint 01 — Core runtime skeleton v0
- **Dates:** 2026-03-02 → 2026-03-15
- **Owner:** Kai (PM)
- **Tech lead:** Jeff
- **Implementer:** Jacob

## Sprint goal
Ship the minimal end-to-end runtime so `ag run "<prompt>"` produces a persisted `RunTrace` (truthful UX) in an isolated workspace.

## Sprint structure (no per-sprint folders)
- No per-sprint directories.
- Sprint tracking lives in: `/docs/dev/sprints/SPRINT_LOG.md`
- Engineer outputs (Jacob) live in: `/docs/dev/backlog/completion/` (canonical)

## Evidence & completion rules (Sprint-level)
- Each behavior PR must include:
  - Passing tests
  - At least one persisted RunTrace created by the PR
  - A completion note in `/docs/dev/backlog/completion/` with:
    - run_id(s)
    - how to reproduce
    - links to trace JSON files
- Captured traces may be stored as files under:
  - `/docs/dev/backlog/completion/<PR-or-AF>/run_<run_id>_trace.json`
  - (in addition to being persisted in the workspace runtime storage)

## Scope (what we intend to ship)
### Must-have (P0)
- AF-0004 — Sprint OS hygiene: sprint log + docs/dev pointers + handoff rules
- AF-0010 — Python project bootstrap (packaging + CLI stub + pytest + placeholder config structure)
- AF-0005 — Contracts: TaskSpec + RunTrace + Playbook schemas v0.1 + builders + contract tests
- AF-0006 — Workspace + storage baseline (sqlite + filesystem) with explicit isolation tests
- AF-0007 — Core runtime skeleton (interfaces + v0 playbook + stub skills) producing persisted RunTrace
- AF-0008 — CLI v0: `ag run`, `ag runs show --json`, truthful labels validated vs trace, manual dev gate

### Should-have (P1)
- AF-0009 — Artifact registry v0 + `ag artifacts list --run <run_id>` (minimal)

## Definition of Done (Sprint-level)
- [ ] All P0 items completed and merged (each via its own PR)
- [ ] Evidence captured per PR (tests + persisted RunTrace + completion note)
- [ ] Truthful UX validated by automated tests (CLI labels derived from RunTrace facts)
- [ ] Sprint log updated in `/docs/dev/sprints/SPRINT_LOG.md`

## PR plan (one PR ↔ one primary backlog item)
1. PR: AF-0004 — docs/dev pointers + sprint log + handoff rules (docs-only)
2. PR: AF-0010 — python bootstrap + CLI stub + pytest + placeholder config structure
3. PR: AF-0005 — schemas/builders/contract tests (TaskSpec/RunTrace/Playbook)
4. PR: AF-0006 — workspace + storage baseline + explicit isolation tests
5. PR: AF-0007 — interfaces + runtime skeleton + v0 playbook + stub skills + integration tests
6. PR: AF-0008 — CLI v0 + truthful label tests + manual dev gate tests
7. PR (optional): AF-0009 — artifact registry + CLI list command
