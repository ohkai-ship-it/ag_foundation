"""Skill framework base classes and protocols (AF0060, AF0067).

This module defines the core skill contract for AG Foundation:
- SkillInput/SkillOutput: Pydantic base models for typed I/O
- SkillContext: Runtime context injected into skills (provider, workspace, config)
- Skill: ABC defining what a skill must implement

Schemas Defined (see docs/dev/additional/SCHEMA_INVENTORY.md):
    SkillInput      — Base input schema (prompt field)
    SkillOutput     — Base output schema (success, summary, error fields)
    StubSkillOutput — Extension for stub responses (stub=True, stub_data)
    SkillContext    — Runtime context (dataclass, not Pydantic)

Contracts Implemented (see docs/dev/additional/CONTRACT_INVENTORY.md):
    Skill[InputT, OutputT] — ABC for typed skills with execute() method

Design Decisions:
    - Skills are stateless callables with typed schemas
    - Context injection provides LLM access without global state
    - Pydantic enforces input/output validation
    - Both legacy (dict->tuple) and new (Skill protocol) signatures supported

Bounded Autonomy (Phase 1 - Playbook-driven):
    - Humans define WHAT (skills exist, playbook structure, budgets)
    - Agents decide HOW (skill parameters, output content within schema)


How to Create a New Skill
=========================

Step 1: Define Input Schema
---------------------------
Subclass SkillInput with your skill's parameters:

    class MyInput(SkillInput):
        topic: str = Field(default="general", description="Topic to process")
        max_items: int = Field(default=10, ge=1, description="Max items to return")

Step 2: Define Output Schema
----------------------------
Subclass SkillOutput with your skill's results:

    class MyOutput(SkillOutput):
        items: list[str] = Field(default_factory=list, description="Processed items")
        count: int = Field(default=0, description="Number of items found")

Step 3: Create Skill Class
--------------------------
Subclass Skill with your input/output types:

    class MySkill(Skill[MyInput, MyOutput]):
        name = "my_skill"
        description = "Processes topics and returns items"
        input_schema = MyInput
        output_schema = MyOutput
        requires_llm = True  # Set to True if skill needs LLM

        def execute(self, input: MyInput, ctx: SkillContext) -> MyOutput:
            # Validate context if needed
            self.validate_context(ctx)

            # Use ctx.provider for LLM calls
            if ctx.provider:
                response = ctx.provider.chat([...])

            # Use ctx.workspace_path for file access
            if ctx.workspace_path:
                files = list(ctx.workspace_path.glob("*.md"))

            return MyOutput(
                success=True,
                summary=f"Found {len(items)} items",
                items=items,
                count=len(items),
            )

Step 4: Register the Skill
--------------------------
In registry.py or your module's __init__.py:

    from ag.skills import get_default_registry
    registry = get_default_registry()
    registry.register(MySkill())

The skill is now available via `ag run --skill my_skill "prompt"`.

See Also:
    - load_documents.py, summarize_docs.py, emit_result.py: v2 skill examples
    - registry.py: Skill registration mechanics
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
        trace_metadata: Optional dict with run trace info (AF-0082)
            Keys may include: elapsed_ms, model, playbook_name, playbook_version,
            steps_summary (list of {skill, duration_ms, output_summary} dicts)
    """

    provider: LLMProvider | None = None
    workspace_path: Path | None = None
    config: dict[str, Any] = field(default_factory=dict)
    step_number: int = 0
    run_id: str | None = None
    trace_metadata: dict[str, Any] = field(default_factory=dict)

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
