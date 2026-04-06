# BACKLOG ITEM — AF0144 — runs_list_filter_expansion
# Convergent version: v1.3.1
# Created: 2026-04-06
# Started: 2026-04-06
# Completed: 2026-04-06
# Status: DONE
# Priority: P2
# Area: CLI / UX
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
>   `pytest tests/test_cli.py -x -q`
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
- **ID:** AF-0144
- **Type:** CLI / UX
- **Status:** DONE
- **Priority:** P2
- **Area:** CLI / UX
- **Owner:** Jacob
- **Target sprint:** Sprint 18 — cli_ux_polish

---

## Problem

`ag runs list` currently supports only `--status success|failure` as a filter. Users with many runs cannot narrow results by playbook or execution mode. The data is already in RunTrace — just not exposed as CLI filters.

---

## Goal

Add `--playbook <name>` and `--mode llm|manual` filter options to the `ag runs list` command.

---

## Scope

1. **`src/ag/cli/main.py`** — `runs_list` function (~line 1294):
   - Add `--playbook` / `-p` option (string, optional) — filter runs where `run.playbook == name`
   - Add `--mode` / `-m` option (enum: `llm`|`manual`, optional) — filter runs where `run.mode == mode`
   - Apply filters after existing status filter, before pagination

2. **`tests/test_cli.py`** — Add tests:
   - `--playbook research_v0` returns only matching runs
   - `--mode manual` returns only manual-mode runs
   - Combined filters (`--status success --playbook research_v0`) work
   - Unknown playbook returns empty list (not an error)

---

## Non-Goals

- Do NOT change RunTrace schema
- Do NOT add filters to `ag runs show` or `ag runs trace`
- Do NOT add date-range filters (future AF)

---

## Acceptance criteria

1. `ag runs list --playbook research_v0` shows only runs using that playbook
2. `ag runs list --mode manual` shows only manual-mode runs
3. Filters compose with existing `--status` filter
4. `--json` output respects all filters
5. All new tests pass; no regressions in existing CLI tests
