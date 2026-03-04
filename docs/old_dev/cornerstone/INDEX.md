# Cornerstone Index (ag_foundation)

This folder contains the **canonical, project-defining documents** for ag_foundation.
If anything conflicts with other docs, **these files win**.

## Reading order (start here)
1. **[PROJECT_PLAN.md](PROJECT_PLAN.md)** — what we're building, scope, and sprint roadmap
2. **[ARCHITECTURE.md](ARCHITECTURE.md)** — system concepts, module boundaries, RunTrace schema
3. **[CLI_REFERENCE.md](CLI_REFERENCE.md)** — command surface and UX contracts
4. **[REVIEW_GUIDE.md](REVIEW_GUIDE.md)** — how we review runs, outputs, and changes

## Principles captured here
- LLM-first end-user behavior; manual mode is dev/test only (LLMs disabled).
- Modular skill/plugin model plus a modular core runtime pipeline.
- Playbook-based orchestration to support different reasoning modes between agents.
- RAG and MLP are optional, interface-first modules (implement later).
- Truthful UX: all CLI labels derived from persisted RunTrace.

## Status
All cornerstone docs are **v0.1 complete** (authored in Sprint 00):
- PROJECT_PLAN.md: v0.1
- ARCHITECTURE.md: v0.1
- CLI_REFERENCE.md: v0.1
- REVIEW_GUIDE.md: v0.1
