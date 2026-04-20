# BACKLOG ITEM — AF0145 — doctor_diagnostic_expansion
# Convergent version: v1.3.1
# Created: 2026-04-06
# Started: 2026-04-06
# Completed: 2026-04-06
# Status: DONE
# Priority: P2
# Area: CLI / Diagnostics
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
- **ID:** AF-0145
- **Type:** CLI / Diagnostics
- **Status:** DONE
- **Priority:** P2
- **Area:** CLI / Diagnostics
- **Owner:** Jacob
- **Target sprint:** Sprint 18 — cli_ux_polish

---

## Problem

`ag doctor` currently checks system info, env vars, config, and workspace storage — but does not validate that the persistence layer is healthy or that a provider is usable. Users troubleshooting issues get no signal about database integrity or API key validity until runtime failure.

---

## Goal

Expand `ag doctor` with 2–3 new diagnostic checks that surface common failure modes early.

---

## Scope

1. **`src/ag/cli/main.py`** — `doctor` function (~line 2609):
   - **SQLite database integrity** — For the default workspace, attempt to open `runs.db` and run `PRAGMA integrity_check`. Report pass/fail.
   - **Provider credential format** — Check if `OPENAI_API_KEY` is set and matches expected format (`sk-...`). Report: set + valid format / set + unexpected format / not set. Do NOT make API calls.
   - **Artifact storage path** — Verify the artifacts directory exists and is writable (attempt create + delete a temp file).

2. **`tests/test_cli.py`** — Add tests:
   - Doctor runs successfully on fresh workspace (no DB yet → reports "no database")
   - Doctor runs with existing workspace (DB present → reports integrity OK)
   - Provider key format check works for valid and invalid formats
   - Artifact path check works for existing and missing directories

---

## Non-Goals

- Do NOT make real API calls to validate provider connectivity
- Do NOT add self-repair capabilities (doctor diagnoses, does not fix)
- Do NOT check network connectivity

---

## Acceptance criteria

1. `ag doctor` displays at least 3 new check results (SQLite, provider key, artifact path)
2. Each check shows pass/fail/warning with actionable hint on failure
3. All new tests pass; no regressions in existing doctor tests
4. Doctor still runs fast (< 2 seconds total)
