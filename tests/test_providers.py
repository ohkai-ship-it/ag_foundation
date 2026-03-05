"""Tests for LLM provider abstraction.

Coverage targets:
- Provider registration and selection
- Stub behavior (fail fast with structured error)
- OpenAI provider config validation (mocked)
- Provider error handling

Sprint 02 policy:
- OpenAI is the only real provider
- Anthropic and local are stubs that fail fast
"""

from __future__ import annotations

import pytest

from ag.providers import (
    ChatMessage,
    ChatResponse,
    LLMProvider,
    MessageRole,
    OpenAIProvider,
    ProviderConfig,
    ProviderError,
    ProviderNotImplementedError,
    get_provider,
    is_provider_registered,
    list_providers,
)


class TestProviderRegistry:
    """Tests for provider registration and selection."""

    def test_openai_registered(self) -> None:
        """OpenAI provider should be registered."""
        assert is_provider_registered("openai")

    def test_anthropic_registered(self) -> None:
        """Anthropic stub should be registered."""
        assert is_provider_registered("anthropic")

    def test_local_registered(self) -> None:
        """Local stub should be registered."""
        assert is_provider_registered("local")

    def test_list_providers_includes_all(self) -> None:
        """list_providers should include all registered providers."""
        providers = list_providers()
        assert "openai" in providers
        assert "anthropic" in providers
        assert "local" in providers

    def test_get_provider_returns_correct_type(self) -> None:
        """get_provider should return correct provider type."""
        config = ProviderConfig(provider="openai", model="gpt-4")
        provider = get_provider(config)
        assert isinstance(provider, OpenAIProvider)

    def test_get_provider_unknown_raises_error(self) -> None:
        """get_provider should raise ProviderError for unknown provider."""
        config = ProviderConfig(provider="unknown", model="test")
        with pytest.raises(ProviderError) as exc_info:
            get_provider(config)
        assert exc_info.value.error_type == "unknown_provider"
        assert "unknown" in exc_info.value.message.lower()

    def test_get_provider_case_insensitive(self) -> None:
        """Provider selection should be case-insensitive."""
        config = ProviderConfig(provider="OpenAI", model="gpt-4")
        provider = get_provider(config)
        assert provider.name == "openai"


class TestStubProviders:
    """Tests for stub provider behavior (fail fast with structured error)."""

    def test_anthropic_is_stub(self) -> None:
        """Anthropic provider should be marked as stub."""
        config = ProviderConfig(provider="anthropic", model="claude-3")
        provider = get_provider(config)
        assert provider.is_stub is True

    def test_local_is_stub(self) -> None:
        """Local provider should be marked as stub."""
        config = ProviderConfig(provider="local", model="llama")
        provider = get_provider(config)
        assert provider.is_stub is True

    def test_openai_is_not_stub(self) -> None:
        """OpenAI provider should NOT be marked as stub."""
        config = ProviderConfig(provider="openai", model="gpt-4")
        provider = get_provider(config)
        assert provider.is_stub is False

    def test_anthropic_chat_fails_fast(self) -> None:
        """Anthropic stub chat() should fail fast with structured error."""
        config = ProviderConfig(provider="anthropic", model="claude-3")
        provider = get_provider(config)

        messages = [ChatMessage(role=MessageRole.USER, content="Hello")]

        with pytest.raises(ProviderNotImplementedError) as exc_info:
            provider.chat(messages)

        error = exc_info.value
        assert error.provider == "anthropic"
        assert error.error_type == "not_implemented"
        assert error.details["stub"] is True

    def test_local_chat_fails_fast(self) -> None:
        """Local stub chat() should fail fast with structured error."""
        config = ProviderConfig(provider="local", model="llama")
        provider = get_provider(config)

        messages = [ChatMessage(role=MessageRole.USER, content="Hello")]

        with pytest.raises(ProviderNotImplementedError) as exc_info:
            provider.chat(messages)

        error = exc_info.value
        assert error.provider == "local"
        assert error.error_type == "not_implemented"

    def test_anthropic_validate_fails_fast(self) -> None:
        """Anthropic stub validate_config() should fail fast."""
        config = ProviderConfig(provider="anthropic", model="claude-3")
        provider = get_provider(config)

        with pytest.raises(ProviderNotImplementedError):
            provider.validate_config()

    def test_stub_error_is_serializable(self) -> None:
        """Stub errors should be serializable for trace recording."""
        config = ProviderConfig(provider="anthropic", model="claude-3")
        provider = get_provider(config)

        messages = [ChatMessage(role=MessageRole.USER, content="Hello")]

        try:
            provider.chat(messages)
        except ProviderNotImplementedError as e:
            error_dict = e.to_dict()
            assert "error_type" in error_dict
            assert "provider" in error_dict
            assert "message" in error_dict
            assert "details" in error_dict


class TestOpenAIProvider:
    """Tests for OpenAI provider configuration (mocked, no real API calls)."""

    def test_openai_name(self) -> None:
        """OpenAI provider should have correct name."""
        config = ProviderConfig(provider="openai", model="gpt-4")
        provider = get_provider(config)
        assert provider.name == "openai"

    def test_openai_validate_without_key_raises(self) -> None:
        """validate_config should fail without API key."""
        from ag.providers.openai import _openai_sdk_available

        if not _openai_sdk_available:
            pytest.skip("OpenAI SDK not installed - skipping SDK-dependent test")

        # Clear any env var BEFORE creating provider (reads key at init)
        import os

        original = os.environ.pop("OPENAI_API_KEY", None)

        try:
            config = ProviderConfig(provider="openai", model="gpt-4", api_key=None)
            provider = get_provider(config)
            with pytest.raises(ProviderError) as exc_info:
                provider.validate_config()
            assert exc_info.value.error_type == "config_error"
        finally:
            if original:
                os.environ["OPENAI_API_KEY"] = original

    def test_openai_chat_without_key_raises(self) -> None:
        """chat() should fail without API key."""
        from ag.providers.openai import _openai_sdk_available

        if not _openai_sdk_available:
            pytest.skip("OpenAI SDK not installed - skipping SDK-dependent test")

        # Clear any env var BEFORE creating provider (reads key at init)
        import os

        original = os.environ.pop("OPENAI_API_KEY", None)

        try:
            config = ProviderConfig(provider="openai", model="gpt-4", api_key=None)
            provider = get_provider(config)
            messages = [ChatMessage(role=MessageRole.USER, content="Hello")]
            with pytest.raises(ProviderError) as exc_info:
                provider.chat(messages)
            assert exc_info.value.error_type == "auth_error"
        finally:
            if original:
                os.environ["OPENAI_API_KEY"] = original


class TestOpenAIProviderMocked:
    """Mocked tests for OpenAI provider chat() method.

    These tests mock the OpenAI client to test request/response mapping
    without making real API calls.
    """

    def test_chat_maps_messages_correctly(self, mocker) -> None:
        """chat() should convert messages to OpenAI format."""
        # Mock the _get_openai_class function
        mock_openai_class = mocker.MagicMock()
        mock_client = mocker.MagicMock()
        mock_openai_class.return_value = mock_client
        mocker.patch("ag.providers.openai._get_openai_class", return_value=mock_openai_class)

        # Mock response
        mock_choice = mocker.MagicMock()
        mock_choice.message.content = "Hello back!"
        mock_choice.finish_reason = "stop"

        mock_usage = mocker.MagicMock()
        mock_usage.total_tokens = 25

        mock_response = mocker.MagicMock()
        mock_response.choices = [mock_choice]
        mock_response.model = "gpt-4"
        mock_response.usage = mock_usage

        mock_client.chat.completions.create.return_value = mock_response

        # Create provider with API key
        config = ProviderConfig(provider="openai", model="gpt-4", api_key="test-key")
        provider = get_provider(config)

        # Send message
        messages = [
            ChatMessage(role=MessageRole.SYSTEM, content="You are helpful"),
            ChatMessage(role=MessageRole.USER, content="Hello"),
        ]
        response = provider.chat(messages)

        # Verify response mapping
        assert response.content == "Hello back!"
        assert response.model == "gpt-4"
        assert response.provider == "openai"
        assert response.tokens_used == 25
        assert response.finish_reason == "stop"

        # Verify correct messages sent to API
        call_args = mock_client.chat.completions.create.call_args
        sent_messages = call_args.kwargs["messages"]
        assert len(sent_messages) == 2
        assert sent_messages[0] == {"role": "system", "content": "You are helpful"}
        assert sent_messages[1] == {"role": "user", "content": "Hello"}

    def test_chat_uses_model_from_config(self, mocker) -> None:
        """chat() should use model from config if not overridden."""
        mock_openai_class = mocker.MagicMock()
        mock_client = mocker.MagicMock()
        mock_openai_class.return_value = mock_client
        mocker.patch("ag.providers.openai._get_openai_class", return_value=mock_openai_class)

        mock_choice = mocker.MagicMock()
        mock_choice.message.content = "Response"
        mock_choice.finish_reason = "stop"

        mock_response = mocker.MagicMock()
        mock_response.choices = [mock_choice]
        mock_response.model = "gpt-4-turbo"
        mock_response.usage = None

        mock_client.chat.completions.create.return_value = mock_response

        config = ProviderConfig(provider="openai", model="gpt-4-turbo", api_key="test-key")
        provider = get_provider(config)

        messages = [ChatMessage(role=MessageRole.USER, content="Hello")]
        provider.chat(messages)

        call_args = mock_client.chat.completions.create.call_args
        assert call_args.kwargs["model"] == "gpt-4-turbo"

    def test_chat_allows_model_override(self, mocker) -> None:
        """chat() should allow model override in parameters."""
        mock_openai_class = mocker.MagicMock()
        mock_client = mocker.MagicMock()
        mock_openai_class.return_value = mock_client
        mocker.patch("ag.providers.openai._get_openai_class", return_value=mock_openai_class)

        mock_choice = mocker.MagicMock()
        mock_choice.message.content = "Response"
        mock_choice.finish_reason = "stop"

        mock_response = mocker.MagicMock()
        mock_response.choices = [mock_choice]
        mock_response.model = "gpt-3.5-turbo"
        mock_response.usage = None

        mock_client.chat.completions.create.return_value = mock_response

        config = ProviderConfig(provider="openai", model="gpt-4", api_key="test-key")
        provider = get_provider(config)

        messages = [ChatMessage(role=MessageRole.USER, content="Hello")]
        provider.chat(messages, model="gpt-3.5-turbo")

        call_args = mock_client.chat.completions.create.call_args
        assert call_args.kwargs["model"] == "gpt-3.5-turbo"

    def test_chat_response_excludes_raw_response(self, mocker) -> None:
        """ChatResponse should not include raw_response (trace safety)."""
        mock_openai_class = mocker.MagicMock()
        mock_client = mocker.MagicMock()
        mock_openai_class.return_value = mock_client
        mocker.patch("ag.providers.openai._get_openai_class", return_value=mock_openai_class)

        mock_choice = mocker.MagicMock()
        mock_choice.message.content = "Response"
        mock_choice.finish_reason = "stop"

        mock_response = mocker.MagicMock()
        mock_response.choices = [mock_choice]
        mock_response.model = "gpt-4"
        mock_response.usage = None

        mock_client.chat.completions.create.return_value = mock_response

        config = ProviderConfig(provider="openai", model="gpt-4", api_key="test-key")
        provider = get_provider(config)

        messages = [ChatMessage(role=MessageRole.USER, content="Hello")]
        response = provider.chat(messages)

        # raw_response should be None (not stored for trace safety)
        assert response.raw_response is None

    def test_chat_handles_api_error(self, mocker) -> None:
        """chat() should map API errors to ProviderError."""
        mock_openai_class = mocker.MagicMock()
        mock_client = mocker.MagicMock()
        mock_openai_class.return_value = mock_client
        mocker.patch("ag.providers.openai._get_openai_class", return_value=mock_openai_class)

        # Simulate API error
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        config = ProviderConfig(provider="openai", model="gpt-4", api_key="test-key")
        provider = get_provider(config)

        messages = [ChatMessage(role=MessageRole.USER, content="Hello")]

        with pytest.raises(ProviderError) as exc_info:
            provider.chat(messages)

        assert exc_info.value.provider == "openai"
        assert exc_info.value.error_type == "api_error"
        assert "API Error" in exc_info.value.message

    def test_openai_client_uses_config_timeout(self, mocker) -> None:
        """OpenAI client should use timeout from config."""
        mock_openai_class = mocker.MagicMock()
        mock_client = mocker.MagicMock()
        mock_openai_class.return_value = mock_client
        mocker.patch("ag.providers.openai._get_openai_class", return_value=mock_openai_class)

        mock_choice = mocker.MagicMock()
        mock_choice.message.content = "Response"
        mock_choice.finish_reason = "stop"

        mock_response = mocker.MagicMock()
        mock_response.choices = [mock_choice]
        mock_response.model = "gpt-4"
        mock_response.usage = None

        mock_client.chat.completions.create.return_value = mock_response

        config = ProviderConfig(
            provider="openai",
            model="gpt-4",
            api_key="test-key",
            timeout=120,
            max_retries=5,
        )
        provider = get_provider(config)

        messages = [ChatMessage(role=MessageRole.USER, content="Hello")]
        provider.chat(messages)

        # Verify client was created with config settings
        mock_openai_class.assert_called_once()
        call_kwargs = mock_openai_class.call_args.kwargs
        assert call_kwargs["timeout"] == 120.0
        assert call_kwargs["max_retries"] == 5


class TestOpenAIProviderIntegration:
    """Optional integration tests that require real OpenAI API key.

    These tests are marked with 'integration' and skipped in CI.
    Run locally with: pytest -m integration
    """

    @pytest.mark.integration
    def test_real_chat_completion(self) -> None:
        """Integration test: actual OpenAI API call (requires API key)."""
        import os

        from dotenv import load_dotenv

        load_dotenv()  # Load .env file if present
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            pytest.skip("OPENAI_API_KEY not set, skipping integration test")

        config = ProviderConfig(provider="openai", model="gpt-4o-mini", api_key=api_key)
        provider = get_provider(config)

        messages = [
            ChatMessage(role=MessageRole.USER, content="Say 'hello' in one word."),
        ]

        response = provider.chat(messages)

        assert response.content  # Non-empty response
        assert response.provider == "openai"
        assert "gpt" in response.model.lower()
        assert response.tokens_used is not None


class TestProviderConfig:
    """Tests for ProviderConfig."""

    def test_from_dict(self) -> None:
        """ProviderConfig.from_dict should create valid config."""
        data = {
            "provider": "openai",
            "model": "gpt-4-turbo",
            "timeout": 120,
        }
        config = ProviderConfig.from_dict(data)
        assert config.provider == "openai"
        assert config.model == "gpt-4-turbo"
        assert config.timeout == 120

    def test_to_dict_excludes_api_key(self) -> None:
        """to_dict should not include api_key (trace safety)."""
        config = ProviderConfig(
            provider="openai",
            model="gpt-4",
            api_key="sk-secret-key",
        )
        data = config.to_dict()
        assert "api_key" not in data
        assert data["provider"] == "openai"

    def test_defaults(self) -> None:
        """ProviderConfig should have sensible defaults."""
        config = ProviderConfig(provider="openai", model="gpt-4")
        assert config.timeout == 60
        assert config.max_retries == 2
        assert config.base_url is None


class TestChatMessage:
    """Tests for ChatMessage."""

    def test_to_dict(self) -> None:
        """ChatMessage.to_dict should return provider-agnostic format."""
        msg = ChatMessage(role=MessageRole.USER, content="Hello")
        data = msg.to_dict()
        assert data == {"role": "user", "content": "Hello"}

    def test_system_message(self) -> None:
        """System messages should work correctly."""
        msg = ChatMessage(role=MessageRole.SYSTEM, content="You are helpful")
        assert msg.role == MessageRole.SYSTEM
        assert msg.to_dict()["role"] == "system"


class TestChatResponse:
    """Tests for ChatResponse."""

    def test_to_dict(self) -> None:
        """ChatResponse.to_dict should return serializable format."""
        response = ChatResponse(
            content="Hello!",
            model="gpt-4",
            provider="openai",
            tokens_used=10,
        )
        data = response.to_dict()
        assert data["content"] == "Hello!"
        assert data["model"] == "gpt-4"
        assert data["provider"] == "openai"
        assert data["tokens_used"] == 10
        assert "created_at" in data


class TestProviderError:
    """Tests for ProviderError."""

    def test_error_to_dict(self) -> None:
        """ProviderError.to_dict should be serializable."""
        error = ProviderError(
            message="Test error",
            provider="openai",
            error_type="test",
            details={"key": "value"},
        )
        data = error.to_dict()
        assert data["error_type"] == "test"
        assert data["provider"] == "openai"
        assert data["message"] == "Test error"
        assert data["details"]["key"] == "value"

    def test_not_implemented_is_provider_error(self) -> None:
        """ProviderNotImplementedError should be a ProviderError."""
        error = ProviderNotImplementedError("test")
        assert isinstance(error, ProviderError)
        assert error.error_type == "not_implemented"


class TestLLMProviderProtocol:
    """Tests for LLMProvider protocol compliance."""

    def test_openai_implements_protocol(self) -> None:
        """OpenAI provider should implement LLMProvider protocol."""
        config = ProviderConfig(provider="openai", model="gpt-4")
        provider = get_provider(config)
        assert isinstance(provider, LLMProvider)

    def test_anthropic_implements_protocol(self) -> None:
        """Anthropic stub should implement LLMProvider protocol."""
        config = ProviderConfig(provider="anthropic", model="claude-3")
        provider = get_provider(config)
        assert isinstance(provider, LLMProvider)

    def test_local_implements_protocol(self) -> None:
        """Local stub should implement LLMProvider protocol."""
        config = ProviderConfig(provider="local", model="llama")
        provider = get_provider(config)
        assert isinstance(provider, LLMProvider)


# ---------------------------------------------------------------------------
# AF-0022: OpenAI Provider Coverage Hardening Tests
# ---------------------------------------------------------------------------


class TestOpenAISDKAvailability:
    """Tests for OpenAI SDK availability handling (AF-0022)."""

    def test_sdk_not_installed_raises_provider_error(self, mocker) -> None:
        """_get_openai_class should raise ProviderError when SDK not installed."""
        # Patch _openai_sdk_available to False
        mocker.patch("ag.providers.openai._openai_sdk_available", False)

        from ag.providers.openai import _get_openai_class

        with pytest.raises(ProviderError) as exc_info:
            _get_openai_class()

        assert exc_info.value.error_type == "dependency_error"
        assert "OpenAI SDK not installed" in exc_info.value.message
        assert exc_info.value.details["missing_package"] == "openai"

    def test_sdk_installed_returns_openai_class(self) -> None:
        """_get_openai_class should return OpenAI class when SDK installed."""
        from ag.providers.openai import _get_openai_class, _OpenAI, _openai_sdk_available

        if not _openai_sdk_available:
            pytest.skip("OpenAI SDK not installed - skipping SDK-present test")

        result = _get_openai_class()
        assert result is _OpenAI


class TestOpenAIClientCaching:
    """Tests for OpenAI client caching (AF-0022)."""

    def test_client_cached_on_second_call(self, mocker) -> None:
        """_get_client should reuse cached client on second call."""
        mock_openai_class = mocker.MagicMock()
        mock_client = mocker.MagicMock()
        mock_openai_class.return_value = mock_client
        mocker.patch("ag.providers.openai._get_openai_class", return_value=mock_openai_class)

        config = ProviderConfig(provider="openai", model="gpt-4", api_key="test-key")
        provider = get_provider(config)

        # First call - creates client
        client1 = provider._get_client()
        assert client1 is mock_client
        assert mock_openai_class.call_count == 1

        # Second call - returns cached client
        client2 = provider._get_client()
        assert client2 is mock_client
        assert mock_openai_class.call_count == 1  # Still 1, not 2


class TestOpenAIErrorMapping:
    """Tests for OpenAI error type mapping in chat() (AF-0022)."""

    def test_authentication_error_mapping(self, mocker) -> None:
        """AuthenticationError should map to auth_error type."""
        mock_openai_class = mocker.MagicMock()
        mock_client = mocker.MagicMock()
        mock_openai_class.return_value = mock_client
        mocker.patch("ag.providers.openai._get_openai_class", return_value=mock_openai_class)

        # Create a fake AuthenticationError class
        class AuthenticationError(Exception):
            pass

        mock_client.chat.completions.create.side_effect = AuthenticationError("Invalid API key")

        config = ProviderConfig(provider="openai", model="gpt-4", api_key="test-key")
        provider = get_provider(config)

        messages = [ChatMessage(role=MessageRole.USER, content="Hello")]

        with pytest.raises(ProviderError) as exc_info:
            provider.chat(messages)

        assert exc_info.value.error_type == "auth_error"
        assert exc_info.value.details["error_class"] == "AuthenticationError"

    def test_rate_limit_error_mapping(self, mocker) -> None:
        """RateLimitError should map to rate_limit type."""
        mock_openai_class = mocker.MagicMock()
        mock_client = mocker.MagicMock()
        mock_openai_class.return_value = mock_client
        mocker.patch("ag.providers.openai._get_openai_class", return_value=mock_openai_class)

        # Create a fake RateLimitError class
        class RateLimitError(Exception):
            pass

        mock_client.chat.completions.create.side_effect = RateLimitError("Rate limit exceeded")

        config = ProviderConfig(provider="openai", model="gpt-4", api_key="test-key")
        provider = get_provider(config)

        messages = [ChatMessage(role=MessageRole.USER, content="Hello")]

        with pytest.raises(ProviderError) as exc_info:
            provider.chat(messages)

        assert exc_info.value.error_type == "rate_limit"
        assert exc_info.value.details["error_class"] == "RateLimitError"

    def test_timeout_error_mapping(self, mocker) -> None:
        """Timeout errors should map to timeout type."""
        mock_openai_class = mocker.MagicMock()
        mock_client = mocker.MagicMock()
        mock_openai_class.return_value = mock_client
        mocker.patch("ag.providers.openai._get_openai_class", return_value=mock_openai_class)

        # Create a fake Timeout class
        class TimeoutError(Exception):
            pass

        mock_client.chat.completions.create.side_effect = TimeoutError("Request timed out")

        config = ProviderConfig(provider="openai", model="gpt-4", api_key="test-key")
        provider = get_provider(config)

        messages = [ChatMessage(role=MessageRole.USER, content="Hello")]

        with pytest.raises(ProviderError) as exc_info:
            provider.chat(messages)

        assert exc_info.value.error_type == "timeout"
        assert exc_info.value.details["error_class"] == "TimeoutError"


class TestOpenAIValidation:
    """Tests for OpenAI validate_config() success path (AF-0022)."""

    def test_validate_config_success(self) -> None:
        """validate_config should return True when API key is set."""
        config = ProviderConfig(provider="openai", model="gpt-4", api_key="test-api-key")
        provider = get_provider(config)

        result = provider.validate_config()
        assert result is True
