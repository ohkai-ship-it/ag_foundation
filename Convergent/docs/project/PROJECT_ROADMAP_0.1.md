# PROJECT ROADMAP — ag_foundation
#### Description: Strategic roadmap for ag_foundation. Defines phases, milestones, autonomy gates, and the path from foundation runtime to full autonomous agent.
#### Convergent: v1.3.2
#### File version: 0.1
#### governs: ag_foundation
#### Updated: 2026-04-20

---

> **FOUNDATION GOVERNANCE**
> This file is governed by: `foundation/SPRINT_PLAYBOOK.md`
> This is a strategic planning document. Update at phase boundaries and major scope shifts.

---

## 1) Executive Summary

ag_foundation builds a modular agent network core that can plan, execute, verify, and learn from runs. IoT integration, web/app UI, and other sensors/data sources are later integrations; the foundation makes those easy to attach.

The project has completed 19 sprints (S00–S18) across four development phases. The intelligent pipeline is operational (V3Planner, V2Verifier, V2Executor), guided autonomy is hardened, and Gates A–C are passed. The current bottleneck is skill catalog breadth — the pipeline intelligence exceeds the capabilities it can route to.

**This roadmap covers ag_foundation's runtime development.** Governance system development is tracked separately in Convergent.

---

## 2) Vision

A modular agent runtime that can autonomously plan, execute, verify, and improve task workflows — starting from research and document generation, expanding to file operations, code execution, and real-world integrations.

**Design principle:** Humans define WHAT, agents decide HOW.

```
RIGID                                                    AUTONOMOUS
(human decides everything)                    (agent decides everything)
    |                                                         |
    v                                                         v
+--------+  +--------+  +--------+  +--------+  +--------+
| Script |  |Playbook|  | Guided |  | Goals  |  |  Full  |
|        |  |        |  | Agent  |  |  Only  |  | Agent  |
+--------+  +--------+  +--------+  +--------+  +--------+
     ✅          ✅          ✅          ✅          ⏳
```

---

## 3) Current State

The system reached Goals-Only autonomy level in Sprint 15 (2026-03-22). Sprints 16–18 focused on governance migration and CLI polish.

| Component | Status | Key versions |
|-----------|--------|-------------|
| Core Runtime | Stable | V1Orchestrator, V1Recorder |
| Planner | Stable | V3Planner (feasibility: FULLY/MOSTLY/PARTIALLY/NOT_FEASIBLE) |
| Verifier | Stable | V2Verifier (LLM semantic checks: relevance, completeness, consistency) |
| Executor | Stable | V2Executor (output schema validation, LLM repair on failure) |
| Skill Framework | Stable | Typed ABC, Pydantic I/O, plugin entry points (AF-0077) |
| Production Skills | 5 skills | `web_search`, `fetch_web_content`, `load_documents`, `synthesize_research`, `emit_result` |
| Playbooks | 2 active | `summarize_v0`, `research_v0` |
| CLI | Complete | Typer-based, truthful UX, inline plan preview, autonomy display |
| Storage | Stable | SQLite index + filesystem artifacts, run-centered layout |
| CI | Enforced | ruff + pytest -W error + coverage ≥70% |
| Governance | v1.3.2 | Convergent server/client model |

**Known gaps:**
- **Skill catalog breadth** — reachable task space is essentially research + summarize + emit. The pipeline is more capable than the skills it routes to.
- **Policy engine** — only basic confirmation hooks exist. No budgets, risk scoring, or scope boundaries.
- **RAG / retrieval** — no workspace-bound indexing, evidence bundles, or citation linking.
- **Internal API** — CLI-only interface. No programmatic access layer.
- **Credentials / secrets** — no workspace-scoped secrets management for external service skills.

---

## 4) Architecture

### 4.1 High-Level Model

```
┌─────────────────────────────────────────────────────┐
│                    CLI Adapter                       │
│              (Typer, plan preview, UX)               │
├─────────────────────────────────────────────────────┤
│                   Core Runtime                       │
│  V3Planner → V1Orchestrator → V2Executor            │
│                    ↕                                 │
│              V2Verifier ← V1Recorder                 │
├─────────────────────────────────────────────────────┤
│               Skills & Playbooks                     │
│  Native skills · LangChain adapters · YAML playbooks │
├─────────────────────────────────────────────────────┤
│                    Storage                           │
│        SQLite index · Filesystem artifacts           │
│         Run-centered layout: runs/<id>/              │
└─────────────────────────────────────────────────────┘
```

See `ARCHITECTURE.md` for full detail.

### 4.2 Key Boundaries

| Boundary | Enforcement |
|----------|-------------|
| **Workspace isolation** | Skills operate within active workspace only. `--workspace` rejects non-existent names. |
| **Truthful UX** | CLI shows only trace-derived data. No fabricated labels or summaries. |
| **Bounded autonomy** | Humans define goals; agent composes plans. Confirmation hooks for high-impact actions. |
| **Layer separation** | CLI ↔ Core ↔ Skills ↔ Storage boundaries enforced via Protocol interfaces. |
| **Trace contract** | Every run produces a RunTrace. All pipeline stages record evidence. |

---

## 5) Phased Roadmap

### Phase 0 — Foundation Build ✅
**Theme:** Core runtime, trace contract, truthful CLI, CI enforcement.
Sprints S00–S05. Established the modular runtime, delegation pattern, schema verifier, and process discipline.

### Phase 1 — Skill & Playbook Foundation ✅
**Theme:** Skill architecture, first LLM-powered skills, playbook composition.
Sprints S06–S08. Delivered typed skill framework, production skills (web_search, summarize), and working playbooks.

### Phase 2 — Autonomy Readiness Hardening ✅
**Theme:** Reliability hardening, Gate A + B, guided autonomy, storage boundaries.
Sprints S09–S12. Achieved Gate A (Reliability) and Gate B (Guided Autonomy). Enabled plan preview, approval workflow, and strict content validation.

### Phase 2b — Intelligent Pipeline ✅
**Theme:** LLM-powered planning, semantic verification, output repair. Gate C.
Sprints S13–S15. Delivered V3Planner (feasibility), V2Verifier (semantic checks), V2Executor (LLM repair). Gate C (Goals-Only) passed 2026-03-22.

### Phase 2c — Governance & Polish ✅
**Theme:** Governance extraction, migration to Convergent, CLI UX polish.
Sprints S16–S18. Migrated governance to Convergent v1.3.2 server/client model. Completed CLI surface (playbooks show, runs filter, doctor diagnostics).

### Phase 3 — Capability Expansion (Active)
**Theme:** Broaden what the agent can DO before deepening how it reasons.

The pipeline intelligence (V3Planner, V2Verifier, V2Executor) is ahead of the skill catalog. Current task reachability: research + summarize + emit. This phase closes that gap.

**Deliverables:**

Skill catalog expansion:
- [ ] LangChain skill adapter infrastructure (AF-0127)
- [ ] First LangChain tool batch: file ops + Wikipedia (AF-0128)
- [ ] Text splitting for large documents (prerequisite for RAG)
- [ ] Rich document loaders (PDF, CSV, DOCX via LangChain community)

Candidate skill domains (unordered, for future sprint planning):
- **File operations** — read/write/move/delete local files. Highest-value, lowest-risk entry point.
- **Code execution** — run scripts, capture output. High value, requires sandboxing.
- **Structured data extraction** — parse tables, CSV, JSON into normalized form.
- **Diff / compare** — compare documents or code files, surface meaningful deltas.
- **Academic search** — ArXiv, PubMed lookups for research workflows.

Candidate playbook patterns:
- **Decision brief** — research topic, extract pros/cons, emit recommendation.
- **Weekly digest** — aggregate sources, deduplicate, emit summary report.
- **Code review assist** — load diff, analyze for issues, emit findings.
- **Meeting prep** — research context for topic + attendees, emit briefing.

Retrieval interface (RAG):
- [ ] Retriever interface definition
- [ ] Workspace-bound indexing model (Chroma or FAISS, workspace-scoped)
- [ ] Evidence bundle capture in trace
- [ ] Citation linking in trace contract

Internal API readiness:
- [ ] Internal adapter interface definition
- [ ] CLI → service layer mapping

See [LANGCHAIN_ANALYSIS_0.1.md](../additional/LANGCHAIN_ANALYSIS_0.1.md) for detailed skill comparison and component viability analysis.

### Phase 4 — Autonomy Evolution (Future)
**Theme:** Gate D prerequisites — policy engine, adaptive replanning, full agent.

Gate D (Full Agent) requires:
1. **Mature policy engine** — budgets, risk scoring, scope boundaries. Currently only basic confirmation hooks.
2. **Adaptive replanning** — genuine mid-run strategy pivot on path failure. Bounded retry exists; true replanning does not.
3. **Skill catalog breadth** — a full agent with narrow skills is still heavily constrained.
4. **RAG / retrieval interface** — workspace-bound indexing, evidence bundles, citation linking.
5. **Internal API readiness** — CLI → service layer so the agent is callable programmatically.

### Phase 5 — Integration (Future)
**Theme:** Real-world I/O — IoT, web/app adapters, multi-interface orchestration.

Prerequisite: Gate D passed, broad skill catalog, internal API operational.

---

## 6) Success Criteria

Progression is gated by autonomy phase gates. No sprint may claim autonomy progression while a P0 gate condition is unmet.

| Gate | Purpose | Required Conditions | Status |
|------|---------|---------------------|--------|
| Gate A: Reliability | Foundation → autonomy-ready execution | Warning-clean tests, isolation stability, failure-path coverage, deterministic cleanup | ✅ Passed (S09) |
| Gate B: Guided Autonomy | Enable guided planning behavior | Policy enforcement, verifier/failure rigor, trace-derived labels for all new behavior | ✅ Passed (S10) |
| Gate C: Goals-Only | Prepare for dynamic composition | (1) Mature policy engine, (2) replanning on step failure, (3) feasibility judgment, (4) strategy justification in trace, (5) controlled extensibility | ✅ Passed (S15) |
| Gate D: Full Agent | Autonomous end-to-end execution | Mature policy engine (budgets, risk scoring), adaptive mid-run replanning, broad skill catalog, RAG/retrieval interface, internal API layer | ⏳ Not started |

---

## 7) Open Decisions

| # | Question | Impact | Status |
|---|----------|--------|--------|
| 1 | Should skills call other skills (composition), or is that the playbook layer's job? | Skill architecture, complexity boundary | OPEN |
| 2 | How to handle skills requiring credentials (email, calendar, APIs)? Secrets management does not exist. | Blocks credential-requiring skills (Gmail, Calendar, DBs) | OPEN |
| 3 | RAG indexing model — workspace-bound Chroma/FAISS, or external service? | Storage architecture, deployment model | OPEN |
| 4 | Is a skill interface version discipline needed (V2 skills coexisting with V1)? | Migration complexity, backward compatibility | OPEN |
| 5 | Code execution sandboxing — how to scope ShellTool/PythonREPLTool safely? | Blocks high-value code execution skills | OPEN |

---

## 8) Immediate Next Steps

1. **Sprint XX (skill_catalog_expansion)** — AF-0127 (LangChain adapter) + AF-0128 (first tool batch). Proposed, ready for scheduling.
2. **AF-0149** — Add LICENSE file (P1, ready).
3. **AF-0150** — CLI `run()` complexity reduction (P2, ready).
4. **AF-0146** — `ag artifacts list --category` filter (P2, proposed).
5. **AF-0148** — Workspace isolation design (P2, proposed).

Prioritization principle: **broaden what the agent can DO** before deepening how it reasons about doing it.

---

## References

- Architecture detail: `ARCHITECTURE.md`
- Project control: `docs/project/PROJECT_CONTROL_0.1.md`
- LangChain analysis: `docs/additional/LANGCHAIN_ANALYSIS_0.1.md`
- Sprint registry: `docs/INDEX_SPRINTS.md`
- Backlog: `docs/INDEX_BACKLOG.md`
