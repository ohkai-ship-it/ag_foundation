# AF0010 — Python project bootstrap (packaging + CLI stub + pytest + placeholder config)
# Version number: v0.3

## Metadata
- **ID:** AF-0010
- **Type:** Foundation
- **Status:** DONE
- **Priority:** P0
- **Area:** Repo
- **Owner:** Jacob
- **Completed in:** Sprint 01
- **Completion date:** 2026-02-24

## Problem
Repo lacks a standard Python scaffold (packaging, module layout, tests, CLI entrypoint). Without this, we can't implement runtime, storage, or CLI in a CI-friendly way.

## Goal
Establish minimal Python foundation: `pyproject.toml`, `src/` layout, installable package, pytest wiring, and an `ag` CLI stub. Also define a placeholder config location/shape for future LLM integration (not implemented).

## Non-goals
- Publishing to PyPI.
- Implementing real LLM calls.
- Heavy tooling decisions beyond what engineering docs mandate.

## Acceptance criteria (Definition of Done)
- [x] `pyproject.toml` exists with supported Python version + dependency groups (dev/test).
- [x] Standard layout exists: `src/ag/` + `tests/` (or repo-standard equivalent).
- [x] `pytest -q` passes in a clean environment (include ≥1 sanity test).
- [x] `ag --help` works via an installed console-script entrypoint and has a basic CLI test.
- [x] Placeholder config is defined: location + minimal schema (e.g., `~/.ag/config.yaml` or `AG_CONFIG_PATH`) with empty/placeholder LLM keys.
- [x] Jacob adds a short note under `/docs/dev/handoff/` describing structure decisions and commands to run.

## Implementation notes
- Keep dependencies minimal.
- No config parsing required; define the contract and document it.
- Avoid path hacks; imports must work from installed package.

## Risks
P0 risk: bikeshedding tooling. Mitigate by choosing the simplest conventional scaffold and moving on.

## PR plan
1. PR (chore/python-bootstrap): Add project scaffold + pytest + CLI stub + placeholder config contract + handoff note.

---
# Completion section (fill when done)

**Completion date:** 2026-02-24  
**Author:** Jacob (Junior Engineer)

**Summary:**
Implemented the Python project bootstrap for ag_foundation, establishing the foundational scaffold for Sprint 01 development.

**What Was Done:**

1. **Project Configuration** (`pyproject.toml`)
   - Build system: hatchling
   - Python version: >=3.10
   - Dependencies: typer, pydantic, rich
   - Dev dependencies: pytest, pytest-cov, ruff, mypy
   - Console script: `ag = "ag.cli.main:app"`

2. **Package Structure** (`src/ag/`)
   - `__init__.py`, `config.py`
   - `cli/`, `core/`, `storage/`, `skills/` subpackages

3. **CLI Stub** (`ag/cli/main.py`)
   - All command groups per CLI_REFERENCE.md
   - Manual mode gate implemented

4. **Configuration Contract** (`ag/config.py`)
   - Config location: `~/.ag/config.yaml` or `AG_CONFIG_PATH`
   - Environment variables: AG_DEV, AG_WORKSPACE, AG_LLM_API_KEY

5. **Test Suite** (`tests/`)
   - test_sanity.py: 6 tests for package imports
   - test_cli.py: 13 tests for CLI

**Commands to Run:**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
ag --help
pytest -v
```

**Test Results:** 19+ tests passed

