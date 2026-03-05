
# BUG0007_OpenAI_test_isolation
# Version number: v0.1

## Metadata
- **ID:** BUG0007
- **Status:** Open
- **Severity:** P1
- **Area:** Providers / Testing
- **Reported by:** Sprint04 Review
- **Date:** 2026-03-04
- **Related backlog item(s):** AF0046
- **Related PR(s):** N/A

## Summary
Two OpenAI provider tests fail due to test isolation issues. The OpenAI SDK caches the API key and client state, which prevents tests from reliably simulating a missing API key after a client has been initialized.

## Expected behavior
Provider tests should run deterministically and allow simulation of missing or invalid API keys.

## Actual behavior
The following tests fail intermittently:

- tests/test_providers.py::TestOpenAIProvider::test_openai_validate_without_key_raises
- tests/test_providers.py::TestOpenAIProvider::test_openai_chat_without_key_raises

Because the OpenAI client caches configuration, clearing the `OPENAI_API_KEY` environment variable during tests does not affect an already initialized client.

## Reproduction steps
1. Run the test suite:
   ```
   pytest -W error
   ```
2. Observe failures in OpenAI provider tests.

## Evidence
- **Tests failing:** 2
- **Passing tests:** 227
- **Logs:** see Sprint04 review artifact `ruff_pytest_output.txt`
- **Environment:** Python 3.14, OpenAI SDK 2.x

## Impact
Test suite is not fully deterministic. CI reports failures even though runtime functionality is correct.

## Suspected cause
OpenAI SDK caches API key/client configuration internally, preventing tests from resetting environment state.

## Proposed fix
Introduce a pytest fixture that resets provider environment and client state between tests.

Example approach:

```python
@pytest.fixture
def clean_openai_env(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
```

## Acceptance criteria
- [ ] Provider tests pass deterministically
- [ ] API key simulation works in tests
- [ ] `pytest -W error` passes
- [ ] Isolation implemented via pytest fixtures

## Notes
This is a **test isolation issue**, not a production runtime bug.
