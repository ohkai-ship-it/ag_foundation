# Sprint 08 Review - Bugs Triage
# Date: 2026-03-09
# Executor: Jacob

## New Bugs Discovered This Sprint

### BUG-0013 (P1) - research_v0 playbook pipeline broken
- **File:** `/docs/dev/bugs/reports/BUG0013_OPEN_research_v0_pipeline_broken.md`
- **Severity:** P1
- **Status:** OPEN
- **Summary:** research_v0 playbook fails to pass documents between fetch_web_content and synthesize_research steps
- **Root cause:** Pipeline data flow issue - documents not passed correctly through runtime
- **Impact:** Core playbook feature (multi-step data passing) does not work

## Pre-existing Bugs (Not Sprint 08 Issues)

### BUG-0012 (P2) - Test workspace cleanup pollution
- **Status:** OPEN  
- **Observed:** SQLite ResourceWarning in `pytest -W error`
- **Note:** This causes 1 test failure with strict warnings

### BUG-0007 (P1) - OpenAI provider test isolation failure
- **Status:** OPEN
- **Note:** Pre-existing, not triggered in Sprint 08

## Bugs Fixed This Sprint
None formally closed, but:
- V1 skill stubs removed (potential source of confusion eliminated)
- V2 skill descriptions now display correctly in `ag skills list`

## Recommendations
1. **BUG-0013** should block Sprint 08 close or be accepted as a known P1
2. **BUG-0012** needs investigation to determine if SQLite connection handling regressed
3. Consider running `pytest -W error` in CI to catch warnings early
