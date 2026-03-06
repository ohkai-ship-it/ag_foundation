"""Skill framework base classes and protocols (AF0060).

This module defines the core skill contract for AG Foundation:
- SkillInput/SkillOutput: Pydantic base models for typed I/O
- SkillContext: Runtime context injected into skills (provider, workspace, config)
- Skill: Protocol defining what a skill must implement

Design Decisions:
- Skills are stateless callables with typed schemas
- Context injection provides LLM access without global state
- Pydantic enforces input/output validation
- Both legacy (dict->tuple) and new (Skill protocol) signatures supported

Bounded Autonomy (Phase 1 - Playbook-driven):
- Humans define WHAT (skills exist, playbook structure, budgets)
- Agents decide HOW (skill parameters, output content within schema)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Generic, TypeVar

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from ag.providers.base import LLMProvider

# ---------------------------------------------------------------------------
# Type Variables for Generic Skill Classes
# ---------------------------------------------------------------------------

InputT = TypeVar("InputT", bound="SkillInput")
OutputT = TypeVar("OutputT", bound="SkillOutput")


# ---------------------------------------------------------------------------
# Base Input/Output Schemas
# ---------------------------------------------------------------------------


class SkillInput(BaseModel):
    """Base class for skill inputs.

    All skill input schemas should inherit from this class.
    Common parameters are defined here; skill-specific params are added in subclasses.
    """

    prompt: str = Field(default="", description="User prompt or task description")

    model_config = {"extra": "forbid"}


class SkillOutput(BaseModel):
    """Base class for skill outputs.

    All skill output schemas should inherit from this class.
    Required fields (success, summary) must be provided; skill-specific data in subclasses.
    """

    success: bool = Field(..., description="Whether the skill execution succeeded")
    summary: str = Field(..., description="Human-readable summary of the result")
    error: str | None = Field(default=None, description="Error message if failed")

    model_config = {"extra": "forbid"}

    def to_legacy_tuple(self) -> tuple[bool, str, dict[str, Any]]:
        """Convert to legacy skill return format for backward compatibility."""
        return (
            self.success,
            self.summary,
            self.model_dump(exclude={"success", "summary"}),
        )


# ---------------------------------------------------------------------------
# Skill Context
# ---------------------------------------------------------------------------


@dataclass
class SkillContext:
    """Runtime context provided to skills during execution.

    This encapsulates all external dependencies a skill might need,
    enabling clean separation between skill logic and runtime concerns.

    Attributes:
        provider: LLM provider for making AI calls (may be None for non-LLM skills)
        workspace_path: Path to workspace directory (None if no workspace)
        config: Additional configuration dict
        step_number: Current step number in playbook execution
        run_id: Current run ID for artifact registration
    """

    provider: LLMProvider | None = None
    workspace_path: Path | None = None
    config: dict[str, Any] = field(default_factory=dict)
    step_number: int = 0
    run_id: str | None = None

    @property
    def has_provider(self) -> bool:
        """Check if an LLM provider is available."""
        return self.provider is not None

    @property
    def has_workspace(self) -> bool:
        """Check if a workspace path is available."""
        return self.workspace_path is not None

    @property
    def inputs_path(self) -> Path | None:
        """Get the inputs directory path (AF0058 structure)."""
        if self.workspace_path is None:
            return None
        return self.workspace_path / "inputs"


# ---------------------------------------------------------------------------
# Skill Protocol and Base Class
# ---------------------------------------------------------------------------


class Skill(ABC, Generic[InputT, OutputT]):
    """Abstract base class for skills.

    Skills are reusable, typed capabilities that can optionally use LLM.
    Each skill defines its input/output schemas via class attributes.

    Example:
        class MySkill(Skill[MyInput, MyOutput]):
            name = "my_skill"
            description = "Does something useful"
            input_schema = MyInput
            output_schema = MyOutput

            def execute(self, input: MyInput, ctx: SkillContext) -> MyOutput:
                # ... implementation ...
                return MyOutput(success=True, summary="Done")
    """

    # Class attributes to be overridden by subclasses
    name: ClassVar[str]
    description: ClassVar[str]
    input_schema: ClassVar[type[SkillInput]]
    output_schema: ClassVar[type[SkillOutput]]

    # Optional: whether this skill requires LLM access
    requires_llm: ClassVar[bool] = False

    @abstractmethod
    def execute(self, input: InputT, ctx: SkillContext) -> OutputT:
        """Execute the skill with given input and context.

        Args:
            input: Validated input matching input_schema
            ctx: Runtime context with provider, workspace, etc.

        Returns:
            Output matching output_schema
        """
        ...

    def validate_context(self, ctx: SkillContext) -> None:
        """Validate that context has required resources.

        Raises:
            ValueError: If required resources are missing
        """
        if self.requires_llm and not ctx.has_provider:
            raise ValueError(f"Skill '{self.name}' requires LLM provider but none available")


# ---------------------------------------------------------------------------
# Stub Skill Base (for testing/placeholder skills)
# ---------------------------------------------------------------------------


class StubSkillOutput(SkillOutput):
    """Output for stub skills."""

    stub: bool = Field(default=True, description="Indicates this is a stub response")
    stub_data: dict[str, Any] = Field(default_factory=dict, description="Stub-specific data")


class StubSkill(Skill[SkillInput, StubSkillOutput]):
    """Base class for stub skills (testing/placeholders).

    Stub skills return predefined responses without real processing.
    They are useful for testing playbook execution and development.
    """

    input_schema: ClassVar[type[SkillInput]] = SkillInput
    output_schema: ClassVar[type[StubSkillOutput]] = StubSkillOutput
    requires_llm: ClassVar[bool] = False

    # Stub response configuration
    stub_success: ClassVar[bool] = True
    stub_summary: ClassVar[str] = "Stub executed"
    stub_data: ClassVar[dict[str, Any]] = {}

    def execute(self, input: SkillInput, ctx: SkillContext) -> StubSkillOutput:
        """Execute stub skill with predefined response."""
        return StubSkillOutput(
            success=self.stub_success,
            summary=self.stub_summary,
            stub=True,
            stub_data=dict(self.stub_data),
        )
