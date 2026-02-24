# Handoff Note — AF-0007 — Core Runtime Skeleton v0
**Date:** 2026-02-24
**Author:** Jacob (Junior Engineer)
**Status:** Ready for review

---

## Summary
Implemented the core runtime skeleton with explicit interfaces, v0 implementations, hardcoded `default_v0` playbook, and stub skill registry. All modules produce a persisted RunTrace.

## What Was Done

### 1. Runtime Interfaces (`src/ag/core/interfaces.py`)
Defined 6 interfaces using `typing.Protocol`:
- `Normalizer`: Validates and enhances task input
- `Planner`: Selects playbook for task
- `Orchestrator`: Executes playbook steps
- `Executor`: Runs individual skills
- `Verifier`: Validates run results
- `Recorder`: Persists traces and artifacts

### 2. v0 Playbook (`src/ag/core/playbooks.py`)
- `default_v0` playbook with 3 sequential steps:
  1. `init` (reasoning)
  2. `execute` (echo_tool skill)
  3. `finalize` (reasoning)
- All steps use `reasoning_mode='balanced'`
- Linear execution only (no branching/loops)

### 3. Skill Registry (`src/ag/skills/registry.py`)
- `SkillRegistry` class with register/get/list operations
- Built-in skills:
  - `echo_tool`: Returns input unchanged (for testing)
  - `stub_search`: Stub implementation
  - `stub_write_file`: Stub implementation

### 4. v0 Runtime Implementations (`src/ag/core/runtime.py`)
- `V0Normalizer`: Creates TaskSpec from prompt
- `V0Planner`: Always returns `default_v0` playbook
- `V0Executor`: Invokes skills from registry
- `V0Verifier`: Basic validation (checks steps completed)
- `V0Recorder`: Persists traces via SQLiteRunStore
- `V0Orchestrator`: Linear step execution loop
- `Runtime`: High-level facade combining all modules
- `create_runtime()`: Factory function

### 5. Test Suite (`tests/test_runtime.py`)
19 tests covering:
- Interface protocol compliance
- Playbook structure validation
- Skill registry operations
- Happy-path integration (full runtime execution)
- Failure-path integration (missing skill, step error)

---

## Acceptance Criteria

- [x] Interfaces defined in `ag/core/interfaces.py` for: Normalizer, Planner, Orchestrator, Executor, Verifier, Recorder
- [x] Interfaces use `typing.Protocol` (consistent, documented)
- [x] Exactly one hardcoded playbook `default_v0` exists in `ag/core/playbooks.py`
- [x] `default_v0` is linear; all steps default to `reasoning_mode='balanced'`
- [x] Executor uses stub skill registry with test skill (`echo_tool`)
- [x] Happy-path integration test exercises all modules and persists valid RunTrace
- [x] Failure-path integration test: missing skill stops orchestration, records error, marks run failed

---

## Test Results

```
tests/test_runtime.py::TestInterfaces::test_normalizer_protocol PASSED
tests/test_runtime.py::TestInterfaces::test_planner_protocol PASSED
tests/test_runtime.py::TestInterfaces::test_executor_protocol PASSED
tests/test_runtime.py::TestInterfaces::test_verifier_protocol PASSED
tests/test_runtime.py::TestInterfaces::test_recorder_protocol PASSED
tests/test_runtime.py::TestInterfaces::test_orchestrator_protocol PASSED
tests/test_runtime.py::TestPlaybook::test_default_v0_exists PASSED
tests/test_runtime.py::TestPlaybook::test_default_v0_is_linear PASSED
tests/test_runtime.py::TestPlaybook::test_default_v0_reasoning_mode PASSED
tests/test_runtime.py::TestSkillRegistry::test_register_and_get_skill PASSED
tests/test_runtime.py::TestSkillRegistry::test_builtin_echo_tool PASSED
tests/test_runtime.py::TestSkillRegistry::test_list_skills PASSED
tests/test_runtime.py::TestSkillRegistry::test_missing_skill_raises PASSED
tests/test_runtime.py::TestRuntimeIntegration::test_happy_path_produces_trace PASSED
tests/test_runtime.py::TestRuntimeIntegration::test_happy_path_trace_has_steps PASSED
tests/test_runtime.py::TestRuntimeIntegration::test_happy_path_trace_persisted PASSED
tests/test_runtime.py::TestRuntimeIntegration::test_failure_path_missing_skill PASSED
tests/test_runtime.py::TestRuntimeIntegration::test_failure_path_step_error PASSED
tests/test_runtime.py::TestRuntimeIntegration::test_runtime_factory PASSED

19 passed
```

---

## Files Changed

| File | Change |
|------|--------|
| `src/ag/core/__init__.py` | Added exports for runtime classes and factory |
| `src/ag/core/interfaces.py` | New: 6 Protocol interfaces |
| `src/ag/core/playbooks.py` | New: default_v0 playbook definition |
| `src/ag/core/runtime.py` | New: v0 implementations and Runtime facade |
| `src/ag/skills/__init__.py` | Added exports for SkillRegistry |
| `src/ag/skills/registry.py` | New: SkillRegistry with builtin skills |
| `tests/test_runtime.py` | New: 19 runtime tests |

---

## Architecture Alignment

- **Layering:** Core layer (`ag.core`) - business logic and orchestration
- **Interfaces touched:** All 6 new interfaces (Normalizer, Planner, Orchestrator, Executor, Verifier, Recorder)
- **Backward compatibility:** New code, no breaking changes

---

## Branch & PR

- **Branch:** `feat/runtime-skeleton`
- **Pushed:** Yes (to origin)
