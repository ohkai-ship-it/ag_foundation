# SPRINT DESCRIPTION — Sprint07 — summarize_playbook
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
> `/docs/dev/foundation/SPRINT_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI discipline (ruff + pytest -W error + coverage)
> - 1 PR = 1 primary AF
> - INDEX update rule (status ↔ filename integrity)

> **Folder naming (required):** `/docs/dev/sprints/documentation/Sprint07_summarize_playbook/`
> **Files (required):**
> - `S07_DESCRIPTION.md` (this file; includes plan + report)
> - `S07_REVIEW_01.md` (created by Jeff+Kai; executed by Jacob)
> - `S07_PR_01.md` (PR checklist for sprint finalization)

---

## 1) Metadata
- **Sprint:** Sprint07
- **Name:** summarize_playbook
- **Dates:** 2026-03-08 → TBD
- **Owner (PM):** Kai
- **Tech lead:** Jeff
- **Implementer:** Jacob
- **State:** In Progress

---

## 2) Sprint goal
Implement the first complete skill-based playbook (`summarize_v0`) with three skills:
load_documents, summarize_docs, and emit_result.

Validate the skill framework through a real-world end-to-end use case.

---

## 3) Scope (what we intend to ship)

### Must-have (P0)
- AF0065 — First skill set (summarize_v0) — Three skills implementing document summarization (Owner: Jacob)

### Should-have (P1)
- AF0068 — Skills/playbooks folder restructure — `src/ag/playbooks/` directory (Owner: Jacob)
- AF0066 — E2E integration test — Generic/configurable test for summarize_v0 (Owner: Jacob)
- AF0062 — Trace LLM model tracking — Record model/provider in RunTrace (Owner: Jacob)

### Nice-to-have (P2)
- AF0067 — Skill code documentation — Docstrings and inline docs for skill modules (Owner: Jacob)

---

## 4) Sprint start checklist (ritual)
### Jeff + Kai
- [x] Create AFs (Status = Ready)
- [x] Create this sprint description file
- [x] Define sprint ID + sprint name

### Jacob
- [x] Read sprint description
- [ ] Check AFs in `/docs/dev/backlog/items/`
- [ ] Ask clarifying questions in chat (no writing required)
- [x] Create branch
- [x] Create sprint folder
- [ ] Update INDEX files (ritual at sprint start):  
  - `/docs/dev/backlog/INDEX_BACKLOG.md`  
  - `/docs/dev/bugs/INDEX_BUGS.md`  
  - `/docs/dev/decisions/INDEX_DECISIONS.md`  
  - `/docs/dev/sprints/INDEX_SPRINTS.md`
- [ ] Confirm with Kai before starting implementation

> **INDEX update rule (strict):**  
> 1) Update when any AF/BUG/ADR/SPRINT status changes  
> 2) Also update as a ritual at sprint start

---

## 5) Technical notes

### AF-0065: summarize_v0 playbook structure
Three skills in sequence:
1. **load_documents** — Glob patterns → list[Document]
2. **summarize_docs** — Documents → LLM summary  
3. **emit_result** — Summary → file output

Runtime pipeline: Normalizer → Planner → Orchestrator → Executor → Verifier → Recorder

See AF0065 for complete specification with flow diagrams.

### AF-0068: Folder restructure
- Create `src/ag/playbooks/` directory
- One file per playbook (e.g., `summarize_v0.py`)
- Keep `core/playbooks.py` for registry

### AF-0062: Model tracking (Option B+C)
- Add `llm_model` and `llm_provider` fields to `RunTrace`
- Resolver logic: explicit → env → provider-default
- Store resolution source for debugging

---

## 6) Exit criteria
- [ ] `ag run --playbook summarize_v0` works with real LLM
- [ ] All three skills registered and documented
- [ ] E2E test passing in CI
- [ ] Model/provider recorded in trace
- [ ] 95%+ coverage maintained
- [ ] All Sprint 07 AFs → DONE

---

## 7) Sprint report (filled at close)
_To be completed at sprint end_

### Velocity
- Planned story points: TBD
- Completed story points: TBD

### What went well
- TBD

### What could improve
- TBD

### Follow-ups identified
- TBD
