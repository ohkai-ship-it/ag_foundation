# Pass 7 — Bug Triage
# Sprint 07 Review S07_REVIEW_01
# Date: 2026-03-08
# Executor: Jacob

## Existing Bugs Observed

### BUG-0012: Test Workspace Cleanup Pollution
**Status:** OPEN (unchanged)
**Observed in:** pytest -W error (2 test failures)
**Cause:** SQLite connections not closed after CLI tests
**Impact:** CI discipline requires -W error to pass
**Action:** No new bug, existing BUG-0012 covers this

### BUG-0007: OpenAI Provider Test Isolation
**Status:** OPEN (unchanged)
**Observed in:** Not directly triggered in review
**Note:** Related to SDK caching, separate from BUG-0012
**Action:** No change

---

## New Issues Found

### Issue 1: Invalid Playbook Falls Back to Default
**Severity:** P2 (Minor)
**Description:** When an unknown playbook name is specified, the system silently
falls back to default_v0 instead of failing with an error.
**Observed:** `ag run --playbook nonexistent_playbook` → runs default_v0
**Expected:** Clear error message: "Playbook 'nonexistent_playbook' not found"
**Recommendation:** Create AF for playbook validation
**Action:** AF follow-up, not a blocking bug

### Issue 2: Ruff Format Drift
**Severity:** P2 (Non-blocking)
**Description:** 4 files need reformatting per `ruff format --check`
**Files:**
- src/ag/skills/registry.py
- src/ag/skills/strategic_brief.py
- tests/test_documentation_drift.py
- tests/test_storage.py
**Fix:** Run `ruff format src tests`
**Action:** Quick fix during sprint closure, not a bug

### Issue 3: Index/Filename Status Mismatches
**Severity:** P1 (Process violation)
**Description:** INDEX_BACKLOG.md shows READY for AF0065/AF0068, but files are DONE
**Impact:** Violates Foundation Manual index integrity rule
**Fix:** Update index entries and AF0065 internal status
**Action:** Fix during sprint closure, not a bug

### Issue 4: Stale AF File
**Severity:** P2 (Cleanup)
**Description:** AF0065_Proposed_first_skill_set.md still exists (old version)
**Action:** Delete during sprint closure

---

## Bugs Summary
| Issue | Severity | New Bug? | Action |
|-------|----------|----------|--------|
| SQLite unclosed connections | P1 | No (BUG-0012) | Existing bug |
| Invalid playbook fallback | P2 | Maybe | AF follow-up |
| Ruff format drift | P2 | No | Quick fix |
| Index mismatches | P1 | No | Quick fix |
| Stale AF file | P2 | No | Delete |

---

## AF Follow-Up Recommendations

### AF-XXXX: Playbook Validation on Unknown Names
**Priority:** P2
**Description:** Add validation in CLI to fail when an unknown playbook name is
specified instead of silently falling back to default.
**Acceptance Criteria:**
- `ag run --playbook nonexistent` fails with clear error
- Suggests using `ag playbooks list` to see available playbooks

---

## Review Conclusion
- No new critical bugs found
- BUG-0012 (SQLite warnings) remains the main test infrastructure issue
- Sprint 07 features work correctly
- Index/file cleanup needed before closure
