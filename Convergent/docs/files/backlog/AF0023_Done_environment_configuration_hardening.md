# AF0023 — Environment & configuration hardening
# Version number: v0.2

## Metadata
- **ID:** AF-0023
- **Type:** Foundation
- **Status:** DONE
- **Priority:** P1
- **Area:** Docs | CLI | Kernel
- **Owner:** Jacob
- **Completed in:** Sprint 02 (Hardening)
- **Completion date:** 2026-02-26

## Problem
We recently introduced `.env` configuration. Hardcoded paths, implicit defaults, or embedded secrets may still exist. This creates portability risks and violates configuration resolution rules.

## Goal
Ensure configuration and environment handling is fully centralized, portable, and deterministic.

## Non-goals
- No feature expansion
- No storage backend changes

## Acceptance criteria (Definition of Done)
- [x] No hardcoded filesystem paths outside configuration layer
- [x] No secrets hardcoded in source files
- [x] Centralized `.env` loading mechanism
- [x] Configuration resolution order enforced: TaskSpec → Workspace → .env → Defaults
- [x] Tests verifying config precedence behavior
- [x] `ag doctor` validates environment consistency

## Implementation notes
- Audit repository for hardcoded paths and secrets
- Refactor config access to single entry point
- Add regression tests for config resolution order

## Risks
- Misordered resolution could alter runtime behavior

## PR plan
1. PR #1: Audit + refactor configuration loading and precedence

---
# Completion section (fill when done)

**Completion date:** 2026-02-26  
**Author:** Jacob

**Summary:**
Hardened environment variable and configuration handling. Config precedence is clear and tested.

**What Changed:**
- `src/ag/config.py` — Clarified precedence logic, improved error messages
- `tests/test_config.py` — Added 18 tests for config precedence and edge cases
- `docs/dev/cornerstone/CLI_REFERENCE.md` — Documented config precedence

**Architecture Alignment:**
- Config layer (cross-cutting concern)
- Interfaces: get_workspace_dir(), is_dev_mode()
- Existing env vars work unchanged

**Config Precedence:**
CLI flag → env var → default

**Tests Executed:**
- pytest tests/test_config.py: PASS (18 tests)
- Config coverage: 98%

**Deferred:**
- Config file support (.ag.toml) — future sprint

