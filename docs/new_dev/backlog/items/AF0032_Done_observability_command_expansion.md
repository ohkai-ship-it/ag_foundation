# AF0032 — Observability Command Expansion
# Version number: v1.0

## Metadata
- **ID:** AF-0032
- **Type:** Foundation
- **Status:** Done
- **Priority:** P0
- **Area:** CLI | Core | Storage
- **Owner:** Jacob
- **Completed in:** Sprint 03
- **Completion date:** 2026-02-27

## Problem
Limited run inspection capabilities.

## Goal
Expand ag runs commands for trace visibility.

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
Expanded `ag runs` commands for trace visibility. Added `ag runs stats` command.

**What Changed:**
- `src/ag/cli/main.py` — Added runs_stats command under runs_app
- `src/ag/cli/main.py` — Stats calculation from stored RunTraces
- `tests/test_cli_truthful.py` — Added TestStatsCommand class

**Architecture Alignment:**
- CLI adapter → Storage layer
- New command, additive change

**Truthful UX:**
- Stats output (counts, rates) backed by aggregation of stored RunTraces

**Tests Executed:**
- pytest tests/test_cli_truthful.py::TestStatsCommand: PASS
- pytest -W error: PASS (188 tests)

**Run Evidence:**
```
ag runs stats --workspace my-ws

Workspace: my-ws
Total runs: 5
Completed: 4 (80%)
Failed: 1 (20%)
```

**Follow-up:**
- Consider time-range filtering for stats
- Consider cross-workspace stats
