# AF-0115 — V1 Verifier: step-aware verification
# Version number: v0.1
# Created: 2026-03-21
# Status: DONE
# Priority: P1
# Area: Core Runtime / Verifier

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`

---

## Summary

Replace V0Verifier's blind error scan with a step-aware V1Verifier that understands required vs optional steps, produces per-step pass/fail breakdowns, and records richer evidence. This fixes BUG-0017 (verifier contradicts orchestrator on optional step failures) and lays the foundation for LLM-powered semantic verification in V2.

---

## Problem

V0Verifier (`runtime.py:219`) has two critical limitations:

1. **No step awareness (BUG-0017).** It scans all steps for any non-null `error` field and fails on the first one — even if the step was `required=False`. This produces contradictory traces: `Status: success` + `Verifier: failed`. Reproduced in run `a4311fc6-c216-43d7-91c6-c6c4321eb982` where `load_documents` (optional) failed but the research pipeline succeeded.

2. **No per-step evidence.** V0Verifier returns a single `(status, message)` tuple. There's no breakdown of which steps passed, which failed, or why. The `Verifier` model in run_trace.py has an `evidence` dict that is always empty.

### What already exists but isn't wired

- `StepType.VERIFICATION` — defined in `run_trace.py:63` but never emitted by any runtime code
- `SchemaValidator` — full repair-loop engine in `schema_verifier.py` with evidence recording, orphaned from runtime
- `SkillInfo.output_schema` — every skill declares output schema, never validated at runtime
- `Step` schema — missing `required` field, so verifier can't distinguish optional from required

---

## Goal

- V1Verifier respects `required` flag per step
- Per-step pass/fail breakdown recorded in verifier evidence
- BUG-0017 fixed: optional step failure no longer fails the run
- `StepType.VERIFICATION` steps emitted in traces
- Clear V2 extension point for LLM-powered semantic checks

---

## Non-goals

- LLM-powered semantic verification (V2 scope — see Future section)
- Output schema validation per step (AF-0116 V1 Executor)
- Per-step verification loop in orchestrator (AF-0117 V1 Orchestrator)
- Changing the Verifier Protocol signature

---

## Design

### Schema change: `required` flag on Step

Add to `Step` model in `run_trace.py`:
```python
required: bool = Field(default=True, description="Whether this step was required for success")
```

Additive, backward-compatible (default=True matches V0 behavior for existing traces).

The orchestrator sets this field when recording steps, based on `PlaybookStep.required`.

### V1Verifier behavior

```python
class V1Verifier:
    def verify(self, trace: RunTrace) -> tuple[str, str | None]:
        return self.verify_components(trace.steps, trace.final)

    def verify_components(self, steps, final_status):
        failed_required = []
        failed_optional = []

        for step in steps:
            if step.error:
                if step.required:
                    failed_required.append(step)
                else:
                    failed_optional.append(step)

        if failed_required:
            msg = "; ".join(f"Step {s.step_number}: {s.error}" for s in failed_required)
            return "failed", f"Required step(s) failed: {msg}"

        if final_status != FinalStatus.SUCCESS:
            return "failed", f"Run ended with status: {final_status.value}"

        if failed_optional:
            msg = "; ".join(f"Step {s.step_number} (optional): {s.error}" for s in failed_optional)
            return "passed", f"Passed with optional step warnings: {msg}"

        return "passed", "All steps completed successfully"
```

### Richer evidence in trace

The `Verifier` model's `evidence` dict (currently always empty) gets populated:

```python
evidence = {
    "total_steps": len(steps),
    "required_passed": count_required_passed,
    "required_failed": count_required_failed,
    "optional_passed": count_optional_passed,
    "optional_skipped": count_optional_failed,
    "per_step": [
        {"step": 0, "required": False, "status": "failed", "reason": "No files found..."},
        {"step": 1, "required": False, "status": "passed"},
        {"step": 2, "required": False, "status": "passed"},
        {"step": 3, "required": True, "status": "passed"},
        {"step": 4, "required": True, "status": "passed"},
    ]
}
```

### Files touched

| File | Change |
|------|--------|
| `src/ag/core/verifier.py` | **New** V1Verifier (assumes AF-0114 extraction done; otherwise modify `runtime.py`) |
| `src/ag/core/run_trace.py` | Add `required: bool = True` to `Step` model |
| `src/ag/core/runtime.py` | Orchestrator sets `step.required` when recording steps; wire V1Verifier |
| `tests/test_runtime.py` | Tests for optional step pass-through, required step failure, evidence population |

---

## V2 roadmap: LLM-powered semantic verification

V1 is mechanical (required/optional awareness, schema checks). V2 adds **intelligence**:

| V2 Capability | What LLM evaluates | Example |
|---|---|---|
| **Relevance check** | Does the output answer the original task? | "User asked about Tokyo demographics — report covers Tokyo tourism instead" |
| **Completeness check** | Are expected sections/elements present? | "Report has data but no conclusion or citations" |
| **Consistency check** | Does the output contradict its own sources? | "Source A says 14M population, synthesis says 9M" |
| **Acceptance criteria** | Does output meet planner-defined criteria? | V3Planner (AF-0104) emits expected-output hints; V2Verifier checks against them |

**V2 design principle:** LLM verification is always **additive** — schema validation runs first (fast, deterministic), then LLM evaluation adds semantic checks. If the LLM verifier is unavailable or times out, the run still has mechanical verification.

**V2 integration point:** `V2Verifier.verify()` calls `V1Verifier.verify()` first, then runs LLM evaluation on steps that passed mechanical checks. The LLM call is bounded by token budget and timeout.

---

## Acceptance criteria

- [ ] `Step` model has `required: bool = True` field
- [ ] Orchestrator populates `step.required` from `PlaybookStep.required`
- [ ] V1Verifier skips optional step errors → verifier reports `passed`
- [ ] V1Verifier fails on required step errors → verifier reports `failed`
- [ ] Verifier `evidence` dict populated with per-step breakdown
- [ ] BUG-0017 fixed: `ag run --playbook research_v0 "..."` with no local docs → `Verifier: passed`
- [ ] `pytest -W error` passes
- [ ] `ruff check src tests` passes
- [ ] Tests cover: optional-fail-passes, required-fail-fails, mixed scenarios, evidence content

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Existing traces lack `required` field | Deserialization breaks | Default=True makes it backward-compatible |
| V2 LLM verification adds latency/cost | Slow runs | V2 is additive + bounded; V1 always runs first |

---

# Completion section (fill when done)

## 1) Metadata
- **Backlog item (primary):** AF-0115
- **PR:** #<number>
- **Author:** <name>
- **Date:** YYYY-MM-DD
- **Branch:** feat/v1-verifier
- **Risk level:** P1
- **Runtime mode used for verification:** llm + manual

## 2–10) (fill when done per template)
