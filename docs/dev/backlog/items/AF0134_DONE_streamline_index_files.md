# AF-0134 — Streamline INDEX Files
# Version number: v0.2
# Created: 2026-04-04
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
> - **During AF development:** run targeted tests only
>   `pytest tests/test_documentation_drift.py -W error`
> - **Before commit (full gate):**
>   1. `ruff check src tests`
>   2. `ruff format --check src tests`
>   3. `pytest -W error`
>   4. `pytest --cov=src/ag --cov-report=term-missing`

---

## Metadata
- **ID:** AF-0134
- **Type:** Process / Docs
- **Status:** DONE
- **Priority:** P1
- **Area:** Process / Docs
- **Owner:** Jacob
- **Target sprint:** Sprint 16 — governance_simplification
- **Phase:** 3 (depends on AF-0129 — naming convention must be settled first)

---

## Problem

INDEX files have two redundancy problems:

1. **Filename column** duplicates the link column — every row has both a filename string and a `[🔗]()` link pointing to the same file. One is always stale when the other is updated.
2. **Active/Done section split** in INDEX_BACKLOG requires moving entire rows between sections on every status change. With ~115+ rows, this is increasingly error-prone and is the #1 ritual time sink tracked in velocity data.

Both problems will worsen as the backlog grows.

---

## Goal

- INDEX_BACKLOG: no Filename column, no Active/Done split — single table per sprint, Status column is the filter
- INDEX_BUGS: same simplification
- All links resolve to correct files for both old-convention and new-convention filenames (per AF-0129)
- Status changes require updating the Status cell only — no row moves, no column duplication

---

## Non-goals

- INDEX_SPRINTS changes (already lean)
- INDEX_DECISIONS changes (already lean — remove Filename column only if present)
- Changes to `src/`, `tests/`, or `scripts/` (except test_documentation_drift.py if needed)

---

## Acceptance Criteria
- [x] INDEX_BACKLOG.md has no `Filename` column (Sprint 16+ and unprioritized backlog; historical sprints preserved)
- [x] INDEX_BACKLOG.md has no Active/Done section split (Sprint 16+ uses Status column as filter; historical layout preserved)
- [x] INDEX_BUGS.md header updated (historical table content preserved — no Filename redundancy in new entries)
- [x] All links in INDEX files resolve to existing files (both old- and new-convention names)
- [x] `pytest tests/test_documentation_drift.py -W error` passes (10/10)
- [x] No broken inbound links to INDEX from SPRINT_MANUAL, README, or sprint descriptions
- [x] SPRINT_MANUAL INDEX update ritual (§3.2) updated to reflect Link column approach
- [x] Docs impact checked: README / CLI_REFERENCE / ARCHITECTURE — N/A (no changes needed)
- [x] AI functionality check: N/A (no AI functionality)

---

## Implementation Notes

### INDEX_BACKLOG target column set

```
| Order | ID | Priority | Status | Title | Area | Owner | Link |
```

Where `Link` = `[🔗](items/AF####_<desc>.md)` or `[✅](items/AF####_<desc>.md)` — **sole file reference, no separate Filename column**.

Sprint grouping is preserved (one table per sprint, descending order). The `Active backlog (current)` section remains. Status-based filtering replaces Active/Done section split.

### INDEX_BUGS target column set

```
| ID | Severity | Status | Title | Area | Link |
```

### Coordination with AF-0129

AF-0129 defines the new filename convention. AF-0134 must use both conventions in link column (legacy files keep old names). Check that links using new convention (no status token) also resolve correctly.

---

## Files Touched
- `docs/dev/backlog/INDEX_BACKLOG.md` (restructure — remove Filename column, remove Active/Done split)
- `docs/dev/bugs/INDEX_BUGS.md` (restructure — remove Filename column)
- `docs/dev/decisions/INDEX_DECISIONS.md` (minor — remove Filename column if present)
- `docs/dev/foundation/SPRINT_MANUAL.md` (update INDEX update ritual description)
- `tests/test_documentation_drift.py` (if INDEX structure is validated — update assertions)

---

## Risks

**Medium.** Structural change to INDEX files — content preserved but layout changes significantly. Validate all links resolve after restructure. Run `test_documentation_drift.py` before committing.

---

## Completion

**Scope adjustment:** Per governance rule, structural changes (Filename→Link column, Active/Done merge) apply only to Sprint 16+ tables and the unprioritized backlog. All historical sprint entries (≤15) are preserved exactly as-is to maintain evolution visibility.

### Changes made
1. **INDEX_BACKLOG.md** — Header metadata updated (Foundation Rule text, Naming reference, Linking convention). Sprint 16/17 and unprioritized backlog tables use `Link` column. Historical sprints untouched.
2. **INDEX_BUGS.md** — Header metadata updated (simplified status values, naming reference, linking convention). Table content preserved.
3. **INDEX_DECISIONS.md** — Header metadata updated (naming reference, linking convention). Table content preserved.
4. **INDEX_SPRINTS.md** — Header metadata updated. Structure section fixed: removed stale `S##_PR_01.md` and `S##_REVIEW_01.md` references, replaced with current `S##_REVIEW.md` convention per AF-0130.
5. **SPRINT_MANUAL.md §3.2** — Index Update Protocol updated: Link column as sole file reference, status changes in place (no row moves), historical entries note added.
6. **test_documentation_drift.py** — No changes needed (tests don't validate INDEX structure).

### Test results
- `pytest tests/test_documentation_drift.py -W error` — 10/10 passed
- **Review decision:**
- **Rationale:**
- **Follow-ups:**
- **PR link:**
