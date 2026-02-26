"""Provider registry for managing LLM provider implementations.

The registry allows selecting providers by name and supports dynamic registration.

Sprint 02 Policy:
- OpenAI is the only real provider (implemented in AF-0017)
- Anthropic and local are stubs that fail fast with structured error
"""

from __future__ import annotations

from typing import Callable, TypeVar

from ag.providers.base import LLMProvider, ProviderConfig, ProviderError

# Type for provider factory functions
ProviderFactory = Callable[[ProviderConfig], LLMProvider]

# Global provider registry
PROVIDER_REGISTRY: dict[str, ProviderFactory] = {}

T = TypeVar("T", bound=LLMProvider)


def register_provider(name: str) -> Callable[[type[T]], type[T]]:
    """Decorator to register a provider class.

    Usage:
        @register_provider("openai")
        class OpenAIProvider:
            def __init__(self, config: ProviderConfig):
                ...

    Args:
        name: Provider name (e.g., 'openai', 'anthropic', 'local')

    Returns:
        Decorator function
    """

    def decorator(cls: type[T]) -> type[T]:
        PROVIDER_REGISTRY[name] = cls
        return cls

    return decorator


def get_provider(config: ProviderConfig) -> LLMProvider:
    """Get a provider instance for the given configuration.

    Args:
        config: Provider configuration

    Returns:
        LLMProvider instance

    Raises:
        ProviderError: If provider is not registered
    """
    provider_name = config.provider.lower()

    if provider_name not in PROVIDER_REGISTRY:
        available = list(PROVIDER_REGISTRY.keys())
        raise ProviderError(
            message=f"Unknown provider: '{provider_name}'. Available: {available}",
            provider=provider_name,
            error_type="unknown_provider",
            details={"available_providers": available},
        )

    factory = PROVIDER_REGISTRY[provider_name]
    return factory(config)


def list_providers() -> list[str]:
    """List all registered provider names.

    Returns:
        List of registered provider names
    """
    return list(PROVIDER_REGISTRY.keys())


def is_provider_registered(name: str) -> bool:
    """Check if a provider is registered.

    Args:
        name: Provider name

    Returns:
        True if registered
    """
    return name.lower() in PROVIDER_REGISTRY
