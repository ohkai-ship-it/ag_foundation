"""Skill registry for AG Foundation runtime (AF0060, AF0065, AF0067, AF0079).

This module provides the SkillRegistry class that manages typed skills.
The registry is the central coordination point for skill discovery,
registration, and execution.

Schemas Defined (see docs/dev/additional/SCHEMA_INVENTORY.md):
    SkillInfo — Metadata for registered skills (name, description, skill, schemas)

Skills use the Pydantic-based Skill[InputT, OutputT] ABC pattern:
    - Subclass of Skill ABC with typed input/output schemas
    - Pydantic schemas for input/output validation
    - Type hints, IDE support, better error messages
    - Used by: load_documents, summarize_docs, emit_result

How to Register Skills:
    registry.register(MySkill())

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

See Also:
    - base.py: Skill ABC and schema definitions
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ag.skills.base import Skill, SkillContext, SkillInput, SkillOutput
from ag.skills.emit_result import EmitResultSkill
from ag.skills.load_documents import LoadDocumentsSkill
from ag.skills.stubs import EchoSkill, ErrorSkill, FailSkill
from ag.skills.summarize_docs import SummarizeDocsSkill


@dataclass
class SkillInfo:
    """Metadata about a registered skill (AF0079 simplified).

    Skills use the Skill protocol with typed Pydantic schemas.
    """

    name: str
    description: str
    skill: Skill[Any, Any]
    input_schema: type[SkillInput]
    output_schema: type[SkillOutput]
    requires_llm: bool = False


# Backward compatibility alias (AF0079)
SkillV2Info = SkillInfo


class SkillRegistry:
    """Registry of available skills (AF0079 simplified).

    All skills use the Pydantic-based Skill protocol.
    V1 legacy support has been removed.

    v0: Skills are registered at startup. No dynamic loading.
    """

    def __init__(self) -> None:
        self._skills: dict[str, SkillInfo] = {}

    def register(self, skill: Skill[Any, Any]) -> None:
        """Register a skill.

        Args:
            skill: Skill instance implementing the Skill protocol
        """
        self._skills[skill.name] = SkillInfo(
            name=skill.name,
            description=skill.description,
            skill=skill,
            input_schema=skill.input_schema,
            output_schema=skill.output_schema,
            requires_llm=skill.requires_llm,
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

        Returns dict with: name, description, requires_llm,
        input_schema, output_schema
        """
        if name not in self._skills:
            return None

        info = self._skills[name]
        return {
            "name": info.name,
            "description": info.description,
            "requires_llm": info.requires_llm,
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


def create_default_registry() -> SkillRegistry:
    """Create a registry with default production skills.

    Skills registered:
    - Production: load_documents, summarize_docs, emit_result
    - Test stubs: echo_tool, fail_skill

    Returns:
        SkillRegistry with production skills registered
    """
    registry = SkillRegistry()

    # Production skills (AF-0065: summarize playbook)
    registry.register(LoadDocumentsSkill())
    registry.register(SummarizeDocsSkill())
    registry.register(EmitResultSkill())

    # Test stub skills (AF-0079: V2 stubs for testing)
    registry.register(EchoSkill())
    registry.register(FailSkill())
    registry.register(ErrorSkill())

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
