# AF-0128 — First LangChain Tool Batch
# Version number: v0.1
# Created: 2026-03-23
# Status: READY
# Priority: P1
# Area: Skills / Capability Expansion

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
>   `pytest tests/test_langchain_tools.py tests/test_skill_framework.py -W error`
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
- **ID:** AF-0128
- **Type:** Skills / Capability Expansion
- **Status:** READY
- **Priority:** P1
- **Area:** Skills / Capability Expansion
- **Owner:** Jacob
- **Target sprint:** Sprint 17 — skill_catalog_expansion

---

## Problem

With `LangChainSkillAdapter` (AF-0127) in place, the infrastructure to add external
tools exists, but no tools have been registered. The skill catalog remains:
`web_search`, `fetch_web_content`, `load_documents`, `synthesize_research`, `emit_result`.

Every task outside research and summarization still returns `PARTIALLY_FEASIBLE`.
The planner's intelligence outpaces the skills it can route to.

The highest-value, lowest-risk tools to enable first are:

1. **File operations** — read, write, list directory, delete local files.
   No credentials. No sandboxing concern. Unlocks personal productivity tasks
   (the agent can now find _and_ manipulate documents).

2. **Wikipedia** — factual lookup with structured output. No API key. No network
   auth. Clean single-call pattern. Expands the research toolkit immediately.

The combination of file ops + Wikipedia is sufficient to enable a new class of
end-user tasks: "research X on Wikipedia and write a summary to a file",
"list files in a directory and summarize their content", "read this document
and emit a report".

---

## Goal

Register and validate the following 5 LangChain tools through `LangChainSkillAdapter`:

| Skill name (ag internal) | LangChain tool class | Package |
|---|---|---|
| `write_file` | `WriteFileTool` | `langchain-community` |
| `read_file` | `ReadFileTool` | `langchain-community` |
| `list_directory` | `ListDirectoryTool` | `langchain-community` |
| `delete_file` | `DeleteFileTool` | `langchain-community` |
| `wikipedia` | `WikipediaQueryRun` | `langchain-community`, `wikipedia` |

Each tool must:
- Be loadable via `load_langchain_skills(["write_file", ...])`
- Be recognized by the planner skill catalog (registered in entry points or dynamic registry)
- Pass through V2Executor schema validation (output schema: `{"output": str, "tool_name": str}`)
- Appear in `ag skills` listing

---

## Non-goals

- `ShellTool` / `PythonREPLTool` (sandboxing prerequisite not met)
- OAuth tools (Gmail, Google Calendar) — credentials model not in place
- `PandasDataFrameTool`, `SQLDatabaseToolkit` — Phase 3 / Gate D territory
- `ArxivQueryRun`, `PubMedQueryRun` — no user story yet, deferred
- Building new playbooks that use these tools (separate AF)

---

## Design

### 1. Tool registration

The 5 tools are registered via the YAML loader / entry point mechanism from AF-0127.
Each tool name maps to its LangChain class:

```python
LANGCHAIN_TOOL_MAP: dict[str, type[BaseTool]] = {
    "write_file":      WriteFileTool,
    "read_file":       ReadFileTool,
    "list_directory":  ListDirectoryTool,
    "delete_file":     DeleteFileTool,
    "wikipedia":       WikipediaQueryRun,
}
```

### 2. Workspace isolation enforcement for file tools

`WriteFileTool`, `ReadFileTool`, `DeleteFileTool`, and `ListDirectoryTool` operate on
the filesystem. The workspace isolation invariant requires that file tools be scoped
to the active workspace directory.

Enforcement strategy: the YAML loader (or adapter constructor) sets the `root_dir`
parameter on file tools to the active workspace path. Calls that resolve outside the
workspace raise `SkillExecutionError`.

```python
# In loader, when constructing file tools:
if hasattr(tool_instance, "root_dir"):
    tool_instance.root_dir = str(context.workspace_path)
```

This preserves the workspace isolation invariant with zero changes to core pipeline code.

### 3. Wikipedia tool configuration

`WikipediaQueryRun` is configured with:
- `top_k_results: 3` (default)
- `doc_content_chars_max: 4000` (prevent oversized outputs)
- Language: inherits from user query (Wikipedia API handles this automatically)

### 4. Output schema

All 5 tools produce the standard adapter output:
```json
{
  "output": "<string result from tool.run()>",
  "tool_name": "<skill name>"
}
```

V2Executor's LLM repair handles any downstream schema coercion when a subsequent
skill or `emit_result` expects a richer structure.

### 5. Skill catalog documentation

`ag skills` must list all 5 new skills with their descriptions (auto-derived from
`BaseTool.description`). No manual description override needed if the LangChain
descriptions are clear enough. If truncation or clarity is needed, the loader
supports an optional `description_override` in the YAML config.

---

## Files to touch

| File | Change |
|---|---|
| `src/ag/skills/langchain_loader.py` | Add `LANGCHAIN_TOOL_MAP` with 5 tools; workspace scoping for file tools |
| `pyproject.toml` | Add `langchain-community`, `wikipedia` as optional extras; update install extras |
| `tests/test_langchain_tools.py` | New file — integration tests for each of the 5 tools via adapter |
| `docs/dev/foundation/ARCHITECTURE.md` | Document new skill entries in skill catalog section |

---

## Acceptance criteria

- [ ] `write_file` skill writes a file within the active workspace directory
- [ ] `read_file` skill reads a file within the active workspace directory
- [ ] `list_directory` skill lists directory contents within the active workspace
- [ ] `delete_file` skill deletes a file within the active workspace directory
- [ ] All file tools reject paths outside the active workspace directory (workspace isolation)
- [ ] `wikipedia` skill returns a factual summary string for a given query
- [ ] All 5 skills appear in `ag skills` listing
- [ ] `ag run -y "Look up Little Tokyo on Wikipedia and write a summary to output.md"` produces a result
- [ ] All tests pass without network calls for file tools (mocked); Wikipedia test is skippable (`@pytest.mark.integration`)
- [ ] Full CI gate passes

---

## Test strategy

- `tests/test_langchain_tools.py`:
  - `test_write_file_creates_file_in_workspace` — adapter writes a file; verify file exists in tmp workspace dir
  - `test_read_file_returns_content` — write a known file, adapter reads it; verify content matches
  - `test_list_directory_returns_entries` — create tmp dir with 2 files; adapter lists them
  - `test_delete_file_removes_file` — create file, adapter deletes it; verify gone
  - `test_file_tools_reject_path_outside_workspace` — path traversal attempt `../../secret.txt` → `SkillExecutionError`
  - `test_wikipedia_adapter_wraps_wikipedia_query_run` — mock `WikipediaQueryRun.run()`, assert adapter returns `output` key
  - `test_wikipedia_integration_with_known_query` — marked `@pytest.mark.integration`, skipped in CI; real Wikipedia call

- `tests/test_skill_framework.py` (existing):
  - Verify that all 5 new skill names appear in the registry after `load_langchain_skills()` is called

---

## Dependencies

- **AF-0127** (LangChainSkillAdapter infrastructure) must be complete first
- `langchain-community` >= 0.2 (PyPI)
- `wikipedia` >= 1.4.0 (PyPI, for `WikipediaQueryRun`)

---
