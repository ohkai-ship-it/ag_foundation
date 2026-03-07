"""Skills and plugin registry.

AF0060: Added base skill framework with typed schemas.
AF0065: Added summarize_v0 skills (load_documents, summarize_docs, emit_result).
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
