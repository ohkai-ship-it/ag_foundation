# SPRINT DESCRIPTION — Sprint11 — guided_autonomy_enablement
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
> `/docs/dev/foundation/SPRINT_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI discipline (ruff + pytest -W error + coverage)
> - 1 PR = 1 primary AF
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
- **Dates:** 2026-03-13 → TBD
- **Owner (PM):** Kai
- **Tech lead:** Jeff
- **Implementer:** Jacob
- **State:** Planning

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
1. Plan preview before execution (`ag plan`)
2. Plan approval workflow (`ag run --plan`)
3. Step-level confirmation for high-impact actions
4. Autonomy mode visibility in CLI and trace

---

## 3) Scope (what we intend to ship)

### Track 1: Planner Suggestion Mode (P1 — core autonomy)
| Order | ID | Priority | Status | Title | Owner |
|:--:|---|:--:|:--|---|---|
| 1 | AF-0098 | P1 | PROPOSED | Plan preview command | TBD |
| 2 | AF-0099 | P1 | PROPOSED | Plan approval workflow | TBD |
| 3 | AF-0100 | P1 | PROPOSED | Step confirmation hooks | TBD |

### Track 2: Observability for Autonomy (P2 — audit support)
| Order | ID | Priority | Status | Title | Owner |
|:--:|---|:--:|:--|---|---|
| 4 | AF-0094 | P2 | PROPOSED | Trace full I/O enrichment | TBD |
| 5 | BUG-0015 | P2 | OPEN | Runs list count mismatch fix | TBD |

### Track 3: UX Polish (P3 — quality of life)
| Order | ID | Priority | Status | Title | Owner |
|:--:|---|:--:|:--|---|---|
| 6 | AF-0097 | P3 | PROPOSED | runs commands default workspace | TBD |
| 7 | AF-0101 | P3 | PROPOSED | Autonomy level display | TBD |

### Bundled bug fixes
| Bug | Addressed by |
|-----|-------------|
| BUG-0015 | Standalone (runs list count fix) |

---

## 4) Sprint start checklist (ritual)

### Kai (PM)
- [x] Create sprint description file
- [ ] Update INDEX_SPRINTS to Active
- [x] Update INDEX_BACKLOG with Sprint 11 scope table
- [ ] Verify OPEN bugs triaged and linked
- [ ] Mark all AFs as READY before proceeding

### Jacob (implementer)
- [ ] Read sprint description
- [ ] Review AF items in scope
- [ ] Confirm scope feasibility
- [ ] Create feature branch: `feat/sprint11-guided-autonomy`

---

## 5) Dependencies and ordering

```
AF-0098 (plan preview) ────────> AF-0099 (plan approval)
                                        │
                         ───────────────┘
                        │
AF-0100 (confirmation) ─┴─> AF-0101 (autonomy display)

Track 2 (AF-0094, BUG-0015) ─── parallel with Track 1
Track 3 (AF-0097) ─── parallel with all
```

- AF-0099 depends on AF-0098 (can't approve plans without generating them)
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
| Plan preview | Target | AF-0098 |
| Plan approval | Target | AF-0099 |
| Confirmation hooks | Target | AF-0100 |
| Trace completeness | Target | AF-0094 |
| Truthful UX | Maintained | BUG-0015 fix |

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
_To be filled at sprint close_

### What didn't ship
_To be filled at sprint close_

### Lessons learned
_To be filled at sprint close_

---

## 10) PR plan
| PR | Primary AF | Branch | Status |
|--|--|--|--|
| PR-01 | Sprint 11 scope | feat/sprint11-guided-autonomy | Not started |
