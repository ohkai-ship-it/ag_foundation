# BACKLOG ITEM — AF0104 — llm_planner_v3_feasibility
# Version number: v0.1

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

> **File naming (required):** `AF####_<STATUS>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0104
- **Type:** Feature
- **Status:** DONE
- **Priority:** P2
- **Area:** Core Runtime / Planner
- **Owner:** TBD
- **Target sprint:** S14
- **Depends on:** AF-0103 (V2Planner skills+playbooks)

---

## Problem

V1 and V2 planners assume the task is achievable with existing capabilities.
But what happens when:

1. The task requires capabilities we don't have?
2. The task is ambiguous and the planner isn't confident?
3. The task would benefit from a skill that doesn't exist yet?

Without feasibility analysis, users get:
- Plans that will fail at execution
- Plans with low confidence that proceed anyway
- No feedback on capability gaps

For mature guided autonomy, the planner should be honest about its limitations.

---

## Goal

Implement `V3Planner` that adds feasibility judgment and capability gap analysis:

```
User: "Book a flight from Berlin to Tokyo for next Tuesday"

V3Planner output:
{
  "feasibility": {
    "score": 0.15,
    "assessment": "NOT_FEASIBLE",
    "reason": "This task requires booking capabilities that are not available"
  },
  "capability_gaps": [
    {
      "missing_capability": "flight_booking",
      "description": "Ability to search and book flights via airline APIs",
      "required_for": "Complete the booking transaction",
      "workaround": "Can research flight options but cannot book"
    },
    {
      "missing_capability": "payment_processing",
      "description": "Ability to process payments",
      "required_for": "Pay for the flight",
      "workaround": null
    }
  ],
  "partial_plan": {
    "description": "What we CAN do with existing capabilities",
    "steps": [
      {"skill": "web_search", "params": {"query": "Berlin to Tokyo flights next Tuesday"}, "rationale": "Find available flights"},
      {"skill": "emit_result", "params": {...}, "rationale": "Present flight options to user"}
    ],
    "outcome": "Research flight options but user must book manually"
  },
  "recommendations": [
    "Consider adding a flight_search skill that uses Skyscanner API",
    "For booking, integration with user's travel account would be needed"
  ]
}
```

---

## Feasibility levels

| Level | Score | Meaning | Action |
|-------|-------|---------|--------|
| `FULLY_FEASIBLE` | 0.8-1.0 | Can accomplish task completely | Proceed with plan |
| `MOSTLY_FEASIBLE` | 0.6-0.8 | Minor gaps, reasonable outcome | Proceed with warnings |
| `PARTIALLY_FEASIBLE` | 0.3-0.6 | Significant gaps, limited outcome | Offer partial plan |
| `NOT_FEASIBLE` | 0.0-0.3 | Cannot meaningfully accomplish | Explain gaps, suggest alternatives |

---

## Non-goals

- Automatically creating new skills (that's future work)
- Refusing to help (always offer what we CAN do)
- External capability discovery (only analyze existing skills)

---

## Acceptance criteria (Definition of Done)

- [ ] `V3Planner` includes feasibility assessment in output
- [ ] Feasibility score (0.0-1.0) calculated based on capability coverage
- [ ] Capability gaps identified with descriptions
- [ ] Partial plan offered when task is partially feasible
- [ ] Recommendations for missing skills provided
- [ ] Clear user-facing messaging for each feasibility level
- [ ] Tests cover all feasibility levels
- [ ] CI passes

---

## Implementation notes

### Enhanced prompt structure
```
SYSTEM: You are an execution planner with self-awareness about your capabilities.

Before creating a plan, assess whether the task is achievable with the available
skills and playbooks. Be honest about limitations.

USER:
Task: {task_description}

Available capabilities:
{skills_and_playbooks}

First, assess feasibility:
1. What capabilities does this task require?
2. Which required capabilities are available?
3. Which required capabilities are MISSING?
4. What is the feasibility score (0.0-1.0)?

Then, based on feasibility:
- If FULLY_FEASIBLE: Create complete plan
- If MOSTLY/PARTIALLY_FEASIBLE: Create plan with warnings about gaps
- If NOT_FEASIBLE: Explain gaps and offer partial plan for what IS possible

Output format:
{json_schema_with_feasibility}
```

### V3Planner output schema
```python
class CapabilityGap(BaseModel):
    missing_capability: str
    description: str
    required_for: str
    workaround: str | None

class FeasibilityAssessment(BaseModel):
    score: float  # 0.0-1.0
    assessment: Literal["FULLY_FEASIBLE", "MOSTLY_FEASIBLE", "PARTIALLY_FEASIBLE", "NOT_FEASIBLE"]
    reason: str

class V3PlannerOutput(BaseModel):
    feasibility: FeasibilityAssessment
    capability_gaps: list[CapabilityGap]
    plan: ExecutionPlan | None  # Full plan if feasible
    partial_plan: ExecutionPlan | None  # What we CAN do
    recommendations: list[str]  # Suggestions for missing skills
```

### CLI integration
```bash
ag plan --task "Book a flight to Tokyo"

⚠️  Task Assessment: PARTIALLY FEASIBLE (score: 0.35)

Capability gaps identified:
  • flight_booking — Cannot book flights (no booking API)
  • payment_processing — Cannot process payments

What we CAN do:
  1. web_search → Find available flights
  2. emit_result → Present options to you

Would you like to proceed with the partial plan? [y/N]
```

---

## Risks

| Risk | Mitigation |
|------|------------|
| LLM overestimates feasibility | Conservative prompting, require confidence justification |
| LLM underestimates feasibility | Test with known-achievable tasks |
| Capability gap descriptions too vague | Require specific missing skill names |
| Users confused by partial plans | Clear messaging about what IS and ISN'T possible |

---

## Open questions

1. Should low feasibility block plan generation entirely?
2. How to handle tasks at the boundary (score ~0.5)?
3. Should recommendations drive a skill backlog?

---

# Completion section (fill when done)

## Outcome
Scoped as feasibility study only per S14 sprint plan ("feasibility study only, no implementation required").

## Deliverable
ADR-0009: V3Planner feasibility design — `docs/dev/decisions/files/ADR009_ACCEPTED_v3planner_feasibility_design.md`

## Key findings
- Current V1/V2 planners already emit a `confidence` float but with no structured capability-gap reasoning
- Two-phase LLM design (feasibility assessment + conditional plan generation) is the recommended approach
- Pydantic schemas designed: `FeasibilityLevel`, `CapabilityGap`, `FeasibilityAssessment`, `V3PlannerOutput`
- `PlanningMetadata` (AF-0119) should gain `feasibility_level` / `feasibility_score` fields when V3 ships
- Implementation scoped to Sprint 15: ~7 steps, fully additive, V0/V1/V2 unaffected

## Status
DONE — feasibility study complete, ADR-0009 accepted, implementation deferred to S15.
