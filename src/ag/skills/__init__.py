"""Skills package — typed capabilities for AG Foundation (AF0060, AF0065, AF0067, AF0079).

This package provides the skill framework for building agent capabilities.
Skills are typed, stateless callables that produce structured outputs.

Documentation References:
    - SCHEMA_INVENTORY.md: Documents all Pydantic schemas (SkillInput, SkillOutput, etc.)
    - CONTRACT_INVENTORY.md: Documents the Skill protocol/ABC
    - SKILLS_ARCHITECTURE_0.1.md: High-level architecture and design rationale

Package Structure:
    base.py         — Core classes: Skill ABC, SkillInput, SkillOutput, SkillContext
    registry.py     — SkillRegistry for typed skill management (V1 removed in AF0079)
    stubs.py        — Test stub skills (echo_tool, fail_skill)
    load_documents.py  — Production skill: loads documents from workspace
    synthesize_research.py — Production skill: LLM-powered document synthesis (AF-0108: canonical)
    emit_result.py     — Production skill: emits final results to trace

Quick Start (Creating a New Skill):
    1. Define input schema: subclass SkillInput
    2. Define output schema: subclass SkillOutput
    3. Create skill class: subclass Skill[YourInput, YourOutput]
    4. Implement execute(input, ctx) -> output
    5. Register with: registry.register(YourSkill())

    See base.py docstring for complete example.
"""

from .base import (
    Skill,
    SkillContext,
    SkillInput,
    SkillOutput,
    StubSkill,
    StubSkillOutput,
)
from .emit_result import (
    EmitResultInput,
    EmitResultOutput,
    EmitResultSkill,
)
from .load_documents import (
    Document,
    LoadDocumentsInput,
    LoadDocumentsOutput,
    LoadDocumentsSkill,
)
from .registry import (
    SkillInfo,
    SkillRegistry,
    SkillV2Info,
    create_default_registry,
    get_default_registry,
)
from .web_search import (
    SearchResult,
    WebSearchInput,
    WebSearchOutput,
    WebSearchSkill,
)
from .zero_skill import (
    ZeroSkill,
    ZeroSkillInput,
    ZeroSkillOutput,
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
    "SkillInfo",
    "SkillRegistry",
    "SkillV2Info",  # Backward compatibility alias
    "create_default_registry",
    "get_default_registry",
    # AF0065: Summarize playbook skills
    "Document",
    "LoadDocumentsInput",
    "LoadDocumentsOutput",
    "LoadDocumentsSkill",
    "EmitResultInput",
    "EmitResultOutput",
    "EmitResultSkill",
    # AF0080: Web search skill
    "SearchResult",
    "WebSearchInput",
    "WebSearchOutput",
    "WebSearchSkill",
    # Zero skill (dummy)
    "ZeroSkill",
    "ZeroSkillInput",
    "ZeroSkillOutput",
]
