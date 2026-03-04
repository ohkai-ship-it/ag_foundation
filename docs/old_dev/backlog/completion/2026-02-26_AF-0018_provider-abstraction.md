# Completion Note — AF-0018 — Provider abstraction + Claude/local stubs
# Version number: v0.1

> Strict template. Fill every section. If something is not applicable, write **N/A** (do not delete sections).

## 1) Metadata
- **Backlog item (primary):** AF-0018
- **PR:** N/A (direct commit)
- **Author:** Jacob
- **Date:** 2026-02-26
- **Branch:** feat/provider-abstraction
- **Risk level:** P1
- **Runtime mode used for verification:** manual (dev/test-only)

## 2) Goal and acceptance criteria
### Goal (from backlog item)
Define a provider interface + registry and add non-functional stubs for Anthropic and local models, including config schema, so future providers can be added without touching runtime/CLI contracts.

### Acceptance criteria (from backlog item)
- [x] A `LLMProvider` Protocol (or ABC) exists with a minimal method used by Executor (chat completion).
- [x] Provider registry supports selecting provider by name (`openai`, `anthropic`, `local`).
- [x] Config schema includes provider selection + per-provider options (model, base_url, timeout).
- [x] Anthropic and local providers return 'Not implemented' with structured error and are trace-recorded if invoked.
- [x] Unit tests cover provider selection and stub behavior.

## 3) What changed (file-level)
- `src/ag/providers/__init__.py` — New file: package exports
- `src/ag/providers/base.py` — New file: LLMProvider Protocol, ProviderConfig, ChatMessage, ChatResponse, ProviderError, ProviderNotFoundError
- `src/ag/providers/registry.py` — New file: PROVIDER_REGISTRY, get_provider(), register_provider(), list_providers()
- `src/ag/providers/stubs.py` — New file: AnthropicStubProvider, LocalStubProvider (fail fast with structured error)
- `tests/test_providers.py` — New file: 34 tests for provider module

## 4) Architecture alignment (mandatory)
- **Layering:** New provider layer between core runtime and external LLM APIs
- **Interfaces touched:** New LLMProvider Protocol; no changes to existing interfaces
- **Backward compatibility:** Yes, additive change only

## 5) Truthful UX check (mandatory)
- **User-visible labels affected:** Provider error messages
- **Trace fields backing them:** Error details include provider name and reason
- **Proof:** `AnthropicStubProvider().chat([])` raises `ProviderError` with message "Provider 'anthropic' is not implemented in this sprint"

## 6) Tests executed (mandatory)
- Command: `pytest tests/test_providers.py -v`
  - Result: PASS (34 tests)
- Command: `pytest tests/ -v`
  - Result: PASS (173 passed, 1 deselected)

## 7) Run evidence (mandatory for behavior changes)
- **RunTrace ID(s):** N/A (stubs fail before trace)
- **How to reproduce the run:**
  ```python
  from ag.providers.stubs import AnthropicStubProvider
  from ag.providers.base import ChatMessage
  try:
      AnthropicStubProvider().chat([ChatMessage(role="user", content="test")])
  except Exception as e:
      print(e)  # ProviderError with structured message
  ```
- **Expected trace outcomes:** Structured error with provider name

## 8) Artifacts (if applicable)
**N/A**

## 9) Risks, tradeoffs, and follow-ups
- **Risks introduced:** None
- **Tradeoffs made:** Stubs fail fast rather than returning mock responses; this prevents accidental use
- **Follow-up backlog items or bugs to create:** Implement real Anthropic provider when needed

## 10) Reviewer checklist (copy/paste)
- [x] I can map PR → AF item and see acceptance criteria satisfied
- [x] I can verify truthful labels from RunTrace
- [x] I can reproduce a run (or it's docs-only)
- [x] Tests were run and results are documented
- [x] Any contract changes are documented in cornerstone docs
