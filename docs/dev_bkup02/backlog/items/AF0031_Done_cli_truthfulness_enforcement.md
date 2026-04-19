# AF0031 — CLI Truthfulness Enforcement
# Version number: v1.0

## Metadata
- **ID:** AF-0031
- **Type:** Foundation
- **Status:** DONE
- **Priority:** P0
- **Area:** CLI | Core | Storage
- **Owner:** Jacob
- **Completed in:** Sprint 03
- **Completion date:** 2026-02-27

## Problem
Risk of hardcoded labels.

## Goal
Ensure all CLI labels derive strictly from RunTrace fields.

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
Ensured all CLI labels derive strictly from RunTrace fields. No hardcoded status labels in CLI output.

**What Changed:**
- `src/ag/cli/main.py` — Added extract_labels() function for trace-derived labels
- `src/ag/cli/main.py` — Updated run display commands to use extract_labels()
- `tests/test_cli_truthful.py` — Added TestExtractLabels class

**Architecture Alignment:**
- CLI adapter only
- Internal refactor, no change to user-facing output

**Truthful UX:**
- All status labels backed by trace fields: final_status, verifier_status, workspace_source, etc.
- Proof: extract_labels(trace) returns dict mapping to trace fields

**Tests Executed:**
- pytest tests/test_cli_truthful.py::TestExtractLabels: PASS
- pytest -W error: PASS (188 tests)

**Run Evidence:**
- `ag runs show <id>` — labels match trace fields
- Every displayed label is trace-derived

