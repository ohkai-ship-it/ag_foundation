"""LLM Provider protocol and base types.

Design Decision: We use typing.Protocol for structural subtyping (duck typing)
to allow flexibility in provider implementations while maintaining type safety.

Sprint 02 Policy: OpenAI is the only real provider. Claude and local are stubs
that fail fast with structured error (and still produce a RunTrace for observability).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Protocol, runtime_checkable


class ProviderError(Exception):
    """Base exception for provider errors.

    Raised when a provider encounters an error during operation.
    These errors are recorded in the RunTrace for observability.
    """

    def __init__(
        self,
        message: str,
        provider: str,
        error_type: str = "provider_error",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.provider = provider
        self.error_type = error_type
        self.details = details or {}

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict for RunTrace recording."""
        return {
            "error_type": self.error_type,
            "provider": self.provider,
            "message": self.message,
            "details": self.details,
        }


class ProviderNotImplementedError(ProviderError):
    """Raised when a provider stub is invoked.

    Sprint 02 policy: Claude and local providers are stubs that fail fast.
    This error is structured and recorded in the trace for observability.
    """

    def __init__(self, provider: str, message: str | None = None) -> None:
        msg = message or f"Provider '{provider}' is not implemented in v0"
        super().__init__(
            message=msg,
            provider=provider,
            error_type="not_implemented",
            details={"stub": True, "version": "v0"},
        )


class MessageRole(str, Enum):
    """Role of a message in a conversation."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class ChatMessage:
    """A single message in a chat conversation."""

    role: MessageRole
    content: str

    def to_dict(self) -> dict[str, str]:
        """Convert to provider-agnostic dict."""
        return {"role": self.role.value, "content": self.content}


@dataclass
class ChatResponse:
    """Response from a chat completion request."""

    content: str
    model: str
    provider: str
    tokens_used: int | None = None
    finish_reason: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    raw_response: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict for recording."""
        return {
            "content": self.content,
            "model": self.model,
            "provider": self.provider,
            "tokens_used": self.tokens_used,
            "finish_reason": self.finish_reason,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class ProviderConfig:
    """Configuration for an LLM provider.

    Resolution order (highest priority first):
    1. Explicit parameters passed to method calls
    2. Environment variables (e.g., OPENAI_API_KEY)
    3. Config file values
    4. Provider defaults
    """

    provider: str
    model: str
    api_key: str | None = None
    base_url: str | None = None
    timeout: int = 60
    max_retries: int = 2
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProviderConfig":
        """Create from configuration dict."""
        return cls(
            provider=data.get("provider", "openai"),
            model=data.get("model", "gpt-4"),
            api_key=data.get("api_key"),
            base_url=data.get("base_url"),
            timeout=data.get("timeout", 60),
            max_retries=data.get("max_retries", 2),
            extra=data.get("extra", {}),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict (excludes api_key for safety)."""
        return {
            "provider": self.provider,
            "model": self.model,
            "base_url": self.base_url,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            # Note: api_key intentionally excluded for trace safety
        }


@runtime_checkable
class LLMProvider(Protocol):
    """Protocol for LLM provider implementations.

    Responsibilities:
    - Send chat completion requests to the provider
    - Handle authentication (via config or env vars)
    - Map provider-specific responses to ChatResponse
    - Raise ProviderError on failures (recorded in trace)

    All providers must be trace-safe: no secrets in returned data.
    """

    @property
    def name(self) -> str:
        """Provider name (e.g., 'openai', 'anthropic', 'local')."""
        ...

    @property
    def is_stub(self) -> bool:
        """Whether this provider is a stub (fails fast with structured error)."""
        ...

    def chat(
        self,
        messages: list[ChatMessage],
        model: str | None = None,
        **kwargs: Any,
    ) -> ChatResponse:
        """Send a chat completion request.

        Args:
            messages: Conversation messages
            model: Model override (uses config default if None)
            **kwargs: Provider-specific options

        Returns:
            ChatResponse with completion result

        Raises:
            ProviderError: On provider errors (auth, timeout, rate limit, etc.)
            ProviderNotImplementedError: If provider is a stub
        """
        ...

    def validate_config(self) -> bool:
        """Validate provider configuration.

        Returns:
            True if config is valid and provider can be used

        Raises:
            ProviderError: If config is invalid with details
        """
        ...
