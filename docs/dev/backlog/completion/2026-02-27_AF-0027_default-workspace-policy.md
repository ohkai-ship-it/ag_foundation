# Completion Note — AF-0027 — Default workspace policy (intuitive precedence)
# Version number: v1.0

> Strict template. Fill every section. If something is not applicable, write **N/A** (do not delete sections).

## 1) Metadata
- **Backlog item (primary):** AF-0027
- **PR:** N/A (direct commit)
- **Author:** Jacob
- **Date:** 2026-02-27
- **Branch:** main
- **Risk level:** P0
- **Runtime mode used for verification:** manual (dev/test-only)

## 2) Goal and acceptance criteria
### Goal (from backlog item)
Implement revised workspace precedence model with explicit source tracking in RunTrace.

### Acceptance criteria (from backlog item)
- [x] Workspace resolution order: `--workspace` → persisted default → `AG_WORKSPACE` → bootstrap 'default' → error
- [x] Persisted default set via `ag ws use <workspace>`
- [x] Bootstrap creates 'default' workspace only when no workspaces exist
- [x] Error with actionable guidance when no workspace can be resolved
- [x] Tests cover all precedence levels

## 3) What changed (file-level)
- `src/ag/cli/main.py` — `resolve_workspace_id()` function with full precedence chain, `get_persisted_default_workspace()`, `set_persisted_default_workspace()`
- `src/ag/cli/main.py` — `ag ws use` command to set persisted default
- `tests/test_cli.py` — `TestWorkspaceResolution` class with tests for precedence, env fallback, persisted default

## 4) Architecture alignment (mandatory)
- **Layering:** CLI-only workspace resolution (no runtime coupling)
- **Interfaces touched:** None (CLI adapter only)
- **Backward compatibility:** Improved UX — new precedence levels are additive

## 5) Truthful UX check (mandatory)
- **User-visible labels affected:** Workspace resolution source in error messages
- **Trace fields backing them:** `RunTrace.workspace_source` (added in AF-0030)
- **Proof:** Error messages indicate resolution step that failed

## 6) Tests executed (mandatory)
- Command: `pytest tests/test_cli.py -k "workspace" -v`
  - Result: PASS (10+ workspace tests)
- Command: `pytest -W error --ignore=tests/test_providers.py`
  - Result: PASS (188 tests)

## 7) Run evidence (mandatory for behavior changes)
- **RunTrace ID(s):** N/A (precedence logic)
- **How to reproduce:**
  - With flag: `ag run --workspace my-ws "test"` → Uses my-ws
  - With persisted: `ag ws use my-ws; ag run "test"` → Uses my-ws
  - With env: `$env:AG_WORKSPACE = "env-ws"; ag run "test"` → Uses env-ws
  - No workspaces: `ag run "test"` → Creates 'default'
  - Workspaces exist, none selected: `ag run "test"` → Error with guidance
- **Expected outcomes:** Predictable resolution with clear precedence

## 8) Artifacts (if applicable)
N/A

## 9) Open issues discovered
None.

## 10) Deferred / follow-up items
- AF-0034: Error message hardening (no name leakage)
- AF-0035: Clarify --workspace help text
