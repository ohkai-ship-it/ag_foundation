# SPRINT DESCRIPTION — Sprint11 — guided_autonomy_enablement
# Version number: v0.2

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
> `/docs/dev/foundation/SPRINT_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI discipline (ruff + pytest -W error + coverage)
> - 1 PR = 1 sprint
> - INDEX update rule (status ↔ filename integrity)

> **Folder naming (required):** `/docs/dev/sprints/documentation/Sprint11_guided_autonomy_enablement/`
> **Files (required):**
> - `S11_DESCRIPTION.md` (this file; includes plan + report)
> - `S11_REVIEW_01.md` (created after implementation)
> - `S11_PR_01.md` (PR checklist for sprint finalization)

---

## 1) Metadata
- **Sprint:** Sprint11
- **Name:** guided_autonomy_enablement
- **Dates:** 2026-03-20 → 2026-03-21
- **Owner (PM):** Kai
- **Tech lead:** Jeff
- **Implementer:** Jacob
- **State:** Closed
- **Branch:** `feat/sprint11-guided-autonomy`

---

## 2) Sprint goal

Enable guided autonomy mode where users can preview, approve, and control
agent execution plans. This is the first step beyond playbook-driven autonomy
on the autonomy spectrum:

```
Playbook → [Guided Agent] → Goals Only → Full Agent
           ^^^^^^^^^^^^^^
           THIS SPRINT
```

Key capabilities:
1. **LLM-based planner** that composes execution plans from available skills
2. Plan preview before execution (`ag plan`)
3. Plan approval workflow (`ag run --plan`)
4. Step-level confirmation for high-impact actions
5. Autonomy mode visibility in CLI and trace

---

## 3) Scope (what we intend to ship)

### Track 1: LLM Planner + Plan Workflow (P1 — core autonomy)
| Order | ID | Priority | Status | Title | Owner |
|:--:|---|:--:|:--|---|---|
| 1 | AF-0102 | P1 | ✅ DONE | LLM Planner V1 (skills) | Jacob |
| 2 | AF-0098 | P1 | ✅ DONE | Plan preview command | Jacob |
| 3 | AF-0099 | P1 | ✅ DONE | Plan approval workflow | Jacob |
| 4 | AF-0100 | P1 | ✅ DONE | Step confirmation hooks | Jacob |

### Track 2: Observability for Autonomy (P2 — audit support)
| Order | ID | Priority | Status | Title | Owner |
|:--:|---|:--:|:--|---|---|
| 5 | AF-0094 | P2 | ✅ DONE | Trace full I/O enrichment | Jacob |
| 6 | BUG-0015 | P2 | ✅ FIXED | Runs list count mismatch fix | Jacob |

### Track 3: UX Polish (P3 — quality of life)
| Order | ID | Priority | Status | Title | Owner |
|:--:|---|:--:|:--|---|---|
| 7 | AF-0097 | P3 | ✅ DONE | runs commands default workspace | Jacob |
| 8 | AF-0101 | P3 | ✅ DONE | Autonomy level display | Jacob |

### Bundled bug fixes
| Bug | Addressed by |
|-----|-------------|
| BUG-0015 | Standalone (runs list count fix) |

---

## 4) Sprint start checklist (ritual)

### Kai (PM)
- [x] Create sprint description file
- [x] Update INDEX_SPRINTS to Active
- [x] Update INDEX_BACKLOG with Sprint 11 scope table
- [x] Verify OPEN bugs triaged and linked
- [x] Mark all AFs as READY before proceeding

### Jacob (implementer)
- [x] Read sprint description
- [x] Review AF items in scope
- [x] Confirm scope feasibility
- [x] Create feature branch: `feat/sprint11-guided-autonomy`

---

## 5) Dependencies and ordering

```
AF-0102 (V1 Planner) ────> AF-0098 (plan preview) ────> AF-0099 (plan approval)
        │                                                       │
        │                                ───────────────────────┘
        │                               │
        └───────────────> AF-0100 (confirmation) ───> AF-0101 (autonomy display)

Track 2 (AF-0094, BUG-0015) ─── parallel with Track 1
Track 3 (AF-0097) ─── parallel with all
```

- **AF-0102 is the core**: V1Planner uses LLM to compose skill sequences
- AF-0098 depends on AF-0102 (plan preview needs a planner to generate plans)
- AF-0099 depends on AF-0098 (can't approve plans without generating them)
- AF-0100 uses planner output to identify policy-flagged steps
- AF-0101 depends on AF-0098/0099/0100 concepts but not implementation
- Tracks 2 and 3 are fully independent

---

## 6) Exit criteria

1. `ag plan --task "..." --workspace <ws>` generates reviewable plan
2. `ag plan show <id>` displays plan details
3. `ag plans list --workspace <ws>` shows pending plans
4. `ag run --plan <id>` executes approved plan
5. Step confirmation policy configurable per workspace
6. Interactive confirmation prompts for flagged steps
7. `--yes` flag bypasses all confirmations
8. Trace records full step I/O (AF-0094)
9. `ag runs list` count matches actual runs (BUG-0015)
10. Autonomy mode visible in CLI and trace (AF-0101)
11. `ruff check src tests` clean
12. `pytest -W error` passes
13. ADR009 documents guided autonomy boundaries (if created)

---

## 7) Autonomy Gate assessment

Sprint 11 advances from Gate B (Guided Autonomy ready) to operating IN
guided autonomy mode.

| Capability | Status | Evidence |
|------------|--------|----------|
| Plan preview | ✅ Shipped | AF-0098 `ag plan generate/show/list/delete` |
| Plan approval | ✅ Shipped | AF-0099 `ag run --plan <id>` |
| Confirmation hooks | ✅ Shipped | AF-0100 policy flags + prompts |
| Trace completeness | ✅ Shipped | AF-0094 full I/O enrichment |
| Truthful UX | ✅ Maintained | BUG-0015 count fix, AF-0101 mode display |

---

## 8) Risk register

| Risk | Impact | Mitigation |
|------|--------|------------|
| Plan storage complexity | Medium | Start simple (JSON files), iterate |
| Confirmation UX friction | Medium | Provide `--yes`, `[A]ll` options |
| Scope creep to goals-only | High | Explicit ADR boundaries |
| Token estimation inaccuracy | Low | Label as "estimated", track over time |

---

## 9) Report (filled at sprint close)

### What shipped
All 8 scope items shipped successfully:

**Track 1 — LLM Planner + Plan Workflow (P1)**
- ✅ AF-0102: V1Planner with LLM skill composition (19 tests)
- ✅ AF-0098: `ag plan generate/show/list/delete` commands
- ✅ AF-0099: `ag run --plan <id>` approval workflow
- ✅ AF-0100: Step confirmation hooks with policy flags (16 tests)

**Track 2 — Observability (P2)**
- ✅ AF-0094: Full step I/O in trace (19 tests)
- ✅ BUG-0015: Runs list count fix

**Track 3 — UX Polish (P3)**
- ✅ AF-0097: Default workspace for runs commands
- ✅ AF-0101: Autonomy mode in CLI output

**Evidence:**
- `pytest -W error`: 676 tests passing
- `ruff check src tests`: Clean
- Coverage: 89%
- Review artifacts: `artifacts/review_S11_01/` (10 evidence files)

### What didn't ship
All scope items shipped. No deferrals.

### Lessons learned
1. **Backlog integrity matters**: Review Pass 0.5 discovered 5 filename/status mismatches that needed correction before sprint close.
2. **Test isolation pays off**: Confirmation hooks and planner tests needed careful mocking to avoid real LLM calls.
3. **CLI contract traceability**: Documenting `ag plan` commands in CLI_REFERENCE.md during implementation prevented documentation drift.
4. **Evidence capture discipline**: Creating artifacts during review passes provides clear audit trail.

---

## 10) PR plan
| PR | Primary AF | Branch | Status |
|--|--|--|--|
| PR-01 | Sprint 11 scope | feat/sprint11-guided-autonomy | Ready for merge |
