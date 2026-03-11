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
- **Status:** PROPOSED
- **Priority:** P1
- **Area:** Core Runtime / Policy
- **Owner:** TBD
- **Target sprint:** Sprint09
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

- [ ] Runtime paths that use policy hooks are identified and documented
- [ ] Tests verify policy checks execute on touched paths
- [ ] Failure paths preserve explicit, traceable policy outcomes
- [ ] Workspace isolation behavior remains intact when policy checks fail
- [ ] `pytest -W error` passes with the new policy tests enabled

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

# Completion section (fill when done)

## 1) Metadata
- **Backlog item (primary):** AF0087
- **PR:** #<number>
- **Author:** <name>
- **Date:** YYYY-MM-DD
- **Branch:** <feature/policy-hook-validation>
- **Risk level:** P1
- **Runtime mode used for verification:** manual
