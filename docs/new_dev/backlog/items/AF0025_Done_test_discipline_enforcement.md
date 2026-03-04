# AF0025 — Test discipline enforcement (coverage + warnings + Ruff)
# Version number: v0.2

## Metadata
- **ID:** AF-0025
- **Type:** Docs | Foundation
- **Status:** Done
- **Priority:** P1
- **Area:** Docs | Repo
- **Owner:** Jacob
- **Completed in:** Sprint 02 (Hardening)
- **Completion date:** 2026-02-26

## Problem
Coverage thresholds, warning policy, and linting enforcement are not formally codified in documentation and workflow.

## Goal
Enforce engineering discipline via documentation and CI expectations:
- Coverage thresholds defined
- Warnings treated as errors
- Ruff mandatory

## Non-goals
- No CI provider migration
- No new documentation files created

## Acceptance criteria (Definition of Done)
- [x] Testing Guidelines updated with coverage thresholds:
  - Overall ≥85%
  - CLI ≥72%
  - Providers ≥95%
  - Storage ≥95%
- [x] Policy added: warnings fail CI (`pytest -W error`)
- [x] PR Checklist updated to require Ruff
- [x] Repo Hygiene updated to require Ruff check/format
- [x] Collaboration Manifest reflects stricter discipline

## Implementation notes
- Update existing docs only
- Do not introduce new documentation files
- Ensure CI instructions reflect new enforcement rules

## Risks
- Increased strictness may initially surface hidden issues

## PR plan
1. PR #1: Documentation updates + enforcement instructions

---
# Completion section (fill when done)

**Completion date:** 2026-02-26  
**Author:** Jacob

**Summary:**
Enforced test discipline via Ruff linting and documentation of testing guidelines.

**What Changed:**
- `pyproject.toml` — Ruff configuration tuned
- `docs/dev/engineering/TESTING_GUIDELINES.md` — Added hardening rules
- All source files — Ruff format applied

**Tests Executed:**
- ruff check src/ tests/: PASS (no errors)
- ruff format --check src/ tests/: PASS (all files formatted)
- pytest -W error: PASS (174 tests, no warnings)

**Deferred:**
- Pre-commit hooks for automated enforcement
