"""Summarize Documents Skill (AF0065).

Calls LLM to summarize document contents and extract key points.

This is the second skill in the summarize_v0 playbook pipeline:
load_documents → summarize_docs → emit_result
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from pydantic import Field

from ag.skills.base import Skill, SkillContext, SkillInput, SkillOutput
from ag.skills.load_documents import Document

if TYPE_CHECKING:
    pass


# ---------------------------------------------------------------------------
# Schema Definitions
# ---------------------------------------------------------------------------


class SummarizeDocsInput(SkillInput):
    """Input schema for summarize_docs skill.

    Attributes:
        documents: List of documents from load_documents skill
        prompt: User's summarization request/focus
        max_tokens: Maximum tokens for LLM response
    """

    documents: list[Document] = Field(
        default_factory=list,
        description="Documents to summarize (from load_documents)",
    )
    max_tokens: int = Field(
        default=2000,
        ge=100,
        le=8000,
        description="Maximum tokens for LLM response",
    )

    model_config = {"extra": "forbid"}


class SummarizeDocsOutput(SkillOutput):
    """Output schema for summarize_docs skill.

    Attributes:
        document_summary: The generated summary text (content)
        key_points: List of extracted key points
        source_count: Number of source documents used
        sources: List of source file paths
    
    Note: Inherits `summary` from SkillOutput for status message.
    Use `document_summary` for the actual LLM-generated content.
    """

    document_summary: str = Field(
        default="",
        description="Generated summary text (LLM output)",
    )
    key_points: list[str] = Field(
        default_factory=list,
        description="Extracted key points",
    )
    source_count: int = Field(
        default=0,
        ge=0,
        description="Number of source documents used",
    )
    sources: list[str] = Field(
        default_factory=list,
        description="List of source file paths",
    )

    model_config = {"extra": "forbid"}


# ---------------------------------------------------------------------------
# Skill Implementation
# ---------------------------------------------------------------------------


class SummarizeDocsSkill(Skill[SummarizeDocsInput, SummarizeDocsOutput]):
    """Summarize documents using LLM.

    This skill takes documents loaded by load_documents and produces
    a summary with key points using an LLM provider.

    If no LLM provider is available, falls back to a simple
    extraction-based summary.

    Example usage:
        skill = SummarizeDocsSkill()
        ctx = SkillContext(provider=llm_provider)
        input = SummarizeDocsInput(
            documents=[...],
            prompt="Summarize the architecture",
        )
        output = skill.execute(input, ctx)
    """

    name: ClassVar[str] = "summarize_docs"
    description: ClassVar[str] = "Summarize documents using LLM"
    input_schema: ClassVar[type[SkillInput]] = SummarizeDocsInput
    output_schema: ClassVar[type[SkillOutput]] = SummarizeDocsOutput
    # LLM is preferred but skill falls back to simple extraction without it
    requires_llm: ClassVar[bool] = True

    def execute(
        self,
        input: SummarizeDocsInput,
        ctx: SkillContext,
    ) -> SummarizeDocsOutput:
        """Execute the summarize_docs skill.

        Args:
            input: Validated input with documents and prompt
            ctx: Runtime context with LLM provider

        Returns:
            SummarizeDocsOutput with summary and key points
        """
        from ag.providers.base import ChatMessage, MessageRole

        # Validate we have documents
        if not input.documents:
            return SummarizeDocsOutput(
                success=False,
                summary="No documents provided to summarize",
                error="no_documents",
            )

        sources = [doc.path for doc in input.documents]

        # Check if LLM provider is available
        if not ctx.has_provider or ctx.provider is None:
            # Fallback to simple extraction
            return self._fallback_summary(input.documents, sources)

        try:
            # Build the LLM prompt
            system_prompt = self._build_system_prompt()
            user_prompt = self._build_user_prompt(input.documents, input.prompt)

            # Call LLM
            messages = [
                ChatMessage(role=MessageRole.SYSTEM, content=system_prompt),
                ChatMessage(role=MessageRole.USER, content=user_prompt),
            ]

            response = ctx.provider.chat(
                messages=messages,
                max_tokens=input.max_tokens,
            )

            # Parse LLM response
            return self._parse_llm_response(response.content, sources)

        except Exception as e:
            return SummarizeDocsOutput(
                success=False,
                summary=f"LLM summarization failed: {e}",
                error=str(e),
                sources=sources,
                source_count=len(sources),
            )

    def _build_system_prompt(self) -> str:
        """Build system prompt for LLM."""
        return """You are a document summarization assistant. Your task is to:
1. Read the provided documents carefully
2. Create a concise but comprehensive summary
3. Extract 3-7 key points as bullet items
4. Maintain accuracy - only include information from the documents

Output format:
## Summary
[Your summary here - 2-4 paragraphs]

## Key Points
- [Key point 1]
- [Key point 2]
- [Key point 3]
...

Be factual and cite document names when making specific claims."""

    def _build_user_prompt(self, documents: list[Document], user_prompt: str) -> str:
        """Build user prompt with documents."""
        parts = []

        if user_prompt:
            parts.append(f"Focus: {user_prompt}")
            parts.append("")

        parts.append("Documents to summarize:")
        parts.append("")

        for doc in documents:
            parts.append(f"=== {doc.path} ===")
            # Include content, truncating very long documents
            content = doc.content
            if len(content) > 10000:
                content = content[:10000] + "\n\n[... content truncated ...]"
            parts.append(content)
            parts.append("")

        return "\n".join(parts)

    def _parse_llm_response(
        self,
        response: str,
        sources: list[str],
    ) -> SummarizeDocsOutput:
        """Parse LLM response into structured output."""
        import sys

        # Split response into sections
        lines = response.split("\n")
        current_section = ""
        summary_lines: list[str] = []
        key_points_lines: list[str] = []
        pre_section_lines: list[str] = []  # Content before any section header

        for line in lines:
            lower_line = line.lower().strip()

            # Detect section headers
            if "## summary" in lower_line or lower_line == "summary":
                current_section = "summary"
                continue
            elif "## key points" in lower_line or lower_line == "key points":
                current_section = "key_points"
                continue

            # Collect content into appropriate section
            if current_section == "summary":
                summary_lines.append(line)
            elif current_section == "key_points":
                key_points_lines.append(line)
            else:
                # Content before any section header
                pre_section_lines.append(line)

        # Extract summary - try section content, then pre-section, then fallback
        summary = "\n".join(summary_lines).strip()
        if not summary:
            # Use pre-section content as summary (common LLM output pattern)
            summary = "\n".join(pre_section_lines).strip()

        # Extract key points
        key_points = self._extract_bullet_points(key_points_lines)

        # Fallback: if no structured output, use whole response
        if not summary and not key_points:
            summary = response.strip()

        return SummarizeDocsOutput(
            success=True,
            summary=f"Summarized {len(sources)} document(s)",
            document_summary=summary or "Summary generated",
            key_points=key_points,
            source_count=len(sources),
            sources=sources,
        )

    def _extract_bullet_points(self, lines: list[str]) -> list[str]:
        """Extract bullet points from lines."""
        points: list[str] = []
        for line in lines:
            line = line.strip()
            if line.startswith("- ") or line.startswith("* "):
                points.append(line[2:].strip())
            elif line.startswith("• "):
                points.append(line[2:].strip())
        return points

    def _fallback_summary(
        self,
        documents: list[Document],
        sources: list[str],
    ) -> SummarizeDocsOutput:
        """Generate simple summary without LLM (fallback mode)."""
        # Extract first paragraph from each document
        summaries: list[str] = []
        key_points: list[str] = []

        for doc in documents[:5]:  # Limit to first 5 docs
            # Get first non-empty paragraph
            paragraphs = doc.content.split("\n\n")
            for para in paragraphs:
                para = para.strip()
                # Skip headers and empty lines
                if para and not para.startswith("#"):
                    summaries.append(f"**{doc.path}**: {para[:200]}...")
                    break

            # Extract H1 headers as key points
            for line in doc.content.split("\n"):
                if line.startswith("# ") and len(key_points) < 7:
                    key_points.append(line[2:].strip())

        summary = "\n\n".join(summaries) if summaries else "No content extracted"

        return SummarizeDocsOutput(
            success=True,
            summary=f"[Fallback mode] Extracted from {len(sources)} document(s)",
            document_summary=summary,
            key_points=key_points,
            source_count=len(sources),
            sources=sources,
        )

    def to_legacy_tuple(self, output: SummarizeDocsOutput) -> tuple[bool, str, dict[str, Any]]:
        """Convert output to legacy skill return format."""
        return output.to_legacy_tuple()
