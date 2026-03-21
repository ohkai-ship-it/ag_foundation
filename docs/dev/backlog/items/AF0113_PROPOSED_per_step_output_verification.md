# AF-0113 — Per-step skill output verification
# Version number: v0.1
# Created: 2026-03-21
# Status: PROPOSED (superseded)
# Priority: P1
# Area: Core Runtime/Verifier/Skills

> **⚠️ SUPERSEDED:** This AF has been decomposed into focused component AFs:
> - **AF-0114** — Extract pipeline V0s to own files (structural prerequisite)
> - **AF-0115** — V1 Verifier: step-aware verification (fixes BUG-0017)
> - **AF-0116** — V1 Executor: output schema validation with retry (+ V2 LLM repair roadmap)
> - **AF-0117** — V1 Orchestrator: per-step verification loop (wires it all together)
> - **AF-0118** — V1 Recorder: verification evidence persistence
>
> This AF remains as the original analysis document. Implementation should follow AF-0114→0118.

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`

---

## Summary

Wire the existing SchemaValidator and per-skill output schemas into the runtime so that every skill output is validated **per-step** — not just once at the end of a run. This closes the gap between the Verifier in the architecture diagram (Skill → Verifier → Recorder) and the actual implementation, where verification is currently a single end-of-run error check.

---

## Problem

Three verification components exist but are disconnected:

| Component | Location | Status |
|-----------|----------|--------|
| **V0Verifier** | `runtime.py:260-280` | Runs once at end of run; checks only `step.error != None` and `final_status == SUCCESS` |
| **SchemaValidator** | `schema_verifier.py` | Full repair-loop engine with bounded retries, evidence recording, trace integration — **orphaned from runtime** (only used in tests) |
| **Skill output schemas** | `SkillInfo.output_schema` in `registry.py:42` | Every skill declares an output schema — **never validated at runtime** |

### Concrete consequences

1. **Malformed LLM output chains forward silently.** If a skill returns data that doesn't match its declared `output_schema`, the next step receives garbage. The error surfaces later (or never), making root cause analysis difficult.

2. **The architecture diagram is a lie.** §3.4.2 Execution Flow shows `Skill → Verifier → Recorder`. The actual flow is `Skill → Recorder` — the Verifier runs once after all steps are done and only checks for crash-level errors.

3. **Input validation is enforced, output validation is not.** `registry.py:136-139` validates inputs against `skill_info.input_schema`. The same `skill_info.output_schema` exists on the next line but is never used. This is an asymmetry that wastes a declared contract.

4. **StepType.VERIFICATION exists but is never emitted.** `run_trace.py:63` defines `VERIFICATION` as a step type. No runtime code ever creates a step with this type. The SchemaValidator's `record_validation_steps()` does — but it's never called.

5. **No repair opportunity.** The SchemaValidator supports bounded repair loops (up to 10 attempts, AF-0055). Without wiring, there is no chance to re-invoke a skill when its output is invalid — the bad output is accepted and persisted.

---

## Goal

After this AF:
- Every skill execution is followed by output schema validation
- Validation results are recorded as `VERIFICATION` steps in the run trace
- Failed validation triggers a bounded repair loop (re-invoke skill, not LLM repair)
- The V0Verifier end-of-run check still runs (unchanged) as a final safety net
- The runtime flow matches the architecture: `Skill → Verifier → Recorder`

---

## Non-goals

- **LLM-powered output repair** — repair means re-invoking the skill, not asking an LLM to fix the output. LLM repair is a V2+ Verifier concern.
- **Acceptance criteria beyond schema** — quality checks ("summary must be >100 words"), semantic validation, or business rules. Those are future Verifier capabilities.
- **Planner-level verification fields** — adding `expected_output` or `acceptance_criteria` to `PlannedStep`/`LLMPlanResponse`. That belongs to V3Planner (AF-0104).
- **Changing the Verifier Protocol** — the existing `Verifier.verify(trace)` protocol stays. Per-step validation is an internal orchestrator concern, not a protocol change.

---

## Design

### Integration point: inside the step execution loop

The wiring belongs in `V0Orchestrator.run()` (runtime.py:360-531), immediately after a skill returns its output and before the result is added to `accumulated_result`.

**Current flow (per step):**
```
skill.execute(input, ctx) → output
output.to_legacy_tuple() → (success, summary, data)
data added to accumulated_result
Step recorded in trace
```

**Proposed flow (per step):**
```
skill.execute(input, ctx) → output
validate output against skill_info.output_schema      ← NEW
  if invalid:
    retry skill.execute (bounded, default 2 retries)   ← NEW
    record VERIFICATION step (failed → repaired)        ← NEW
  if still invalid after retries:
    record VERIFICATION step (failed)                   ← NEW
    mark step as failed, skip remaining steps            ← NEW
  if valid:
    record VERIFICATION step (passed)                   ← NEW
output.to_legacy_tuple() → (success, summary, data)
data added to accumulated_result
Step recorded in trace
```

### Key design decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Where to validate | Orchestrator (after skill execute, before chaining) | Keeps Executor/Skill unchanged; verifier is an orchestrator concern |
| What to validate against | `SkillInfo.output_schema` from registry | Already declared by every skill; no new schema work needed |
| Validation engine | `SchemaValidator` from `schema_verifier.py` | Already built, bounded, evidence-producing; just needs to be called |
| Repair strategy | Re-invoke same skill with same input | Simplest idempotent retry; LLM repair is out of scope |
| Max retries | 2 (total 3 attempts including initial) | Matches `DEFAULT_MAX_VALIDATION_ATTEMPTS` |
| On final failure | Fail the step, abort remaining steps | Consistent with current `required=True` behavior |
| Trace recording | One `VERIFICATION` step per validation attempt | Uses existing `StepType.VERIFICATION` and `record_validation_steps()` |
| End-of-run verifier | Unchanged | V0Verifier still runs; per-step validation is additive |

### Files touched

| File | Change |
|------|--------|
| `src/ag/core/runtime.py` | V0Orchestrator.run(): add output validation after skill execute (~20 lines). Import SchemaValidator. |
| `src/ag/skills/registry.py` | Add `get_skill_info(name) -> SkillInfo` public method (if not already exposed) so orchestrator can access output_schema. Registry.execute() stays unchanged. |
| `tests/test_schema_verifier.py` | Add integration tests: valid output passes, invalid output triggers retry, exhausted retries fail the step |
| `tests/test_runtime.py` | Add orchestrator-level tests: run with valid skill output, run with invalid skill output, verify VERIFICATION steps in trace |

### Files NOT touched

| File | Why unchanged |
|------|---------------|
| `src/ag/core/interfaces.py` | Verifier Protocol unchanged — per-step validation is internal |
| `src/ag/core/schema_verifier.py` | Already has everything needed; no changes |
| `src/ag/skills/base.py` | SkillOutput unchanged |
| `src/ag/skills/*.py` | Individual skills unchanged — they already declare output_schema |
| `src/ag/core/run_trace.py` | StepType.VERIFICATION already exists; no changes |
| `src/ag/core/planner.py` | No planner changes — validation is a runtime concern |

---

## Acceptance criteria

### Functional
- [ ] After each skill execution, output is validated against `SkillInfo.output_schema`
- [ ] Valid output: a `VERIFICATION` step with `status=passed` is recorded in the trace
- [ ] Invalid output: skill is re-invoked (up to 2 retries, 3 total attempts)
- [ ] Exhausted retries: step is marked failed, remaining steps are skipped
- [ ] Repair attempt: each retry records a `VERIFICATION` step with `repaired=true`
- [ ] V0Verifier end-of-run check still runs and produces the same results as before
- [ ] Run trace contains interleaved `SKILL_CALL` and `VERIFICATION` steps (visible in `ag runs show`)

### Non-functional
- [ ] `ruff check src tests`
- [ ] `ruff format --check src tests`
- [ ] `pytest -W error` — all existing tests still pass
- [ ] Coverage: new code has ≥90% branch coverage
- [ ] No performance regression in test suite (<10% slowdown)

### Trace evidence
- [ ] `ag runs show <run_id>` displays VERIFICATION steps after each SKILL_CALL
- [ ] Failed validation run shows retry attempts in trace
- [ ] All VERIFICATION steps have `evidence_refs` with schema name and attempt number

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Existing skill outputs don't match their declared schemas | All runs fail on validation | Run all skills through schema validation in a pre-flight test before merging; fix any schema drift first |
| Retry re-invokes LLM skills (cost) | Extra LLM calls on invalid output | Default 2 retries is conservative; LLM skills already have token budgets. Log retry count in trace for cost visibility. |
| `to_legacy_tuple()` loses schema information | Validation must happen before tuple conversion | Validate the SkillOutput object directly, before `to_legacy_tuple()` |
| Playbook steps marked `required=False` should tolerate validation failure | Optional steps silently swallowed | Respect `required` flag: if `required=False` and validation fails after retries, log warning and continue |

---

## Gate C alignment

This AF addresses **Gate C condition #2** (replanning on step failure) at the lowest level: detecting that a step produced invalid output before it chains forward. It does not implement replanning (that's an Orchestrator ↔ Planner loop, future work), but it provides the detection signal that would trigger replanning.

| Gate C Condition | This AF's contribution |
|---|---|
| (1) Mature policy engine | — |
| (2) Replanning on step failure | Provides the **failure detection** signal (output schema mismatch) |
| (3) Feasibility judgment | — |
| (4) Strategy justification in trace | VERIFICATION steps with evidence_refs |
| (5) Controlled extensibility | — |

---

# Completion section (fill when done)

## 1) Metadata
- **Backlog item (primary):** AF-0113
- **PR:** #<number>
- **Author:** <name>
- **Date:** YYYY-MM-DD
- **Branch:** <feat/... | fix/... | chore/...>
- **Risk level:** P1
- **Runtime mode used for verification:** llm | manual (dev/test-only)

---

## 2) Acceptance criteria verification
- [ ] After each skill execution, output is validated against `SkillInfo.output_schema`
- [ ] Valid output: a `VERIFICATION` step with `status=passed` is recorded in the trace
- [ ] Invalid output: skill is re-invoked (up to 2 retries, 3 total attempts)
- [ ] Exhausted retries: step is marked failed, remaining steps are skipped
- [ ] Repair attempt: each retry records a `VERIFICATION` step with `repaired=true`
- [ ] V0Verifier end-of-run check still runs
- [ ] Run trace contains interleaved `SKILL_CALL` and `VERIFICATION` steps
- [ ] `ruff check src tests`
- [ ] `ruff format --check src tests`
- [ ] `pytest -W error`
- [ ] Coverage ≥90% on new code
- [ ] `ag runs show <run_id>` displays VERIFICATION steps
- [ ] Failed validation run shows retry attempts in trace

---

## 3) What changed (file-level)
- `<path/to/file>` — ...

---

## 4) Architecture alignment (mandatory)
- **Layering:** Core Runtime (Orchestrator calls SchemaValidator after Executor returns skill output)
- **Interfaces touched:** Orchestrator (internal change), Verifier (unchanged contract), Recorder (receives VERIFICATION steps)
- **Backward compatibility:** No contract/schema changes. New VERIFICATION steps in traces are additive. Existing traces remain valid.

---

## 5) Truthful UX check (mandatory when user-visible)
- **User-visible labels affected:** `ag runs show` will display new VERIFICATION steps
- **Trace fields backing them:** `Step.step_type = "verification"`, `Step.evidence_refs`
- **Proof:** point to `ag runs show <run_id>` fields demonstrating truthfulness

---

## 6) Tests executed (mandatory unless docs-only)
- Command: `pytest -W error`
  - Result: PASS/FAIL
- Command: `ruff check src tests`
  - Result: PASS/FAIL

---

## 7) Run evidence (mandatory for behavior changes)
- **RunTrace ID(s):** `run_...`
- **How to reproduce:** `ag run --playbook summarize_v0 -w <workspace>`
- **Expected trace outcomes:**
  - Each SKILL_CALL step followed by a VERIFICATION step
  - VERIFICATION steps show `status=passed` and schema name in evidence_refs
  - End-of-run verifier result unchanged

---

## 8) Artifacts (if applicable)
- N/A

---

## 9) Risks, tradeoffs, follow-ups
- **Risks introduced:** Extra LLM calls on retry (bounded at 2)
- **Tradeoffs made:** Schema-only validation (no semantic quality checks)
- **Follow-up items to create:**
  - AF-____ V1Verifier: semantic/quality output validation (LLM-powered)
  - AF-____ Planner acceptance criteria fields (V3Planner, see AF-0104)

---

## 10) Reviewer checklist (copy/paste)
- [ ] I can map PR → AF-0113 and see acceptance criteria satisfied
- [ ] I can verify VERIFICATION steps in RunTrace
- [ ] I can reproduce a run and see VERIFICATION steps in `ag runs show`
- [ ] Tests were run and results are documented
- [ ] No contract/schema changes (additive only)
