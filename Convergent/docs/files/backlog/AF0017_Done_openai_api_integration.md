# AF0017 — OpenAI API integration (provider adapter) + config wiring (LLM mode)
# Version number: v0.2

## Metadata
- **ID:** AF-0017
- **Type:** Feature
- **Status:** DONE
- **Priority:** P0
- **Area:** Providers
- **Owner:** Jacob
- **Completed in:** Sprint 02
- **Completion date:** 2026-02-26

## Problem
Sprint 01 proved the runtime and truthful UX in manual mode, but end-user behavior is LLM-first. We need the first real LLM provider integration so LLM mode is executable and traceable.

## Goal
Implement an OpenAI provider adapter behind a provider interface, with config/env var wiring and trace-safe recording so LLM mode runs end-to-end without leaking secrets.

## Non-goals
- Adding multi-provider routing logic (covered by AF-0018).
- Adding tool calling beyond plain chat completions (defer).
- Making network calls mandatory in CI (must be mockable).

## Acceptance criteria (Definition of Done)
- [x] Provider abstraction supports a basic 'chat completion' call used by Executor in LLM mode.
- [x] OpenAI adapter reads API key from env/config (no secrets committed; missing key yields clear error).
- [x] RunTrace records provider name/model and timing; does NOT persist raw API key or sensitive headers.
- [x] Unit tests mock the OpenAI client and validate request/response mapping + error mapping.
- [x] Integration test (optional/marked) can run locally with real key and produces a persisted RunTrace with `mode=autonomous` (or `supervised` as implemented).
- [x] Documentation updated: how to configure OpenAI for local dev (env vars or config).

## Implementation notes
- Prefer official OpenAI Python SDK.
- Add config fields: provider='openai', model, timeout; key via `OPENAI_API_KEY`.
- Add `ProviderError` mapping (auth/timeout/rate-limit) into RunTrace step error.
- Ensure JSON output stays truthful: labels derived from trace fields.

## Risks
Medium: network flakiness and API changes. Mitigate with mocks + optional integration test marked/skipped in CI.

## PR plan
1. PR (feat/openai-provider): Add provider interface, OpenAI adapter, config wiring, unit tests, optional integration test.

---
# Completion section (fill when done)

**Completion date:** 2026-02-26  
**Author:** Jacob

**Summary:**
Implemented OpenAI provider adapter behind provider interface with config/env wiring. Traces record provider metadata without leaking secrets.

**What Changed:**
- `src/ag/providers/openai.py` — New: OpenAIProvider class with chat(), validate_config(), _get_openai_class()
- `tests/test_providers.py` — Added mocked OpenAI tests
- `pyproject.toml` — Added openai to optional dependencies, added integration marker

**Architecture Alignment:**
- Provider adapter layer; no core runtime changes
- LLMProvider Protocol implemented by OpenAIProvider
- Additive change only

**Truthful UX:**
- Provider name and model in trace (not API key)
- Mocked tests verify no secrets in response

**Tests Executed:**
- pytest tests/test_providers.py -k openai: PASS (mocked)
- pytest tests/: PASS (173 passed, 1 deselected)

**Run Evidence:**
- Mocked: pytest tests/test_providers.py::test_openai_chat_success
- Real: Requires OPENAI_API_KEY env var

