# BUG-0022 — V3Planner CLI test flakiness
# Version number: v0.1
# Created: 2026-03-22
# Status: FIXED
# Severity: P2
# Area: Testing / CI

---

## Summary

After AF-0121 replaced V2Planner with V3Planner in the CLI inline-plan flow, some integration tests in `test_cli.py` that invoke real OpenAI provider calls became intermittently flaky. V3Planner makes 2 LLM calls (feasibility assessment + plan generation) vs V2Planner's 1, increasing exposure to LLM non-determinism. Tests pass individually but intermittently fail in full suite runs.

---

## Reproduction

```bash
pytest tests/test_cli.py -x -q
```

Intermittent — different tests fail on different runs. Common failures:
- `test_bootstrap_creates_default_when_no_workspaces`
- `test_inline_plan_abort_stops_execution`

Re-running the specific failing test individually usually passes.

---

## Root cause (suspected)

V3Planner's feasibility call sends a structured JSON prompt to the LLM. For vague prompts like "Test" (used in several CLI tests), the LLM may:
1. Return NOT_FEASIBLE, causing PlannerError (V3 rejects the task)
2. Return malformed JSON that the feasibility parser rejects (fallback to MOSTLY_FEASIBLE works, but adds variance)

The additional LLM call doubles the non-deterministic surface area.

---

## Mitigation options

1. Improve V3Planner fallback robustness (broader parse tolerance)
2. Mock the provider in affected CLI integration tests
3. Accept as inherent to real-LLM integration tests (document tolerance)

---

## Evidence

- Sprint 15 branch `feat/sprint15-llm-intelligence-layer`
- Observed during AF-0121 implementation (V3Planner)
- Tests pass 80-90% of the time; failure patterns are non-deterministic
