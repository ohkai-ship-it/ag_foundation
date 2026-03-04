# Completion Note — AF-0028 — Run ID truncation fix
# Version number: v1.0

> Strict template. Fill every section. If something is not applicable, write **N/A** (do not delete sections).

## 1) Metadata
- **Backlog item (primary):** AF-0028
- **PR:** N/A (direct commit)
- **Author:** Jacob
- **Date:** 2026-02-27
- **Branch:** main
- **Risk level:** P0
- **Runtime mode used for verification:** manual (dev/test-only)

## 2) Goal and acceptance criteria
### Goal (from backlog item)
Display full run_id in `ag runs list` output.

### Acceptance criteria (from backlog item)
- [x] Full UUID displayed in run list output
- [x] Run ID copyable for use with `ag runs show`
- [x] No truncation of run_id field

## 3) What changed (file-level)
- `src/ag/cli/main.py` — Updated `runs_list` command to display full run_id without truncation

## 4) Architecture alignment (mandatory)
- **Layering:** CLI adapter only
- **Interfaces touched:** None
- **Backward compatibility:** UX improvement only, no breaking changes

## 5) Truthful UX check (mandatory)
- **User-visible labels affected:** run_id in list output
- **Trace fields backing them:** `RunTrace.run_id`
- **Proof:** `ag runs list --workspace <ws>` shows full UUID

## 6) Tests executed (mandatory)
- Command: `pytest tests/test_cli_truthful.py -k "runs" -v`
  - Result: PASS
- Command: `pytest -W error --ignore=tests/test_providers.py`
  - Result: PASS (188 tests)

## 7) Run evidence (mandatory for behavior changes)
- **RunTrace ID(s):** Any run
- **How to reproduce:** `ag runs list --workspace <ws>`
- **Expected outcomes:** Full UUID like `run_a1b2c3d4-e5f6-7890-abcd-ef1234567890`

## 8) Artifacts (if applicable)
N/A

## 9) Open issues discovered
None.

## 10) Deferred / follow-up items
None.
