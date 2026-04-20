# Sprint Report — Sprint 03 — Observability & Truthful UX
# Version number: v1.0

## Metadata
- **Sprint:** Sprint 03 — Observability & Truthful UX
- **Dates:** 2026-02-27 → 2026-02-28

## Outcome summary
- Shipped intuitive workspace resolution order (CLI → persisted → env → bootstrap → error)
- Shipped RunTrace metadata completeness with `workspace_source` field
- Shipped verifier consistency validation in trace schema
- Fixed manual mode .env loading (BUG-0006)
- Shipped `ag runs stats` observability command
- Test count: 178 → 188 (+10 tests)
- Coverage: 90% → 76% (adjusted for providers exclusion from main test run)

## Completed work
- ✅ AF-0027 — Default workspace policy (intuitive precedence)
- ✅ AF-0028 — Run ID truncation fix
- ✅ AF-0029 — RunTrace verification hardening
- ✅ AF-0030 — RunTrace metadata completeness (workspace_source)
- ✅ AF-0031 — CLI truthfulness enforcement
- ✅ AF-0032 — Observability command expansion (`ag runs stats`)
- ✅ AF-0033 — Early .env loading + manual mode gate fix
- ✅ BUG-0006 — Manual mode .env loading defect (resolved)

## Not completed / carried over
- ⏭️ AF-0034 — Workspace error hardening — Ready (Sprint 04 candidate)
- ⏭️ AF-0035 — Clarify --workspace help text — Ready (low priority)
- ⏭️ AF-0036 — Remove global CLI flags — Proposed (needs design)
- ⏭️ AF-0037 — Standardize workspace errors — Ready (Sprint 04 candidate)
- ⏭️ AF-0038 — JSON error path consistency — Ready (Sprint 04 candidate)

## Evidence
- Review entries:
  - `docs/dev/reviews/entries/REVIEW_S03_2026-02-27/REVIEW_S03_FINDINGS.md`
- Completion note:
  - `docs/dev/sprints/S03_COMPLETION_NOTE.md`
- Sprint plan:
  - `docs/dev/sprints/SPRINT_03_PLAN.md`

## Metrics
- PR count: N/A (direct-to-main development environment)
- Tests added: 10 (178 → 188)
- Bugs opened: 0
- Bugs closed: 1 (BUG-0006)

### Coverage breakdown
| Module | Coverage |
|---|---|
| run_trace | 100% |
| task_spec | 100% |
| config | 100% |
| runtime | 95% |
| sqlite_store | 96% |
| workspace | 97% |
| cli/main | 74% |
| **Total** | **76%** |

## Learnings
### What worked
- Workspace resolution order is now predictable and documented
- WorkspaceSource enum provides audit trail for where workspace came from
- Early `load_dotenv()` pattern ensures .env is respected before any env var checks
- Verifier consistency validation catches trace corruption early

### What to improve next sprint
- Error message hardening (AF-0034, AF-0037) for better UX
- Consider JSON output consistency for error paths (AF-0038)
- Provider test coverage excluded from main run — needs integration test strategy

## Next sprint candidate slice
- P0: None critical
- P1: AF-0034 (error hardening), AF-0037 (error standardization)
- P2: AF-0035 (help text), AF-0038 (JSON errors)

## Risk summary
No P0/P1 risks remain open. Sprint delivered all committed scope.
