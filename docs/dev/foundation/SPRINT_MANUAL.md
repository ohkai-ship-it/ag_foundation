# SPRINT EXECUTION PLAYBOOK
# Version: v1.0
# Effective date: 2026-03-04

This document is a deterministic step-by-step operational script.
It contains zero ambiguity. Follow each step exactly.

---

## 0. Pre-Sprint Read Phase

### 0.1 Mandatory Reads (Before Any Action)
Read these documents completely before starting:
1. `/docs/dev/foundation/FOUNDATION_MANUAL.md`
2. Sprint description file (`S##_DESCRIPTION.md`)
3. All AF files referenced in sprint scope
4. All INDEX files:
   - `/docs/dev/backlog/INDEX_BACKLOG.md`
   - `/docs/dev/bugs/INDEX_BUGS.md`
   - `/docs/dev/decisions/INDEX_DECISIONS.md`
   - `/docs/dev/sprints/INDEX_SPRINTS.md`

### 0.2 Pre-Sprint Checklist
- [ ] Confirm sprint scope matches INDEX entries
- [ ] Confirm all AF statuses are `Ready` (not `Proposed`)
- [ ] Confirm naming conventions are applied to all files
- [ ] Create sprint folder and move description file into it
- [ ] Update all index files
- [ ] Confirm no filename ↔ status mismatches exist
- [ ] Ask clarifying questions in chat if anything unclear
- [ ] **Wait for explicit "proceed" from Kai before implementation**

---

## 1. Branch Creation Phase

> **Branch lifecycle (CRITICAL):**
> - Create ONE branch per sprint at sprint start
> - Each AF gets its own commit on the branch (1 commit = 1 AF)
> - Merge to main via ONE PR at sprint close only
>
> PRs are NOT created continuously during the sprint.
> The PR lists ALL AFs completed in the sprint for traceability.

### 1.1 Create Branch
Execute:
```bash
git checkout main
git pull origin main
git checkout -b <branch-type>/<short-name>
```

Branch types:
- `feat/<short-name>` — new features
- `fix/<short-name>` — bug fixes
- `chore/<short-name>` — maintenance, docs, refactors

### 1.2 Verify Branch
Execute:
```bash
git status
git branch
```

Confirm:
- [ ] Working directory clean
- [ ] On correct branch
- [ ] Branch name follows convention

### 1.3 Record in Sprint Description
Update `S##_DESCRIPTION.md` with branch name in the PR plan section.

---

## 2. File Creation / Rename Protocol

### 2.1 Creating New AF File
1. Copy template from `/docs/dev/backlog/templates/BACKLOG_ITEM_TEMPLATE.md`
2. Save to `/docs/dev/backlog/items/AF####_<STATUS>_<three_word_description>.md`
3. Fill all metadata fields
4. Ensure internal `Status:` field matches filename status

### 2.2 Naming Convention Enforcement
```
Filename:  AF0047_READY_feature_description.md
Internal:  Status: READY
```

**These MUST match. Mismatch is a blocking defect.**

### 2.3 Renaming on Status Change
When status changes:
1. Rename file:
   ```
   AF0047_READY_feature_description.md → AF0047_IN_PROGRESS_feature_description.md
   ```
2. Update internal `Status:` field to match
3. Update INDEX_BACKLOG.md entry
4. Verify no broken links in other documents
5. Commit all changes together

### 2.4 Bug Report Creation
1. Copy template from `/docs/dev/bugs/templates/BUG_REPORT_TEMPLATE.md`
2. Save to `/docs/dev/bugs/reports/BUG####_<STATUS>_<three_word_description>.md`
3. Fill all metadata fields
4. Update `/docs/dev/bugs/INDEX_BUGS.md`

### 2.5 ADR Creation
1. Copy template from `/docs/dev/decisions/templates/ADR_TEMPLATE.md`
2. Save to `/docs/dev/decisions/files/ADR###_<three_word_description>.md`
3. Fill all sections
4. Update `/docs/dev/decisions/INDEX_DECISIONS.md`

---

## 3. Index Update Protocol (STRICT)

### 3.1 Trigger Events
INDEX files MUST be updated when:
- New AF created
- AF status changes
- New bug created
- Bug status changes
- New ADR created
- ADR status changes
- Sprint created
- Sprint status changes

### 3.2 Update Procedure
For each trigger event:
1. Open respective INDEX file
2. Locate the correct table section
3. Insert/update row with:
   - Correct ID
   - Current status
   - Accurate file path
4. Verify row is in correct status table (e.g., "Active backlog" vs "Done")
5. Confirm filename path matches actual file location

### 3.3 Commit Rule
INDEX update must be committed:
- In the same PR if tied to the AF being addressed
- As a standalone commit if independent status change

### 3.4 Verification
After every INDEX update:
```bash
# Verify files exist at documented paths
ls docs/dev/backlog/items/AF####_*.md
ls docs/dev/bugs/reports/BUG####_*.md
ls docs/dev/decisions/files/ADR###_*.md
```

---

## 4. Implementation Phase (Code Changes)

### 4.1 Pre-Implementation Checklist
- [ ] Branch created and verified
- [ ] AF file exists with correct status
- [ ] INDEX updated
- [ ] Scope understood completely

### 4.2 During Implementation
- Make atomic commits
- Each commit should be reversible
- Do not mix unrelated changes
- **Run targeted tests only** — do NOT run the full suite on every change:
  ```bash
  pytest tests/test_<relevant>.py -W error
  ```
  This keeps feedback fast and avoids wasted CI cycles.

### 4.3 Before Commit (Full Gate)

Run the complete CI gate **once, right before `git commit`**.
Do NOT run these on every save — that's what targeted tests (4.2) are for.

**Run ALL of these commands. All must pass.**

**Linting:**
```bash
ruff check src tests
```
Expected: No errors

**Formatting:**
```bash
ruff format --check src tests
```
Expected: No files would be reformatted

If formatting needed:
```bash
ruff format src tests
```

**Tests:**
```bash
pytest -W error
```
Expected: All tests pass, no warnings

**Coverage:**
```bash
pytest --cov=src/ag --cov-report=term-missing
```
Expected: Coverage thresholds met (see FOUNDATION_MANUAL.md Section 6.1)

### 4.4 If Tests Fail
1. **Fix the tests before PR**
2. No "fix in next PR" deferrals
3. No merge with failing tests
4. If blocked, escalate immediately

---

## 5. Evidence Capture Protocol

### 5.1 When Evidence Is Required
Evidence is required when:
- CLI output changes
- Runtime behavior changes
- Planner/Orchestrator/Executor/Verifier logic changes
- Any user-visible behavior changes

### 5.2 Capture Procedure
1. Execute the command that demonstrates the behavior:
   ```bash
   ag run --task "..." --workspace <workspace>
   ```

2. Record the RunTrace ID from output

3. Validate trace fields:
   ```bash
   ag runs show <run_id> --json
   ```

4. Verify:
   - [ ] `status` field is correct
   - [ ] `reasoning_mode` field is correct
   - [ ] Step fields present (`step_id`, `role`, `status`, `timing_ms`)
   - [ ] CLI label matches trace-derived value

### 5.3 Evidence Documentation
In AF completion section, include:
```
### Evidence
- **Command:** `ag run --task "..." --workspace demo`
- **RunTrace ID:** `run_abc123...`
- **Validation:** `ag runs show run_abc123... --json`
- **Key fields verified:**
  - status: completed
  - reasoning_mode: llm
  - steps: [list key steps]
```

---

## 6. PR Creation Protocol

### 6.0 When to Create a PR (CRITICAL)

> **PRs are created ONLY at sprint close, not during the sprint.**
>
> - **During sprint:** Commit work directly to feature branch (multiple commits per AF is fine)
> - **At sprint close:** Create ONE PR to merge feature branch → main
> - **PR scope:** One PR covers all sprint work items

This is the intended workflow:
1. Sprint start: Create feature branch from main
2. During sprint: Commit work to feature branch
3. Sprint end: Create ONE PR to merge the entire sprint branch to main

### 6.1 PR Template Sections (All Required)

**Sprint work items:**
- List ALL AF items completed in this sprint

**Summary:**
- What changed (2–5 bullets)
- Why it changed

**Non-goals:**
- What is explicitly NOT in scope

**Files changed:**
- List all significant paths touched

**Evidence:**
- Lint commands + results
- Test commands + results
- RunTrace ID(s) for behavior changes

**Risk level:**
- P0 / P1 / P2 with justification

### 6.2 PR Size Verification
- [ ] PR is reviewable in 15–30 minutes
- [ ] If larger, split plan documented

### 6.3 Checklist Before Submitting
- [ ] All sprint AF items listed in PR
- [ ] Each AF has its own commit on the branch
- [ ] All CI commands pass locally
- [ ] Evidence captured and documented
- [ ] AF completion section filled
- [ ] INDEX files updated
- [ ] No filename ↔ status mismatches

---

## 7. Post-Merge Ritual

### 7.1 Immediately After Merge
1. Update AF status to `DONE`:
   - Rename file: `AF####_IN_PROGRESS_desc.md` → `AF####_DONE_desc.md`
   - Update internal `Status:` field to `DONE`

2. Fill completion section (if not already done):
   - All metadata filled
   - Acceptance criteria marked
   - Files changed listed
   - Evidence captured

3. Update INDEX_BACKLOG.md:
   - Move entry from "Active" table to "Done" table
   - Verify file path is correct

### 7.2 Verification
- [ ] AF filename shows `Done`
- [ ] AF internal status shows `Done`
- [ ] INDEX shows correct status and path
- [ ] No stale `Proposed` or `In progress` entries for this AF

### 7.3 Sprint State Update
Update `S##_DESCRIPTION.md`:
- Move AF from "in progress" to "completed" section
- Add PR reference

---

## 8. Sprint Close Ritual

### 8.1 Full Repo Hygiene Check
Execute:
```bash
# Verify all files pass linting
ruff check src tests

# Verify formatting
ruff format --check src tests

# Verify tests pass
pytest -W error

# Verify coverage
pytest --cov=src/ag --cov-report=term-missing
```

### 8.2 Index Consistency Check
For each INDEX file:
- [ ] All entries have valid file paths
- [ ] All statuses match filename statuses
- [ ] No duplicate entries
- [ ] No orphaned entries (file exists but not in index)
- [ ] No phantom entries (in index but file doesn't exist)

### 8.3 File System Scan
Verify no stray files:
```bash
# List all AF files
ls docs/dev/backlog/items/

# List all BUG files
ls docs/dev/bugs/reports/

# List all ADR files
ls docs/dev/decisions/files/

# List sprint folders
ls docs/dev/sprints/documentation/
```

Cross-reference each file against respective INDEX.

### 8.4 Status Mismatch Scan
For each AF/BUG file:
1. Extract status from filename
2. Read internal Status field
3. Confirm match
4. If mismatch: FIX IMMEDIATELY

### 8.5 Sprint Description Update
Update `S##_DESCRIPTION.md`:
- Fill "Sprint report section" completely
- Document all shipped items
- Document all not-shipped items with reasons
- Include evidence (RunTrace IDs, test summaries)
- Include learnings

### 8.6 Final State
- [ ] All P0 items merged
- [ ] All completion sections filled
- [ ] All indices consistent
- [ ] Sprint description complete
- [ ] Review file created/updated
- [ ] Sprint status updated to `Closed`

---

## 9. Autonomy Gate (Required For Autonomy-Affecting Sprints)

This gate is mandatory when sprint scope touches planner, orchestrator,
verifier, skill chaining, policy hooks, or user-visible execution labels.

### 9.1 Start Gate (Sprint Planning)
- [ ] Scope identifies autonomy-affecting AF/BUG items explicitly
- [ ] Policy impact identified (permission, confirmation, budget, escalation)
- [ ] Trace impact identified (new/changed labels and required trace fields)
- [ ] Failure-path scenarios identified up front
- [ ] Workspace-boundary risks identified

### 9.2 Close Gate (Sprint Review/Closure)
- [ ] User-visible labels verified as trace-derived
- [ ] Policy checks verified in touched behavior paths
- [ ] Retry/timeout/failure behavior verified and trace-aligned
- [ ] Workspace isolation verified in happy and failure paths
- [ ] `pytest -W error` evidence captured
- [ ] Open autonomy blockers converted to AF/BUG items with index updates

### 9.3 Autonomy Milestones
| Date | Sprint | Milestone | Evidence |
|------|--------|-----------|----------|
| 2026-03-21 | S12 (pre-impl) | V1 Planner produces multi-output plans (two `emit_result` calls) with accumulated chaining | BUG-0016c fix; `plan_486286485e3b` |
| 2026-03-21 | S13 (planned) | V2Planner composes mixed skill+playbook plans; V1Orchestrator handles playbook expansion inline; V1Verifier respects required/optional steps (BUG-0017 fix); pipeline V0s extracted to dedicated files | AF-0103, AF-0114, AF-0115, AF-0117 (partial) |
| TBD | S14 (planned) | Per-step verification loop: V1Executor validates output against schema with bounded retry; V1Orchestrator wires per-step verification; VERIFICATION steps in trace; V1Recorder persists verification evidence | AF-0116, AF-0117 (remainder), AF-0118 |

### 9.4 Decision Rule
- If any P0 Autonomy Gate item is unchecked: sprint cannot be Closed.
- If only P1/P2 items remain: `ACCEPT WITH FOLLOW-UPS` is allowed only if
   follow-up AF/BUG items are created and indexed.

---

## Quick Reference: Commands

### CI Commands
```bash
ruff check src tests              # Linting
ruff format --check src tests     # Format check
ruff format src tests             # Apply formatting
pytest -W error                   # Tests with warnings-as-errors
pytest --cov=src/ag --cov-report=term-missing  # Coverage
```

### Git Commands
```bash
git checkout main                 # Switch to main
git pull origin main              # Update main
git checkout -b feat/<name>       # Create feature branch
git checkout -b fix/<name>        # Create fix branch
git checkout -b chore/<name>      # Create chore branch
git status                        # Verify state
git branch                        # Verify branch
```

### Evidence Commands
```bash
ag run --task "..." --workspace <ws>    # Execute run
ag runs show <run_id> --json            # Validate trace
ag runs list --workspace <ws>           # List runs
```

---

## Escalation Triggers

**STOP and escalate if:**
- Invariant conflict detected
- Cannot determine correct approach
- Tests fail with no clear fix
- Scope creep detected
- Blocking dependency discovered
- CI cannot pass

**Escalation procedure:**
1. Document the issue clearly
2. Propose 2–3 options if possible
3. Recommend one option
4. Wait for explicit decision
5. Do not proceed with workarounds

---

## References

- Operating manual: `/docs/dev/foundation/FOUNDATION_MANUAL.md`
- Deprecated docs: `/docs/dev/foundation/old/`
