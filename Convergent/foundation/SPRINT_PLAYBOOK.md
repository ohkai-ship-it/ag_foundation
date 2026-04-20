# SPRINT PLAYBOOK
#### Description: Deterministic step-by-step operational script that turns Governance Standard rules into executable actions. Covers all six lifecycle phases: Planning (P1), Start (P2), Implementation (P3), Review (P4), Sprint End (P5), and Inter-Sprint (P6). Each phase defines steps, tasks, and gates with severity levels and required actions. Rules and rationale live in the Governance Standard; project-specific values are resolved through GS §IM08.
#### Convergent: v1.3.2
#### governs: ag_foundation

This document is a deterministic step-by-step operational script.
It contains zero ambiguity. Follow each step exactly.

Rules and rationale live in `GOVERNANCE_STANDARD.md`. Project-specific values
(CI commands, coverage thresholds, workspace boundaries) are resolved through
GS §IM08. This playbook references GS sections only (GS §X).
Do not duplicate rules here.

> **HITL gates** are marked inline with their ID, severity, and required action.
> Gate definitions: GS §IM04. Human rights: GS §IM06.
> Gate severity labels: GS §DS04.

---
## Phases
### Phase 1: Sprint Planning

#### 1.1 Gate P1: Additional

HITL initiates sprint planning. Agent may assist but HITL owns scope decisions.

#### 1.2 Step: Scoping

##### 1.2.1 Task: Review backlog

- Review `docs/INDEX_BACKLOG.md` — identify candidate AFs
- Review `docs/INDEX_BUGS.md` — identify candidate BUGs
- Review `docs/INDEX_DECISIONS.md` — check for pending ADRs
- Consider follow-ups from previous sprint review decisions

HITL decides sprint scope, priorities, and execution order.

#### 1.3 Step: Create sprint docs

##### 1.3.1 Task: Create sprint and artifacts folder

Create sprint folder using naming convention:
```
docs/files/sprints/S##/
docs/files/sprints/S##/artifacts

```

##### 1.3.2 Task: Use templates to build sprint description, review and PR files

Create these files from templates:
- `S##_DESCRIPTION.md` ← `foundation/templates/SPRINT_DESCRIPTION_TEMPLATE.md`
- `S##_REVIEW.md` ← `foundation/templates/SPRINT_REVIEW_TEMPLATE.md`
- `S##_PULL_REQUEST.md` ← `foundation/templates/PULL_REQUEST_TEMPLATE.md`

Fill out all sections applicable for pre-sprint start:
- Sprint goal (one sentence, outcome-focused)
- Scope table (P0/P1/P2 items with AF IDs and owners)
- Execution sequence (ordered list of AFs)
- Non-goals
- Risk assessment

#### 1.4 Gate G1: Additional

Present planning artifacts to HITL. Ask: "Approve planning commit?"

#### 1.5 Step: Commit

```bash
git add <planning files>
git commit -m "chore: sprint ## planning — <description>"
```

Update `docs/INDEX_SPRINTS.md` with new sprint entry.

---

### Phase 2: Sprint Start

#### 2.1 Gate P2: Critical

This is the readiness gate. Agent reads all governance and sprint documents before proceeding.

#### 2.2 Step: Read & verify

##### 2.2.1 Task: Mandatory reads

Read these documents completely before starting:
1. `foundation/GOVERNANCE_STANDARD.md`
2. `foundation/SPRINT_PLAYBOOK.md` (this document)
3. Consumer-specific project control documents (see GS §IM08)
4. Sprint description file (`S##_DESCRIPTION.md`)
5. All AF files referenced in sprint scope
6. All INDEX files:
   - `docs/INDEX_BACKLOG.md`
   - `docs/INDEX_BUGS.md`
   - `docs/INDEX_DECISIONS.md`
   - `docs/INDEX_SPRINTS.md`

##### 2.2.2 Task: Pre-sprint checklist

- [ ] Sprint scope matches INDEX entries
- [ ] All AF statuses are `READY` (not `PROPOSED`)

> Transition T1 (PROPOSED → READY) fires at G1. See GS §IM07.4.
- [ ] Naming conventions applied to all files
- [ ] No filename ↔ status mismatches

**Sprint Start Ownership:**

| Owner | Responsibility |
|-------|---------------|
| HITL | Create AFs (Status = READY), create sprint description, define sprint ID + name, assign agents (GS §IM03.2) |
| Agent-I | Read sprint description, check AFs, ask questions, create branch, create sprint folder, update ALL INDEX files |
| Agent-C | Available for governance/architecture AFs if assigned by HITL |

##### 2.2.3 Task: Baseline manifest check

Count files in each artifact folder and compare against the expected baseline.
Expected counts come from the sprint description or the previous sprint's verified counts.

| Category | Path | Expected | Actual |
|----------|------|:--------:|:------:|
| Backlog items | `docs/files/backlog/` | ___ | ___ |
| Bug reports | `docs/files/bugs/` | ___ | ___ |
| ADR files | `docs/files/decisions/` | ___ | ___ |
| Sprint folders | `docs/files/sprints/` | ___ | ___ |

**If any count mismatches: STOP → escalate (E7 — blocking dependency).**
Do not proceed to branch creation or AF work until the mismatch is resolved.

Present verification summary (including manifest counts) to HITL.

#### 2.3 Step: Agent actively asks questions

If anything is unclear about scope, execution order, constraints, or expected outcomes — ask now. This is the designated time for clarifying questions before implementation begins.

#### 2.4 Gate O1: Normal — Questions

Present questions to HITL. Receive answers before proceeding.
If no questions: state "No questions — ready to proceed."

#### 2.5 Gate G2: Additional

Ask: "May I create the sprint branch and begin implementation?"
**Do NOT proceed until explicit approval.**

#### 2.6 Step: Branch creation

```bash
git checkout main
git pull origin main
git checkout -b <branch-type>/<short-name>
```

Branch types: `feat/`, `fix/`, `chore/` (see GS §DS01).

Verify:
- [ ] Working directory clean
- [ ] On correct branch
- [ ] Branch name follows convention

Update `docs/INDEX_SPRINTS.md` status to `In Progress`.

Commit sprint start:
```bash
git add <files>
git commit -m "chore: sprint ## start — branch created, INDEX_SPRINTS → In Progress"
```

---

### Phase 3: Implementation

#### 3.1 Gate P3: Normal — Phase entry

All AFs are `READY`. Branch exists. Verification complete.

> **Loop:** Repeat Steps 3.3–3.7 for each AF in execution order.
> On iteration 1, P3 entry and O2 are the same gate.
> On iteration 2+, O2 opens the next AF loop without re-entering P3.

#### 3.2 Gate O2: Normal — AF iteration start

Present which AF is next. Ask: "Proceed with AF-####?"

#### 3.3 Step: Implement

- Make atomic, reversible changes
- Do not mix unrelated changes
- If blocked → escalate (GS §PO03, gate E3/E6/E7)

#### 3.4 Step: Evidence capture

**Code projects:**
- Run targeted tests for this AF only
- Capture test output and coverage for changed modules

**Docs-only projects:**
- Cross-reference edits against canonical sources
- Verify INDEX consistency for affected entries

#### 3.5 Step: C1 — Targeted CI Checkpoint

**Code projects:** Run targeted tests per GS §PO07. Run only the tests relevant to this AF. Do NOT run the full suite per commit.

**Docs-only projects:**
- Verify affected INDEX entries match internal `Status:` fields
- Verify file existence for affected entries
- Verify naming compliance for new files

#### 3.6 Gate G3: Normal — AF commit

Present AF summary to HITL:
- Files changed
- Key decisions made
- Evidence/verification results

Ask: "Approve AF-#### commit?"

#### 3.7 Step: Commit

After G3 approval:
```bash
git add <files>
git commit -m "<type>(AF-####): <description>"
```

Update AF status to `DONE` (internal `Status:` field + INDEX row).

> Transition T4 (READY → DONE) fires at G3 for AFs/BUGs. See GS §IM07.4.

> **If tests fail** during Step 3.5, do NOT commit. Fix the issue first, re-run targeted tests, then proceed to G3.

*Return to Gate O2 for next AF, or proceed to Phase 4 if all AFs are complete.*

---

### Phase 4: Review

#### 4.1 Gate P4: Normal

All AFs in sprint scope are committed. Ready for sprint review.

#### 4.2 Step: C2 — Full CI Checkpoint + evidence

**Code projects:** Run full CI suite per GS §PO07. All checks must pass.

**Docs-only projects — run these checks:**
- [ ] INDEX consistency: all INDEX rows match internal `Status:` fields
- [ ] File existence: all linked files in INDEX tables exist
- [ ] Naming compliance: new-convention files have no status token in filename

#### 4.3 Step: PR

##### 4.3.1 Task: Follow additional instructions in review doc

Check `S##_REVIEW.md` for any sprint-specific review instructions from HITL.

##### 4.3.2 Task: Gather artifacts

Collect:
- List of all AFs completed with final status
- Test/CI results (or docs-only verification results)
- Any decisions made during implementation

##### 4.3.3 Task: Fill out relevant doc sections

Fill `S##_REVIEW.md`:
1. Work items table (all AFs with final status)
2. Sprint Cognitive Health section
3. Learnings (optional)

##### 4.3.4 Task: Fill out PR
Fill `S##_PULL_REQUEST.md`
All required sections must be complete.

##### 4.3.5 Task: Present review

Present review summary to HITL with all evidence.

#### 4.4 Step: Human review

Discretionary HITL step. HITL reviews the sprint output at their own discretion — this may include testing, inspection, exploration, or assessment of delivered artifacts. This step is NOT a gate: it has no checklist, no required output, and no pass/fail criteria. Observations feed into the O3 review decision.

#### 4.5 Gate O3: Critical — Review decision

HITL decides:

| Decision | Action |
|----------|--------|
| **ACCEPTED** | Proceed to Phase 5 |
| **ACCEPT WITH FOLLOW-UPS** | Create follow-up AFs, then proceed to Phase 5 |
| **REJECTED** | Sprint status → `REJECTED`. Branch preserved. No merge. Record rationale. STOP. |

#### 4.6 Gate G4: Normal — Review decision commit

Commit gate for review artifacts and any follow-up AF files. Ask: "Approve review decision commit?"

#### 4.7 Step: Commit

```bash
git add <files>
git commit -m "<type>(sprint ##): review artifacts"
```

---

### Phase 5: Sprint End

#### 5.1 Gate P5: Additional

Review decision is ACCEPTED or ACCEPT WITH FOLLOW-UPS.

#### 5.2 Step: Quick fixes

If HITL identified minor issues during review:
- Budget: 30 min total cumulative (HITL-overridable)
- Implement fix → present → commit
- If fixes exceed budget: create follow-up AFs instead

#### 5.3 Step: Finalize docs

##### 5.3.1 Task: Index consistency check

1. Update each AF's internal `Status:` field to `DONE`
2. Update each AF's INDEX_BACKLOG row to `DONE`
3. Update bugs and ADR internal `Status:` according to state, if applicable
4. Update INDEX for bugs and ADRs `Status:` according to state, if applicable
5. Fill completion sections (if not already done)
6. Update sprint description status to `DONE`
7. Update INDEX_SPRINTS to `Done`

> Transition T4 (READY → DONE) fires at G4 for Sprint Descriptions. See GS §IM07.4.

For each INDEX file:
- [ ] All entries have valid file paths
- [ ] All statuses match (internal field ↔ INDEX row)
- [ ] No duplicate entries
- [ ] No orphaned entries (file exists but not in INDEX)
- [ ] No phantom entries (in INDEX but file doesn't exist)

##### 5.3.2 Task: File system scan

Cross-reference each artifact file against its respective INDEX:
```bash
ls docs/files/backlog/
ls docs/files/bugs/
ls docs/files/decisions/
ls docs/files/sprints/
```

Record final file counts — these become the expected baseline for the next sprint's manifest check (Phase 2, Step 2.2.3).

##### 5.3.3 Task: Living docs sweep

Check whether living documents need updating based on sprint changes (GS §PO08). Update only if the sprint introduced stale references. Mark each as **Updated** or **N/A** in the sprint review.

> **Docs-only projects:** Skip living docs sweep for non-existent documents.

#### 5.4 Gate O4: Critical — Opt-in to skip C3

HITL decides whether C3 is required or can be skipped. Relevant when no quick fixes were made in Step 5.2 AND C2 already passed in P4. If quick fixes were made, C3 is mandatory.

Ask: "No quick fixes were made / Quick fixes were made. Skip C3 or run C3?"

#### 5.5 Step: C3 — Full CI Checkpoint

Full re-validation before merge. Confirms nothing regressed after quick fixes.

**Code projects:** Run full CI suite per GS §PO07. All checks must pass.

**Docs-only projects — run these checks:**
- [ ] INDEX consistency: all INDEX rows match internal `Status:` fields
- [ ] File existence: all linked files in INDEX tables exist
- [ ] Naming compliance: new-convention files have no status token in filename

#### 5.6 Gate G5: Critical — Pre-merge

All CI checks must pass (or C3 skipped via O4).
Ask: "Approve PR for merge?"

#### 5.7 Step: Merge

After G5 approval:
- Merge to main (`--no-ff` preferred to preserve branch topology)
- Verify CI passes after merge

---

### Phase 6: Inter-Sprint

#### 6.1 Gate P6: Additional

Sprint closed (Phase 5 complete). Next sprint not yet started.

#### 6.2 Step: Housekeeping

**Allowed work:**
1. New AF/BUG files with `PROPOSED` or `READY` status
2. INDEX updates for new entries
3. Sprint description file creation
4. Backlog grooming (reprioritization, status updates)

**Not allowed:**
- Code changes (`src/`, `tests/`)
- Modifying server files (§IM08.4) — applies in ALL phases for consumer projects
- Changing status of in-flight items from a previous sprint

#### 6.3 Step: AF creation

Create new files using the appropriate template:
- AF items: `foundation/templates/BACKLOG_ITEM_TEMPLATE.md`
- BUG reports: `foundation/templates/BUG_REPORT_TEMPLATE.md`
- ADR decisions: `foundation/templates/ADR_TEMPLATE.md`

Update corresponding INDEX files.

#### 6.4 Gate G6: Additional

Inter-sprint commit approval. Ask: "Approve inter-sprint commit?"

#### 6.5 Step: Commit procedure

1. Create a short-lived branch: `chore/inter-sprint-<description>`
2. Scope is docs-only
3. Create a minimal PR with one-line summary
4. Merge before the next sprint branch is created

---

## Appendices
### Appendix A: Quick Reference Commands


#### CI Commands

Project-specific CI commands (linting, testing, coverage) → GS §PO07.

#### Git Commands
```bash
git checkout main                 # Switch to main
git pull origin main              # Update main
git checkout -b <type>/<name>     # Create branch (types per GS §DS01)
git status                        # Verify state
git branch                        # Verify branch
```

#### Evidence Commands

Project-specific evidence commands → GS §PO07.

---

### Appendix B: Escalation Triggers (→ GS §IM05)

**STOP and escalate if:**
- Invariant conflict detected (E4)
- Cannot determine correct approach (E6)
- Tests fail with no clear fix (E3)
- Scope creep detected (E5)
- Blocking dependency discovered (E7)
- CI cannot pass (E8)

For escalation procedure, see GS §IM05.

---

### Appendix C: Canonical Source Pointers

- **C.1** Status values → GS §IM07 (universal lifecycle model)
- **C.2** Priority definitions → GS §DS03 (lifecycle overview)
- **C.3** Naming conventions → GS §DS01 (repository structure & naming)
- **C.4** INDEX discipline → GS §IM01 (update rules, status alignment)
- **C.5** File creation workflow → GS §DS01 (repository structure & naming)
- **C.6** PR and merge rules → SP Phase 4 (Review) and Phase 5 (Sprint End)

## References

- R3 (implements): `foundation/GOVERNANCE_STANDARD.md`
- R4 (executes governance via): `foundation/templates/`
