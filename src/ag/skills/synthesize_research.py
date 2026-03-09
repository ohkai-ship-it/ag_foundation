"""Synthesize Research Skill — LLM-Powered Research Synthesis (AF0074).

This skill synthesizes research from multiple source documents into a
coherent report with citations. It is the core LLM capability skill
for the research_v0 playbook.

Schemas Defined (see docs/dev/additional/SCHEMA_INVENTORY.md):
    SourceDocument — Unified document schema for research sources
    SynthesizeResearchInput — Input schema (prompt, documents, output_format)
    SynthesizeResearchOutput — Output schema (report, sources_used, key_findings)

Contracts Implemented (see docs/dev/additional/CONTRACT_INVENTORY.md):
    Skill[SynthesizeResearchInput, SynthesizeResearchOutput] — Research synthesis

Pipeline Position:
    This is step 3 of the research_v0 playbook:
    load_documents → fetch_web_content → synthesize_research → emit_result

LLM Integration:
    This skill requires ctx.provider to be set. It:
    1. Combines local and web documents into a context
    2. Builds a synthesis prompt with the research question
    3. Calls provider.chat() for synthesis
    4. Parses response into structured report with citations

    In manual mode (no provider), returns a stub output.
"""

from __future__ import annotations

import re
from typing import Any, ClassVar

from pydantic import BaseModel, Field, model_validator

from ag.skills.base import Skill, SkillContext, SkillInput, SkillOutput


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------


class SourceDocument(BaseModel):
    """A source document for research synthesis.

    This unified schema represents documents from any source:
    - Local files (from load_documents)
    - Web pages (from fetch_web_content)

    Schema: SCHEMA_INVENTORY.md#SourceDocument
    """

    source: str = Field(..., description="Source identifier (filepath or URL)")
    content: str = Field(..., description="Text content of the document")
    title: str | None = Field(default=None, description="Document title if available")
    source_type: str = Field(
        default="unknown", description="Source type: 'file', 'url', or 'unknown'"
    )

    model_config = {"extra": "forbid"}


def _convert_to_source_document(doc: dict | SourceDocument) -> SourceDocument:
    """Convert various document formats to SourceDocument.

    Handles:
    - SourceDocument (passthrough)
    - FetchedDocument dict (from fetch_web_content)
    - Document dict (from load_documents)

    Args:
        doc: Document in any supported format

    Returns:
        SourceDocument instance
    """
    if isinstance(doc, SourceDocument):
        return doc

    # Handle dict format
    if isinstance(doc, dict):
        # FetchedDocument format (from fetch_web_content)
        if "url" in doc:
            return SourceDocument(
                source=doc.get("url", "unknown"),
                content=doc.get("content", ""),
                title=doc.get("title"),
                source_type="url",
            )
        # Document format (from load_documents)
        if "path" in doc:
            return SourceDocument(
                source=doc.get("path", "unknown"),
                content=doc.get("content", ""),
                title=None,
                source_type="file",
            )
        # Generic dict with source field
        return SourceDocument(
            source=doc.get("source", "unknown"),
            content=doc.get("content", ""),
            title=doc.get("title"),
            source_type=doc.get("source_type", "unknown"),
        )

    # Fallback
    return SourceDocument(source="unknown", content=str(doc), source_type="unknown")


class SynthesizeResearchInput(SkillInput):
    """Input for synthesize_research skill.

    Schema: SCHEMA_INVENTORY.md#SynthesizeResearchInput

    Accepts documents in multiple formats:
    - SourceDocument objects
    - FetchedDocument dicts (from fetch_web_content pipeline)
    - Document dicts (from load_documents pipeline)
    """

    documents: list[SourceDocument] = Field(
        default_factory=list, description="Source documents for synthesis"
    )
    output_format: str = Field(
        default="markdown",
        description="Output format: 'markdown', 'plain', or 'json'",
    )
    max_tokens: int = Field(
        default=4000,
        ge=500,
        le=16000,
        description="Maximum tokens for LLM response",
    )
    include_citations: bool = Field(
        default=True, description="Include source citations in output"
    )

    # Allow extra fields from pipeline chaining (e.g., failed_urls, total_fetched)
    model_config = {"extra": "ignore"}

    @model_validator(mode="before")
    @classmethod
    def convert_documents(cls, data: dict) -> dict:
        """Convert incoming documents to SourceDocument format."""
        if "documents" in data and data["documents"]:
            data["documents"] = [
                _convert_to_source_document(doc) for doc in data["documents"]
            ]
        return data


class SynthesizeResearchOutput(SkillOutput):
    """Output from synthesize_research skill.

    Schema: SCHEMA_INVENTORY.md#SynthesizeResearchOutput
    """

    report: str = Field(default="", description="Synthesized research report")
    sources_used: list[str] = Field(
        default_factory=list, description="List of sources cited in report"
    )
    key_findings: list[str] = Field(
        default_factory=list, description="Key findings as bullet points"
    )
    source_count: int = Field(default=0, description="Number of source documents used")

    model_config = {"extra": "forbid"}


# ---------------------------------------------------------------------------
# Prompt Construction
# ---------------------------------------------------------------------------


def _build_synthesis_prompt(
    research_question: str,
    documents: list[SourceDocument],
    output_format: str,
    include_citations: bool,
) -> str:
    """Build the LLM prompt for research synthesis.

    Args:
        research_question: User's research question/topic
        documents: Source documents to synthesize
        output_format: Desired output format
        include_citations: Whether to include source citations

    Returns:
        Formatted prompt for LLM
    """
    # Build document context
    doc_sections = []
    for i, doc in enumerate(documents, 1):
        source_label = f"[Source {i}]"
        source_info = doc.title or doc.source
        doc_sections.append(
            f"{source_label} {source_info}\n"
            f"Type: {doc.source_type}\n"
            f"Content:\n{doc.content[:10000]}..."  # Truncate very long docs
            if len(doc.content) > 10000
            else f"{source_label} {source_info}\n"
            f"Type: {doc.source_type}\n"
            f"Content:\n{doc.content}"
        )

    documents_text = "\n\n---\n\n".join(doc_sections)

    citation_instruction = (
        "Include citations to sources using [Source N] format."
        if include_citations
        else "Do not include explicit citations."
    )

    format_instruction = {
        "markdown": "Format the response in Markdown with headers and bullet points.",
        "plain": "Format the response as plain text with clear paragraphs.",
        "json": 'Format the response as JSON with "report", "key_findings", and "sources" fields.',
    }.get(output_format, "Format the response in Markdown.")

    prompt = f"""You are a research analyst synthesizing information from multiple sources.

RESEARCH QUESTION:
{research_question}

SOURCE DOCUMENTS:
{documents_text}

INSTRUCTIONS:
1. Synthesize a comprehensive research report answering the research question
2. Extract 3-7 key findings as bullet points
3. {citation_instruction}
4. {format_instruction}
5. Be objective and note any conflicting information between sources
6. If sources are insufficient, note what additional information would be helpful

Please provide your synthesis:"""

    return prompt


def _extract_key_findings(report: str) -> list[str]:
    """Extract key findings from the report.

    Simple extraction looking for bullet points or numbered lists.

    Args:
        report: The generated report

    Returns:
        List of key finding strings
    """
    findings = []

    # Look for bullet points (- or * or •)
    bullet_matches = re.findall(r"^[\-\*•]\s*(.+)$", report, re.MULTILINE)
    findings.extend(bullet_matches[:10])  # Max 10 findings

    # If not enough, look for numbered lists
    if len(findings) < 3:
        numbered_matches = re.findall(r"^\d+[\.\)]\s*(.+)$", report, re.MULTILINE)
        for match in numbered_matches:
            if match not in findings:
                findings.append(match)
            if len(findings) >= 7:
                break

    return findings[:7]  # Cap at 7 key findings


def _extract_sources_used(report: str, documents: list[SourceDocument]) -> list[str]:
    """Extract which sources were cited in the report.

    Args:
        report: The generated report
        documents: Original source documents

    Returns:
        List of source identifiers that were cited
    """
    sources_used = []

    # Look for [Source N] citations
    citations = re.findall(r"\[Source\s+(\d+)\]", report)
    cited_indices = set(int(c) for c in citations)

    for i, doc in enumerate(documents, 1):
        if i in cited_indices:
            sources_used.append(doc.source)

    # If no explicit citations found, assume all were used
    if not sources_used:
        sources_used = [doc.source for doc in documents]

    return sources_used


# ---------------------------------------------------------------------------
# Fallback for Manual Mode
# ---------------------------------------------------------------------------


def _fallback_synthesis(
    research_question: str,
    documents: list[SourceDocument],
) -> tuple[str, list[str]]:
    """Generate a stub synthesis when no LLM is available.

    Args:
        research_question: User's research question
        documents: Source documents

    Returns:
        Tuple of (report, key_findings)
    """
    source_list = "\n".join(
        f"- {doc.title or doc.source} ({doc.source_type})" for doc in documents
    )

    report = f"""# Research Synthesis (Stub)

**Research Question:** {research_question}

## Sources Analyzed

{source_list}

## Summary

This is a stub synthesis generated without LLM access.
In production mode, this would contain a comprehensive analysis
of the {len(documents)} source document(s) provided.

## Key Findings

- Source documents were successfully loaded
- Manual mode active (no LLM provider)
- Full synthesis requires LLM execution mode

## Next Steps

Run with `--mode llm` and a configured LLM provider for full synthesis.
"""

    key_findings = [
        f"Analyzed {len(documents)} source documents",
        "Manual mode - LLM synthesis not available",
        "Run with LLM mode for full research synthesis",
    ]

    return report, key_findings


# ---------------------------------------------------------------------------
# Skill Implementation
# ---------------------------------------------------------------------------


class SynthesizeResearchSkill(Skill[SynthesizeResearchInput, SynthesizeResearchOutput]):
    """Synthesize research from multiple source documents.

    This skill uses an LLM to synthesize a research report from multiple
    sources, including citations and key findings extraction.

    Contract: CONTRACT_INVENTORY.md#SynthesizeResearchSkill

    Args:
        prompt: Research question or topic
        documents: List of SourceDocument objects
        output_format: 'markdown', 'plain', or 'json'
        include_citations: Whether to cite sources

    Returns:
        SynthesizeResearchOutput with report, sources_used, key_findings

    Example:
        skill = SynthesizeResearchSkill()
        output = skill.execute(
            SynthesizeResearchInput(
                prompt="What are the key trends in AI?",
                documents=[...],
            ),
            SkillContext(provider=llm_provider)
        )
        print(output.report)
    """

    name: ClassVar[str] = "synthesize_research"
    description: ClassVar[str] = "Synthesize research report from multiple sources"
    input_schema: ClassVar[type[SynthesizeResearchInput]] = SynthesizeResearchInput
    output_schema: ClassVar[type[SynthesizeResearchOutput]] = SynthesizeResearchOutput
    requires_llm: ClassVar[bool] = True

    def execute(
        self, input: SynthesizeResearchInput, ctx: SkillContext
    ) -> SynthesizeResearchOutput:
        """Synthesize research from the provided documents.

        Args:
            input: Research question and source documents
            ctx: Skill context with LLM provider

        Returns:
            Output with synthesized report and findings
        """
        if not input.documents:
            return SynthesizeResearchOutput(
                success=False,
                summary="No documents provided for synthesis",
                error="At least one source document is required",
                report="",
                sources_used=[],
                key_findings=[],
                source_count=0,
            )

        research_question = input.prompt or "Provide a comprehensive research synthesis"

        # Fallback for manual mode (no LLM)
        if not ctx.has_provider:
            report, key_findings = _fallback_synthesis(research_question, input.documents)
            return SynthesizeResearchOutput(
                success=True,
                summary=f"Stub synthesis of {len(input.documents)} documents (manual mode)",
                report=report,
                sources_used=[doc.source for doc in input.documents],
                key_findings=key_findings,
                source_count=len(input.documents),
            )

        # Build synthesis prompt
        prompt = _build_synthesis_prompt(
            research_question=research_question,
            documents=input.documents,
            output_format=input.output_format,
            include_citations=input.include_citations,
        )

        # Call LLM
        try:
            response = ctx.provider.chat(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=input.max_tokens,
            )
            report = response.get("content", "")
        except Exception as e:
            return SynthesizeResearchOutput(
                success=False,
                summary=f"LLM synthesis failed: {e}",
                error=str(e),
                report="",
                sources_used=[],
                key_findings=[],
                source_count=len(input.documents),
            )

        # Extract key findings and sources
        key_findings = _extract_key_findings(report)
        sources_used = _extract_sources_used(report, input.documents)

        return SynthesizeResearchOutput(
            success=True,
            summary=f"Synthesized research from {len(input.documents)} sources",
            report=report,
            sources_used=sources_used,
            key_findings=key_findings,
            source_count=len(input.documents),
        )
