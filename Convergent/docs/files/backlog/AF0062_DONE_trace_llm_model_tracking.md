# BACKLOG ITEM — AF0062 — trace_llm_model_tracking
# Version number: v0.2

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI discipline (ruff + pytest -W error + coverage)
> - 1 PR = 1 primary AF
> - INDEX update rule (status ↔ filename integrity)

> **File naming (required):** `AF####_<Status>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0062
- **Type:** Feature
- **Status:** DONE
- **Priority:** P1
- **Area:** Core
- **Owner:** Kai
- **Target sprint:** Sprint07 (after AF0065)

---

## Problem
RunTrace currently captures execution details but **not which LLM was used**:

**Current RunTrace fields:**
- `mode`: manual | llm (just the mode, not specifics)
- `playbook`: name/version
- `steps`: execution log
- `metadata`: generic dict (optional)

**Missing:**
- Which provider (openai, anthropic, local)
- Which model (gpt-4o, gpt-4o-mini, claude-3-opus, etc.)
- Potentially: token counts, cost, latency per call

This makes it impossible to:
- Know which model produced a result
- Compare runs across different models
- Track costs
- Debug model-specific issues
- Ensure truthful UX (user should know what generated the output)

---

## Goal
Extend RunTrace schema to capture LLM execution details.

**Minimum viable:**
- Provider name (openai, anthropic, manual, none)
- Model identifier (gpt-4o-mini, claude-3-sonnet, etc.)

**Nice to have:**
- Token counts (input/output/total)
- API latency
- Cost (if computable)

---

## Non-goals
- Changing provider implementation (just capturing what's already known)
- Token counting implementation (v1+)
- Cost calculation (v1+)

---

## Design options

### Option A: Add fields to RunTrace root
```python
class RunTrace(BaseModel):
    # ... existing fields ...
    provider: str | None = Field(default=None, description="LLM provider used")
    model: str | None = Field(default=None, description="Model identifier")
```

**Pros:** Simple, flat structure
**Cons:** Only captures one model per run (what if multiple?)

### Option B: Add nested LLMExecution model
```python
class LLMExecution(BaseModel):
    provider: str
    model: str
    call_count: int = 0
    total_tokens: int | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None

class RunTrace(BaseModel):
    # ... existing fields ...
    llm: LLMExecution | None = Field(default=None, description="LLM execution details")
```

**Pros:** Extensible, can add more fields later
**Cons:** More complex, nested structure

### Option C: Per-step model tracking
```python
class Step(BaseModel):
    # ... existing fields ...
    model_used: str | None = Field(default=None, description="Model for this step")
```

**Pros:** Captures model per step (useful for multi-model runs)
**Cons:** Redundant if same model for all steps

### Recommendation
**Option B** — nested `LLMExecution` model with run-level summary, plus **Option C** per-step tracking for detail.

> **CONFIRMED:** This design choice was reviewed and approved. Implement both:
> - Run-level `llm: LLMExecution` for summary stats
> - Per-step `model_used: str | None` for step-level detail

---

## Acceptance criteria (Definition of Done)
- [x] RunTrace includes `llm` field with provider/model
- [x] `ag runs show --json` displays LLM info
- [x] `ag runs list` shows model column (optional)
- [x] Manual mode runs show "manual" or null for model
- [x] Existing traces without LLM field still load (backward compatible)
- [x] Tests cover new schema fields
- [x] `pytest -W error` passes
- [x] `ruff check src tests` passes

---

## Implementation notes

### Schema change (run_trace.py)
```python
class LLMExecution(BaseModel):
    """LLM execution details for a run."""
    provider: str = Field(..., description="Provider name (openai, anthropic, manual)")
    model: str | None = Field(default=None, description="Model identifier")
    call_count: int = Field(default=0, ge=0, description="Number of LLM calls")
    # Future: token counts, cost
    
    model_config = {"extra": "forbid"}

class RunTrace(BaseModel):
    # ... existing fields ...
    llm: LLMExecution | None = Field(
        default=None, 
        description="LLM execution details (null for manual mode)"
    )
```

### Capture point
The runtime already knows the provider/model when it makes calls. Need to:
1. Pass model info to RunTraceBuilder
2. Populate `llm` field before saving trace

### CLI display
```
Run ID:    abc12345
Status:    SUCCESS
Mode:      llm
Provider:  openai
Model:     gpt-4o-mini
Duration:  2.3s
```

---

## Risks
- Schema version bump may be needed (trace_version: "0.2"?)
- Existing traces need graceful handling of missing field

---

## Related
- AF0060 (Skill definition framework) — skills need LLM access, should track usage
- ADR002 (Trace versioning strategy) — how to handle schema evolution

---

## Documentation impact
- **ARCHITECTURE.md:** Update RunTrace schema documentation
- **CLI_REFERENCE.md:** Update `ag runs show` output examples

---

# Completion section (fill when done)

## 1) Metadata
- **Backlog item (primary):** AF0062
- **PR:** #<number>
- **Author:** <name>
- **Date:** YYYY-MM-DD
- **Branch:** feat/trace-llm-tracking
- **Risk level:** P1
- **Runtime mode used for verification:** llm

---

## 2) Acceptance criteria verification
(Copy AC list and mark when done)

---

## 3) What changed (file-level)
(Fill when done)

---

## 4) Architecture alignment (mandatory)
- **Layering:** Core schema change in run_trace.py, propagates to CLI display

