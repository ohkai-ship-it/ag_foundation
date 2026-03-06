"""Skills and plugin registry.

AF0060: Added base skill framework with typed schemas.
"""

from .base import (
    Skill,
    SkillContext,
    SkillInput,
    SkillOutput,
    StubSkill,
    StubSkillOutput,
)
from .registry import (
    SkillFn,
    SkillInfo,
    SkillRegistry,
    SkillV2Info,
    create_default_registry,
    get_default_registry,
)

__all__ = [
    # Base framework (AF0060)
    "Skill",
    "SkillContext",
    "SkillInput",
    "SkillOutput",
    "StubSkill",
    "StubSkillOutput",
    # Registry
    "SkillFn",
    "SkillInfo",
    "SkillRegistry",
    "SkillV2Info",
    "create_default_registry",
    "get_default_registry",
]
