# S18_REVIEW — Sprint18 — cli_ux_polish
# Convergent version: v1.3.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
> `/docs/dev/foundation/SPRINT_MANUAL.md`
>
> This is the **outcomes** artifact. Written at sprint close.
> Planning lives in `S18_DESCRIPTION.md`.

---

## Sprint Reference
- **Sprint:** Sprint18
- **Name:** cli_ux_polish
- **PR:** #13
- **Models:** Claude Opus 4 (Copilot)

---

## Work Items

| ID | Title | Status | Notes |
|---:|---|:--:|---|
| AF-0147 | `ag playbooks show` command | DONE | Full implementation: Rich display + JSON output. 7 new tests. Commit 0036555. |
| AF-0144 | `ag runs list` filter expansion | DONE | Added --playbook, --mode filters. 5 new tests. Commit 304a394. |
| AF-0145 | `ag doctor` diagnostic expansion | DONE | 3 new checks: DB integrity, provider credentials, artifact storage. 8 new tests. Commit 0faf7e6. |

---

## Review Decision

- **Decision:** ACCEPTED
- **Rationale:** All 3 AFs delivered as scoped, 814 tests pass, no blockers, no scope changes. First code sprint under v1.3.1 validated cleanly.
- **Follow-ups:** none
- **PR link:** TBD

> **Decision rules:**
> - **ACCEPTED** — Close sprint. Merge PR.
> - **ACCEPT WITH FOLLOW-UPS** — Create follow-up AFs. Close sprint. Merge PR.
> - **REJECTED** — Sprint status → `REJECTED`. Branch preserved (not deleted). No merge. Record rejection rationale + learnings.
>
> **Quickfix budget:** 30 min **total cumulative** for in-sprint fixes before close. Human-overridable ad hoc.

---

## Sprint Cognitive Health (see SM §8.8)

| Field | Value |
|-------|-------|
| **Sprint velocity** | 3/3 AFs completed |
| **Ceremony time** | ~15 min (sprint start ritual + close ritual) |
| **Blocked time** | 0 — no blockers encountered |
| **Scope changes** | None — all 3 AFs shipped as planned |
| **Tool friction** | Minor: ruff caught import sorting + formatting issues in tests — fixed immediately |
| **Decision quality** | Clean — Q1 (step table columns) and Q2 (--mode semantics) resolved at G1 with no escalation |
| **Carry-forward** | JSON output pattern: use `print()` not `console.print()` to avoid Rich ANSI artifacts |

---

## Learnings (optional, 2–3 bullets)

- Lightweight CLI polish sprint was a good v1.3.1 validation target — governance overhead stayed proportional to work size.
- The `print()` vs `console.print()` distinction for JSON output is a recurring pattern worth remembering for future CLI work.
- All 3 AFs were truly independent — no merge conflicts, no ordering dependencies. Good sprint scoping.
