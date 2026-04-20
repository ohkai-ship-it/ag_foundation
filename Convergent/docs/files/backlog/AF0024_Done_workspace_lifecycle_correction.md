# AF0024 — Workspace lifecycle correction
# Version number: v0.2

## Metadata
- **ID:** AF-0024
- **Type:** Foundation
- **Status:** DONE
- **Priority:** P0
- **Area:** Storage | CLI
- **Owner:** Jacob
- **Completed in:** Sprint 02 (Hardening)
- **Completion date:** 2026-02-26

## Problem
Workspaces appear to be created implicitly per run. Runs must live inside explicit workspace boundaries. Automatic workspace creation violates architectural intent and storage isolation guarantees.

## Goal
Ensure workspace lifecycle is explicit and consistent:
- Workspaces created only via `ag ws create`
- `ag run` never silently creates new workspaces
- Repeated runs reuse the same workspace database

## Non-goals
- No redesign of workspace schema
- No multi-tenant features

## Acceptance criteria (Definition of Done)
- [x] No implicit workspace creation during `ag run`
- [x] Multiple runs in same workspace reuse same DB file
- [x] `--workspace` flag strictly honored
- [x] Workspace ID correctly recorded in RunTrace
- [x] Tests covering repeated runs inside same workspace
- [x] Workspace isolation validated

## Implementation notes
- Audit CLI run flow and workspace initialization logic
- Add tests for repeated run behavior
- Confirm DB path consistency

## Risks
- Incorrect refactor could break run storage behavior

## PR plan
1. PR #1: Workspace lifecycle audit + fix + tests

---
# Completion section (fill when done)

**Completion date:** 2026-02-26  
**Author:** Jacob

**Summary:**
Implemented proper workspace lifecycle via `ag ws create` and `ag ws list` commands. Workspaces are explicitly created before use.

**What Changed:**
- `src/ag/cli/main.py` — Added ws command group with create and list subcommands
- `src/ag/storage/workspace.py` — Enhanced Workspace class for explicit creation
- `tests/test_cli.py` — Added tests for workspace commands

**Architecture Alignment:**
- CLI adapter → Storage layer
- Breaking change: workspaces must be created before use

**Tests Executed:**
- pytest tests/test_cli.py -k "ws": PASS
- pytest -W error: PASS (174 tests)

**Run Evidence:**
- `ag ws create myworkspace`
- `ag ws list`
- `ag --workspace myworkspace run "test"`

**Deferred:**
- `ag ws delete` command
- `ag ws info` command

