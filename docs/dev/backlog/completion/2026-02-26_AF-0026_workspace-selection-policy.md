# Completion Note — AF-0026 / BUG-0005 — Workspace selection policy enforcement
# Version number: v0.1

> Strict template. Fill every section. If something is not applicable, write **N/A** (do not delete sections).

## 1) Metadata
- **Backlog item (primary):** AF-0026
- **Related:** BUG-0005 (Implicit workspace creation on ag run)
- **PR:** N/A (direct commit)
- **Author:** Jacob
- **Date:** 2026-02-26
- **Branch:** main
- **Risk level:** P0
- **Runtime mode used for verification:** manual (dev/test-only)

## 2) Goal and acceptance criteria
### Goal (from backlog item)
Implement deterministic workspace selection policy. Prevent implicit workspace creation. Enforce explicit workspace selection via `--workspace` flag or `AG_WORKSPACE` env var.

### Acceptance criteria (from backlog item)
- [x] `--workspace` flag takes precedence over env var
- [x] `AG_WORKSPACE` env var used when no flag provided
- [x] Error with helpful message when no workspace selected
- [x] No implicit workspace creation on `ag run`
- [x] Regression tests for workspace selection policy
- [x] CLI_REFERENCE.md updated with policy documentation

## 3) What changed (file-level)
- `src/ag/cli/main.py` — Workspace selection policy enforcement before manual mode check
- `src/ag/core/runtime.py` — `V0Normalizer.normalize()` requires explicit workspace, raises ValueError if None
- `tests/test_cli.py` — Added `TestWorkspaceSelectionPolicy` class with 5 regression tests
- `tests/test_cli_global_options.py` — Updated tests to create workspaces before running
- `tests/test_cli_truthful.py` — Updated tests to use workspace_setup fixture
- `docs/dev/cornerstone/CLI_REFERENCE.md` — Updated to v0.2 with Workspace Selection Policy section

## 4) Architecture alignment (mandatory)
- **Layering:** CLI adapter → Core runtime
- **Interfaces touched:** `V0Normalizer.normalize()` (workspace parameter now required)
- **Backward compatibility:** Breaking change — workspace must be explicitly selected

## 5) Truthful UX check (mandatory)
- **User-visible labels affected:** Error message when no workspace selected
- **Trace fields backing them:** N/A
- **Proof:** Error message guides user to create workspace or set AG_WORKSPACE

## 6) Tests executed (mandatory)
- Command: `pytest tests/test_cli.py::TestWorkspaceSelectionPolicy -v`
  - Result: PASS (5 tests)
- Command: `pytest -W error --ignore=tests/test_providers.py`
  - Result: PASS (174 tests)
- Command: `pytest --cov=ag --cov-report=term`
  - Result: 90% overall coverage

## 7) Run evidence (mandatory for behavior changes)
- **RunTrace ID(s):** N/A (policy enforcement)
- **How to reproduce:**
  - Without workspace: `ag run "test"` → Error with helpful message
  - With flag: `$env:AG_DEV = "1"; ag --workspace test_ws run "test"` → Works
  - With env: `$env:AG_WORKSPACE = "test_ws"; ag run "test"` → Works
- **Expected outcomes:**
  - Clear precedence: `--workspace` → `AG_WORKSPACE` → error
  - No implicit workspace creation

## 8) Artifacts (if applicable)
N/A

## 9) Open issues discovered
None.

## 10) Deferred / follow-up items
- Default workspace support (AF-0027 candidate)
- Workspace validation (ensure workspace exists before run)
