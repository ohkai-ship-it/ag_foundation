"""Tests for AF-0094: Trace full I/O enrichment.

Tests the trace enrichment features:
1. Step model input_data/output_data fields
2. ChatResponse token tracking fields
3. TrackingLLMProvider usage accumulation
4. Runtime LLM usage population
5. Step output artifact saving
"""

from __future__ import annotations

from datetime import UTC, datetime

from ag.core.run_trace import Step, StepType
from ag.providers.base import ChatResponse

# ---------------------------------------------------------------------------
# Step Model Tests
# ---------------------------------------------------------------------------


class TestStepInputOutputData:
    """Tests for Step model input_data and output_data fields (AF-0094)."""

    def test_step_accepts_input_data(self) -> None:
        """Step model should accept input_data field."""
        step = Step(
            step_id="test-step-1",
            step_number=0,
            step_type=StepType.SKILL_CALL,
            skill_name="test_skill",
            input_summary="test input",
            output_summary="test output",
            started_at=datetime.now(UTC),
            input_data={"prompt": "test prompt", "param1": "value1"},
        )
        assert step.input_data == {"prompt": "test prompt", "param1": "value1"}

    def test_step_accepts_output_data(self) -> None:
        """Step model should accept output_data field."""
        step = Step(
            step_id="test-step-1",
            step_number=0,
            step_type=StepType.SKILL_CALL,
            skill_name="test_skill",
            input_summary="test input",
            output_summary="test output",
            started_at=datetime.now(UTC),
            output_data={"results": ["a", "b"], "count": 2},
        )
        assert step.output_data == {"results": ["a", "b"], "count": 2}

    def test_step_input_data_defaults_to_none(self) -> None:
        """input_data should default to None for backward compatibility."""
        step = Step(
            step_id="test-step-1",
            step_number=0,
            step_type=StepType.SKILL_CALL,
            skill_name="test_skill",
            input_summary="test",
            output_summary="test",
            started_at=datetime.now(UTC),
        )
        assert step.input_data is None

    def test_step_output_data_defaults_to_none(self) -> None:
        """output_data should default to None for backward compatibility."""
        step = Step(
            step_id="test-step-1",
            step_number=0,
            step_type=StepType.SKILL_CALL,
            skill_name="test_skill",
            input_summary="test",
            output_summary="test",
            started_at=datetime.now(UTC),
        )
        assert step.output_data is None

    def test_step_with_both_input_and_output_data(self) -> None:
        """Step should accept both input_data and output_data."""
        input_data = {"prompt": "search for X", "urls": ["http://a.com"]}
        output_data = {"documents": [{"url": "http://a.com", "content": "..."}]}

        step = Step(
            step_id="test-step-1",
            step_number=0,
            step_type=StepType.SKILL_CALL,
            skill_name="fetch_web_content",
            input_summary="Fetch URLs",
            output_summary="Fetched 1 URL",
            started_at=datetime.now(UTC),
            input_data=input_data,
            output_data=output_data,
        )
        assert step.input_data == input_data
        assert step.output_data == output_data

    def test_step_serializes_input_output_data(self) -> None:
        """Step should serialize input_data and output_data to JSON."""
        step = Step(
            step_id="test-step-1",
            step_number=0,
            step_type=StepType.SKILL_CALL,
            skill_name="test_skill",
            input_summary="test",
            output_summary="test",
            started_at=datetime.now(UTC),
            input_data={"key": "value"},
            output_data={"result": 42},
        )
        dumped = step.model_dump()
        assert dumped["input_data"] == {"key": "value"}
        assert dumped["output_data"] == {"result": 42}


# ---------------------------------------------------------------------------
# ChatResponse Token Tracking Tests
# ---------------------------------------------------------------------------


class TestChatResponseTokens:
    """Tests for ChatResponse token tracking fields (AF-0094)."""

    def test_chat_response_accepts_input_tokens(self) -> None:
        """ChatResponse should accept input_tokens field."""
        response = ChatResponse(
            content="Hello",
            model="gpt-4o-mini",
            provider="openai",
            tokens_used=100,
            input_tokens=80,
            output_tokens=20,
        )
        assert response.input_tokens == 80

    def test_chat_response_accepts_output_tokens(self) -> None:
        """ChatResponse should accept output_tokens field."""
        response = ChatResponse(
            content="Hello",
            model="gpt-4o-mini",
            provider="openai",
            tokens_used=100,
            input_tokens=80,
            output_tokens=20,
        )
        assert response.output_tokens == 20

    def test_chat_response_tokens_default_to_none(self) -> None:
        """input_tokens and output_tokens should default to None."""
        response = ChatResponse(
            content="Hello",
            model="gpt-4o-mini",
            provider="openai",
        )
        assert response.input_tokens is None
        assert response.output_tokens is None

    def test_chat_response_to_dict_includes_tokens(self) -> None:
        """to_dict should include input_tokens and output_tokens."""
        response = ChatResponse(
            content="Hello",
            model="gpt-4o-mini",
            provider="openai",
            tokens_used=100,
            input_tokens=80,
            output_tokens=20,
        )
        data = response.to_dict()
        assert data["input_tokens"] == 80
        assert data["output_tokens"] == 20


# ---------------------------------------------------------------------------
# TrackingLLMProvider Tests
# ---------------------------------------------------------------------------


class TestTrackingLLMProvider:
    """Tests for TrackingLLMProvider usage accumulation (AF-0094)."""

    def test_tracking_provider_wraps_underlying_provider(self) -> None:
        """TrackingLLMProvider should wrap an underlying provider."""
        from ag.core.runtime import TrackingLLMProvider

        class MockProvider:
            @property
            def name(self) -> str:
                return "mock"

            @property
            def is_stub(self) -> bool:
                return True

            def chat(self, messages, model=None, **kwargs):
                return ChatResponse(
                    content="response",
                    model="mock-model",
                    provider="mock",
                    tokens_used=100,
                    input_tokens=70,
                    output_tokens=30,
                )

        mock = MockProvider()
        tracker = TrackingLLMProvider(mock)

        assert tracker.name == "mock"
        assert tracker.is_stub is True

    def test_tracking_provider_accumulates_call_count(self) -> None:
        """TrackingLLMProvider should count LLM calls."""
        from ag.core.runtime import TrackingLLMProvider

        class MockProvider:
            @property
            def name(self) -> str:
                return "mock"

            @property
            def is_stub(self) -> bool:
                return False

            def chat(self, messages, model=None, **kwargs):
                return ChatResponse(
                    content="response",
                    model="mock-model",
                    provider="mock",
                )

        tracker = TrackingLLMProvider(MockProvider())
        assert tracker.call_count == 0

        tracker.chat([])
        assert tracker.call_count == 1

        tracker.chat([])
        tracker.chat([])
        assert tracker.call_count == 3

    def test_tracking_provider_accumulates_token_counts(self) -> None:
        """TrackingLLMProvider should accumulate token counts across calls."""
        from ag.core.runtime import TrackingLLMProvider

        call_number = 0

        class MockProvider:
            @property
            def name(self) -> str:
                return "mock"

            @property
            def is_stub(self) -> bool:
                return False

            def chat(self, messages, model=None, **kwargs):
                nonlocal call_number
                call_number += 1
                # Varying token counts per call
                if call_number == 1:
                    return ChatResponse(
                        content="first",
                        model="m",
                        provider="mock",
                        tokens_used=100,
                        input_tokens=60,
                        output_tokens=40,
                    )
                else:
                    return ChatResponse(
                        content="second",
                        model="m",
                        provider="mock",
                        tokens_used=200,
                        input_tokens=150,
                        output_tokens=50,
                    )

        tracker = TrackingLLMProvider(MockProvider())

        tracker.chat([])
        assert tracker.total_tokens == 100
        assert tracker.input_tokens == 60
        assert tracker.output_tokens == 40

        tracker.chat([])
        assert tracker.total_tokens == 300
        assert tracker.input_tokens == 210
        assert tracker.output_tokens == 90

    def test_tracking_provider_handles_none_tokens(self) -> None:
        """TrackingLLMProvider should handle None token values gracefully."""
        from ag.core.runtime import TrackingLLMProvider

        class MockProvider:
            @property
            def name(self) -> str:
                return "mock"

            @property
            def is_stub(self) -> bool:
                return False

            def chat(self, messages, model=None, **kwargs):
                return ChatResponse(
                    content="response",
                    model="m",
                    provider="mock",
                    tokens_used=None,
                    input_tokens=None,
                    output_tokens=None,
                )

        tracker = TrackingLLMProvider(MockProvider())
        tracker.chat([])

        # Should not raise, tokens remain 0
        assert tracker.call_count == 1
        assert tracker.total_tokens == 0
        assert tracker.input_tokens == 0
        assert tracker.output_tokens == 0

    def test_tracking_provider_get_usage(self) -> None:
        """get_usage should return accumulated statistics."""
        from ag.core.runtime import TrackingLLMProvider

        class MockProvider:
            @property
            def name(self) -> str:
                return "mock"

            @property
            def is_stub(self) -> bool:
                return False

            def chat(self, messages, model=None, **kwargs):
                return ChatResponse(
                    content="r",
                    model="m",
                    provider="p",
                    tokens_used=50,
                    input_tokens=30,
                    output_tokens=20,
                )

        tracker = TrackingLLMProvider(MockProvider())
        tracker.chat([])

        usage = tracker.get_usage()
        assert usage["call_count"] == 1
        assert usage["total_tokens"] == 50
        assert usage["input_tokens"] == 30
        assert usage["output_tokens"] == 20

    def test_tracking_provider_get_usage_returns_none_for_zero_tokens(self) -> None:
        """get_usage should return None for token fields when no tokens tracked."""
        from ag.core.runtime import TrackingLLMProvider

        class MockProvider:
            @property
            def name(self) -> str:
                return "mock"

            @property
            def is_stub(self) -> bool:
                return False

            def chat(self, messages, model=None, **kwargs):
                return ChatResponse(
                    content="r",
                    model="m",
                    provider="p",
                )

        tracker = TrackingLLMProvider(MockProvider())

        # No calls yet
        usage = tracker.get_usage()
        assert usage["call_count"] == 0
        assert usage["total_tokens"] is None
        assert usage["input_tokens"] is None
        assert usage["output_tokens"] is None


# ---------------------------------------------------------------------------
# LLMExecution Token Tracking Tests
# ---------------------------------------------------------------------------


class TestLLMExecutionTokens:
    """Tests for LLMExecution token tracking fields (AF-0094)."""

    def test_llm_execution_accepts_all_token_fields(self) -> None:
        """LLMExecution should accept all token tracking fields."""
        from ag.core.run_trace import LLMExecution

        llm = LLMExecution(
            provider="openai",
            model="gpt-4o-mini",
            call_count=3,
            total_tokens=1500,
            input_tokens=1000,
            output_tokens=500,
        )
        assert llm.call_count == 3
        assert llm.total_tokens == 1500
        assert llm.input_tokens == 1000
        assert llm.output_tokens == 500

    def test_llm_execution_token_fields_default_correctly(self) -> None:
        """LLMExecution token fields should default appropriately."""
        from ag.core.run_trace import LLMExecution

        llm = LLMExecution(
            provider="openai",
            model="gpt-4o-mini",
        )
        assert llm.call_count == 0
        assert llm.total_tokens is None
        assert llm.input_tokens is None
        assert llm.output_tokens is None


# ---------------------------------------------------------------------------
# Integration Tests
# ---------------------------------------------------------------------------


class TestTraceEnrichmentIntegration:
    """Integration tests for trace enrichment in runtime."""

    def test_step_output_includes_failed_urls_from_fetch(self) -> None:
        """fetch_web_content output should include failed_urls in step output_data."""
        from ag.skills.base import SkillContext
        from ag.skills.fetch_web_content import (
            FetchWebContentInput,
            FetchWebContentSkill,
        )

        skill = FetchWebContentSkill()
        # Invalid URL that will fail
        input = FetchWebContentInput(urls=["not-a-valid-url"])
        output = skill.execute(input, SkillContext())

        # The output should have failed_urls populated
        assert "not-a-valid-url" in output.failed_urls
        assert output.total_failed == 1

        # When serialized to dict (as would happen in runtime), failed_urls is present
        output_dict = output.model_dump()
        assert "failed_urls" in output_dict
        assert "not-a-valid-url" in output_dict["failed_urls"]
