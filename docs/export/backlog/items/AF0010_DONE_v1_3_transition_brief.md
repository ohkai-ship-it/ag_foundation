# AF-0010 — v1.3 Transition Brief
# Version number: v0.1
# Created: 2026-04-05
# Started: 2026-04-05
# Completed: 2026-04-05
# Status: DONE
# Priority: P1
# Area: Process / Docs
# Models: Claude Opus 4

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> **CI workflow (CRITICAL):**
> - **During AF development:** no code changes; docs-only review
> - **Before commit (full gate):**
>   1. `ruff check src tests`
>   2. `ruff format --check src tests`
>   3. `pytest -W error`
>   4. `pytest --cov=src/ag --cov-report=term-missing`

---

## Metadata
- **ID:** AF-0010
- **Type:** Process / Docs
- **Status:** DONE
- **Priority:** P1
- **Area:** Process / Docs
- **Owner:** Jacob
- **Target sprint:** Sprint 01 — governance_simplification
- **Phase:** 7.5 (after AF-0006, before AF-0008)

---

## Problem

The v1.3 governance simplification changes naming conventions, INDEX layouts, and template structures. Without an explicit transition statement, implementers (human or agent) will reflexively attempt to normalize pre-v1.3 historical entries to the new format — causing cascading edits across dozens of files (AFs, bugs, sprint docs, INDEX tables) for no functional benefit, and violating the immutability of historical records.

This pattern has already been observed during Sprint 01 implementation.

---

## Goal

Add a short, tiered "v1.3 transition brief" across three locations so that the historical-immutability rule is unmissable:

1. **FOUNDATION_MANUAL** — Canonical definition (2–3 sentences)
2. **SPRINT_MANUAL §2** — One-sentence pointer to FOUNDATION_MANUAL
3. **INDEX files** — Single-line HTML comment in header metadata

Total new content: ~4 lines across all files. No duplication of logic — one source of truth with signposts.

---

## Non-goals

- Retroactively renaming or reformatting any historical entries
- Changing the v1.3 conventions themselves (that's AF-0001 through AF-0006)
- Documenting the full governance system (that's AF-0008)

---

## Acceptance Criteria
- [x] FOUNDATION_MANUAL contains a "Historical Record Immutability" statement (§7.7) with these elements:
  - Pre-v1.3 entries retain their original layout
  - Do not retroactively rename, restructure, or normalize historical records
  - New conventions apply from the sprint following their introduction
- [x] SPRINT_MANUAL §2 contains a one-sentence reference to the FOUNDATION_MANUAL immutability rule
- [x] Each governance INDEX file contains a single-line comment in its header block pointing to the FOUNDATION_MANUAL rule:
  - `docs/dev/backlog/INDEX_BACKLOG.md` ✔
  - `docs/dev/sprints/INDEX_SPRINTS.md` ✔
  - `docs/dev/bugs/INDEX_BUGS.md` ✔
  - `docs/dev/decisions/INDEX_DECISIONS.md` ✔
- [x] No historical entries were modified in the process
- [x] Docs impact checked: README / CLI_REFERENCE / ARCHITECTURE — N/A
- [x] AI functionality check: N/A (no AI functionality)

---

## Implementation Notes

### FOUNDATION_MANUAL placement
Add after the existing INDEX Discipline section (§7) or as a subsection within it. Suggested wording:

> **Historical Record Immutability.** Pre-v1.3 governance entries (INDEX rows, AF/BUG files, sprint docs) retain their original layout and naming conventions. Do not retroactively rename, restructure, or normalize historical records to match current conventions. New conventions take effect from the sprint following their introduction.

### SPRINT_MANUAL §2 placement
After the new naming convention documentation (which AF-0001/AF-0008 will add). One line:

> Historical files follow their original convention and must not be renamed (see FOUNDATION_MANUAL §X — Historical Record Immutability).

### INDEX files
Add as an HTML comment in the header block, after the version line:

```markdown
<!-- Pre-v1.3 entries retain their original layout — see FOUNDATION_MANUAL §X -->
```

---

## Completion

### Changes made
1. **FOUNDATION_MANUAL.md §7.7** — Added "Historical Record Immutability" subsection (3 sentences: pre-v1.3 entries retain original layout, no retroactive normalization, new conventions apply from next sprint).
2. **SPRINT_MANUAL.md §2** — Added one-sentence blockquote pointer after the "Both conventions coexist" paragraph, referencing FOUNDATION_MANUAL §7.7.
3. **INDEX_BACKLOG.md** — Added HTML comment after version line: `<!-- Pre-v1.3 entries retain their original layout — see FOUNDATION_MANUAL §7.7 -->`
4. **INDEX_BUGS.md** — Same HTML comment added.
5. **INDEX_DECISIONS.md** — Same HTML comment added.
6. **INDEX_SPRINTS.md** — Same HTML comment added.

### Test results
- `pytest tests/test_documentation_drift.py -W error` — 10/10 passed

### Verification
- Zero historical entries modified. Diff shows only header metadata additions and new subsection content.
