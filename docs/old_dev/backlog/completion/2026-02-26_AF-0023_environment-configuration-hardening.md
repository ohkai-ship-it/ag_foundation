# Completion Note — AF-0023 — Environment & configuration hardening
# Version number: v0.1

> Strict template. Fill every section. If something is not applicable, write **N/A** (do not delete sections).

## 1) Metadata
- **Backlog item (primary):** AF-0023
- **PR:** N/A (direct commit)
- **Author:** Jacob
- **Date:** 2026-02-26
- **Branch:** main
- **Risk level:** P1
- **Runtime mode used for verification:** manual (dev/test-only)

## 2) Goal and acceptance criteria
### Goal (from backlog item)
Harden environment variable and configuration handling. Ensure config precedence is clear and tested.

### Acceptance criteria (from backlog item)
- [x] Config precedence documented: CLI flag → env var → default
- [x] `AG_DEV`, `AG_WORKSPACE`, `AG_WORKSPACE_DIR` behavior tested
- [x] Config module coverage ≥90%
- [x] Error messages guide user when config is missing

## 3) What changed (file-level)
- `src/ag/config.py` — Clarified precedence logic, improved error messages
- `tests/test_config.py` — Added 18 tests for config precedence and edge cases
- `docs/dev/cornerstone/CLI_REFERENCE.md` — Documented config precedence

## 4) Architecture alignment (mandatory)
- **Layering:** Config layer (cross-cutting concern)
- **Interfaces touched:** `get_workspace_dir()`, `is_dev_mode()`
- **Backward compatibility:** Yes, existing env vars work unchanged

## 5) Truthful UX check (mandatory)
- **User-visible labels affected:** None; config is internal
- **Trace fields backing them:** N/A
- **Proof:** N/A (no user-visible labels)

## 6) Tests executed (mandatory)
- Command: `pytest tests/test_config.py -v`
  - Result: PASS (18 tests)
- Command: `pytest --cov=ag.config --cov-report=term`
  - Result: 98% coverage on config module

## 7) Run evidence (mandatory for behavior changes)
- **RunTrace ID(s):** N/A (internal config change)
- **How to reproduce:**
  - `$env:AG_WORKSPACE = "C:\temp\ws"; ag run "test"`
  - Check workspace used matches env var
- **Expected outcomes:**
  - Config precedence: CLI flag → env var → default

## 8) Artifacts (if applicable)
N/A

## 9) Open issues discovered
- Config file support (`.ag.toml`) not implemented — deferred to future sprint

## 10) Deferred / follow-up items
- Config file support (`.ag.toml` or similar)
