# AF0015 — Resolve storage DB filename mismatch (docs vs code): ag.db vs db.sqlite
# Version number: v0.2

## Metadata
- **ID:** AF-0015
- **Type:** Quality
- **Status:** DONE
- **Priority:** P2
- **Area:** Storage
- **Owner:** Jacob
- **Target sprint:** Sprint 09
- **Related:** AF0058 (overlapping scope, partially absorbed)

## Problem
Contract inventory describes workspace SQLite file as `ag.db`, while other docs/plans reference `db.sqlite`. This may be (a) docs mismatch, or (b) inconsistent naming across code paths.

## Goal
Standardize on a single canonical workspace DB filename and ensure all references (code, tests, docs) use the same constant/behavior.

## Non-goals
- Changing SQLite schema.
- Switching DB backend.
- Complex migration work (dev-only; optional backward-compat if trivial).

## Acceptance criteria (Definition of Done)
- [x] Audit: confirm actual filename(s) created on disk for at least two workspaces.
- [x] Choose canonical filename (prefer existing implementation unless strong reason).
- [x] Unify code to a single constant (e.g., `DB_FILENAME`) referenced everywhere.
- [x] Update docs (CONTRACT_INVENTORY, ARCHITECTURE, CLI_REFERENCE if needed) to match canonical filename.
- [x] Update tests to assert the canonical filename.
- [x] Optional: if trivial, accept both names with deprecation note. (N/A - no mismatch found)

## Implementation notes
- Search for hardcoded strings and unify.
- Add a test that creates a workspace and asserts DB file exists at expected path.

## Risks
Low: mainly naming; mitigate by updating tests and running full suite.

## PR plan
1. PR (chore/storage-db-filename): Audit + unify DB filename constant + update docs/tests.

---
# Completion section

## 1) Metadata
- **Backlog item (primary):** AF-0015
- **PR:** N/A (in sprint branch)
- **Author:** Jacob
- **Date:** 2026-03-11
- **Branch:** feat/sprint09-reliability-safety-hardening
- **Risk level:** P2
- **Runtime mode used for verification:** N/A (test verification)

## 2) Audit Findings

### Code Analysis
- **Canonical filename:** `db.sqlite`
- **Constant location:** `src/ag/storage/workspace.py` → `Workspace.DB_FILE = "db.sqlite"`
- **Usage:** `Workspace.db_path` property returns `self._path / self.DB_FILE`

### Documentation References
All current documentation consistently uses `db.sqlite`:
- `docs/dev/backlog/items/AF0006_Done_workspace_storage_baseline.md`
- `docs/dev/decisions/files/ADR006_PROPOSED_workspace_folder_structure.md`
- `docs/dev/backlog/items/AF0058_Done_workspace_folder_restructure.md`
- `docs/dev/backlog/items/AF0065_DONE_first_skill_set.md`

### Original Issue Status
The original issue claimed `ag.db` vs `db.sqlite` mismatch. Upon audit:
- **No `ag.db` references found** in current codebase or active docs
- Likely fixed during AF-0058 (workspace folder restructure)
- AF-0058 docs note: "AF0015 absorbed"

## 3) Test Added

```python
# tests/test_storage.py::TestWorkspace::test_db_filename_is_canonical
def test_db_filename_is_canonical(self, temp_root: Path) -> None:
    """Workspace uses canonical db.sqlite filename (AF-0015)."""
    ws = Workspace("test-ws", temp_root)
    ws.ensure_exists()

    # Verify the canonical filename constant
    assert ws.DB_FILE == "db.sqlite"

    # Verify db_path uses the canonical filename
    assert ws.db_path.name == "db.sqlite"
    assert ws.db_path == ws.path / "db.sqlite"
```

## 4) Resolution

**Status:** Issue no longer exists. The codebase is already consistent with `db.sqlite`.
- Added explicit test to prevent future drift
- Existing `test_sqlite_databases_separate` already exercises `db_path`

