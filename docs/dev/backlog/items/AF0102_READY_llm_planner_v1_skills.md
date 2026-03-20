# BACKLOG ITEM — AF0102 — llm_planner_v1_skills
# Version number: v0.3

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
- **ID:** AF0102
- **Type:** Feature
- **Status:** READY
- **Priority:** P1
- **Area:** Core Runtime / Planner
- **Owner:** TBD
- **Target sprint:** Sprint 11 — guided_autonomy_enablement
- **Depends on:** —

---

## Problem

The current `V0Planner` is a simple registry lookup — it requires users to
explicitly specify `--playbook <name>`. There is no intelligence in selecting
or composing execution plans.

For guided autonomy, the planner must:
1. Analyze the user's task description
2. Understand what skills are available
3. Autonomously compose a skill sequence to accomplish the task
4. Present this plan for user approval (via AF-0098)

Without LLM involvement, there is no "autonomy" in guided autonomy.

---

## Goal

Implement `V1Planner` that uses an LLM to compose execution plans from the
available skill set. **V1Planner is a pure function** — it returns an in-memory
`Playbook` object with zero disk I/O. Plan storage is handled by AF-0098.

```
User: "Research the population growth of Tokyo over the last 50 years"

V1Planner receives:
- Task description (TaskSpec)
- Skill registry with metadata (name, description, I/O schemas)

V1Planner LLM prompt (conceptual):
"""
You are a task planner. Given a task and available skills, create an
execution plan as a sequence of skill invocations.

Task: Research the population growth of Tokyo over the last 50 years

Available skills:
- web_search: Search the web for information. Input: {query: str}. Output: {results: list[SearchResult]}
- fetch_web_content: Fetch content from URLs. Input: {urls: list[str]}. Output: {content: list[WebContent]}
- synthesize_research: Synthesize research into a report. Input: {content: str, task: str}. Output: {report: str}
- emit_result: Save final output as artifact. Input: {content: str, filename: str}. Output: {artifact_path: str}
- load_documents: Load documents from workspace. Input: {path: str}. Output: {documents: list[Document]}
- summarize_docs: Summarize documents. Input: {documents: list[Document]}. Output: {summary: str}

Create a plan as a JSON array of steps. Each step has:
- skill: skill name
- params: input parameters for this step (initial values only)
- rationale: why this step is needed
"""

V1Planner returns Playbook with steps:
[
  {"skill": "web_search", "params": {"query": "Tokyo population growth 1975-2025"}, "rationale": "Find sources"},
  {"skill": "fetch_web_content", "params": {}, "rationale": "Fetch content from search results"},
  {"skill": "synthesize_research", "params": {}, "rationale": "Analyze findings"},
  {"skill": "emit_result", "params": {"filename": "tokyo_population_research.md"}, "rationale": "Save report"}
]
```

**Param chaining:** The orchestrator chains step outputs at runtime (existing
behavior). V1Planner generates initial params only — no placeholder syntax.

---

## Non-goals

- **Disk I/O** — V1Planner is pure; plan storage is AF-0098's responsibility
- Using playbooks as building blocks (that's V2Planner, AF-0103)
- Judging task feasibility or recommending new skills (that's V3Planner, AF-0104)
- Executing the plan (that's AF-0099)
- Dynamic re-planning during execution
- Param chaining syntax — orchestrator handles at runtime

---

## Acceptance criteria (Definition of Done)

- [ ] `V1Planner` class implemented in `src/ag/core/runtime.py` (or new module)
- [ ] Planner receives skill registry and extracts skill metadata (name, description, I/O schema)
- [ ] LLM prompt template includes task + all available skills
- [ ] LLM returns structured plan (JSON schema validated)
- [ ] Plan includes: steps[], estimated_tokens, confidence score
- [ ] Each step includes: skill name, params, rationale
- [ ] Planner handles LLM errors gracefully (timeout, malformed response)
- [ ] Planner validates that all referenced skills exist
- [ ] Unit tests with mocked LLM responses
- [ ] Integration test with real LLM (can be marked slow/optional)
- [ ] CI passes

---

## Implementation notes

### Skill metadata extraction
```python
def get_skill_catalog() -> list[SkillMetadata]:
    """Extract skill info for LLM context."""
    registry = get_default_registry()
    return [
        SkillMetadata(
            name=skill.name,
            description=skill.description,
            input_schema=skill.input_schema.model_json_schema(),
            output_schema=skill.output_schema.model_json_schema(),
            policy_flags=skill.policy_flags,
        )
        for skill in registry.list_skills()
    ]
```

### LLM prompt structure
```
SYSTEM: You are an execution planner for an agent system...

USER:
Task: {task_description}

Available skills:
{formatted_skill_catalog}

Create an execution plan as JSON:
{json_schema}
```

### Plan schema
```python
class PlannedStep(BaseModel):
    skill: str
    params: dict[str, Any]
    rationale: str
    estimated_tokens: int | None = None
    policy_flags: list[str] = []

class ExecutionPlan(BaseModel):
    plan_id: str
    task: str
    steps: list[PlannedStep]
    estimated_total_tokens: int
    confidence: float  # 0.0-1.0
    warnings: list[str] = []
```

### V1Planner class
```python
class V1Planner:
    """LLM-based planner that composes skill sequences.
    
    Pure function: no disk I/O. Returns in-memory Playbook.
    Implements Planner Protocol: plan(task) -> Playbook
    """
    def __init__(self, provider: LLMProvider, skill_registry: SkillRegistry):
        self.provider = provider
        self.skill_registry = skill_registry
    
    def plan(self, task: TaskSpec) -> Playbook:
        """Generate execution plan from task and skill catalog.
        
        Returns Playbook (not ExecutionPlan) to match Planner Protocol.
        The Playbook contains PlaybookSteps with skill_name and parameters.
        Orchestrator handles param chaining at runtime.
        """
        catalog = self._get_skill_catalog()
        prompt = self._build_prompt(task, catalog)
        response = self.provider.chat(prompt)  # Uses chat(), not complete()
        playbook = self._parse_and_build_playbook(response, task)
        return playbook
```

---

## Risks

| Risk | Mitigation |
|------|------------|
| LLM produces invalid skill names | Validate against registry, reject plan if invalid |
| LLM produces invalid param structure | Validate against skill input schema |
| Token estimation inaccurate | Mark as "estimated", track over time |
| LLM hallucinates non-existent capabilities | Strict skill catalog, no tool-use hallucination |
| Plan too long / expensive | Add budget constraints to prompt, enforce max steps |

---

## Open questions — RESOLVED

| # | Question | Resolution |
|---|----------|------------|
| 1 | Should we allow the LLM to skip steps? | **N/A** — The LLM composes any valid skill sequence; no "required" steps exist. Remove question. |
| 2 | How to handle param chaining? | **Dot-access syntax** — `{{step_N.field}}` with custom resolver (see below) |
| 3 | Confidence < threshold trigger warning? | **Yes** — Display warning in plan preview when `confidence < 0.5` |

### Param chaining implementation

Steps reference outputs from previous steps using `{{step_N.field}}` placeholders:

```python
import re
from typing import Any

def resolve_params(params: dict[str, Any], step_outputs: dict[int, Any]) -> dict[str, Any]:
    """Replace {{step_N.field}} placeholders with actual values from previous step outputs."""
    def resolve_value(value: Any) -> Any:
        if isinstance(value, str):
            # Match {{step_0.results}} or {{step_1.content.text}}
            pattern = r"\{\{step_(\d+)\.([\w.]+)\}\}"
            match = re.fullmatch(pattern, value.strip())
            if match:
                step_idx = int(match.group(1))
                field_path = match.group(2)
                return _get_nested(step_outputs[step_idx], field_path)
            # Handle embedded placeholders in strings
            def replacer(m: re.Match) -> str:
                step_idx = int(m.group(1))
                field_path = m.group(2)
                return str(_get_nested(step_outputs[step_idx], field_path))
            return re.sub(pattern, replacer, value)
        elif isinstance(value, dict):
            return {k: resolve_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [resolve_value(item) for item in value]
        return value
    
    return resolve_value(params)

def _get_nested(obj: Any, path: str) -> Any:
    """Get nested attribute/key by dot path: 'results.0.url' -> obj['results'][0]['url']"""
    for part in path.split("."):
        if isinstance(obj, dict):
            obj = obj[part]
        elif isinstance(obj, list) and part.isdigit():
            obj = obj[int(part)]
        else:
            obj = getattr(obj, part)
    return obj
```

### Confidence warning logic

The planner adds warnings to the plan when confidence is low:

```python
CONFIDENCE_WARNING_THRESHOLD = 0.5

def _add_confidence_warnings(plan: ExecutionPlan) -> None:
    """Add user-facing warnings based on confidence and plan characteristics."""
    if plan.confidence < CONFIDENCE_WARNING_THRESHOLD:
        plan.warnings.append(
            f"Low planner confidence ({plan.confidence:.0%}) — review plan carefully"
        )
    if len(plan.steps) > 10:
        plan.warnings.append(
            f"Long plan ({len(plan.steps)} steps) — higher risk of errors"
        )
```

AF-0098 (plan preview) displays these warnings prominently.

---

# Completion section (fill when done)

_To be filled upon completion_
