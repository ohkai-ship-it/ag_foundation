# Handoff Note — AF-0010 — Python Project Bootstrap
**Date:** 2026-02-24
**Author:** Jacob (Junior Engineer)
**Status:** Ready for review

---

## Summary
Implemented the Python project bootstrap for ag_foundation, establishing the foundational scaffold for Sprint 01 development.

## What Was Done

### 1. Project Configuration (`pyproject.toml`)
- Build system: hatchling
- Python version: >=3.10
- Dependencies:
  - `typer>=0.9.0` (CLI framework)
  - `pydantic>=2.0.0` (schemas)
  - `rich>=13.0.0` (console output)
- Dev dependencies: pytest, pytest-cov, ruff, mypy
- Console script entrypoint: `ag = "ag.cli.main:app"`

### 2. Package Structure (`src/ag/`)
```
src/ag/
├── __init__.py          # Package root, version "0.1.0"
├── config.py            # Configuration contract (placeholder)
├── cli/
│   ├── __init__.py
│   └── main.py          # Typer CLI stub
├── core/
│   └── __init__.py      # Core runtime (empty, for AF-0005+)
├── storage/
│   └── __init__.py      # Storage layer (empty, for AF-0006)
└── skills/
    └── __init__.py      # Skills registry (empty, for AF-0007)
```

### 3. CLI Stub (`ag/cli/main.py`)
Implemented all command groups per CLI_REFERENCE.md:
- `ag run <prompt>` — with `--mode`, `--workspace`, `--playbook`, `--reasoning` options
- `ag runs list|show|trace` — run inspection
- `ag ws list|create|use|show` — workspace management
- `ag artifacts list|show` — artifact registry
- `ag skills list|info` — skills management
- `ag playbooks list|show` — playbook management
- `ag config list|get|set` — configuration management
- `ag doctor` — diagnostics

**Manual mode gate implemented:**
- `--mode manual` requires `AG_DEV=1` environment variable
- Fails with clear error message if env var not set
- Prints banner: `DEV MODE: manual (LLMs disabled)`

### 4. Configuration Contract (`ag/config.py`)
Documented but NOT implemented (per scope):
- Config file location: `~/.ag/config.yaml` (or `AG_CONFIG_PATH`)
- Schema structure for: workspaces, LLM providers, telemetry, defaults
- Environment variable overrides: `AG_DEV`, `AG_WORKSPACE`, `AG_LLM_API_KEY`, etc.

### 5. Test Suite (`tests/`)
- `tests/test_sanity.py` — 6 tests for package imports
- `tests/test_cli.py` — 13 tests for CLI help, manual mode gate, run command options

### 6. Additional Files
- `README.md` — Quick start guide
- `.gitignore` — Python, IDE, and ag-specific ignores

---

## Commands to Run

```powershell
# Navigate to project
cd "c:\Users\Kai\OneDrive\Documents\04 Themen\Tech\Programmierung\VS Code\Agents\ag_foundation"

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install package with dev dependencies
pip install -e ".[dev]"

# Verify CLI works
ag --help
ag --version

# Run tests
pytest -v

# Run tests with coverage
pytest --cov=ag
```

---

## Test Results

```
============================= test session starts =============================
platform win32 -- Python 3.14.0, pytest-9.0.2, pluggy-1.6.0
collected 19 items

tests/test_cli.py::TestCLIHelp::test_main_help PASSED
tests/test_cli.py::TestCLIHelp::test_version PASSED
tests/test_cli.py::TestCLIHelp::test_run_help PASSED
tests/test_cli.py::TestCLIHelp::test_runs_help PASSED
tests/test_cli.py::TestCLIHelp::test_ws_help PASSED
tests/test_cli.py::TestCLIHelp::test_artifacts_help PASSED
tests/test_cli.py::TestCLIHelp::test_doctor PASSED
tests/test_cli.py::TestManualModeGate::test_manual_mode_without_env_var_fails PASSED
tests/test_cli.py::TestManualModeGate::test_manual_mode_with_env_var_succeeds PASSED
tests/test_cli.py::TestManualModeGate::test_llm_mode_without_env_var_succeeds PASSED
tests/test_cli.py::TestRunCommand::test_run_with_prompt PASSED
tests/test_cli.py::TestRunCommand::test_run_with_workspace_option PASSED
tests/test_cli.py::TestRunCommand::test_run_with_playbook_option PASSED
tests/test_sanity.py::test_import_ag PASSED
tests/test_sanity.py::test_import_cli PASSED
tests/test_sanity.py::test_import_core PASSED
tests/test_sanity.py::test_import_storage PASSED
tests/test_sanity.py::test_import_skills PASSED
tests/test_sanity.py::test_import_config PASSED

============================= 19 passed in 0.48s ==============================
```

---

## Acceptance Criteria Checklist

| Criteria | Status | Evidence |
|----------|--------|----------|
| `pyproject.toml` exists with supported Python version + dependency groups | ✅ | [pyproject.toml](../../pyproject.toml) |
| Standard layout: `src/ag/` + `tests/` | ✅ | Directory structure above |
| `pytest -q` passes (≥1 sanity test) | ✅ | 19 tests passed |
| `ag --help` works via console-script | ✅ | Output shown above |
| Placeholder config defined (location + schema) | ✅ | [src/ag/config.py](../../src/ag/config.py) |
| Handoff note in `/docs/dev/handoff/` | ✅ | This file |

---

## Structure Decisions

1. **Build system:** Chose `hatchling` for modern Python packaging (PEP 517/518 compliant, minimal config).

2. **Source layout:** Used `src/` layout per Python packaging best practices — prevents accidental imports from uninstalled code.

3. **CLI framework:** Chose `typer` per ARCHITECTURE.md recommendation — minimal ceremony, rich integration.

4. **Config location:** `~/.ag/config.yaml` with `AG_CONFIG_PATH` override — follows XDG-like conventions on Unix, adapts for Windows.

5. **Manual mode gate:** Environment variable `AG_DEV=1` rather than build-time flag — simpler to test and document.

---

## Dependencies on This Work

AF-0005, AF-0006, AF-0007, AF-0008 all depend on this bootstrap being complete:
- Schemas go in `src/ag/core/`
- Storage goes in `src/ag/storage/`
- Runtime modules go in `src/ag/core/`
- CLI implementation extends `src/ag/cli/main.py`

---

## Open Items / Notes for Reviewers

1. **No real config parsing:** Config contract is documented but not implemented. Real parsing deferred to future AF.

2. **All commands are stubs:** `ag run` and other commands print stub messages. Real implementation in AF-0007/AF-0008.

3. **Python version:** Requires Python 3.10+. Tested on Python 3.14.0.

4. **No change_playbooks or ADRs updated:** This is a bootstrapping PR; no architectural decisions beyond tooling.
