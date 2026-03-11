# BACKLOG ITEM — AF0088 — runs_list_pagination
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI discipline (ruff + pytest -W error + coverage)
> - INDEX update rule (status ↔ filename integrity)

> **File naming (required):** `AF####_<STATUS>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0088
- **Type:** Feature
- **Status:** DONE
- **Priority:** P2
- **Area:** CLI
- **Owner:** Jacob
- **Target sprint:** Sprint09

---

## Problem
`ag runs list` appears capped to a small number of rows without explicit pagination context in output.
Users cannot tell whether all runs are shown or truncated.

---

## Goal
Add explicit pagination/limit UX for runs listing.

---

## Non-goals
- Redesigning all CLI table output
- Changing run storage behavior

---

## Acceptance criteria (Definition of Done)
- [ ] `ag runs list` output indicates total count and displayed count
- [ ] CLI provides clear controls (`--limit`, `--offset`, and/or `--all`)
- [ ] Help text documents pagination behavior
- [ ] Tests cover default, limited, and offset/all cases
- [ ] `ruff check src tests` passes
- [ ] `pytest -W error` passes

---

## Implementation notes
Likely touchpoints:
- `src/ag/cli/main.py` (`runs list` command)
- `tests/test_cli_truthful.py` and/or `tests/test_cli.py`

---

## Risks
- Breaking scripts that parse current plain table output
- Inconsistent behavior between table and `--json`

---

## Completion (Sprint09)

### Files changed
- `src/ag/storage/interfaces.py` — added `count(workspace_id) -> int` method to `RunStore` protocol
- `src/ag/storage/sqlite_store.py` — implemented `count()` using SQL COUNT
- `src/ag/cli/main.py` — `runs list` command: added `--all` flag, pagination info in table title ("showing X of Y"), JSON output changed to `{total, showing, runs}` object

### Tests added
- `tests/test_storage.py`:
  - `test_count_empty_workspace`
  - `test_count_returns_total`
  - `test_count_per_workspace`
- `tests/test_cli.py`:
  - `TestRunsListPagination.test_default_shows_10`
  - `TestRunsListPagination.test_all_flag_shows_all`
  - `TestRunsListPagination.test_json_includes_pagination_info`
  - `TestRunsListPagination.test_title_shows_pagination_status`

### Breaking changes
- JSON output for `runs list` changed from array to `{total: int, showing: int, runs: [...]}` object
- Updated dependent tests in `test_cli_global_options.py`, `test_cli_truthful.py`, `test_delegation.py`

### Evidence
- All 459 tests pass
- `ruff check src tests` clean
- Coverage: 86%
