# BACKLOG ITEM — AF0091 — verifier_failure_path_maturity
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI discipline (ruff + pytest -W error + coverage)
> - 1 PR = 1 primary AF
> - INDEX update rule (status ↔ filename integrity)

> **File naming (required):** `AF####_<STATUS>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0091
- **Type:** Feature / Investigation
- **Status:** READY
- **Priority:** P1
- **Area:** Core Runtime / Verifier
- **Owner:** TBD
- **Target sprint:** Sprint 10
- **Depends on:** AF-0087 (policy hook validation baseline — DONE Sprint 09)

---

## Problem

Gate B (Guided Autonomy) requires:
- "Verifier outcomes consistent across happy and failure paths"
- "Retry/failure behavior testable and deterministic"

Currently:
1. **No failure-path verifier tests** — verifier is only exercised in happy-path scenarios
2. **Retry/timeout behavior undocumented** — no explicit test coverage for retry semantics
3. **Verifier decision matrix absent** — no documented mapping of input conditions → verifier outcomes
4. **Inconsistent status under errors** — provider errors, invalid inputs, and timeouts may
   produce different verifier statuses depending on code path

### Evidence
- AF-0087 (Sprint 09) established policy hook validation baseline but focused on
  policy enforcement, not verifier consistency under failure
- Sprint 09 review captured happy and failure traces but did not systematically
  verify verifier status consistency across failure types

---

## Goal

Make verifier behavior deterministic and testable for all failure modes:
1. Audit verifier outcomes under each failure type
2. Add explicit test coverage for non-happy-path verifier behavior
3. Document verifier decision matrix
4. Ensure retry/timeout behavior is deterministic and trace-recorded

---

## Non-goals

- Changing verifier pass/fail semantics fundamentally
- Adding new verifier types or strategies
- Implementing automatic retry (just validating existing behavior)
- Policy engine redesign (that's Phase 3 / Gate C territory)

---

## Investigation Scope

### Failure Scenarios to Verify

| Scenario | Expected Verifier Status | Current Coverage |
|----------|--------------------------|-----------------|
| Invalid skill input | FAIL with validation error | ❓ Unknown |
| Provider timeout | FAIL with timeout reason | ❓ Unknown |
| Provider error (API 500) | FAIL with provider error | ❓ Unknown |
| Provider auth failure | FAIL with auth error | ❓ Unknown |
| Skill raises exception | FAIL with exception detail | ❓ Unknown |
| Empty/null skill output | FAIL or SKIP? | ❓ Unknown |
| Playbook step skip condition | SKIP with reason | ❓ Unknown |
| Policy rejection | FAIL with policy violation | Partial (AF-0087) |

### Key Files to Investigate
- `src/ag/core/runtime.py` — orchestrator error handling
- `src/ag/core/run_trace.py` — verifier status recording
- `src/ag/core/interfaces.py` — verifier interface
- `src/ag/providers/` — provider error types
- `tests/test_runtime.py` — existing verifier coverage

---

## Acceptance criteria (Definition of Done)

- [ ] Verifier decision matrix documented (scenario → expected status → actual status)
- [ ] Each failure scenario in the matrix has explicit test coverage
- [ ] Verifier produces consistent status for identical failure scenarios (deterministic)
- [ ] Retry/timeout behavior has explicit tests showing deterministic outcomes
- [ ] Failure-path traces include verifier outcome with rationale in trace.json
- [ ] No regressions in existing happy-path verifier tests
- [ ] `ruff check src tests` passes
- [ ] `pytest -W error` passes

---

## Implementation Notes

### Phase 1: Audit (Investigation)
1. Map all code paths that invoke verifier
2. Inject each failure type and record actual verifier status
3. Document findings in decision matrix table

### Phase 2: Fix inconsistencies
1. Ensure error → verifier status mapping is consistent
2. Add explicit error type handling if missing
3. Ensure trace records verifier rationale for all outcomes

### Phase 3: Test coverage
1. Add parametrized test for each failure scenario
2. Verify deterministic behavior (run twice, same result)
3. Verify trace content matches verifier status

---

## Risks

| Risk | Mitigation |
|------|------------|
| Verifier changes break happy-path behavior | Run full test suite before/after |
| Provider error types vary by backend | Test with stub provider for consistency |
| Retry semantics may need design decision | Document current behavior first, propose changes separately |

---

## Related Items

- **AF-0087:** Policy hook validation baseline (DONE — established enforcement checks)
- **AF-0090:** Artifact evidence deepdive (related — both are Gate B prerequisites)
- **Gate B:** Guided Autonomy (this AF directly addresses a Gate B requirement)
