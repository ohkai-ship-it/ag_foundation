# AF-0136 — Governance Docs Consolidation
# Version number: v0.2
# Created: 2026-04-04
# Started:
# Completed:
# Status: READY
# Priority: P1
# Area: Process / Docs
# Models:

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> **CI workflow (CRITICAL):**
> - **During AF development:** run targeted tests only
>   `pytest tests/test_documentation_drift.py -W error`
> - **Before commit (full gate):**
>   1. `ruff check src tests`
>   2. `ruff format --check src tests`
>   3. `pytest -W error`
>   4. `pytest --cov=src/ag --cov-report=term-missing`

---

## Metadata
- **ID:** AF-0136
- **Type:** Process / Docs
- **Status:** READY
- **Priority:** P1
- **Area:** Process / Docs
- **Owner:** Jacob
- **Target sprint:** Sprint 16 — governance_simplification
- **Phase:** 8 (depends on all above: AF-0129 through AF-0135)

---

## Problem

After Phases 1–7, the governance docs (SPRINT_MANUAL, FOUNDATION_MANUAL, FOLDER_STRUCTURE, README, ARCHITECTURE) still reference old conventions. Without a consolidation pass, the new rules exist in templates and AF files but not in the authoritative human-facing documentation. Additionally, there is no ADR recording the governance simplification decision itself. All governance INDEX files and templates still carry disparate version numbers (INDEX_BACKLOG v1.2, INDEX_SPRINTS v0.5, templates v0.2) — after this AF they should all carry Governance System Version v1.3.

---

## Goal

- All governance docs internally consistent with new rules
- ADR-0010 records the governance simplification decision for traceability
- README reflects actual project state
- FOLDER_STRUCTURE_0.3 documents the current (simplified) folder layout
- Sprint Cognitive Health convention in SPRINT_MANUAL §8
- ADR creation criteria formalized (inline vs. full ADR)
- Inter-sprint planning commits convention documented
- **All governance INDEX files and templates bumped to Governance System Version v1.3**

---

## Non-goals

- Changes to `src/`, `tests/`, or `scripts/gov.py` (that's AF-0135)
- Touching S01–S15 historical sprint folders
- Genericizing for deployable template kit (deferred)

---

## Acceptance Criteria
- [ ] SPRINT_MANUAL §2: New file naming convention documented; no references to old AF/BUG status-in-filename convention for new files
- [ ] SPRINT_MANUAL §6: GitHub PR as canonical artifact; no S##_PR_01 creation steps
- [ ] SPRINT_MANUAL §7: No post-merge rename step for new-convention files
- [ ] SPRINT_MANUAL §8: Review decision rules (ACCEPTED / ACCEPT WITH FOLLOW-UPS / REJECTED) with consequences
- [ ] SPRINT_MANUAL §8: Living reference docs sweep checklist (6 docs, conditional)
- [ ] SPRINT_MANUAL §8: Sprint Cognitive Health close ritual (7 fields)
- [ ] SPRINT_MANUAL §8: ADR creation criteria (inline Decision Record vs. full ADR)
- [ ] SPRINT_MANUAL new section §X: Inter-sprint planning commits convention
- [ ] SPRINT_MANUAL references HITL Framework (AF-0132) at all relevant decision points
- [ ] `FOLDER_STRUCTURE_0.3.md` exists; documents current folder layout including both filename conventions
- [ ] ADR-0010 exists in `docs/dev/decisions/files/` with ACCEPTED status
- [ ] INDEX_DECISIONS updated with ADR-0010 row
- [ ] README project structure, test count, and coverage reflect current state
- [ ] ARCHITECTURE.md Implementation Map verified current (update if stale)
- [ ] **All governance INDEX files carry version v1.3:**
  - `docs/dev/backlog/INDEX_BACKLOG.md`
  - `docs/dev/sprints/INDEX_SPRINTS.md`
  - `docs/dev/bugs/INDEX_BUGS.md`
  - `docs/dev/decisions/INDEX_DECISIONS.md`
- [ ] **All template files carry version v1.3:**
  - `docs/dev/backlog/templates/BACKLOG_ITEM_TEMPLATE.md`
  - `docs/dev/sprints/templates/SPRINT_DESCRIPTION_TEMPLATE.md`
  - `docs/dev/bugs/templates/BUG_REPORT_TEMPLATE.md`
  - `docs/dev/decisions/templates/ADR_TEMPLATE.md`
- [ ] `pytest tests/test_documentation_drift.py -W error` passes
- [ ] Docs impact checked: README / CLI_REFERENCE / ARCHITECTURE (updated or N/A)
- [ ] AI functionality check: N/A (no AI functionality)

---

## Implementation Notes

### SPRINT_MANUAL sections to rewrite

1. **§0/intro**: Add HITL cross-reference
2. **§2**: Remove file-rename protocol; add new naming convention; note legacy files
3. **§3**: Simplify INDEX update protocol (2 places: file metadata + INDEX row; no rename)
4. **§6**: Simplify PR protocol (GitHub PR only, no S##_PR_01)
5. **§7**: Post-merge — no rename step; status update only
6. **§8**: Full rewrite — review decisions, quickfix budget, cognitive health close ritual, living reference sweep, ADR creation criteria
7. **new §X**: Inter-sprint planning commits — housekeeping branch + minimal PR, docs-only scope, merge before next sprint starts

### FOLDER_STRUCTURE_0.3.md

New file. Documents:
- Current sprint folder: `S##/S##_DESCRIPTION.md` + `artifacts/` (no PR/review docs)
- Two filename conventions: legacy (with status token) and new (without)
- `scripts/gov.py` location
- `docs/dev/*/templates/archived/` for deprecated templates

### ADR-0010 — Governance Simplification

Minimal content:
- **Context:** 15 sprints of data; ceremony overhead 30–50 min/sprint; see GOVERNANCE_SIMPLIFICATION_PLAN_0.1.md
- **Decision:** Eliminate filename-status coupling; drop PR/review docs; add HITL framework; add time/model logging; introduce gov.py; unify Governance System Version
- **Status:** ACCEPTED
- **Consequences:** ~10 min/sprint ceremony target; new GSV v1.3 convention; gov.py as optional automation

### Governance System Version bump

Set `# Version number: v1.3` in header of:
- `docs/dev/backlog/INDEX_BACKLOG.md` (was v1.2)
- `docs/dev/sprints/INDEX_SPRINTS.md` (was v0.5)
- `docs/dev/bugs/INDEX_BUGS.md`
- `docs/dev/decisions/INDEX_DECISIONS.md`
- `docs/dev/backlog/templates/BACKLOG_ITEM_TEMPLATE.md` (was v0.2)
- `docs/dev/sprints/templates/SPRINT_DESCRIPTION_TEMPLATE.md` (was v0.2)
- `docs/dev/bugs/templates/BUG_REPORT_TEMPLATE.md` (was v0.2)
- `docs/dev/decisions/templates/ADR_TEMPLATE.md` (was v0.2)

All Sprint 16 AF files (AF0129–AF0136) were created with v0.2 and may be bumped to v1.3 as part of this AF.

---

## Files Touched
- `docs/dev/foundation/SPRINT_MANUAL.md` (rewrite affected sections)
- `docs/dev/foundation/FOLDER_STRUCTURE_0.3.md` (new file)
- `docs/dev/decisions/files/ADR010_governance_simplification.md` (new file)
- `docs/dev/decisions/INDEX_DECISIONS.md` (add ADR-0010 row + bump to v1.3)
- `docs/dev/backlog/INDEX_BACKLOG.md` (bump to v1.3)
- `docs/dev/sprints/INDEX_SPRINTS.md` (bump to v1.3)
- `docs/dev/bugs/INDEX_BUGS.md` (bump to v1.3)
- All template files under `docs/dev/*/templates/` (bump to v1.3)
- Sprint 16 AF files AF0129–AF0136 (bump to v1.3)
- `README.md` (update project structure, test count, coverage)
- `ARCHITECTURE.md` (verify and update Implementation Map)

---

## Risks

**Low.** Documentation-only. Validated by full read-through and `test_documentation_drift.py`. Do not commit until `gov.py check` passes.

---

## Decision Record (if applicable)

- **Decision:** Governance System Version (GSV) v1.3 assigned to all governance docs after S16.
- **Alternatives considered:** Keep per-file versioning (INDEX had v1.2, templates v0.2, etc.).
- **Rationale:** A single GSV number tells any reader which governance generation is in effect. Disparate version numbers made it impossible to know if a template and an INDEX were from the same governance generation. After this AF, v1.3 is the answer to "what governance system is running?" See D10 and D20 in GOVERNANCE_SIMPLIFICATION_PLAN_0.1.md.

---

## Completion

*(fill when Status = DONE)*
- **Review decision:**
- **Rationale:**
- **Follow-ups:**
- **PR link:**
