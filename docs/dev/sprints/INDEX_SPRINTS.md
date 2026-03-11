# INDEX_SPRINTS
# Version number: v0.2

> **FOUNDATION RULE**
> INDEX integrity is mandatory.
> Sprint status must be kept current.
> Update required:
> - at sprint start ritual
> - whenever sprint status changes
> See `/docs/dev/foundation/FOUNDATION_MANUAL.md` → Section 7: Index Discipline.

> **Location:** `/docs/dev/sprints/INDEX_SPRINTS.md`
> **Rule:** Each sprint gets a folder under `/docs/dev/sprints/documentation/`.

---

## Structure (new)
Each sprint folder:
- `/docs/dev/sprints/documentation/Sprint##_three_word_description/`
  - `S##_DESCRIPTION.md` (plan + report)
  - `S##_REVIEW_01.md`
  - `S##_PR_01.md`
  - `artifacts/` (review outputs, traces, logs)

---

## Sprint status
| Sprint | Status | Folder |
|---:|:--:|---|
| Sprint 00 | Closed | (legacy `/docs/old_dev`) |
| Sprint 01 | Closed | (legacy `/docs/old_dev`) |
| Sprint 02 | Closed | (legacy `/docs/old_dev`) |
| Sprint 02 Hardening | Closed | (legacy `/docs/old_dev`) |
| Sprint 03 | Closed | (legacy `/docs/old_dev`) |
| Sprint 04 | Closed | [Sprint04_process_hardening](documentation/Sprint04_process_hardening/) |
| Sprint 05 | Closed | [Sprint05_High_Pressure_Skills](documentation/Sprint05_High_Pressure_Skills/) |
| Sprint 06 | Closed | [Sprint06_skill_foundation](documentation/Sprint06_skill_foundation/) |
| Sprint 07 | Closed | [Sprint07_summarize_playbook](documentation/Sprint07_summarize_playbook/) |
| Sprint 08 | Closed | [Sprint08_skills_playbooks_maturity](documentation/Sprint08_skills_playbooks_maturity/) |
| Sprint 09 | Active | [Sprint09_reliability_safety_hardening](documentation/Sprint09_reliability_safety_hardening/) |
| Sprint 10 | Preliminary | (backlog planning only) |

---

## Migration notes (legacy → new)
Legacy sprint tracking files live under `/docs/dev/sprints/` today (e.g., `SPRINT_LOG.md`, `SPRINT_REPORT_*`).  
During migration, we:
1) Keep legacy files as historical record under `/docs/dev/`
2) Start Sprint 04 using the new per-sprint folder model under `/docs/dev/`
3) Deprecate `SPRINT_LOG.md` (redundant with this index + per-sprint folders)
