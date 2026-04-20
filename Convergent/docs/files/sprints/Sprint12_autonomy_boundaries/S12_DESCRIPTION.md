# SPRINT DESCRIPTION — Sprint12 — autonomy_boundaries
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
> - 1 PR = 1 sprint
> - INDEX update rule (status ↔ filename integrity)

> **Folder naming (required):** `/docs/dev/sprints/documentation/Sprint##_three_word_description/`
> **Files (required):**
> - `S##_DESCRIPTION.md` (this file; includes plan + report)
> - `S##_REVIEW_01.md` (created by Jeff+Kai; executed by Jacob)
> - `S##_PR_01.md` (PR checklist for sprint finalization)

---

## 1) Metadata
- **Sprint:** Sprint12
- **Name:** autonomy_boundaries
- **Dates:** 2026-03-21 → 2026-03-21
- **Owner (PM):** Kai
- **Tech lead:** Jeff
- **Implementer:** Jacob
- **State:** Closed

---

## 2) Sprint goal
Stabilize guided autonomy output quality and storage boundaries by unifying summarization, hardening content emission, and standardizing run-centered artifact/plan layout.

---

## 3) Scope (what we intend to ship)

### Must-have (P0)
- AF0108 — Unify summarization skill (Owner: Jacob)
- AF0109 — emit_result strict content validation (Owner: Jacob)
- AF0110 — Run layout and plan artifacts refactor (Owner: Jacob)

### Should-have (P1)
- AF0107 — load_documents MD inputs reliability (Owner: Jacob)

### Nice-to-have (P2)
- AF0105 — CLI defaults verification audit (Owner: TBD)
- AF0106 — V1Planner file pattern defaults (Owner: TBD)
- AF0096 — Test workspace cleanup pollution (Owner: TBD)
- AF0111 — --workspace flag must never create (Owner: Jacob)

Excluded explicitly for this sprint:
- AF0103 — LLM Planner V2 (skills+playbooks)
- AF0104 — LLM Planner V3 (feasibility)

---

## 4) Sprint start checklist (ritual)
### Jeff + Kai
- [x] Create AFs (Status = Ready)
- [x] Create this sprint description file
- [x] Define sprint ID + sprint name

### Jacob
- [x] Read sprint description
- [x] Check AFs in `/docs/dev/backlog/items/`
- [x] Ask clarifying questions in chat (no writing required)
- [x] Create branch (`feat/sprint12-autonomy-boundaries`)
- [x] Create sprint folder
- [x] Update INDEX files (ritual at sprint start):
  - `/docs/dev/backlog/INDEX_BACKLOG.md` — 4 AFs promoted PROPOSED → READY
  - `/docs/dev/bugs/INDEX_BUGS.md` — no changes needed
  - `/docs/dev/decisions/INDEX_DECISIONS.md` — no changes needed
  - `/docs/dev/sprints/INDEX_SPRINTS.md` — already Active
- [ ] Confirm with Kai before starting implementation

> **INDEX update rule (strict):**
> 1) Update when any AF/BUG/ADR/SPRINT status changes
> 2) Also update as a ritual at sprint start

---

## 5) PR plan (expected slices)
> Rule: **1 PR = 1 sprint (per SPRINT_MANUAL §1.1 + §6.0).**

- **Single branch:** `feat/sprint12-autonomy-boundaries`
- **Single PR at sprint close** covering all scope items:
  - AF0107 — load_documents MD inputs reliability
  - AF0108 — Unify summarization skill
  - AF0109 — emit_result strict content validation
  - AF0110 — Run layout and plan artifacts refactor
  - AF0111 — --workspace flag must never create
  - AF0105 — CLI defaults verification audit
  - AF0106 — V1Planner file pattern defaults
  - AF0096 — Test workspace cleanup pollution

---

## 6) Definition of Done (Sprint-level)
- [x] All P0 items are merged
- [x] Each merged AF has its completion section filled
- [x] Evidence captured for behavior changes (tests + RunTrace ID(s))
- [x] Review completed (ACCEPT WITH FOLLOW-UPS)
- [x] Repo hygiene executed (per checklist)
- [x] Indices updated and consistent

---

## 7) Risks & mitigations
- Risk: Breaking change due to plan storage path move and removal of deprecated files
  - Mitigation: Explicit no-backward-compatibility scope + targeted runtime/storage tests
- Risk: Skill unification causes planner/playbook references to fail
  - Mitigation: Registry validation + playbook and planner integration tests
- Risk: Strict emit validation blocks expected workflows
  - Mitigation: Clear error messaging + trace evidence for rejection reasons

---

## 8) Dependencies
- Internal: AF0108 depends on AF0107; AF0109 depends on AF0108; AF0110 depends on AF0109
- External: none

---

# Sprint report section (fill at sprint end)

## 9) Outcome summary
- Shipped:
  - AF-0107: load_documents fallback patterns + planner Rule 6
  - AF-0108: Unified summarization (deleted summarize_docs, conversion adapter)
  - AF-0109: emit_result strict content validation (_validate_content)
  - AF-0110: Removed _build_result_artifact, plan-as-artifact storage
  - AF-0111: Workspace guard — ag run/plan list/runs list reject nonexistent workspace
  - AF-0105: CLI defaults — 7 commands use _resolve_workspace_with_default
  - AF-0106: Workspace-aware file pattern detection in V1Planner
- Not shipped:
  - AF-0096: Test workspace cleanup pollution (P2, deferred — no regressions observed)

---

## 10) Completed work
- ✅ AF-0107 (P1): Hardcoded fallback `["**/*.md"]` in load_documents + Rule 6 in planner system prompt
- ✅ AF-0108 (P0): Deleted summarize_docs.py, fixed summarize_v0 playbook to use synthesize_research, added `_adapt_document_to_source()` adapter in runtime
- ✅ AF-0109 (P0): Added `_TEMPLATE_MARKERS` regex and `_validate_content()` in emit_result.py; rejects empty, whitespace-only, and template-placeholder content
- ✅ AF-0110 (P0): Removed `_build_result_artifact()` from runtime.py; plan JSON now saved as `{run_id}-plan` artifact in main.py after execution
- ✅ AF-0111 (P2): Added `_guard_workspace_exists()` helper; applied to `ag run`, `ag plan list`, `ag runs list`; 4 contract tests
- ✅ AF-0105 (P2): Replaced 7 hardcoded `--workspace is required` patterns with `_resolve_workspace_with_default()` calls
- ✅ AF-0106 (P2): Added `_detect_workspace_files()` to V1Planner; scans workspace inputs for file extensions, includes hint in user prompt

---

## 11) Not completed / carried over
- ⏭️ AF-0096 (P2): Test workspace cleanup pollution — low-priority, no observed test isolation failures; defer to Sprint 13 if needed

---

## 12) Evidence
- Review file(s):
  - `S12_REVIEW_01.md`
- Representative RunTrace IDs:
  - `bf02b3bb-930e-4e81-8590-f0cea0b7db9e` — successful dual-emit run (MD + JSON)
  - `9e70dcf7` — MD-only Düsseldorf history report
  - `b908e74b` — failure-path run (content validation rejection, pre-fix)
- Runtime bugfix commits (discovered during live testing):
  - `04563f1` — strip `previous_step.*` placeholder strings from plan params
  - `c87b99f` — tolerate trailing commas in LLM JSON output
  - `461de59` — strip `//` comments from LLM JSON output
  - `7af500d` — alias fields override placeholder canonical values (BUG-0016b)
  - `517aba1` — accumulated chaining for multi-emit plans (BUG-0016c)
  - `4066240` — remove unused `previous_result` variable (ruff F841)
- Test summary:
  - 690 passed, 3 deselected
  - `ruff check src tests` — All checks passed
  - `ruff format --check src tests` — All formatted
  - `pytest -W error` — 690 passed
  - Coverage: 89% (3598 statements, 398 missed)

---

## 13) Learnings
- What worked: Sequential AF implementation with per-AF todo tracking and immediate commits kept progress clear; lint/format/test cycle after each AF caught issues early
- What to improve: Some AF files used different metadata formats (# Status: vs - **Status:**), causing mismatch risk during close ritual; standardize AF templates

---

## 14) Next sprint candidate slice
- P0: AF-0103 (LLM Planner V2 — skills+playbooks)
- P1: AF-0104 (LLM Planner V3 — feasibility)
- P2: AF-0096 (Test workspace cleanup, carried over)
