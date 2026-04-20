# BACKLOG ITEM — AF0066 — e2e_integration_test
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

> **File naming (required):** `AF####_<Status>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0066
- **Type:** Testing
- **Status:** DONE
- **Priority:** P1
- **Area:** Testing/Integration
- **Owner:** Kai
- **Target sprint:** Sprint07 (after AF0065)
- **Depends on:** AF0065 (first skill set), AF0058 (workspace restructure)

---

## Problem
We have unit tests but no end-to-end integration test that validates the full flow:

```
skill execution → verifier validation → trace recording → artifact storage
```

Without this, we cannot be confident that:
1. Skills produce valid outputs
2. The verifier accepts those outputs
3. Traces are recorded correctly
4. Artifacts land in the right place

---

## Goal
Create an E2E integration test that exercises the complete pipeline:

1. **Skill → Verifier** — Skill output passes schema verification
2. **Verifier → Trace** — Verified run creates proper RunTrace
3. **Trace → Artifact** — Artifacts are stored in `runs/<id>/artifacts/`
4. **Full round-trip** — `ag run` → `ag runs show` → `ag artifacts list`

**Test design: Generic and configurable**
- Tests should be parametrizable for any skill/playbook combination
- Not hardcoded to `summarize_v0` — can validate any registered skill
- Fixture-based: `@pytest.fixture` provides workspace, skill name, expected outputs

Two test modes:
- **CI mode:** Mock provider (deterministic, fast, runs in GitHub Actions)
- **Dev mode:** Real provider (optional, manual, validates actual LLM integration)

---

## Non-goals
- Performance benchmarking
- Load testing
- Multi-run stress tests
- Provider comparison tests

---

## Acceptance criteria (Definition of Done)
- [x] E2E test file: `tests/test_e2e_integration.py`
- [x] Test covers: skill → verifier → trace → artifact flow
- [x] CI mode: Uses mock provider, runs in pytest
- [x] Dev mode: Uses real provider, skipped by default (`@pytest.mark.manual`)
- [x] Validates workspace structure per AF0058 (`inputs/`, `runs/<id>/`)
- [x] Validates artifact storage in `runs/<id>/artifacts/`
- [x] Validates RunTrace contains expected evidence
- [x] Test is deterministic (no flaky failures)
- [x] `ruff check src tests` passes
- [x] `pytest -W error` passes (excluding manual tests)
- [x] Coverage threshold maintained

---

## Test structure (conceptual)

```python
# tests/test_e2e_integration.py

class TestE2EIntegration:
    """End-to-end integration tests for the full pipeline."""
    
    def test_skill_to_artifact_flow_mock(self, tmp_workspace):
        """CI mode: Full flow with mock provider."""
        # 1. Create workspace with inputs
        # 2. Run skill via ag run (mock provider)
        # 3. Verify skill output passes verifier
        # 4. Verify trace is recorded
        # 5. Verify artifacts in runs/<id>/artifacts/
        
    @pytest.mark.manual
    def test_skill_to_artifact_flow_real(self, tmp_workspace):
        """Dev mode: Full flow with real OpenAI provider."""
        # Same as above, but with real LLM calls
        # Requires OPENAI_API_KEY
```

### Mock provider strategy
```python
class MockProvider(BaseProvider):
    """Deterministic mock for CI testing."""
    
    def complete(self, prompt: str) -> str:
        # Return canned response based on prompt hash or pattern matching
        return self._canned_responses.get(hash(prompt), "Mock response")
```

---

## Implementation notes

### Files to create/modify

| File | Changes |
|------|---------|
| `tests/test_e2e_integration.py` | New E2E test file |
| `src/ag/providers/stubs.py` | Enhance mock provider if needed |
| `tests/conftest.py` | Add `tmp_workspace` fixture with inputs/ |

### Test isolation
- Each test creates fresh temp workspace
- No shared state between tests
- Mock provider is stateless

---

## Risks

| Risk | Mitigation |
|------|------------|
| AF0065 skills not ready | This AF depends on AF0065 completion |
| Mock provider too simplistic | Design mock to be extensible |
| Flaky tests | Ensure deterministic mock responses |

---

## Related
- AF0065 (First skill set) — **prerequisite**
- AF0058 (Workspace folder restructure) — **prerequisite**
- AF0046 (Test isolation framework) — complementary

---

## Documentation impact
- Add testing guide section on E2E tests
- Document mock provider usage

---

# Completion section (fill when done)

Pending completion.

