# Bug Triage  S15_REVIEW_01

## Pre-filed bugs (all present and in INDEX)
| ID | File | Status | Verified |
|---|---|---|---|
| BUG-0022 | BUG0022_OPEN_v3planner_cli_test_flakiness.md | OPEN | YES  9 expected skips in test suite |
| BUG-0023 | BUG0023_OPEN_v2_pipeline_evidence_hidden.md | OPEN | YES  logging.WARNING bleed observed in cli_outputs.txt |
| BUG-0024 | BUG0024_OPEN_planner_duplicates_emit_result.md | OPEN | YES  load_documents repair failures observed |

## New bugs found during review
None requiring new filing.

## Test regression discovered and fixed
- TestInlinePlanConfirmRun (4 tests) failed because mocks targeted plan() after BUG-0023
  fix switched code to plan_with_metadata(). Fixed in commit cfd1a0f  not a new BUG entry,
  treated as BUG-0023 followup test fix.
