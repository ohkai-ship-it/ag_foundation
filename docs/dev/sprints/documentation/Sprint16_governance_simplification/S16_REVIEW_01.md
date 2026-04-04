# SPRINT REVIEW — S16_REVIEW_01 — governance_simplification
# Version number: v0.2

> **Purpose:** (A) Review execution tasks Jacob must perform. (B) Final review entry for Jeff+Kai to decide: **ACCEPT / ACCEPT WITH FOLLOW-UPS / REJECT**.
> **Location:** `/docs/dev/sprints/documentation/Sprint16_governance_simplification/S16_REVIEW_01.md`

---

## A) Review execution tasks (Jacob)

### Metadata
- **Review ID:** S16_REVIEW_01
- **Scope:** Sprint16
- **Executor:** Jacob
- **Date:**
- **Commit / tag:**
- **Environment:**

### Inputs
- Sprint description: `S16_DESCRIPTION.md`
- AF items in scope: `docs/dev/backlog/items/AF0129_READY_eliminate_filename_status.md` through `AF0136_READY_governance_docs_consolidation.md`
- Governance plan: `docs/dev/additional/GOVERNANCE_SIMPLIFICATION_PLAN_0.1.md`

### Outputs (paths)
Evidence folder: `/docs/dev/sprints/documentation/Sprint16_governance_simplification/artifacts/review_S16_01/`

---

### Pass 0 — Setup
- [ ] Fresh venv; install project
- [ ] Record `python --version`
- [ ] Confirm `ag --help` works

---

### Pass 1 — Scope verification
- [ ] Confirm each shipped AF file exists in `/docs/dev/backlog/items/`
- [ ] Confirm internal Status = DONE for each shipped AF
- [ ] Confirm INDEX files updated consistently
- [ ] Confirm GSV v1.3 appears in all governance INDEX + template file headers (AF-0136 AC)

---

### Pass 2 — CI gate (authoritative)
- [ ] `ruff check src tests`
- [ ] `ruff format --check src tests`
- [ ] `pytest -W error`
- [ ] `pytest --cov=src/ag --cov-report=term-missing`

---

### Pass 3 — New convention smoke test
- [ ] Verify no status token in any AF file created during this sprint
- [ ] Verify `test_documentation_drift.py` passes with both old and new filename conventions
- [ ] Verify new SPRINT_DESCRIPTION_TEMPLATE.md has no close/review section
- [ ] Verify new SPRINT_REVIEW_TEMPLATE.md exists with 7-field Cognitive Health block

---

### Pass 4 — Bugs triage (if any discovered)
- [ ] Create bug reports in `/docs/dev/bugs/reports/` using template
- [ ] Link from relevant AF and note in review

---

## Jacob completion
- **Executed by:** Jacob
- **Date:**
- **Evidence folder:** `artifacts/review_S16_01/`
- **Notes:**

---

## B) Review entry (Jeff + Kai)

### Review metadata
- **Reviewed by:** Jeff + Kai
- **Date:**
- **Scope:** Sprint16
- **Decision:** ACCEPT | ACCEPT WITH FOLLOW-UPS | REJECT

---

### What changed (high-level)
*(fill at close)*

---

### Verification performed
*(fill at close)*

---

### Findings
- ✅ What works / improved:
- ⚠️ Issues found (P0/P1/P2):
- 🧩 Follow-ups (AF/BUG/ADR to create):

---

### Sprint Cognitive Health
- Collapse events (INCOMPLETE_IMPL follow-ups): [N]
- Drift events (AF spec revised mid-implementation): [N, list AF IDs]
- Repair events: [informal]
- Agent-initiated HITL gates: [G codes, or "none"]
- Negative test coverage added: [yes / no / partial]
- LLM avoidance events: [N, list AF IDs]
- Integration coverage: [pass / partial / fail — unit-level vs. component-boundary]

---

### Decision rationale
*(fill at close)*

---

### Next actions
- [ ] Close sprint (if ACCEPT / ACCEPT WITH FOLLOW-UPS)
- [ ] Create follow-up AF/BUG items and update indices
- [ ] If REJECT: specify blocking issues and required fixes
- [ ] Update Sprint 16 State → Closed in S16_DESCRIPTION.md and INDEX_SPRINTS.md
