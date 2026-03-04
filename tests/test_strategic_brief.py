"""Tests for strategic_brief skill (AF0048)."""

from __future__ import annotations

import json
from pathlib import Path

from ag.skills.strategic_brief import (
    Citation,
    SourceExcerpt,
    SourceFile,
    StrategicBrief,
    _extract_title_from_markdown,
    _read_markdown_files,
    strategic_brief_skill,
)


class TestStrategicBriefSchema:
    """Tests for the strategic brief schema structures."""

    def test_source_excerpt_schema(self):
        """Source excerpt has required fields."""
        excerpt = SourceExcerpt(line_start=1, line_end=10, content="test content")
        assert excerpt.line_start == 1
        assert excerpt.line_end == 10
        assert excerpt.content == "test content"

    def test_source_file_schema(self):
        """Source file has required fields."""
        source = SourceFile(path="docs/test.md", title="Test Doc")
        assert source.path == "docs/test.md"
        assert source.title == "Test Doc"
        assert source.excerpts == []

    def test_strategic_brief_schema(self):
        """Strategic brief has required fields."""
        brief = StrategicBrief(
            title="Test Brief",
            workspace_path="/test/workspace",
        )
        assert brief.title == "Test Brief"
        assert brief.workspace_path == "/test/workspace"
        assert brief.schema_version == "1.0"
        assert brief.sources == []
        assert brief.sections == []

    def test_brief_serializes_to_json(self):
        """Brief can be serialized to JSON."""
        brief = StrategicBrief(
            title="Test Brief",
            workspace_path="/test",
        )
        json_str = brief.model_dump_json()
        parsed = json.loads(json_str)
        assert parsed["title"] == "Test Brief"


class TestMarkdownParsing:
    """Tests for markdown parsing utilities."""

    def test_extract_title_from_h1(self):
        """Extracts title from H1 heading."""
        content = "# My Document\n\nSome content here."
        title = _extract_title_from_markdown(content)
        assert title == "My Document"

    def test_extract_title_strips_whitespace(self):
        """Title extraction handles whitespace."""
        content = "#   Spaced Title  \n\nContent"
        title = _extract_title_from_markdown(content)
        assert title == "Spaced Title"

    def test_extract_title_returns_none_without_h1(self):
        """Returns None if no H1 heading found."""
        content = "## H2 Heading\n\nNo H1 here."
        title = _extract_title_from_markdown(content)
        assert title is None

    def test_extract_title_ignores_h2(self):
        """Does not extract H2 as title."""
        content = "Some text\n## Not a title\nMore text"
        title = _extract_title_from_markdown(content)
        assert title is None


class TestReadMarkdownFiles:
    """Tests for reading markdown files from workspace."""

    def test_reads_md_files(self, tmp_path: Path):
        """Reads markdown files from directory."""
        # Create test files
        (tmp_path / "doc1.md").write_text("# Document 1\n\nContent here.", encoding="utf-8")
        (tmp_path / "doc2.md").write_text("# Document 2\n\nMore content.", encoding="utf-8")

        sources = _read_markdown_files(tmp_path)

        assert len(sources) == 2
        titles = {s.title for s in sources}
        assert "Document 1" in titles
        assert "Document 2" in titles

    def test_reads_nested_md_files(self, tmp_path: Path):
        """Reads markdown files from subdirectories."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "nested.md").write_text("# Nested Doc\n\nNested content.", encoding="utf-8")

        sources = _read_markdown_files(tmp_path)

        assert len(sources) == 1
        assert sources[0].title == "Nested Doc"
        assert "subdir" in sources[0].path

    def test_returns_empty_for_nonexistent_path(self, tmp_path: Path):
        """Returns empty list for non-existent path."""
        nonexistent = tmp_path / "does_not_exist"
        sources = _read_markdown_files(nonexistent)
        assert sources == []

    def test_respects_max_files_limit(self, tmp_path: Path):
        """Respects max_files parameter."""
        # Create many files
        for i in range(10):
            (tmp_path / f"doc{i}.md").write_text(f"# Doc {i}\n\nContent", encoding="utf-8")

        sources = _read_markdown_files(tmp_path, max_files=3)

        assert len(sources) == 3

    def test_extracts_excerpts(self, tmp_path: Path):
        """Extracts content excerpts from files."""
        content = "# Title\n\nLine 1\nLine 2\nLine 3"
        (tmp_path / "doc.md").write_text(content, encoding="utf-8")

        sources = _read_markdown_files(tmp_path)

        assert len(sources) == 1
        assert len(sources[0].excerpts) == 1
        assert "Title" in sources[0].excerpts[0].content

    def test_ignores_non_md_files(self, tmp_path: Path):
        """Ignores non-markdown files."""
        (tmp_path / "doc.md").write_text("# Markdown", encoding="utf-8")
        (tmp_path / "image.png").write_bytes(b"fake image")
        (tmp_path / "data.json").write_text('{"key": "value"}', encoding="utf-8")

        sources = _read_markdown_files(tmp_path)

        assert len(sources) == 1
        assert sources[0].path == "doc.md"


class TestStrategicBriefSkill:
    """Tests for the strategic_brief skill function."""

    def test_skill_success_with_md_files(self, tmp_path: Path):
        """Skill succeeds with valid workspace containing markdown files."""
        # Create test workspace
        (tmp_path / "readme.md").write_text(
            "# Project README\n\nProject description.", encoding="utf-8"
        )
        (tmp_path / "design.md").write_text("# Design Doc\n\nDesign details.", encoding="utf-8")

        success, summary, result = strategic_brief_skill({"workspace_path": str(tmp_path)})

        assert success is True
        assert "2 sources" in summary
        assert result["source_count"] == 2
        assert "brief_json" in result
        assert "brief_md" in result

    def test_skill_fails_without_workspace_path(self):
        """Skill fails when workspace_path not provided."""
        success, summary, result = strategic_brief_skill({})

        assert success is False
        assert "missing" in summary.lower() or "workspace_path" in summary
        assert "error" in result

    def test_skill_fails_with_nonexistent_workspace(self, tmp_path: Path):
        """Skill fails when workspace does not exist."""
        nonexistent = tmp_path / "does_not_exist"

        success, summary, result = strategic_brief_skill({"workspace_path": str(nonexistent)})

        assert success is False
        assert "not exist" in summary.lower() or "not found" in summary.lower()

    def test_skill_fails_with_no_md_files(self, tmp_path: Path):
        """Skill fails when workspace has no markdown files."""
        (tmp_path / "data.json").write_text('{"key": "value"}', encoding="utf-8")

        success, summary, result = strategic_brief_skill({"workspace_path": str(tmp_path)})

        assert success is False
        assert "no markdown" in summary.lower() or "no_sources" in result.get("error", "")

    def test_skill_custom_title(self, tmp_path: Path):
        """Skill uses custom title when provided."""
        (tmp_path / "doc.md").write_text("# Doc\n\nContent", encoding="utf-8")

        success, summary, result = strategic_brief_skill(
            {
                "workspace_path": str(tmp_path),
                "title": "Custom Brief Title",
            }
        )

        assert success is True
        brief = result["brief"]
        assert brief["title"] == "Custom Brief Title"

    def test_skill_respects_max_files(self, tmp_path: Path):
        """Skill respects max_files parameter."""
        for i in range(10):
            (tmp_path / f"doc{i}.md").write_text(f"# Doc {i}\n\nContent", encoding="utf-8")

        success, summary, result = strategic_brief_skill(
            {
                "workspace_path": str(tmp_path),
                "max_files": 3,
            }
        )

        assert success is True
        assert result["source_count"] == 3

    def test_skill_output_json_valid(self, tmp_path: Path):
        """Skill produces valid JSON output."""
        (tmp_path / "doc.md").write_text("# Doc\n\nContent", encoding="utf-8")

        success, _, result = strategic_brief_skill({"workspace_path": str(tmp_path)})

        assert success is True
        # Parse JSON to verify it's valid
        parsed = json.loads(result["brief_json"])
        assert "title" in parsed
        assert "sources" in parsed
        assert "sections" in parsed

    def test_skill_output_markdown_formatted(self, tmp_path: Path):
        """Skill produces formatted markdown output."""
        (tmp_path / "doc.md").write_text("# Test Doc\n\nContent here.", encoding="utf-8")

        success, _, result = strategic_brief_skill({"workspace_path": str(tmp_path)})

        assert success is True
        md = result["brief_md"]
        assert "# Strategic Brief" in md  # Default title
        assert "Executive Summary" in md
        assert "Source Index" in md

    def test_skill_citations_reference_sources(self, tmp_path: Path):
        """Skill generates citations that reference sources."""
        (tmp_path / "doc.md").write_text("# Doc\n\nContent", encoding="utf-8")

        success, _, result = strategic_brief_skill({"workspace_path": str(tmp_path)})

        assert success is True
        brief = result["brief"]

        # Check that citations reference existing source paths
        source_paths = {s["path"] for s in brief["sources"]}
        for section in brief["sections"]:
            for citation in section["citations"]:
                assert citation["source_path"] in source_paths


class TestStrategicBriefIntegration:
    """Integration tests with realistic workspace structures."""

    def test_processes_nested_project_structure(self, tmp_path: Path):
        """Handles typical project documentation structure."""
        # Create realistic structure
        docs = tmp_path / "docs"
        docs.mkdir()
        (docs / "README.md").write_text("# Project Docs\n\nMain documentation.", encoding="utf-8")
        (docs / "ARCHITECTURE.md").write_text("# Architecture\n\nSystem design.", encoding="utf-8")

        src = tmp_path / "src"
        src.mkdir()
        (src / "module.md").write_text("# Module Guide\n\nUsage guide.", encoding="utf-8")

        success, summary, result = strategic_brief_skill({"workspace_path": str(tmp_path)})

        assert success is True
        assert result["source_count"] == 3

        # Check sections are categorized
        brief = result["brief"]
        section_headings = {s["heading"] for s in brief["sections"]}
        assert "Docs" in section_headings or "docs" in str(section_headings).lower()

    def test_handles_large_workspace(self, tmp_path: Path):
        """Handles workspace with many files efficiently."""
        # Create 30 files
        for i in range(30):
            (tmp_path / f"doc_{i:03d}.md").write_text(
                f"# Document {i}\n\nContent for document {i}.", encoding="utf-8"
            )

        success, summary, result = strategic_brief_skill(
            {
                "workspace_path": str(tmp_path),
                "max_files": 25,
            }
        )

        assert success is True
        assert result["source_count"] == 25
        assert "25 sources" in summary


class TestCitationEvidenceRefConversion:
    """Tests for Citation to EvidenceRef conversion (AF0054)."""

    def test_citation_to_evidence_ref_basic(self):
        """Citation converts to EvidenceRef with correct fields."""
        citation = Citation(
            source_path="docs/test.md",
            excerpt_index=None,
            context="Test context",
        )
        evidence_ref = citation.to_evidence_ref()

        assert evidence_ref.source_type == "file"
        assert evidence_ref.source_path == "docs/test.md"
        assert evidence_ref.relevance == "Test context"
        assert evidence_ref.ref_id.startswith("cite-")
        assert len(evidence_ref.ref_id) == 13  # "cite-" + 8 hex chars

    def test_citation_to_evidence_ref_custom_id(self):
        """Citation accepts custom ref_id."""
        citation = Citation(source_path="test.md", context="ctx")
        evidence_ref = citation.to_evidence_ref(ref_id="custom-001")

        assert evidence_ref.ref_id == "custom-001"

    def test_citation_to_evidence_ref_with_source_file(self):
        """Citation extracts excerpt from SourceFile."""
        source_file = SourceFile(
            path="docs/test.md",
            title="Test Doc",
            excerpts=[
                SourceExcerpt(line_start=10, line_end=15, content="First excerpt"),
                SourceExcerpt(line_start=20, line_end=25, content="Second excerpt"),
            ],
        )
        citation = Citation(
            source_path="docs/test.md",
            excerpt_index=1,
            context="Referencing second excerpt",
        )
        evidence_ref = citation.to_evidence_ref(source_file=source_file)

        assert evidence_ref.excerpt == "Second excerpt"
        assert evidence_ref.line_start == 20
        assert evidence_ref.line_end == 25
        assert evidence_ref.relevance == "Referencing second excerpt"

    def test_citation_to_evidence_ref_invalid_excerpt_index(self):
        """Citation handles out-of-range excerpt_index gracefully."""
        source_file = SourceFile(
            path="docs/test.md",
            excerpts=[SourceExcerpt(line_start=1, line_end=5, content="Only one")],
        )
        citation = Citation(source_path="docs/test.md", excerpt_index=99)
        evidence_ref = citation.to_evidence_ref(source_file=source_file)

        assert evidence_ref.excerpt is None
        assert evidence_ref.line_start is None
        assert evidence_ref.line_end is None

    def test_citation_to_evidence_ref_empty_context(self):
        """Citation with empty context sets relevance to None."""
        citation = Citation(source_path="test.md", context="")
        evidence_ref = citation.to_evidence_ref()

        assert evidence_ref.relevance is None