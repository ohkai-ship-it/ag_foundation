# BACKLOG ITEM — AF0147 — playbooks_show_command
# Convergent version: v1.3.1
# Created: 2026-04-06
# Started:
# Completed:
# Status: READY
# Priority: P2
# Area: CLI / Playbooks
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
- **ID:** AF-0147
- **Type:** CLI / Playbooks
- **Status:** READY
- **Priority:** P2
- **Area:** CLI / Playbooks
- **Owner:** Jacob
- **Target sprint:** Sprint 18 — cli_ux_polish

---

## Problem

`ag playbooks show <name>` is currently a stub (`_not_implemented`). Users can list playbooks but cannot inspect their structure — steps, skills used, reasoning modes, budgets — without reading source code. This is the only playbook command that's still unimplemented.

---

## Goal

Implement `ag playbooks show <name>` to display full playbook detail.

---

## Scope

1. **`src/ag/cli/main.py`** — `playbooks_show` function (~line 2545):
   - Load playbook from registry by name
   - Display: name, description, version, roles
   - Display steps table: order, skill name, reasoning mode, required flag, budget (if set)
   - Handle unknown playbook name with clean error message
   - Support `--json` for machine-readable output

2. **`tests/test_cli.py`** — Add tests:
   - `ag playbooks show research_v0` displays correct detail
   - `ag playbooks show summarize_v0` displays correct detail
   - Unknown playbook gives clean error (exit code 1, helpful message)
   - `--json` returns valid JSON with all fields
   - Step order matches playbook definition

---

## Non-Goals

- Do NOT add playbook editing or creation commands
- Do NOT change the Playbook schema
- Do NOT implement `ag playbooks validate` (separate future AF)

---

## Acceptance criteria

1. `ag playbooks show research_v0` displays name, description, roles, and step table
2. Step table shows: order, skill, reasoning mode, required, budget
3. `ag playbooks show nonexistent` exits with code 1 and helpful error
4. `--json` output includes all displayed fields
5. All new tests pass; no regressions in existing CLI tests
