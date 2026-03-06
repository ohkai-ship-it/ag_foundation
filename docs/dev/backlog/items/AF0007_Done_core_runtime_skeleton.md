# AF0007 — Core runtime skeleton v0 (interfaces + v0 playbook + stub skills) producing RunTrace
# Version number: v0.3

## Metadata
- **ID:** AF-0007
- **Type:** Foundation
- **Status:** DONE
- **Priority:** P0
- **Area:** Kernel
- **Owner:** Jacob
- **Completed in:** Sprint 01
- **Completion date:** 2026-02-24

## Problem
Need a working pipeline, but we must lock down interface style, method signatures, playbook definition strategy, and skill/tool behavior to avoid rework.

## Goal
Implement minimal sequence-only runtime with explicit interfaces and v0 implementations, using one hardcoded v0 playbook and a stub skill registry, producing a persisted RunTrace.

## Non-goals
- Branching/loops.
- Real LLM calls.
- Multi-agent delegation beyond linear steps.

## Acceptance criteria (Definition of Done)
- [x] Interfaces are defined in `ag/core/interfaces.py` for: Normalizer, Planner, Orchestrator, Executor, Verifier, Recorder.
- [x] Interfaces use `typing.Protocol` (preferred) or `abc.ABC` (acceptable) — consistent and documented.
- [x] Exactly one hardcoded playbook `default_v0` exists in `ag/core/playbooks.py` (or equivalent).
- [x] `default_v0` is linear; all steps default to `reasoning_mode='balanced'`.
- [x] Executor uses a stub skill registry (`ag/skills/registry.py`) with at least one test skill (e.g., `echo_tool`).
- [x] Happy-path integration test exercises all modules and persists a valid RunTrace.
- [x] Failure-path integration test: missing skill or forced step error stops orchestration, records error, marks run failed.

## Implementation notes
- Playbooks are hardcoded in v0; defer YAML/JSON loading.
- Orchestrator is a simple loop.
- Verifier v0 can be basic; retries/repairs hardcoded to 0 or 1 (document).

## Risks
P1: interface drift. Mitigate by locking signatures early and enforcing with tests/type checks.

## PR plan
1. PR (feat/runtime-skeleton): Add interfaces + v0 playbook + stub skills + runtime loop + integration tests.

---
# Completion section (fill when done)

**Completion date:** 2026-02-24  
**Author:** Jacob (Junior Engineer)

**Summary:**
Implemented the core runtime skeleton with explicit interfaces, v0 implementations, hardcoded `default_v0` playbook, and stub skill registry. All modules produce a persisted RunTrace.

**What Was Done:**

1. **Runtime Interfaces** (`src/ag/core/interfaces.py`)
   - 6 interfaces using `typing.Protocol`: Normalizer, Planner, Orchestrator, Executor, Verifier, Recorder

2. **v0 Playbook** (`src/ag/core/playbooks.py`)
   - `default_v0` playbook with 3 sequential steps: init, execute, finalize
   - All steps use `reasoning_mode='balanced'`

3. **Skill Registry** (`src/ag/skills/registry.py`)
   - SkillRegistry class with register/get/list
   - Built-in skills: echo_tool, stub_search, stub_write_file

4. **v0 Runtime Implementations** (`src/ag/core/runtime.py`)
   - V0Normalizer, V0Planner, V0Executor, V0Verifier, V0Recorder, V0Orchestrator
   - Runtime facade and create_runtime() factory

5. **Test Suite** (`tests/test_runtime.py`)
   - 19 tests: interface protocols, playbook structure, skill registry, happy-path, failure-path

**Test Results:** 19 passed

