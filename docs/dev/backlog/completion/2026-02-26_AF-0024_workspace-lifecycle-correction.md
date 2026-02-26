# Completion Note — AF-0024 — Workspace lifecycle correction
# Version number: v0.1

> Strict template. Fill every section. If something is not applicable, write **N/A** (do not delete sections).

## 1) Metadata
- **Backlog item (primary):** AF-0024
- **PR:** N/A (direct commit)
- **Author:** Jacob
- **Date:** 2026-02-26
- **Branch:** main
- **Risk level:** P1
- **Runtime mode used for verification:** manual (dev/test-only)

## 2) Goal and acceptance criteria
### Goal (from backlog item)
Implement proper workspace lifecycle via `ag ws create` and `ag ws list` commands. Ensure workspaces are explicitly created before use.

### Acceptance criteria (from backlog item)
- [x] `ag ws create [name]` creates workspace directory + metadata
- [x] `ag ws list` shows available workspaces
- [x] Workspace creation is explicit (no auto-creation on run)
- [x] Tests for workspace CLI commands

## 3) What changed (file-level)
- `src/ag/cli/main.py` — Added `ws` command group with `create` and `list` subcommands
- `src/ag/storage/workspace.py` — Enhanced `Workspace` class for explicit creation
- `tests/test_cli.py` — Added tests for workspace commands

## 4) Architecture alignment (mandatory)
- **Layering:** CLI adapter → Storage layer
- **Interfaces touched:** `Workspace.create()`, CLI `ws` group
- **Backward compatibility:** Breaking change — workspaces must be created before use

## 5) Truthful UX check (mandatory)
- **User-visible labels affected:** None; workspace commands are metadata
- **Trace fields backing them:** N/A
- **Proof:** N/A (no user-visible labels)

## 6) Tests executed (mandatory)
- Command: `pytest tests/test_cli.py -v -k "ws"`
  - Result: PASS (workspace-related tests)
- Command: `pytest -W error --ignore=tests/test_providers.py`
  - Result: PASS (174 tests)

## 7) Run evidence (mandatory for behavior changes)
- **RunTrace ID(s):** N/A (CLI command change)
- **How to reproduce:**
  - `ag ws create myworkspace`
  - `ag ws list`
  - `ag --workspace myworkspace run "test"`
- **Expected outcomes:**
  - Workspace created in `AG_WORKSPACE_DIR/myworkspace/`
  - List shows available workspaces

## 8) Artifacts (if applicable)
N/A

## 9) Open issues discovered
None.

## 10) Deferred / follow-up items
- `ag ws delete` command (cleanup)
- `ag ws info` command (detailed workspace metadata)
