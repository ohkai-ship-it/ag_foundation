# BUG REPORT — BUG-0020 — Empty plan reports success
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI discipline (ruff + pytest -W error + coverage)
> - INDEX update rule (status ↔ filename integrity)
> - Evidence capture requirement (RunTrace ID for CLI/runtime bugs)

> **File naming (required):** `BUG####_<STATUS>_<three_word_description>.md`
> Status values: `OPEN | IN_PROGRESS | FIXED | VERIFIED | DROPPED`

---

## Metadata
- **ID:** BUG-0020
- **Status:** FIXED
- **Severity:** P0
- **Area:** Core Runtime / Orchestrator / Verifier / CLI
- **Reported by:** Kai
- **Date:** 2026-03-22
- **Related backlog item(s):** AF-0121 (V3Planner implementation), AF-0117 (V1Orchestrator)
- **Related ADR(s):** ADR-0009 (V3Planner feasibility design)
- **Related PR(s):** —

---

## Summary

When the V2Planner correctly identifies that no skills or playbooks can handle a task (e.g., "Read my email"), it returns a plan with zero steps and a warning. The pipeline proceeds to execute the empty plan: the CLI shows an empty table and still asks "Execute this plan? [Y/n]", the orchestrator loops over zero steps, the verifier reports `passed` (no failures), and the final status is `success`. A run that did **nothing** should not report success.

---

## Expected behavior

When the planner returns a plan with zero executable steps:
- The CLI should display a clear message: "No available skills or playbooks can handle this task"
- The CLI should **not** prompt "Execute this plan?" for an empty plan
- If execution does proceed (e.g., via `--yes`), the run status should be `not_feasible` or `failure`, not `success`
- The verifier should not pass a run with zero executed steps

---

## Actual behavior

```
Plan ID: plan_b06a8fdbfa1d
Task: Read my email
Confidence: 85%
Warnings: No available playbooks or skills match the task 'Read my email'.

Proposed execution:
┏━━━━━┳━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ #   ┃ Skill ┃ Est. Tokens ┃ Policy Flags ┃ Status ┃
┡━━━━━╇━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━┩
└─────┴───────┴─────────────┴──────────────┴────────┘

Execute this plan? [Y/n]

Run completed
  Status: success
  Verifier: passed
```

---

## Reproduction steps

1. Run: `ag run "Read my email"` (or any task with no matching skills/playbooks)
2. Confirm plan execution when prompted
3. Observe: `Status: success`, `Verifier: passed`

---

## Evidence

- **RunTrace ID:** `86ebd367-8efd-434a-a8f6-587c618fe560`
- **CLI output:** See "Actual behavior" above
- **Environment:** Windows 11, Python 3.14.0a6, Sprint 14 branch

---

## Impact

**Truthful UX violation.** The system reports success for a task it cannot perform. Users believe their request was handled when nothing happened. This is the most basic form of misleading output — a no-op presented as success.

---

## Root cause

Three components contribute:

1. **CLI (`main.py`):** `_display_plan()` renders an empty table and prompts Y/n with no guard for zero steps
2. **V1Orchestrator:** `run()` loops over `expanded_playbook.steps` — empty list means no work, but `final_status` defaults to `FinalStatus.SUCCESS` at initialization
3. **V1Verifier:** `verify_components()` iterates over steps — with zero steps, no failures are found, so it returns `passed`

---

## Proposed fix

**Quick guard (Sprint 15, P0):**
1. In `V1Orchestrator.run()`: if `len(expanded_playbook.steps) == 0`, set `final_status = FinalStatus.FAILURE` with reason "No executable steps in plan"
2. In CLI inline plan flow: if `len(plan.planned_steps) == 0`, display "Nothing to execute — no skills or playbooks match this task" and skip the Y/n prompt
3. In V1Verifier: if `len(steps) == 0`, return `("failed", "No steps executed")`

**Structural fix (Sprint 15, AF-0121):**
V3Planner (ADR-0009) evaluates feasibility *before* planning. A `NOT_FEASIBLE` assessment prevents execution entirely, making the guard above a safety net rather than the primary defense.

---

## Acceptance criteria

- [ ] `ag run "Read my email"` does NOT report `Status: success`
- [ ] CLI shows clear "not feasible" message for tasks with no matching capabilities
- [ ] Empty-plan runs are recorded with appropriate failure status in trace
- [ ] V1Verifier fails runs with zero executed steps
- [ ] Regression: runs with actual steps still pass normally
- [ ] `pytest -W error` passes
- [ ] `ruff check src tests` passes

---

## Status log
- 2026-03-22 — Opened by Kai (reproduced with run `86ebd367-8efd-434a-a8f6-587c618fe560`)
