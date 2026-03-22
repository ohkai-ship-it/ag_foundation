# AF-0121 — V3Planner: feasibility assessment
# Version number: v0.1
# Created: 2026-03-22
# Status: READY
# Priority: P1
# Area: Core Runtime / Planner

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`

---

## Summary

Implement V3Planner based on the accepted ADR-0009 design. V3Planner adds a feasibility assessment phase *before* plan generation: it evaluates whether the task can be performed with available skills and playbooks, identifies capability gaps, and only generates a plan if the task is feasible. This structurally prevents the empty-plan-as-success problem (BUG-0020).

---

## Problem

V0/V1/V2 planners assume all tasks are achievable. When they can't find matching capabilities:
- V2Planner returns zero steps with a warning, but pipeline continues to "success" (BUG-0020)
- Users get no actionable feedback about *what's* missing or *why* the task can't be performed
- No structured way to report capability gaps or suggest alternatives

---

## Goal

- V3Planner performs feasibility assessment before plan generation
- Tasks below feasibility threshold produce a clear `NOT_FEASIBLE` result with reasons
- Capability gaps are identified and reported to the user
- Feasible tasks proceed to plan generation as normal
- CLI displays feasibility assessment before asking for plan approval

---

## Non-goals

- Changing V0/V1/V2 planner behavior (V3 is additive)
- Automatic capability acquisition (installing new skills at runtime)
- Multi-agent delegation to external systems for missing capabilities

---

## Design

Based on **ADR-0009** (accepted). Two-phase LLM approach:

### Phase 1: Feasibility assessment

```python
class FeasibilityLevel(Enum):
    FULLY_FEASIBLE = "fully_feasible"         # 0.8–1.0
    MOSTLY_FEASIBLE = "mostly_feasible"       # 0.6–0.8
    PARTIALLY_FEASIBLE = "partially_feasible" # 0.3–0.6
    NOT_FEASIBLE = "not_feasible"             # 0.0–0.3

class CapabilityGap(BaseModel):
    missing_capability: str
    description: str
    required_for: str
    workaround: str | None

class FeasibilityAssessment(BaseModel):
    level: FeasibilityLevel
    score: float
    reason: str
    capability_gaps: list[CapabilityGap]
    recommendations: list[str]
```

### Phase 2: Conditional plan generation

- `FULLY_FEASIBLE` / `MOSTLY_FEASIBLE` → generate plan normally
- `PARTIALLY_FEASIBLE` → generate partial plan, warn about gaps
- `NOT_FEASIBLE` → return assessment only, no plan generation

### LLM integration (CRITICAL — follow existing patterns)

V3Planner extends V2Planner. Use the **same provider injection** pattern:

```python
from ag.providers.base import LLMProvider, ChatMessage, MessageRole

class V3Planner(V2Planner):
    """Two-phase planner: feasibility assessment → conditional plan generation."""

    def __init__(self, provider: LLMProvider, skill_registry: SkillRegistry) -> None:
        super().__init__(provider, skill_registry)

    def plan(self, task: TaskSpec) -> Playbook:
        # Phase 1: feasibility assessment (new LLM call)
        assessment = self._assess_feasibility(task)
        if assessment.level == FeasibilityLevel.NOT_FEASIBLE:
            return self._build_infeasible_result(assessment)

        # Phase 2: delegate to V2Planner.plan() for plan generation
        playbook = super().plan(task)
        playbook.metadata["feasibility"] = assessment.model_dump()
        return playbook

    def _assess_feasibility(self, task: TaskSpec) -> FeasibilityAssessment:
        catalog = self._get_skill_catalog()
        playbook_catalog = self._get_playbook_catalog()
        messages = [
            ChatMessage(role=MessageRole.SYSTEM, content=self._feasibility_system_prompt()),
            ChatMessage(role=MessageRole.USER, content=self._feasibility_user_prompt(task, catalog, playbook_catalog)),
        ]
        response = self.provider.chat(messages=messages)
        # Parse structured response into FeasibilityAssessment
        return self._parse_feasibility(response.content)
```

**Provider instantiation** — CLI already creates a provider for V2Planner. Same instance is reused:
```python
# In src/ag/cli/main.py (existing pattern)
provider = get_provider(ProviderConfig(provider="openai", model="gpt-4o-mini"))
planner = V3Planner(provider, registry)  # ← replaces V2Planner(provider, registry)
```

### Default pipeline version update (CRITICAL)

Sprint 15 must update the default pipeline versions:
- `src/ag/core/runtime.py` `create_runtime()`: currently hardcodes V0Planner — not relevant (CLI bypasses it)
- `src/ag/cli/main.py`: currently instantiates `V2Planner(provider, registry)` — **change to `V3Planner`**
- `ARCHITECTURE.md` implementation map: update Planner row to show V3Planner as current

### Integration points

- `PlanningMetadata` (AF-0119) gains `feasibility_level` and `feasibility_score` fields
- CLI displays feasibility assessment before the plan approval prompt
- V1Orchestrator checks feasibility before execution (guard for non-V3 planners)

### Files touched

| File | Change |
|------|--------|
| `src/ag/core/planner.py` | V3Planner class with two-phase approach |
| `src/ag/core/run_trace.py` | `FeasibilityAssessment` model, `PlanningMetadata` extension |
| `src/ag/cli/main.py` | **Replace V2Planner with V3Planner as default**; display feasibility assessment in inline plan flow |
| `ARCHITECTURE.md` | Update implementation map: Planner → V3Planner |
| `tests/test_runtime.py` | V3Planner tests: feasible/not-feasible/partial scenarios |

---

## Acceptance criteria

- [ ] V3Planner returns `NOT_FEASIBLE` for tasks with no matching capabilities
- [ ] `NOT_FEASIBLE` assessment prevents plan execution (no empty-plan success)
- [ ] Capability gaps listed with descriptions and workaround suggestions
- [ ] CLI displays feasibility level and gaps before plan approval
- [ ] `FULLY_FEASIBLE` tasks produce plans identical to V2Planner
- [ ] `PARTIALLY_FEASIBLE` tasks produce partial plans with warnings
- [ ] Feasibility data recorded in RunTrace.planning
- [ ] `pytest -W error` passes
- [ ] `ruff check src tests` passes

---

## Dependencies

- ADR-0009 (accepted — design reference)
- AF-0119 (PlanningMetadata structure, Sprint 14)
- BUG-0020 quick guard (should be implemented first as safety net)

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Extra LLM call adds latency | ~1-2s per run | Feasibility call is lightweight (capability list + task, no full plan) |
| LLM overestimates feasibility | Misses gaps | Conservative scoring + explicit capability gap enumeration |
| V3 replaces V2 as default | Breaking change if V3 has different behavior | Additive: V3 extends V2, selectable via config |
