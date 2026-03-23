# AF-0127 — LangChain Skill Adapter
# Version number: v0.1
# Created: 2026-03-23
# Status: READY
# Priority: P1
# Area: Skills / Plugin Architecture

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI workflow (two-phase — see below)
> - 1 PR = 1 sprint
> - INDEX update rule (status ↔ filename integrity)
>
> **CI workflow (CRITICAL):**
> - **During AF development:** run targeted tests only
>   `pytest tests/test_skill_framework.py tests/test_contracts.py -W error`
> - **Before commit (full gate):** run the complete CI gate
>   1. `ruff check src tests`
>   2. `ruff format --check src tests`
>   3. `pytest -W error`
>   4. `pytest --cov=src/ag --cov-report=term-missing`
>
> Do NOT run the full suite on every save. Targeted tests keep feedback fast.
> The full gate runs once, right before `git commit`.

> **File naming (required):** `AF####_<STATUS>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF-0127
- **Type:** Skills / Plugin Architecture
- **Status:** READY
- **Priority:** P1
- **Area:** Skills / Plugin Architecture
- **Owner:** Jacob
- **Target sprint:** Sprint 16

---

## Problem

The agent's reachable task space is bounded by its skill catalog:
`web_search`, `fetch_web_content`, `load_documents`, `synthesize_research`, `emit_result`.

Everything outside research + summarize + emit reports `PARTIALLY_FEASIBLE` or
falls back to `research_v0`. There is no mechanism to add external tools without
writing a full skill implementation from scratch — a Python module, entry point
registration, YAML schema declaration, and test suite.

LangChain (`langchain-community`) provides a mature catalog of ~80+ ready-made tools
covering file operations, databases, APIs, Wikipedia, academic search, email, and more.
Each tool implements a standard `BaseTool` interface: `name`, `description`,
`args_schema` (Pydantic model), and `run(input)`.

Without a bridge layer, every LangChain tool requires its own custom skill wrapper.
That is O(n) implementation effort. An adapter that reads the `BaseTool` interface
automatically requires O(1) infrastructure effort and then O(0) per tool.

---

## Goal

Deliver a generic `LangChainSkillAdapter` class that bridges any `langchain_core.tools.BaseTool`
into the ag skill interface, plus a YAML-driven loader so new tools are enabled
through config alone.

- Zero per-tool Python code after the adapter infrastructure exists
- LangChain tool metadata (`name`, `description`, `args_schema`) drives skill registration automatically
- Output schema is inferred from `args_schema` where available; `V2Executor` LLM repair handles mismatches
- A `FakeTool` stub enables deterministic testing without installing LangChain community packages in CI

---

## Non-goals

- Bundling specific LangChain tools (that is AF-0128's scope)
- Secrets / credential management for tools that require API keys (deferred)
- `ShellTool` / `PythonREPLTool` adoption (sandboxing not yet in place)
- Tool composition or chaining within the adapter

---

## Design

### 1. `LangChainSkillAdapter` class

Location: `src/ag/skills/langchain_adapter.py`

```python
from langchain_core.tools import BaseTool
from ag.skills.base import BaseSkill, SkillContext

class LangChainSkillAdapter(BaseSkill):
    """Wraps any LangChain BaseTool as an ag skill.

    The skill name, description, and input schema are derived automatically
    from the wrapped tool's metadata. Output is normalized to {"output": str}
    so V2Executor's LLM repair can coerce it to the declared output_schema.
    """

    def __init__(self, tool: BaseTool) -> None:
        self._tool = tool

    @property
    def name(self) -> str:
        return self._tool.name

    @property
    def description(self) -> str:
        return self._tool.description

    @property
    def input_schema(self) -> dict:
        if self._tool.args_schema is not None:
            return self._tool.args_schema.model_json_schema()
        return {"type": "object", "properties": {"input": {"type": "string"}}}

    @property
    def output_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "output": {"type": "string"},
                "tool_name": {"type": "string"},
            },
            "required": ["output", "tool_name"],
        }

    def execute(self, context: SkillContext) -> dict:
        params = context.params
        tool_input = params.get("input", params)
        result = self._tool.run(tool_input)
        return {"output": str(result), "tool_name": self._tool.name}
```

### 2. YAML-driven loader

Location: `src/ag/skills/langchain_loader.py`

The loader reads a list of tool names from workspace or global config and returns a
registry of `LangChainSkillAdapter` instances.

```yaml
# In workspace config or global ag config:
langchain_tools:
  - wikipedia
  - write_file
  - read_file
  - list_directory
  - delete_file
```

```python
def load_langchain_skills(tool_names: list[str]) -> dict[str, LangChainSkillAdapter]:
    """Import and wrap named LangChain tools. Returns skill_name → adapter."""
    ...
```

Import is lazy: only tools listed in config are imported. Tools not installed raise
a clear `SkillConfigError` with the missing package name.

### 3. Skill registry integration

`LangChainSkillAdapter` instances are registered through the existing skill registry
(entry points or dynamic registration). The adapter's `name` property drives the
registry key — identical to how named skills work today.

### 4. `FakeTool` test stub

Location: `tests/` (test utility, not production code)

```python
class FakeTool(BaseTool):
    name: str = "fake_tool"
    description: str = "A deterministic test tool."
    args_schema: type[BaseModel] = FakeToolInput

    def _run(self, query: str) -> str:
        return f"fake result for: {query}"
```

Used in all adapter tests. No LangChain community package required at test time.

### 5. Error handling

- Tool raises exception → `SkillExecutionError` with the original exception chained
- Tool is not installed → `SkillConfigError` at load time (not at execution time)
- Output is not a string → `str(result)` coercion always applied

---

## Files to touch

| File | Change |
|---|---|
| `src/ag/skills/langchain_adapter.py` | New file — `LangChainSkillAdapter` class |
| `src/ag/skills/langchain_loader.py` | New file — YAML-driven loader |
| `src/ag/skills/__init__.py` | Export `LangChainSkillAdapter`, `load_langchain_skills` |
| `pyproject.toml` | Add `langchain-core` as dependency; `langchain-community` as optional extra |
| `tests/test_langchain_adapter.py` | New file — adapter tests using `FakeTool` |

---

## Acceptance criteria

- [ ] `LangChainSkillAdapter` wraps any `BaseTool` and produces a valid skill
- [ ] `adapter.name`, `adapter.description`, `adapter.input_schema` are derived from the wrapped tool
- [ ] `adapter.execute(context)` calls `tool.run()` and returns `{"output": str, "tool_name": str}`
- [ ] `load_langchain_skills(["wikipedia"])` returns a `LangChainSkillAdapter` for `WikipediaQueryRun`
- [ ] Tool not installed raises `SkillConfigError` at load time (not execution time)
- [ ] Tool execution exception is wrapped in `SkillExecutionError`
- [ ] `FakeTool` stub works without installing `langchain-community`
- [ ] All tests pass without LLM or network calls
- [ ] Full CI gate passes

---

## Test strategy

- `tests/test_langchain_adapter.py`:
  - `test_adapter_name_description_from_tool` — assert `.name` and `.description` match `FakeTool`
  - `test_adapter_input_schema_from_args_schema` — assert Pydantic model is converted to JSON schema
  - `test_adapter_input_schema_fallback_when_no_args_schema` — tool without `args_schema` gets `{"input": string}`
  - `test_adapter_execute_calls_tool_run` — mock `FakeTool._run`, assert it is called with correct input
  - `test_adapter_execute_returns_output_and_tool_name` — assert output dict shape
  - `test_adapter_execute_wraps_tool_exception_in_skill_error` — tool raises → `SkillExecutionError`
  - `test_loader_returns_adapter_for_known_tool` — `load_langchain_skills(["fake"])` returns adapter
  - `test_loader_raises_config_error_for_unknown_tool` — unknown tool name → `SkillConfigError`

---

## Dependencies

- `langchain-core` (new, lightweight — only base classes, no community tools)
- AF-0128 (first tool batch) depends on this AF being complete

---
