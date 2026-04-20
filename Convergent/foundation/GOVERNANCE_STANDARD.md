# GOVERNANCE STANDARD
#### Description: The single source of truth for all governance rules. Defines core conventions (§IM01–§IM02), team roles and HITL authority (§IM03), sprint lifecycle overview (§DS03), gate definitions and escalation procedures (§IM04–§IM06), artifact status lifecycle (§IM07), and the consumer extension pattern (§IM08). Phase definitions (Phases 1–6) are canonical in LIFECYCLE_REGISTRY; GS retains a pointer. All rules are non-negotiable unless escalated via gate E4. The Sprint Playbook operationalizes these rules into executable steps.
#### Convergent: v1.3.2
#### governs: ag_foundation

This document is the **single source of truth** for governance rules. All rules herein are non-negotiable unless explicitly escalated and approved. For step-by-step execution, see `SPRINT_PLAYBOOK.md`.
---

**Index**

**Governance (immutable)**
- §IM01 Index Discipline & Status Integrity
- §IM02 Historical Record Immutability
- §IM03 Team Structure
  - §IM03.1 Roles
  - §IM03.2 Assignment Criteria
  - §IM03.3 Artifact Ownership
- §IM04 Gate Behavior at Runtime
- §IM05 Escalation Procedure
- §IM06 Human Rights & Constitutional Principle
- §IM07 Status Lifecycle Reference
  - §IM07.1 Universal Status Model
  - §IM07.2 State Machine
  - §IM07.3 Transitions
  - §IM07.4 Gate Mapping
  - §IM07.5 Historical Compatibility
- §IM08 System Architecture
  - §IM08.1 File Roles
  - §IM08.2 Section Classification
  - §IM08.3 Directional Rules
  - §IM08.4 Server Boundary
  - §IM08.5 Consumer Extension Pattern

**Defaults (Source-Delegated)**
- §DS01 Repository Structure & Naming
- → `foundation/sources/FOLDER_STRUCTURE.md`
- §DS02 Session Continuity & Handoff
- → `foundation/sources/SESSION_CHAIN.md`
- §DS03 Lifecycle Overview
  - §DS03.1 The 6 Sprint Phases
  - §DS03.2 Gate Summary
- → `foundation/sources/LIFECYCLE_REGISTRY.md` (canonical phase definitions, Phases 1–6)
- §DS04 Gate Severity Labels
- §DS05 Gate Categories

**Defaults (PC Override)**
- §PO01 Non-Negotiable Invariants
- §PO02 Testing Framework
- §PO03 Violations & Escalation
- §PO04 ADR Creation Criteria
- §PO05 Architectural Layering
- §PO06 Autonomy Gate
- §PO07 CI Checkpoints
- §PO08 Living Docs

---

# Governance (Immutable)

> Core governance rules that apply universally. These rules cannot be overridden by PROJECT_CONTROL.

## §IM01 Index Discipline & Status Integrity

**Index Update Rule (Strict):**

INDEX files MUST be updated:
1. Whenever AF/BUG/ADR/SPRINT status changes
2. As a ritual at sprint start
3. In the same commit if tied to the status change

**Status Alignment Rule:**

*New-convention files (immutable filenames):*
- Status lives in exactly **2 places**: internal `Status:` field + INDEX row.
- Status changes require exactly **2 edits**, zero renames.

*Legacy files (status token in filename):* see §IM02.1.

Mismatched statuses are blocking defects.

For INDEX file locations and linking conventions → `FOLDER_STRUCTURE.md`.

> For status values, valid transitions, and lifecycle diagrams, see §IM07.

## §IM02 Historical Record Immutability

Pre-v1.3.2 governance entries (INDEX rows, AF/BUG files, sprint docs) retain their original layout and naming conventions. Do not retroactively rename, restructure, or normalize historical records to match current conventions. New conventions take effect from the sprint following their introduction.

### §IM02.1 Legacy File Naming

Legacy files carry a status token in the filename (e.g. `AF0012_DONE_description.md`).

- Status lives in **3 places**: filename token + internal `Status:` field + INDEX row.
- All three must match. Status changes require a file rename + internal field update + INDEX update.
- Do not create new files with status tokens — that convention is legacy only.

### §IM02.2 Legacy Status Mapping

Historical artifacts retain their original status values. The following legacy values remain valid in closed records:

| Legacy Status | Equivalent Universal Status | Artifact Type |
|---------------|:---------------------------:|---------------|
| OPEN | PROPOSED or READY | BUG |
| FIXED | DONE | BUG |
| DECIDED | DONE | ADR |
| ACCEPTED | DONE | ADR |
| SUPERSEDED | DEPRECATED | ADR |
| PLANNED | READY | Sprint Description |
| REJECTED | DEPRECATED | Sprint Description |
| DROPPED | DEPRECATED | AF, BUG |

New artifacts (v1.3.2+) use the 5 universal statuses exclusively. Legacy files keep their original names — do not rename them.

## §IM03 Team Structure
<!-- Kai: can do more here; make it virtual? -->
GVS assumes a multi-agent team. Each project has a HITL (human-in-the-loop) and one or more agents with distinct roles. The generic term "agent" in all GS sections refers to whichever agent is assigned the current task.

### §IM03.1 Roles

| Role | Shorthand | Responsibilities |
|------|-----------|-----------------|
| HITL | — | Sprint planning, gate approvals, agent routing, scope decisions, escalation resolution |
| Implementation Agent | Agent-I | AF execution, code/docs changes, test runs, INDEX updates, branch management |
| Conceptual Agent | Agent-C | Architecture design, governance evolution, system reasoning, GVS maintenance |

**HITL is the router.** HITL assigns tasks to agents based on problem category. This assignment is explicit — either in the sprint description or at gate O2 (AF iteration start).

### §IM03.2 Assignment Criteria

| Problem Category | Typical Assignment | Rationale |
|-----------------|-------------------|-----------|
| Code changes, doc edits, template fixes | Agent-I | Execution-focused, bounded scope |
| Architecture, governance design, cross-cutting analysis | Agent-C | Requires system-level reasoning |
| Mixed (execution + design in same AF) | HITL splits or assigns primary | Avoid context overload in single agent |

### §IM03.3 Artifact Ownership

| Artifact Category | Primary Owner | Secondary (may edit) |
|------------------|---------------|---------------------|
| AF item files (execution) | Agent-I | — |
| AF item files (governance/architecture) | Agent-C | — |
| BUG item files | Agent-I | — |
| ADR files | Agent-C | Agent-I (inline records) |
| INDEX files | Agent-I (during sprint) | Agent-C (if editing governed content) |
| Sprint description | HITL | — |
| Sprint review / PR files | Agent-I | — |
| PROJECT_CONTROL.md | Agent-C | — |
| PROJECT_ROADMAP.md | HITL | Agent-C |
| CHANGELOG.md | Agent-I | Agent-C |

**Conflict rule:** If both agents need to edit the same file in the same sprint, HITL sequences the work (one agent finishes before the other starts on that file). No concurrent edits to the same file.

## §IM04 Gate Behavior at Runtime
<!-- Kai: can do more here -->
At every gate, the agent MUST:
1. Summarize what was completed
2. State readiness for the next action
3. Explicitly ask for approval to proceed

A gate is a **checkpoint where the agent drives the conversation**, not a wall where the agent goes silent.

## §IM05 Escalation Procedure (all Ex gates)
<!-- Kai: can do more here -->
1. Document the issue clearly
2. Propose 2–3 options if possible
3. Recommend one option
4. Present to HITL and ask for decision
5. Never go silent — always drive toward resolution

## §IM06 Human Rights & Constitutional Principle

**Human Rights (exercisable at any time via chat):**

| Right | Description |
|-------|-------------|
| Ad hoc rule override | Modify any operational parameter for the current situation |
| Scope change | Add, remove, or reprioritize AFs mid-sprint |
| Stop work | Halt any activity immediately |
| Override recommendation | Agent advises, human decides. Human decision is final. |

**Constitutional Principle:**

> Chat messages are temporary amendments. They apply to the current situation only and do not modify documented workflows. Permanent changes to governance documents always require a formal AF with review.

Example: If the human says “stretch quickfix budget to 60 min this time,” that’s valid for *this sprint only*. Next sprint reverts to the documented 30 min rule unless an AF formally changes it.

## §IM07 Status Lifecycle Reference

All governed artifacts follow a single universal status lifecycle. Five statuses, three tiers, seven transitions.

> **Source of truth:** `docs/additional/File_transitions.png`

### §IM07.1 Universal Status Model

| Tier | Status | Description |
|------|--------|-------------|
| Initial | PROPOSED | Artifact created, not yet approved for work |
| Intermediate | READY | Approved and available for implementation |
| Intermediate | BLOCKED | Work impediment — escalation required |
| Final | DONE | Completed successfully |
| Final | DEPRECATED | Abandoned, superseded, or rejected |

This model applies universally to all artifact types: AFs, BUGs, ADRs, and Sprint Descriptions.

### §IM07.2 State Machine

Three layers with strict directional rules:

| Layer | Statuses | Rules |
|-------|----------|-------|
| Initial | PROPOSED | Entry point for all artifacts. Only outbound transitions. |
| Intermediate | READY, BLOCKED | Active work states. Bidirectional (T5 ↔ T6). Receive from Initial, emit to Final. |
| Final | DONE, DEPRECATED | Terminal states. No outbound transitions. |

No transition skips a layer (e.g., PROPOSED cannot go directly to DONE).

### §IM07.3 Transitions

| # | From → To | Trigger Type |
|---|-----------|:------------:|
| T1 | PROPOSED → READY | Gate |
| T2 | PROPOSED → BLOCKED | Escalation |
| T3 | PROPOSED → DEPRECATED | Escalation / HITL decision |
| T4 | READY → DONE | Gate |
| T5 | READY → BLOCKED | Escalation |
| T6 | BLOCKED → READY | Escalation resolution |
| T7 | BLOCKED → DEPRECATED | Escalation resolution |

### §IM07.4 Gate Mapping

Which gate fires each transition, per artifact type. Only T1 and T4 are gate-triggered; all others are escalation-driven (no gate enforcement).

| Transition | From → To | AF | BUG | Sprint | ADR |
|:---:|---|:---:|:---:|:---:|:---:|
| T1 | PROPOSED → READY | G1 | G1 | G1 | -- |
| T2 | PROPOSED → BLOCKED | Escalation | Escalation | Escalation | Escalation |
| T3 | PROPOSED → DEPRECATED | Escalation | Escalation | Escalation | Escalation |
| T4 | READY → DONE | G3 | G3 | G4 | -- |
| T5 | READY → BLOCKED | Escalation | Escalation | Escalation | Escalation |
| T6 | BLOCKED → READY | Escalation | Escalation | Escalation | Escalation |
| T7 | BLOCKED → DEPRECATED | Escalation | Escalation | Escalation | Escalation |

**Reading this table:**
- **G1** (Planning commit): HITL approves artifact scope → status moves to READY
- **G3** (AF commit): Agent presents AF summary, HITL approves → AF/BUG status moves to DONE
- **G4** (Review decision commit): HITL approves sprint review → Sprint status moves to DONE
- **ADR = always `--`**: ADR transitions are HITL-driven with no gate enforcement
- **Escalation**: Triggered by human or agent escalation (E1–E8), not by passing a checkpoint

### §IM07.5 Historical Compatibility

Legacy status values and their universal equivalents → §IM02.2.

## §IM08 System Architecture

GVS uses a server/consumer architecture. The server (`foundation/`) provides immutable governance rules. Consumer projects read the server and extend it through their own `PROJECT_CONTROL.md`.

### §IM08.1 File Roles

| Role | Files | Description |
|------|-------|-------------|
| Interface | `GOVERNANCE_STANDARD.md` | Single source of truth for all governance rules. Defines the contract. |
| Implementation | `SPRINT_PLAYBOOK.md` | Executable script that operationalizes GS rules into sprint steps. |
| Delegated Content | `sources/FOLDER_STRUCTURE.md` | Canonical folder layout and naming (delegated by §DS01). |
| Delegated Content | `sources/LIFECYCLE_REGISTRY.md` | Canonical phase/step/task/gate definitions (delegated by §DS03). |
| Delegated Content | `sources/SESSION_CHAIN.md` | Session continuity and handoff model (delegated by §DS02). |
| Scaffolding | `templates/*.md` | Starting-point files for consumer artifacts. Read-only at runtime. |
| Consumer Override | `docs/project/PROJECT_CONTROL.md` | Project-specific rules that override or extend GS §PO defaults. |

### §IM08.2 Section Classification

| Prefix | Modifier | Meaning |
|--------|----------|---------|
| §IM | Immutable | Cannot be overridden. Applies universally to all consumers. Equivalent to `final`. |
| §DS | Virtual (source-delegated) | Default content lives in a source file (R1). GS retains enforcement rules or pointers. |
| §PO | Virtual (PC override) | Default content lives in GS body. Consumers may override or extend via PROJECT_CONTROL (R2). |

All three types are defined exclusively in GS. No other document defines § sections.

### §IM08.3 Directional Rules

| Rule | Direction | Description |
|------|-----------|-------------|
| R1 | GS → Sources | GS delegates content to source files. Sources never reference GS. |
| R2 | GS → PC | GS defines defaults. PC overrides or extends them. PC never modifies GS. |
| R3 | SP ↔ GS | SP implements GS. Bidirectional references allowed. |
| R4 | SP ↔ Templates | SP references templates for artifact creation. Bidirectional references allowed. |

Sources reference only siblings. Templates reference only GS (for § pointers) and siblings.

### §IM08.4 Server Boundary

**Everything under `foundation/` is the governance server.** Consumer projects read it as an immutable dependency. No consumer sprint may create, edit, or delete any server file.

**Server files (exhaustive list):**

| Path | File |
|------|------|
| `foundation/` | `GOVERNANCE_STANDARD.md` |
| `foundation/` | `SPRINT_PLAYBOOK.md` |
| `foundation/sources/` | `FOLDER_STRUCTURE.md` |
| `foundation/sources/` | `LIFECYCLE_REGISTRY.md` |
| `foundation/sources/` | `SESSION_CHAIN.md` |
| `foundation/templates/` | `ADR_TEMPLATE.md` |
| `foundation/templates/` | `BACKLOG_ITEM_TEMPLATE.md` |
| `foundation/templates/` | `BUG_REPORT_TEMPLATE.md` |
| `foundation/templates/` | `INDEX_BACKLOG_TEMPLATE.md` |
| `foundation/templates/` | `INDEX_BUGS_TEMPLATE.md` |
| `foundation/templates/` | `INDEX_DECISIONS_TEMPLATE.md` |
| `foundation/templates/` | `INDEX_SPRINTS_TEMPLATE.md` |
| `foundation/templates/` | `PROJECT_CONTROL_TEMPLATE.md` |
| `foundation/templates/` | `PROJECT_ROADMAP_TEMPLATE.md` |
| `foundation/templates/` | `PULL_REQUEST_TEMPLATE.md` |
| `foundation/templates/` | `SPRINT_DESCRIPTION_TEMPLATE.md` |
| `foundation/templates/` | `SPRINT_REVIEW_TEMPLATE.md` |

If a consumer needs a governance change, it creates a backlog item in the GVS development project (convergent). Changes to server files require a governance AF executed in convergent.

### §IM08.5 Consumer Extension Pattern

Each GVS consumer reads all GS sections (generic rules) and defines project-specific rules in their own `PROJECT_CONTROL.md` document.

At execution time, the SP resolves project-specific values (CI commands, coverage thresholds, workspace boundaries) through the consumer's PC. Every §PO section in GS has a corresponding `GS:POxx` section in PC that may override or extend the default.

**Registered consumers:**

| Consumer | PROJECT_CONTROL location |
|----------|-------------------------|
| convergent | `docs/project/PROJECT_CONTROL.md` |

---

# Defaults (Source-Delegated)

> Sections whose canonical content is delegated to source files (R1). GS retains enforcement rules or pointers.

## §DS01 Repository Structure & Naming

Canonical locations, naming conventions, branch naming, and file creation workflows are defined in `FOLDER_STRUCTURE.md`.

**Key rule (enforced here):**
- Legacy file handling (naming, status alignment) → §IM02

Folder invariants, canonical locations, and naming tables → `FOLDER_STRUCTURE.md`.

## §DS02 Session Continuity & Handoff

Session continuity and inter-agent handoff procedures are defined in `SESSION_CHAIN.md`.

**Key rule (enforced here):** Agents do not communicate directly. HITL mediates all inter-agent handoffs.

## §DS03 Lifecycle Overview

### §DS03.1 The 6 Sprint Phases

Every sprint follows a 6-phase lifecycle. Each phase has defined triggers, owners, rules, and gates.

| Phase | ID | Description | Primary Owner |
|-------|:--:|-------------|---------------|
| Sprint Planning | P1 | Scoping, sprint docs, planning commit | HITL |
| Sprint Start | P2 | Read/verify, questions, branch creation | Agent |
| Implementation | P3 | AF loop: implement → evidence → C1 (targeted CI) → commit (repeats per AF) | Agent |
| Review | P4 | C2 (full CI + evidence), PR, human review, decision | Agent + HITL |
| Sprint End | P5 | Quick fixes, finalize docs, C3 (full CI), merge | Agent |
| Inter-Sprint | P6 | Clean up, AF creation, backlog grooming, commit | Agent / HITL |

### §DS03.2 Gate Summary

16 non-escalation gates across 3 categories (Phase, Git, Operational) plus 8 escalation gates (E1–E8) and CI checkpoints (C1/C2/C3).
All gate definitions, severities, and required actions → §DS04–§DS05 (labels, categories), §IM04–§IM06 (behavior, escalation, human rights).

> **Canonical phase definitions (Phases 1–6) have been moved to `foundation/sources/LIFECYCLE_REGISTRY.md`.**
> LR contains the full phase/step/task/gate content for all 6 sprint phases.
> GS retains the lifecycle overview (§DS03) and gate rules (§DS04–§DS05, §IM04–§IM06).

## §DS04 Gate Severity Labels

Three severity levels (Critical, Normal, Additional) control gate activation. Full definitions → `LIFECYCLE_REGISTRY.md`.

## §DS05 Gate Categories

Four gate categories: Phase (Px), Git (Gx), Operational (Ox), Escalation (Ex). Full per-gate tables → `LIFECYCLE_REGISTRY.md`.

---

# Defaults (PC Override)

> Default rules that PROJECT_CONTROL may override or extend (R2) goverened by §IM08

## §PO01 Non-Negotiable Invariants

These rules are absolute. No PR may violate them. No exception exists without explicit escalation (E4).

**Commit & PR Discipline:**
- 1 commit per AF, 1 PR per sprint.
- Every PR must be reviewable in ~15–30 minutes.
- If larger, split plan required.

**CI Discipline:**
- All CI checks must pass before merge.
- No PR merges with CI failures.

**Server Immutability:** See §IM08.4 for the server boundary definition and exhaustive file list.

> Additive: PC GS:PO01 adds project-specific invariants.

## §PO02 Testing Framework

**Test Tier Responsibilities:**

*Unit tests (required for core logic):*
- Pure functions and module logic
- No network calls
- Fast (< 1s per test suite chunk)

*Integration tests (required when pipeline behavior changes):*
- Exercise end-to-end flows
- Validate output correctness

*Contract tests (required for interfaces/schemas):*
- Validate schema stability
- Validate interface contracts

**Required Tests by Change Type:**

| Change Type | Tests Required |
|-------------|---------------|
| Docs-only | None |
| CLI adapter | Unit + Integration |
| Core runtime | Unit + Integration + trace evidence |
| Skill/plugin | Unit + Integration |
| Storage | Unit + Integration |
| Trace schema (P1+) | Contract + compat note + doc update |

**Test Evidence in PRs:**

Every behavior-changing PR must include:
- Commands run
- Summary of results
- Trace/evidence IDs if behavior changed

> Override: PC GS:PO02 sets coverage thresholds, assertion targets, warnings policy.

## §PO03 Violations & Escalation

> Override: PC GS:PO03 adds project-specific blocking conditions and prohibited actions.

**If Unsure:**
- Propose 2–3 options
- Recommend one
- Present to HITL and ask for decision

**If Invariant Conflict Detected:**
- **STOP immediately**
- Document the conflict
- Escalate to HITL with clear summary and proposed resolution (E4)
- Ask for decision before proceeding

**Prohibited Actions:**
- No silent shortcuts (undocumented workarounds)
- No undocumented behavior changes
- No “fix in next PR” deferrals for failing tests
- No merge with CI failures

**When to Block PR:**

A PR must be blocked (E8) if:
- CI fails
- Coverage drops below threshold
- INDEX not updated
- Filename ↔ status mismatch exists

## §PO04 ADR Creation Criteria

Not every decision needs a full ADR. Use this guide:

| Scope | Format | When to Use |
|-------|--------|-------------|
| Inline Decision Record | `## Decision Record` section in the AF file | Single-AF scope, reversible, low risk |
| Full ADR | Standalone file in `docs/files/decisions/` | Cross-AF impact, irreversible, architectural, or sets precedent |

If in doubt, start with an inline record. Promote to full ADR if the decision is referenced by multiple files or affects future sprints.

> Override: PC GS:PO04 sets project-specific ADR thresholds.

## §PO05 Architectural Layering

By default, no layering constraints apply. Code projects should define module boundaries, interface-first rules, and dependency directions in PC.

> Override: PC GS:PO05 defines module structure, interface-first rules, trace instrumentation, error handling, configuration resolution, performance constraints.

## §PO06 Autonomy Gate

By default, no autonomy gate applies. Code projects with autonomy-affecting scope (planner, orchestrator, decision-making modules) must define start/close gate checklists in PC.

> Override: PC GS:PO06 defines start/close gate checklists and decision rules for autonomy-affecting sprints.

## §PO07 CI Checkpoints

CI checkpoints (`C1`–`C3`) are steps (not gates) that feed into gates. See `LIFECYCLE_REGISTRY.md` for the checkpoint table.

> `C<n>` is a checkpoint naming convention, NOT a gate category. Gates remain P/G/O/E.

> Override: PC GS:PO07 defines project-specific CI commands and success criteria for C1/C2/C3.

> **Docs-only projects:** CI checkpoints are replaced with docs-only verification (INDEX consistency, file existence, naming compliance).

## §PO08 Living Docs

By default, the sprint review sweep checks all INDEX files for consistency (status alignment, filename compliance, no orphan entries). PC may extend with project-specific living documents.

> Override: PC GS:PO08 defines which living documents to check during the sprint review sweep.


---

## References

- R3 (implemented by): `foundation/SPRINT_PLAYBOOK.md` — see §IM08.3
- R1 (delegates canonical phases/gates to): `foundation/sources/LIFECYCLE_REGISTRY.md` — see §IM08.3
- R1 (delegates canonical structure to): `foundation/sources/FOLDER_STRUCTURE.md` — see §IM08.3
- R1 (delegates canonical handoff to): `foundation/sources/SESSION_CHAIN.md` — see §IM08.3
- R2 (override contract with): `docs/project/PROJECT_CONTROL.md` — see §IM08.3, §IM08.5 <!-- generic name — use highest version on disk -->
