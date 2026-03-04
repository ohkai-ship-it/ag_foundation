# Completion Note — AF-0019 — Agent network playbook v0: delegation
# Version number: v0.1

> Strict template. Fill every section. If something is not applicable, write **N/A** (do not delete sections).

## 1) Metadata
- **Backlog item (primary):** AF-0019
- **PR:** N/A (direct commit)
- **Author:** Jacob
- **Date:** 2026-02-26
- **Branch:** feat/delegation-playbook
- **Risk level:** P0
- **Runtime mode used for verification:** manual (dev/test-only)

## 2) Goal and acceptance criteria
### Goal (from backlog item)
Ship a v0 delegated playbook (still linear) where Planner produces multiple subtasks, Executor runs them (via skill or LLM), Verifier evaluates, Recorder persists a multi-step RunTrace showing delegation.

### Acceptance criteria (from backlog item)
- [x] A new playbook exists (`delegate_v0`) that produces ≥5 steps: normalize, plan, execute_subtask_1, execute_subtask_2, verify, finalize.
- [x] Planner produces at least two subtasks (simple heuristic) and records them in the trace.
- [x] Executor executes subtasks using: (a) stub skill in manual mode, (b) provider-backed call in LLM mode.
- [x] Verifier records pass/fail and evidence pointers in trace.
- [x] Integration tests exist for: manual delegated run and (mocked) LLM delegated run.
- [x] CLI can run delegated playbook and `ag runs show --json` displays full multi-step trace.

## 3) What changed (file-level)
- `src/ag/core/playbooks.py` — Added `DELEGATE_V0` playbook with 6 steps (normalize, plan, execute_subtask_1, execute_subtask_2, verify, finalize)
- `src/ag/core/run_trace.py` — Added `Subtask` model (subtask_id, description, status, result_summary), added `StepType.PLANNING` enum value, added `Step.subtasks` optional field
- `src/ag/core/runtime.py` — Added subtask tracking in orchestrator for delegation flows
- `src/ag/skills/registry.py` — Added 5 delegation skills (normalize_input, plan_subtasks, execute_subtask, verify_delegation, finalize_result)
- `tests/test_delegation.py` — New file: 23 tests for delegation playbook

## 4) Architecture alignment (mandatory)
- **Layering:** Core runtime + skills; no adapter changes
- **Interfaces touched:** Playbook, Step, RunTrace (extended with Subtask)
- **Backward compatibility:** Yes, additive changes only; existing playbooks unchanged

## 5) Truthful UX check (mandatory)
- **User-visible labels affected:** Step names in trace, subtask details
- **Trace fields backing them:** `step.name`, `step.subtasks[]`, `subtask.status`, `subtask.result_summary`
- **Proof:** `ag runs show --json <run_id>` shows 6 steps with subtask details in plan step

## 6) Tests executed (mandatory)
- Command: `pytest tests/test_delegation.py -v`
  - Result: PASS (23 tests)
- Command: `pytest tests/ -v`
  - Result: PASS (173 passed, 1 deselected)

## 7) Run evidence (mandatory for behavior changes)
- **RunTrace ID(s):** Generated during test runs
- **How to reproduce the run:**
  ```powershell
  $env:AG_DEV = "1"
  ag run "Test delegation" --playbook delegate_v0 --json
  ```
- **Expected trace outcomes:**
  - 6 steps: normalize, plan, execute_subtask_1, execute_subtask_2, verify, finalize
  - Plan step contains `subtasks` array with 2+ subtasks
  - Each subtask has `subtask_id`, `description`, `status`
  - Verify step has `passed` field

## 8) Artifacts (if applicable)
**N/A**

## 9) Risks, tradeoffs, and follow-ups
- **Risks introduced:** None
- **Tradeoffs made:** Delegation is still linear (no branching); subtask count is heuristic-based
- **Follow-up backlog items or bugs to create:** Consider dynamic subtask generation based on task complexity

## 10) Reviewer checklist (copy/paste)
- [x] I can map PR → AF item and see acceptance criteria satisfied
- [x] I can verify truthful labels from RunTrace
- [x] I can reproduce a run (or it's docs-only)
- [x] Tests were run and results are documented
- [x] Any contract changes are documented in cornerstone docs
