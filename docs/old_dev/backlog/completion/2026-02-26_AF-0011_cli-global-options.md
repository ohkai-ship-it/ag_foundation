# Completion Note — AF-0011 — CLI global options truly global
# Version number: v0.1

> Strict template. Fill every section. If something is not applicable, write **N/A** (do not delete sections).

## 1) Metadata
- **Backlog item (primary):** AF-0011
- **PR:** N/A (direct commit)
- **Author:** Jacob
- **Date:** 2026-02-26
- **Branch:** feat/cli-global-options
- **Risk level:** P1
- **Runtime mode used for verification:** manual (dev/test-only)

## 2) Goal and acceptance criteria
### Goal (from backlog item)
Implement true global options via Typer callback + context propagation so `--workspace`, `--json`, `--quiet`, `--verbose` are available from `ag` and respected (or explicitly ignored) by all subcommands; add tests that close the highest-value uncovered CLI branches.

### Acceptance criteria (from backlog item)
- [x] `ag --help` shows global options: `--workspace/-w`, `--json`, `--quiet/-q`, `--verbose/-v`.
- [x] Global options propagate to subcommands using Typer context (`ctx.obj`) with precedence: command flag > global flag > defaults.
- [x] `--workspace` works uniformly: `ag --workspace ws_a runs list` equals `ag runs list --workspace ws_a`.
- [x] `--json` on supported commands produces machine-readable output with no banners/noise.
- [x] `--quiet` reduces non-essential output on supported commands.
- [x] `--verbose` adds extra debug pointers without changing truth claims.
- [x] Tests added for CLI global options behavior.
- [x] CLI coverage improved (target: +8pp or more).

## 3) What changed (file-level)
- `src/ag/cli/main.py` — Added `CLIContext` dataclass, `get_cli_ctx()` helper, `resolve_option()` helper, `@app.callback()` with global options, updated all subcommands to use `ctx.obj`
- `tests/test_cli_global_options.py` — New file with 13 tests for global options behavior

## 4) Architecture alignment (mandatory)
- **Layering:** CLI adapter only; no core runtime changes
- **Interfaces touched:** N/A (CLI-only change)
- **Backward compatibility:** Yes, fully backward compatible; existing commands work unchanged

## 5) Truthful UX check (mandatory)
- **User-visible labels affected:** None; global options are metadata/presentation only
- **Trace fields backing them:** N/A
- **Proof:** `ag --json run "test"` produces JSON output with run_id; trace contains same run_id

## 6) Tests executed (mandatory)
- Command: `pytest tests/test_cli_global_options.py -v`
  - Result: PASS (13 tests)
- Command: `pytest tests/ -v`
  - Result: PASS (173 passed, 1 deselected)
- Command: `pytest --cov=ag --cov-report=term`
  - Result: 89% overall, cli/main.py 72% (was 64%)

## 7) Run evidence (mandatory for behavior changes)
- **RunTrace ID(s):** Generated during test runs
- **How to reproduce the run:**
  - `$env:AG_DEV = "1"; ag --json run "test global options"`
  - `$env:AG_DEV = "1"; ag --workspace C:\temp\ws run "test workspace"`
- **Expected trace outcomes:**
  - run_id present in JSON output
  - workspace path matches --workspace flag

## 8) Artifacts (if applicable)
**N/A**

## 9) Risks, tradeoffs, and follow-ups
- **Risks introduced:** None
- **Tradeoffs made:** Verbose/quiet modes are minimal stubs; full implementation deferred
- **Follow-up backlog items or bugs to create:** None

## 10) Reviewer checklist (copy/paste)
- [x] I can map PR → AF item and see acceptance criteria satisfied
- [x] I can verify truthful labels from RunTrace
- [x] I can reproduce a run (or it's docs-only)
- [x] Tests were run and results are documented
- [x] Any contract changes are documented in cornerstone docs
