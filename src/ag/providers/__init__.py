"""LLM providers package.

Exposes provider interface, registry, and implementations.
"""

from ag.providers.base import (
    ChatMessage,
    ChatResponse,
    LLMProvider,
    MessageRole,
    ProviderConfig,
    ProviderError,
    ProviderNotImplementedError,
)

# Import implementations to register them
from ag.providers.openai import OpenAIProvider
from ag.providers.registry import (
    PROVIDER_REGISTRY,
    get_provider,
    is_provider_registered,
    list_providers,
    register_provider,
)
from ag.providers.stubs import (
    AnthropicStubProvider,
    LocalStubProvider,
)

__all__ = [
    # Base types
    "LLMProvider",
    "ProviderConfig",
    "ProviderError",
    "ProviderNotImplementedError",
    "ChatMessage",
    "ChatResponse",
    "MessageRole",
    # Registry
    "get_provider",
    "register_provider",
    "list_providers",
    "is_provider_registered",
    "PROVIDER_REGISTRY",
    # Implementations
    "OpenAIProvider",
    "AnthropicStubProvider",
    "LocalStubProvider",
]
