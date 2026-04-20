# BACKLOG ITEM — AF0103 — llm_planner_v2_playbooks
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
- **ID:** AF0103
- **Type:** Feature
- **Status:** DONE
- **Priority:** P2
- **Area:** Core Runtime / Planner
- **Owner:** S13
- **Target sprint:** Sprint 13
- **Depends on:** AF-0102 (V1Planner skills-only)

---

## Problem

V1Planner (AF-0102) can compose plans from individual skills, but it doesn't
leverage existing playbooks. Playbooks are pre-validated, tested sequences
that encapsulate domain expertise (e.g., `research_v0` is a proven research
pipeline).

For efficient planning, the LLM should be able to:
1. Use a playbook as a single "macro" step when it fits
2. Compose mixed plans with both playbooks and individual skills
3. Understand when a playbook is overkill vs. when it's the right tool

---

## Goal

Implement `V2Planner` that extends V1Planner to use both skills AND playbooks:

```
User: "Research climate change impacts on agriculture and summarize key findings"

V2Planner receives:
- Task description
- List of available skills (from V1)
- List of available playbooks with their skill sequences

V2Planner LLM output:
{
  "plan_id": "plan_xyz789",
  "task": "Research climate change impacts...",
  "steps": [
    {
      "type": "playbook",
      "playbook": "research_v0",
      "params": {"query": "climate change agriculture impacts"},
      "rationale": "research_v0 handles the full research pipeline"
    },
    {
      "type": "skill",
      "skill": "summarize_docs",
      "params": {"documents": "{{step_0_output.artifacts}}"},
      "rationale": "Additional summarization of research output"
    }
  ],
  "estimated_tokens": 8000,
  "confidence": 0.90
}
```

---

## Non-goals

- Creating new playbooks dynamically (playbooks are predefined)
- Modifying playbook internals (playbooks are atomic units)
- Judging feasibility (that's V3Planner, AF-0104)

## Implementation decisions (Sprint 13 planning)

- **Multiple playbooks in sequence:** Yes, a plan can have multiple playbooks.
- **Orchestrator:** V1Orchestrator created as part of this sprint (AF-0117 partial).
  V1Orchestrator handles mixed plans: iterates plan steps and, for `type=playbook`
  steps, loads and executes that playbook's skill sequence inline.
  V0Orchestrator stays untouched.
- **PlaybookStepType:** Add `PLAYBOOK = "playbook"` to the enum. The planner
  outputs `PlannedStep` with `type: Literal["skill", "playbook"]`, and the
  plan-to-playbook conversion maps this to `PlaybookStepType.PLAYBOOK`.
- **V1Verifier wiring:** `create_runtime()` switches to V1Verifier as default
  (AF-0115). V0Verifier stays in file for reference.

---

## Acceptance criteria (Definition of Done)

- [ ] `V2Planner` extends/replaces V1Planner
- [ ] Planner receives both skill registry AND playbook registry
- [ ] LLM prompt includes playbook descriptions and their skill sequences
- [ ] Plan steps can be either `{"type": "skill", ...}` or `{"type": "playbook", ...}`
- [ ] Playbook steps expand to their skill sequence during execution
- [ ] Planner prefers playbooks for well-known task patterns
- [ ] Planner uses individual skills for custom composition
- [ ] Tests verify mixed skill+playbook plans
- [ ] CI passes

---

## Implementation notes

### Playbook metadata extraction
```python
def get_playbook_catalog() -> list[PlaybookMetadata]:
    """Extract playbook info for LLM context."""
    registry = get_playbook_registry()
    return [
        PlaybookMetadata(
            name=playbook.name,
            description=playbook.description,
            steps=[step.skill_name for step in playbook.steps],
            use_cases=playbook.use_cases,  # When to use this playbook
        )
        for playbook in registry.list_playbooks()
    ]
```

### Enhanced prompt structure
```
SYSTEM: You are an execution planner...

USER:
Task: {task_description}

Available playbooks (pre-built sequences):
- research_v0: "Full research pipeline for web-based research"
  Steps: web_search → fetch_web_content → synthesize_research → emit_result
  Use when: User wants comprehensive research on a topic

- summarize_v0: "Document summarization pipeline"
  Steps: load_documents → summarize_docs → emit_result
  Use when: User wants to summarize existing documents

Available skills (for custom composition):
{formatted_skill_catalog}

Strategy:
1. Prefer playbooks when the task closely matches a playbook's use case
2. Use individual skills when playbooks don't fit or for additional steps
3. You can mix playbooks and skills in a single plan

Create an execution plan as JSON:
{json_schema}
```

### Plan schema extension
```python
class PlannedStep(BaseModel):
    type: Literal["skill", "playbook"]
    skill: str | None = None  # For type="skill"
    playbook: str | None = None  # For type="playbook"
    params: dict[str, Any]
    rationale: str
```

---

## Risks

| Risk | Mitigation |
|------|------------|
| LLM always picks playbooks (lazy) | Prompt engineering: "Use skills when playbook is overkill" |
| LLM never picks playbooks | Prompt engineering: "Prefer playbooks for matching use cases" |
| Param chaining between playbook and skill | Define clear output contract for playbooks |
| Playbook output format varies | Standardize playbook output schema |

---

## Open questions

1. Should playbook output schema be standardized?
2. Can a plan have multiple playbooks in sequence?
3. How to handle playbook params that differ from skill params?

---

# Completion section (fill when done)

_To be filled upon completion_
