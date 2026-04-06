# FOUNDATION OPERATING MANUAL
# Convergent version: v1.3.1
# File version: v1.0
# Effective date: 2026-03-04

This document is the **single source of truth** for engineering execution in ag_foundation.
It replaces and consolidates:
- CODING_GUIDELINES.md
- ENGINEERING_GUIDELINES.md
- GITHUB_WORKFLOW.md
- REPO_HYGIENE.md

All rules herein are non-negotiable unless explicitly escalated and approved.

---

## 1. Core Invariants (Non-Negotiable)

These rules are absolute. No PR may violate them. No exception exists without explicit escalation.

### 1.1 Truthful UX
- Any user-visible label MUST be derivable from persisted `RunTrace` data.
- Labels are not invented, assumed, or approximated.
- Proof requirement: `ag runs show <run_id>` must demonstrate the exact trace fields backing any printed label.

### 1.2 Workspace Isolation
- The runtime MUST NOT read or write outside active workspace boundaries.
- No cross-workspace data leakage.
- No implicit workspace creation.
- Workspace paths are strict; violations are blocking bugs.

### 1.3 Manual Mode Gating
- Manual mode is **dev/test-only**.
- If manual mode is touched, enforce a dev gate (`AG_DEV=1` or equivalent).
- Print an explicit banner when manual mode is active.
- Manual mode must never be silently enabled.

### 1.4 Layer Separation
- CLI/API/Event adapters parse inputs and call core pipeline only.
- No business logic in adapters.
- Planner/Orchestrator/Executor/Verifier/Recorder must remain independently replaceable.
- Prefer small, composable modules.

### 1.5 Commit & PR Discipline
- 1 commit per AF (each AF is committed separately to the sprint branch).
- 1 PR per sprint (the sprint branch is merged to main via a single PR at sprint close).
- Every PR must be reviewable in ~15–30 minutes.
- If larger, split plan required.

### 1.6 CI Discipline
- Ruff linting must pass.
- Ruff formatting must pass.
- Tests must pass with warnings treated as errors.
- Coverage thresholds must be maintained.
- No PR merges with CI failures.

---

## 2. Architectural Layering Rules

### 2.1 Module Structure
```
ag/cli/       — CLI adapter only (Typer/Click). No business logic.
ag/core/      — Core runtime modules and interfaces:
                task_spec.py, run_trace.py (schemas)
                normalizer.py, planner.py, orchestrator.py, 
                executor.py, verifier.py, recorder.py
ag/skills/    — Skill registry + skill implementations
ag/storage/   — Persistence (sqlite, artifacts, configs)
ag/telemetry/ — Trace export (optional; OTel/Langfuse)
ag/policy/    — Safety hook interfaces and minimal implementations
ag/providers/ — LLM provider adapters (OpenAI, Claude, local stubs)
```
If folder names differ, **layer separation must be preserved**.

### 2.2 Interface-First Development
When adding behavior:
1. Define or extend an interface
2. Implement behind that interface
3. Add tests
4. Add trace fields (if behavior is user-visible)

Examples:
- Adding retrieval: add `Retriever` interface + stub; do NOT embed retrieval into Planner directly.
- Adding a workflow backend: keep `Orchestrator` interface stable; swap backend implementation.

### 2.3 Trace Instrumentation Rules
Any behavior that affects outputs or execution decisions MUST be traceable.

Every step emits:
- `step_id`, `role`, `reasoning_mode`, `status`, `timing_ms`
- tool/skill calls with outcomes
- evidence refs (if used)
- errors + retries

Trace schema changes are **P1+** and require:
- ARCHITECTURE.md doc update
- Migration/compat note (if needed)

### 2.4 Error Handling Rules
- Fail fast on invalid inputs (adapter/normalizer level).
- Inside the runtime:
  - Capture exceptions into trace step `errors`
  - Return a controlled failure status with next-action hints
- **Never swallow errors silently.**

### 2.5 Configuration Rules
Config resolution order is fixed:
1. TaskSpec overrides
2. Workspace config
3. System defaults

Config must be:
- Explicit and discoverable (`ag ws config ...`)
- Recorded in trace (what defaults/overrides were applied)

### 2.6 Performance / Overhead Rules
- Keep the "happy path" minimal; avoid heavy frameworks until thresholds are reached.
- If introducing a dependency (LangGraph/LlamaIndex/etc.), include:
  - Why now (threshold)
  - What interface it implements
  - How to disable or bypass for dev/test

---

## 3. Repository Structure & Artifact Locations

### 3.1 Canonical Locations
| Artifact Type | Location |
|---------------|----------|
| Backlog items | `/docs/dev/backlog/items/` |
| Backlog templates | `/docs/dev/backlog/templates/` |
| Backlog index | `/docs/dev/backlog/INDEX_BACKLOG.md` |
| Bug reports | `/docs/dev/bugs/reports/` |
| Bug templates | `/docs/dev/bugs/templates/` |
| Bug index | `/docs/dev/bugs/INDEX_BUGS.md` |
| ADRs | `/docs/dev/decisions/files/` |
| ADR templates | `/docs/dev/decisions/templates/` |
| ADR index | `/docs/dev/decisions/INDEX_DECISIONS.md` |
| Sprint docs | `/docs/dev/sprints/documentation/Sprint##_desc/` |
| Sprint templates | `/docs/dev/sprints/templates/` |
| Sprint index | `/docs/dev/sprints/INDEX_SPRINTS.md` |
| CHANGELOG | `/docs/dev/CHANGELOG.md` (governance root) |
| Foundation docs | `/docs/dev/foundation/` |

### 3.2 Naming Conventions (Strict)

**Backlog Items:**
- File name: `AF####_<STATUS>_<three_word_description>.md`
- Status values: `PROPOSED | READY | BLOCKED | DONE | DROPPED`

**Bug Reports:**
- File name: `BUG####_<STATUS>_<three_word_description>.md`
- Status values: `OPEN | FIXED | DROPPED`

**ADRs:**
- File name: `ADR###_<STATUS>_<three_word_description>.md`
- Status values: `PROPOSED | ACCEPTED | SUPERSEDED | DEPRECATED`

**Sprints:**
- Folder: `Sprint##_three_word_description/`
- Files: `S##_DESCRIPTION.md`, `S##_REVIEW_01.md`, `S##_PR_01.md`
- Artifacts: `artifacts/` subfolder

### 3.3 Folder Invariants
- Process docs canonical location: `/docs/dev/foundation/`
- Templates canonical location: respective `/templates/` folders
- Index files must exist at top of each artifact folder
- No stray files outside canonical locations

### 3.4 Versioning Conventions

Two version types exist. Every governance file carries at least the convergent version. Foundation documents additionally carry an independent file version.

**Convergent version** — the GVS release version (e.g. `v1.3.1`).
- Present in ALL governance files as a metadata header field.
- Bumped only when a new GVS version is released — not by individual AFs.
- All files updated in batch at release time.

**File version** — the document's own revision counter (e.g. `v0.3`).
- Present in foundation documents only (`FOUNDATION_MANUAL`, `SPRINT_MANUAL`, `FOLDER_STRUCTURE_*`, `PROJECT_PLAN_*`).
- Bumped by the AF that edits the document.
- Minor bump (`v0.2 → v0.3`) for additive changes; major bump (`v0.3 → v1.0`) at PM discretion for structural rewrites.

**Where versions appear:**

| File category | Convergent version | File version | Version in filename |
|---|:--:|:--:|:--:|
| Foundation docs | ✅ header | ✅ header | ✅ (e.g. `FOLDER_STRUCTURE_0.3.md`) |
| INDEX files | ✅ header | — | — |
| Templates | ✅ header | — | — |
| AF / BUG / ADR files | ✅ header | — | — |
| Sprint docs | ✅ header | — | — |
| Additional files | ✅ header | — | ✅ (new version = new file) |

---

## 4. Branching & PR Discipline

### 4.1 Branch Naming
Required format:
- `feat/<short-name>` — new features
- `fix/<short-name>` — bug fixes
- `chore/<short-name>` — maintenance, docs, refactors

### 4.2 Branch Model
- `main`: always releasable, protected
- Feature branches created from `main`
- Squash merge preferred
- PR title should be a good changelog line

### 4.3 PR Requirements (Minimum)
Every PR must include:
1. **Sprint reference:** sprint ID + all AF items completed in the sprint
2. **Summary:** clear description + non-goals
3. **Files changed:** list of important paths touched
4. **Evidence:**
   - Tests run (commands + results)
   - RunTrace ID(s) for behavior changes
5. **Docs updated:** if contracts or workflow changed
6. **Risk level:** P0 / P1 / P2

### 4.4 PR Size Rule
- Must be reviewable in ~15–30 minutes
- If larger: split plan required
- Each AF is a separate commit on the sprint branch for traceability

### 4.5 Evidence Requirements by PR Type
| PR Type | Tests Required | RunTrace Required |
|---------|---------------|-------------------|
| Docs-only | No | No |
| CLI adapter | Unit + Integration | Yes (if labels change) |
| Core runtime | Unit + Integration | Yes |
| Skill/plugin | Unit + Integration | Yes |
| Storage | Unit + Integration | No (unless behavior visible) |
| Trace schema | Contract tests | Yes |

### 4.6 Merge Strategy
- Regular merge (no squash) to preserve per-AF commit traceability on main
- Verify CI passes before merge
- AF completion section must be filled before merge

---

## 5. CI & Quality Enforcement

### 5.0 Two-Phase CI Workflow (CRITICAL)

**During AF development** — run targeted tests only:
```bash
pytest tests/test_<relevant>.py -W error
```
Do NOT run the full suite on every save. Targeted tests keep feedback fast.

**Before commit (full gate)** — run the complete gate once:
```bash
ruff check src tests
ruff format --check src tests
pytest -W error
pytest --cov=src/ag --cov-report=term-missing
```
All four commands must pass before `git commit`.

### 5.1 Full Gate Commands (Reference)

**Linting:**
```bash
ruff check src tests
```

**Formatting:**
```bash
ruff format --check src tests
# Or apply formatting:
ruff format src tests
```

**Tests:**
```bash
pytest -W error
```

**Coverage:**
```bash
pytest --cov=src/ag --cov-report=term-missing
```

### 5.2 CI Pipeline Enforcement
CI will fail if:
1. Ruff linting fails
2. Ruff formatting check fails
3. Any warning is raised during tests (warnings-as-errors)
4. Coverage drops below thresholds
5. External network dependency detected (unless explicitly allowed)

### 5.3 Warnings Policy
All tests MUST pass with warnings treated as errors.

This catches:
- ResourceWarning (unclosed files/connections)
- DeprecationWarning (deprecated APIs)
- UserWarning (potential issues)

### 5.4 Network Restrictions
- No external network calls in CI tests unless explicitly allowed
- No hidden LLM provider dependencies
- Non-deterministic tests require explicit controls

---

## 6. Testing Requirements by Change Type

### 6.1 Coverage Thresholds
| Module | Minimum Coverage |
|--------|-----------------|
| Overall | ≥85% |
| CLI (`src/ag/cli/`) | ≥72% |
| Providers (`src/ag/providers/`) | ≥95% |
| Storage (`src/ag/storage/`) | ≥95% |
| Core (`src/ag/core/`) | ≥85% |

### 6.2 Test Tier Responsibilities

**Unit tests (required for core logic):**
- Pure functions and module logic (planner heuristics, normalizer, trace builders)
- No network calls
- Fast (< 1s per test suite chunk)

**Integration tests (required when pipeline behavior changes):**
- Exercise `ag run` end-to-end (prefer manual mode for speed where allowed)
- Validate that:
  - a RunTrace is created
  - trace fields match expectations
  - CLI output labels match trace facts

**Contract tests (required for interfaces/schemas):**
- Validate `TaskSpec` and `RunTrace` schema stability
- Validate skill contracts (inputs/outputs/permissions metadata)

### 6.3 Required Tests by Change Type

**A) Docs-only changes:**
- No tests required

**B) CLI adapter changes:**
- Unit test parsing/flag behavior (if non-trivial)
- Integration test to confirm CLI output remains trace-derived

**C) Core runtime changes (planner/orchestrator/executor/verifier/recorder):**
- Unit tests for logic
- Integration test for `ag run` pipeline
- At least one captured trace (run_id) as evidence

**D) Skill/plugin changes:**
- Unit test for skill logic
- Integration test showing invocation recorded in trace

**E) Storage changes:**
- Unit tests for storage adapters
- Integration test to confirm persistence + workspace isolation

**F) Trace schema changes (P1+):**
- Contract tests for new fields
- Backwards-compat note (or migration)
- Update ARCHITECTURE doc section on trace contract

### 6.4 What to Assert in Tests
- `run.status` and `verifier.status` expectations
- Presence and correctness of step fields:
  - `role`, `reasoning_mode`, `status`, `timing_ms`
- Correctness of "truthful label" derivation from trace facts
- Workspace isolation (paths, DB, artifacts)

### 6.5 Test Evidence in PRs
Every behavior-changing PR must include:
- Commands run (`pytest ...`)
- Summary of results
- RunTrace ID(s) if behavior changed

---

## 7. Index Discipline & Status Integrity

### 7.1 Index Update Rule (Strict)
INDEX files MUST be updated:
1. Whenever AF/BUG/ADR/SPRINT status changes
2. As a ritual at sprint start
3. In the same PR if tied to the status change

### 7.2 Status Alignment Rule
- **Filename status MUST match internal Status field.**
- If status changes: rename file AND update internal Status field AND update INDEX.
- Mismatched statuses are blocking defects.

### 7.3 Index Files
| Index | Location |
|-------|----------|
| Backlog | `/docs/dev/backlog/INDEX_BACKLOG.md` |
| Bugs | `/docs/dev/bugs/INDEX_BUGS.md` |
| Decisions | `/docs/dev/decisions/INDEX_DECISIONS.md` |
| Sprints | `/docs/dev/sprints/INDEX_SPRINTS.md` |

### 7.4 Linking Convention
Filename columns in index files MUST use clickable markdown links:
- Format: `[filename](subfolder/filename)`
- Example: `[AF0073_READY_index_file_linking.md](items/AF0073_READY_index_file_linking.md)`
- Links must be relative to the index file location
- Works in VS Code, GitHub, and most markdown renderers

### 7.5 Sprint Start Ritual
**Jeff + Kai:**
- Create AFs (Status = Ready)
- Create sprint description file
- Define sprint ID + name

**Jacob:**
- Read sprint description
- Check AFs in scope
- Ask clarifying questions (chat only)
- Create branch
- Create sprint folder
- **Update ALL INDEX files**
- Confirm with Kai before starting implementation

### 7.6 Status Transitions

> **Canonical status values** are defined here. All other documents (FOLDER_STRUCTURE, templates, INDEX headers) must reference this section — not redefine their own sets.

**Backlog Items:**
```
Proposed → Ready → Done
                 ↘ Blocked → (resume) → Done
                 ↘ Dropped
```

**Bug Reports:**
```
Open → Fixed
     ↘ Dropped
```

**ADRs:**
```
Proposed → Accepted → Superseded
                   ↘ Deprecated
```

**Sprints:**
```
Planned → Done
       ↘ Rejected
```

### 7.7 Historical Record Immutability

Pre-v1.3 governance entries (INDEX rows, AF/BUG files, sprint docs) retain their original layout and naming conventions. Do not retroactively rename, restructure, or normalize historical records to match current conventions. New conventions take effect from the sprint following their introduction.

---

## 8. Evidence & Truthfulness Requirements

### 8.1 RunTrace Requirements
Every behavior change affecting outputs or execution decisions requires:
- Captured RunTrace ID
- Validation that trace fields match expectations

### 8.2 Label Derivation Rule
Any label printed to user MUST be derivable from:
- `RunTrace.status`
- `RunTrace.verifier.status`
- Step-level `reasoning_mode`, `role`, `status`

Labels are never:
- Approximated
- Hardcoded without trace backing
- Derived from internal-only state

### 8.3 Proof via `ag runs show`
Evidence must demonstrate:
```bash
ag runs show <run_id> --json
```
And show exact field → label mapping.

### 8.4 When Trace ID is Mandatory
- CLI output changes involving labels
- Planner/Orchestrator/Executor behavior changes
- Verifier logic changes
- Any user-visible status derivation

### 8.5 Artifact Capture
When behavior changes:
- Capture representative trace
- Store trace ID in AF completion section
- Optionally store full trace in sprint artifacts folder

---

## 9. Violations & Escalation Protocol

### 9.1 If Unsure
- Propose 2–3 options
- Recommend one
- Present to human and ask for decision

### 9.2 If Invariant Conflict Detected
- **STOP immediately** — do not attempt a workaround or partial fix.
- Document the conflict in a BUG report (`bugs/reports/BUG####_<description>.md`).
- Post a summary in chat:
  1. Which invariant(s) conflict
  2. Where the conflict was found (file, section, line)
  3. Proposed resolution (2–3 options if ambiguous)
- **Do not proceed** until explicit human confirmation (G10 — scope-level finding).
- If no human response within the current session, park the AF as `BLOCKED` and move to the next work item.

### 9.3 Prohibited Actions
- No silent shortcuts (undocumented workarounds)
- No undocumented behavior changes
- No "fix in next PR" deferrals for failing tests
- No merge with CI failures
- No bypassing manual mode gate

### 9.4 Escalation Path
1. Document the issue clearly
2. Create bug report if appropriate
3. Present the issue in chat with proposed resolution
4. Ask for decision before proceeding

### 9.5 When to Block PR
A PR must be blocked if:
- CI fails
- Coverage drops below threshold
- Truthful UX violated
- Workspace isolation violated
- Index not updated
- Filename ↔ status mismatch exists

---

## 10. Human-in-the-Loop (HITL) Framework

This framework is a first-class governance component, not an afterthought.

### 10.1 Mandatory Gates (Agent MUST Present Result and Request Approval)

At every gate, the agent MUST:
1. Summarize what was completed
2. State readiness for the next action
3. Explicitly ask for approval to proceed

A gate is a **checkpoint where the agent drives the conversation**, not a wall where the agent goes silent.

**Approval authority:** The PM (Kai) is the sole approval authority for all gates. No timeout SLA — the agent waits until the PM responds.

#### Active gates (currently referenced in sprint workflows)

| # | Gate | Trigger | Agent Action | Example |
|:--:|---|---|---|---|
| G1 | Sprint scope approval | Before any implementation begins | Present scope summary, confirm readiness, ask "May I proceed?" | After reading all AF files and verifying INDEX entries, present the scope table and ask for go-ahead. |
| G2 | Clarifying questions | Scope is ambiguous or unclear | Present specific questions, propose defaults if possible, ask for answers | AF says "reconcile status values" but two valid sets exist — present both, recommend one, ask PM to decide. |
| G3 | Pre-implementation confirmation | Scope, INDEX, statuses verified | Present verification results, confirm all clear, ask "Ready to start implementation?" | Sprint start ritual done, checklist passed — present results and ask "Ready to start AF-0009?" |
| G4 | AF completion approval | After each AF is implemented | Present AF summary (files changed, tests passed, key decisions), ask "Approve and move to next AF?" | AF-0009 done — list files edited, acceptance criteria met, ask for commit approval. |
| G5 | Review decision | Before sprint close | Present review summary, ask for ACCEPT / ACCEPT WITH FOLLOW-UPS / REJECT | All 7 AFs complete, verification passed — present S01_REVIEW summary, ask for sprint decision. |

#### Reserved gates (defined for future use, not yet referenced in workflows)

| # | Gate | Trigger | Agent Action |
|:--:|---|---|---|
| G6 | Destructive actions | force push, branch deletion, data drops | Describe the destructive action and its impact, ask for explicit confirmation |
| G7 | Rule exceptions | Agent proposes any deviation from documented rules | Explain the deviation, justify it, ask for approval |
| G8 | Escalation: blocked work | Tests fail with no clear fix | Present the failure, propose 2–3 options, recommend one, ask for decision |
| G9 | Escalation: invariant conflict | Core invariant may be violated | Identify the conflict, explain consequences, ask for resolution |
| G10 | Escalation: scope creep | Work exceeds documented AF scope | Flag the excess, propose trim or expansion, ask for decision |
| G11 | Escalation: unclear approach | Cannot determine correct implementation | Present the ambiguity, propose options, ask which to pursue |
| G12 | Escalation: blocking dependency | External dependency prevents progress | Describe the blocker, propose workaround or wait, ask for decision |
| G13 | Autonomy gate (start) | Sprint touches planner/orchestrator/verifier/execution | Present autonomy impact assessment, ask for approval to proceed |
| G14 | Autonomy gate (close) | P0 autonomy items must be resolved before close | Present autonomy checklist status, ask for close approval |
| G15 | PR block | CI fails, coverage drops, truthful UX violated, workspace isolation violated, INDEX not updated | Present the blocking issue, propose fix, ask for approval |

**Escalation procedure (G8–G12):** Document issue → propose 2–3 options → recommend one → present to human and ask for decision. Never go silent.

### 10.2 Human Rights (Exercisable at Any Time via Chat)

| Right | Description |
|---|---|
| **Ad hoc rule override** | Modify any operational parameter for the current situation (e.g., "stretch quickfix budget to 60 min") |
| **Scope change** | Add, remove, or reprioritize AFs mid-sprint |
| **Stop work** | Halt any activity immediately |
| **Override recommendation** | Agent advises, human decides. Human decision is final. |

### 10.3 Constitutional Principle

> **Chat messages are temporary amendments.**
> They apply to the current situation only and do not modify documented workflows.
> Permanent changes to governance documents always require a formal AF with review.

Example: If the human says "stretch quickfix budget to 60 min this time," that's valid for *this sprint only*. Next sprint reverts to the documented 30 min rule unless an AF formally changes it.

### 10.4 Review Decisions

The human-in-the-loop makes one of three decisions at sprint close:

| Decision | Action |
|---|---|
| **ACCEPTED** | Close sprint. Merge PR. |
| **ACCEPT WITH FOLLOW-UPS** | Create follow-up AFs. Close sprint. Merge PR. |
| **REJECTED** | Sprint status → `REJECTED`. Branch preserved (not deleted). No merge. Sprint description records rejection rationale + learnings. Human decides next step. |

**Quickfix budget:** 30 min **total cumulative** for in-sprint fixes before close. Human-overridable ad hoc per §10.2.

---

## References

- Sprint execution: `/docs/dev/foundation/SPRINT_MANUAL.md`
- Architecture: `/ARCHITECTURE.md`
- CLI reference: `/CLI_REFERENCE.md`
- Deprecated docs: `/docs/dev/foundation/old/`
