# BUG REPORT — BUG#### — <three_word_description>
#### Description: Template for bug reports. A BUG documents a defect with reproduction steps, expected vs. actual behavior, and root cause analysis. Each BUG progresses through the status lifecycle and is tracked in INDEX_BUGS. Copy, rename per naming conventions (SP Appendix C.3), and fill all sections.
#### Convergent: v1.3.2
#### governs: <project_name>

---

> **FOUNDATION GOVERNANCE**
> This file is governed by: `foundation/SPRINT_PLAYBOOK.md`

---

## Metadata
- **BUG:** BUG####
- **Owner:** <name>

- **Status:** PROPOSED | READY | BLOCKED | DONE | DEPRECATED
- **PRIORITY:** P0 | P1 | P2
- **Area:** CLI | Core Runtime | Orchestrator | Skills | Storage | Docs | Process | CI

- **PROPOSED:** DD-MM-YYYY, hh:mm
- **Started implementation:** DD-MM-YYYY, hh:mm
- **DONE:** DD-MM-YYYY, hh:mm

- **Related backlog item(s):** AF#### (optional)
- **Related ADR(s):** ADR### (optional)
- **Related PR(s):** #<number> (optional)

- **Models:**
- **Description:** (1-3 sentences)

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
- [ ] Evidence captured (new RunTrace ID or test output)

---

## Notes
Anything else.

---

## References

- Sprint execution: `foundation/SPRINT_PLAYBOOK.md`