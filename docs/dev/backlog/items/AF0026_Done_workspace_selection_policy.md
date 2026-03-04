# AF0026 — Workspace selection policy enforcement
# Version number: v0.2

## Metadata
- **ID:** AF-0026
- **Type:** Foundation
- **Status:** Done
- **Priority:** P0
- **Area:** CLI | Runtime | Storage
- **Owner:** Jacob
- **Completed in:** Sprint 02 (Hardening)
- **Completion date:** 2026-02-26

## Problem
`ag run` currently creates workspaces implicitly when none is selected. This contradicts the architecture contract that workspaces are explicit isolation boundaries.

## Goal
Implement a deterministic workspace selection policy:
1. If `--workspace` provided → use it
2. Else if default workspace configured → use it
3. Else → fail with explicit error message

Implicit workspace creation must be eliminated.

## Non-goals
- No redesign of workspace schema.
- No multi-tenant feature additions.

## Acceptance criteria (Definition of Done)
- [x] No implicit workspace creation during `ag run`
- [x] Explicit error message when no workspace selected
- [x] Default workspace behavior clearly defined
- [x] Regression tests covering selection logic
- [x] CLI_REFERENCE updated to reflect final policy

## Implementation notes
- Audit CLI run path.
- Remove auto-creation branch.
- Ensure RunTrace records correct workspace_id.
- Update documentation accordingly (existing docs only).

## Risks
- Could temporarily break user flows relying on implicit behavior.
- Must ensure tests updated accordingly.

## PR plan
1. PR #1: Implement workspace selection enforcement + regression tests.

---
# Completion section (fill when done)

**Completion date:** 2026-02-26  
**Author:** Jacob

**Summary:**
Implemented deterministic workspace selection policy. Implicit workspace creation eliminated. Explicit workspace selection enforced via --workspace flag or AG_WORKSPACE env var.

**What Changed:**
- `src/ag/cli/main.py` — Workspace selection policy enforcement before manual mode check
- `src/ag/core/runtime.py` — V0Normalizer.normalize() requires explicit workspace
- `tests/test_cli.py` — Added TestWorkspaceSelectionPolicy class with 5 regression tests
- `tests/test_cli_global_options.py` — Updated tests to create workspaces before running
- `tests/test_cli_truthful.py` — Updated tests to use workspace_setup fixture
- `docs/dev/cornerstone/CLI_REFERENCE.md` — Updated to v0.2 with Workspace Selection Policy section

**Workspace Selection Precedence:**
1. `--workspace` flag
2. `AG_WORKSPACE` env var
3. Error with helpful message

**Architecture Alignment:**
- CLI adapter → Core runtime
- Breaking change: workspace must be explicitly selected

**Tests Executed:**
- pytest tests/test_cli.py::TestWorkspaceSelectionPolicy: PASS (5 tests)
- pytest -W error: PASS (174 tests)
- Overall coverage: 90%

**Run Evidence:**
- Without workspace: `ag run "test"` → Error with helpful message
- With flag: `ag --workspace test_ws run "test"` → Works
- With env: `$env:AG_WORKSPACE = "test_ws"; ag run "test"` → Works
