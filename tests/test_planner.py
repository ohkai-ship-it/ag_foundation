"""Unit tests for V1Planner (AF-0102).

Tests cover:
1. Happy path: LLM returns valid plan → Playbook generated
2. Skill catalog extraction from registry
3. LLM response parsing (JSON, markdown code blocks)
4. Error handling (invalid JSON, missing skills, LLM errors)
5. Validation of referenced skills
6. Playbook structure correctness
"""

from __future__ import annotations

from unittest.mock import MagicMock, PropertyMock

import pytest

from ag.core import (
    Budgets,
    Constraints,
    ExecutionMode,
    PlannerError,
    Playbook,
    PlaybookStepType,
    TaskSpec,
    V1Planner,
)
from ag.providers.base import ChatResponse, LLMProvider, MessageRole
from ag.skills import SkillRegistry
from ag.skills.base import Skill, SkillContext, SkillInput, SkillOutput

# ---------------------------------------------------------------------------
# Test Fixtures
# ---------------------------------------------------------------------------


class MockSkillInput(SkillInput):
    """Mock skill input schema."""

    query: str = ""


class MockSkillOutput(SkillOutput):
    """Mock skill output schema."""

    result: str = ""


class MockSkill(Skill[MockSkillInput, MockSkillOutput]):
    """Mock skill for testing."""

    name = "mock_skill"
    description = "A mock skill for testing"
    input_schema = MockSkillInput
    output_schema = MockSkillOutput
    requires_llm = False

    def execute(self, input_data: MockSkillInput, ctx: SkillContext) -> MockSkillOutput:
        return MockSkillOutput(result="mock result")


class MockLLMSkill(Skill[MockSkillInput, MockSkillOutput]):
    """Mock LLM skill for testing."""

    name = "mock_llm_skill"
    description = "A mock LLM skill that requires provider"
    input_schema = MockSkillInput
    output_schema = MockSkillOutput
    requires_llm = True

    def execute(self, input_data: MockSkillInput, ctx: SkillContext) -> MockSkillOutput:
        return MockSkillOutput(result="llm result")


@pytest.fixture
def mock_registry() -> SkillRegistry:
    """Create a mock skill registry with test skills."""
    registry = SkillRegistry()
    registry.register(MockSkill(), source="test-stub")
    registry.register(MockLLMSkill(), source="test-stub")
    return registry


@pytest.fixture
def mock_provider() -> MagicMock:
    """Create a mock LLM provider."""
    provider = MagicMock(spec=LLMProvider)
    type(provider).name = PropertyMock(return_value="mock")
    type(provider).is_stub = PropertyMock(return_value=True)
    return provider


@pytest.fixture
def task_spec() -> TaskSpec:
    """Create a test TaskSpec."""
    return TaskSpec(
        prompt="Test task: do something useful",
        workspace_id="test-workspace",
        mode=ExecutionMode.SUPERVISED,
        budgets=Budgets(),
        constraints=Constraints(),
    )


# ---------------------------------------------------------------------------
# Test Data Constants
# ---------------------------------------------------------------------------

# Common JSON patterns for mocking LLM responses
SIMPLE_PLAN_JSON = (
    '{"steps": [{"skill": "mock_skill", "params": {}, "rationale": "test"}], '
    '"estimated_tokens": 100, "confidence": 0.8}'
)

SIMPLE_PLAN_WITH_WARNINGS = (
    '{"steps": [{"skill": "mock_skill", "params": {}, "rationale": "test"}], '
    '"estimated_tokens": 100, "confidence": 0.8, "warnings": []}'
)


# ---------------------------------------------------------------------------
# Happy Path Tests
# ---------------------------------------------------------------------------


class TestV1PlannerHappyPath:
    """Happy path tests for V1Planner."""

    def test_plan_returns_playbook(
        self, mock_provider: MagicMock, mock_registry: SkillRegistry, task_spec: TaskSpec
    ) -> None:
        """V1Planner returns a Playbook object."""
        # Arrange: Mock LLM to return valid plan
        plan_json = (
            '{"steps": [{"skill": "mock_skill", "params": {"query": "test"}, '
            '"rationale": "Test step"}], "estimated_tokens": 100, '
            '"confidence": 0.9, "warnings": []}'
        )
        mock_provider.chat.return_value = ChatResponse(
            content=plan_json,
            model="mock-model",
            provider="mock",
            tokens_used=50,
            finish_reason="stop",
            created_at=None,
            raw_response=None,
        )

        planner = V1Planner(mock_provider, mock_registry)

        # Act
        result = planner.plan(task_spec)

        # Assert
        assert isinstance(result, Playbook)
        assert len(result.steps) == 1
        assert result.steps[0].skill_name == "mock_skill"

    def test_plan_includes_metadata(
        self, mock_provider: MagicMock, mock_registry: SkillRegistry, task_spec: TaskSpec
    ) -> None:
        """Generated playbook includes V1Planner metadata."""
        plan_json = (
            '{"steps": [{"skill": "mock_skill", "params": {}, "rationale": "Do it"}], '
            '"estimated_tokens": 200, "confidence": 0.85, "warnings": ["Be careful"]}'
        )
        mock_provider.chat.return_value = ChatResponse(
            content=plan_json,
            model="mock-model",
            provider="mock",
            tokens_used=50,
            finish_reason="stop",
            created_at=None,
            raw_response=None,
        )

        planner = V1Planner(mock_provider, mock_registry)
        result = planner.plan(task_spec)

        # Check metadata
        assert result.metadata["generated_by"] == "V1Planner"
        assert result.metadata["confidence"] == 0.85
        assert "Be careful" in result.metadata["warnings"]
        assert "generated_at" in result.metadata

    def test_plan_with_multiple_steps(
        self, mock_provider: MagicMock, mock_registry: SkillRegistry, task_spec: TaskSpec
    ) -> None:
        """V1Planner handles multi-step plans."""
        plan_json = """{
            "steps": [
                {"skill": "mock_skill", "params": {"query": "step 1"}, "rationale": "First"},
                {"skill": "mock_llm_skill", "params": {"query": "s2"}, "rationale": "Second"}
            ],
            "estimated_tokens": 500,
            "confidence": 0.75,
            "warnings": []
        }"""
        mock_provider.chat.return_value = ChatResponse(
            content=plan_json,
            model="mock-model",
            provider="mock",
            tokens_used=100,
            finish_reason="stop",
            created_at=None,
            raw_response=None,
        )

        planner = V1Planner(mock_provider, mock_registry)
        result = planner.plan(task_spec)

        assert len(result.steps) == 2
        assert result.steps[0].skill_name == "mock_skill"
        assert result.steps[1].skill_name == "mock_llm_skill"
        # Verify step naming
        assert result.steps[0].name == "mock_skill_0"
        assert result.steps[1].name == "mock_llm_skill_1"


# ---------------------------------------------------------------------------
# Skill Catalog Tests
# ---------------------------------------------------------------------------


class TestSkillCatalogExtraction:
    """Tests for skill catalog extraction."""

    def test_catalog_includes_all_skills(
        self, mock_provider: MagicMock, mock_registry: SkillRegistry
    ) -> None:
        """Skill catalog includes all registered skills."""
        planner = V1Planner(mock_provider, mock_registry)
        catalog = planner._get_skill_catalog()

        skill_names = [s["name"] for s in catalog]
        assert "mock_skill" in skill_names
        assert "mock_llm_skill" in skill_names

    def test_catalog_includes_requires_llm_flag(
        self, mock_provider: MagicMock, mock_registry: SkillRegistry
    ) -> None:
        """Skill catalog includes requires_llm flag."""
        planner = V1Planner(mock_provider, mock_registry)
        catalog = planner._get_skill_catalog()

        skills_by_name = {s["name"]: s for s in catalog}
        assert skills_by_name["mock_skill"]["requires_llm"] is False
        assert skills_by_name["mock_llm_skill"]["requires_llm"] is True


# ---------------------------------------------------------------------------
# Response Parsing Tests
# ---------------------------------------------------------------------------


class TestResponseParsing:
    """Tests for LLM response parsing."""

    def test_parse_json_response(
        self, mock_provider: MagicMock, mock_registry: SkillRegistry
    ) -> None:
        """Parser handles plain JSON response."""
        planner = V1Planner(mock_provider, mock_registry)

        response = planner._parse_response(SIMPLE_PLAN_JSON)

        assert len(response.steps) == 1
        assert response.steps[0].skill == "mock_skill"
        assert response.confidence == 0.8

    def test_parse_markdown_code_block(
        self, mock_provider: MagicMock, mock_registry: SkillRegistry
    ) -> None:
        """Parser handles JSON in markdown code block."""
        planner = V1Planner(mock_provider, mock_registry)

        md_json = f"```json\n{SIMPLE_PLAN_JSON}\n```"
        response = planner._parse_response(md_json)

        assert len(response.steps) == 1
        assert response.steps[0].skill == "mock_skill"

    def test_parse_response_with_extra_fields(
        self, mock_provider: MagicMock, mock_registry: SkillRegistry
    ) -> None:
        """Parser ignores extra fields from LLM (extra='ignore')."""
        planner = V1Planner(mock_provider, mock_registry)

        # LLM might add extra fields we didn't ask for
        json_with_extra = (
            '{"steps": [{"skill": "mock_skill", "params": {}, '
            '"rationale": "test"}], "estimated_tokens": 100, '
            '"confidence": 0.8, "extra_field": "ignored"}'
        )
        response = planner._parse_response(json_with_extra)

        assert len(response.steps) == 1

    def test_parse_invalid_json_raises_error(
        self, mock_provider: MagicMock, mock_registry: SkillRegistry
    ) -> None:
        """Parser raises PlannerError for invalid JSON."""
        planner = V1Planner(mock_provider, mock_registry)

        with pytest.raises(PlannerError, match="Invalid JSON"):
            planner._parse_response("not valid json {")

    def test_parse_missing_steps_raises_error(
        self, mock_provider: MagicMock, mock_registry: SkillRegistry
    ) -> None:
        """Parser raises PlannerError when steps are missing."""
        planner = V1Planner(mock_provider, mock_registry)

        with pytest.raises(PlannerError, match="doesn't match schema"):
            planner._parse_response('{"estimated_tokens": 100}')  # Missing steps


# ---------------------------------------------------------------------------
# Error Handling Tests
# ---------------------------------------------------------------------------


class TestErrorHandling:
    """Tests for error handling."""

    def test_invalid_skill_raises_error(
        self, mock_provider: MagicMock, mock_registry: SkillRegistry, task_spec: TaskSpec
    ) -> None:
        """PlannerError raised when LLM references non-existent skill."""
        bad_skill_json = (
            '{"steps": [{"skill": "nonexistent_skill", "params": {}, '
            '"rationale": "test"}], "estimated_tokens": 100, "confidence": 0.8}'
        )
        mock_provider.chat.return_value = ChatResponse(
            content=bad_skill_json,
            model="mock-model",
            provider="mock",
            tokens_used=50,
            finish_reason="stop",
            created_at=None,
            raw_response=None,
        )

        planner = V1Planner(mock_provider, mock_registry)

        with pytest.raises(PlannerError, match="Invalid skill 'nonexistent_skill'"):
            planner.plan(task_spec)

    def test_llm_error_raises_planner_error(
        self, mock_provider: MagicMock, mock_registry: SkillRegistry, task_spec: TaskSpec
    ) -> None:
        """PlannerError raised when LLM call fails."""
        mock_provider.chat.side_effect = Exception("API timeout")

        planner = V1Planner(mock_provider, mock_registry)

        with pytest.raises(PlannerError, match="LLM call failed"):
            planner.plan(task_spec)

    def test_empty_registry_raises_error(
        self, mock_provider: MagicMock, task_spec: TaskSpec
    ) -> None:
        """PlannerError raised when no skills available."""
        empty_registry = SkillRegistry()

        planner = V1Planner(mock_provider, empty_registry)

        with pytest.raises(PlannerError, match="No skills available"):
            planner.plan(task_spec)


# ---------------------------------------------------------------------------
# Playbook Structure Tests
# ---------------------------------------------------------------------------


class TestPlaybookStructure:
    """Tests for generated Playbook structure."""

    def test_playbook_step_types(
        self, mock_provider: MagicMock, mock_registry: SkillRegistry, task_spec: TaskSpec
    ) -> None:
        """Generated steps have correct step_type."""
        mock_provider.chat.return_value = ChatResponse(
            content=SIMPLE_PLAN_JSON,
            model="mock-model",
            provider="mock",
            tokens_used=50,
            finish_reason="stop",
            created_at=None,
            raw_response=None,
        )

        planner = V1Planner(mock_provider, mock_registry)
        result = planner.plan(task_spec)

        assert result.steps[0].step_type == PlaybookStepType.SKILL

    def test_playbook_steps_have_retry_count(
        self, mock_provider: MagicMock, mock_registry: SkillRegistry, task_spec: TaskSpec
    ) -> None:
        """Generated steps have retry_count set."""
        mock_provider.chat.return_value = ChatResponse(
            content=SIMPLE_PLAN_JSON,
            model="mock-model",
            provider="mock",
            tokens_used=50,
            finish_reason="stop",
            created_at=None,
            raw_response=None,
        )

        planner = V1Planner(mock_provider, mock_registry)
        result = planner.plan(task_spec)

        assert result.steps[0].retry_count == 1

    def test_playbook_has_budgets(
        self, mock_provider: MagicMock, mock_registry: SkillRegistry, task_spec: TaskSpec
    ) -> None:
        """Generated playbook includes budgets from LLM estimate."""
        budget_json = (
            '{"steps": [{"skill": "mock_skill", "params": {}, '
            '"rationale": "test"}], "estimated_tokens": 5000, "confidence": 0.8}'
        )
        mock_provider.chat.return_value = ChatResponse(
            content=budget_json,
            model="mock-model",
            provider="mock",
            tokens_used=50,
            finish_reason="stop",
            created_at=None,
            raw_response=None,
        )

        planner = V1Planner(mock_provider, mock_registry)
        result = planner.plan(task_spec)

        assert result.budgets.max_tokens == 5000

    def test_playbook_name_is_unique(
        self, mock_provider: MagicMock, mock_registry: SkillRegistry, task_spec: TaskSpec
    ) -> None:
        """Generated playbook has unique name."""
        mock_provider.chat.return_value = ChatResponse(
            content=SIMPLE_PLAN_JSON,
            model="mock-model",
            provider="mock",
            tokens_used=50,
            finish_reason="stop",
            created_at=None,
            raw_response=None,
        )

        planner = V1Planner(mock_provider, mock_registry)
        result1 = planner.plan(task_spec)
        result2 = planner.plan(task_spec)

        assert result1.name != result2.name
        assert result1.name.startswith("v1plan_")
        assert result2.name.startswith("v1plan_")


# ---------------------------------------------------------------------------
# Integration-style Tests (still unit tests, but more realistic)
# ---------------------------------------------------------------------------


class TestV1PlannerIntegration:
    """Integration-style tests with realistic scenarios."""

    def test_research_task_plan(
        self, mock_provider: MagicMock, task_spec: TaskSpec
    ) -> None:
        """Test planning a research-style task."""
        # Set up registry with research skills
        from ag.skills import create_default_registry

        registry = create_default_registry()

        # Mock LLM to return a realistic research plan
        research_plan_json = """{
            "steps": [
                {"skill": "web_search", "params": {"query": "topic"},
                 "rationale": "Find sources"},
                {"skill": "fetch_web_content", "params": {},
                 "rationale": "Get content"},
                {"skill": "synthesize_research", "params": {},
                 "rationale": "Synthesize"},
                {"skill": "emit_result", "params": {"filename": "result.md"},
                 "rationale": "Save output"}
            ],
            "estimated_tokens": 5000,
            "confidence": 0.85,
            "warnings": []
        }"""
        mock_provider.chat.return_value = ChatResponse(
            content=research_plan_json,
            model="gpt-4o-mini",
            provider="openai",
            tokens_used=200,
            finish_reason="stop",
            created_at=None,
            raw_response=None,
        )

        planner = V1Planner(mock_provider, registry)
        result = planner.plan(task_spec)

        # Verify the plan makes sense
        assert len(result.steps) == 4
        skill_sequence = [s.skill_name for s in result.steps]
        expected = ["web_search", "fetch_web_content", "synthesize_research", "emit_result"]
        assert skill_sequence == expected

    def test_prompt_includes_task_and_skills(
        self, mock_provider: MagicMock, mock_registry: SkillRegistry, task_spec: TaskSpec
    ) -> None:
        """Verify the LLM prompt includes task and skill catalog."""
        mock_provider.chat.return_value = ChatResponse(
            content=SIMPLE_PLAN_JSON,
            model="mock-model",
            provider="mock",
            tokens_used=50,
            finish_reason="stop",
            created_at=None,
            raw_response=None,
        )

        planner = V1Planner(mock_provider, mock_registry)
        planner.plan(task_spec)

        # Check the LLM was called with appropriate messages
        call_args = mock_provider.chat.call_args
        messages = call_args.kwargs["messages"]

        # Should have system and user messages
        assert len(messages) == 2
        assert messages[0].role == MessageRole.SYSTEM
        assert messages[1].role == MessageRole.USER

        # User message should include task
        assert task_spec.prompt in messages[1].content
        # User message should include skill names
        assert "mock_skill" in messages[1].content
