# S##_REVIEW — Sprint## — <sprint_name>
#### Description: Template for sprint reviews. A sprint review documents outcomes, cognitive health metrics, and learnings from a completed sprint. Filled during Phase 4 (Review) and finalized at sprint close. Copy into the sprint folder, rename per naming conventions (SP Appendix C.3), and fill all sections.
#### Convergent: v1.3.2
#### governs: <project_name>

> **FOUNDATION GOVERNANCE**
> This file is governed by: `foundation/SPRINT_PLAYBOOK.md`

---

## 1) Metadata
- **Sprint:** Sprint##
- **Branch:**
- **PR:** #<number>

- **Status:** PROPOSED | READY | BLOCKED | DONE | DEPRECATED
- **PRIORITY:** P0 | P1 | P2
- **Area:** CLI | Core Runtime | Orchestrator | Skills | Storage | Docs | Process | CI

- **PROPOSED:** DD-MM-YYYY, hh:mm
- **Started implementation:** DD-MM-YYYY, hh:mm
- **DONE:** DD-MM-YYYY, hh:mm

- **Related backlog item(s):** AF#### (optional)
- **Related bug(s):** BUG#### (optional)
- **Related PR(s):** #<number> (optional)


- **Models:**
- **Description:** (1-3 sentences)

---

## Work Items

| ID | Title | Status | Notes |
|---:|---|:--:|---|
| AF-#### | <title> | PROPOSED / READY / DONE / BLOCKED / DEPRECATED | |
| AF-#### | <title> | PROPOSED / READY / DONE / BLOCKED / DEPRECATED | |

---

## Review Decision

- **Decision:** ACCEPTED / ACCEPT WITH FOLLOW-UPS / REJECTED
- **Rationale:** *(1–2 sentences)*
- **Follow-ups:** *(AF/BUG IDs, or "none")*
- **PR link:**

> See SP Step 5.2 for quick fix budget.

---

## Sprint Cognitive Health (see SP Step 4.3)

> Collated from per-AF Cognitive Observations during Run Review (Phase P4).

| Field | Value |
|-------|-------|
| **Sprint velocity** | AFs completed / AFs planned |
| **Ceremony time** | Estimated total time spent on governance overhead |
| **Blocked time** | Time lost to blockers, unclear scope, or escalations |
| **Scope changes** | AFs added, deferred, or dropped mid-sprint |
| **Tool friction** | Any tooling issues (CI, git, templates) that slowed work |
| **Decision quality** | Were escalations timely? Were decisions clear? |
| **Carry-forward** | Lessons or patterns to apply in next sprint |

**Per-AF aggregation:**

- **Collapse events** (INCOMPLETE_IMPL follow-ups): [total count, list AF IDs]
- **Drift events** (AF spec revised mid-implementation): [total count, list AF IDs]
- **Repair events:** [summary across AFs]
- **Agent-initiated HITL gates:** [gate codes, or "none"]
- **LLM avoidance events:** [total count, list AF IDs]
- **Patterns observed:** [free text — recurring type hints, phase clusters, etc.]

> **Type hints** (optional tags from per-AF observations):
> data error · process skip · misinterpretation · scope violation · stale input · validation gap

---

## Learnings (optional, 2–3 bullets)

- 

---

## References

- Sprint execution: `foundation/SPRINT_PLAYBOOK.md`
