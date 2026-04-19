# AF0006 — Workspace + storage baseline (sqlite + filesystem) with explicit isolation tests
# Version number: v0.3

## Metadata
- **ID:** AF-0006
- **Type:** Foundation
- **Status:** DONE
- **Priority:** P0
- **Area:** Storage
- **Owner:** Jacob
- **Completed in:** Sprint 01
- **Completion date:** 2026-02-24

## Problem
Need durable run persistence and strict workspace isolation. Previous criteria lacked concrete, testable isolation scenarios.

## Goal
Implement workspace-scoped storage (SQLite indices + filesystem traces/artifacts) and prove isolation via automated tests covering multi-workspace runs and CLI listing.

## Non-goals
- Postgres/migrations.
- Remote storage.
- RAG/memory stores.

## Acceptance criteria (Definition of Done)
- [x] Workspace directory layout is created on demand (e.g., `runs/`, `artifacts/`, `db.sqlite`).
- [x] RunTrace JSON is persisted under the active workspace and indexed in SQLite.
- [x] Isolation tests create two workspaces (ws_a, ws_b), run tasks in both, and assert no cross-visibility (runs list/show).
- [x] Isolation tests assert disk directories are separate and no artifacts/runs leak between workspaces.
- [x] Storage access is behind interfaces (`RunStore`, `ArtifactStore`) and all queries are scoped by workspace_id.

## Implementation notes
- Keep SQLite schema minimal.
- Enforce path safety.
- Prefer CLI-level tests where practical (`ag runs list --workspace ws_a`).

## Risks
P0: leakage across workspaces. Mitigate with strict scoping + automated isolation tests.

## PR plan
1. PR (feat/storage-baseline): Implement storage + explicit isolation tests (2 workspaces, 2 runs, no leakage).

---
# Completion section (fill when done)

**Completion date:** 2026-02-24  
**Author:** Jacob (Junior Engineer)

**Summary:**
Implemented workspace-scoped storage with SQLite indices and filesystem-based JSON traces/artifacts, including explicit isolation tests.

**What Was Done:**

1. **Workspace Directory Layout** (`src/ag/storage/workspace.py`)
   - Workspace class manages per-workspace directories
   - Structure: `{root}/{workspace_id}/runs/`, `artifacts/`, `db.sqlite`
   - Path safety validation prevents path traversal

2. **Storage Interfaces** (`src/ag/storage/interfaces.py`)
   - RunStore protocol: save, get, list, delete
   - ArtifactStore protocol: save, get, list, delete
   - All operations scoped by workspace_id

3. **SQLite Implementation** (`src/ag/storage/sqlite_store.py`)
   - SQLiteRunStore and SQLiteArtifactStore
   - Per-workspace database files

4. **Test Suite** (`tests/test_storage.py`)
   - 19 tests including 6 explicit isolation tests
   - Tests: workspace creation, CRUD operations, cross-workspace isolation

**Test Results:** 19 passed

**Architecture Alignment:** Storage layer (ag.storage) - data persistence only, no business logic.

