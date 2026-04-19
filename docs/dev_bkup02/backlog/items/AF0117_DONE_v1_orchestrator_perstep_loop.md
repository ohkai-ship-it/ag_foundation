# AF-0117 — V1 Orchestrator: per-step verification loop
# Version number: v0.4
# Created: 2026-03-21
# Status: DONE
# Priority: P1
# Area: Core Runtime / Orchestrator

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`

---

> **SCOPE SPLIT (Sprint 13/14)**
> This AF was delivered in two parts:
> - **Sprint 13 (DONE):** V1Orchestrator creation with mixed skill+playbook plan support
>   (iterates plan steps, expands `type=playbook` steps to their skill sequences inline,
>   adds `PLAYBOOK` to `PlaybookStepType` enum). Co-delivered with AF-0103 (V2Planner).
> - **Sprint 14 (DONE):** Per-step verification wiring (V1Executor + V1Verifier integration,
>   `VERIFICATION` steps in trace, stop/continue decisions per step).

---

## Summary

Upgrade V0Orchestrator to handle mixed skill+playbook plans (Sprint 13) and run verification **after each step** instead of once at the end (Sprint 14). The full AF wires V1Executor (output validation, AF-0116) and V1Verifier (step-aware, AF-0115) into a per-step feedback loop, making the runtime match the architecture diagram: `TaskSpec → Planner → Orchestrator → Executor → Skill → Verifier → Recorder`. Sprint 13 portion depends on AF-0114 (extraction) and AF-0115 (V1 Verifier). Sprint 14 portion additionally depends on AF-0116 (V1 Executor).

---

## Problem

V0Orchestrator's step loop is fire-and-forget:

```
for step in playbook.steps:
    result = executor.execute(step)     # execute
    steps.append(result)                # record
                                        # ← no verification here
# after all steps:
verifier.verify(steps, final_status)    # verify once at end
```

This means:
1. Bad output from step N chains to step N+1 before anyone checks it
2. The only verification is a post-hoc error scan at the end
3. The architecture diagram (`Skill → Verifier → Recorder` per step) doesn't match reality

---

## Goal

- Verification runs after each step, before output chains to the next step
- Failed required step → stop execution (existing behavior, now with richer error data)
- Failed optional step → continue, but record verification result (BUG-0017 fix)
- Verification results visible as `VERIFICATION` steps interleaved with `SKILL_CALL` steps in trace (Option A — interleaved, decided 2026-03-22: preserves causal ordering in the trace event log; callers can filter by `StepType` when they only want skill steps)
- Runtime flow matches architecture: `Executor → Verifier → Recorder` per step

---

## Non-goals

- **Replanning on failure** (Gate C condition #2) — V1 Orchestrator stops on required failure; replanning requires Orchestrator → Planner loop, which is V2 Orchestrator / Gate C scope
- LLM calls inside the orchestrator — intelligence lives in Planner, Executor, and Verifier
- Parallel step execution — V1 is still sequential

---

## Design

### V1 Orchestrator step loop

```python
class V1Orchestrator:
    def run(self, task_spec, playbook):
        plan = self._planner.plan(task_spec)
        steps = []
        accumulated_result = {}

        for playbook_step in plan.steps:
            # Execute
            step_result = self._executor.execute(
                playbook_step.skill_name,
                playbook_step.parameters | accumulated_result,
                ctx
            )

            # Record step (with required flag)
            step = self._record_step(step_result, playbook_step)
            steps.append(step)

            # Verify per-step
            verification = self._verifier.verify_step(step)
            verification_step = self._record_verification(verification, step)
            steps.append(verification_step)

            # Decision: continue or stop?
            if not verification.passed:
                if playbook_step.required:
                    final_status = FinalStatus.FAILURE
                    break
                # Optional: continue despite failure

            # Chain output to next step
            accumulated_result.update(step_result.output_data)

        # End-of-run verification (summary)
        final_verification = self._verifier.verify(steps, final_status)
        self._recorder.record(trace, final_verification)
```

### Key changes vs V0

| Aspect | V0 | V1 |
|--------|-----|-----|
| Verification timing | Once at end | After each step + summary at end |
| Step recording | Step only | Step + VERIFICATION step in sequence |
| Optional step failure | Continues but verifier fails later (BUG-0017) | Continues, verification marks it as optional skip |
| Required step failure | Sets final_status, breaks loop | Same, but with verification evidence |
| Output chaining | Unconditional | Only chains if verification passed or step is optional |

### Trace shape (before vs after)

**V0 trace:**
```
Step 0: SKILL_CALL (load_documents) — error: "No files found"
Step 1: SKILL_CALL (web_search) — ok
Step 2: SKILL_CALL (fetch_web_content) — ok
Step 3: SKILL_CALL (synthesize_research) — ok
Step 4: SKILL_CALL (emit_result) — ok
Verifier: failed (Step 0 failed: No files found)   ← contradicts success
```

**V1 trace:**
```
Step 0: SKILL_CALL (load_documents) — error: "No files found"
Step 1: VERIFICATION — optional step 0 failed, continuing
Step 2: SKILL_CALL (web_search) — ok
Step 3: VERIFICATION — passed
Step 4: SKILL_CALL (fetch_web_content) — ok
Step 5: VERIFICATION — passed
Step 6: SKILL_CALL (synthesize_research) — ok
Step 7: VERIFICATION — passed
Step 8: SKILL_CALL (emit_result) — ok
Step 9: VERIFICATION — passed
Verifier: passed (5/5 required steps ok, 1 optional skipped)
```

### Files touched

| File | Change |
|------|--------|
| `src/ag/core/orchestrator.py` | V1Orchestrator with per-step verification loop |
| `src/ag/core/verifier.py` | Add `verify_step(step) -> StepVerification` method to V1Verifier |
| `src/ag/core/runtime.py` | Wire V1Orchestrator with V1Executor + V1Verifier + V1Recorder |
| `tests/test_runtime.py` | Tests: interleaved VERIFICATION steps in trace, optional pass-through, required failure stops |

### Dependency chain

```
AF-0114 (extract V0s)
    ├── AF-0115 (V1 Verifier) ──┐
    ├── AF-0116 (V1 Executor) ──┼── AF-0117 (V1 Orchestrator) ← this AF
    └── AF-0118 (V1 Recorder) ──┘
```

---

## Gate C alignment

This AF implements the **structural prerequisite** for Gate C condition #2 (replanning on step failure). V1 Orchestrator detects failure per-step and stops. V2 Orchestrator would replace "stop" with "call Planner to replan," creating the Verifier → Planner loop. The per-step verification loop is the foundation that makes replanning possible.

| Gate C Condition | This AF | Future |
|---|---|---|
| (2) Replanning on step failure | Per-step failure **detection** | V2 Orchestrator: detection → Planner replan loop |

---

## Acceptance criteria

- [ ] Verification runs after each step (not just end of run)
- [ ] `VERIFICATION` steps appear in trace interleaved with `SKILL_CALL` steps
- [ ] Optional step failure: verification records skip, orchestrator continues
- [ ] Required step failure: verification records failure, orchestrator stops
- [ ] Output only chains to next step after verification passes (or step is optional)
- [ ] End-of-run summary verification still runs
- [ ] `ag runs show <id>` displays interleaved SKILL_CALL + VERIFICATION steps
- [ ] `pytest -W error` passes
- [ ] `ruff check src tests` passes

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Step count doubles (each skill + verification) | Trace verbosity | VERIFICATION steps are lightweight; `ag runs show` can group them |
| V1Verifier.verify_step() is a new protocol method | Interface expansion | Additive method; V0Verifier doesn't need it (only used by V1Orchestrator) |
| Depends on AF-0114, AF-0115, AF-0116 | Blocked if prerequisites incomplete | Sequence sprints: AF-0114 first, then AF-0115+0116, then AF-0117 |

---

# Completion section (fill when done)

## 1) Metadata
- **Backlog item (primary):** AF-0117
- **PR:** #<number>
- **Author:** <name>
- **Date:** YYYY-MM-DD
- **Branch:** feat/v1-orchestrator
- **Risk level:** P1
- **Runtime mode used for verification:** llm + manual

## 2–10) (fill when done per template)
