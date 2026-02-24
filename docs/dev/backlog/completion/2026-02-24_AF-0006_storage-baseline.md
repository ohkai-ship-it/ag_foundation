# Handoff Note — AF-0006 — Workspace + Storage Baseline
**Date:** 2026-02-24
**Author:** Jacob (Junior Engineer)
**Status:** Ready for review

---

## Summary
Implemented workspace-scoped storage with SQLite indices and filesystem-based JSON traces/artifacts, including explicit isolation tests.

## What Was Done

### 1. Workspace Directory Layout (`src/ag/storage/workspace.py`)
- `Workspace` class manages per-workspace directories
- Directory structure: `{root}/{workspace_id}/runs/`, `artifacts/`, `db.sqlite`
- Automatic directory creation on demand
- Path safety validation (`_validate_safe_path_component()`) prevents path traversal

### 2. Storage Interfaces (`src/ag/storage/interfaces.py`)
- `RunStore` protocol: `save()`, `get()`, `list()`, `delete()`
- `ArtifactStore` protocol: `save()`, `get()`, `list()`, `delete()`
- All operations scoped by `workspace_id`

### 3. SQLite Implementation (`src/ag/storage/sqlite_store.py`)
- `SQLiteRunStore`: Persists RunTrace JSON to filesystem, indexes in SQLite
- `SQLiteArtifactStore`: Stores artifact content on filesystem, indexes in SQLite
- Schema includes: `runs`, `artifacts`, `schema_version` tables
- Per-workspace database files (no cross-workspace access)

### 4. Package Exports (`src/ag/storage/__init__.py`)
- Exports: `Workspace`, `RunStore`, `ArtifactStore`, `SQLiteRunStore`, `SQLiteArtifactStore`

### 5. Test Suite (`tests/test_storage.py`)
19 tests covering:
- Workspace directory creation and path safety
- RunStore CRUD operations
- ArtifactStore CRUD operations
- **6 explicit isolation tests:**
  - `test_isolation_workspaces_separate_directories`
  - `test_isolation_runs_not_visible_across_workspaces`
  - `test_isolation_artifacts_not_visible_across_workspaces`
  - `test_isolation_run_listing_scoped`
  - `test_isolation_artifact_listing_scoped`
  - `test_isolation_delete_does_not_affect_other_workspace`

---

## Acceptance Criteria

- [x] Workspace directory layout is created on demand (runs/, artifacts/, db.sqlite)
- [x] RunTrace JSON is persisted under the active workspace and indexed in SQLite
- [x] Isolation tests create two workspaces, run tasks in both, assert no cross-visibility
- [x] Isolation tests assert disk directories are separate and no artifacts/runs leak
- [x] Storage access is behind interfaces (RunStore, ArtifactStore), all queries scoped by workspace_id

---

## Test Results

```
tests/test_storage.py::TestWorkspace::test_workspace_creates_directories PASSED
tests/test_storage.py::TestWorkspace::test_workspace_run_path PASSED
tests/test_storage.py::TestWorkspace::test_workspace_artifact_path PASSED
tests/test_storage.py::TestWorkspace::test_path_safety_rejects_traversal PASSED
tests/test_storage.py::TestWorkspace::test_path_safety_rejects_special_chars PASSED
tests/test_storage.py::TestRunStore::test_save_creates_json_file PASSED
tests/test_storage.py::TestRunStore::test_get_returns_trace PASSED
tests/test_storage.py::TestRunStore::test_get_nonexistent_returns_none PASSED
tests/test_storage.py::TestRunStore::test_list_returns_runs_sorted PASSED
tests/test_storage.py::TestRunStore::test_delete_removes_run PASSED
tests/test_storage.py::TestArtifactStore::test_save_creates_file PASSED
tests/test_storage.py::TestArtifactStore::test_get_returns_artifact_and_content PASSED
tests/test_storage.py::TestArtifactStore::test_list_returns_artifacts PASSED
tests/test_storage.py::TestIsolation::test_isolation_workspaces_separate_directories PASSED
tests/test_storage.py::TestIsolation::test_isolation_runs_not_visible_across_workspaces PASSED
tests/test_storage.py::TestIsolation::test_isolation_artifacts_not_visible_across_workspaces PASSED
tests/test_storage.py::TestIsolation::test_isolation_run_listing_scoped PASSED
tests/test_storage.py::TestIsolation::test_isolation_artifact_listing_scoped PASSED
tests/test_storage.py::TestIsolation::test_isolation_delete_does_not_affect_other_workspace PASSED

19 passed
```

---

## Files Changed

| File | Change |
|------|--------|
| `src/ag/storage/__init__.py` | Added exports for Workspace, stores, interfaces |
| `src/ag/storage/workspace.py` | New: Workspace class with path safety |
| `src/ag/storage/interfaces.py` | New: RunStore and ArtifactStore protocols |
| `src/ag/storage/sqlite_store.py` | New: SQLite implementations |
| `tests/test_storage.py` | New: 19 storage tests including 6 isolation tests |

---

## Architecture Alignment

- **Layering:** Storage layer (`ag.storage`) - data persistence only, no business logic
- **Interfaces touched:** RunStore, ArtifactStore (new protocols)
- **Backward compatibility:** New code, no breaking changes

---

## Branch & PR

- **Branch:** `feat/storage-baseline`
- **Pushed:** Yes (to origin)
