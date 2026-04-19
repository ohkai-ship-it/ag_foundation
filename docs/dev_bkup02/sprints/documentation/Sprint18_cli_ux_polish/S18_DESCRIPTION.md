# S18_DESCRIPTION — Sprint18 — cli_ux_polish
# Convergent version: v1.3.1
# Status: DONE

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
> - INDEX update rule

> **Folder naming (required):** `/docs/dev/sprints/documentation/Sprint18_cli_ux_polish/`
> **Files (required):**
> - `S18_DESCRIPTION.md` (this file — planning artifact, stable during sprint)
> - `S18_REVIEW.md` (outcomes artifact, written at sprint close)

> **NOTE:** This is the first code sprint executing under GVS v1.3.1 rules.
> It is an intentionally lightweight sprint — CLI polish features — to validate the v1.3.1 governance cycle (HITL gates, commit discipline, sprint close) on real code changes.

---

## 1) Metadata
- **Sprint:** Sprint18
- **Name:** cli_ux_polish
- **Dates:** TBD → TBD
- **Branch:** feat/sprint18-cli-ux-polish
- **Owner (PM):** Kai
- **Tech lead:** Jeff
- **Implementer:** Jacob
- **Status:** DONE
- **Models:**
- **Started:** 2026-04-06
- **Completed:** 2026-04-06

---

## 2) Sprint goal

Deliver 3 small, independent CLI improvements. Each item is independently testable and touches a different CLI command area. This sprint validates v1.3.1 governance on real code changes before tackling heavier feature work (skill_catalog_expansion).

---

## 3) Scope (what we intend to ship)

### Must-have (P2 — all items equal priority)

| Order | ID | Title | Area | Owner |
|:--:|---:|---|---|---|
| 1 | AF-0147 | `ag playbooks show` command | CLI / Playbooks | Jacob |
| 2 | AF-0144 | `ag runs list` filter expansion | CLI / UX | Jacob |
| 3 | AF-0145 | `ag doctor` diagnostic expansion | CLI / Diagnostics | Jacob |

> **Removed during planning review (2026-04-06):**
> - AF-0146 (`artifacts list --category`): Deferred — needs category taxonomy + trace/storage design first.
> - BUG-0011 (workspace name leak): Dropped as bug → replaced by AF-0148 (workspace isolation design), a conceptual AF to address cross-workspace leakage holistically.

---

## 4) Execution sequence

All 3 items are **independent** — no ordering constraints, no cross-AF dependencies. Each touches `cli/main.py` but in different functions, so merge conflicts are unlikely.

Recommended order (easiest-first for governance warm-up):
1. **AF-0147** — Implement `playbooks show` (currently a stub → fill in)
2. **AF-0144** — Add filters to `runs list` (extend existing function)
3. **AF-0145** — Expand `doctor` checks (additive, least impactful)

---

## 5) Sprint start checklist (ritual)

### Jeff + Kai
- [x] Create AFs (Status = READY)
- [x] Create this sprint description file
- [x] Define sprint ID + sprint name

### Jacob
- [ ] Read this sprint description
- [ ] Read all 3 AF files (AF-0147, AF-0144, AF-0145)
- [ ] Ask clarifying questions in chat (no writing required)
- [ ] Create branch: `feat/sprint18-cli-ux-polish`
- [ ] Update INDEX files (ritual at sprint start):
  - `/docs/dev/backlog/INDEX_BACKLOG.md`
  - `/docs/dev/bugs/INDEX_BUGS.md`
  - `/docs/dev/decisions/INDEX_DECISIONS.md`
  - `/docs/dev/sprints/INDEX_SPRINTS.md` (Sprint 18 → In Progress)
- [ ] Confirm with Kai before starting implementation (G1 + G3)

> **INDEX update rule (strict):**
> 1) Update when any AF/BUG/ADR/SPRINT status changes
> 2) Also update as a ritual at sprint start

---

## 6) PR plan

> Rule: **1 commit per AF, 1 PR per sprint.**
> All AFs are committed separately to the sprint branch. The branch is merged to main via one PR at sprint close.

- Branch: `feat/sprint18-cli-ux-polish`
- Commit plan (in execution order):
  - AF-0147 — `ag playbooks show` command
  - AF-0144 — `ag runs list` filter expansion
  - AF-0145 — `ag doctor` diagnostic expansion

---

## 7) Definition of Done (Sprint-level)
- [ ] All P0 items merged and CI passes
- [ ] All shipped AFs have completion sections filled
- [ ] Review completed (`S18_REVIEW.md` filled, decision recorded)
- [ ] Repo hygiene executed
- [ ] INDEX files updated and consistent

---

## 8) Risks & mitigations
- Risk: First code sprint under v1.3.1 — governance overhead unknown
  - Mitigation: Intentionally lightweight scope (3 AFs) to focus on process validation
- Risk: All 3 AFs touch `cli/main.py`
  - Mitigation: Each AF targets a different function — no merge conflicts expected

---

## 9) Dependencies
- Internal: None — all 3 AFs are independent
- External: None

---

## 10) Testing strategy

- **During each AF:** run only the targeted test file
  - AF-0144, AF-0145, AF-0147: `pytest tests/test_cli.py -x -q`
- **Full gate (before each commit):**
  1. `ruff check src tests`
  2. `ruff format --check src tests`
  3. `pytest -W error`
  4. `pytest --cov=src/ag --cov-report=term-missing`
- **Coverage target:** `cli/main.py` should improve from 72% baseline

---

## 11) Success criteria

1. All 3 AFs complete (DONE)
2. Full test suite passes: `pytest -W error`
3. No coverage regressions; `cli/main.py` coverage ≥ 75%
4. v1.3.1 governance cycle validated: HITL gates fired correctly, commit discipline held
5. Sprint closes cleanly: INDEX files consistent, review written
