# BACKLOG ITEM — AF0146 — artifacts_category_filter
# Convergent version: v1.3.1
# Created: 2026-04-06
# Started:
# Completed:
# Status: READY
# Priority: P2
# Area: CLI / Artifacts
# Models:

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI workflow (two-phase — see below)
> - 1 PR = 1 sprint
> - INDEX update rule (status ↔ filename integrity)
>
> **CI workflow (CRITICAL):**
> - **During AF development:** run targeted tests only
>   `pytest tests/test_artifacts.py -x -q`
> - **Before commit (full gate):** run the complete CI gate
>   1. `ruff check src tests`
>   2. `ruff format --check src tests`
>   3. `pytest -W error`
>   4. `pytest --cov=src/ag --cov-report=term-missing`
>
> Do NOT run the full suite on every save. Targeted tests keep feedback fast.
> The full gate runs once, right before `git commit`.

---

## Metadata
- **ID:** AF-0146
- **Type:** CLI / Artifacts
- **Status:** READY
- **Priority:** P2
- **Area:** CLI / Artifacts
- **Owner:** Jacob
- **Target sprint:** Sprint 18 — cli_ux_polish

---

## Problem

`ag artifacts list --run <id>` shows all artifacts for a run with raw `artifact_type` values. Users cannot filter by logical category (e.g., show only results, or only logs). The categorization logic already exists internally — it just isn't exposed to the CLI.

---

## Goal

Add a `--category` filter to `ag artifacts list` and show the category label in table output.

---

## Scope

1. **`src/ag/cli/main.py`** — `artifacts_list` function (~line 2212):
   - Add `--category` / `-c` option (enum or string: `RESULT`, `DOCUMENT`, `LOG`, `CODE`, `DATA`)
   - Filter artifacts where category matches before display
   - Add a "Category" column in the table output (between Type and Size)

2. **`tests/test_artifacts.py`** — Add tests:
   - `--category RESULT` returns only result-type artifacts
   - Unknown category returns empty list or helpful error
   - Category column appears in table output
   - `--json` output includes category field

---

## Non-Goals

- Do NOT change the artifact storage schema
- Do NOT add category as a stored field (derive at display time)
- Do NOT implement category editing

---

## Acceptance criteria

1. `ag artifacts list --run <id> --category RESULT` shows only matching artifacts
2. Table output includes a "Category" column
3. `--json` output includes `category` for each artifact
4. All new tests pass; no regressions in existing artifact tests
