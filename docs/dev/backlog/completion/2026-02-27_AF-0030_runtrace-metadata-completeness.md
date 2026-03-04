# Completion Note — AF-0030 — RunTrace metadata completeness (workspace_source)
# Version number: v1.0

> Strict template. Fill every section. If something is not applicable, write **N/A** (do not delete sections).

## 1) Metadata
- **Backlog item (primary):** AF-0030
- **PR:** N/A (direct commit)
- **Author:** Jacob
- **Date:** 2026-02-27
- **Branch:** main
- **Risk level:** P0
- **Runtime mode used for verification:** manual (dev/test-only)

## 2) Goal and acceptance criteria
### Goal (from backlog item)
Add workspace_source field to RunTrace for audit trail.

### Acceptance criteria (from backlog item)
- [x] `workspace_source` field added to RunTrace
- [x] WorkspaceSource enum: CLI_FLAG, PERSISTED_DEFAULT, ENV_VAR, BOOTSTRAP
- [x] Source captured at run creation time
- [x] Tests verify workspace_source population

## 3) What changed (file-level)
- `src/ag/core/run_trace.py` — Added `WorkspaceSource` enum
- `src/ag/core/run_trace.py` — Added `workspace_source: Optional[WorkspaceSource]` field to RunTrace
- `src/ag/cli/main.py` — `resolve_workspace_id()` returns tuple of (workspace_id, source)
- `tests/test_cli_truthful.py` — Added `TestWorkspaceSource` class with 2 tests

## 4) Architecture alignment (mandatory)
- **Layering:** Core domain model (RunTrace) + CLI adapter
- **Interfaces touched:** RunTrace (new field), CLI (source tracking)
- **Backward compatibility:** New field is Optional, additive change

## 5) Truthful UX check (mandatory)
- **User-visible labels affected:** workspace_source in trace output
- **Trace fields backing them:** `RunTrace.workspace_source`
- **Proof:** `ag runs show <run_id> --json` includes workspace_source

## 6) Tests executed (mandatory)
- Command: `pytest tests/test_cli_truthful.py::TestWorkspaceSource -v`
  - Result: PASS (2 tests)
- Command: `pytest -W error --ignore=tests/test_providers.py`
  - Result: PASS (188 tests)

## 7) Run evidence (mandatory for behavior changes)
- **RunTrace ID(s):** Any new run
- **How to reproduce:** `ag run --workspace my-ws "test"; ag runs show <id> --json`
- **Expected outcomes:** `"workspace_source": "CLI_FLAG"` in JSON output

## 8) Artifacts (if applicable)
N/A

## 9) Open issues discovered
None.

## 10) Deferred / follow-up items
None.
