# BACKLOG ITEM — AF0047 — Foundation Consolidation Refactor
# Version number: v0.2

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI discipline (ruff + pytest -W error + coverage)
> - 1 PR = 1 primary AF
> - INDEX update rule (status ↔ filename integrity)

> **File naming (required):** `AF####_<Status>_<three_word_description>.md`
> Status values: `Proposed | Ready | In progress | Blocked | Done | Dropped`

---

## Metadata
- **ID:** AF0047
- **Type:** Refactor
- **Status:** Done
- **Priority:** P0
- **Area:** Docs/Process
- **Owner:** Jacob
- **Target sprint:** Sprint05 — foundation_consolidation

---

## Problem
Foundation rules were fragmented across multiple documents:
- CODING_GUIDELINES.md
- ENGINEERING_GUIDELINES.md
- GITHUB_WORKFLOW.md
- REPO_HYGIENE.md

This created:
- Duplication and potential conflicts
- Unclear canonical source
- Sprint execution ambiguity

---

## Goal
1. Create single canonical operating manual: `FOUNDATION_MANUAL.md`
2. Create deterministic sprint execution playbook: `SPRINT_MANUAL.md`
3. Mark old docs as deprecated (not deleted)
4. Harden templates with foundation invariants box
5. Reinforce INDEX files with foundation rule notices
6. Update all references to old docs

---

## Non-goals
- Delete old foundation docs (retain for historical reference)
- Change any actual rules (consolidation only)
- Relax enforcement

---

## Acceptance criteria (Definition of Done)
- [x] FOUNDATION_MANUAL.md created with all rules from 4 deprecated docs
- [x] SPRINT_MANUAL.md created with deterministic execution steps
- [x] CODING_GUIDELINES.md marked deprecated
- [x] ENGINEERING_GUIDELINES.md marked deprecated
- [x] GITHUB_WORKFLOW.md marked deprecated
- [x] REPO_HYGIENE.md marked deprecated
- [x] BACKLOG_ITEM_TEMPLATE.md has foundation invariants box
- [x] BUG_REPORT_TEMPLATE.md has foundation invariants box
- [x] ADR_TEMPLATE.md has foundation invariants box
- [x] SPRINT_DESCRIPTION_TEMPLATE.md has foundation invariants box
- [x] PULL_REQUEST_TEMPLATE.md has foundation invariants box
- [x] INDEX_BACKLOG.md has foundation rule notice
- [x] INDEX_BUGS.md has foundation rule notice
- [x] INDEX_DECISIONS.md has foundation rule notice
- [x] INDEX_SPRINTS.md has foundation rule notice
- [x] PROCESS_GUIDELINES.md references new manual
- [x] TESTING_GUIDELINES.md references new manual
- [x] TEAM_GUIDELINES.md references new manual
- [x] Jacob onboarding prompt references updated
- [x] No rule missing from original 4 docs
- [x] No duplicate conflicting rules
- [x] INDEX files updated

---

## Implementation notes
**Phase A — Foundation Consolidation:**
- Created `/docs/dev/foundation/FOUNDATION_MANUAL.md` v1.0
- Organized by execution lifecycle, not original file grouping
- All invariants preserved with zero relaxation

**Phase B — Sprint Execution Playbook:**
- Created `/docs/dev/foundation/SPRINT_MANUAL.md` v1.0
- Deterministic step-by-step operational script
- Includes: pre-sprint, branch, file, index, implementation, evidence, PR, post-merge, close rituals

**Phase C — Template & Index Hardening:**
- Added Foundation Governance box to all 5 templates
- Added Foundation Rule notice to all 4 INDEX files
- Updated references in onboarding prompt and guideline docs

---

## Risks
- Risk: Missing rule during consolidation
  - Mitigation: Manual cross-check of all sections

- Risk: Broken references
  - Mitigation: grep search for old doc names, update all found

---

# Completion section (fill when done)

## 1) Metadata
- **Backlog item (primary):** AF0047
- **PR:** chore/foundation_consolidation
- **Author:** Jacob
- **Date:** 2026-03-04
- **Branch:** chore/foundation_consolidation
- **Risk level:** P1 (docs-only, no code changes)
- **Runtime mode used for verification:** N/A (docs-only)

---

## 2) Acceptance criteria verification
- [x] FOUNDATION_MANUAL.md created with all rules from 4 deprecated docs
- [x] SPRINT_MANUAL.md created with deterministic execution steps
- [x] CODING_GUIDELINES.md marked deprecated
- [x] ENGINEERING_GUIDELINES.md marked deprecated
- [x] GITHUB_WORKFLOW.md marked deprecated
- [x] REPO_HYGIENE.md marked deprecated
- [x] All 5 templates have foundation invariants box
- [x] All 4 INDEX files have foundation rule notice
- [x] Supporting docs reference new manual
- [x] No rule missing from original 4 docs
- [x] No duplicate conflicting rules
- [x] INDEX_BACKLOG.md updated with this AF

---

## 3) What changed (file-level)

### Created
- `docs/dev/foundation/FOUNDATION_MANUAL.md` — new canonical operating manual v1.0
- `docs/dev/foundation/SPRINT_MANUAL.md` — new deterministic execution playbook v1.0
- `docs/dev/backlog/items/AF0047_Done_foundation_consolidation.md` — this AF

### Modified (deprecated)
- `docs/dev/foundation/CODING_GUIDELINES.md` — added deprecation notice
- `docs/dev/foundation/ENGINEERING_GUIDELINES.md` — added deprecation notice
- `docs/dev/foundation/GITHUB_WORKFLOW.md` — added deprecation notice
- `docs/dev/foundation/REPO_HYGIENE.md` — added deprecation notice

### Modified (template hardening)
- `docs/dev/backlog/templates/BACKLOG_ITEM_TEMPLATE.md` — added foundation governance box
- `docs/dev/bugs/templates/BUG_REPORT_TEMPLATE.md` — added foundation governance box
- `docs/dev/decisions/templates/ADR_TEMPLATE.md` — added foundation governance box
- `docs/dev/sprints/templates/SPRINT_DESCRIPTION_TEMPLATE.md` — added foundation governance box
- `docs/dev/sprints/templates/PULL_REQUEST_TEMPLATE.md` — added foundation governance box

### Modified (INDEX reinforcement)
- `docs/dev/backlog/INDEX_BACKLOG.md` — added foundation rule notice + this AF entry
- `docs/dev/bugs/INDEX_BUGS.md` — added foundation rule notice
- `docs/dev/decisions/INDEX_DECISIONS.md` — added foundation rule notice
- `docs/dev/sprints/INDEX_SPRINTS.md` — added foundation rule notice

### Modified (reference updates)
- `docs/dev/foundation/PROCESS_GUIDELINES.md` — added reference to new manual/playbook
- `docs/dev/foundation/TESTING_GUIDELINES.md` — added reference to new manual
- `docs/dev/foundation/TEAM_GUIDELINES.md` — added reference to new manual
- `docs/dev/additional/prompts/kickoff_prompt_jacob_onboarding.md` — updated doc references

---

## 4) Architecture alignment (mandatory)
- **Layering:** Documentation only, no code changes
- **Interfaces touched:** None
- **Backward compatibility:** Yes — old docs retained with deprecation notice for historical reference

---

## 5) Truthful UX check (mandatory when user-visible)
- **User-visible labels affected:** None (docs-only change)
- **Trace fields backing them:** N/A
- **Proof:** N/A

---

## 6) Test evidence
This is a docs-only change. No code tests required.

CI validation:
- All existing tests continue to pass
- No coverage impact
