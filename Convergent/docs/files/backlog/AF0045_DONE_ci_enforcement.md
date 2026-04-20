# AF0045 — Enforce CI + Ruff + pytest -W error + coverage thresholds (pre-commit + GitHub Actions)
# Version number: v0.1

## Metadata
- **ID:** AF0045
- **Type:** Docs | Refactor
- **Status:** DONE
- **Priority:** P0
- **Area:** CI/Quality
- **Owner:** Jacob
- **Target sprint:** Sprint04
- **Completion date:** 2026-03-03

## Problem
Code-quality rules exist in docs but are not enforced (ruff not integrated; CI not blocking merges). This allows regressions and undermines the PR checklist.

## Goal
Add enforceable automation so every PR is blocked unless ruff passes, formatting is correct, tests pass with warnings as errors, and coverage thresholds are maintained.

## Non-goals
No functional changes to runtime behavior unless required to fix newly revealed lint/test failures.

## Renaming / naming conventions (template first)
N/A (config addition).

## Files that change

### Legacy (`/docs/dev/`)
- `docs/dev/engineering/PR_CHECKLIST.md`
- `docs/dev/engineering/CODING_GUIDELINES.md`
- `docs/dev/engineering/TESTING_GUIDELINES.md`

### Canonical (`/docs/dev/`)
- `.pre-commit-config.yaml`
- `.github/workflows/ci.yml (or .github/workflows/python.yml — exact filename chosen in implementation)`
- `pyproject.toml (if needed for ruff config / tool settings)`
- `docs/dev/foundation/PR_CHECKLIST.md`
- `docs/dev/foundation/CODING_GUIDELINES.md`
- `docs/dev/foundation/TESTING_GUIDELINES.md`

## Acceptance criteria (Definition of Done)
- [ ] Pre-commit hook exists and runs ruff + ruff-format
- [ ] GitHub Actions workflow exists and runs: `ruff check`, `ruff format --check`, `pytest -W error`, and coverage check vs thresholds
- [ ] CI fails on any warning, lint/format error, or coverage drop below thresholds
- [ ] PR checklist and foundation docs reference the canonical commands and paths (no stale `/docs/dev/...` references)

## Implementation notes
Keep the workflow minimal. Prefer a single CI job first (fast feedback) before matrix expansion. If the repo already has workflows, extend rather than duplicate.

## Risks
CI may fail initially due to existing lint debt; mitigate by scoping fixes to only what is required to pass and tracking remaining debt as AF/BUG items.

## PR plan (PR-sized)
1. PR: Add pre-commit config + GitHub Actions workflow + minimal ruff/pytest/coverage wiring
2. PR (optional): Fix any newly revealed lint/test failures (small, focused)

