# Sprint Process (ag_foundation)
# Version number: v0.2

This playbook defines the **standard sprint operating process** for ag_foundation.

## Definitions
- **Sprint**: a timeboxed iteration aligned to the roadmap in `PROJECT_PLAN.md` (Sprint 00–08).
- **Backlog item**: AF-000x. The unit of planning and tracking.
- **PR**: Pull Request. The unit of delivery. **Strict rule:** one PR maps to exactly one primary AF item.

## Roles
- **Kai (PM):** owns sprint goal, backlog ordering, acceptance criteria, release decisions
- **Jeff (Tech lead):** owns architecture invariants, PR review gatekeeping for P1+ changes
- **Jacob (Implementer):** ships PR-sized slices, tests, trace evidence, completion notes

---

## Sprint start (30–45 minutes)

### 1) Set sprint goal
- One sentence: what outcome do we want by sprint end?

### 2) Select sprint scope (backlog slice)
- Pick 3–8 AF items (depending on size), ordered by priority.
- Mark as:
  - **P0 must** (ship)
  - **P1 should** (ship if time)
  - **P2 could** (only if slack)

### 3) Define PR slicing
For each AF item:
- Add “Expected PR” section in the AF item:
  - PR1 title (and PR2/PR3 if needed)
- Ensure PRs are reviewable (~15–30 min).

### 4) Define evidence expectations (per AF item)
- Tests required (unit/integration/contract)
- Required run traces (run_id) to capture
- Whether a review entry is required (P1+)

### 5) Update sprint tracking
Update `SPRINT_LOG.md` with a new sprint section:
- Sprint dates and goal
- Targeted backlog items table
- Link to detailed sprint plan if needed (e.g., `SPRINT_PLAN_SPRINT01.md`)

**Note:** We do NOT create per-sprint folders. All tracking goes in `SPRINT_LOG.md`.

---

## During sprint (daily operating rules)

### Daily rules
- Keep PRs small and focused.
- Every PR references exactly one primary AF item.
- Every behavior PR includes:
  - tests results
  - run trace id(s) where applicable
  - completion note MD linked in PR

### Status updates
- When PR is opened: update AF item status → **In progress**
- When PR is merged: update AF item status → **Done** (or **Partially done** if multi-PR)- Update `SPRINT_LOG.md` item status and PR link- Open bugs as soon as discovered (don’t hide them in PR comments).

### Drift control
- If an AF item needs scope change:
  - update the AF item text (goal/AC)
  - if P1+, record an ADR or update one
  - adjust sprint plan accordingly

---

## Sprint end (30 minutes)

### 1) Update sprint log
In `SPRINT_LOG.md`, update the sprint section with:
- Final status for all items (Done / Carried over / Dropped)
- Evidence summary (representative run_ids, review entries)
- Learnings + risks (brief notes)

### 2) Groom carry-over
- Move unfinished items to next sprint with updated scope.
- Create new AF items discovered during the sprint.

### 3) Decision hygiene
- Ensure any P1+ changes have ADRs recorded.
- Link ADRs from sprint log notes.

---

## Sprint quality gates (what "done" means)
A sprint is "done" when:
- all **P0 must** items are merged and verified
- completion notes exist for merged PRs (in `/docs/dev/handoff/`)
- sprint log section is updated with final status
- no P0 bugs are left untracked

---

## File structure (sprints folder)
```
/docs/dev/sprints/
├── INDEX.md                    # This index
├── PROCESS.md                  # This process doc
├── SPRINT_LOG.md               # Central log (one section per sprint)
├── SPRINT_PLAN_SPRINT01.md     # Detailed plan (optional, per sprint)
└── templates/                  # Templates for reference
```
