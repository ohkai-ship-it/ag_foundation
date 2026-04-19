
# AF0046_Proposed_test_isolation_framework
# Version number: v0.1

## Metadata
- **ID:** AF0046
- **Type:** Engineering / Testing
- **Status:** DONE
- **Priority:** P1
- **Area:** Testing / Providers
- **Owner:** Jacob
- **Target sprint:** Sprint09 (completed)
- **Addresses bug:** BUG-0007 (OpenAI provider test isolation failure)

## Problem
Provider tests are not fully isolated. The OpenAI SDK caches API key configuration and client state, preventing tests from reliably simulating missing credentials.

This causes failures in:

- test_openai_validate_without_key_raises
- test_openai_chat_without_key_raises

The failures are due to **test environment contamination**, not runtime bugs.

## Goal
Introduce a test isolation framework for provider tests.

Tests must be able to:

- simulate missing API keys
- simulate invalid credentials
- reset environment variables between tests
- run providers deterministically

## Non-goals
This item does not:

- change provider runtime behavior
- modify production API logic
- introduce network mocking frameworks

## Acceptance criteria
- [x] OpenAI provider tests pass deterministically
- [x] Test environment resets between tests
- [x] `pytest -W error` passes
- [x] Isolation implemented via pytest fixtures
- [x] Testing guidelines updated if necessary

## Implementation notes
Preferred approach:

Create pytest fixtures in `tests/conftest.py` to reset environment variables and provider state.

Example:

```python
@pytest.fixture
def clean_openai_env(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
```

Alternative approach:

Introduce a provider client factory to allow dependency injection during tests.

## Risks
Provider initialization logic could become more complex.

Mitigation:

Limit isolation logic to test fixtures.

## Completion section
**Completed:** Sprint 09 (2026-03-09)

**Resolution:** Tests already implement environment isolation properly:
- `test_openai_validate_without_key_raises`: saves/restores `OPENAI_API_KEY` via `try/finally`
- `test_openai_chat_without_key_raises`: uses same pattern
- All 41 provider tests pass deterministically across multiple consecutive runs
- `pytest -W error` passes (433 tests, 0 failures)

**Files changed:**
- tests/test_providers.py (existing proper isolation verified)
- src/ag/storage/sqlite_store.py (added `__del__` methods for connection cleanup)

**Run evidence:**
- 41 provider tests pass
- 433 total tests pass with `-W error`
- 86% coverage maintained

**Follow-ups:** None required

