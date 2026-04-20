# BACKLOG ITEM — AF0087 — policy_hook_validation
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - Policy enforcement in runtime behavior
>
> **File naming (required):** `AF####_<STATUS>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0087
- **Type:** Engineering / Testing
- **Status:** DONE
- **Priority:** P1
- **Area:** Core Runtime / Policy
- **Owner:** Jacob
- **Target sprint:** Sprint 09 (completed)
- **Depends on:** None

---

## Problem

Policy hooks are documented as architecture constraints but are not yet covered by explicit runtime tests.

This creates a reliability and safety gap for bounded autonomy:
- hook presence may drift from behavior
- regressions can pass without clear policy evidence
- sprint review cannot prove policy checks executed on touched paths

---

## Goal

Establish a **policy hook runtime validation baseline** that proves policy checks are executed and trace-visible in relevant runtime paths.

---

## Non-goals

- Building a new policy engine
- Expanding autonomy scope
- Introducing external policy infrastructure

---

## Acceptance criteria (Definition of Done)

- [x] Runtime paths that use policy hooks are identified and documented
- [x] Tests verify policy checks execute on touched paths
- [x] Failure paths preserve explicit, traceable policy outcomes
- [x] Workspace isolation behavior remains intact when policy checks fail
- [x] `pytest -W error` passes with the new policy tests enabled

---

## Implementation notes

### Scope

1. Map current policy-hook call points in runtime/orchestration paths
2. Add focused tests (happy + failure) for:
   - permission/confirmation checks where applicable
   - budget/check guard behavior where applicable
   - deterministic failure signaling
3. Ensure trace/output evidence is consistent with truthful UX constraints

### Candidate files

- `src/ag/core/runtime.py`
- `tests/test_runtime.py`
- `tests/test_cli_truthful.py` (if user-visible labels affected)

---

## Risks

| Risk | Mitigation |
|------|------------|
| Over-scoping into full policy system | Keep to validation baseline only |
| Brittle tests tied to internals | Focus assertions on behavior + trace outcomes |

---

## Context

This item supports Sprint09 reliability and safety hardening and Gate A readiness from `/docs/dev/foundation/PROJECT_PLAN_0.2.md`.

Related:
- AF-0046 test isolation framework
- AF-0071 warning-clean test discipline
- AF-0083 artifact evidence strategy

---

# Completion section

**Completed:** Sprint 09 (2026-03-11)

## Policy Hooks Identified and Documented

| Policy Hook | Location | Purpose |
|-------------|----------|---------|
| **Normalizer validation** | `V0Normalizer.normalize()` | Rejects empty prompts, missing workspace |
| **Verifier validation** | `V0Verifier.verify_components()` | Fails on step errors, non-success status |
| **Workspace isolation** | `SQLiteRunStore`, `SQLiteArtifactStore` | Scopes data to workspace_id |
| **Manual mode gate** | `_check_manual_mode_gate()` in CLI | Requires AG_DEV=1 |
| **Playbook validation** | CLI `run` command (AF-0072) | Rejects invalid playbook names |

## Tests Added

Added 11 policy validation tests in `tests/test_runtime.py`:

### TestPolicyNormalizerValidation (4 tests)
- `test_empty_prompt_rejected` — empty prompt raises ValueError
- `test_whitespace_only_prompt_rejected` — whitespace prompt raises ValueError
- `test_missing_workspace_rejected` — None workspace raises ValueError
- `test_valid_task_passes_policy` — valid input creates TaskSpec

### TestPolicyVerifierValidation (3 tests)
- `test_step_error_fails_verification` — step with error returns "failed"
- `test_non_success_final_status_fails_verification` — non-SUCCESS returns "failed"
- `test_successful_run_passes_verification` — all-success returns "passed"

### TestPolicyWorkspaceIsolation (2 tests)
- `test_workspaces_isolated` — different workspaces maintain separate histories
- `test_run_scoped_to_workspace` — run can only be retrieved from correct workspace

### TestPolicyTraceEvidence (2 tests)
- `test_failure_reason_in_trace` — failure reasons recorded in trace
- `test_success_outcome_traceable` — success outcomes have required evidence fields

## Run Evidence

```
pytest -W error -q
445 passed, 3 deselected in 17.18s
```

## Files Changed

- `tests/test_runtime.py`: Added Policy Validation test classes (11 tests)
