"""Stub providers for future implementation + FakeLLMProvider for tests (AF-0125).

Sprint 02 Policy:
- OpenAI is the only real provider in this sprint
- These stubs fail fast with structured error
- The error is recorded in the RunTrace for observability
- This prevents accidental scope creep while keeping the architecture future-ready

AF-0125: FakeLLMProvider — deterministic zero-latency LLM stub for the test suite.
"""

from __future__ import annotations

import json
from typing import Any

from ag.providers.base import (
    ChatMessage,
    ChatResponse,
    MessageRole,
    ProviderConfig,
    ProviderNotImplementedError,
)
from ag.providers.registry import register_provider

# ---------------------------------------------------------------------------
# AF-0125: Deterministic test provider
# ---------------------------------------------------------------------------


class FakeLLMProvider:
    """Zero-latency deterministic LLM stub for tests (AF-0125).

    Returns hard-coded, structurally-valid JSON for each pipeline call type.
    Call type is detected by keyword in the system prompt:
    - "feasibility" → MOSTLY_FEASIBLE assessment (V3Planner phase 1)
    - default       → minimal valid plan (V3Planner phase 2 / V2Planner / V1Planner)
    """

    model = "fake-model"

    @property
    def name(self) -> str:
        return "fake"

    @property
    def is_stub(self) -> bool:
        return True

    def chat(
        self,
        messages: list[ChatMessage] | list[dict[str, str]],
        model: str | None = None,
        **kwargs: Any,
    ) -> ChatResponse:
        system = ""
        for m in messages:
            if isinstance(m, ChatMessage):
                if m.role == MessageRole.SYSTEM:
                    system = m.content
                    break
            elif isinstance(m, dict) and m.get("role") == "system":
                system = m.get("content", "")
                break

        if "feasibility" in system.lower():
            content = self._feasibility_response()
        elif "quality evaluator" in system.lower():
            content = self._semantic_response()
        elif "fix the json" in system.lower():
            content = self._repair_response()
        else:
            content = self._plan_response()

        return ChatResponse(
            content=content,
            model=self.model,
            provider="fake",
            tokens_used=10,
            input_tokens=5,
            output_tokens=5,
        )

    @staticmethod
    def _feasibility_response() -> str:
        return json.dumps(
            {
                "level": "mostly_feasible",
                "score": 0.8,
                "reason": "Task can be handled with available skills.",
                "capability_gaps": [],
                "recommendations": [],
            }
        )

    @staticmethod
    def _plan_response() -> str:
        return json.dumps(
            {
                "steps": [
                    {
                        "type": "skill",
                        "skill": "zero_skill",
                        "params": {},
                        "rationale": "deterministic test step",
                    }
                ],
                "estimated_tokens": 100,
                "confidence": 0.9,
                "warnings": [],
            }
        )

    @staticmethod
    def _semantic_response() -> str:
        """Deterministic semantic verification response (AF-0126)."""
        return json.dumps(
            [
                {
                    "step_number": 0,
                    "relevance_score": 0.9,
                    "relevance_reason": "Output addresses the task",
                    "completeness_score": 0.85,
                    "completeness_missing": [],
                    "consistency_score": 0.95,
                    "consistency_issues": [],
                }
            ]
        )

    @staticmethod
    def _repair_response() -> str:
        """Deterministic repair response — returns minimal valid output (AF-0126)."""
        return json.dumps(
            {
                "success": True,
                "summary": "repaired output",
            }
        )


@register_provider("anthropic")
class AnthropicStubProvider:
    """Stub provider for Anthropic/Claude API.

    NOT IMPLEMENTED in Sprint 02.
    Fails fast with structured error that is recorded in the trace.
    """

    def __init__(self, config: ProviderConfig) -> None:
        self._config = config

    @property
    def name(self) -> str:
        return "anthropic"

    @property
    def is_stub(self) -> bool:
        return True

    def chat(
        self,
        messages: list[ChatMessage],
        model: str | None = None,
        **kwargs: Any,
    ) -> ChatResponse:
        """Stub: raises ProviderNotImplementedError.

        The error is structured and will be recorded in the RunTrace.
        """
        raise ProviderNotImplementedError(
            provider="anthropic",
            message=(
                "Anthropic/Claude provider is not implemented in Sprint 02. "
                "Use provider='openai' or set AG_LLM_PROVIDER=openai."
            ),
        )

    def validate_config(self) -> bool:
        """Stub validation always fails with structured error."""
        raise ProviderNotImplementedError(
            provider="anthropic",
            message="Anthropic provider is a stub in Sprint 02.",
        )


@register_provider("local")
class LocalStubProvider:
    """Stub provider for local LLM inference.

    NOT IMPLEMENTED in Sprint 02.
    Fails fast with structured error that is recorded in the trace.
    """

    def __init__(self, config: ProviderConfig) -> None:
        self._config = config

    @property
    def name(self) -> str:
        return "local"

    @property
    def is_stub(self) -> bool:
        return True

    def chat(
        self,
        messages: list[ChatMessage],
        model: str | None = None,
        **kwargs: Any,
    ) -> ChatResponse:
        """Stub: raises ProviderNotImplementedError.

        The error is structured and will be recorded in the RunTrace.
        """
        raise ProviderNotImplementedError(
            provider="local",
            message=(
                "Local LLM provider is not implemented in Sprint 02. "
                "Use provider='openai' or set AG_LLM_PROVIDER=openai."
            ),
        )

    def validate_config(self) -> bool:
        """Stub validation always fails with structured error."""
        raise ProviderNotImplementedError(
            provider="local",
            message="Local provider is a stub in Sprint 02.",
        )
