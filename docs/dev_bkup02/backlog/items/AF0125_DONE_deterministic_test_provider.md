# AF-0125 — Deterministic test provider
# Version number: v0.1
# Created: 2026-03-22
# Status: DONE
# Priority: P1
# Area: Testing / CI

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI workflow (two-phase — see below)
> - 1 PR = 1 sprint
> - INDEX update rule (status ↔ filename integrity)
>
> **CI workflow (CRITICAL):**
> - **During AF development:** run targeted tests only
>   `pytest tests/test_<relevant>.py -W error`
> - **Before commit (full gate):** run the complete CI gate
>   1. `ruff check src tests`
>   2. `ruff format --check src tests`
>   3. `pytest -W error`
>   4. `pytest --cov=src/ag --cov-report=term-missing`
>
> Do NOT run the full suite on every save. Targeted tests keep feedback fast.
> The full gate runs once, right before `git commit`.

> **File naming (required):** `AF####_<STATUS>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF-0125
- **Type:** Testing / CI
- **Status:** READY
- **Priority:** P1
- **Area:** Testing / CI
- **Owner:** Jacob
- **Target sprint:** Sprint 15 — llm_intelligence_layer

---

## Problem

The default `pytest` run is slow and intermittently flaky because some tests trigger
real OpenAI API calls:

1. **CLI inline plan flow** (`src/ag/cli/main.py`): when no `--mode manual`, `--playbook`,
   or `--skill` is given, the run command instantiates `V3Planner` with a real
   `OpenAIProvider`. V3Planner makes **two** LLM calls per invocation (feasibility
   assessment + plan generation), doubling the latency and non-determinism vs V2Planner.

2. **Runtime LLM-mode tests** (`tests/test_runtime.py`): a handful of tests use
   `mode="llm"` without mocking the provider, potentially reaching real OpenAI.

There is no global test-level provider mock — each test is responsible for its own
provider setup, and several tests omit this. The result:

- Full suite is slow (real HTTP round-trips, 2–5s per LLM call)
- Tests are intermittently flaky (BUG-0022): LLM non-determinism causes parse failures
  or `NOT_FEASIBLE` assessments for prompts like `"Test"` used in CLI tests
- Several tests are currently `@pytest.mark.skip` as a workaround (BUG-0022)

Related: BUG-0022 (V3Planner CLI test flakiness).

---

## Goal

- All tests in the default `pytest` run are deterministic and fast (no real API calls)
- `@pytest.mark.integration` and `@pytest.mark.manual` tests opt out and may still
  use real providers
- BUG-0022 skipped tests are unblocked and pass reliably
- No individual test file needs to be changed to add provider mocks

---

## Non-goals

- Changing the behavior of integration or manual tests
- Modifying production provider selection logic
- Adding any new CLI flags or runtime configuration
- Mocking providers in individual test files (autouse fixture handles it globally)

---

## Design

### 1. `FakeLLMProvider` — deterministic zero-latency stub

Add `FakeLLMProvider` to `src/ag/providers/stubs.py`. It implements the `LLMProvider`
protocol and returns hard-coded, structurally-valid JSON responses for each call type
that the pipeline parsers expect.

**Response multiplexing:** V3Planner calls `.chat()` twice per plan (feasibility then
plan generation). The fake provider detects the call type by checking for the keyword
`"feasibility"` in the system prompt:

```python
class FakeLLMProvider:
    """Zero-latency deterministic LLM stub for tests."""

    model = "fake-model"

    def chat(self, messages, model=None, **kwargs):
        system = next(
            (m.content for m in messages if m.role == MessageRole.SYSTEM), ""
        )
        if "feasibility" in system.lower():
            return self._feasibility_response()
        return self._plan_response()

    def _feasibility_response(self):
        # Returns MOSTLY_FEASIBLE so plan generation is never blocked
        return ChatResponse(content=json.dumps({
            "level": "MOSTLY_FEASIBLE",
            "score": 0.8,
            "reason": "Task can be handled with available skills.",
            "capability_gaps": [],
            "recommendations": []
        }))

    def _plan_response(self):
        # Returns a minimal valid plan with one echo_tool step
        return ChatResponse(content=json.dumps({
            "steps": [
                {"type": "skill", "skill": "echo_tool",
                 "params": {"message": "test"}, "rationale": "test step"}
            ],
            "confidence": 0.9,
            "estimated_tokens": 100,
            "warnings": []
        }))
```

The same provider covers V2Verifier semantic checks and V2Executor repair calls by
returning appropriate JSON for those prompt shapes (detected by checking for
`"semantic"` or `"repair"` keywords in the system prompt).

### 2. `autouse` fixture in `tests/conftest.py`

Patch `ag.providers.get_provider` globally for all non-integration, non-manual tests:

```python
import pytest
from unittest.mock import patch
from ag.providers.stubs import FakeLLMProvider

@pytest.fixture(autouse=True)
def _fake_llm_provider(request):
    """Patch get_provider globally so no test makes real LLM calls by default.

    Tests marked @pytest.mark.integration or @pytest.mark.manual opt out and
    receive the real provider selection logic.
    """
    markers = {m.name for m in request.node.iter_markers()}
    if "integration" in markers or "manual" in markers:
        yield  # real provider
        return

    with patch("ag.providers.get_provider", return_value=FakeLLMProvider()):
        yield
```

This is an `autouse` fixture so it applies to every test automatically. Opt-out
is via the existing `integration` and `manual` markers.

### 3. Unblock BUG-0022 skipped tests

Remove `@pytest.mark.skip(reason="Flaky in full suite — see BUG-0022")` from
the previously-skipped tests in `tests/test_cli.py`. With the fake provider,
these tests are now deterministic.

Update BUG-0022 status to FIXED.

### Files touched

| File | Change |
|------|--------|
| `src/ag/providers/stubs.py` | Add `FakeLLMProvider` class |
| `tests/conftest.py` | Add `_fake_llm_provider` autouse fixture |
| `tests/test_cli.py` | Remove `@pytest.mark.skip` from BUG-0022 tests (3 instances) |
| `docs/dev/bugs/reports/BUG0022_OPEN_v3planner_cli_test_flakiness.md` | Update status to FIXED |
| `docs/dev/bugs/INDEX_BUGS.md` | Move BUG-0022 from OPEN to FIXED |

---

## Acceptance criteria (Definition of Done)

- [ ] Deliverable exists in the correct folder
- [ ] Naming conventions applied (file name + internal Status match)
- [ ] INDEX file(s) updated
- [ ] CI/local checks pass (two-phase workflow):
  - **During development:** targeted tests run (`pytest tests/test_cli.py tests/test_runtime.py -W error`)
  - **Before commit (full gate):**
    - [ ] `ruff check src tests`
    - [ ] `ruff format --check src tests`
    - [ ] `pytest -W error`
    - [ ] coverage thresholds met (`pytest --cov=src/ag --cov-report=term-missing`)
- [ ] `pytest` (default, no markers) completes without real OpenAI API calls
- [ ] Previously-skipped BUG-0022 tests pass deterministically (run 5× to confirm)
- [ ] `pytest -m integration` still reaches real OpenAI (fixture excluded for that marker)
- [ ] `FakeLLMProvider` returns valid parseable JSON for all call shapes:
  - Feasibility response (V3Planner Phase 1)
  - Plan response (V3Planner/V2Planner Phase 2)
  - Semantic verification response (V2Verifier)
  - Repair response (V2Executor)
- [ ] BUG-0022 status updated to FIXED in report and INDEX

---

## Dependencies

- V3Planner (AF-0121) — must understand V3 two-phase prompt shapes to build correct fake responses
- V2Verifier (AF-0123) — fake must cover semantic check prompt shape
- V2Executor (AF-0124, DONE) — fake must cover repair prompt shape
- `src/ag/providers/base.py` — `LLMProvider` protocol, `ChatMessage`, `ChatResponse`

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Fake response doesn't parse correctly | Tests fail in new ways | Validate fake JSON against actual parser in unit test of `FakeLLMProvider` itself |
| autouse fixture accidentally covers integration tests | Real calls blocked | Check `request.node.iter_markers()` for integration/manual markers before patching |
| New test added that needs real provider without marker | Silent fake use | Document the contract; add note in conftest explaining opt-out mechanism |
| Call-type detection by keyword is fragile | Wrong fake response returned | Use a call counter as fallback; V3Planner always calls feasibility first |

---

# Completion section (fill when done)

## 1) Metadata
- **Backlog item (primary):** AF-0125
- **PR:** #
- **Author:**
- **Date:** YYYY-MM-DD
- **Branch:** feat/sprint15-llm-intelligence-layer
- **Risk level:** P1
- **Runtime mode used for verification:** N/A (test infrastructure only)

---

## 2) Acceptance criteria verification

- [ ] ...

---

## 3) What changed (file-level)

- ...

---

## 4) Architecture alignment (mandatory)
- **Layering:** Test infrastructure only — no production code changed
- **Interfaces touched:** `LLMProvider` protocol (implemented by `FakeLLMProvider`)
- **Backward compatibility:** No schema or contract changes

---

## 5) Truthful UX check (mandatory when user-visible)
- N/A — test infrastructure change only

---

## 6) Tests executed (mandatory unless docs-only)

- Command: `...`
  - Result:

---

## 7) Run evidence (mandatory for behavior changes)
- N/A — no runtime behavior changed; run evidence not applicable

---

## 8) Artifacts (if applicable)
- N/A

---

## 9) Risks, tradeoffs, follow-ups
- **Risks introduced:** See Risks table above
- **Tradeoffs made:** Fake responses are minimal (echo_tool plan); integration test coverage for real LLM parsing remains only in `@pytest.mark.integration` tests
- **Follow-up items:** BUG-0022 → FIXED after this AF is done

---

## 10) Reviewer checklist (copy/paste)
- [ ] I can map PR → AF item and see acceptance criteria satisfied
- [ ] I can verify truthful labels from RunTrace
- [ ] I can reproduce a run (or it's docs-only)
- [ ] Tests were run and results are documented
- [ ] Any contract changes are documented in cornerstone docs
