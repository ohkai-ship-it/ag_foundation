# BUG REPORT — BUG-0017 — Verifier ignores optional steps
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

---

## Metadata
- **ID:** BUG-0017
- **Status:** FIXED
- **Severity:** P1
- **Area:** Core Runtime / Verifier
- **Reported by:** Kai
- **Date:** 2026-03-21
- **Fixed in:** Sprint 13 (AF-0115)
- **Related backlog item(s):** AF-0115 (V1 Verifier: step-aware verification), AF-0113 (superseded)
- **Related ADR(s):** —
- **Related PR(s):** feat/sprint13-intelligent-pipeline

---

## Summary

V0Verifier fails the entire run when an optional step (`required=False`) records an error, even though the orchestrator correctly continued past the failure and the run completed successfully. This produces a contradictory trace: `Status: success` + `Verifier: failed`.

---

## Expected behavior

When a playbook step is marked `required=False` and the step fails:
- The orchestrator should continue to the next step (✅ it does)
- The run should complete with `status: success` if all required steps pass (✅ it does)
- The verifier should report `passed` because the run met all its requirements (❌ it does not)

---

## Actual behavior

The V0Verifier scans all steps for any non-null `error` field and returns `failed` on the first one it finds — regardless of whether that step was optional.

```
Run completed
  Status: success        ← orchestrator says run succeeded
  Verifier: failed       ← verifier contradicts: "Step 0 failed: No files found matching patterns"
```

The user sees two conflicting signals in the same trace output.

---

## Reproduction steps

1. Ensure workspace `ws01` has no `.md` files in `inputs/`
2. Run: `ag run --playbook research_v0 "Research the Düsseldorf meteorite"`
3. Observe output: `Status: success` but `Verifier: failed`
4. Run: `ag runs show <run_id>` — verifier message reads:
   `Step 0 failed: No files found matching patterns: ['**/*.md']`

Step 0 is `load_documents`, which is `required=False` in `research_v0`.

---

## Evidence

- **RunTrace ID:** `a4311fc6-c216-43d7-91c6-c6c4321eb982`
- **CLI output:**
  ```
  Run completed
    Run ID: a4311fc6-c216-43d7-91c6-c6c4321eb982
    Workspace: ws01
    Mode: supervised
    Autonomy: playbook
    Status: success
    Verifier: failed
    Duration: 15578ms
    Playbook: research_v0@1.1.0
  ```
- **Verifier message:** `Step 0 failed: No files found matching patterns: ['**/*.md']`
- **Environment:** Windows, Python 3.x, ag_foundation main branch (2026-03-21)

---

## Impact

- **Truthful UX violation:** The trace says both "success" and "failed" — contradictory labels.
- **User confusion:** Every `research_v0` run without local docs shows a red "failed" verifier status, even though the research report was successfully produced.
- **Silent for playbook runs with any optional step:** Any playbook that uses `required=False` steps will trigger this if those steps encounter errors.
- **Blocks AF-0113:** Per-step verification (AF-0113) wires SchemaValidator into the step loop and relies on clear pass/fail semantics. If the end-of-run verifier already misreports optional failures, adding per-step verification will compound the confusion.

---

## Suspected cause

`V0Verifier.verify_components()` in `runtime.py:260-280`:

```python
def verify_components(self, steps, final_status):
    for step in steps:
        if step.error:  # ← no knowledge of required vs optional
            return "failed", f"Step {step.step_number} failed: {step.error}"
    if final_status != FinalStatus.SUCCESS:
        return "failed", f"Run ended with status: {final_status.value}"
    return "passed", "All steps completed successfully"
```

The verifier receives a flat `list[Step]` with no metadata about whether each step was required. The `Step` schema does not carry a `required` flag. The verifier cannot distinguish "optional step failed (expected)" from "required step failed (real problem)."

---

## Proposed fix

Three options, in order of preference:

### Option A: Tag optional step errors as warnings in the trace (recommended)

When the orchestrator encounters a failed optional step, record the error with a distinct marker (e.g. `step.error = None`, `step.output_summary = "Skipped (optional): ..."`) so the verifier's existing scan does not trip on it.

**Pros:** No schema change, no Verifier Protocol change, backward-compatible.
**Cons:** Loses the original error message in the `error` field (can move to `output_summary` or a metadata field).

### Option B: Add `required` flag to `Step` schema

Add `required: bool = True` to the `Step` model in `run_trace.py`. V0Verifier then skips steps where `required=False`.

**Pros:** Preserves error information, verifier can make informed decisions.
**Cons:** Schema change (additive, backward-compatible with default=True).

### Option C: V0Verifier trusts `final_status` first

If `final_status == SUCCESS`, skip the step-error scan entirely.

**Pros:** Simplest one-line fix.
**Cons:** Defeats the purpose of verification — if the verifier just rubber-stamps the orchestrator's decision, it adds no value.

**Recommendation:** Option B — it's additive, backward-compatible, and gives the verifier the information it needs without losing any data.

---

## Acceptance criteria (for verification)

- [ ] `ag run --playbook research_v0 "..."` with no local docs: `Status: success` AND `Verifier: passed`
- [ ] Optional step failure recorded in trace but does not cause verifier failure
- [ ] Required step failure still causes verifier failure (regression check)
- [ ] `pytest -W error` passes
- [ ] `ruff check src tests` passes
- [ ] New/updated test: optional step error does not fail verification
- [ ] New/updated test: required step error still fails verification
- [ ] Evidence captured: RunTrace ID from successful research run

---

## Notes

- The `research_v0` playbook correctly marks `load_documents` as `required=False` (line ~52 of `research_v0.py`). The playbook is not the problem.
- The orchestrator correctly handles `required=False` (runtime.py:561-566). The orchestrator is not the problem.
- The bug is isolated to V0Verifier and/or the Step schema.

---

## Status log
- 2026-03-21 — Opened by Kai (reproduced with run `a4311fc6-c216-43d7-91c6-c6c4321eb982`)
- 2026-03-22 — FIXED in Sprint 13 via AF-0115: V1Verifier implements Option B (`required` field on Step model + step-aware verification). V1Verifier now tracks required vs optional steps; only required failures trigger verifier `failed`. 9 contract tests added. Evidence: happy_trace.json shows `required_passed`, `optional_skipped` fields.
