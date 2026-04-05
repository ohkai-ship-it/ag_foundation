# INDEX_BUGS
# Version number: v1.3

> **FOUNDATION RULE**
> INDEX integrity is mandatory.
> Status must match between internal file metadata and INDEX row.
> Update required:
> - at sprint start ritual
> - whenever status changes
> See `/docs/dev/foundation/FOUNDATION_MANUAL.md` → Section 7: Index Discipline.

> **Location:** `/docs/dev/bugs/INDEX_BUGS.md`
> **Naming:** See SPRINT_MANUAL §2 for naming conventions (legacy and new).
> Status values: `OPEN | FIXED | DROPPED`
> **Linking convention (new entries):** Link column is the sole file reference: `[🔗](reports/filename)`

---

## OPEN bugs
| ID | Severity | Status | Title | Area | Filename |
|---:|:--:|:--|---|---|---|
| BUG-0001 | P2 | OPEN | Leftover READY duplicates (5 AF files) | Process | [🔗](reports/BUG0001_leftover_ready_duplicates.md) |
| BUG-0002 | P2 | OPEN | PR template version gap (v0.2 → v1.3) | Docs | [🔗](reports/BUG0002_pr_template_version_gap.md) |

---

## FIXED bugs
(none)

---

## How to use
1. Create bug report from `/docs/dev/bugs/templates/BUG_REPORT_TEMPLATE.md`
2. Link bug from PR and/or AF item
3. Update status in:
   - bug filename
   - bug metadata
   - this index
