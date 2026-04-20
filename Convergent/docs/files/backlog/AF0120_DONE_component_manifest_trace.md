# AF-0120 — Component manifest in RunTrace
# Version number: v0.1
# Created: 2026-03-22
# Status: DONE
# Priority: P2
# Area: Core Runtime / Recorder

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`

---

## Summary

Add a `pipeline` block to RunTrace that records which component versions (Planner, Orchestrator, Executor, Verifier, Recorder) were used for the run. Currently this information must be inferred indirectly from trace artifacts.

---

## Problem

The trace contains no explicit record of which pipeline components executed the run. With V0/V1/V2 variants coexisting:

- You can guess `V1Planner` from `playbook.name: "v1plan_..."` but that's indirect
- Orchestrator, Executor, Verifier, Recorder versions are completely invisible
- Reproducing a bug requires knowing the exact component mix
- `create_runtime()` selects components but doesn't record the selection

---

## Goal

- RunTrace includes `pipeline` manifest listing component class names
- `ag runs show <id>` displays the pipeline configuration
- Reproducibility: given a trace, you know exactly which components ran

---

## Non-goals

- Component version negotiation or selection logic (that's `create_runtime()`)
- Changing how components are selected
- Adding component-level configuration details beyond class name

---

## Design

Add a `pipeline` block to `RunTrace`:

```json
"pipeline": {
  "planner": "V2Planner",
  "orchestrator": "V1Orchestrator",
  "executor": "V0Executor",
  "verifier": "V1Verifier",
  "recorder": "V0Recorder"
}
```

Implementation:
- `create_runtime()` already instantiates all components — capture their class names
- Store in RunTrace before execution begins
- Simple: `{role: component.__class__.__name__ for role, component in ...}`

---

## Acceptance criteria

- [ ] RunTrace contains `pipeline` block with all 5 component names
- [ ] `ag runs show <id> --json` includes pipeline manifest
- [ ] New test: pipeline block present and correct in trace
- [ ] Backward-compatible: old traces without `pipeline` block still load
- [ ] `pytest -W error` passes
- [ ] `ruff check src tests` passes

---

## Dependencies

- Pairs naturally with AF-0119 (planner trace) and AF-0118 (V1Recorder)
- No blocking dependencies

---

## Risks

- Minimal — purely additive schema change with `pipeline: null` default
- One-session scope, low complexity

---

# Completion section (fill when done)

## Outcome
Implemented as designed. `PipelineManifest` model and `RunTrace.pipeline` field were already present in `src/ag/core/run_trace.py`. `create_runtime()` populates the manifest from component class names.

## Deliverable
- `src/ag/core/run_trace.py` — `PipelineManifest` model, `RunTrace.pipeline: PipelineManifest | None`
- `src/ag/core/runtime.py` — `create_runtime()` builds manifest from component instances
- `tests/test_runtime.py` — added `TestPipelineManifest` class (5 tests)
- `ag runs show <id> --json` exposes `pipeline` block

## Key findings
- Feature was already partially implemented; sprint work verified and tested the integration
- `PipelineManifest` is backward-compatible: old traces load cleanly with `pipeline: null`
- `V1Orchestrator` reads `RunTrace.pipeline` for logging/routing context

## Status
DONE — pipeline manifest in RunTrace, 5 tests pass
