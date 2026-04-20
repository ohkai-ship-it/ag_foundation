# AF-0133 — Copilot Instructions: ToDo List Discipline
# Version number: v0.2
# Created: 2026-04-04
# Started: 2026-04-05T12:00:00+02:00
# Completed: 2026-04-05T12:15:00+02:00
# Status: DONE
# Priority: P1
# Area: Process / Tooling
# Models: Claude Opus 4 (Copilot)

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
- **ID:** AF-0133
- **Type:** Process / Tooling
- **Status:** DONE
- **Priority:** P1
- **Area:** Process / Tooling
- **Owner:** Jacob
- **Target sprint:** Sprint 16 — governance_simplification
- **Phase:** 6 (no dependencies)

---

## Problem

No standardized task tracking per AF during implementation. Copilot (GitHub Copilot / VS Code agent) creates ad hoc task lists without:
- Consistent AF ID in the checklist title (no traceability to which work item is being executed)
- Guaranteed per-AF granularity (tasks may span multiple AFs)
- Persistence across sessions (instructions reset with context)

Without persistent Copilot instructions, every new session risks the agent losing the discipline convention.

---

## Goal

- Every AF implementation gets a ToDo checklist with the AF ID clearly in the title
- This instruction is persistent via project-level Copilot configuration (`.github/copilot-instructions.md`)
- Validated across at least 2 consecutive AFs in the first sprint under new rules (Sprint 17)

---

## Non-goals

- Changing any code in `src/`, `tests/`, or `scripts/`
- Prescribing the content of ToDo items (agent determines those from AC)
- Configuring other Copilot behaviors beyond ToDo discipline (add incrementally)

---

## Acceptance Criteria
- [x] `.github/copilot-instructions.md` exists (create if absent, update if present)
- [x] File contains: ToDo list discipline rule with title format `AF-####: <AF Title>`
- [x] File contains: mark in-progress before starting, completed immediately after finishing
- [x] File contains: one active Todo at a time constraint
- [ ] Validated across at least 2 consecutive AFs in Sprint 17 (first sprint under new rules)
- [x] Docs impact checked: README / CLI_REFERENCE / ARCHITECTURE (updated or N/A)
- [x] AI functionality check: N/A (no AI functionality)

---

## Implementation Notes

### Minimum content for `.github/copilot-instructions.md`

```markdown
## ToDo List Discipline

For every AF being implemented, create a ToDo checklist with the AF ID in the title.

Title format: `AF-####: <AF Title>` — e.g. `AF-0129: Eliminate Filename-Status Coupling`

Rules:
- Mark one Todo in-progress before starting work on it
- Mark it completed immediately after finishing, before moving to the next
- Only one Todo in-progress at a time
- Derive Todo items from the AF acceptance criteria
```

If `.github/copilot-instructions.md` already exists, append this section without removing existing content.

---

## Files Touched
- `.github/copilot-instructions.md` (create or update)

---

## Risks

**Low.** Configuration file only. No impact on code, tests, or running system.

---

## Completion

- **Review decision:** Pending sprint review
- **Rationale:** `.github/copilot-instructions.md` created with ToDo discipline (title format, status tracking, one-at-a-time), testing workflow reference, and governance doc pointers. Validation across 2 AFs deferred to Sprint 17.
- **Follow-ups:** None
- **PR link:** (sprint PR at close)

### Docs Impact Check
- README: N/A
- CLI_REFERENCE: N/A
- ARCHITECTURE.md: N/A
