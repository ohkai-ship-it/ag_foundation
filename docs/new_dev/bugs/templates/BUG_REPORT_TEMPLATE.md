# BUG REPORT — BUG#### — <three_word_description>
# Version number: v0.2

> **File naming (required):** `BUG####_<Status>_<three_word_description>.md`  
> Status values: `Open | In progress | Fixed | Verified | Dropped`

---

## Metadata
- **ID:** BUG####
- **Status:** Open | In progress | Fixed | Verified | Dropped
- **Severity:** P0 | P1 | P2
- **Area:** CLI | Core Runtime | Orchestrator | Skills | Storage | Docs | Process | CI
- **Reported by:** <name>
- **Date:** YYYY-MM-DD
- **Related backlog item(s):** AF#### (optional)
- **Related ADR(s):** ADR### (optional)
- **Related PR(s):** #<number> (optional)

---

## Summary
One-paragraph description of the problem.

---

## Expected behavior
What should happen?

---

## Actual behavior
What happens instead?

---

## Reproduction steps
1. ...
2. ...
3. ...

---

## Evidence
- **RunTrace ID(s):** `run_...` (if applicable)
- **CLI output:** (paste excerpt or point to artifact file)
- **Logs:** (paths or excerpts)
- **Artifacts:** `artifact://...` (if applicable)
- **Environment:** OS, Python version, commit hash

---

## Impact
Who/what is affected and how bad is it?

---

## Suspected cause (optional)
Hypothesis only (not a conclusion).

---

## Proposed fix (optional)
Suggested approach (high level).

---

## Acceptance criteria (for verification)
- [ ] Repro steps no longer trigger the issue
- [ ] Tests added/updated (if code change)
- [ ] `pytest -W error` passes
- [ ] `ruff check src tests` passes
- [ ] Evidence captured (new RunTrace ID or test output)

---

## Notes
Anything else.

---

## Status log (optional)
- YYYY-MM-DD — Opened by <name>
- YYYY-MM-DD — Fixed in PR #___
- YYYY-MM-DD — Verified by <name> (run_...)
