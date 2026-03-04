"""Strategic Brief Skill (AF0048).

Reads markdown files from a workspace directory and produces a structured
strategic brief with evidence citations.

Output:
- brief.json: Structured JSON with sections and citations
- brief.md: Human-readable markdown summary
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Schema definitions for structured output
# ---------------------------------------------------------------------------


class SourceExcerpt(BaseModel):
    """An excerpt from a source file."""

    line_start: int = Field(..., ge=1, description="Starting line number")
    line_end: int = Field(..., ge=1, description="Ending line number")
    content: str = Field(..., description="Excerpt content")


class SourceFile(BaseModel):
    """A source file read during brief generation."""

    path: str = Field(..., description="Relative path to source file")
    title: str | None = Field(default=None, description="Document title if found")
    excerpts: list[SourceExcerpt] = Field(default_factory=list, description="Extracted excerpts")


class Citation(BaseModel):
    """A citation referencing a source file."""

    source_path: str = Field(..., description="Path to cited source")
    excerpt_index: int | None = Field(default=None, description="Index into source excerpts")
    context: str = Field(default="", description="Citation context")


class BriefSection(BaseModel):
    """A section in the strategic brief."""

    heading: str = Field(..., description="Section heading")
    content: str = Field(..., description="Section content")
    citations: list[Citation] = Field(
        default_factory=list, description="Citations for this section"
    )


class StrategicBrief(BaseModel):
    """The complete strategic brief output schema."""

    schema_version: str = Field(default="1.0", description="Brief schema version")
    title: str = Field(..., description="Brief title")
    generated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Generation timestamp",
    )
    workspace_path: str = Field(..., description="Source workspace path")
    sources: list[SourceFile] = Field(default_factory=list, description="Source files read")
    sections: list[BriefSection] = Field(default_factory=list, description="Brief sections")
    summary: str = Field(default="", description="Executive summary")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    model_config = {"extra": "forbid"}


# ---------------------------------------------------------------------------
# Skill implementation
# ---------------------------------------------------------------------------


def _extract_title_from_markdown(content: str) -> str | None:
    """Extract title from markdown content (first H1 heading)."""
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return None


def _read_markdown_files(workspace_path: Path, max_files: int = 50) -> list[SourceFile]:
    """Read markdown files from workspace directory.

    Args:
        workspace_path: Path to workspace directory
        max_files: Maximum number of files to read

    Returns:
        List of SourceFile objects with content excerpts
    """
    sources: list[SourceFile] = []

    if not workspace_path.exists():
        return sources

    md_files = list(workspace_path.rglob("*.md"))[:max_files]

    for md_path in md_files:
        try:
            content = md_path.read_text(encoding="utf-8")
            lines = content.split("\n")

            # Extract title
            title = _extract_title_from_markdown(content)

            # Create excerpt from first meaningful section (up to 20 lines)
            excerpts: list[SourceExcerpt] = []
            if lines:
                # Find first non-empty content
                start_line = 0
                for i, line in enumerate(lines):
                    if line.strip():
                        start_line = i
                        break

                # Take up to 20 lines of content
                end_line = min(start_line + 20, len(lines))
                excerpt_content = "\n".join(lines[start_line:end_line])

                if excerpt_content.strip():
                    excerpts.append(
                        SourceExcerpt(
                            line_start=start_line + 1,  # 1-indexed
                            line_end=end_line,
                            content=excerpt_content,
                        )
                    )

            rel_path = str(md_path.relative_to(workspace_path))
            sources.append(SourceFile(path=rel_path, title=title, excerpts=excerpts))

        except (OSError, UnicodeDecodeError):
            # Skip files that can't be read
            continue

    return sources


def _generate_sections_from_sources(sources: list[SourceFile]) -> list[BriefSection]:
    """Generate brief sections from source files.

    v0: Simple aggregation by source file. Future versions will use
    LLM for intelligent synthesis.
    """
    sections: list[BriefSection] = []

    # Group sources by apparent category (based on path structure)
    categorized: dict[str, list[SourceFile]] = {"general": []}

    for source in sources:
        # Simple categorization by first directory
        parts = Path(source.path).parts
        if len(parts) > 1:
            category = parts[0]
        else:
            category = "general"

        if category not in categorized:
            categorized[category] = []
        categorized[category].append(source)

    # Generate a section per category
    for category, cat_sources in categorized.items():
        if not cat_sources:
            continue

        # Build section content from source titles/excerpts
        content_parts: list[str] = []
        citations: list[Citation] = []

        for source in cat_sources:
            if source.title:
                content_parts.append(f"- **{source.title}** ({source.path})")
            else:
                content_parts.append(f"- {source.path}")

            # Add citation
            citations.append(
                Citation(
                    source_path=source.path,
                    excerpt_index=0 if source.excerpts else None,
                    context=source.title or source.path,
                )
            )

        section = BriefSection(
            heading=category.replace("_", " ").title(),
            content="\n".join(content_parts),
            citations=citations,
        )
        sections.append(section)

    return sections


def _generate_summary(sources: list[SourceFile], sections: list[BriefSection]) -> str:
    """Generate executive summary.

    v0: Simple statistics. Future versions will use LLM.
    """
    total_sources = len(sources)
    total_sections = len(sections)
    titled_sources = sum(1 for s in sources if s.title)

    return (
        f"This strategic brief synthesizes {total_sources} source documents "
        f"into {total_sections} sections. {titled_sources} documents have "
        f"explicit titles. Review each section for detailed evidence citations."
    )


def _generate_markdown_output(brief: StrategicBrief) -> str:
    """Generate human-readable markdown from the brief."""
    lines: list[str] = []

    lines.append(f"# {brief.title}")
    lines.append("")
    lines.append(f"*Generated: {brief.generated_at.isoformat()}*")
    lines.append("")

    # Summary
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(brief.summary)
    lines.append("")

    # Sections
    for section in brief.sections:
        lines.append(f"## {section.heading}")
        lines.append("")
        lines.append(section.content)
        lines.append("")

        if section.citations:
            lines.append("**Sources:**")
            for citation in section.citations:
                lines.append(f"- {citation.source_path}")
            lines.append("")

    # Source index
    lines.append("## Source Index")
    lines.append("")
    for source in brief.sources:
        title_part = f" - {source.title}" if source.title else ""
        lines.append(f"- `{source.path}`{title_part}")
    lines.append("")

    return "\n".join(lines)


def strategic_brief_skill(params: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    """Generate a strategic brief from workspace markdown files.

    Args (via params):
        workspace_path: Path to workspace directory containing markdown files
        title: Optional title for the brief (default: "Strategic Brief")
        max_files: Maximum files to process (default: 50)

    Returns:
        Tuple of (success, output_summary, result_data)
        result_data contains:
        - brief_json: Serialized StrategicBrief
        - brief_md: Markdown formatted output
        - source_count: Number of sources processed
        - section_count: Number of sections generated
    """
    # Extract parameters
    workspace_path_str = params.get("workspace_path")
    if not workspace_path_str:
        return (
            False,
            "Missing required parameter: workspace_path",
            {"error": "missing_workspace_path"},
        )

    workspace_path = Path(workspace_path_str)
    if not workspace_path.exists():
        return (
            False,
            f"Workspace path does not exist: {workspace_path}",
            {"error": "workspace_not_found"},
        )

    title = params.get("title", "Strategic Brief")
    max_files = params.get("max_files", 50)

    try:
        # Read sources
        sources = _read_markdown_files(workspace_path, max_files=max_files)

        if not sources:
            return (
                False,
                "No markdown files found in workspace",
                {"error": "no_sources", "workspace_path": str(workspace_path)},
            )

        # Generate sections
        sections = _generate_sections_from_sources(sources)

        # Generate summary
        summary = _generate_summary(sources, sections)

        # Build the brief
        brief = StrategicBrief(
            title=title,
            workspace_path=str(workspace_path),
            sources=sources,
            sections=sections,
            summary=summary,
            metadata={
                "max_files": max_files,
                "generator": "strategic_brief_skill",
                "version": "1.0",
            },
        )

        # Generate outputs
        brief_json = brief.model_dump_json(indent=2)
        brief_md = _generate_markdown_output(brief)

        # Build result
        result_data = {
            "brief_json": brief_json,
            "brief_md": brief_md,
            "source_count": len(sources),
            "section_count": len(sections),
            "brief": json.loads(brief_json),  # Also include as dict for convenience
        }

        output_summary = (
            f"Generated strategic brief with {len(sources)} sources and {len(sections)} sections"
        )

        return True, output_summary, result_data

    except Exception as e:
        return False, f"Brief generation failed: {e}", {"error": str(e)}
