# AF0019 — Agent network playbook v0: delegation with multi-step trace (linear orchestration)
# Version number: v0.2

## Metadata
- **ID:** AF-0019
- **Type:** Feature
- **Status:** DONE
- **Priority:** P0
- **Area:** Kernel
- **Owner:** Jacob
- **Completed in:** Sprint 02
- **Completion date:** 2026-02-26

## Problem
Sprint 02 goal per Project Plan is agent-network behavior: multi-step delegation with clear boundaries. Current v0 playbook is a simple linear echo and doesn't demonstrate decomposition or role-like steps.

## Goal
Ship a v0 delegated playbook (still linear) where Planner produces multiple subtasks, Executor runs them (via skill or LLM), Verifier evaluates, Recorder persists a multi-step RunTrace showing delegation.

## Non-goals
- Branching/graph orchestration.
- Parallel execution.
- Long-running resumability.

## Acceptance criteria (Definition of Done)
- [x] A new playbook exists (e.g., `delegate_v0`) that produces ≥5 steps: normalize, plan, execute_subtask_1, execute_subtask_2, verify, finalize.
- [x] Planner produces at least two subtasks (simple heuristic is OK) and records them in the trace.
- [x] Executor executes subtasks using: (a) stub skill in manual mode, (b) provider-backed call in LLM mode (OpenAI).
- [x] Verifier records pass/fail and evidence pointers in trace.
- [x] Integration tests exist for: manual delegated run and (mocked) LLM delegated run.
- [x] CLI can run delegated playbook and `ag runs show --json` displays full multi-step trace.

## Implementation notes
- Keep it linear. Delegation is represented by separate planned steps with bounded inputs/outputs.
- Ensure each step has: id, kind, started/ended, status, inputs summary, outputs summary.
- Consider adding a simple `subtasks[]` field under a plan step in RunTrace metadata (additive).

## Risks
Medium: may touch schemas. Mitigate by additive-only changes and updating contract tests first.

## PR plan
1. PR (feat/delegation-playbook): Add `delegate_v0` playbook + planner changes + executor support + tests.

---
# Completion section (fill when done)

**Completion date:** 2026-02-26  
**Author:** Jacob

**Summary:**
Shipped v0 delegated playbook with multi-step delegation. Planner produces subtasks, Executor runs them, Verifier evaluates, Recorder persists multi-step RunTrace.

**What Changed:**
- `src/ag/core/playbooks.py` — Added DELEGATE_V0 playbook with 6 steps
- `src/ag/core/run_trace.py` — Added Subtask model, StepType.PLANNING, Step.subtasks field
- `src/ag/core/runtime.py` — Added subtask tracking in orchestrator
- `src/ag/skills/registry.py` — Added 5 delegation skills
- `tests/test_delegation.py` — New: 23 tests for delegation

**DELEGATE_V0 Steps:**
1. normalize
2. plan (produces subtasks)
3. execute_subtask_1
4. execute_subtask_2
5. verify
6. finalize

**Architecture Alignment:**
- Core runtime + skills
- Playbook, Step, RunTrace extended (additive)
- Backward compatible

**Truthful UX:**
- `ag runs show --json` shows 6 steps with subtask details

**Tests Executed:**
- pytest tests/test_delegation.py: PASS (23 tests)
- pytest tests/: PASS (173 passed)

**Run Evidence:**
```powershell
$env:AG_DEV = "1"
ag run "Test delegation" --playbook delegate_v0 --json
```

