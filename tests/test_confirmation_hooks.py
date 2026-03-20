"""Tests for step confirmation hooks (AF-0100).

Tests:
- Skill policy_flags declaration
- StepConfirmation schema
- --yes flag recognition in CLI
- Policy flags exposed via registry
"""

from datetime import datetime, timezone

import pytest
from typer.testing import CliRunner

from ag.cli.main import app
from ag.core import StepConfirmation
from ag.skills import get_default_registry
from ag.skills.base import Skill, SkillContext, SkillInput, SkillOutput

runner = CliRunner()


# ---------------------------------------------------------------------------
# Skill Policy Flags Tests
# ---------------------------------------------------------------------------


class TestSkillPolicyFlags:
    """Tests for skill policy_flags declaration."""

    def test_skill_base_has_policy_flags_attribute(self) -> None:
        """Skill base class defines policy_flags as empty list by default."""
        # Create a minimal skill
        class MinimalOutput(SkillOutput):
            pass

        class MinimalSkill(Skill[SkillInput, MinimalOutput]):
            name = "minimal"
            description = "Minimal skill for testing"
            input_schema = SkillInput
            output_schema = MinimalOutput

            def execute(self, input: SkillInput, ctx: SkillContext) -> MinimalOutput:
                return MinimalOutput(success=True, summary="Done")

        skill = MinimalSkill()
        assert hasattr(skill, "policy_flags")
        assert skill.policy_flags == []

    def test_skill_can_declare_policy_flags(self) -> None:
        """Skills can declare policy_flags as class attribute."""

        class FlaggedOutput(SkillOutput):
            pass

        class FlaggedSkill(Skill[SkillInput, FlaggedOutput]):
            name = "flagged"
            description = "Skill with policy flags"
            input_schema = SkillInput
            output_schema = FlaggedOutput
            policy_flags = ["external_api", "network"]

            def execute(self, input: SkillInput, ctx: SkillContext) -> FlaggedOutput:
                return FlaggedOutput(success=True, summary="Done")

        skill = FlaggedSkill()
        assert skill.policy_flags == ["external_api", "network"]

    def test_web_search_has_external_api_flag(self) -> None:
        """web_search skill declares external_api flag."""
        registry = get_default_registry()
        info = registry.get_info("web_search")
        assert info is not None
        assert "external_api" in info["policy_flags"]
        assert "network" in info["policy_flags"]

    def test_fetch_web_content_has_external_api_flag(self) -> None:
        """fetch_web_content skill declares external_api flag."""
        registry = get_default_registry()
        info = registry.get_info("fetch_web_content")
        assert info is not None
        assert "external_api" in info["policy_flags"]

    def test_summarize_docs_has_llm_call_flag(self) -> None:
        """summarize_docs skill declares llm_call flag."""
        registry = get_default_registry()
        info = registry.get_info("summarize_docs")
        assert info is not None
        assert "llm_call" in info["policy_flags"]

    def test_synthesize_research_has_llm_call_flag(self) -> None:
        """synthesize_research skill declares llm_call flag."""
        registry = get_default_registry()
        info = registry.get_info("synthesize_research")
        assert info is not None
        assert "llm_call" in info["policy_flags"]

    def test_load_documents_has_file_read_flag(self) -> None:
        """load_documents skill declares file_read flag."""
        registry = get_default_registry()
        info = registry.get_info("load_documents")
        assert info is not None
        assert "file_read" in info["policy_flags"]

    def test_emit_result_has_file_write_flag(self) -> None:
        """emit_result skill declares file_write flag."""
        registry = get_default_registry()
        info = registry.get_info("emit_result")
        assert info is not None
        assert "file_write" in info["policy_flags"]


# ---------------------------------------------------------------------------
# StepConfirmation Schema Tests
# ---------------------------------------------------------------------------


class TestStepConfirmationSchema:
    """Tests for StepConfirmation schema."""

    def test_step_confirmation_minimal(self) -> None:
        """StepConfirmation can be created with defaults."""
        confirmation = StepConfirmation()
        assert confirmation.required is False
        assert confirmation.policy_flags == []
        assert confirmation.decision is None
        assert confirmation.decided_at is None
        assert confirmation.decided_by is None

    def test_step_confirmation_full(self) -> None:
        """StepConfirmation with all fields."""
        now = datetime.now(timezone.utc)
        confirmation = StepConfirmation(
            required=True,
            policy_flags=["external_api", "network"],
            decision="approved",
            decided_at=now,
            decided_by="user_interactive",
        )
        assert confirmation.required is True
        assert confirmation.policy_flags == ["external_api", "network"]
        assert confirmation.decision == "approved"
        assert confirmation.decided_at == now
        assert confirmation.decided_by == "user_interactive"

    def test_step_confirmation_serialization(self) -> None:
        """StepConfirmation serializes to JSON correctly."""
        now = datetime.now(timezone.utc)
        confirmation = StepConfirmation(
            required=True,
            policy_flags=["llm_call"],
            decision="approved",
            decided_at=now,
            decided_by="user_yes_flag",
        )
        data = confirmation.model_dump()
        assert data["required"] is True
        assert data["policy_flags"] == ["llm_call"]
        assert data["decision"] == "approved"
        assert data["decided_by"] == "user_yes_flag"


# ---------------------------------------------------------------------------
# CLI --yes Flag Tests
# ---------------------------------------------------------------------------


class TestYesFlagCLI:
    """Tests for --yes flag in ag run."""

    def test_run_help_shows_yes_flag(self) -> None:
        """ag run --help shows --yes/-y option."""
        result = runner.invoke(app, ["run", "--help"])
        assert result.exit_code == 0
        assert "--yes" in result.output
        assert "-y" in result.output
        assert "confirmation" in result.output.lower()

    def test_run_accepts_yes_flag(self) -> None:
        """ag run accepts --yes flag without error."""
        # This will fail for other reasons (no workspace) but should not
        # fail due to --yes being unrecognized
        result = runner.invoke(app, ["run", "--yes", "test prompt"])
        # Should fail with workspace error, not unknown option error
        assert "unrecognized" not in result.output.lower()
        assert "invalid" not in result.output.lower()

    def test_run_accepts_y_shorthand(self) -> None:
        """ag run accepts -y shorthand for --yes."""
        result = runner.invoke(app, ["run", "-y", "test prompt"])
        # Should fail with workspace error, not unknown option error
        assert "unrecognized" not in result.output.lower()
        assert "invalid" not in result.output.lower()


# ---------------------------------------------------------------------------
# Registry Policy Flags Tests
# ---------------------------------------------------------------------------


class TestRegistryPolicyFlags:
    """Tests for policy_flags in skill registry."""

    def test_registry_get_info_includes_policy_flags(self) -> None:
        """get_info returns policy_flags in result."""
        registry = get_default_registry()

        # Check a skill with flags
        info = registry.get_info("web_search")
        assert info is not None
        assert "policy_flags" in info
        assert isinstance(info["policy_flags"], list)

        # Check a skill without flags (emit_result has file_write)
        info = registry.get_info("emit_result")
        assert info is not None
        assert "policy_flags" in info

    def test_registry_preserves_policy_flags_on_registration(self) -> None:
        """Skill policy_flags are preserved when registered."""
        from ag.skills import SkillRegistry
        from ag.skills.base import Skill, SkillContext, SkillInput, SkillOutput

        class TestOutput(SkillOutput):
            pass

        class TestSkill(Skill[SkillInput, TestOutput]):
            name = "test_flags_skill"
            description = "Test skill with flags"
            input_schema = SkillInput
            output_schema = TestOutput
            policy_flags = ["external_api", "sensitive"]

            def execute(self, input: SkillInput, ctx: SkillContext) -> TestOutput:
                return TestOutput(success=True, summary="Test")

        registry = SkillRegistry()
        registry.register(TestSkill())

        skill_info = registry.get_skill("test_flags_skill")
        assert skill_info is not None
        assert skill_info.policy_flags == ["external_api", "sensitive"]

        info_dict = registry.get_info("test_flags_skill")
        assert info_dict is not None
        assert info_dict["policy_flags"] == ["external_api", "sensitive"]
