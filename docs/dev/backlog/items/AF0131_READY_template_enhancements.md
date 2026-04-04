# AF-0131 — Template Enhancements: Time, Model, Docs Impact & Decision Capture
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
> - **During AF development:** no code changes — no targeted test run required
> - **Before commit (full gate):**
>   1. `ruff check src tests`
>   2. `ruff format --check src tests`
>   3. `pytest -W error`
>   4. `pytest --cov=src/ag --cov-report=term-missing`

---

## Metadata
- **ID:** AF-0131
- **Type:** Process
- **Status:** READY
- **Priority:** P1
- **Area:** Process / Docs
- **Owner:** Jacob
- **Target sprint:** Sprint 16 — governance_simplification
- **Phase:** 4 (no dependencies)

---

## Problem

Four gaps in the current template set:

1. **No timing data** — git timestamps miss context switches, offline discussions, and re-reads. There is no way to measure per-AF active implementation duration (the smallest measurable velocity unit).
2. **No model provenance** — which AI model worked on an AF is not recorded anywhere. Critical data for a system intended to be deployable with different AI models and for diagnosing failure modes.
3. **No docs impact gate** — no template field prompts the implementer to check whether README, ARCHITECTURE, or CLI_REFERENCE needs updating. This is the primary cause of documentation drift (README 3 phases stale, inventory docs 1 month stale at S16 start).
4. **No decision capture in AFs** — architectural decisions made inside an AF are lost unless a full ADR is written. Full ADRs are too heavyweight for single-AF-scope decisions.

---

## Goal

- Every AF, sprint, bug, and ADR records the AI model(s) involved and the timing boundaries
- `Started:` and `Completed:` capture actual work, not file creation time
- Every AF includes a mandatory Docs Impact Check (prevents drift)
- Every AF includes a conditional AI Functionality Check (catches LLM Avoidance)
- Architectural decisions made within a single AF scope are captured inline

---

## Non-goals

- Retroactively filling timestamps on S01–S15 AFs
- Changing any code in `src/`, `tests/`, or `scripts/`

---

## Acceptance Criteria
- [ ] `BACKLOG_ITEM_TEMPLATE.md` includes `Started:`, `Completed:`, `Models:` fields
- [ ] `SPRINT_DESCRIPTION_TEMPLATE.md` includes `Started:`, `Completed:`, `Models:` fields (coordinate with AF-0130 if running concurrently)
- [ ] `BUG_REPORT_TEMPLATE.md` includes `Models:` field
- [ ] `ADR_TEMPLATE.md` includes `Models:` field
- [ ] `BACKLOG_ITEM_TEMPLATE.md` includes Docs Impact Check as a standard acceptance criterion
- [ ] `BACKLOG_ITEM_TEMPLATE.md` includes AI Functionality Check (conditional — N/A if no AI functionality delivered)
- [ ] `BACKLOG_ITEM_TEMPLATE.md` includes Decision Record section (marked "if applicable")
- [ ] Format convention documented: ISO 8601 (e.g. `2026-04-04T14:30:00+02:00`)
- [ ] Model format: `<Model Name> (<Tool/Platform>)` — e.g. `Claude Opus 4 (Copilot)`
- [ ] `gov.py new-af` convention documented: `Started:` left blank; filled by agent when picking up the AF; `Completed:` filled when AC met, before commit
- [ ] Bug status vocabulary: `BUG_REPORT_TEMPLATE.md` updated to exactly 3 values (OPEN / FIXED / DROPPED); IN_PROGRESS and VERIFIED removed; `INDEX_BUGS.md` status legend updated (coordinate with AF-0134)
- [ ] Sprint `State:` → `Status:` renamed in `SPRINT_DESCRIPTION_TEMPLATE.md`; exactly 3 values (PLANNED / DONE / REJECTED); old values removed; `INDEX_SPRINTS.md` legend updated (coordinate with AF-0134)
- [ ] Docs impact checked: README / CLI_REFERENCE / ARCHITECTURE (updated or N/A)
- [ ] AI functionality check: N/A (no AI functionality)

---

## Implementation Notes

### New fields to add

**AF template (`BACKLOG_ITEM_TEMPLATE.md`) — header:**
```
# Started:
# Completed:
# Models:
```

**AF template — Acceptance Criteria block, append:**
```
- [ ] Docs impact checked: README / CLI_REFERENCE / ARCHITECTURE (updated or N/A)
- [ ] AI functionality check: if this AF delivers or modifies AI functionality (LLM calls, planner, orchestrator, verifier), RunTrace evidence of a real LLM call is required (N/A if no AI functionality)
```

**AF template — new section after Completion:**
```
## Decision Record (if applicable)
- **Decision:** What was decided?
- **Alternatives considered:** What else was possible?
- **Rationale:** Why this choice?
```

### Convention (must be documented in SPRINT_MANUAL or template header)

`gov.py new-af` leaves `Started:` blank. The agent fills it when it picks up that specific AF — not at file creation time. AF files may be created at sprint kickoff for the entire sprint scope. `Completed:` is filled when acceptance criteria are met, just before the commit. The `Started:`→`Completed:` span is the per-AF active implementation duration: the smallest measurable velocity unit in the system.

---

## Files Touched
- `docs/dev/backlog/templates/BACKLOG_ITEM_TEMPLATE.md`
- `docs/dev/sprints/templates/SPRINT_DESCRIPTION_TEMPLATE.md` (coordinate with AF-0130)
- `docs/dev/bugs/templates/BUG_REPORT_TEMPLATE.md`
- `docs/dev/decisions/templates/ADR_TEMPLATE.md`

---

## Risks

**Low.** Additive metadata fields and optional sections. No breaking changes. Existing AF files remain valid (new fields absent = pre-enhancement era).

---

## Completion

*(fill when Status = DONE)*
- **Review decision:**
- **Rationale:**
- **Follow-ups:**
- **PR link:**
