# Architectural Findings — ag_foundation
# Version: 0.2
# Prepared: 2026-04-02
# Prepared by: Jeff
# For: LinkedIn campaign (Simon / Kai)

---

## Methodology and source confidence

**Primary sources: codebase + AF/BUG files (high confidence)**
Every finding below is traceable to a specific file, line, or AF/BUG record.
Component version history is derived from module docstrings, AF completion
notes, and git commit messages — not reconstructed from memory.

**Secondary source: bug metadata (medium confidence)**
Bug severity, sprint, and detection method fields were written by Jacob at
fix time. The "57% live testing / 22% CI / 13% review" detection split
in Section 5 is Jacob's classification of 24 bugs across S00–S15.

**What the data cannot tell us**
- Pre-extraction line count of `runtime.py` (AF-0114 states "600+ lines" in
  its problem statement; current post-extraction runtime.py is 296 lines).
- The number of breaking test runs per sprint — Jacob ran tests in targeted
  mode during development (per `FOUNDATION_MANUAL.md`), so not every failure
  produced a CI log.
- Whether any architectural decision prevented a class of bug that was never
  attempted, versus one that was tried and caught.

All sprint date boundaries use merge-commit timestamps from the velocity
analysis; sprint-to-AF mapping uses the `Target sprint` field in each AF file.

---

## 1. Component version history

### The swappable brain claim

ag_foundation's pipeline is defined by five `typing.Protocol` interfaces in
`src/ag/core/interfaces.py` (164 lines). These Protocols have never changed
their method signatures across 15 sprints. 13 distinct component
implementations were shipped against those unchanged interfaces.

The Protocols and their signatures:

| Protocol | Method signature | Defined | Last changed |
|---|---|---|---|
| `Planner` | `plan(task: TaskSpec) → Playbook` | AF-0005, S01 | Never — unchanged |
| `Orchestrator` | `run(task: TaskSpec, playbook: Playbook) → RunTrace` | AF-0005, S01 | Never — unchanged |
| `Executor` | `execute(skill_name, params) → (bool, str, dict)` | AF-0005, S01 | Never — unchanged |
| `Verifier` | `verify(trace: RunTrace) → (str, str\|None)` | AF-0005, S01 | Never — unchanged |
| `Recorder` | `record(trace)` + `register_artifact(...)` | AF-0005, S01 | Never — unchanged |

The `Normalizer` Protocol is also defined in `interfaces.py` but has only one
implementation (`V0Normalizer` in `runtime.py`) across all sprints.

---

### Planner version history

| Version | Sprint introduced | What changed | What stayed stable | Key AF / BUG |
|---|---|---|---|---|
| V0Planner | S00/01 (Feb 24) | Registry lookup. Requires explicit `--playbook` flag. No LLM call. | `plan(task) → Playbook` Protocol | AF-0003, AF-0005 |
| V1Planner | S11 (Mar 12–21) | LLM composes a skill-only sequence from the task description. First LLM call in the planner path. Adds `confidence` float to plan response. | Same Protocol | AF-0102 |
| V2Planner | S13 (Mar 21–22) | LLM composes mixed plans using both individual skills AND existing playbooks as macro steps. `PlannedStep.type` field: `"skill"\|"playbook"`. Co-delivered with V1Orchestrator part 1 (step expansion). | Same Protocol | AF-0103, AF-0117 |
| V3Planner | S15 (Mar 22) | Two-phase LLM call: Phase 1 is a feasibility assessment producing `FeasibilityAssessment` + `list[CapabilityGap]`. Phase 2 conditionally generates a plan scoped to available capabilities. `NOT_FEASIBLE` skips plan generation entirely. | Same Protocol | AF-0104 (study), AF-0121, ADR-0009 |

**Observation:** V3Planner adds a pre-planning feasibility gate that V0–V2 lack.
This directly addresses the BUG-0020 failure class (zero-step plans that report
success) at the *planning* level rather than the *verifier* level. Both fixes now
exist in the codebase simultaneously.

---

### Orchestrator version history

| Version | Sprint introduced | What changed | What stayed stable | Key AF / BUG |
|---|---|---|---|---|
| V0Orchestrator | S00/01 (Feb 24) | Linear step execution. Single verification run at end of all steps. No per-step feedback. | `run(task, playbook) → RunTrace` Protocol | AF-0003, AF-0007 |
| V1Orchestrator pt.1 | S13 (Mar 21–22) | Adds `PLAYBOOK` step type to `PlaybookStepType` enum. Expands `type=playbook` steps into their constituent skill steps inline. Required for V2Planner mixed plans. | Same Protocol | AF-0117, AF-0103 |
| V1Orchestrator pt.2 | S14 (Mar 22) | Per-step verification loop: V1Executor + V1Verifier called after each skill step. Required step failure → stops execution. Optional step failure → continues, records warning. Produces interleaved `VERIFICATION` steps in trace. | Same Protocol | AF-0117, AF-0115, AF-0116 |

**Observation:** V1Orchestrator was delivered in two parts across two sprints
(S13 and S14). This is the only component with a split delivery. The split was
deliberate: S13 required expanding playbook step support for V2Planner; S14
added the per-step verification loop that required V1Executor and V1Verifier
to exist first.

BUG-0019 (V1Orchestrator drops required flag on expansion) was a wiring defect
in V1Orchestrator pt.1 detected in Sprint 14: when expanding a `PLAYBOOK` step
into skill steps, the orchestrator defaulted `required=True` on all expanded
steps instead of propagating the original `required` value. Reproduced with
RunTrace `19eb2092-c433-4727-ab6f-80accdaa565c`. Fixed in the same sprint.

---

### Executor version history

| Version | Sprint introduced | What changed | What stayed stable | Key AF / BUG |
|---|---|---|---|---|
| V0Executor | S00/01 (Feb 24) | Resolves skill from registry; executes; returns `(success, output_summary, result_data)` tuple. No output validation. | `execute(skill_name, params) → tuple` Protocol | AF-0003, AF-0014 |
| (Extraction) | S13 | Moved from `runtime.py` to `executor.py` (AF-0114). Zero behavior change. | Same Protocol | AF-0114 |
| V1Executor | S14 (Mar 22) | Validates skill output against `SkillInfo.output_schema` after each execution. Bounded retry: `DEFAULT_MAX_VALIDATION_ATTEMPTS = 3`. Records `VERIFICATION` steps in trace. | Same Protocol | AF-0116 |
| V2Executor | S15 (Mar 22) | LLM-powered output repair after retry exhaustion. Sends malformed output + schema + error to LLM for structural correction. Repair attempt stored in `ExecutionMetadata.repairs`. Inherits from V1Executor. | Same Protocol | AF-0124, AF-0126 |

**File:** `src/ag/core/executor.py` — 391 lines (V0 + V1 + V2 + shared helpers).
`DEFAULT_MAX_VALIDATION_ATTEMPTS = 3` is defined at module level (line 28).

---

### Verifier version history

| Version | Sprint introduced | What changed | What stayed stable | Key AF / BUG |
|---|---|---|---|---|
| V0Verifier | S00/01 (Feb 24) | Basic error scan: any non-null `step.error` = `"failed"`. No step-level awareness. | `verify(trace) → (str, str\|None)` Protocol | AF-0003, AF-0029 |
| (Extraction + BUG-0020 fix) | S13 | Moved from `runtime.py` to `verifier.py` (AF-0114). Added empty-step guard: zero executed steps → `"failed"` (BUG-0020 fix). | Same Protocol | AF-0114 |
| V1Verifier | S14 (Mar 22) | Step-aware: respects `Step.required` flag. Required step failure → fails; optional step failure → passes with warning. Per-step breakdown recorded in verifier evidence dict. Adds `verify_step()` method for per-step use by V1Orchestrator. Fixes BUG-0017. | Same Protocol | AF-0115, BUG-0017 |
| V2Verifier | S15 (Mar 22) | LLM semantic quality checks layered on V1: relevance, completeness, and consistency scores (each 0–1) via `SemanticVerification` model. Scores stored in trace; `overall_pass` derived from threshold. | Same Protocol | AF-0123, AF-0126 |

**File:** `src/ag/core/verifier.py` — 489 lines (V0 + V1 + V2).

---

### Recorder version history

| Version | Sprint introduced | What changed | What stayed stable | Key AF / BUG |
|---|---|---|---|---|
| V0Recorder | S00/01 (Feb 24) | Persists `RunTrace` to `SQLiteRunStore`; registers artifacts to `SQLiteArtifactStore`. | `record(trace)` + `register_artifact(...)` Protocol | AF-0006, AF-0014, AF-0015 |
| (Extraction) | S13 | Moved from `runtime.py` to `recorder.py` (AF-0114). Zero behavior change. | Same Protocol | AF-0114 |
| V0Recorder (enhanced) | S14 (Mar 22) | Structured `Verifier.evidence` dict populated with per-step breakdown, retry history, and version tag. Scope expanded from AF-0118 (originally scoped to "V1Recorder" but implemented as in-place enhancement to V0). | Same Protocol | AF-0118 |

**File:** `src/ag/core/recorder.py` — 47 lines. The recorder is the only
pipeline component that did not receive a new-class version upgrade. All
enhancements to evidence persistence landed in the Orchestrator's step-recording
logic rather than in a new Recorder class.

---

### Summary: swappable brain evidence

| Component | Implementations shipped | Protocol signature changes | Sprints between first and latest version |
|---|---|---|---|
| Planner | 4 (V0 → V3) | 0 | S01 → S15 (14 sprints) |
| Orchestrator | 2 (V0 → V1) | 0 | S01 → S14 (13 sprints) |
| Executor | 3 (V0 → V2) | 0 | S01 → S15 (14 sprints) |
| Verifier | 3 (V0 → V2) | 0 | S01 → S15 (14 sprints) |
| Recorder | 1 (V0, enhanced) | 0 | S01 → S14 (13 sprints) |
| **Total** | **13 implementations** | **0** | — |

The 13 implementations shipped against 5 unchanged Protocol signatures across
14 sprints. No implementation required the caller to change how it invokes the
component. `runtime.py` (296 lines) wires the current composition but has never
needed to change the wiring *interface* — only the concrete class instantiated.

---

## 2. The Sprint 13 extraction (AF-0114)

### Before: runtime.py as a monolith

Before AF-0114 (delivered Sprint 13, March 21–22), the file
`src/ag/core/runtime.py` contained all five pipeline component implementations:
`V0Orchestrator`, `V0Executor`, `V0Verifier`, `V0Recorder`, plus the
`Runtime` facade and `V0Normalizer`. The AF-0114 problem statement describes
it as "600+ line `runtime.py`" containing:

- The four component implementations (Orchestrator, Executor, Verifier, Recorder)
- `TrackingLLMProvider` and `_adapt_document_to_source` (both orchestration helpers)
- Assembly/wiring code for `create_runtime()`
- `V0Normalizer`

V0Planner already had its own `planner.py` file before Sprint 13; TaskSpec and
RunTrace already had `task_spec.py` and `run_trace.py`. The inconsistency was
that these data models had independent files while the four executable components
did not.

### The extraction

AF-0114 was a pure structural refactor: **zero behavior change**. The AF's
stated goal was to move each component to its own file so that upgrading any
component to V1 would mean editing a dedicated file, not a shared 600-line one.

**Target dependency graph (from AF-0114 design):**
```
executor.py  → skills/registry, interfaces
verifier.py  → run_trace, interfaces
recorder.py  → storage, run_trace, interfaces
     ↑
orchestrator.py → executor, verifier, recorder, run_trace
     ↑
runtime.py  → all of the above (composition root only)
```

**After extraction — post-Sprint 15 current state:**

| File | Lines | Contents |
|---|---|---|
| `runtime.py` | 296 | Composition root: V0Normalizer, Runtime facade, wiring only |
| `orchestrator.py` | 1,015 | V0Orchestrator + V1Orchestrator + TrackingLLMProvider |
| `planner.py` | 1,252 | V0/V1/V2/V3Planner + PlanningResult + Pydantic schemas |
| `verifier.py` | 489 | V0/V1/V2Verifier |
| `executor.py` | 391 | V0/V1/V2Executor |
| `recorder.py` | 47 | V0Recorder |
| `interfaces.py` | 164 | 5 Protocols + Normalizer Protocol (never changed) |
| `run_trace.py` | 741 | RunTrace schema (20 Pydantic models, all `extra="forbid"`) |

`runtime.py` dropped from 600+ lines to 296 by becoming a pure composition root.

### What the extraction enabled

The extraction was the prerequisite for all V1/V2/V3 upgrades that followed in
Sprints 14 and 15. Without dedicated files, each of the following would have
meant editing a shared 600-line module:

| Upgrade | Sprint | Dependency on AF-0114 |
|---|---|---|
| V1Verifier (step-aware, BUG-0017 fix) | S14 | New class in `verifier.py` |
| V1Executor (schema validation + retry) | S14 | New class in `executor.py` |
| V1Orchestrator pt.2 (per-step loop) | S14 | V1Executor + V1Verifier in their own files first |
| V0Recorder evidence enhancement | S14 | Own file allowed targeted edits |
| V2Verifier (LLM semantic checks) | S15 | New class in `verifier.py` |
| V2Executor (LLM repair) | S15 | Inherits V1Executor in `executor.py` |
| V3Planner (feasibility) | S15 | Already in own `planner.py` since before S13 |

The extraction was delivered as a standalone sprint (Sprint 13 included AF-0114
as its structural prerequisite before the V2Planner and V1Orchestrator work).
The non-goals in AF-0114 explicitly state: "V1 implementations (separate AFs:
AF-0115 through AF-0118)." This separation was deliberate: extraction had to be
confirmed clean (all tests pass with no behavior change) before any V1 work began.

---

## 3. Framework boundary decisions

### What ag_foundation builds

The following capabilities are implemented from scratch with no external framework:

| Capability | Module | Notes |
|---|---|---|
| Pipeline orchestration | `orchestrator.py` (1,015 lines) | Sequential step execution, per-step verification, playbook expansion |
| Execution tracing | `run_trace.py` (741 lines) | 20 Pydantic models, all `extra="forbid"`, additive-only schema evolution policy (ADR-0002) |
| Output schema verification | `schema_verifier.py` (372 lines) | Bounded retry loop with `DEFAULT_MAX_VALIDATION_ATTEMPTS=3` and ceiling at 10 (AF-0055) |
| Skill plugin architecture | `src/ag/skills/` | Entry-point-based registry, SkillBase ABC, input/output Pydantic schemas per skill |
| Playbook system | `src/ag/playbooks/` + `playbook.py` | YAML-defined step graphs, `PlaybookStep.required` flag, `ReasoningMode` policy enum |
| LLM planning | `planner.py` (1,252 lines) | 4 planner versions; all LLM prompts are custom; no framework-managed chains |
| Output repair loop | `executor.py` (V2Executor) | Custom LLM repair prompt; not LangChain's output parsers |
| Semantic verification | `verifier.py` (V2Verifier) | Custom LLM relevance/completeness/consistency scoring |
| WorkflowStorage | `src/ag/storage/` | SQLite (`SQLiteRunStore`, `SQLiteArtifactStore`); no ORM dependency |
| CLI | `src/ag/cli/` | Typer-based; all output derives from RunTrace (Truthful UX invariant) |

### What ag_foundation borrows

| Capability | Library | Nature of use |
|---|---|---|
| LLM API calls | `openai` (Python client) | Runtime LLM provider. `gpt-4o-mini` is the configured default model. The `LLMProvider` Protocol means any provider can be swapped without caller changes. Anthropic and local providers are **stubs** — the Protocol exists, the implementation doesn't. |
| Schema validation | `pydantic` v2 | All data models: RunTrace (20 models), TaskSpec, Playbook, skill input/output schemas, planner response schemas. `extra="forbid"` is applied uniformly to prevent silent field loss. |
| Web search | `duckduckgo-search` (`ddgs`) | The `web_search` skill (AF-0080, S08) uses DuckDuckGo. BUG-0021 surfaced SSL noise from the library's `primp` dependency — caught in Sprint 15, fixed with `ssl_verify=False` workaround under a guard. |
| LangChain tools | `langchain-community` | **Sprint 16 only (AF-0127, READY).** Not yet in the codebase. Treated as an external tool catalog, not as a runtime. |

### The framework boundary and why it sits where it does

ADR-0001 (Feb 23, 2026) states:

> "We will implement a minimal in-house orchestrator first (sequence execution),
> keeping the `Orchestrator` interface stable. If/when step graphs require
> branching/cycles/persistence/streaming, we may adopt a framework backend
> (e.g., LangGraph) behind the interface via a new ADR."

This was not anti-framework ideology. It was a deliberate risk sequencing
decision: at Sprint 01, the team didn't know what parts of the system would
be stable versus experimental. Building the orchestrator in-house meant the
`run(task, playbook) → RunTrace` interface could be locked early while the
implementation evolved freely.

By Sprint 16, 4 Planner versions and 2 Orchestrator versions have shipped
without a caller change. The Protocol boundary is validated empirically,
not just theoretically. That creates a concrete anchor point: if LangGraph is
adopted in the future, it would plug in behind `Orchestrator.run()` with no
change to Runtime, CLI, or the planning stack.

### How Sprint 16's LangChain adapter works

AF-0127 (READY, not yet implemented) proposes a `LangChainSkillAdapter` class
that wraps a LangChain `BaseTool` into a `SkillBase`-compatible skill:

```
LangChain BaseTool                      ag_foundation SkillBase
────────────────────────────────────────────────────────────────
BaseTool.name          ──►  SkillInfo.name
BaseTool.description   ──►  SkillInfo.description  
BaseTool.args_schema   ──►  SkillInfo.input_schema (Pydantic model)
BaseTool.run(input)    ──►  SkillBase.execute(input, ctx) → SkillOutput
```

The adapter registers in the skill registry via the existing plugin entry
point mechanism. From the orchestrator's perspective, a LangChain-wrapped tool
is indistinguishable from a native ag_foundation skill. The trace captures it
identically: `skill_name`, execution timing, output, `VERIFICATION` step result.

**What this means for the boundary:** LangChain's tool execution logic
(`BaseTool.run`) is called, but LangChain's runtime is not adopted. The
LangChain tool is an input to ag_foundation's traced, verified pipeline — it
doesn't replace that pipeline. V1Executor still validates the tool's output
against a declared schema. V1Verifier still determines whether the run passed.
The `RunTrace` still records everything.

---

## 4. Truthful UX as architectural invariant

### Definition

ADR-0001 (Feb 23, 2026): "RunTrace is the canonical record; user-visible labels
must be derived from trace facts."

This was not a UX preference. It was an architectural constraint: the CLI is an
adapter over RunTrace data, not a layer that computes its own results. Any label
that isn't derivable from a trace field is a bug, regardless of whether it's
technically accurate.

The structural enforcement: `AF-0031` (Sprint 03) added `extract_labels(trace)`
in `src/ag/cli/main.py` and a dedicated `tests/test_cli_truthful.py` (470 lines,
19 test functions) that verifies every displayed label against a real RunTrace.

### Instances where the invariant caught a real problem

**BUG-0020 — Empty plan reports success (P0, Mar 22)**

V2Planner correctly identified that no skills could handle "Read my email" and
returned a plan with zero steps and a warning. The pipeline executed the zero-step
plan, the verifier found no errors (there were none — nothing ran), and the final
status was `success`. The CLI displayed this as a successful execution.

The Truthful UX invariant: if the trace says `success`, the CLI says `success`.
The problem was not in the CLI — it was that the trace was lying. The fix landed
in `V0Verifier.verify_components()`:

```python
if not steps:
    return "failed", "No steps executed"
```

Three lines. Added during the Sprint 13 extraction (AF-0114). The empty-step
guard is now in `verifier.py` at line 34, before any step iteration. This fix
is **permanently upstream** of all three verifier versions — V0, V1, and V2 all
call `verify_components()` which contains this guard.

**AF-0122 — CLI planning display forced trace-derivation design decision (Sprint 14)**

After Sprint 14, `RunTrace` contained a `planning` block with the planner name,
duration, tokens, and confidence. This data existed only in `trace.planning` —
not in the CLI's scope. The CLI needed to display it.

The problem: when V3Planner ran in the CLI layer (before Runtime.execute()), the
Runtime's internal planner was V0Planner (a passthrough). Without the Truthful UX
invariant, the shortcut would have been: display `self._planner.__class__.__name__`
and show "V0Planner". That would be technically wrong.

The fix required passing the real `PlanningResult` into `Runtime.execute()`:

```python
# AF-0122 fix: when the real planner ran externally, build PlanningMetadata
# from the provided PlanningResult so trace.planning truthfully records the
# planner that actually ran.
if plan_result is not None:
    planning_metadata = PlanningMetadata(
        planner=plan_result.planner_name,  ← "V3Planner", not "V0Planner"
        ...
    )
```

This is the most architecturally significant instance of the invariant: it
required changing the Runtime API signature (adding `plan_result` parameter) to
preserve trace honesty. The pipeline manifest now derives the planner name from
`planning_metadata.planner` not from `self._planner.__class__.__name__` when
external planning occurred.

**BUG-0009 — Direct skill execution bypasses verifier (P0, Sprint 05)**

When using `ag run --skill strategic_brief`, the direct skill path set
`verifier.status = "skipped"` while `final = success`. Two contradictory signals
in the same trace output. The Truthful UX invariant made this a bug, not a
feature: a successful run must have a verifier result, not a skipped one.
Fixed by routing direct skill calls through the verification path. Related
AF-0056 was later DROPPED (the final implementation chose a different wiring).

**AF-0031 — Structural enforcement of truthful labels (Sprint 03)**

Before AF-0031, there were no tests that proved CLI labels came from trace fields.
The invariant existed as a policy statement (ADR-0001) but had no code guarantee.
AF-0031 added `extract_labels(trace)` and 19 tests. The tests run as part of
`pytest -W error` on every sprint gate. This is the structural lock that forces
any new label to be trace-derived or the PR fails CI.

**BUG-0016 — Plan steps not executed (P1, Sprint 11)**

When running a pre-generated plan via `ag run --plan plan_5a5575893295`, the
runtime executed the default playbook's echo skill instead of the plan's steps.
The CLI reported "Plan executed — Status: success." The trace showed only the
echo skill was called. The plan's four steps (web_search, fetch_web_content,
summarize_docs, emit_result) were never executed. The truthful UX invariant made
this immediately visible: the reported success was demonstrably false.

Reproduced via RunTrace `eb43f355-2532-4f0a-abe0-ffbb3a54aa3a`. Fixed in Sprint 11
(AF-0099, plan approval workflow).

### The cost: where the invariant created friction

**AF-0122 scope expansion.** The planning display AF required modifying the
`Runtime.execute()` signature to accept `plan_result: PlanningResult | None`.
Without the Truthful UX invariant, showing "V0Planner" in the CLI would have
been acceptable. The invariant added ~50 lines to runtime.py and an additional
test to `test_cli_truthful.py` to verify the planner name is correct.

**Every new RunTrace field creates a CLI obligation.** When `PipelineManifest`
was added (AF-0120), `ag runs show` had to be updated to display it. When
`FeasibilityAssessment` was added (AF-0121), the CLI had to handle the new block.
The obligation propagates: add a trace field, update the display, add a test.
This is the correct behavior, but it added scope to multiple AFs that otherwise
would have been "just the model."

**"unknown" as the honest output.** When a trace field is absent (older traces,
or mid-sprint before a field was added), the CLI renders `unknown`. This was
occasionally confusing to Kai during live testing sessions. The alternative —
infer or default — was rejected by the invariant. The `test_cli_truthful.py`
tests explicitly verify that missing fields produce `"unknown"` rather than
a hardcoded fallback.

**Summary: cost vs. benefit**

| Cost incurred | Bugs caught or prevented |
|---|---|
| Runtime.execute() signature change | BUG-0020 (P0): empty plan success |
| 470-line test file, 19 test functions | BUG-0009 (P0): verifier bypass on direct skill |
| Every new trace field triggers CLI update | BUG-0016 (P1): plan steps not executed |
| "unknown" in CLI for missing fields | AF-0122 design decision: honest planner attribution |

---

## 5. Cross-reference: architecture choices vs. failure modes

Jacob's failure mode inventory: 24 bugs across S00–S15.
Detection split: 57% live testing, 22% CI, 13% review, 8% other.
Most dangerous class: partial pipeline wiring (5 bugs, invisible to unit tests).

---

### A. Protocol file boundaries → partial pipeline wiring defects

**Decision:** interfaces.py holds only Protocols. Each component lives in its
own file. Wiring lives in runtime.py only.

**Before AF-0114 (Sprint 13):** all components in one file. A wiring defect in
one component (e.g., wrong attribute reference on `self`) could be masked by a
nearby attribute in the same class. Import errors were less informative.

**After AF-0114:** `from ag.core.verifier import V1Verifier` is explicit. If
V1Verifier doesn't exist, the import fails at startup with a clear module error.
If V1Orchestrator passes the wrong argument type to `V1Verifier.verify()`, the
Pydantic validation on `RunTrace` fires at that specific line rather than
somewhere downstream.

**Classification: Prevention for import-level defects; Detection for semantic wiring.**

BUG-0019 (V1Orchestrator drops required flag) was a Sprint 14 semantic wiring
defect that the file boundary did not prevent: the code compiled, the tests ran,
and the bug only manifested on a live research run where `load_documents` was
optional but got treated as required. Detected via live testing (RunTrace
`19eb2092-c433-4727-ab6f-80accdaa565c`). Fixed in the same sprint.

The file boundary reduced partial wiring bugs from 5 (S00–S12, before
extraction) to 2 (S13–S15, after extraction). The two post-extraction wiring
defects (BUG-0019, BUG-0023) were semantic rather than structural — the kind
the file boundary cannot catch.

---

### B. `extra = "forbid"` on trace models → silent field loss

**Decision:** All 20 Pydantic models in `run_trace.py` use `model_config = {"extra": "forbid"}`.
ADR-0002 adds an additive-only policy: no field removals or renames within v0.

**What this guards:** If component A writes `SemanticVerification.relevance_score`
and a serialization round-trip drops the field, the deserialization fails
explicitly rather than silently. If V2Executor produces a `RepairResult` with
a field that isn't in the schema, `extra="forbid"` raises a `ValidationError`
immediately.

**BUG-0023 (V2 pipeline evidence hidden):**
V2Executor and V2Verifier produced structured evidence (repair attempts, semantic
scores), but this evidence was invisible in the CLI. The data was in the trace;
`extra="forbid"` ensured it was serialized correctly. The problem was that the
CLI display code (`ag runs show`) wasn't reading the evidence blocks.

Classification: The `extra="forbid"` **prevented** silent field loss (the data
was correctly stored). The bug (BUG-0023) was a display omission — the CLI
wasn't surfacing the data — not a data corruption bug. Detection was via live
testing (Kai noticed the mismatch between verbose warnings and "Status: success").

**BUG-0010 (artifacts not captured, Sprint 05):**
`RunTrace.artifacts` was empty after skill execution. This was not a schema
corruption — `extra="forbid"` wouldn't fire on missing optional fields. The bug
was that the orchestrator wasn't calling `recorder.register_artifact()`. Fixed
by AF-0057. Classification: **Not prevented by `extra="forbid"`** — the guard
catches undeclared fields, not missing calls to populate declared fields.

Overall: `extra="forbid"` has a clean record on its target failure class
(silent schema drift). The failure modes it doesn't cover — omitted writes,
display omissions — remain the dominant category.

---

### C. Loop bounding constants → runaway LLM repair cycles

**Decision:** `schema_verifier.py` defines `DEFAULT_MAX_VALIDATION_ATTEMPTS = 3`
and `MAX_VALIDATION_ATTEMPTS_CEILING = 10` (AF-0055, Sprint 09).
`SchemaValidator.__init__` enforces the ceiling at construction time.

Since Sprint 09, any validation loop in the codebase has used these constants
or an equivalent. When V1Executor (Sprint 14) and V2Executor with LLM repair
(Sprint 15) were built, the bounding pattern was already established and was
applied directly:

```python
# executor.py line 28
DEFAULT_MAX_VALIDATION_ATTEMPTS = 3

class V1Executor(V0Executor):
    def __init__(self, registry=None, max_attempts=DEFAULT_MAX_VALIDATION_ATTEMPTS):
        self._max_attempts = max_attempts
```

**Classification: Prevention.** There are no LLM loop runaway bugs in the
bug inventory. Sprint 09 established the bounding pattern four sprints before
V1Executor introduced a validation loop, and six sprints before V2Executor
introduced LLM-powered repair. The pattern was available before it was needed.

The ceiling (`MAX_VALIDATION_ATTEMPTS_CEILING = 10`) is enforced at
`SchemaValidator` construction, not at call time — meaning a misconfigured
instantiation fails immediately, not after 11 expensive LLM calls.

---

### D. Pipeline manifest → debugging version-specific regressions

**Decision:** AF-0120 (Sprint 14) adds a `PipelineManifest` to every
`RunTrace` recording which component class names ran:
`{planner, orchestrator, executor, verifier, recorder}`.

**BUG-0019 debugging:** When the required-flag regression appeared in Sprint 14,
the pipeline manifest showed `V1Orchestrator` as the orchestrator. That
immediately scoped the bug to the orchestrator and specifically to the V1
expansion logic, rather than requiring a grep through the codebase to determine
which orchestrator was active.

**BUG-0023 debugging:** The manifest confirmed `V2Executor` and `V2Verifier`
were running (not fallback V0/V1 versions). This ruled out "we're not running
the V2 components" as a hypothesis and confirmed the bug was in evidence
display, not component selection.

**Classification: Detection.** The manifest doesn't prevent failures; it
shortens the diagnostic path. Sprint 14 delivered 6 AFs in one session
(Mar 22), all in the same pipeline hardening batch. The manifest was essential
for attributing bugs to specific component versions within that rapid sprint.

---

### E. Documentation drift tests → stale docs as CI failures

**Decision:** `tests/test_documentation_drift.py` (AF-0013, AF-0063, 228 lines)
tests that every `typing.Protocol` in `interfaces.py` and `storage/interfaces.py`
appears in `CONTRACT_INVENTORY.md`, and every Pydantic model in the codebase
appears in `SCHEMA_INVENTORY.md`. The tests run in `pytest -W error` with the
full suite.

**What this catches:** When a new Protocol or model is added to the codebase
without updating the inventory documents, CI fails. The failure is explicit
and sprints don't close with undocumented contracts.

**Scale:** 20 models in `run_trace.py` alone, all with `extra="forbid"`, all
requiring inventory entries. Each sprint that added trace fields (S09: SafetyFlags;
S11: PlanningMetadata, LLMExecution; S14: PipelineManifest, RepairResult; S15:
FeasibilityAssessment, SemanticVerification, ExecutionMetadata) would have
produced CI failures if inventory documentation was omitted.

**Classification: Detection.** The tests don't prevent adding undocumented
fields — they detect the omission before the sprint closes. The 22% CI detection
rate in Jacob's failure data includes documentation drift tests as a category
alongside structural test failures.

**Caveat:** This mechanism only covers documented contracts. Implementation-level
bugs (BUG-0019: wrong flag propagation; BUG-0020: empty plan success) are not
caught by documentation consistency. The documentation drift tests protect the
contract surface, not the implementation behavior.

---

### Failure mode summary table

| Architectural decision | Target failure class | Classification | Key evidence |
|---|---|---|---|
| Protocol file boundaries (AF-0114) | Partial pipeline wiring (import-level) | **Prevention** (import-level) + **Detection** (semantic-level) | 5 wiring bugs pre-S13 → 2 post-S13; BUG-0019 post-extraction |
| `extra="forbid"` on trace models (AF-0005, ADR-0002) | Silent field loss between component versions | **Prevention** | BUG-0023 was detected as display omission, not data loss |
| Loop bounding constants (AF-0055) | Runaway LLM retry/repair cycles | **Prevention** | Zero loop runaway bugs in 24-bug inventory |
| Pipeline manifest (AF-0120) | Version identification for regression debugging | **Detection** | BUG-0019 and BUG-0023 triaged using manifest data |
| Documentation drift tests (AF-0013, AF-0063) | Stale contract and schema documentation | **Detection** | ~22% of CI-detected bugs; every new trace model requires inventory entry |
| Truthful UX invariant (ADR-0001, AF-0031) | False success/failure reporting | **Detection** (catches when a trace lies) | BUG-0020 (empty plan success, P0), BUG-0009 (verifier bypass, P0), BUG-0016 (plan not executed, P1) |

**What the data shows and doesn't show:**
The dominant failure type — trace field placeholders (~10 items across 6 sprints)
— is not fully addressed by any single architectural decision. Placeholders
(`placeholder`, `N/A`, `0`) in trace fields pass `extra="forbid"`, pass the drift
tests, and pass the loop bounds. They are semantic lies told by a structurally
valid trace. The Truthful UX invariant catches some of them (BUG-0020 is
effectively a placeholder run reported as success), but the general placeholder
class requires review-time or live-testing detection — which explains the 57%
live testing detection rate in Jacob's data.

---

*End of document. All file paths reference the `src/` tree at commit HEAD as of Sprint 15 close (Mar 22, 2026). Sprint 16 (AF-0127, AF-0128) is READY, not yet implemented.*
