# Sprint 03 Completion Note — Observability & Truthful UX
# Version number: v1.0

> Sprint closure documentation per COMPLETION_NOTE_TEMPLATE.md

## 1) Metadata
- **Sprint:** Sprint 03 — Observability & Truthful UX
- **Backlog items:** AF-0027 through AF-0033, BUG-0006
- **Author:** Jacob
- **Date:** 2026-02-28
- **Risk level:** P0 (scope complete, no regressions)
- **Runtime mode used for verification:** manual (dev/test-only)

## 2) Goal and acceptance criteria
### Goal (from sprint plan)
Strengthen workspace maturity, fix manual mode gating, and enforce observability + truthful UX.

### Acceptance criteria (from sprint plan)
- [x] Workspace precedence implemented and tested
- [x] Manual mode works with .env AG_DEV=1
- [x] No implicit workspace creation except bootstrap case
- [x] CLI labels trace-derived
- [x] pytest clean (no warnings)
- [x] Coverage maintained ≥ previous sprint

## 3) Delivered Items

| ID | Title | Evidence |
|---:|---|---|
| AF-0027 | Default workspace policy (intuitive precedence) | 5+ workspace policy tests |
| AF-0028 | Run ID truncation fix | Full UUID in `ag runs list` |
| AF-0029 | RunTrace verification hardening | 3 verifier consistency tests |
| AF-0030 | RunTrace metadata completeness (workspace_source) | 2 workspace_source tests |
| AF-0031 | CLI truthfulness enforcement | extract_labels tests |
| AF-0032 | Observability command expansion | `ag runs stats` command |
| AF-0033 | Early .env loading + manual mode gate fix | subprocess dotenv test |
| BUG-0006 | Manual mode .env loading defect | AG_DEV from .env works |

## 4) What changed (summary)

### Core
- `src/ag/core/run_trace.py` — Added `WorkspaceSource` enum, `workspace_source` field, verifier consistency validation

### CLI
- `src/ag/cli/main.py` — Workspace resolution order, `load_dotenv()` early, `ag runs stats`, full run_id display, actionable error messages

### Tests
- `tests/test_cli.py` — Workspace precedence tests, env var fallback, persisted default
- `tests/test_cli_truthful.py` — extract_labels, workspace_source, verifier consistency, stats command

## 5) Architecture alignment
- **Layering:** Workspace resolution is CLI-only (no runtime coupling)
- **Interfaces touched:** RunTrace (new field: workspace_source, new enum: WorkspaceSource)
- **Backward compatibility:** No breaking changes; new field is additive

## 6) Truthful UX check
- **User-visible labels affected:** workspace_source, verifier status, run_id
- **Trace fields backing them:** `RunTrace.workspace_source`, `RunTrace.verifier_status`, `RunTrace.run_id`
- **Proof:** `ag runs show <run_id>` displays trace-derived labels only

## 7) Tests executed

| Command | Result |
|---|---|
| `pytest -W error --ignore=tests/test_providers.py` | 188 passed |
| `pytest --cov=src/ag` | 76% overall |
| `ruff check .` | All checks passed |

## 8) Coverage metrics

| Module | Coverage |
|---|---|
| run_trace | 100% |
| task_spec | 100% |
| config | 100% |
| runtime | 95% |
| sqlite_store | 96% |
| workspace | 97% |
| **Overall** | **76%** |

## 9) Deferred Items

| ID | Status | Reason |
|---:|---|---|
| AF-0034 | Ready | Error hardening — next sprint candidate |
| AF-0035 | Ready | Help text polish — low priority |
| AF-0036 | Proposed | Global flag removal — needs design |
| AF-0037 | Ready | Error standardization — next sprint candidate |
| AF-0038 | Ready | JSON error consistency — next sprint candidate |

## 10) Risks and follow-ups
- **Risks introduced:** None
- **Tradeoffs made:** None
- **Follow-up items:** AF-0034 through AF-0038 queued for Sprint 04

## 11) Sign-off statement

Sprint 03 delivered all P0 items (AF-0027 through AF-0033) and resolved BUG-0006.
All tests pass (188), coverage maintained (76%), Ruff clean, no regressions.
Review: APPROVED — see [REVIEW_S03_FINDINGS.md](../reviews/entries/REVIEW_S03_2026-02-27/REVIEW_S03_FINDINGS.md)

**Sprint 03 is CLOSED.**
