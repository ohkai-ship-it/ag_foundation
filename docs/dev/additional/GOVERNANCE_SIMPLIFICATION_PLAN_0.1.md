# GOVERNANCE SIMPLIFICATION PLAN
# Version: v0.1
# Date: 2026-04-03
# Authors: Kai (human), Jacob (Claude Opus 4, Copilot)
# Reviewed by: Jeff (GitHub Copilot, Claude Sonnet 4.6)
# Approved: 2026-04-04
# Status: APPROVED

---

## 1. Executive Summary

Reduce sprint ceremony overhead from **30–50 min/sprint** to **~10 min/sprint** by eliminating filename-status coupling, dropping redundant sprint artifacts, adding time/model logging, formalizing Human-in-the-Loop rights, and introducing lightweight automation.

**Core invariants are preserved.** Truthful UX, CI discipline, evidence capture, 1-commit-per-AF, 1-PR-per-sprint — none of these change. Only the bookkeeping changes.

**Evidence base:** 15 sprints of structural data showing:
- Ceremony overhead: 33–53% of total sprint time
- Triple-sync (filename ↔ internal status ↔ INDEX row) is the dominant pain point
- S##_PR_01.md and S##_REVIEW_01.md duplicate GitHub's native workflow
- BUG-0022 and BUG-0023 were directly caused by filename-status mismatch
- Zero automation exists — all ceremony is manual

---

## 2. Human-in-the-Loop (HITL) Framework

This framework is a first-class governance component, not an afterthought.

### 2.1 Mandatory Gates (Agent MUST Stop and Wait)

| # | Gate | Trigger | Location |
|:--:|---|---|---|
| G1 | Sprint scope approval | Before any implementation begins | SPRINT_MANUAL §0.2 ("proceed") |
| G2 | Clarifying questions | Scope is ambiguous or unclear | SPRINT_MANUAL §0.2, FOUNDATION_MANUAL §7.5 |
| G3 | Pre-implementation confirmation | Scope, INDEX, statuses verified | SPRINT_MANUAL §0.2 |
| G4 | AF completion approval | After each AF — present result, wait for human approval before next AF | SPRINT_MANUAL §4 |
| G5 | Review decision | Before sprint close | SPRINT_MANUAL §8 |
| G6 | Destructive actions | force push, branch deletion, data drops | Always |
| G7 | Rule exceptions | Agent proposes any deviation from documented rules | Always |
| G8 | Escalation: blocked work | Tests fail with no clear fix | SPRINT_MANUAL §4.4 |
| G9 | Escalation: invariant conflict | Core invariant may be violated | FOUNDATION_MANUAL §1, §9.2 |
| G10 | Escalation: scope creep | Work exceeds documented AF scope | SPRINT_MANUAL §11 |
| G11 | Escalation: unclear approach | Cannot determine correct implementation | SPRINT_MANUAL §11, FOUNDATION_MANUAL §9.1 |
| G12 | Escalation: blocking dependency | External dependency prevents progress | SPRINT_MANUAL §11 |
| G13 | Autonomy gate (start) | Sprint touches planner/orchestrator/verifier/execution | SPRINT_MANUAL §9.1 |
| G14 | Autonomy gate (close) | P0 autonomy items must be resolved before close | SPRINT_MANUAL §9.4 |
| G15 | PR block | CI fails, coverage drops, truthful UX violated, workspace isolation violated, INDEX not updated | FOUNDATION_MANUAL §9.5 |

**Escalation procedure (G8–G12):** Document issue → propose 2–3 options → recommend one → wait for explicit decision. Do not proceed with workarounds.

### 2.2 Human Rights (Exercisable at Any Time via Chat)

| Right | Description |
|---|---|
| **Ad hoc rule override** | Modify any operational parameter for the current situation (e.g., "stretch quickfix budget to 60 min") |
| **Scope change** | Add, remove, or reprioritize AFs mid-sprint |
| **Stop work** | Halt any activity immediately |
| **Override recommendation** | Agent advises, human decides. Human decision is final. |

### 2.3 Constitutional Principle

> **Chat messages are temporary amendments.**
> They apply to the current situation only and do not modify documented workflows.
> Permanent changes to governance documents always require a formal AF with review.

Example: If the human says "stretch quickfix budget to 60 min this time," that's valid for *this sprint only*. Next sprint reverts to the documented 30 min rule unless an AF formally changes it.

### 2.4 Review Decisions

The human-in-the-loop makes one of three decisions at sprint close:

| Decision | Action |
|---|---|
| **ACCEPTED** | Close sprint. Merge PR. |
| **ACCEPT WITH FOLLOW-UPS** | Create follow-up AFs and group in a follow-up sprint as '### SPrint XX Scope - Follow-up' in INDEX_BACKLOG. Close sprint. Merge PR. |
| **REJECTED** | Sprint status → `Rejected`. Branch preserved (not deleted). No merge. Sprint description records rejection rationale + learnings. Human decides next step. |

**Quickfix budget:** 30 min **total cumulative** for in-sprint fixes before close. Human-overridable ad hoc per §2.2.

---

## 3. What's NOT Changing

These are preserved exactly as-is:
- **FOUNDATION_MANUAL core invariants** (truthful UX, workspace isolation, CI discipline, manual mode gating, layer separation)
- **Evidence capture protocol** (RunTrace IDs for behavior changes)
- **Review artifacts folder** (`artifacts/` inside sprint folders) — traces, logs, evidence outputs stay
- **ADR process** (lightweight, pays for itself)
- **1-commit-per-AF discipline**
- **1-PR-per-sprint discipline**
- **CI gate before commit** (ruff, pytest, coverage)
- **Sprint description as single source of sprint truth**
- **Autonomy gates** (kept as-is; genericization deferred to deployable sprint)
- **Existing file names** — all files created before this plan keep their current names

**Sprint execution note:** This governance simplification sprint runs under the **old rules** (current SPRINT_MANUAL). The first sprint under the new rules is the next coding sprint, which serves as the validation.

---

## 4. Action Features (AFs) — Scope & Sequence

### AF Overview

| Order | ID | Priority | Title | Phase | Dependencies |
|:--:|---:|:--:|---|:--:|---|
| 1 | AF-0129 | P0 | Eliminate filename-status coupling | 1 | — |
| 2 | AF-0130 | P1 | Drop redundant sprint artifacts | 2 | — |
| 3 | AF-0131 | P1 | Template enhancements: time, model, docs impact & decision capture | 4 | — |
| 4 | AF-0132 | P1 | HITL framework in governance docs | 5 | — |
| 5 | AF-0133 | P1 | Copilot instructions: ToDo discipline | 6 | — |
| 6 | AF-0134 | P1 | Streamline INDEX files | 3 | AF-0129 |
| 7 | AF-0135 | P2 | Governance automation script (`gov.py`) | 7 | AF-0129, AF-0134 |
| 8 | AF-0136 | P1 | Governance docs consolidation (SPRINT_MANUAL, ADR-0010, README) | 8 | All above |

### Execution Sequence

```
              ┌─ AF-0129 (filenames) ─────┐
              │                            ├─→ AF-0134 (INDEX) ─→ AF-0135 (gov.py) ─┐
              ├─ AF-0130 (artifacts) ──────┘                                         │
 Start ──→    ├─ AF-0131 (templates) ─────────────────────────────────────────────────┼─→ AF-0136 (docs)
              ├─ AF-0132 (HITL) ──────────────────────────────────────────────────────┘
              └─ AF-0133 (Copilot) ───────────────────────────────────────────────────┘
```

**Parallelizable:** AF-0129 through AF-0133 have no mutual dependencies.
**Sequential:** AF-0134 depends on AF-0129. AF-0135 depends on AF-0129 + AF-0134. AF-0136 depends on all.

---

## 5. AF Specifications

---

### AF-0129 — Eliminate Filename-Status Coupling
**Priority:** P0 | **Phase:** 1 | **Dependencies:** None | **Area:** Process / Docs

#### Problem
Every status change requires **3 synchronized edits**: (1) rename file to change status token, (2) update internal `Status:` metadata field, (3) update INDEX row. This is the #1 source of bugs (BUG-0022, BUG-0023) and the biggest ceremony time sink. The SPRINT_MANUAL §2.2, §2.3, §7.1, §8.4 all exist to manage this coupling.

#### Goal
- **New files** use immutable filenames without status tokens: `AF0129_eliminate_filename_status.md`
- **Existing files** keep their current names — no retroactive renames. Evolution is visible in the file system.
- Status lives in exactly **2 places**: internal file metadata + INDEX row
- Status changes require exactly **2 edits** (file metadata + INDEX), zero renames
- ADRs already follow this pattern — align new AF and BUG files to match

#### Changes
1. **New naming convention (for new files only):**
   - AF files: `AF####_<three_word_description>.md` (no status token)
   - BUG files: `BUG####_<three_word_description>.md` (no status token)
   - ADR files: unchanged (already `ADR###_<description>.md`)
2. **Existing files are NOT renamed** — old-convention files coexist with new-convention files
3. **INDEX files support both conventions** — old links point to old filenames, new entries use new format
4. **Update `test_documentation_drift.py`** if it validates filename patterns (must accept both conventions)
5. **Update SPRINT_MANUAL for new files:**
   - §2.2: New naming convention for new files; note that existing files keep old names
   - §2.3: Renaming on Status Change — removed for new files (status not in filename)
   - §7.1: Post-merge — no rename step for new files
   - §8.4: Status Mismatch Scan — only applies to legacy files created before this change

#### Acceptance Criteria
- [ ] New AF/BUG files created after this AF do NOT contain status tokens in filename
- [ ] Existing files remain untouched (old names preserved)
- [ ] All INDEX links resolve to existing files (both old and new convention)
- [ ] `pytest tests/test_documentation_drift.py` passes
- [ ] SPRINT_MANUAL updated with new naming convention for new files
- [ ] FOLDER_STRUCTURE updated to document both conventions (legacy + new)

#### Files Touched
- `docs/dev/foundation/SPRINT_MANUAL.md` (§2.2, §2.3, §7.1, §8.4)
- `docs/dev/foundation/FOLDER_STRUCTURE_0.2.md` (naming convention — add new convention)
- `tests/test_documentation_drift.py` (if filename pattern enforced — accept both conventions)

#### Risk
**Low.** No file renames, no INDEX rewrite. Only documentation and test updates. New convention validated on first new AF created.

---

### AF-0130 — Drop Redundant Sprint Artifacts
**Priority:** P1 | **Phase:** 2 | **Dependencies:** None | **Area:** Process / Docs

#### Problem
`S##_PR_01.md` duplicates the GitHub PR body. `S##_REVIEW_01.md` with its 46-item checklist duplicates the checks already mandated by SPRINT_MANUAL §8 (Sprint Close Ritual) and §9 (Autonomy Gate). For a solo-developer project, the review document is pure ceremony — the review IS the PR merge.

#### Goal
- GitHub PR is the canonical PR artifact (no separate file)
- Review functions are absorbed into S##_DESCRIPTION.md and SPRINT_MANUAL
- Sprint folder contains: `S##_DESCRIPTION.md` + `artifacts/` (no PR or review docs)
- Review rigor is preserved — same checks, fewer files

#### Changes
1. **Rewrite `SPRINT_DESCRIPTION_TEMPLATE.md`** — streamlined format:
   - Sprint metadata (goal, scope, dates, branch, models)
   - Work items table (filled during sprint)
   - Close section:
     - Review decision: `ACCEPTED` / `ACCEPT WITH FOLLOW-UPS` / `REJECTED`
     - Rationale (1–2 sentences)
     - Follow-ups (AF IDs, if any)
     - PR link
   - Sprint Cognitive Health (close — seven fields):
     - Collapse events (INCOMPLETE_IMPL follow-ups): [N]
     - Drift events (AF spec revised mid-implementation): [N, list AF IDs]
     - Repair events: [informal, e.g. "3 attempts on BUG-0019"]
     - Agent-initiated HITL gates: [G codes, or "none"]
     - Negative test coverage added: [yes / no / partial]
     - LLM avoidance events: AFs claiming AI functionality with no RunTrace evidence of a real LLM call [N, list AF IDs]
     - Integration coverage: E2E test result at sprint close [pass / partial / fail — categorise any failures as unit-level vs. component-boundary wiring]
   - Learnings (optional, 2–3 bullets)
2. **Archive** `SPRINT_PR_TEMPLATE.md` and `REVIEW_TEMPLATE.md` (move to `templates/archived/`)
3. **Update SPRINT_MANUAL:**
   - §6: Reference GitHub PR directly, remove S##_PR_01 creation steps
   - §7: Remove post-merge doc creation
   - §8: Add review decision rules (ACCEPTED / ACCEPT WITH FOLLOW-UPS / REJECTED)
   - §8: Add quickfix budget rule (30 min cumulative, human-overridable)
4. **Review function mapping** (how each check migrates):

| Review function | Old home | New home |
|---|---|---|
| CI gate | REVIEW_01 checklist | SPRINT_MANUAL §8 (unchanged) |
| INDEX consistency | REVIEW_01 checklist | SPRINT_MANUAL §8 + `gov.py check` |
| Evidence verification | REVIEW_01 checklist | S##_DESCRIPTION close section |
| Autonomy gate | REVIEW_01 checklist | SPRINT_MANUAL §9 (unchanged) |
| Decision record | REVIEW_01 summary | S##_DESCRIPTION close section |
| Follow-up items | REVIEW_01 action items | Filed as new AF/BUG items |

5. **Historical files untouched** — S01-S15 PR and review docs remain as-is

#### Acceptance Criteria
- [ ] New `SPRINT_DESCRIPTION_TEMPLATE.md` includes close/review section
- [ ] New `SPRINT_DESCRIPTION_TEMPLATE.md` includes Sprint Cognitive Health section (seven fields)
- [ ] `SPRINT_PR_TEMPLATE.md` and `REVIEW_TEMPLATE.md` moved to `templates/archived/`
- [ ] SPRINT_MANUAL §6–§8 updated — no references to S##_PR_01 or S##_REVIEW_01 creation
- [ ] Sprint 16 (or next sprint) successfully uses new template

#### Files Touched
- `docs/dev/sprints/templates/SPRINT_DESCRIPTION_TEMPLATE.md` (rewrite)
- `docs/dev/sprints/templates/SPRINT_PR_TEMPLATE.md` (archive)
- `docs/dev/sprints/templates/REVIEW_TEMPLATE.md` (archive)
- `docs/dev/foundation/SPRINT_MANUAL.md` (§6, §7, §8)

#### Risk
**Low.** Template change only. Historical files untouched. Validated on next sprint.

---

### AF-0131 — Template Enhancements: Time, Model, Docs Impact & Decision Capture
**Priority:** P1 | **Phase:** 4 | **Dependencies:** None | **Area:** Process / Docs

#### Problem
Timing data relies solely on git timestamps, which miss workflow disruptions (context switches, offline discussions, re-reads). Model provenance is not tracked at all — critical data for a system intended to be deployable with different AI models. Documentation drift happens because no AF template prompts the implementer to check whether surface-level docs (README, ARCHITECTURE, CLI_REFERENCE) need updating. Architectural decisions made inside AFs are lost because the AF template has no decision capture section.

#### Goal
- Every AF, sprint, bug, and ADR records who (which model) worked on it and when
- Timestamps capture actual work boundaries, not file creation time
- Git timestamps remain as another data source
- Every AF includes a mandatory docs impact check (prevents drift)
- Architectural decisions made within an AF are captured inline (prevents ADR gaps)

#### Changes
1. **AF template** — add metadata fields:
   - `Started:` — ISO 8601 datetime, logged when agent begins work
   - `Completed:` — ISO 8601 datetime, logged when AF marked DONE
   - `Models:` — comma-separated list, e.g. `Claude Opus 4 (Copilot)`
2. **AF template** — add **Docs Impact Check** acceptance criterion:
   ```
   - [ ] Docs impact checked: README / CLI_REFERENCE / ARCHITECTURE (updated or N/A)
   ```
   The agent checks at AF completion: "Did this AF change CLI commands? Update CLI_REFERENCE. Change architecture? Update ARCHITECTURE.md. Change project structure? Update README." If none apply, mark N/A. Cost: ~30 seconds. Prevention: drift.
2b. **AF template** — add **AI Functionality Check** acceptance criterion (conditional):
   ```
   - [ ] AI functionality check: if this AF delivers or modifies AI functionality (LLM calls, planner, orchestrator, verifier), RunTrace evidence of a real LLM call is required (N/A if no AI functionality)
   ```
   Catches LLM Avoidance — the pattern where an AF claims AI functionality but the implementation is a structural shell with no actual LLM call. Cost: zero if N/A; one RunTrace reference if applicable.
3. **AF template** — add **Decision Record** section (optional, filled when applicable):
   ```
   ## Decision Record (if applicable)
   - **Decision:** What was decided?
   - **Alternatives considered:** What else was possible?
   - **Rationale:** Why this choice?
   ```
   This captures decisions *where the work happens*. Full ADRs (separate files) are reserved for cross-cutting decisions per the criteria defined in AF-0136.
4. **Sprint description template** — add:
   - `Started:` / `Completed:` datetimes
   - `Models:` list
5. **Bug report template** — add: `Models:`
6. **ADR template** — add: `Models:`
7. **Convention:** `gov.py new-af` leaves `Started:` blank — it is filled by the agent at the moment implementation of *that specific AF* begins, not at file creation. AF files may be created at sprint kickoff for the entire sprint scope; `Started:` is logged per-AF when the agent picks it up. `Completed:` is logged when acceptance criteria are met, just before the commit. The `Started:`→`Completed:` span is the per-AF active implementation duration: the smallest measurable velocity unit in the system.

#### Acceptance Criteria
- [ ] All four templates include `Started:`, `Completed:`, and `Models:` fields
- [ ] AF template includes Docs Impact Check as a standard acceptance criterion
- [ ] AF template includes AI Functionality Check (conditional — N/A if no AI functionality delivered)
- [ ] AF template includes Decision Record section (marked "if applicable")
- [ ] Format convention documented: ISO 8601 (e.g. `2026-04-03T14:30:00+02:00`)
- [ ] Model format: `<Model Name> (<Tool/Platform>)` — e.g. `Claude Opus 4 (Copilot)`

#### Files Touched
- `docs/dev/backlog/templates/BACKLOG_ITEM_TEMPLATE.md`
- `docs/dev/sprints/templates/SPRINT_DESCRIPTION_TEMPLATE.md`
- `docs/dev/bugs/templates/BUG_REPORT_TEMPLATE.md`
- `docs/dev/decisions/templates/ADR_TEMPLATE.md`

#### Risk
**Low.** Additive metadata fields and sections. No breaking changes.

---

### AF-0132 — HITL Framework in Governance Docs
**Priority:** P1 | **Phase:** 5 | **Dependencies:** None | **Area:** Process / Governance

#### Problem
Human decision points and rights are implicit, scattered across SPRINT_MANUAL sections. No single reference exists for when the agent must stop, what the human can override, and how ad hoc decisions interact with documented rules.

#### Goal
- Single authoritative section codifying all HITL gates, rights, and the constitutional principle
- Clear distinction between temporary (chat) and permanent (AF) governance changes
- Agent and human both know exactly where authority boundaries lie

#### Changes
1. Add **HITL Framework** as a new section in FOUNDATION_MANUAL (§1.7 or new top-level section)
2. Content as specified in Section 2 of this document:
   - All 15 mandatory gates (G1–G15) in numbered table
   - Escalation procedure (document → propose options → recommend → wait)
   - Human rights table (4 rights)
   - Constitutional principle (chat = temporary amendment)
   - Review decisions table (ACCEPTED / ACCEPT WITH FOLLOW-UPS / REJECTED)
   - Quickfix budget rule (30 min cumulative, human-overridable)

#### Acceptance Criteria
- [ ] HITL Framework section exists in FOUNDATION_MANUAL
- [ ] All 15 mandatory gates documented (G1–G15)
- [ ] Escalation procedure documented
- [ ] All four human rights documented
- [ ] Constitutional principle stated verbatim
- [ ] Review decision table with all three outcomes
- [ ] SPRINT_MANUAL references HITL section for decision points

#### Files Touched
- `docs/dev/foundation/FOUNDATION_MANUAL.md` (new section)
- `docs/dev/foundation/SPRINT_MANUAL.md` (cross-references)

#### Risk
**Low.** Additive documentation. Formalizes existing practice.

---

### AF-0133 — Copilot Instructions: ToDo List Discipline
**Priority:** P1 | **Phase:** 6 | **Dependencies:** None | **Area:** Process / Tooling

#### Problem
No standardized task tracking per AF during implementation. Copilot creates ad hoc task lists without consistent AF identification.

#### Goal
- Every AF gets a ToDo checklist with the AF ID clearly in the title
- Instruction is persistent across sessions via project-level Copilot config

#### Changes
1. Create or update `.github/copilot-instructions.md` with:
   - ToDo list discipline: create a ToDo checklist for each AF
   - Title format: `AF-0129: Eliminate Filename-Status Coupling`
   - Mark in-progress before starting, completed immediately after finishing
2. Include any other project-specific Copilot instructions discovered during implementation

#### Acceptance Criteria
- [ ] `.github/copilot-instructions.md` exists with ToDo discipline rule
- [ ] Next AF executed by Copilot creates a properly titled ToDo list
- [ ] Validated across at least 2 consecutive AFs in the first sprint under new rules

#### Files Touched
- `.github/copilot-instructions.md` (create or update)

#### Risk
**Low.** Configuration file only.

---

### AF-0134 — Streamline INDEX Files
**Priority:** P1 | **Phase:** 3 | **Dependencies:** AF-0129 (naming convention must be settled) | **Area:** Process / Docs

#### Problem
INDEX files are cluttered with redundant columns (Filename duplicates the link) and require moving rows between Active/Done sections on every status change. With ~115 rows in INDEX_BACKLOG, this is increasingly error-prone.

#### Goal
- Leaner INDEX tables — fewer columns, no section shuffling
- Status changes require updating the Status cell only (no row moves)
- Links serve as the sole file reference (no separate Filename column)

#### Changes
1. **INDEX_BACKLOG.md:**
   - Remove `Filename` column — the link column (`[🔗]()` / `[✅]()`) is the file reference
   - Remove Active/Done section splitting — single table per sprint, `Status` column is the filter
   - Keep sprint grouping (one table per sprint) for readability
   - Simplify columns to: `Order | ID | Priority | Status | Title | Area | Owner | Link`
2. **INDEX_BUGS.md:**
   - Same simplification: remove Filename column, single table, Status as filter
   - Columns: `ID | Severity | Status | Title | Area | Link`
3. **INDEX_SPRINTS.md:** Already lean — no changes needed
4. **INDEX_DECISIONS.md:** Already lean — minimal changes (remove Filename if present)

#### Acceptance Criteria
- [ ] INDEX_BACKLOG has no `Filename` column
- [ ] INDEX_BACKLOG has no Active/Done section split (single table per sprint)
- [ ] INDEX_BUGS has no `Filename` column
- [ ] All links in INDEX files resolve to existing files
- [ ] `test_documentation_drift.py` passes
- [ ] No broken inbound links to INDEX from SPRINT_MANUAL, README, or sprint descriptions

#### Files Touched
- `docs/dev/backlog/INDEX_BACKLOG.md` (restructure)
- `docs/dev/bugs/INDEX_BUGS.md` (restructure)
- `docs/dev/decisions/INDEX_DECISIONS.md` (minor cleanup if needed)

#### Risk
**Medium.** Structural change to INDEX files, but content is preserved. All changes are mechanical.

---

### AF-0135 — Governance Automation Script (`gov.py`)
**Priority:** P2 | **Phase:** 7 | **Dependencies:** AF-0129, AF-0134 | **Area:** Process / Tooling

#### Problem
All ceremony is manual. Even with simplified naming (AF-0129) and streamlined INDEX (AF-0134), creating a new AF or updating a status involves multiple file edits.

#### Goal
- Optional CLI helper that automates the most common governance operations
- Reduces per-status-change from 2 manual edits to 1 command
- Provides a validation command to catch inconsistencies early

#### Changes
1. Create `scripts/gov.py` (~150–200 lines, stdlib + argparse only):

| Command | Action |
|---|---|
| `gov.py new-af 0129 "Description" --priority P1 --sprint 16` | Creates AF file from template + adds INDEX row + sets `Started:` timestamp |
| `gov.py new-bug 0025 "Description" --severity P1` | Creates bug file from template + adds INDEX row |
| `gov.py status af 0129 DONE` | Updates internal `Status:` field + INDEX row + sets `Completed:` if DONE |
| `gov.py check` | Validates: all INDEX links resolve, all internal statuses match INDEX, no orphans, no phantoms. Warns on cognitive health thresholds: collapse events > 2, agent-initiated gates = "none" for 2 consecutive sprints, or LLM avoidance events > 0 |
| `gov.py follow-up 0129 "Follow-up description"` | Creates follow-up AF (for ACCEPT WITH FOLLOW-UPS workflow) |

2. **Manual editing remains a valid fallback** — the script is a convenience, not a gate
3. **No auto-commit** — git operations stay manual for safety
4. **No external dependencies** — stdlib only (pathlib, argparse, re, datetime)

#### Acceptance Criteria
- [ ] `python scripts/gov.py check` passes on current repo state
- [ ] `python scripts/gov.py new-af` creates correct file + correct INDEX entry
- [ ] `python scripts/gov.py status` updates both file and INDEX correctly
- [ ] Script has `--help` for all subcommands
- [ ] Zero external dependencies
- [ ] `gov.py check` produces no false positives on legacy-format filenames (pre-AF-0129 convention)

#### Files Touched
- `scripts/gov.py` (new)

#### Risk
**Low.** Optional tooling. Does not change any governance rules. Manual workflow remains valid.

---

### AF-0136 — Governance Docs Consolidation
**Priority:** P1 | **Phase:** 8 | **Dependencies:** All above (AF-0129 through AF-0135) | **Area:** Process / Docs

#### Problem
After Phases 1–7, the governance docs (SPRINT_MANUAL, FOLDER_STRUCTURE, README) reference old conventions. They need a consolidation pass to reflect the new reality.

#### Goal
- All governance docs internally consistent with new rules
- ADR-0010 records the governance simplification decision for traceability
- README reflects actual project state (currently 3 phases stale)
- Sprint close ritual includes living reference docs sweep
- ADR creation criteria formalized (inline vs. full ADR)

#### Changes
1. **SPRINT_MANUAL.md** — full rewrite of affected sections:
   - §0: Add HITL cross-reference
   - §2: Remove file-rename protocol, update naming convention
   - §3: Simplify INDEX update protocol (2 places, not 3)
   - §6: Simplify PR protocol (GitHub PR only, no S##_PR_01)
   - §7: Simplify post-merge (no rename step, just status update)
   - §8: Replace sprint close ritual (no mismatch scan, add review decision rules)
   - §8: Add **living reference docs sweep** — at sprint close, check if the sprint touched areas covered by these docs and update if needed:
     - `SCHEMA_INVENTORY.md` — if schemas changed
     - `CONTRACT_INVENTORY.md` — if contracts changed
     - `SKILLS_ARCHITECTURE_0.1.md` — if skill framework changed
     - `ARCHITECTURE.md` — if architecture changed (Implementation Map)
     - `CLI_REFERENCE.md` — if CLI commands changed
     - `README.md` — if project structure or capabilities changed
   - §8: Add **ADR creation criteria**:
     - **Inline Decision Record** (in AF template): Single-AF scope. Captured where the work happens.
     - **Full ADR** (separate file): Affects 2+ modules, sets a reusable pattern, or constrains future work.
   - Add new section **§X: Inter-Sprint Planning Commits** — lightweight convention for docs-only artifacts created between sprints (planning docs, analyses, backlog scoping). Rules:
     - Housekeeping branch + minimal PR (one-line description). No sprint structure, no AFs.
     - Commit message format: `docs: <description>`
     - Scope: docs-only changes. Any change touching `src/`, `tests/`, or `scripts/` requires a sprint.
     - Must be merged to main before next sprint branch is created.
2. **FOLDER_STRUCTURE_0.3.md** (new) — updated naming conventions, simplified sprint folder structure
3. **ADR-0010** — "Governance Simplification" decision record:
   - Context: 15 sprints of evidence, ceremony overhead data
   - Decision: eliminate filename-status coupling, drop PR/review docs, add HITL, add time/model logging
   - Consequences: reduced overhead, simpler onboarding, automation opportunity
4. **README.md** — update project structure section, test count, coverage
5. **ARCHITECTURE.md** — verify Implementation Map is current; update if stale

#### Acceptance Criteria
- [ ] No references to old naming convention (`AF####_<STATUS>_desc.md`) in SPRINT_MANUAL
- [ ] No references to S##_PR_01 or S##_REVIEW_01 creation in SPRINT_MANUAL
- [ ] ADR-0010 exists with ACCEPTED status in INDEX_DECISIONS
- [ ] FOLDER_STRUCTURE_0.3.md exists and is internally consistent
- [ ] README project structure matches reality
- [ ] SPRINT_MANUAL §8 includes living reference docs sweep checklist
- [ ] SPRINT_MANUAL §8 includes ADR creation criteria (inline vs. full)
- [ ] ARCHITECTURE.md Implementation Map reflects current codebase

#### Files Touched
- `docs/dev/foundation/SPRINT_MANUAL.md` (rewrite affected sections)
- `docs/dev/foundation/FOLDER_STRUCTURE_0.3.md` (new)
- `docs/dev/decisions/files/ADR010_governance_simplification.md` (new)
- `docs/dev/decisions/INDEX_DECISIONS.md` (add ADR-0010 row)
- `README.md` (update project structure, test count, coverage)
- `ARCHITECTURE.md` (verify and update Implementation Map)

#### Risk
**Low.** Documentation-only. Validated by full read-through.

---

## 6. Decisions Log

| # | Decision | Rationale |
|---|---|---|
| D1 | **No batch rename** — existing files keep old names, new files use new convention | Preserve history; evolution visible in file system; zero blast radius |
| D2 | 30 min total cumulative quickfix budget, human-overridable | Prevents scope creep while respecting human authority |
| D3 | REJECTED = branch preserved, human decides next step | Maximum flexibility; no destructive auto-undo |
| D4 | ACCEPT WITH FOLLOW-UPS = auto-create follow-up AFs and follow up sprint table | Ensures nothing falls through the cracks |
| D5 | Chat = temporary amendment, not permanent governance change | Preserves documented governance integrity while enabling flexibility |
| D6 | `gov.py`: argparse, stdlib only, no auto-commit | Minimal dependencies; git operations stay under human control |
| D7 | Model field format: `<Model Name> (<Platform>)` | E.g. `Claude Opus 4 (Copilot)` — traceable across tools |
| D8 | Historical files (S01–S15) untouched | No retroactive cleanup; clean break going forward |
| D9 | Deployable template kit: separate follow-up sprint | Validate improvements first by running a real sprint under new rules |
| D10 | Template versions bump to v0.3 | Tracks the governance generation |
| D11 | This sprint runs under **old rules** | Can't reliably use rules you're still writing; next sprint validates new rules |
| D12 | Autonomy gates stay as-is; genericized in deployable sprint | Current project needs them; others may not — defer to template kit |
| D13 | Docs Impact Check in AF template | ~30 sec cost per AF; prevents documentation drift (README 3 phases stale, inventory docs 1 month stale) |
| D14 | Sprint-close sweep for living reference docs | Catches drift that individual AF checks miss; 6 docs checked only when relevant areas touched |
| D15 | ADR criteria: inline Decision Record for single-AF scope, full ADR for cross-cutting | Inline = no overhead; full ADR when affects 2+ modules, sets reusable pattern, or constrains future work |
| D16 | CLI_REFERENCE abstraction deferred to deployable sprint | Not every project has a CLI; needs Reference Docs Registry concept (opt-in mechanism) |
| D17 | Inter-sprint planning commits via housekeeping branch + minimal PR | Docs-only; no sprint apparatus needed; must merge before next sprint starts |
| D18 | Sprint Cognitive Health section in sprint description template | Captures 7 failure mode signals from existing artifacts; enables longitudinal analysis without external tooling; `gov.py check` warns on threshold violations |
| D19 | LLM Avoidance and Partial Wiring added to Cognitive Health in v0.1, not deferred | Both failure modes empirically confirmed across 15 sprints (planner went 10 sprints without an LLM call; partial wiring was the largest single bug category). Instrument immediately to get data from first sprint under new rules rather than waiting for a v0.2 iteration |

---

## 7. Scope Boundaries

### In Scope
- Governance docs (SPRINT_MANUAL, FOUNDATION_MANUAL, FOLDER_STRUCTURE)
- File naming conventions (AF, BUG filenames)
- INDEX files (restructure)
- Sprint templates (DESCRIPTION, PR, REVIEW)
- All four metadata templates (AF, Sprint, Bug, ADR)
- HITL framework
- Copilot instructions
- Automation script (`gov.py`)
- ADR-0010
- README update

### Out of Scope
- Runtime code changes (no `src/ag/` modifications except `test_documentation_drift.py`)
- FOUNDATION_MANUAL core invariants (§1.1–§1.6)
- ADR process itself (structurally unchanged)
- Historical sprint files (S01–S15 untouched)
- Deployable template kit (deferred to follow-up sprint)

---

## 8. Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|---|---|---|---|
| Two naming conventions coexist (old + new) | Low | Certain | Documented in FOLDER_STRUCTURE; INDEX accepts both; `gov.py check` validates both |
| INDEX restructure introduces broken links | Medium | Medium | `gov.py check` + `test_documentation_drift.py` as validation |
| New template fields forgotten mid-sprint | Low | Medium | Copilot instructions enforce; `gov.py` auto-populates |
| `gov.py` becomes a maintenance burden | Low | Low | Minimal scope (~200 lines), stdlib only, optional tooling |
| New rules untested during this sprint | Low | Low | Deliberate choice (D11); validated on next coding sprint |

---

## 9. Estimated Savings (Post-Implementation)

| Activity | Before | After | Saving |
|---|---|---|---|
| Per status change (new files) | 3 edits (rename + metadata + INDEX) | 2 edits (metadata + INDEX), or 1 command via `gov.py` | 33–66% |
| Per status change (legacy files) | 3 edits (rename + metadata + INDEX) | 3 edits (unchanged — legacy convention) | 0% |
| Sprint close ceremony | ~20 min (PR doc + review doc + INDEX alignment) | ~5 min (fill description close section + merge PR) | 75% |
| Per-sprint total ceremony | 30–50 min | ~10 min | 66–80% |
| Status mismatch debugging (new files) | Ad hoc (BUG-0022, BUG-0023) | Eliminated (status not in filename) | 100% |

---

## 10. Deferred: Deployable Template Kit (Future Sprint)

After validating the improvements by running the next coding sprint under new rules:
- Extract generalized governance template (remove project-specific references)
- Package as standalone starter kit for human operators
- Include `gov.py`, all templates, HITL framework, SPRINT_MANUAL
- Document setup and customization guide

### Deferred AF: Depersonalize & Genericize Gates

**Problem:** The current governance system uses project-specific names (Kai, Jeff, Jacob) and project-specific gate types ("Autonomy Gate" for AI runtime). This prevents reuse by other teams building different products.

**Goal:**
- Replace all personal name references with role-based references (e.g., `Product Owner`, `Tech Lead`, `Implementer`)
- Rename "Autonomy Gate" to a generic **optional gate** system — gates can be enabled/disabled per project
- Implement gate configuration: each project declares which gates are active in a config section
- Preserve the HITL framework as a universal component (gates G1–G7 are universal; G8–G15 are project-configurable)

---

### Deferred AF: Abstract Project-Specific Reference Docs

**Problem:** The Docs Impact Check (AF-0131) and sprint-close sweep (AF-0136) reference project-specific docs like `CLI_REFERENCE.md`. Not every project has a CLI — this hard-coded list prevents reuse by other teams.

**Goal:**
- Define a **Reference Docs Registry** — an opt-in mechanism where each project declares which living reference docs it maintains
- Standard docs (README, ARCHITECTURE) are always included
- Project-specific docs (CLI_REFERENCE, SKILLS_ARCHITECTURE, etc.) are registered per project
- Docs Impact Check and sprint-close sweep read from the registry instead of a hard-coded list

**Changes:**
- Design registry format (e.g., a section in FOUNDATION_MANUAL or a simple config file)
- Update Docs Impact Check to reference registry
- Update sprint-close sweep to reference registry
- Template kit ships with only universal docs; project-specific docs are opt-in

---

### Scope check for deployable sprint (both deferred AFs)
- Audit all governance docs for personal names and project-specific terminology
- Create role mapping table (Kai → Product Owner, Jeff → Tech Lead, Jacob → Implementer)
- Design gate enable/disable mechanism
- Design Reference Docs Registry format
- Extract template kit with placeholder roles, configurable gates, and registry-based doc checks
