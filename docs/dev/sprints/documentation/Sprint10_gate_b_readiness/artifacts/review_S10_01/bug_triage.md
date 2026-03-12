# Bug Triage — Sprint 10
# Date: 2026-03-12
# Triaged by: Kai (manual testing)

## Bugs Discovered

### BUG-0015: Runs list count mismatch
- **Severity:** P2
- **Status:** OPEN
- **File:** `/docs/dev/bugs/reports/BUG0015_OPEN_runs_list_count_mismatch.md`
- **Summary:** `ag runs list --all` shows inflated total count (46) but only displays 15 runs. Caused by orphaned SQLite index entries referencing deleted trace files.
- **Root cause:** Filesystem cleanup (trace file deletion) doesn't sync with SQLite index.
- **Impact:** Misleading UX — user sees "46 total" but only 15 are retrievable.
- **Recommended fix:** Either:
  1. `list()` method should update count to reflect actual retrievable runs
  2. Add index cleanup/vacuum command
  3. Sync SQLite entries when runs are deleted

## New Backlog Items (from testing observations)

### AF-0094: Trace full I/O enrichment
- **Priority:** P3
- **Status:** PROPOSED
- **Origin:** Deferred Phase 2 from AF-0090
- **Summary:** Trace lacks full step input/output data. Only summaries (~50 chars) are captured, making debugging and auditing difficult.

### AF-0095: research_v0 skill output audit
- **Priority:** P2
- **Status:** PROPOSED
- **Origin:** Manual testing of research_v0 playbook
- **Summary:** Observed discrepancies between skill behavior and CLI reporting. Need systematic audit of research pipeline data flow.

## Existing Bugs Status

| Bug ID | Status | Notes |
|--------|--------|-------|
| BUG-0002 | OPEN | Missing ag run options — partially addressed by AF-0012 (deferred options documented) |
| BUG-0003 | Open→Closed? | Missing CLI subcommands — addressed by AF-0012 stubs |
| BUG-0011 | OPEN | Default workspace name leaked — needs review |
| BUG-0015 | OPEN | New — runs list count mismatch |

## Recommendations

1. Close BUG-0003 after AF-0012 verification (stubs added)
2. Keep BUG-0002 open (deferred ag run options noted in CLI_REFERENCE)
3. Review BUG-0011 in Sprint 11
4. Address BUG-0015 in Sprint 11 (storage/index sync)
