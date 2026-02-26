"""Stub providers for future implementation.

Sprint 02 Policy:
- OpenAI is the only real provider in this sprint
- These stubs fail fast with structured error
- The error is recorded in the RunTrace for observability
- This prevents accidental scope creep while keeping the architecture future-ready
"""

from __future__ import annotations

from typing import Any

from ag.providers.base import (
    ChatMessage,
    ChatResponse,
    ProviderConfig,
    ProviderNotImplementedError,
)
from ag.providers.registry import register_provider


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
