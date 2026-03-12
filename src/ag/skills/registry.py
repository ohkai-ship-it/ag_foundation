"""Skill registry for AG Foundation runtime (AF0060, AF0065, AF0067, AF0074, AF0079, AF0077).

This module provides the SkillRegistry class that manages typed skills.
The registry is the central coordination point for skill discovery,
registration, and execution.

Schemas Defined (see docs/dev/additional/SCHEMA_INVENTORY.md):
    SkillInfo — Metadata for registered skills (name, description, skill, schemas, source)

Skills use the Pydantic-based Skill[InputT, OutputT] ABC pattern:
    - Subclass of Skill ABC with typed input/output schemas
    - Pydantic schemas for input/output validation
    - Type hints, IDE support, better error messages
    - Used by: load_documents, summarize_docs, emit_result, fetch_web_content, etc.

Plugin Architecture (AF0077):
    External packages can register skills via Python entry points:

    # pyproject.toml
    [project.entry-points."ag.skills"]
    my_skill = "my_package.skills:MySkill"

    After `pip install`, `ag skills list` shows the skill automatically.

How to Register Skills:
    registry.register(MySkill())
    registry.register(MySkill(), source="entry-point")

How to Execute Skills:
    # Using registry.execute
    success, summary, data = registry.execute("my_skill", params, context)

    # Direct execution
    skill_info = registry.get_skill("my_skill")
    output = skill_info.skill.execute(input_obj, context)

Built-in Skills:
    - load_documents: Loads documents from workspace inputs folder
    - summarize_docs: LLM-powered document summarization
    - emit_result: Emits final results to run trace
    - fetch_web_content: Fetches content from URLs (AF0074)
    - synthesize_research: LLM-powered research synthesis (AF0074)

See Also:
    - base.py: Skill ABC and schema definitions
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from importlib.metadata import entry_points
from typing import Any

from ag.skills.base import Skill, SkillContext, SkillInput, SkillOutput

logger = logging.getLogger(__name__)

# Entry point group name for skill plugins
SKILL_ENTRY_POINT_GROUP = "ag.skills"


@dataclass
class SkillInfo:
    """Metadata about a registered skill (AF0079 simplified, AF0077 source tracking).

    Skills use the Skill protocol with typed Pydantic schemas.

    Attributes:
        source: Origin of the skill - "built-in", "entry-point", or "test-stub"
    """

    name: str
    description: str
    skill: Skill[Any, Any]
    input_schema: type[SkillInput]
    output_schema: type[SkillOutput]
    requires_llm: bool = False
    source: str = "built-in"


# Backward compatibility alias (AF0079)
SkillV2Info = SkillInfo


class SkillRegistry:
    """Registry of available skills (AF0079 simplified, AF0077 plugin support).

    All skills use the Pydantic-based Skill protocol.
    V1 legacy support has been removed.

    Skills can be registered:
    - Directly via register() method (built-in or test stubs)
    - Via Python entry points (external packages)

    v0: Skills are registered at startup. No dynamic loading.
    """

    def __init__(self) -> None:
        self._skills: dict[str, SkillInfo] = {}

    def register(self, skill: Skill[Any, Any], *, source: str = "built-in") -> None:
        """Register a skill.

        Args:
            skill: Skill instance implementing the Skill protocol
            source: Origin of the skill - "built-in", "entry-point", or "test-stub"
        """
        self._skills[skill.name] = SkillInfo(
            name=skill.name,
            description=skill.description,
            skill=skill,
            input_schema=skill.input_schema,
            output_schema=skill.output_schema,
            requires_llm=skill.requires_llm,
            source=source,
        )

    def get_skill(self, name: str) -> SkillInfo | None:
        """Get a skill by name."""
        return self._skills.get(name)

    def execute(
        self,
        name: str,
        parameters: dict[str, Any],
        context: SkillContext | None = None,
    ) -> tuple[bool, str, dict[str, Any]]:
        """Execute a skill by name.

        Args:
            name: Skill name
            parameters: Skill parameters
            context: Optional SkillContext

        Returns:
            Tuple of (success, output_summary, result_data)

        Raises:
            KeyError: If skill not found
        """
        skill_info = self._skills.get(name)
        if skill_info is None:
            raise KeyError(f"Skill not found: {name}")

        skill = skill_info.skill

        # Build context if not provided
        ctx = context or SkillContext()

        # Validate context requirements
        try:
            skill.validate_context(ctx)
        except ValueError as e:
            return False, str(e), {"error": "context_validation_failed"}

        # Parse input from parameters
        # Filter to only include fields defined in the schema (ignore extras like 'step')
        # This is required for skills with extra="forbid" in their input schema.
        # Skills that need aliased inputs should define those aliases as schema fields.
        try:
            schema_fields = set(skill_info.input_schema.model_fields.keys())
            filtered_params = {k: v for k, v in parameters.items() if k in schema_fields}
            input_data = skill_info.input_schema.model_validate(filtered_params)
        except Exception as e:
            return False, f"Invalid input: {e}", {"error": "input_validation_failed"}

        # Execute skill
        try:
            output = skill.execute(input_data, ctx)
            return output.to_legacy_tuple()
        except Exception as e:
            return False, f"Skill execution failed: {e}", {"error": str(e)}

    def list_skills(self) -> list[str]:
        """List all registered skill names."""
        return sorted(self._skills.keys())

    def list(self) -> list[str]:
        """List all registered skill names (alias for list_skills)."""
        return self.list_skills()

    def has(self, name: str) -> bool:
        """Check if a skill is registered."""
        return name in self._skills

    def get_info(self, name: str) -> dict[str, Any] | None:
        """Get skill info dict.

        Returns dict with: name, description, requires_llm, source,
        input_schema, output_schema
        """
        if name not in self._skills:
            return None

        info = self._skills[name]
        return {
            "name": info.name,
            "description": info.description,
            "requires_llm": info.requires_llm,
            "source": info.source,
            "input_schema": info.input_schema.model_json_schema(),
            "output_schema": info.output_schema.model_json_schema(),
        }

    # -------------------------------------------------------------------------
    # Backward Compatibility Aliases (AF0079)
    # -------------------------------------------------------------------------
    # These methods provide API compatibility during the V1 → V2 transition.
    # They will be removed in a future version.

    def register_v2(self, skill: Skill[Any, Any]) -> None:
        """Register a skill (alias for register, for backward compatibility)."""
        self.register(skill)

    def get_v2(self, name: str) -> SkillInfo | None:
        """Get a skill by name (alias for get_skill, for backward compatibility)."""
        return self.get_skill(name)

    def get(self, name: str) -> SkillInfo | None:
        """Get a skill by name (alias for get_skill, for backward compatibility)."""
        return self.get_skill(name)

    def is_v2(self, name: str) -> bool:
        """Check if skill is V2 (always True now, for backward compatibility)."""
        return name in self._skills


# ---------------------------------------------------------------------------
# Default Registry
# ---------------------------------------------------------------------------


def _discover_entrypoint_skills(registry: SkillRegistry) -> None:
    """Discover and register skills from installed Python entry points (AF0077).

    Entry points allow external packages to register skills via pyproject.toml:

        [project.entry-points."ag.skills"]
        my_skill = "my_package.skills:MySkill"

    After `pip install`, the skill is automatically discovered and registered.

    Args:
        registry: SkillRegistry to register discovered skills into

    Notes:
        - Invalid entry points are logged and skipped (never crash)
        - Name conflicts with existing skills are rejected with warning
        - Entry points that don't implement Skill protocol are skipped
    """
    eps = entry_points(group=SKILL_ENTRY_POINT_GROUP)

    for ep in eps:
        try:
            skill_class = ep.load()
            skill = skill_class()

            # Validate it implements the Skill protocol
            if not isinstance(skill, Skill):
                logger.warning(
                    "Entry point %r does not implement Skill protocol, skipping",
                    ep.name,
                )
                continue

            # Don't overwrite existing skills (e.g., test stubs registered first)
            if registry.has(skill.name):
                logger.warning(
                    "Entry point skill %r conflicts with existing skill, skipping",
                    skill.name,
                )
                continue

            registry.register(skill, source="entry-point")
            logger.debug("Registered entry-point skill: %s", skill.name)

        except Exception:
            logger.warning(
                "Failed to load skill entry point %r",
                ep.name,
                exc_info=True,
            )


def create_default_registry() -> SkillRegistry:
    """Create a registry with default production skills (AF0077 plugin architecture).

    Skills are discovered and registered from two sources:

    1. **Entry points** (production + external skills):
       - Built-in skills are registered via pyproject.toml entry points
       - External packages can add skills the same way
       - Source: "entry-point"

    2. **Direct registration** (test stubs only):
       - Test stubs are registered directly, not via entry points
       - This prevents them from appearing in production skill lists
       - Source: "test-stub"

    Returns:
        SkillRegistry with production and test-stub skills registered
    """
    registry = SkillRegistry()

    # 1. Discover and register entry-point skills (production + external)
    _discover_entrypoint_skills(registry)

    # 2. Register test stub skills directly (not via entry points)
    # Import here to avoid circular imports and keep stubs out of entry points
    from ag.skills.stubs import EchoSkill, ErrorSkill, FailSkill

    registry.register(EchoSkill(), source="test-stub")
    registry.register(FailSkill(), source="test-stub")
    registry.register(ErrorSkill(), source="test-stub")

    return registry


# Global default registry instance
_default_registry: SkillRegistry | None = None


def get_default_registry() -> SkillRegistry:
    """Get the default skill registry (lazy-initialized singleton)."""
    global _default_registry
    if _default_registry is None:
        _default_registry = create_default_registry()
    return _default_registry


def reset_default_registry() -> None:
    """Reset the default registry (for testing)."""
    global _default_registry
    _default_registry = None
