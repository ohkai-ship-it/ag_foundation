# AF-0119 — Planner trace + per-step LLM attribution
# Version number: v0.1
# Created: 2026-03-22
# Status: READY
# Priority: P1
# Area: Core Runtime / Planner / Recorder

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`

---

## Summary

Record the planner's work as a first-class trace element and populate per-step LLM attribution (`tokens_used`, `model_used`) so that every LLM call in a run is auditable. Currently the planning phase is invisible in the trace and per-step LLM fields are always null.

---

## Problem

Examining `trace.json` for run `8cec9c63-3dfc-40cc-a497-9e7e3e84cae7`:

1. **Planning is invisible.** The LLM made 1 call (11,978 tokens) to generate the plan, but the trace starts at step 0 (the first skill). There is no record of what prompt was sent, what the raw response was, how long planning took, or whether validation corrected anything (relevant to BUG-0018).
2. **Per-step LLM attribution is empty.** Every step shows `tokens_used: null` and `model_used: null`. Step 2 (`synthesize_research`) took 28.8s and clearly made an LLM call, but it's not recorded per-step. The top-level `llm` block has aggregate stats only.

---

## Goal

- Planner work recorded as trace preamble (prompt, response, duration, validation corrections)
- Per-step `tokens_used` and `model_used` populated by skills that call LLMs
- Aggregate `llm` block remains as summary, with per-step breakdown available

---

## Non-goals

- Changing the planner's behavior or LLM selection
- Recording intermediate LLM retries (save for V1Executor scope)
- Persisting raw LLM prompts or full LLM responses in RunTrace (security concern — decided 2026-03-22: record parsed plan steps only, not raw LLM response; avoids prompt/user-data leakage, keeps configuration simple vs env-var toggles)

---

## Design

### Part A: Planner trace preamble

Add a `planning` block to `RunTrace`:

```json
"planning": {
  "planner": "V2Planner",
  "plan_id": "plan_e5348e14966b",
  "started_at": "...",
  "ended_at": "...",
  "duration_ms": 1234,
  "llm_call": {
    "model": "gpt-4o-mini",
    "input_tokens": 11333,
    "output_tokens": 645,
    "total_tokens": 11978
  },
  "raw_plan_steps": [...],       // parsed steps only (no raw LLM response)
  "validation_corrections": [],  // auto-corrections applied (e.g. BUG-0018)
  "confidence": 0.85
}
```

Implementation:
- Planner returns a `PlanResult` that includes timing + LLM metadata
- `create_runtime()` / orchestrator stores this in the RunTrace before execution begins

### Part B: Per-step LLM attribution

Skills that make LLM calls must populate `tokens_used` and `model_used` in their step output. This requires:
- Skill return type (`SkillOutput` or equivalent) gains optional `llm_metadata` field
- Executor copies `llm_metadata` into the Step record
- `synthesize_research` and any LLM-calling skills populate the field

---

## Acceptance criteria

- [ ] RunTrace contains `planning` block with planner name, timing, token usage
- [ ] `ag runs show <id> --json` displays planning metadata
- [ ] `synthesize_research` step shows `tokens_used` and `model_used`
- [ ] Aggregate `llm` block is consistent with sum of per-step + planning tokens
- [ ] New test: planner metadata present in trace after plan-based run
- [ ] New test: per-step LLM attribution populated for LLM-calling skills
- [ ] `pytest -W error` passes
- [ ] `ruff check src tests` passes

---

## Dependencies

- Builds on AF-0103 (V2Planner) and AF-0117 (V1Orchestrator)
- Pairs well with AF-0118 (V1Recorder evidence persistence)

---

## Risks

- Schema change to RunTrace (additive, backward-compatible with `planning: null` default)
- Skills must opt-in to LLM attribution — existing skills without LLM calls unaffected
