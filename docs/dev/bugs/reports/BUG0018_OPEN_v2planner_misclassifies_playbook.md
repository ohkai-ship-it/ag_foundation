# BUG REPORT — BUG-0018 — V2Planner misclassifies playbook as skill
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI discipline (ruff + pytest -W error + coverage)
> - INDEX update rule (status ↔ filename integrity)
> - Evidence capture requirement (RunTrace ID for CLI/runtime bugs)

> **File naming (required):** `BUG####_<STATUS>_<three_word_description>.md`
> Status values: `OPEN | IN_PROGRESS | FIXED | VERIFIED | DROPPED`

---

## Metadata
- **ID:** BUG-0018
- **Status:** OPEN
- **Severity:** P1
- **Area:** Core Runtime / Planner
- **Reported by:** Kai
- **Date:** 2026-03-22
- **Related backlog item(s):** AF-0103 (V2 Planner), AF-0104 (V3 Planner feasibility)
- **Related ADR(s):** —
- **Related PR(s):** —

---

## Summary

The V2Planner's LLM sometimes classifies a playbook (e.g. `research_v0`) as a skill step (`"type": "skill"`), causing the orchestrator to fail with `Skill not found: research_v0`. The validation in `_validate_v2_steps()` does not cross-check skill step names against the playbook catalog, so the misclassification passes validation and only fails at execution time.

---

## Expected behavior

When the LLM returns `{"type": "skill", "skill": "research_v0"}` and `research_v0` is a playbook:
- Validation should detect the mismatch (name exists as playbook, not as skill)
- Either auto-correct to `{"type": "playbook", "playbook": "research_v0"}` with a warning, or raise a clear validation error

---

## Actual behavior

- `_validate_v2_steps()` checks `skill_registry.has("research_v0")` → fails
- The step passes through and fails at orchestrator execution
- Run fails: `Required step 'research_v0_0' failed: 'Skill not found: research_v0'`

---

## Reproduction steps

1. Run: `ag run -y "Wetterbericht Düsseldorf"`
2. V2Planner generates plan with `research_v0` as a skill step
3. Orchestrator fails: `Skill not found: research_v0`

---

## Evidence

- **RunTrace ID:** `25495bba-224e-4c56-9371-eca8ffe546ce`
- **CLI output:**
  ```
  Run completed
  Plan ID: plan_3cc22f88cd1a
  Run ID: 25495bba-224e-4c56-9371-eca8ffe546ce
  Workspace: ws01
  Autonomy: guided (inline plan)
  Status: failure
  Verifier: failed
  Duration: unknown
  Playbook: v2plan_ca9c83c6@1.0.0

  Error: Required step 'research_v0_0' failed: 'Skill not found: research_v0'
  ```
- **Environment:** Windows 11, Python 3.14.0a6, commit `04b1e9e` on `feat/sprint13-intelligent-pipeline`

---

## Root cause

`_validate_v2_steps()` in `planner.py` validates skill steps against `skill_registry` and playbook steps against `get_pb()`, but never cross-checks namespaces. The LLM conflates playbook names with skill names.

---

## Proposed fix

**Decision (2026-03-22, Kai):** Auto-correct + warn (maximize success rate; LLM retry is expensive and may repeat the same error).

### Fix 1: Cross-check validation in `_validate_v2_steps()` (required)

Add bi-directional cross-check with these rules:
1. `type=skill` but name exists only as playbook → auto-correct to `type=playbook`, log warning
2. `type=playbook` but name exists only as skill → auto-correct to `type=skill`, log warning
3. Name exists in *neither* namespace → raise `PlannerError` (current behavior, correct)
4. Name exists in *both* namespaces → trust the declared type (unlikely edge case, but safe)

### Fix 2: Improve V2 system prompt (recommended)

Add explicit instruction listing playbook names as disjoint from skill names to reduce misclassification frequency.

---

## Acceptance criteria

- [ ] V2Planner auto-corrects misclassified playbook-as-skill during validation
- [ ] Warning logged when auto-correction occurs
- [ ] `ag run -y "Wetterbericht Düsseldorf"` succeeds when LLM returns research_v0 as skill type
- [ ] New test: misclassified playbook name in skill step gets corrected
- [ ] New test: misclassified skill name in playbook step gets corrected
- [ ] `pytest -W error` passes
- [ ] `ruff check src tests` passes

---

## Status log
- 2026-03-22 — Opened by Kai (reproduced with run `25495bba-224e-4c56-9371-eca8ffe546ce`)
