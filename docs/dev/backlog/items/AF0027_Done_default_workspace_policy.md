# AF0027 — Default Workspace Policy
# Version number: v1.0

## Metadata
- **ID:** AF-0027
- **Type:** Foundation
- **Status:** DONE
- **Priority:** P0
- **Area:** CLI | Core | Storage
- **Owner:** Jacob
- **Completed in:** Sprint 03
- **Completion date:** 2026-02-27

## Problem
Workspace resolution must be intuitive and predictable.

## Goal
Implement revised precedence model with explicit source tracking in RunTrace.

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
Implemented revised workspace precedence model with explicit source tracking in RunTrace.

**Workspace Resolution Order:**
1. `--workspace` flag
2. Persisted default (via `ag ws use`)
3. `AG_WORKSPACE` env var
4. Bootstrap 'default' workspace (only when no workspaces exist)
5. Error with actionable guidance

**What Changed:**
- `src/ag/cli/main.py` — resolve_workspace_id() function, get_persisted_default_workspace(), set_persisted_default_workspace()
- `src/ag/cli/main.py` — `ag ws use` command to set persisted default
- `tests/test_cli.py` — TestWorkspaceResolution class

**Tests Executed:**
- pytest tests/test_cli.py -k "workspace": PASS (10+ tests)
- pytest -W error: PASS (188 tests)

**Run Evidence:**
- With flag: `ag run --workspace my-ws "test"` → Uses my-ws
- With persisted: `ag ws use my-ws; ag run "test"` → Uses my-ws
- With env: `$env:AG_WORKSPACE = "env-ws"; ag run "test"` → Uses env-ws

**Follow-up:**
- AF-0034: Error message hardening
- AF-0035: Clarify --workspace help text

