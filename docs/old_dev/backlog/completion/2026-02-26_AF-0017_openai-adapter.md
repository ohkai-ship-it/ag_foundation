# Completion Note — AF-0017 — OpenAI API integration (provider adapter)
# Version number: v0.1

> Strict template. Fill every section. If something is not applicable, write **N/A** (do not delete sections).

## 1) Metadata
- **Backlog item (primary):** AF-0017
- **PR:** N/A (direct commit)
- **Author:** Jacob
- **Date:** 2026-02-26
- **Branch:** feat/openai-adapter
- **Risk level:** P0
- **Runtime mode used for verification:** manual (dev/test-only) + mocked LLM

## 2) Goal and acceptance criteria
### Goal (from backlog item)
Implement an OpenAI provider adapter behind a provider interface, with config/env var wiring and trace-safe recording so LLM mode runs end-to-end without leaking secrets.

### Acceptance criteria (from backlog item)
- [x] Provider abstraction supports a basic 'chat completion' call used by Executor in LLM mode.
- [x] OpenAI adapter reads API key from env/config (no secrets committed; missing key yields clear error).
- [x] RunTrace records provider name/model and timing; does NOT persist raw API key or sensitive headers.
- [x] Unit tests mock the OpenAI client and validate request/response mapping + error mapping.
- [x] Integration test (optional/marked) can run locally with real key.
- [x] Documentation updated: how to configure OpenAI for local dev.

## 3) What changed (file-level)
- `src/ag/providers/openai.py` — New file: OpenAIProvider class with `chat()`, `validate_config()`, `_get_openai_class()` for mockability
- `tests/test_providers.py` — Added mocked OpenAI tests (part of 34 provider tests)
- `pyproject.toml` — Added `openai` to optional dependencies, added `integration` pytest marker
- `docs/dev/prompts/continuation_prompt_sprint03_opus.md` — Added OpenAI setup instructions

## 4) Architecture alignment (mandatory)
- **Layering:** Provider adapter layer; no core runtime changes
- **Interfaces touched:** LLMProvider Protocol (implemented by OpenAIProvider)
- **Backward compatibility:** Yes, additive change only

## 5) Truthful UX check (mandatory)
- **User-visible labels affected:** Provider name in trace
- **Trace fields backing them:** `provider`, `model` fields in step metadata
- **Proof:** Mocked tests verify response includes model name; no API key in trace

## 6) Tests executed (mandatory)
- Command: `pytest tests/test_providers.py -v -k openai`
  - Result: PASS (mocked tests)
- Command: `pytest tests/test_providers.py -v -m integration` (requires OPENAI_API_KEY)
  - Result: SKIP (1 deselected without key)
- Command: `pytest tests/ -v`
  - Result: PASS (173 passed, 1 deselected)

## 7) Run evidence (mandatory for behavior changes)
- **RunTrace ID(s):** Generated via mocked tests
- **How to reproduce the run:**
  - Mocked: `pytest tests/test_providers.py::test_openai_chat_success -v`
  - Real: `$env:OPENAI_API_KEY = "sk-..."; pytest tests/test_providers.py -m integration -v`
- **Expected trace outcomes:**
  - Response contains `content`, `model`, `usage` fields
  - No API key in response or trace

## 8) Artifacts (if applicable)
**N/A**

## 9) Risks, tradeoffs, and follow-ups
- **Risks introduced:** Network dependency for integration tests
- **Tradeoffs made:** Integration test marked and skipped by default to avoid CI flakiness
- **Follow-up backlog items or bugs to create:** Consider adding retry logic for transient API errors

## 10) Reviewer checklist (copy/paste)
- [x] I can map PR → AF item and see acceptance criteria satisfied
- [x] I can verify truthful labels from RunTrace
- [x] I can reproduce a run (or it's docs-only)
- [x] Tests were run and results are documented
- [x] Any contract changes are documented in cornerstone docs
