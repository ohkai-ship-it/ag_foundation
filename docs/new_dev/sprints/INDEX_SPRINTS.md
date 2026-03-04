# INDEX_SPRINTS
# Version number: v0.2

> **Location (new):** `/docs/new_dev/sprints/INDEX_SPRINTS.md`  
> **Rule:** Each sprint gets a folder under `/docs/new_dev/sprints/documentation/`.

---

## Structure (new)
Each sprint folder:
- `/docs/new_dev/sprints/documentation/Sprint##_three_word_description/`
  - `S##_DESCRIPTION.md` (plan + report)
  - `S##_REVIEW_01.md`
  - `S##_PR_01.md`
  - `artifacts/` (review outputs, traces, logs)

---

## Sprint status
| Sprint | Status | Folder |
|---:|:--:|---|
| Sprint 00 | Closed | (legacy `/docs/dev`) |
| Sprint 01 | Closed | (legacy `/docs/dev`) |
| Sprint 02 | Closed | (legacy `/docs/dev`) |
| Sprint 02 Hardening | Closed | (legacy `/docs/dev`) |
| Sprint 03 | Closed | (legacy `/docs/dev`) |
| Sprint 04 | In Progress | [Sprint04_process_hardening](documentation/Sprint04_process_hardening/) |

---

## Migration notes (legacy → new)
Legacy sprint tracking files live under `/docs/dev/sprints/` today (e.g., `SPRINT_LOG.md`, `SPRINT_REPORT_*`).  
During migration, we:
1) Keep legacy files as historical record under `/docs/dev/`
2) Start Sprint 04 using the new per-sprint folder model under `/docs/new_dev/`
3) Deprecate `SPRINT_LOG.md` (redundant with this index + per-sprint folders)
