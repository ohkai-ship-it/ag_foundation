"""Skills package — typed capabilities for AG Foundation (AF0060, AF0065, AF0067).

This package provides the skill framework for building agent capabilities.
Skills are typed, stateless callables that produce structured outputs.

Documentation References:
    - SCHEMA_INVENTORY.md: Documents all Pydantic schemas (SkillInput, SkillOutput, etc.)
    - CONTRACT_INVENTORY.md: Documents the Skill protocol/ABC
    - SKILLS_ARCHITECTURE_0.1.md: High-level architecture and design rationale

Package Structure:
    base.py         — Core classes: Skill ABC, SkillInput, SkillOutput, SkillContext
    registry.py     — SkillRegistry for v1 (legacy) and v2 (typed) skill management
    strategic_brief.py — Example v2 skill: generates strategic briefs from markdown
    load_documents.py  — V2 skill: loads and validates documents from workspace
    summarize_docs.py  — V2 skill: LLM-powered document summarization
    emit_result.py     — V2 skill: emits final results to trace

Quick Start (Creating a New Skill):
    1. Define input schema: subclass SkillInput
    2. Define output schema: subclass SkillOutput
    3. Create skill class: subclass Skill[YourInput, YourOutput]
    4. Implement execute(input, ctx) -> output
    5. Register with: registry.register_v2(YourSkill())

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
    SkillFn,
    SkillInfo,
    SkillRegistry,
    SkillV2Info,
    create_default_registry,
    get_default_registry,
)
from .summarize_docs import (
    SummarizeDocsInput,
    SummarizeDocsOutput,
    SummarizeDocsSkill,
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
    # AF0065: Summarize playbook skills
    "Document",
    "LoadDocumentsInput",
    "LoadDocumentsOutput",
    "LoadDocumentsSkill",
    "SummarizeDocsInput",
    "SummarizeDocsOutput",
    "SummarizeDocsSkill",
    "EmitResultInput",
    "EmitResultOutput",
    "EmitResultSkill",
]
