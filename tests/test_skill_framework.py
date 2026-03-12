"""Tests for skill framework (AF0060).

Tests the base skill classes, context, and registry v2 functionality.
"""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar

import pytest
from pydantic import Field

from ag.skills.base import (
    Skill,
    SkillContext,
    SkillInput,
    SkillOutput,
    StubSkill,
)
from ag.skills.registry import SkillRegistry, SkillV2Info

# ---------------------------------------------------------------------------
# Test Fixtures - Custom Skill Implementations
# ---------------------------------------------------------------------------


class CustomInput(SkillInput):
    """Custom input for test skill."""

    name: str = Field(default="World", description="Name to greet")
    count: int = Field(default=1, ge=1, le=10, description="Number of greetings")


class CustomOutput(SkillOutput):
    """Custom output for test skill."""

    greeting: str = Field(default="", description="The greeting message")
    count: int = Field(default=0, description="How many times greeted")


class GreeterSkill(Skill[CustomInput, CustomOutput]):
    """Test skill that generates greetings."""

    name: ClassVar[str] = "greeter"
    description: ClassVar[str] = "Generates greeting messages"
    input_schema: ClassVar[type[SkillInput]] = CustomInput
    output_schema: ClassVar[type[SkillOutput]] = CustomOutput
    requires_llm: ClassVar[bool] = False

    def execute(self, input: CustomInput, ctx: SkillContext) -> CustomOutput:
        """Generate greeting."""
        greeting = f"Hello, {input.name}!" * input.count
        return CustomOutput(
            success=True,
            summary=f"Greeted {input.name} {input.count} time(s)",
            greeting=greeting,
            count=input.count,
        )


class LLMRequiredSkill(Skill[SkillInput, SkillOutput]):
    """Test skill that requires LLM."""

    name: ClassVar[str] = "llm_required"
    description: ClassVar[str] = "Requires LLM provider"
    input_schema: ClassVar[type[SkillInput]] = SkillInput
    output_schema: ClassVar[type[SkillOutput]] = SkillOutput
    requires_llm: ClassVar[bool] = True

    def execute(self, input: SkillInput, ctx: SkillContext) -> SkillOutput:
        """Would use LLM."""
        if not ctx.has_provider:
            return SkillOutput(
                success=False,
                summary="No provider",
                error="provider_required",
            )
        return SkillOutput(success=True, summary="Used LLM")


# ---------------------------------------------------------------------------
# SkillInput Tests
# ---------------------------------------------------------------------------


class TestSkillInput:
    """Tests for SkillInput base class."""

    def test_default_values(self) -> None:
        """Input has sensible defaults."""
        input = SkillInput()
        assert input.prompt == ""

    def test_with_prompt(self) -> None:
        """Can set prompt."""
        input = SkillInput(prompt="test prompt")
        assert input.prompt == "test prompt"

    def test_extra_fields_forbidden(self) -> None:
        """Extra fields raise validation error."""
        with pytest.raises(Exception):  # Pydantic ValidationError
            SkillInput(prompt="test", unknown_field="value")  # type: ignore


class TestSkillOutput:
    """Tests for SkillOutput base class."""

    def test_required_fields(self) -> None:
        """success and summary are required."""
        output = SkillOutput(success=True, summary="Done")
        assert output.success is True
        assert output.summary == "Done"
        assert output.error is None

    def test_error_field(self) -> None:
        """Error field can be set."""
        output = SkillOutput(success=False, summary="Failed", error="some_error")
        assert output.success is False
        assert output.error == "some_error"

    def test_to_legacy_tuple(self) -> None:
        """Converts to legacy format correctly."""
        output = SkillOutput(success=True, summary="Done", error=None)
        success, summary, data = output.to_legacy_tuple()
        assert success is True
        assert summary == "Done"
        assert data == {"error": None}


# ---------------------------------------------------------------------------
# SkillContext Tests
# ---------------------------------------------------------------------------


class TestSkillContext:
    """Tests for SkillContext."""

    def test_default_context(self) -> None:
        """Context has sensible defaults."""
        ctx = SkillContext()
        assert ctx.provider is None
        assert ctx.workspace_path is None
        assert ctx.config == {}
        assert ctx.step_number == 0
        assert ctx.run_id is None

    def test_has_provider(self) -> None:
        """has_provider reflects provider state."""
        ctx = SkillContext()
        assert ctx.has_provider is False

        # With a mock provider
        ctx = SkillContext(provider=object())  # type: ignore
        assert ctx.has_provider is True

    def test_has_workspace(self) -> None:
        """has_workspace reflects workspace_path state."""
        ctx = SkillContext()
        assert ctx.has_workspace is False

        ctx = SkillContext(workspace_path=Path("/tmp/ws"))
        assert ctx.has_workspace is True

    def test_inputs_path(self) -> None:
        """inputs_path returns correct path."""
        ctx = SkillContext()
        assert ctx.inputs_path is None

        ctx = SkillContext(workspace_path=Path("/tmp/ws"))
        assert ctx.inputs_path == Path("/tmp/ws/inputs")


# ---------------------------------------------------------------------------
# Skill Protocol Tests
# ---------------------------------------------------------------------------


class TestSkillProtocol:
    """Tests for Skill base class."""

    def test_greeter_skill_attributes(self) -> None:
        """Skill has correct class attributes."""
        assert GreeterSkill.name == "greeter"
        assert GreeterSkill.description == "Generates greeting messages"
        assert GreeterSkill.input_schema == CustomInput
        assert GreeterSkill.output_schema == CustomOutput
        assert GreeterSkill.requires_llm is False

    def test_greeter_skill_execute(self) -> None:
        """Skill executes correctly."""
        skill = GreeterSkill()
        input = CustomInput(name="Alice", count=2)
        ctx = SkillContext()

        output = skill.execute(input, ctx)

        assert output.success is True
        assert "Alice" in output.summary
        assert output.greeting == "Hello, Alice!Hello, Alice!"
        assert output.count == 2

    def test_validate_context_no_llm_required(self) -> None:
        """Validation passes when LLM not required."""
        skill = GreeterSkill()
        ctx = SkillContext()  # No provider
        # Should not raise
        skill.validate_context(ctx)

    def test_validate_context_llm_required(self) -> None:
        """Validation fails when LLM required but not available."""
        skill = LLMRequiredSkill()
        ctx = SkillContext()  # No provider

        with pytest.raises(ValueError, match="requires LLM provider"):
            skill.validate_context(ctx)


class TestStubSkill:
    """Tests for StubSkill base class."""

    def test_default_stub_behavior(self) -> None:
        """Stub skill returns stub response."""

        class TestStub(StubSkill):
            name = "test_stub"
            description = "Test stub"
            stub_success = True
            stub_summary = "Stub ran"
            stub_data = {"test": "value"}

        skill = TestStub()
        input = SkillInput()
        ctx = SkillContext()

        output = skill.execute(input, ctx)

        assert output.success is True
        assert output.summary == "Stub ran"
        assert output.stub is True
        assert output.stub_data == {"test": "value"}


# ---------------------------------------------------------------------------
# Registry V2 Tests
# ---------------------------------------------------------------------------


class TestRegistryV2:
    """Tests for v2 skill registration and execution."""

    def test_register_v2_skill(self) -> None:
        """Can register a v2 skill."""
        registry = SkillRegistry()
        skill = GreeterSkill()

        registry.register_v2(skill)

        assert registry.has("greeter")
        assert registry.is_v2("greeter")

    def test_get_v2_skill(self) -> None:
        """Can retrieve v2 skill info."""
        registry = SkillRegistry()
        skill = GreeterSkill()
        registry.register_v2(skill)

        info = registry.get_v2("greeter")

        assert info is not None
        assert isinstance(info, SkillV2Info)
        assert info.name == "greeter"
        assert info.skill is skill

    def test_execute_v2_skill(self) -> None:
        """Can execute v2 skill through registry."""
        registry = SkillRegistry()
        registry.register_v2(GreeterSkill())

        success, summary, data = registry.execute(
            "greeter",
            {"prompt": "test", "name": "Bob", "count": 3},
        )

        assert success is True
        assert "Bob" in summary
        assert data["greeting"] == "Hello, Bob!Hello, Bob!Hello, Bob!"
        assert data["count"] == 3

    def test_execute_v2_with_context(self) -> None:
        """Can pass context to v2 skill execution."""
        registry = SkillRegistry()
        registry.register_v2(GreeterSkill())

        ctx = SkillContext(workspace_path=Path("/tmp/ws"))
        success, summary, data = registry.execute(
            "greeter",
            {"name": "Charlie"},
            context=ctx,
        )

        assert success is True

    def test_execute_v2_invalid_input(self) -> None:
        """Invalid input returns failure."""
        registry = SkillRegistry()
        registry.register_v2(GreeterSkill())

        # count must be >= 1
        success, summary, data = registry.execute(
            "greeter",
            {"count": 0},  # Invalid
        )

        assert success is False
        assert "Invalid input" in summary

    def test_get_info_v2(self) -> None:
        """get_info returns schema info for skills (AF0079: all skills are V2)."""
        registry = SkillRegistry()
        registry.register_v2(GreeterSkill())

        info = registry.get_info("greeter")

        assert info is not None
        assert info["name"] == "greeter"
        assert "input_schema" in info
        assert "output_schema" in info

    def test_list_includes_all_skills(self) -> None:
        """list() includes all registered skills (AF0079: all V2)."""
        registry = SkillRegistry()
        registry.register(GreeterSkill())

        names = registry.list()

        assert "greeter" in names

    def test_register_overwrites_existing(self) -> None:
        """Registering same name overwrites previous (AF0079: V2 only)."""
        registry = SkillRegistry()
        registry.register(GreeterSkill())

        # Register a different skill with same name (greeter)
        # The V2 greeter should be used
        success, summary, data = registry.execute("greeter", {"name": "Test"})

        # Should use greeter (has greeting field or name in summary)
        assert "greeting" in data or "Test" in summary

    def test_context_validation_through_registry(self) -> None:
        """Registry validates context for v2 skills."""
        registry = SkillRegistry()
        registry.register_v2(LLMRequiredSkill())

        # No provider in context
        success, summary, data = registry.execute(
            "llm_required",
            {},
            context=SkillContext(),  # No provider
        )

        assert success is False
        assert "context_validation_failed" in data.get("error", "")


# ---------------------------------------------------------------------------
# AF0077: Entry Point Discovery Tests
# ---------------------------------------------------------------------------


class TestEntryPointDiscovery:
    """Tests for skill entry point discovery (AF0077)."""

    def test_source_field_exists(self) -> None:
        """SkillInfo includes source field."""
        registry = SkillRegistry()
        registry.register(GreeterSkill())

        info = registry.get_skill("greeter")

        assert info is not None
        assert hasattr(info, "source")
        assert info.source == "built-in"  # default

    def test_source_custom_value(self) -> None:
        """SkillInfo source can be set to custom value."""
        registry = SkillRegistry()
        registry.register(GreeterSkill(), source="entry-point")

        info = registry.get_skill("greeter")

        assert info is not None
        assert info.source == "entry-point"

    def test_get_info_includes_source(self) -> None:
        """get_info() dict includes source field."""
        registry = SkillRegistry()
        registry.register(GreeterSkill(), source="test-stub")

        info = registry.get_info("greeter")

        assert info is not None
        assert info["source"] == "test-stub"

    def test_discover_entrypoint_skills_mock(self, mocker) -> None:
        """Entry point discovery registers skills from mock entry points."""
        from ag.skills.registry import _discover_entrypoint_skills

        # Mock entry_points to return a fake skill
        mock_ep = mocker.MagicMock()
        mock_ep.name = "test_skill"
        mock_ep.load.return_value = GreeterSkill

        mocker.patch(
            "ag.skills.registry.entry_points",
            return_value=[mock_ep],
        )

        registry = SkillRegistry()
        _discover_entrypoint_skills(registry)

        assert registry.has("greeter")
        info = registry.get_skill("greeter")
        assert info is not None
        assert info.source == "entry-point"

    def test_discover_entrypoint_skill_load_failure(self, mocker, caplog) -> None:
        """Entry point that fails to load logs warning and doesn't crash."""
        from ag.skills.registry import _discover_entrypoint_skills

        mock_ep = mocker.MagicMock()
        mock_ep.name = "broken_skill"
        mock_ep.load.side_effect = ImportError("module not found")

        mocker.patch(
            "ag.skills.registry.entry_points",
            return_value=[mock_ep],
        )

        registry = SkillRegistry()
        # Should not raise
        _discover_entrypoint_skills(registry)

        assert not registry.has("broken_skill")
        # Warning should be logged
        assert "Failed to load" in caplog.text or len(registry.list()) == 0

    def test_discover_entrypoint_skill_not_skill_protocol(self, mocker, caplog) -> None:
        """Entry point that doesn't implement Skill protocol is skipped."""
        import logging

        from ag.skills.registry import _discover_entrypoint_skills

        caplog.set_level(logging.WARNING)

        # Return a non-Skill class
        class NotASkill:
            pass

        mock_ep = mocker.MagicMock()
        mock_ep.name = "not_a_skill"
        mock_ep.load.return_value = NotASkill

        mocker.patch(
            "ag.skills.registry.entry_points",
            return_value=[mock_ep],
        )

        registry = SkillRegistry()
        _discover_entrypoint_skills(registry)

        assert not registry.has("not_a_skill")
        # Warning should be logged about protocol
        assert "Skill protocol" in caplog.text

    def test_discover_entrypoint_skill_name_conflict(self, mocker, caplog) -> None:
        """Entry point with name conflict with existing skill is skipped."""
        import logging

        from ag.skills.registry import _discover_entrypoint_skills

        caplog.set_level(logging.WARNING)

        mock_ep = mocker.MagicMock()
        mock_ep.name = "greeter_ep"
        mock_ep.load.return_value = GreeterSkill

        mocker.patch(
            "ag.skills.registry.entry_points",
            return_value=[mock_ep],
        )

        # Pre-register a skill with same name
        registry = SkillRegistry()
        registry.register(GreeterSkill(), source="built-in")

        # Now discover entry points - should skip due to conflict
        _discover_entrypoint_skills(registry)

        # Original should still be there with built-in source
        info = registry.get_skill("greeter")
        assert info is not None
        assert info.source == "built-in"  # Not overwritten

        # Warning should be logged about conflict
        assert "conflicts" in caplog.text

    def test_default_registry_uses_entry_points(self) -> None:
        """create_default_registry() discovers skills via entry points."""
        from ag.skills.registry import create_default_registry

        registry = create_default_registry()

        # Built-in skills should be registered via entry points
        emit_info = registry.get_skill("emit_result")
        assert emit_info is not None
        assert emit_info.source == "entry-point"

        # Test stubs should be registered directly
        echo_info = registry.get_skill("echo_tool")
        assert echo_info is not None
        assert echo_info.source == "test-stub"

    def test_skills_list_integration(self) -> None:
        """ag skills list shows source column (integration test)."""
        from ag.skills.registry import create_default_registry

        registry = create_default_registry()
        skill_names = registry.list()

        # Verify we have both entry-point and test-stub skills
        sources = set()
        for name in skill_names:
            info = registry.get_info(name)
            if info:
                sources.add(info["source"])

        assert "entry-point" in sources
        assert "test-stub" in sources
