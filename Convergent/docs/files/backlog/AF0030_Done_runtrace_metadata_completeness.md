# AF0030 — RunTrace Metadata Completeness
# Version number: v1.0

## Metadata
- **ID:** AF-0030
- **Type:** Foundation
- **Status:** DONE
- **Priority:** P0
- **Area:** CLI | Core | Storage
- **Owner:** Jacob
- **Completed in:** Sprint 03
- **Completion date:** 2026-02-27

## Problem
Trace lacks workspace source metadata.

## Goal
Add workspace_source field to RunTrace.

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
Added workspace_source field to RunTrace for audit trail.

**WorkspaceSource enum values:**
- CLI_FLAG
- PERSISTED_DEFAULT
- ENV_VAR
- BOOTSTRAP

**What Changed:**
- `src/ag/core/run_trace.py` — Added WorkspaceSource enum
- `src/ag/core/run_trace.py` — Added workspace_source: Optional[WorkspaceSource] field
- `src/ag/cli/main.py` — resolve_workspace_id() returns tuple (workspace_id, source)
- `tests/test_cli_truthful.py` — Added TestWorkspaceSource class with 2 tests

**Architecture Alignment:**
- Core domain model (RunTrace) + CLI adapter
- New field is Optional, additive change

**Truthful UX:**
- workspace_source in trace output backed by RunTrace.workspace_source

**Tests Executed:**
- pytest tests/test_cli_truthful.py::TestWorkspaceSource: PASS (2 tests)
- pytest -W error: PASS (188 tests)

**Run Evidence:**
- `ag runs show <run_id> --json` includes `"workspace_source": "CLI_FLAG"`

