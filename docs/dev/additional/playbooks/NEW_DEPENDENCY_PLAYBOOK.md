# New Dependency Playbook (P1+) — ag_foundation
# Version number: v0.1

Use this playbook before adding a major dependency/framework (e.g., LangGraph, LlamaIndex, new DB).

## 1) Threshold check (avoid overhead)
Explain why now:
- What requirement cannot be met with current minimal approach?
- What is the expected benefit (measurable)?
- What complexity/lock-in does it introduce?

## 2) Interface mapping (mandatory)
- Which existing interface will the dependency implement?
  - Example: LangGraph implements `Orchestrator` backend
  - Example: LlamaIndex implements `Retriever`
- Ensure swapping back is feasible (at least in principle).

## 3) ADR (mandatory for P1+)
- Record decision + alternatives.

## 4) Adoption plan (sliced)
1) PR1: Add dependency + adapter implementation behind feature flag/config
2) PR2: Add tests and a small “canary” workflow or retriever
3) PR3: Expand usage or keep optional

## 5) Performance and failure modes
- Startup overhead
- Memory/cpu impact
- What happens if it fails? (fallback path)

## 6) Done criteria
- Dependency is optional unless explicitly enabled
- Contracts unchanged for callers
- Tests + trace evidence included
- Docs updated (ARCHITECTURE + relevant references)
