# ADR-0009 — V3Planner: Feasibility Judgment Design
# Version number: v0.1

## Status
ACCEPTED

## Date
2026-03-22

## Context
AF-0104 (S14 scope: feasibility study only) — assess whether and how a V3Planner that
judges task feasibility before planning should be built, given the current planner lineage.

### Current planner lineage

| Class | Strategy | LLM call | Confidence field |
|-------|----------|-----------|-----------------|
| `V0Planner` | Registry lookup, requires `--playbook` flag | None | None |
| `V1Planner` | LLM composes skill sequence from task description | Yes | `float 0–1` in `LLMPlanResponse` |
| `V2Planner` | LLM composes mixed skill + playbook plan | Yes | `float 0–1` in `LLMPlanResponse` |
| `V3Planner` | Feasibility assessment + capability-gap analysis | Yes (2-phase or extended) | `FeasibilityAssessment` + `float` |

V1 and V2 already produce a `confidence` score, but:
- The score is self-reported by the LLM with no structured reasoning
- No capability gap analysis is performed
- Low-confidence plans are logged but always executed
- There is no partial-plan or user-facing "we can only do X of Y" messaging

### What V3Planner adds

1. **Feasibility assessment first** — before producing steps, explicitly reason about which
   required capabilities exist vs. are missing
2. **Structured gap list** — each missing capability gets a `CapabilityGap` entry with
   `description`, `required_for`, and optional `workaround`
3. **Feasibility level** — `FULLY_FEASIBLE / MOSTLY_FEASIBLE / PARTIALLY_FEASIBLE / NOT_FEASIBLE`
   with a numeric score `0.0–1.0` to allow threshold-based routing
4. **Partial plan** — always offer what IS achievable; never refuse silently
5. **Recommendations** — LLM suggests missing skills that would close the gap

---

## Decision

Implement `V3Planner` in Sprint 15 as a two-phase LLM call:

**Phase 1 — Feasibility assessment:**
- Prompt includes task, full skill catalog, and explicit reasoning scaffold
- LLM returns `FeasibilityAssessment` + `list[CapabilityGap]` + `recommendations`
- Short, cheap call; can abort before expensive plan generation if clearly infeasible

**Phase 2 — Plan generation (conditional):**
- If `FULLY_FEASIBLE` or `MOSTLY_FEASIBLE`: call V2-equivalent plan generation
- If `PARTIALLY_FEASIBLE`: generate plan scoped to available capabilities only
- If `NOT_FEASIBLE`: skip plan generation, return gap report + minimal rescue attempt

This two-phase approach is preferred over a single extended prompt because:
- Token efficiency: feasibility phase uses a smaller context (catalog only)
- Separation of concerns: feasibility reasoning is explicit, not mixed into plan steps
- Testability: each phase can be tested independently with stub providers

### Pydantic schemas (proposed)

```python
class FeasibilityLevel(str, Enum):
    FULLY_FEASIBLE      = "FULLY_FEASIBLE"       # score 0.8–1.0
    MOSTLY_FEASIBLE     = "MOSTLY_FEASIBLE"      # score 0.6–0.8
    PARTIALLY_FEASIBLE  = "PARTIALLY_FEASIBLE"   # score 0.3–0.6
    NOT_FEASIBLE        = "NOT_FEASIBLE"         # score 0.0–0.3

class CapabilityGap(BaseModel):
    missing_capability: str        # e.g. "flight_booking"
    description: str               # human-readable explanation
    required_for: str              # which part of the task needs it
    workaround: str | None         # what we CAN do instead

class FeasibilityAssessment(BaseModel):
    level: FeasibilityLevel
    score: float                   # 0.0–1.0
    reason: str                    # brief summary sentence
    capability_gaps: list[CapabilityGap]
    recommendations: list[str]     # suggested missing skills

class V3PlannerOutput(BaseModel):
    feasibility: FeasibilityAssessment
    plan: Playbook | None          # full plan if FULLY/MOSTLY feasible
    partial_plan: Playbook | None  # what we CAN do (PARTIALLY feasible)
```

### RunTrace integration

`PlanningMetadata` (AF-0119) should gain two optional fields:
- `feasibility_level: str | None`
- `feasibility_score: float | None`

This keeps the trace self-describing without coupling it to V3Planner schemas.

### CLI integration (future)

```
ag plan "Book a flight to Tokyo"

⚠️  Task Assessment: PARTIALLY FEASIBLE (score: 0.35)
Capability gaps:
  • flight_booking — no airline API integration
  • payment_processing — no payment capability

What we CAN do (2 steps):
  1. web_search → Find flight options
  2. emit_result → Present options for manual booking

Proceed with partial plan? [y/N]
```

This requires `ag plan` to surface `V3PlannerOutput.feasibility` before asking for approval.

---

## Alternatives considered

### A) Single extended prompt (V2 + feasibility inline)
Pros: single LLM call, simpler code path  
Cons: reasoning gets mixed into plan steps; harder to test; higher token usage if task is infeasible  
**Rejected**: two-phase is cleaner and more testable

### B) Confidence threshold on V2 (low effort)
Use existing `confidence < 0.5` to trigger a warning  
Pros: minimal code (current `warnings` field already exists in `LLMPlanResponse`)  
Cons: confidence is self-reported without structured gap analysis; no partial plan  
**Rejected as insufficient**: gap identification requires structured output

### C) Post-execution feasibility check (retrospective)
Assess feasibility after the plan fails  
Pros: simpler pre-run path  
Cons: wastes execution resources; poor UX  
**Rejected**: detect early, not late

---

## Implementation plan (Sprint 15 scope)

| Step | What | Estimated effort |
|------|------|-----------------|
| 1 | Add `FeasibilityLevel`, `CapabilityGap`, `FeasibilityAssessment` Pydantic models to `planner.py` | Small |
| 2 | Implement `V3Planner._assess_feasibility()` (Phase 1 LLM call) | Medium |
| 3 | Implement `V3Planner.plan()` routing based on feasibility level | Medium |
| 4 | Add `feasibility_level` / `feasibility_score` to `PlanningMetadata` (additive) | Small |
| 5 | Update `ag plan` CLI to display feasibility assessment before approval | Small |
| 6 | Tests: all four feasibility levels with stub provider | Medium |
| 7 | Update INDEX_BACKLOG, `create_runtime()` to accept planner kwarg | Small |

Estimate: 1 sprint (S15), low risk — purely additive, V0/V1/V2 paths unaffected.

---

## Consequences

**Pros:**
- Honest UX: users know before execution whether the task is achievable
- Capability gaps drive skill backlog (recommendations = future AFs)
- Partial plans prevent silent failures for near-feasible tasks
- Fully additive — V0/V1/V2 are untouched; `create_runtime()` continues to default to V0

**Cons:**
- Extra LLM call per run (Phase 1) — cost and latency tradeoff
- LLM may overestimate or underestimate feasibility; needs conservative prompting
- Users may be confused by "partial plan" concept; requires clear CLI messaging

---

## Open questions (deferred to S15)

1. Should `NOT_FEASIBLE` scoring block plan execution entirely, or always offer the partial plan?
2. How to handle edge-case scores near thresholds (e.g., 0.59 vs 0.61)?
3. Should capability gap `recommendations` feed an automation backlog AF?
