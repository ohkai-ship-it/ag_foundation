# Engineering Guidelines (ag_foundation)
# Version number: v0.2
# Effective date: 2026-03-03

This document is the **single source of truth** for engineering execution in ag_foundation under `/docs/dev/`.

## Canonical references
- Coding: `/docs/dev/foundation/CODING_GUIDELINES.md`
- Testing: `/docs/dev/foundation/TESTING_GUIDELINES.md`
- Repo hygiene: `/docs/dev/foundation/REPO_HYGIENE.md`
- PR checklist: keep using the repo PR checklist (see PR template / checklist)

## Non-negotiables
1) **Truthful UX:** user-visible labels must be trace-derived.
2) **Workspace isolation:** no cross-workspace reads/writes.
3) **Manual mode is dev/test-only:** must be gated and clearly labeled.
4) **Small PRs:** reviewable in ~15–30 minutes.
5) **CI discipline:** Ruff + tests with warnings-as-errors + coverage thresholds.

## Code quality commands (required before review)
- `ruff check src tests`
- `ruff format --check src tests` (or `ruff format src tests`)
- `pytest -W error`
- `pytest --cov=src/ag --cov-report=term-missing`

## Evidence rule (behavior changes)
Every behavior-changing PR must include:
- tests run (with commands), and
- at least one RunTrace ID (unless docs-only).

## Where things live (new)
- Backlog items: `/docs/dev/backlog/items/`
- Bugs: `/docs/dev/bugs/reports/`
- ADRs: `/docs/dev/decisions/files/`
- Sprint documentation: `/docs/dev/sprints/documentation/Sprint##_.../`
