# AF-0122 — CLI planning and pipeline display
# Version number: v0.1
# Created: 2026-03-22
# Status: READY
# Priority: P2
# Area: CLI

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`

---

## Summary

Display planning metadata (planner name, LLM tokens, duration, confidence) and pipeline manifest (component versions) in the CLI output for `ag run` and `ag runs show`. Currently this data is captured in RunTrace (AF-0119, AF-0120) but only visible via `--json`. The planner LLM call is often the most expensive single call in a run and should be visible to users.

---

## Problem

After Sprint 14, `RunTrace` contains rich planning and pipeline data:
- `planning.planner`, `planning.duration_ms`, `planning.llm_call` (model, tokens), `planning.confidence`
- `pipeline.planner`, `pipeline.orchestrator`, `pipeline.executor`, `pipeline.verifier`, `pipeline.recorder`

None of this is shown in the human-readable CLI output. Users must use `--json` and search through raw JSON to see which planner was used, how many tokens planning consumed, or which component versions ran.

---

## Goal

- `ag run` post-execution output shows planning summary line
- `ag runs show` displays a "Planning" section and a "Pipeline" section
- Token transparency: users see exactly how much the planner consumed

---

## Non-goals

- Changing the RunTrace schema (data is already there)
- Adding new CLI commands
- Real-time planning progress display (stream events — future)

---

## Design

### `ag run` output (after execution)

Add two lines to the post-execution summary:

```
Run completed
  Plan ID: plan_b06a8fdbfa1d
  Run ID: 86ebd367-8efd-434a-a8f6-587c618fe560
  Workspace: ws01
  Autonomy: guided (inline plan)
  Planning: V2Planner (645 tokens, 1.2s, confidence: 85%)    ← NEW
  Pipeline: V2Planner → V1Orchestrator → V0Executor → V1Verifier → V0Recorder  ← NEW
  Status: success
  Verifier: passed
  Duration: 32.1s
  Playbook: v2plan_f00c5443@1.0.0
```

### `ag runs show` output (human)

Add a "Planning" and "Pipeline" section:

```
Planning
  Planner:    V2Planner
  Duration:   1234ms
  Tokens:     11978 (input: 11333, output: 645)
  Model:      gpt-4o-mini
  Confidence: 85%

Pipeline
  Planner:      V2Planner
  Orchestrator: V1Orchestrator
  Executor:     V0Executor
  Verifier:     V1Verifier
  Recorder:     V0Recorder
```

### Graceful degradation

- If `trace.planning` is `None` (old traces): omit "Planning" section
- If `trace.pipeline` is `None` (old traces): omit "Pipeline" section

### Files touched

| File | Change |
|------|--------|
| `src/ag/cli/main.py` | Format planning + pipeline in run output and runs show |
| `tests/test_cli.py` | Verify planning/pipeline lines present in CLI output |

---

## Acceptance criteria

- [ ] `ag run` output includes planning summary line (planner, tokens, duration, confidence)
- [ ] `ag run` output includes pipeline summary line (component names in arrow notation)
- [ ] `ag runs show` displays Planning section with full breakdown
- [ ] `ag runs show` displays Pipeline section with all 5 components
- [ ] Old traces without planning/pipeline data render gracefully (no errors, sections omitted)
- [ ] `pytest -W error` passes
- [ ] `ruff check src tests` passes

---

## Dependencies

- AF-0119 (PlanningMetadata in RunTrace — Sprint 14)
- AF-0120 (PipelineManifest in RunTrace — Sprint 14)

---

## Risks

- Minimal — display-only changes, no runtime behavior affected
- CLI output format changes may affect tests that assert on exact output strings
