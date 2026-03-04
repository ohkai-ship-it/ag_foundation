# Change Playbooks — Index (ag_foundation)

This folder contains **playbooks for larger or higher-risk changes** to keep the project consistent and reviewable.

## When to use
Use these playbooks for P1+ work, especially:
- changes to cornerstone contracts (TaskSpec, RunTrace, module boundaries)
- large changes spanning multiple PRs
- CLI contract changes
- trace schema changes / migrations
- introducing a major dependency (LangGraph, LlamaIndex, storage engine)

## Playbooks
1. **LARGE_CHANGE_PLAYBOOK.md** — default for multi-PR architecture changes
2. **TRACE_SCHEMA_CHANGE_PLAYBOOK.md** — how to evolve RunTrace safely
3. **CLI_CHANGE_PLAYBOOK.md** — how to change CLI commands/flags without drift
4. **NEW_DEPENDENCY_PLAYBOOK.md** — how to adopt frameworks without overhead

## Output expectations
Every playbook ends with:
- a list of AF items (epic + slices)
- an ADR (if P1+)
- an evidence plan (tests + RunTrace IDs + review entries)
