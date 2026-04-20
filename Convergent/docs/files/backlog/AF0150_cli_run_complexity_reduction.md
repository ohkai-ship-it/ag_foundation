# BACKLOG ITEM — AF0150 — cli_run_complexity_reduction
# Convergent version: v1.3.1
# Created: 2026-04-12
# Started:
# Completed:
# Status: READY
# Priority: P2
# Area: CLI / Code Quality
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
- **ID:** AF-0150
- **Type:** Code Quality / Refactor
- **Status:** READY
- **Priority:** P2
- **Area:** CLI / Code Quality
- **Owner:** (unassigned)
- **Target sprint:** (unassigned)
- **Origin:** M&A Audit Report 2026-04-12 — Part II §2 Cyclomatic Complexity, Refactor Priority Matrix P1

---

## Problem

`cli/main.py:run()` has a cyclomatic complexity of **CC=91**, making it the most complex function in the codebase by a wide margin (next highest: `runs_show()` at CC=39). This function handles workspace resolution, mode selection, playbook lookup, plan creation, plan approval, execution invocation, trace formatting, error handling, and output rendering — all in a single function body.

High CC makes the function:
- Hard to test in isolation (requires many paths to cover)
- Prone to regressions when adding new flags or execution modes
- Difficult for new contributors to understand

---

## Acceptance Criteria

1. `cli/main.py:run()` cyclomatic complexity is reduced to **CC ≤ 25**
2. Extracted helper functions have clear single responsibilities
3. All existing CLI tests (`test_cli.py`, `test_cli_truthful.py`, `test_cli_global_options.py`) pass unchanged
4. No behavior changes — pure structural refactor
5. Overall coverage does not regress

---

## Approach (suggested)

Extract coherent phases into private helper functions:

| Phase | Candidate function | Responsibility |
|-------|-------------------|----------------|
| Workspace setup | `_resolve_workspace()` | Workspace resolution + validation |
| Mode resolution | `_resolve_execution_mode()` | LLM vs manual mode selection |
| Playbook/plan | `_resolve_plan()` | Playbook lookup, plan creation, approval flow |
| Execution | `_execute_run()` | Runtime creation + run invocation |
| Output | `_render_result()` | Trace formatting + output display |
| Error handling | `_handle_run_error()` | Error classification + user messaging |

Each extracted function should be independently testable but initially tested only through existing integration tests.

---

## Secondary targets (same AF or follow-up)

| Function | Current CC | Target CC |
|----------|-----------|-----------|
| `runs_show()` | 39 | ≤ 20 |
| `_format_markdown()` (emit_result) | 24 | ≤ 15 |

These are lower priority but could be addressed in the same refactor pass if time permits. If scoped out, they should become a separate AF.

---

## Out of Scope

- CLI behavior changes or new flags
- Splitting `main.py` into multiple files (separate AF if needed)
- Addressing silent `except Exception` patterns (tracked separately)

---

## Estimate

**M** — structural refactor across a large function, requires careful test verification.
