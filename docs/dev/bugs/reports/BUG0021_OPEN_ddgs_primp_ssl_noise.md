# BUG-0021 — ddgs primp SSL socket noise
# Version number: v0.1
# Created: 2026-03-22
# Status: OPEN
# Severity: P2
# Area: Testing / CI

---

## Summary

`pytest -W error` intermittently fails due to `ResourceWarning` / `PytestUnraisableExceptionWarning` from the `duckduckgo_search` (`ddgs`) and `primp` libraries. The `primp` HTTP client opens SSL sockets on import; when Python's GC finalizes them, pytest's warnings-as-errors mode catches the noise and fails the test run.

---

## Reproduction

```bash
pytest -W error
```

Intermittent failure — depends on GC timing. More likely on CI or under memory pressure.

Warning chain:
1. `primp` (HTTP client used by `ddgs`) opens SSL socket during import or mock setup
2. Socket is not explicitly closed
3. Python GC finalizes the socket → `ResourceWarning: unclosed <ssl.SSLSocket>`
4. `pytest -W error` converts this to `PytestUnraisableExceptionWarning` → test failure

---

## Current workaround

Two suppressions in place:
- `pyproject.toml` `[tool.pytest.ini_options]`: `filterwarnings = ["ignore::ResourceWarning"]`
- `tests/conftest.py`: `warnings.filterwarnings("ignore", category=pytest.PytestUnraisableExceptionWarning)`

These suppress the noise but weaken the warnings-as-errors gate for legitimate `ResourceWarning` issues.

---

## Root cause

The `ddgs` library uses `primp` as its HTTP transport. `primp` may open connections during module import or when `DDGS()` is instantiated, even if the actual search call is mocked. The SSL sockets are not explicitly closed, relying on GC finalization.

---

## Proposed fix

**Option A (preferred):** Mock at transport layer — patch `primp` or the socket before `ddgs` import in test setup. Prevents real connections from being opened.

**Option B:** Explicit teardown fixture — after each test using `ddgs`, force-close any lingering SSL sockets via `gc.collect()` + socket cleanup.

**Option C:** Replace `ddgs` with a custom DuckDuckGo wrapper that uses a managed HTTP client (e.g., `httpx` with explicit lifecycle).

After fix: remove both `filterwarnings` suppressions and confirm `pytest -W error` passes cleanly.

---

## Affected files

- `tests/conftest.py` — warning suppression
- `pyproject.toml` — filterwarnings config
- `tests/test_web_search.py` — ddgs mock tests
- `tests/test_research_skills.py` — ddgs mock tests
- `src/ag/skills/web_search.py` — `from ddgs import DDGS`

---

## Impact

- **Runtime:** None — this is test infrastructure only
- **CI:** `pytest -W error` is unreliable, weakening the warnings gate
- **Developer experience:** Intermittent failures cause confusion during review

---

## Discovery

Found during Sprint 14 review (S14_REVIEW_01, Pass 2). Documented in `artifacts/review_S14_01/bug_triage.md`.
