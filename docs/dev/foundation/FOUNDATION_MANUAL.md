# FOUNDATION OPERATING MANUAL
# Version: v1.0
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

### 1.5 Small PR Discipline
- Every PR must be reviewable in ~15–30 minutes.
- If larger, split into multiple PRs.
- 1 PR = 1 primary AF item (for traceability — the PR references one primary work item, but may include multiple items from the same sprint).

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
| Foundation docs | `/docs/dev/foundation/` |

### 3.2 Naming Conventions (Strict)

**Backlog Items:**
- File name: `AF####_<STATUS>_<three_word_description>.md`
- Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

**Bug Reports:**
- File name: `BUG####_<STATUS>_<three_word_description>.md`
- Status values: `OPEN | IN_PROGRESS | FIXED | VERIFIED | DROPPED`

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
1. **Primary AF reference:** exactly one `AF-####`
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
- No "multi-AF" PRs (exception: explicitly scoped chore PRs)

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
- Squash merge preferred
- Verify CI passes before merge
- AF completion section must be filled before merge

---

## 5. CI & Quality Enforcement

### 5.1 Required Commands Before PR

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

**Backlog Items:**
```
Proposed → Ready → In progress → Done
                               ↘ Blocked → (resume) → Done
                               ↘ Dropped
```

**Bug Reports:**
```
Open → In progress → Fixed → Verified
                   ↘ Dropped
```

**ADRs:**
```
Proposed → Accepted → Superseded
                   ↘ Deprecated
```

**Sprints:**
```
Draft → Ready → In Progress → In Review → Accepted → Closed
```

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
- Wait for decision before proceeding

### 9.2 If Invariant Conflict Detected
- **STOP immediately**
- Document the conflict
- Escalate to Kai/Jeff
- Do not proceed with workarounds

### 9.3 Prohibited Actions
- No silent shortcuts (undocumented workarounds)
- No undocumented behavior changes
- No "fix in next PR" deferrals for failing tests
- No merge with CI failures
- No bypassing manual mode gate

### 9.4 Escalation Path
1. Document the issue clearly
2. Create bug report if appropriate
3. Notify in chat immediately
4. Wait for explicit resolution

### 9.5 When to Block PR
A PR must be blocked if:
- CI fails
- Coverage drops below threshold
- Truthful UX violated
- Workspace isolation violated
- Index not updated
- Filename ↔ status mismatch exists

---

## References

- Sprint execution: `/docs/dev/foundation/SPRINT_MANUAL.md`
- Architecture: `/ARCHITECTURE.md`
- CLI reference: `/CLI_REFERENCE.md`
- Deprecated docs: `/docs/dev/foundation/old/`
