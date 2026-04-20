# LIFECYCLE REGISTRY
#### Description: Canonical reference for the complete sprint lifecycle. Delegated by GS §DS03. Contains the full phase definitions (Phases 1–6) with all steps, tasks, and gates. Also includes the complete gate registry (phase, git, operational, and escalation) with severity levels and trigger conditions, CI checkpoint definitions, and numbering conventions. Use this as the source of truth for lifecycle structure; the Sprint Playbook implements these phases as an executable script.
#### Convergent: v1.3.2
#### governs: ag_foundation

> **Nomenclature:** Phases → Steps → Tasks. Gates use format: `Gate <ID>: <Severity> — <description>`.

---
## Phases

### Phase 1: Sprint Planning (P1)

#### 1.1 Gate P1: Additional

Entry gate. Sprint planning begins when backlog has READY items and capacity is available, or a new version cycle begins.

#### 1.2 Step: Scoping

**Ownership:** HITL. Agent is not involved in planning decisions; may propose AFs during inter-sprint.

##### 1.2.1 Task: Review backlog

1. Review prioritized backlog
2. Select AFs for sprint scope based on: priority, capacity, thematic coherence, dependencies
3. Move selected AFs to READY status

**Priority levels:**
| Level | Meaning |
|:---:|---|
| P0 | Must-ship — sprint fails without it |
| P1 | Should-ship — expected in scope, defer only if blocked |
| P2 | Nice-to-have — include if capacity allows |

#### 1.3 Step: Create sprint docs

##### 1.3.1 Task: Create sprint folder and artifacts

Create the sprint folder: `docs/files/sprints/S##/`

##### 1.3.2 Task: Use templates to build sprint description, review, and PR files

1. Create `S##_DESCRIPTION.md` from template — fill sprint ID, name, scope, execution order
2. Create `S##_REVIEW.md` from template — leave empty (filled at review)
3. Create `S##_PULL_REQUEST.md` from template — leave empty (filled at close)

#### 1.4 Gate G1: Additional

Planning commit gate. Sprint description and all AF files must exist with Status = READY.

#### 1.5 Step: Commit

Commit planning artifacts.

---

### Phase 2: Sprint Start (P2)

#### 2.1 Gate P2: Critical

Entry gate. Sprint description file exists. Agent is assigned. **This gate is never skippable** — scope confirmation is a hard requirement.

#### 2.2 Step: Read & verify

##### 2.2.1 Task: Mandatory reads

Read these documents completely before any action:
1. `foundation/GOVERNANCE_STANDARD.md` (governance rules) <!-- Kai: These are necessary back referrences -->
2. `foundation/SPRINT_PLAYBOOK.md` (execution script)<!-- Kai: These are necessary back referrences -->
3. Sprint description file (`S##_DESCRIPTION.md`)
4. All AF files referenced in sprint scope
5. All INDEX files

##### 2.2.2 Task: Pre-sprint checklist

- [ ] Sprint scope matches INDEX entries
- [ ] All AF statuses are READY (not PROPOSED)
- [ ] Naming conventions applied to all files
- [ ] No filename ↔ status mismatches

##### 2.2.3 Task: Baseline manifest check

Count files in each artifact folder and compare against the expected baseline (from previous sprint's verified counts or sprint description).

| Category | Path | Expected | Actual |
|----------|------|:--------:|:------:|
| Backlog items | `docs/files/backlog/` | ___ | ___ |
| Bug reports | `docs/files/bugs/` | ___ | ___ |
| ADR files | `docs/files/decisions/` | ___ | ___ |
| Sprint folders | `docs/files/sprints/` | ___ | ___ |

If any count mismatches: STOP → escalate (E7 — blocking dependency).

Present verification summary (including manifest counts) to HITL.

#### 2.3 Step: Agent actively asks questions

Agent asks clarifying questions about scope, ambiguity, or approach. HITL answers.

#### 2.4 Gate O1: Normal — Questions

Scope clarification gate. Agent presents questions, HITL answers.

#### 2.5 Gate G2: Additional

Branch creation gate.

#### 2.6 Step: Branch creation

```bash
git checkout main
git pull origin main
git checkout -b <branch-type>/<short-name>
```

Branch types and naming conventions → `FOLDER_STRUCTURE.md`.

Verify: working directory clean, on correct branch, name follows convention.

---

### Phase 3: Implementation (P3)

#### 3.1 Gate P3: Normal — Phase entry

All pre-sprint verification complete. Branch created. Ready to implement.

> **Loop:** Repeat Steps 3.3–3.7 for each AF in execution order.
> On iteration 1, P3 entry and O2 are the same gate.
> On iteration 2+, O2 opens the next AF loop without re-entering P3.

#### 3.2 Gate O2: Normal — AF iteration start

Agent presents AF scope summary. HITL confirms: "Proceed with AF-####."

#### 3.3 Step: Implement

- Pre-implementation check: AF file exists with correct status, scope understood
- Make atomic, reversible changes
- Do not mix unrelated changes
- If destructive action required → escalate (E1)
- If rule exception needed → escalate (E2)
- If invariant conflict detected → escalate (E4)
- If scope creep detected → escalate (E5)
- If blocked → escalate (E3/E6/E7)

#### 3.4 Step: Evidence capture

Evidence is required when behavior changes affect outputs or execution decisions.

| PR Type | Tests Required | RunTrace Required |
|---------|---------------|-------------------|
| Docs-only | No | No |
| Code change | Per project PR type taxonomy | Per project PR type taxonomy |

Code projects: the project-specific PR type taxonomy and evidence requirements are defined at the interface level and resolved at execution time.
Docs-only projects: verification checklists replace test/trace evidence.

#### 3.5 Step: C1 — Targeted CI Checkpoint

**Code projects:** Run only the tests relevant to the current AF. Project-specific CI commands are defined at the interface level and resolved at execution time. Do NOT run the full suite per commit.

**Docs-only projects:** Cross-reference edits against canonical sources. Verify INDEX consistency for affected entries.

#### 3.6 Gate G3: Normal — AF commit

Agent presents AF summary: files changed, key decisions, evidence/verification results.
HITL approves: "Approve AF-#### and move to next?"

#### 3.7 Step: Commit

One commit per AF. Commit message: `docs: AF-#### — <description>` (or `feat:`/`fix:` for code).

**Commit discipline** is defined at the interface level and enforced at execution time.

**If tests fail:**
1. Fix before commit
2. No "fix in next PR" deferrals
3. If blocked → E3 escalation

---

### Phase 4: Review (P4)

#### 4.1 Gate P4: Normal

All AFs in sprint scope committed. Agent presents implementation summary.
<!-- Kai: need to take a look at these expressions -->
#### 4.2 Step: C2 — Full CI Checkpoint + evidence

Run full CI suite + generate evidence files during review preparation.

#### 4.3 Step: PR
<!-- Kai: need to take a look at these expressions -->
##### 4.3.1 Task: Follow additional instructions in review doc

Check `S##_REVIEW.md` or sprint-specific review instructions.

##### 4.3.2 Task: Gather artifacts

Collect all review artifacts: evidence, verification checklists, cognitive health data.

##### 4.3.3 Task: Fill out relevant doc sections
<!-- Kai: need to take a look at these expressions -->
Agent prepares sprint review document (`S##_REVIEW.md`):
1. Work items table (all AFs with final status)
2. Sprint Cognitive Health section (see below)
3. Learnings (optional)

**Sprint Cognitive Health fields:**

| Field | Description |
|-------|-------------|
| Sprint velocity | AFs completed / AFs planned |
| Ceremony time | Estimated total time on governance overhead |
| Blocked time | Time lost to blockers, unclear scope, escalations |
| Scope changes | AFs added, deferred, or dropped mid-sprint |
| Tool friction | Tooling issues that slowed work |
| Decision quality | Were escalations timely? Were decisions clear? |
| Carry-forward | Lessons or patterns for next sprint |

##### 4.3.4 Task: Fill out PR

Fill `S##_PULL_REQUEST.md` (created in P1). All required sections must be complete. The agent may extend the document non-destructively to match sprint-specific requirements.

Every PR must include:
1. Sprint reference and all AF items completed
2. Summary (what changed, why)
3. Non-goals
4. Files changed
5. Evidence (lint/test/trace results)
6. Docs updated confirmation
7. Risk level (P0 / P1 / P2)

PR size rule: Must be reviewable in 15–30 minutes. If larger, split plan required.

##### 4.3.5 Task: Present review

Agent presents review summary to HITL.

#### 4.4 Step: Human review

Discretionary HITL step. HITL reviews the sprint output at their own discretion — this may include testing, inspection, exploration, or assessment of delivered artifacts. This step is NOT a gate: it has no checklist, no required output, and no pass/fail criteria. Observations from human review feed into the O3 review decision.

#### 4.5 Gate O3: Critical — Review decision

HITL makes one of three decisions:

| Decision | Action |
|----------|--------|
| **ACCEPTED** | Close sprint. Proceed to Sprint End (P5). |
| **ACCEPT WITH FOLLOW-UPS** | Create follow-up AFs in backlog. Close sprint. Proceed to P5. |
| **REJECTED** | Sprint status → `REJECTED`. Branch preserved (not deleted). No merge. Record rationale + learnings. |

#### 4.6 Gate G4: Normal — Review decision commit

Commit gate for review artifacts and any follow-up AF files created during the review decision.

#### 4.7 Step: Commit

Commit review artifacts.

---

### Phase 5: Sprint End (P5)

#### 5.1 Gate P5: Additional

Review decision is ACCEPTED or ACCEPT WITH FOLLOW-UPS.

#### 5.2 Step: Quick fixes

If HITL identified minor issues during review:
- Quick fix budget: 30 min **total cumulative** (HITL-overridable ad hoc)
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

For each INDEX file:
- [ ] All entries have valid file paths
- [ ] All statuses match (internal field ↔ INDEX row
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

Check whether living documents need updating based on sprint changes. Update only if the sprint introduced stale references.

| Document | Update if sprint changed... |
|----------|----------------------------|
| INDEX files | Artifact statuses, file paths, entry counts |
| `PROJECT_CONTROL.md` | CI commands, thresholds, invariants |
| `PROJECT_ROADMAP.md` | Milestones, phase boundaries, strategic priorities |
| `CHANGELOG.md` | Version history, sprint summary |
| *(project-specific)* | Additional living docs as defined in PC GS:PO08 |

> **Server files (`foundation/` and its subdirectories) are never living docs targets.** If a sprint reveals stale server content, create a backlog item in the GVS project.

Mark each as **Updated** or **N/A** in the sprint review.

> **Docs-only projects:** Skip living docs sweep for non-existent documents.

#### 5.4 Gate O4: Critical — Opt-in to skip C3

HITL decides whether C3 (full CI re-validation) is required or can be skipped. O4 is relevant when no quick fixes were made in Step 5.2 AND C2 already passed in P4. If quick fixes were made, C3 is mandatory — O4 still fires but skip is not available.

- **Severity:** Critical (always active, never skippable)
- **HITL approves:** Skip C3 (no quick fixes, C2 already passed) OR require C3

#### 5.5 Step: C3 — Full CI Checkpoint

Full re-validation before merge. Confirms nothing regressed after quick fixes.

**Code projects:** Run full CI per project-specific CI commands. All checks must pass.

**Docs-only projects — run these checks:**
- [ ] INDEX consistency: all INDEX rows match internal `Status:` fields
- [ ] File existence: all linked files in INDEX tables exist
- [ ] Naming compliance: new-convention files have no status token in filename

#### 5.6 Gate G5: Critical — Pre-merge

All CI checks must pass (or C3 skipped via O4). HITL approves PR for merge.
- If PR is blocked → escalate (E8)

#### 5.7 Step: Merge

- Merge to main (`--no-ff` preferred to preserve branch topology)
- Verify CI passes after merge

---

### Phase 6: Inter-Sprint (P6)

#### 6.1 Gate P6: Additional

Sprint closed (P5 complete). Next sprint not yet started.

#### 6.2 Step: Housekeeping

Allowed work:
1. New AF/BUG files with `PROPOSED` or `READY` status
2. INDEX updates for new entries
3. Sprint description file creation
4. Backlog grooming (reprioritization, status updates)

Not allowed:
- Code changes (`src/`, `tests/`)
- Modifying server files (§IM08.4) — applies in ALL phases for consumer projects <!-- Kai: These are necessary back referrences -->
- Changing status of in-flight items from a previous sprint

#### 6.3 Step: AF creation

Create new AF/BUG files using templates. Update corresponding INDEX files.

#### 6.4 Gate G6: Additional

Inter-sprint commit gate.

#### 6.5 Step: Commit procedure

1. Create a short-lived branch: `chore/inter-sprint-<description>`
2. Scope is docs-only
3. Create a minimal PR with one-line summary
4. Merge before the next sprint branch is created

---

## Gate Registry

### Severity Levels

| Label | Behavior | HITL Control |
|-------|----------|:------------:|
| **Critical** | Always active. Never skippable. | Cannot disable |
| **Normal** | Active by default. | Can disable per sprint |
| **Additional** | Off by default. | Can enable per sprint |

HITL can say "run this sprint with critical gates only" for trusted, low-risk sprints.

### Phase Gates (Px)

Phase gates mark entry into a new lifecycle phase. HITL approval required.

| Gate | Phase Entry | Severity | HITL Action |
|:----:|-----------|:--------:|-------------|
| P1 | Sprint Planning | Additional | Approve scope |
| P2 | Sprint Start | Critical | Approve readiness |
| P3 | Implementation | Normal | Acknowledge completion |
| P4 | Review | Normal | Confirm review ready |
| P5 | Sprint End | Additional | Confirm sprint closed |
| P6 | Inter-Sprint | Additional | Confirm ready for next sprint |

### Git Gates (Gx)

Git gates guard every repository state change. HITL approval required.

| Gate | Operation | Severity | HITL Action |
|:----:|----------|:--------:|-------------|
| G1 | Planning commit | Additional | Approve planning artifacts |
| G2 | Branch creation | Additional | Approve branch |
| G3 | AF commit | Normal | Approve AF completion |
| G4 | Review decision commit | Normal | Approve review artifacts |
| G5 | Pre-merge (after C3) | Critical | Approve PR |
| G6 | Inter-sprint commit | Additional | Approve housekeeping |

### Operational Gates (Ox)

Special-purpose checkpoints within phases. HITL approval required.

| Gate | Purpose | Severity | HITL Action |
|:----:|--------|:--------:|-------------|
| O1 | Agent asks questions | Normal | Answer questions |
| O2 | AF iteration start | Normal | Approve & proceed to next AF |
| O3 | Review decision | Critical | ACCEPTED / ACCEPT WITH FOLLOW-UPS / REJECTED |
| O4 | Opt-in to skip C3 | Critical | Approve skipping C3 or require it |

### Escalation Gates (Ex)

Exception-triggered, always Critical. Agent MUST: document the issue, propose 2–3 options, recommend one, present to HITL.

| Gate | Trigger | Agent Action |
|:----:|--------|-------------|
| E1 | Destructive actions | Describe impact, ask for explicit confirmation |
| E2 | Rule exceptions | Explain deviation, justify, ask for approval |
| E3 | Blocked work | Present failure, propose 2–3 options, recommend one |
| E4 | Invariant conflict | Identify conflict, explain consequences, ask for resolution |
| E5 | Scope creep | Flag excess, propose trim or expansion |
| E6 | Unclear approach | Present ambiguity, propose options |
| E7 | Blocking dependency | Describe blocker, propose workaround or wait |
| E8 | PR block | Present blocking issue, propose fix |

### CI Checkpoints

CI checkpoints are steps (not gates) that feed into gates. They use the `C<n>` naming convention.

| Checkpoint | Name | Phase | Purpose | Feeds into |
|:----------:|------|:-----:|---------|:----------:|
| C1 | Targeted CI Checkpoint | P3 | Tests relevant to current AF only. Fast feedback. | G3 |
| C2 | Full CI Checkpoint + evidence | P4 | Full suite + evidence files for PR. | O3 |
| C3 | Full CI Checkpoint | P5 | Full re-validation before merge. | G5 |

> `C<n>` is a checkpoint naming convention, NOT a gate category. Gates remain P/G/O/E.

### Complete Gate Table

| ID | Name | Category | Severity | Phase | Trigger Summary |
|:--:|------|----------|:--------:|:-----:|-----------------|
| P1 | Sprint Planning entry | Phase | Additional | P1 | Backlog has READY items + capacity |
| P2 | Sprint Start entry | Phase | Critical | P2 | Sprint description exists, agent assigned |
| P3 | Implementation entry | Phase | Normal | P3 | Verification complete, branch created |
| P4 | Review entry | Phase | Normal | P4 | All AFs committed |
| P5 | Sprint End entry | Phase | Additional | P5 | Review ACCEPTED or ACCEPT WITH FOLLOW-UPS |
| P6 | Inter-Sprint entry | Phase | Additional | P6 | Sprint closed |
| G1 | Planning commit | Git | Additional | P1 | Sprint docs exist, AFs READY |
| G2 | Branch creation | Git | Additional | P2 | Branch approved |
| G3 | AF commit | Git | Normal | P3 | AF summary + evidence presented |
| G4 | Review decision commit | Git | Normal | P4 | Review decision made |
| G5 | Pre-merge (after C3) | Git | Critical | P5 | All CI pass |
| G6 | Inter-sprint commit | Git | Additional | P6 | Housekeeping ready |
| O1 | Agent asks questions | Operational | Normal | P2 | Agent presents questions |
| O2 | AF iteration start | Operational | Normal | P3 | Agent presents AF scope |
| O3 | Review decision | Operational | Critical | P4 | HITL decides outcome |
| O4 | Opt-in to skip C3 | Operational | Critical | P5 | HITL decides outcome based on quick fixes work |
| E1 | Destructive actions | Escalation | Critical | Any | Describe impact, ask confirmation |
| E2 | Rule exceptions | Escalation | Critical | Any | Explain deviation, justify |
| E3 | Blocked work | Escalation | Critical | P3 | Present failure, propose options |
| E4 | Invariant conflict | Escalation | Critical | Any | Identify conflict, propose resolution |
| E5 | Scope creep | Escalation | Critical | P3 | Flag excess, propose trim |
| E6 | Unclear approach | Escalation | Critical | P3 | Present ambiguity, propose options |
| E7 | Blocking dependency | Escalation | Critical | Any | Describe blocker, propose workaround |
| E8 | PR block | Escalation | Critical | P5 | Present issue, propose fix |

---



## References

- Sibling source: `foundation/sources/FOLDER_STRUCTURE.md`
- Sibling source: `foundation/sources/SESSION_CHAIN.md`

