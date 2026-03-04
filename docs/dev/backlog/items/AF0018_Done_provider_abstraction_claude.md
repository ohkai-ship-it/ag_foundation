# AF0018 — Provider abstraction + Claude/local stubs (future-ready, no real calls yet)
# Version number: v0.2

## Metadata
- **ID:** AF-0018
- **Type:** Foundation
- **Status:** Done
- **Priority:** P1
- **Area:** Providers
- **Owner:** Jacob
- **Completed in:** Sprint 02
- **Completion date:** 2026-02-26

## Problem
We want OpenAI first, but must keep the system pluggable. Without a clean provider interface and config shape, adding Anthropic (Claude) and local models later will cause refactors.

## Goal
Define a provider interface + registry and add non-functional stubs for Anthropic and local models, including config schema, so future providers can be added without touching runtime/CLI contracts.

## Non-goals
- Implementing real Claude/local calls in this sprint.
- Provider selection UX beyond config field.

## Acceptance criteria (Definition of Done)
- [x] A `LLMProvider` Protocol (or ABC) exists with a minimal method used by Executor (chat completion).
- [x] Provider registry supports selecting provider by name (`openai`, `anthropic`, `local`).
- [x] Config schema includes provider selection + per-provider options (model, base_url, timeout).
- [x] Anthropic and local providers return 'Not implemented' with structured error and are trace-recorded if invoked.
- [x] Unit tests cover provider selection and stub behavior.

## Implementation notes
- Keep interface minimal; don't bake in tool calling yet.
- Use a factory like `get_provider(config)`.
- Stubs should fail fast with clear message and non-zero status but still produce a RunTrace.

## Risks
Low: mostly scaffolding. Risk is over-design; mitigate by keeping the interface small.

## PR plan
1. PR (chore/provider-abstraction): Add provider interface + registry + config schema + anthropic/local stubs + tests.

---
# Completion section (fill when done)

**Completion date:** 2026-02-26  
**Author:** Jacob

**Summary:**
Defined provider interface + registry and added non-functional stubs for Anthropic and local models. Future providers can be added without touching runtime/CLI contracts.

**What Changed:**
- `src/ag/providers/__init__.py` — Package exports
- `src/ag/providers/base.py` — LLMProvider Protocol, ProviderConfig, ChatMessage, ChatResponse, ProviderError
- `src/ag/providers/registry.py` — PROVIDER_REGISTRY, get_provider(), register_provider(), list_providers()
- `src/ag/providers/stubs.py` — AnthropicStubProvider, LocalStubProvider (fail fast with structured error)
- `tests/test_providers.py` — 34 tests for provider module

**Architecture Alignment:**
- New provider layer between core runtime and external LLM APIs
- LLMProvider Protocol defines minimal interface
- Additive change only

**Stub Behavior:**
- `AnthropicStubProvider().chat([])` raises ProviderError: "Provider 'anthropic' is not implemented in this sprint"

**Tests Executed:**
- pytest tests/test_providers.py: PASS (34 tests)
- pytest tests/: PASS (173 passed)
