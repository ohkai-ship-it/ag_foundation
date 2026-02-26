"""OpenAI provider implementation.

This is the only real LLM provider in Sprint 02.
Implements chat completion using the OpenAI API.

Implementation: AF-0017
"""

from __future__ import annotations

import os
from typing import Any

from ag.providers.base import (
    ChatMessage,
    ChatResponse,
    ProviderConfig,
    ProviderError,
)
from ag.providers.registry import register_provider

# Environment variable for API key
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"

# Try to import OpenAI SDK at module level for mockability
# If not installed, we'll raise ProviderError when trying to use it
_openai_sdk_available = False
_OpenAI: Any = None

try:
    from openai import OpenAI as _OpenAI

    _openai_sdk_available = True
except ImportError:
    pass


def _get_openai_class() -> Any:
    """Get the OpenAI client class, raising ProviderError if not installed."""
    if not _openai_sdk_available:
        raise ProviderError(
            message="OpenAI SDK not installed. Run: pip install openai",
            provider="openai",
            error_type="dependency_error",
            details={"missing_package": "openai"},
        )
    return _OpenAI


@register_provider("openai")
class OpenAIProvider:
    """OpenAI API provider for chat completions.

    Authentication:
    - API key from config.api_key (highest priority)
    - OPENAI_API_KEY environment variable (recommended)

    This is the only real LLM provider in Sprint 02.
    """

    def __init__(self, config: ProviderConfig) -> None:
        self._config = config
        self._api_key = config.api_key or os.environ.get(OPENAI_API_KEY_ENV)
        self._client: Any = None  # Lazy initialization

    @property
    def name(self) -> str:
        return "openai"

    @property
    def is_stub(self) -> bool:
        return False

    def _get_client(self) -> Any:
        """Get or create the OpenAI client (lazy initialization)."""
        if self._client is not None:
            return self._client

        if not self._api_key:
            raise ProviderError(
                message=(
                    f"OpenAI API key not found. "
                    f"Set {OPENAI_API_KEY_ENV} environment variable or provide api_key in config."
                ),
                provider="openai",
                error_type="auth_error",
                details={"env_var": OPENAI_API_KEY_ENV},
            )

        OpenAI = _get_openai_class()
        self._client = OpenAI(
            api_key=self._api_key,
            base_url=self._config.base_url,
            timeout=float(self._config.timeout),
            max_retries=self._config.max_retries,
        )
        return self._client

    def chat(
        self,
        messages: list[ChatMessage],
        model: str | None = None,
        **kwargs: Any,
    ) -> ChatResponse:
        """Send a chat completion request to OpenAI.

        Args:
            messages: Conversation messages
            model: Model override (uses config default if None)
            **kwargs: Additional OpenAI API parameters

        Returns:
            ChatResponse with completion result

        Raises:
            ProviderError: On API errors
        """
        client = self._get_client()
        model_name = model or self._config.model

        try:
            # Convert messages to OpenAI format
            openai_messages = [msg.to_dict() for msg in messages]

            response = client.chat.completions.create(
                model=model_name,
                messages=openai_messages,
                **kwargs,
            )

            # Extract response data
            choice = response.choices[0]
            usage = response.usage

            return ChatResponse(
                content=choice.message.content or "",
                model=response.model,
                provider="openai",
                tokens_used=usage.total_tokens if usage else None,
                finish_reason=choice.finish_reason,
                raw_response=None,  # Don't store raw response in trace
            )

        except Exception as e:
            # Map OpenAI errors to ProviderError
            error_type = "api_error"
            error_class = type(e).__name__

            if "AuthenticationError" in error_class:
                error_type = "auth_error"
            elif "RateLimitError" in error_class:
                error_type = "rate_limit"
            elif "Timeout" in error_class:
                error_type = "timeout"

            raise ProviderError(
                message=str(e),
                provider="openai",
                error_type=error_type,
                details={"model": model_name, "error_class": error_class},
            ) from e

    def validate_config(self) -> bool:
        """Validate OpenAI configuration.

        Returns:
            True if config is valid

        Raises:
            ProviderError: If config is invalid
        """
        if not self._api_key:
            raise ProviderError(
                message=f"OpenAI API key not configured. Set {OPENAI_API_KEY_ENV}.",
                provider="openai",
                error_type="config_error",
            )
        return True
