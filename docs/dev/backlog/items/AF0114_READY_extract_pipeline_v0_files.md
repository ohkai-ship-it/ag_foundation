# AF-0114 — Extract pipeline V0s to own files
# Version number: v0.1
# Created: 2026-03-21
# Status: READY
# Priority: P1
# Area: Core Runtime / Refactor

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`

---

## Summary

Extract V0Orchestrator, V0Executor, V0Verifier, and V0Recorder from `runtime.py` into dedicated files: `orchestrator.py`, `executor.py`, `verifier.py`, `recorder.py`. Pure structural refactor — zero behavior change. This mirrors the existing pattern where V1Planner lives in `planner.py` and TaskSpec lives in `task_spec.py`.

---

## Problem

All four pipeline components (Orchestrator, Executor, Verifier, Recorder) are defined in a single 600+ line `runtime.py`. This creates:

1. **File bloat** — `runtime.py` mixes assembly/wiring with four distinct implementations
2. **V1 friction** — upgrading any component to V1 means editing a shared file, increasing merge conflicts and cognitive load
3. **Inconsistency** — Planner already has its own file (`planner.py`), TaskSpec has its own (`task_spec.py`), but the other four components don't

After extraction, `runtime.py` becomes the **composition root** — it wires components together but doesn't implement them.

---

## Goal

- Each pipeline component has its own file in `src/ag/core/`
- `runtime.py` only contains assembly/wiring logic
- All existing tests pass without modification (or with import-only changes)
- No behavior change whatsoever

---

## Non-goals

- V1 implementations (separate AFs: AF-0115 through AF-0118)
- Protocol/interface changes
- New tests (existing tests must pass; structure tests optional)

---

## Design

### Target file structure

```
src/ag/core/
├── interfaces.py        # Protocols (unchanged)
├── task_spec.py         # TaskSpec (unchanged)
├── planner.py           # V0Planner, V1Planner (V0Planner moves here from runtime.py)
├── orchestrator.py      # V0Orchestrator (extracted from runtime.py)
├── executor.py          # V0Executor (extracted from runtime.py)
├── verifier.py          # V0Verifier (extracted from runtime.py)
├── recorder.py          # V0Recorder (extracted from runtime.py)
├── runtime.py           # Composition root: create_runtime(), wire dependencies
├── run_trace.py         # RunTrace, Step, etc. (unchanged)
├── playbook.py          # Playbook, PlaybookStep (unchanged)
├── execution_plan.py    # ExecutionPlan (unchanged)
└── schema_verifier.py   # SchemaValidator (unchanged)
```

### Dependency graph (after extraction)

```
executor.py      (depends on: skills/registry, interfaces)
verifier.py      (depends on: run_trace, interfaces)
recorder.py      (depends on: storage, run_trace, interfaces)
     ↑ ↑ ↑
orchestrator.py  (depends on: executor, verifier, recorder, planner, run_trace)
     ↑
runtime.py       (imports all, wires together, exports create_runtime())
```

### Migration steps

1. Create `executor.py` — move `V0Executor` class, update imports
2. Create `verifier.py` — move `V0Verifier` class, update imports
3. Create `recorder.py` — move `V0Recorder` class, update imports
4. Create `orchestrator.py` — move `V0Orchestrator` class, update imports
5. Move `V0Planner` from `runtime.py` to `planner.py` (alongside V1Planner)
6. Update `runtime.py` — keep only `create_runtime()` and assembly logic
7. Update `src/ag/core/__init__.py` — re-export public symbols
8. Update all test imports if needed

### Files touched

| File | Change |
|------|--------|
| `src/ag/core/executor.py` | **New** — V0Executor extracted |
| `src/ag/core/verifier.py` | **New** — V0Verifier extracted |
| `src/ag/core/recorder.py` | **New** — V0Recorder extracted |
| `src/ag/core/orchestrator.py` | **New** — V0Orchestrator extracted |
| `src/ag/core/planner.py` | V0Planner added (moved from runtime.py) |
| `src/ag/core/runtime.py` | Stripped to composition root |
| `src/ag/core/__init__.py` | Updated re-exports |
| `tests/*.py` | Import path updates only (if needed) |

---

## Acceptance criteria

- [ ] V0Orchestrator in `orchestrator.py`, V0Executor in `executor.py`, V0Verifier in `verifier.py`, V0Recorder in `recorder.py`
- [ ] V0Planner moved to `planner.py`
- [ ] `runtime.py` contains only composition/wiring logic
- [ ] All existing tests pass (`pytest -W error`)
- [ ] `ruff check src tests` and `ruff format --check src tests` pass
- [ ] No behavior change — same CLI output, same traces, same test results
- [ ] `__init__.py` re-exports maintain backward compatibility

---

## Risks

| Risk | Mitigation |
|------|------------|
| Circular imports between extracted files | Dependency graph is acyclic (verified above); interfaces.py breaks cycles |
| Test imports break | Maintain re-exports in `__init__.py`; update test imports if needed |
| Merge conflicts with in-flight work | Do this AF first in the sprint, before V1 work |

---

# Completion section (fill when done)

## 1) Metadata
- **Backlog item (primary):** AF-0114
- **PR:** #<number>
- **Author:** <name>
- **Date:** YYYY-MM-DD
- **Branch:** refactor/extract-pipeline-components
- **Risk level:** P1
- **Runtime mode used for verification:** manual (dev/test-only)

---

## 2) Acceptance criteria verification
- [ ] V0 classes in own files
- [ ] `runtime.py` is composition root only
- [ ] `pytest -W error` passes
- [ ] `ruff check src tests` passes
- [ ] No behavior change

---

## 3) What changed (file-level)
- `src/ag/core/executor.py` — NEW: V0Executor extracted
- `src/ag/core/verifier.py` — NEW: V0Verifier extracted
- `src/ag/core/recorder.py` — NEW: V0Recorder extracted
- `src/ag/core/orchestrator.py` — NEW: V0Orchestrator extracted
- `src/ag/core/planner.py` — V0Planner added
- `src/ag/core/runtime.py` — stripped to wiring only
- `src/ag/core/__init__.py` — re-exports updated

---

## 4) Architecture alignment (mandatory)
- **Layering:** Core Runtime — pure structural refactor within the same layer
- **Interfaces touched:** None (Protocols unchanged)
- **Backward compatibility:** Full — re-exports maintain all existing import paths

---

## 5) Truthful UX check (mandatory when user-visible)
- N/A — no user-visible changes

---

## 6) Tests executed (mandatory unless docs-only)
- Command: `pytest -W error`
  - Result: PASS/FAIL

---

## 7) Run evidence (mandatory for behavior changes)
- N/A — pure refactor, no behavior change

---

## 8) Artifacts (if applicable)
- N/A

---

## 9) Risks, tradeoffs, follow-ups
- **Follow-up items:** AF-0115 (V1 Verifier), AF-0116 (V1 Executor), AF-0117 (V1 Orchestrator), AF-0118 (V1 Recorder)

---

## 10) Reviewer checklist (copy/paste)
- [ ] Each V0 class is in its own file
- [ ] `runtime.py` only wires components
- [ ] All tests pass with no behavior change
- [ ] Import paths work (re-exports in __init__.py)
