# Pull Request — Sprint 13: Intelligent Pipeline
# Version number: v0.2

> **FOUNDATION GOVERNANCE**
> This PR is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md` — Section 4: Branching & PR Discipline
> `/docs/dev/foundation/SPRINT_MANUAL.md` — Section 6: PR Creation Protocol
>
> Critical invariants:
> - 1 PR = 1 sprint
> - CI discipline (ruff + pytest -W error + coverage)
> - Evidence required for behavior changes (RunTrace ID)
> - INDEX update required if statuses change

## Sprint work items
- **Sprint:** Sprint13 — intelligent_pipeline
- **Backlog items:** AF-0114, AF-0115, AF-0103, AF-0117 (partial)
- **Bugs:** BUG-0017 (fixed in AF-0115)
- **ADRs:** —

## Summary
- Extracted monolithic runtime.py into dedicated V0 component files (Planner, Orchestrator, Executor, Recorder, Verifier)
- Implemented V1Verifier with step-aware verification and required/optional step handling (9 contract tests)
- Delivered V2Planner that composes mixed skill+playbook plans with new PLAYBOOK step type
- Built V1Orchestrator for mixed plan execution with inline playbook expansion
- Fixed BUG-0017: optional step failures no longer block run completion

## Scope / Non-goals
- In scope: Pipeline extraction, V1Verifier, V2Planner, V1Orchestrator (mixed plans)
- Out of scope: Per-step verification wiring (AF-0117 remainder → Sprint 14), V1Executor output validation (AF-0116), V1Recorder evidence (AF-0118)

## Files changed (required)
- `src/ag/core/runtime.py` — `create_runtime()` updated, V0 logic extracted
- `src/ag/core/v0_planner.py` — extracted V0Planner
- `src/ag/core/v0_orchestrator.py` — extracted V0Orchestrator
- `src/ag/core/v0_executor.py` — extracted V0Executor
- `src/ag/core/v0_recorder.py` — extracted V0Recorder
- `src/ag/core/v0_verifier.py` — extracted V0Verifier
- `src/ag/core/v1_verifier.py` — new V1Verifier with step-aware logic
- `src/ag/core/v1_orchestrator.py` — new V1Orchestrator for mixed plans
- `src/ag/core/v2_planner.py` — new V2Planner with playbook awareness
- `src/ag/core/interfaces.py` — PlaybookStepType.PLAYBOOK added; Step.required field
- `src/ag/core/run_trace.py` — Step model updated with `required` field
- `docs/dev/backlog/items/AF01*.md` — status updates
- `docs/dev/backlog/INDEX_BACKLOG.md` — Sprint 13 scope section
- `docs/dev/sprints/INDEX_SPRINTS.md` — Sprint 13 row
- `docs/dev/sprints/documentation/Sprint13_intelligent_pipeline/` — sprint docs

## Architecture & contracts
- Layers touched: core
- Interfaces touched: Planner, Orchestrator, Executor, Verifier, Recorder (extraction); Step model (required field); PlaybookStepType (PLAYBOOK enum)
- Contract changes? Yes — updated in ARCHITECTURE.md (v0.4: component versioning, pipeline V0/V1 distinction)

## Evidence (required)
### Lint / format
- `ruff check src tests`:
- `ruff format --check src tests`:

### Tests
- Command(s):
  - `pytest -W error`
  - `pytest --cov=src/ag --cov-report=term-missing`
- Result summary:

### Run evidence (required for behavior changes)
- RunTrace ID(s): `run_...`
- Repro command(s):
  - `ag run ...`
- What reviewers should look for in the trace:
  - V1Verifier verdicts on required vs optional steps
  - PLAYBOOK step types in plan
  - Playbook expansion in orchestrator output

### Artifacts (if applicable)
- `artifact://...`

## Docs updates (required when process/contracts touched)
- Updated `/docs/dev/...` files:
  - `ARCHITECTURE.md` (v0.4)
  - `INDEX_BACKLOG.md` (v1.3 — Sprint 13 + Sprint 14 scope)
  - `INDEX_SPRINTS.md` (v0.5)
  - `SPRINT_MANUAL.md` (§9.3 autonomy milestones)
  - `PROJECT_PLAN_0.2.md` (v1.0 — Phase 2b added)
- Notes: Sprint 14 scope items promoted from PROPOSED to READY

## Risk level
- P1
- Notes: Behavior changes to Planner, Orchestrator, and Verifier; autonomy gate applies

## Checklist (must be true to request review)
- [ ] This PR lists all AF items completed in the sprint
- [ ] PR is reviewable in ~15–30 minutes (or split plan exists)
- [ ] Truthful UX preserved (labels trace-derived)
- [ ] Tests run and results included
- [ ] AF completion section filled (for merged PRs)
- [ ] INDEX files updated (if statuses or entries changed):
  - [ ] `/docs/dev/backlog/INDEX_BACKLOG.md`
  - [ ] `/docs/dev/bugs/INDEX_BUGS.md`
  - [ ] `/docs/dev/decisions/INDEX_DECISIONS.md`
  - [ ] `/docs/dev/sprints/INDEX_SPRINTS.md`

## Completion reference
- AF-0114: `/docs/dev/backlog/items/AF0114_DONE_extract_pipeline_v0_files.md`
- AF-0115: `/docs/dev/backlog/items/AF0115_DONE_v1_verifier_step_aware.md`
- AF-0103: `/docs/dev/backlog/items/AF0103_DONE_llm_planner_v2_playbooks.md`
- AF-0117: `/docs/dev/backlog/items/AF0117_DONE_v1_orchestrator_perstep_loop.md` (partial)
