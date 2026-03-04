# Completion Note — AF-0032 — Observability command expansion
# Version number: v1.0

> Strict template. Fill every section. If something is not applicable, write **N/A** (do not delete sections).

## 1) Metadata
- **Backlog item (primary):** AF-0032
- **PR:** N/A (direct commit)
- **Author:** Jacob
- **Date:** 2026-02-27
- **Branch:** main
- **Risk level:** P0
- **Runtime mode used for verification:** manual (dev/test-only)

## 2) Goal and acceptance criteria
### Goal (from backlog item)
Expand `ag runs` commands for trace visibility.

### Acceptance criteria (from backlog item)
- [x] `ag runs stats` command added
- [x] Stats show run count, success/failure rate, workspace info
- [x] `--workspace` flag required for stats
- [x] Tests cover stats command

## 3) What changed (file-level)
- `src/ag/cli/main.py` — Added `runs_stats` command under `runs_app`
- `src/ag/cli/main.py` — Stats calculation from stored RunTraces
- `tests/test_cli_truthful.py` — Added `TestStatsCommand` class with tests

## 4) Architecture alignment (mandatory)
- **Layering:** CLI adapter → Storage layer
- **Interfaces touched:** SQLiteRunStore (read-only)
- **Backward compatibility:** New command, additive change

## 5) Truthful UX check (mandatory)
- **User-visible labels affected:** stats output (counts, rates)
- **Trace fields backing them:** Aggregation of stored RunTraces
- **Proof:** `ag runs stats --workspace <ws>` shows accurate counts

## 6) Tests executed (mandatory)
- Command: `pytest tests/test_cli_truthful.py::TestStatsCommand -v`
  - Result: PASS
- Command: `pytest -W error --ignore=tests/test_providers.py`
  - Result: PASS (188 tests)

## 7) Run evidence (mandatory for behavior changes)
- **RunTrace ID(s):** N/A (aggregation command)
- **How to reproduce:** `ag runs stats --workspace my-ws`
- **Expected outcomes:**
  ```
  Workspace: my-ws
  Total runs: 5
  Completed: 4 (80%)
  Failed: 1 (20%)
  ```

## 8) Artifacts (if applicable)
N/A

## 9) Open issues discovered
None.

## 10) Deferred / follow-up items
- Consider time-range filtering for stats
- Consider cross-workspace stats
