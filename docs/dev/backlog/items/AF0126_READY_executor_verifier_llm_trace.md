# AF-0126 — Executor / Verifier LLM trace
# Version number: v0.1
# Created: 2026-03-22
# Status: READY
# Priority: P1
# Area: Core Runtime / Trace / CLI

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI workflow (two-phase — see below)
> - 1 PR = 1 sprint
> - INDEX update rule (status ↔ filename integrity)
>
> **CI workflow (CRITICAL):**
> - **During AF development:** run targeted tests only
>   `pytest tests/test_<relevant>.py -W error`
> - **Before commit (full gate):** run the complete CI gate
>   1. `ruff check src tests`
>   2. `ruff format --check src tests`
>   3. `pytest -W error`
>   4. `pytest --cov=src/ag --cov-report=term-missing`
>
> Do NOT run the full suite on every save. Targeted tests keep feedback fast.
> The full gate runs once, right before `git commit`.

> **File naming (required):** `AF####_<STATUS>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF-0126
- **Type:** Core Runtime / Observability
- **Status:** READY
- **Priority:** P1
- **Area:** Core Runtime / Trace / CLI
- **Owner:** Jacob
- **Target sprint:** Sprint 16

---

## Problem

The trace file already captures structured LLM call data for the **planner** via the
`planning.llm_call` field (`model`, `input_tokens`, `output_tokens`, `total_tokens`).
No equivalent exists for V2Executor and V2Verifier, even though both components make
real LLM calls on every run:

**V2Executor** — LLM repair after retry exhaustion:
Each failed step that triggers repair records `repair_model`, `repair_tokens`, and
`repair_ms` deep inside `steps[N].output_data.repair_result`. There is no run-level
aggregation. In the sample trace (`b0f76c50`), step 0 consumed **1116 tokens** on a
repair call that still failed — but those tokens are invisible at the top level.

**V2Verifier** — LLM semantic quality check:
When V2Verifier's semantic gate runs, it records results inside
`verifier.evidence.semantic` (model, tokens, scores, evaluation_ms). There is no
top-level trace field for this call. In the sample trace, V2Verifier is listed in the
pipeline manifest but the verifier section has no `llm_call` information.

**Top-level `llm` block — undercounting:**
The trace has a top-level `llm` block:
```json
"llm": {
  "provider": "openai",
  "model": "gpt-4o-mini",
  "call_count": 1,
  "total_tokens": 5187,
  "input_tokens": 4645,
  "output_tokens": 542
}
```
`call_count: 1` is wrong — at minimum the planner makes two calls (feasibility +
plan). Executor repair adds more. This block does not accurately reflect LLM usage
for the run.

The net effect: there is no single place in the trace (or CLI output) where a user
can see total LLM token spend across all pipeline components, or identify which
component caused the highest cost.

Related: BUG-0023 (V2 pipeline evidence hidden), AF-0122 (CLI planning/pipeline display).

---

## Goal

- The trace has a structured, top-level `execution` section capturing V2Executor's
  aggregate LLM repair activity (total calls, total tokens, per-step repair summary)
- The trace has a structured `llm_call` field inside the existing `verifier` section
  capturing V2Verifier's semantic check LLM call (model, tokens, duration)
- The top-level `llm` block accurately reflects the total LLM usage across all
  pipeline components (planner + executor repair + verifier semantic)
- The CLI (`ag run` summary and `ag runs show`) surfaces these fields alongside
  the existing Planning section — consistent with AF-0122 display patterns
- All changes are additive (no breaking changes to existing trace fields)

---

## Non-goals

- Tracking LLM calls made _inside_ skills (e.g. `synthesize_research`) — those are
  skill-internal and tracked separately via their own output schema
- Changing how BUG-0023's `logging.warning()` bleed is suppressed (separate fix)
- Modifying the `PlanningMetadata` or `planning.llm_call` structure
- Adding per-token cost estimation (out of scope for trace layer)

---

## Design

### 1. New `ExecutionMetadata` model in `run_trace.py`

```python
class RepairSummary(BaseModel):
    """Per-step repair attempt summary for executor trace."""
    step_number: int
    skill_name: str
    repair_attempted: bool
    repair_succeeded: bool
    repair_tokens: int
    repair_ms: int
    repair_model: str

class ExecutionMetadata(BaseModel):
    """Aggregate trace of LLM calls made by V2Executor during the run."""
    executor: str = "V2Executor"
    total_repair_attempts: int
    total_repair_successes: int
    total_repair_tokens: int
    repairs: list[RepairSummary] = []
```

`RunTrace` gets a new optional field:
```python
execution: ExecutionMetadata | None = None
```

### 2. Extend `verifier` section with `llm_call`

The `VerifierEvidence` model (or the `verifier` dict written by V0Recorder) gets a
top-level `llm_call` field:
```python
class VerifierLLMCall(BaseModel):
    model: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    evaluation_ms: int
```
Populated only when V2Verifier makes a semantic check. When V1Verifier or V0Verifier
is used, `llm_call` is `null`.

### 3. Fix the top-level `llm` aggregation

The top-level `llm` block is assembled by V0Recorder. After this AF, it should sum:
- `planning.llm_call.total_tokens`
- `execution.total_repair_tokens` (if `execution` is set)
- `verifier.llm_call.total_tokens` (if `verifier.llm_call` is set)
- `call_count` must reflect the actual number of distinct LLM `.chat()` calls

### 4. Data flow

```
V2Executor.execute_step()
  → per-step RepairResult already in output_data.repair_result
  → NEW: V2Executor exposes get_execution_metadata() → ExecutionMetadata
         (aggregates across all steps after run completes)

V2Verifier.verify()
  → SemanticVerification already in verifier.evidence.semantic
  → NEW: V2Verifier exposes get_llm_call() → VerifierLLMCall | None

V1Orchestrator.run()
  → calls executor.get_execution_metadata() after all steps finish
  → passes ExecutionMetadata to V0Recorder

V0Recorder.save()
  → writes execution section to trace
  → writes verifier.llm_call to trace
  → recalculates top-level llm aggregate
```

### 5. CLI display (analogous to AF-0122 Planning section)

`ag run` summary and `ag runs show` gain an **Execution** section (only if
`V2Executor` was used and at least one repair was triggered):

```
Execution     V2Executor
  Repairs     1 attempted, 0 succeeded
  Tokens      1,116 repair tokens (gpt-4o-mini-2024-07-18)
```

And the verifier section gains an LLM line (only if V2Verifier semantic check ran):

```
Verifier      V2Verifier  →  passed
  Semantic    relevance=0.85  completeness=0.72  consistency=0.91
  LLM         gpt-4o-mini-2024-07-18  ·  832 tokens  ·  2,100 ms
```

The top-level `llm` block in the summary changes from:
```
LLM           1 call · 5,187 tokens
```
to:
```
LLM           4 calls · 8,099 tokens  (planner: 1,795 | repairs: 1,116 | verifier: 832 | skills: 4,356)
```

---

## Files to touch

| File | Change |
|---|---|
| `src/ag/core/run_trace.py` | Add `RepairSummary`, `ExecutionMetadata`, `VerifierLLMCall` models; add `execution` field to `RunTrace`; add `llm_call` to verifier evidence |
| `src/ag/core/executor.py` | V2Executor: track repair calls internally; expose `get_execution_metadata()` |
| `src/ag/core/verifier.py` | V2Verifier: expose `get_llm_call()` returning `VerifierLLMCall | None` |
| `src/ag/core/orchestrator.py` | V1Orchestrator: collect execution/verifier metadata after run; pass to recorder |
| `src/ag/core/recorder.py` | V0Recorder: write new fields; recalculate top-level `llm` aggregate |
| `src/ag/cli/main.py` | Add Execution section display; extend Verifier section with LLM line; fix top-level LLM count |
| `ARCHITECTURE.md` | Update trace contract section to document new fields |

---

## Acceptance criteria

- [ ] `trace.json` has `execution` section when V2Executor is used and repair was attempted
- [ ] `trace.json` has `verifier.llm_call` when V2Verifier semantic check runs
- [ ] `trace.json` top-level `llm.call_count` matches actual LLM call count
- [ ] `trace.json` top-level `llm.total_tokens` correctly sums all component tokens
- [ ] `ag run` CLI output shows Execution section (repairs + tokens) when applicable
- [ ] `ag runs show` CLI output includes the same Execution and Verifier LLM detail
- [ ] No existing trace fields are modified (additive only)
- [ ] `pytest tests/test_runtime.py tests/test_executor.py tests/test_trace_enrichment.py -W error` passes
- [ ] Full CI gate passes

---

## Test strategy

- `tests/test_executor.py`: add `test_v2_executor_execution_metadata_populated` — run
  V2Executor with a skill that always fails; verify `get_execution_metadata()` returns
  `ExecutionMetadata` with correct totals
- `tests/test_runtime.py`: add `test_run_trace_has_execution_section` — run pipeline
  end-to-end with FakeLLMProvider; assert `run_trace.execution` is not None and
  `run_trace.execution.total_repair_tokens` matches injected repair token count
- `tests/test_trace_enrichment.py` (new or existing): add
  `test_verifier_llm_call_in_trace` — assert `verifier.llm_call` populated when
  V2Verifier is used
- `tests/test_trace_enrichment.py`: add `test_top_level_llm_aggregate_correct` —
  verify `llm.call_count` and `llm.total_tokens` sum correctly across all components

---

## Notes

- The `RepairSummary` list is per-step, which allows future drill-down in `ag runs show`
- When V2Executor makes zero repair attempts (all steps pass on first try), `execution`
  may be omitted or populated with all-zero values — implementation choice
- This AF closes the observability gap identified in BUG-0023 at the **trace schema
  layer**; BUG-0023 tracks the **CLI display layer** separately
- AF-0125 (FakeLLMProvider) must be implemented first so tests for this AF run
  deterministically without real API calls
