# Sprint Report — Sprint 02 Hardening Extension
# Version number: v0.1

## Metadata
- **Sprint:** Sprint 02 Hardening Extension — Storage, Coverage, Config, Workspace Policy
- **Dates:** 2026-02-26
- **Trigger:** BUG-0004 discovery (SQLite connection leak) + sign-off verification findings

## Outcome summary
- Fixed critical SQLite connection leak (BUG-0004)
- Fixed implicit workspace creation bug (BUG-0005)
- Implemented workspace selection policy (AF-0026)
- Achieved coverage targets: 90%+ overall, 96% storage, 96% providers
- Test count: 173 → 174 (+1 test, +5 regression tests for AF-0026)
- All tests pass with `-W error` (no warnings)

## Completed work
- ✅ BUG-0004 — SQLite connections not closed → ResourceWarning (Fixed)
- ✅ BUG-0005 — Implicit workspace creation on ag run (Fixed)
- ✅ AF-0021 — Storage lifecycle hardening (SQLite deterministic closure)
- ✅ AF-0022 — Provider coverage hardening (≥95% target)
- ✅ AF-0023 — Environment & configuration hardening
- ✅ AF-0024 — Workspace lifecycle correction (ag ws create/list)
- ✅ AF-0025 — Test discipline enforcement (Ruff + docs)
- ✅ AF-0026 — Workspace selection policy enforcement

## Not completed / carried over
None — all hardening items completed.

## Evidence
- Review entries:
  - `docs/dev/reviews/entries/REVIEW_S02_2026-02-26_SIGNOFF_FINDINGS.md`
- Completion notes:
  - `docs/dev/backlog/completion/2026-02-26_AF-0021_storage-lifecycle-hardening.md`
  - `docs/dev/backlog/completion/2026-02-26_AF-0022_provider-coverage-hardening.md`
  - `docs/dev/backlog/completion/2026-02-26_AF-0023_environment-configuration-hardening.md`
  - `docs/dev/backlog/completion/2026-02-26_AF-0024_workspace-lifecycle-correction.md`
  - `docs/dev/backlog/completion/2026-02-26_AF-0025_test-discipline-enforcement.md`
  - `docs/dev/backlog/completion/2026-02-26_AF-0026_workspace-selection-policy.md`
- Bug reports:
  - `docs/dev/bugs/reports/BUG-0004-sqlite-connection-leak.md`
  - `docs/dev/bugs/reports/BUG-0005-implicit-workspace-creation.md`

## Metrics
- Items completed: 8 (2 bugs + 6 AF items)
- Tests added: 5 (workspace selection policy regression tests)
- Bugs opened: 1 (BUG-0005, discovered during sign-off)
- Bugs closed: 2 (BUG-0004, BUG-0005)
- Coverage: 90%+ overall (target met)

## Coverage breakdown
| Module | Target | Achieved |
|--------|--------|----------|
| Overall | 90% | 90% |
| CLI | 73% | 73% |
| Providers | 95% | 96% |
| Storage | 95% | 96% |
| Config | 90% | 98% |

## Learnings
### What worked
- Sign-off verification process caught workspace proliferation bug (BUG-0005)
- Context manager pattern for SQLite connections is clean and Pythonic
- Workspace selection policy provides clear user guidance
- Regression tests prevent future implicit behavior

### What to improve next sprint
- Consider pre-commit hooks for Ruff enforcement
- Integration tests need real API keys (CI secret management)
- Config file support (.ag.toml) would improve UX

## Breaking changes
- **Workspace selection policy (AF-0026):** `ag run` now requires explicit workspace selection via `--workspace` flag or `AG_WORKSPACE` env var. No implicit workspace creation.

## Next sprint candidate slice
- P1: AF-0012 (CLI surface parity), AF-0013 (contract hardening)
- P2: AF-0015 (DB filename mismatch)
