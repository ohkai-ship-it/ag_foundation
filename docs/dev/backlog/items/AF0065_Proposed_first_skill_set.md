# BACKLOG ITEM — AF0065 — first_skill_set
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

> **File naming (required):** `AF####_<Status>_<three_word_description>.md`
> Status values: `Proposed | Ready | In progress | Blocked | Done | Dropped`

---

## Metadata
- **ID:** AF0065
- **Type:** Feature
- **Status:** Proposed
- **Priority:** P0
- **Area:** Skills
- **Owner:** Kai
- **Target sprint:** Sprint07
- **Depends on:** AF0060 (skill definition framework), AF0058 (workspace restructure)

---

## Problem
The current codebase has no production-ready skills:

1. **strategic_brief is deprecated** — It doesn't use LLM, just lists files. Not a model for future skills.
2. **All other skills are stubs** — 11 of 12 skills return hardcoded values
3. **No playbook composition** — No example of skills chaining together
4. **No LLM integration pattern** — No reference implementation for provider injection

We need at least one real skill to validate the framework from AF0060.

---

## Goal
Implement the first working skill set from scratch, using the skill definition framework:

1. **First skill** — A simple, LLM-powered skill (e.g., `summarize`, `code_review`, or similar)
2. **Second skill** — Another skill to demonstrate variety and composability
3. **Default playbook** — A playbook that chains the skills together
4. **Reference implementation** — Pattern for future skill development

**Important:** This work starts fresh. The existing `strategic_brief` skill is NOT a template or dependency.

---

## Non-goals
- Migrating or reusing `strategic_brief` code
- Complex multi-agent orchestration
- External tool integration (web search, file writing, etc.)
- Streaming responses

---

## Acceptance criteria (Definition of Done)
- [ ] At least 2 working skills implemented using AF0060 framework
- [ ] Skills call LLM via provider abstraction
- [ ] Skills produce proper evidence/citations
- [ ] Skills emit artifacts to workspace
- [ ] Default playbook chains skills together
- [ ] Skills read inputs from `workspace/inputs/` (per AF0058)
- [ ] All skills registered in skill registry
- [ ] Unit tests for each skill (mocked provider)
- [ ] Integration test with real provider (manual mode)
- [ ] `ruff check src tests` passes
- [ ] `pytest -W error` passes
- [ ] Coverage threshold maintained

---

## Candidate skills (choose 2)

| Skill | Description | Complexity |
|-------|-------------|------------|
| `summarize` | Summarize a document or collection of files | Low |
| `code_review` | Review code for issues, suggest improvements | Medium |
| `explain_code` | Explain what a code file does | Low |
| `generate_tests` | Generate test cases for code | Medium |
| `extract_requirements` | Extract requirements from documents | Low |

Recommended starting pair: `summarize` + `explain_code` (both low complexity, useful, testable)

---

## Implementation notes

### Skill structure (conceptual)
```python
class SummarizeSkill(BaseSkill):
    """Summarize documents from workspace inputs."""
    
    input_schema = SummarizeInput  # Pydantic model
    output_schema = SummarizeOutput  # Pydantic model
    
    def execute(self, input: SummarizeInput, context: SkillContext) -> SummarizeOutput:
        # Read files from workspace.inputs_path
        # Call LLM via context.provider
        # Return structured output with citations
        ...
```

### Playbook composition
```python
default_playbook = Playbook(
    name="default",
    steps=[
        PlaybookStep(skill="summarize", inputs={...}),
        PlaybookStep(skill="explain_code", inputs={...}),
    ]
)
```

---

## Risks

| Risk | Mitigation |
|------|------------|
| AF0060 design changes | Wait for AF0060 to stabilize before implementing |
| Provider abstraction gaps | Validate provider interface in AF0060 |
| Scope creep (too many skills) | Strict limit: 2 skills only |

---

## Related
- AF0060 (Skill definition framework) — **prerequisite**
- AF0058 (Workspace folder restructure) — **prerequisite**
- AF0066 (E2E integration test) — validates this work

---

## Documentation impact
- Update ARCHITECTURE.md with skill examples
- Add skill development guide (optional, if time permits)

---

# Completion section (fill when done)

Pending completion.
