# BUG REPORT — BUG0002 — pr_template_version_gap
# Version number: v1.3

---

## Metadata
- **ID:** BUG0002
- **Status:** OPEN
- **Severity:** P2
- **Area:** Docs
- **Reported by:** Jacob (Sprint Review S01_REVIEW_01)
- **Date:** 2026-04-05
- **Related backlog item(s):** AF-0008
- **Related PR(s):** —

---

## Summary
`PULL_REQUEST_TEMPLATE.md` was not bumped to v1.3 during the GSV v1.3 rollout in AF-0008. All other governance INDEX files (4) and templates (5) were updated, but this template remains at v0.2.

---

## Expected behavior
All governance templates should carry the same GSV version (v1.3).

---

## Actual behavior
`docs/dev/sprints/templates/PULL_REQUEST_TEMPLATE.md` header shows `v0.2`.

---

## Reproduction steps
1. Open `docs/dev/sprints/templates/PULL_REQUEST_TEMPLATE.md`
2. Check line 2: `# Version number: v0.2`

---

## Evidence
- **Environment:** Windows, Python 3.14.0, commit 192cb62

---

## Impact
Minor inconsistency. No functional impact.

---

## Proposed fix
Bump the version header to v1.3.

---

## Acceptance criteria (for verification)
- [ ] `PULL_REQUEST_TEMPLATE.md` header shows v1.3
- [ ] `pytest -W error` passes
- [ ] `ruff check src tests` passes
