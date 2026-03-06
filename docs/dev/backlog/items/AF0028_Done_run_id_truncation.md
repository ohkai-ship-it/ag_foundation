# AF0028 — Run ID Formatting Fix
# Version number: v1.0

## Metadata
- **ID:** AF-0028
- **Type:** Foundation
- **Status:** DONE
- **Priority:** P0
- **Area:** CLI | Core | Storage
- **Owner:** Jacob
- **Completed in:** Sprint 03
- **Completion date:** 2026-02-27

## Problem
Run IDs truncated in CLI list output.

## Goal
Display full run_id in ag runs list output.

## Non-goals
N/A

## Acceptance criteria (Definition of Done)
- [x] Implementation complete
- [x] Tests added/updated
- [x] No regression
- [x] Evidence captured (tests + trace)

## Implementation notes
N/A

## Risks
- Regression in CLI behavior
- Workspace state inconsistencies

## PR plan
N/A

---
# Completion section (fill when done)

**Completion date:** 2026-02-27  
**Author:** Jacob

**Summary:**
Display full run_id in `ag runs list` output. Run ID is now copyable for use with `ag runs show`.

**What Changed:**
- `src/ag/cli/main.py` — Updated runs_list command to display full run_id without truncation

**Architecture Alignment:**
- CLI adapter only
- UX improvement, no breaking changes

**Truthful UX:**
- run_id in list output backed by RunTrace.run_id

**Tests Executed:**
- pytest tests/test_cli_truthful.py -k "runs": PASS
- pytest -W error: PASS (188 tests)

**Run Evidence:**
- `ag runs list --workspace <ws>` shows full UUID like `run_a1b2c3d4-e5f6-7890-abcd-ef1234567890`

