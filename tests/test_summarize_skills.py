"""Tests for summarize_v0 playbook skills (AF0065, AF0108).

Tests the three skills that make up the summarize_v0 playbook:
- load_documents: Read files from workspace
- synthesize_research: Synthesize/summarize documents with LLM (AF-0108: replaces summarize_docs)
- emit_result: Store output as artifact
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ag.skills.base import SkillContext
from ag.skills.emit_result import EmitResultInput, EmitResultOutput, EmitResultSkill
from ag.skills.load_documents import (
    Document,
    LoadDocumentsInput,
    LoadDocumentsOutput,
    LoadDocumentsSkill,
)

# ---------------------------------------------------------------------------
# LoadDocumentsSkill Tests
# ---------------------------------------------------------------------------


class TestLoadDocumentsSkill:
    """Tests for load_documents skill."""

    def test_skill_metadata(self) -> None:
        """Skill has correct metadata."""
        skill = LoadDocumentsSkill()
        assert skill.name == "load_documents"
        assert skill.requires_llm is False
        assert skill.input_schema == LoadDocumentsInput
        assert skill.output_schema == LoadDocumentsOutput

    def test_load_markdown_files(self, tmp_path: Path) -> None:
        """Successfully loads markdown files from workspace."""
        # Create test files
        (tmp_path / "doc1.md").write_text("# Document 1\nContent 1", encoding="utf-8")
        (tmp_path / "doc2.md").write_text("# Document 2\nContent 2", encoding="utf-8")

        skill = LoadDocumentsSkill()
        ctx = SkillContext(workspace_path=tmp_path)
        input_data = LoadDocumentsInput(patterns=["**/*.md"], max_files=10)

        result = skill.execute(input_data, ctx)

        assert result.success is True
        assert result.file_count == 2
        assert len(result.documents) == 2
        assert result.total_bytes > 0

    def test_load_with_custom_patterns(self, tmp_path: Path) -> None:
        """Loads files matching custom glob patterns."""
        # Create test files
        (tmp_path / "readme.md").write_text("# README", encoding="utf-8")
        (tmp_path / "config.txt").write_text("config data", encoding="utf-8")
        (tmp_path / "data.json").write_text('{"key": "value"}', encoding="utf-8")

        skill = LoadDocumentsSkill()
        ctx = SkillContext(workspace_path=tmp_path)

        # Load only .txt files
        input_data = LoadDocumentsInput(patterns=["**/*.txt"], max_files=10)
        result = skill.execute(input_data, ctx)

        assert result.success is True
        assert result.file_count == 1
        assert result.documents[0].path == "config.txt"

    def test_load_respects_max_files(self, tmp_path: Path) -> None:
        """Respects max_files limit."""
        # Create more files than limit
        for i in range(5):
            (tmp_path / f"doc{i}.md").write_text(f"Doc {i}", encoding="utf-8")

        skill = LoadDocumentsSkill()
        ctx = SkillContext(workspace_path=tmp_path)
        input_data = LoadDocumentsInput(patterns=["**/*.md"], max_files=3)

        result = skill.execute(input_data, ctx)

        assert result.success is True
        assert result.file_count == 3
        assert len(result.documents) == 3

    def test_load_from_inputs_subfolder(self, tmp_path: Path) -> None:
        """Prefers inputs/ subfolder when it exists."""
        # Create inputs subfolder with files
        inputs_dir = tmp_path / "inputs"
        inputs_dir.mkdir()
        (inputs_dir / "input.md").write_text("Input content", encoding="utf-8")
        # Also create file in root
        (tmp_path / "root.md").write_text("Root content", encoding="utf-8")

        skill = LoadDocumentsSkill()
        ctx = SkillContext(workspace_path=tmp_path)
        input_data = LoadDocumentsInput(patterns=["**/*.md"], max_files=10)

        result = skill.execute(input_data, ctx)

        # Should only find file in inputs/
        assert result.success is True
        assert result.file_count == 1
        assert result.documents[0].path == "input.md"

    def test_fails_without_workspace(self) -> None:
        """Fails gracefully when no workspace provided."""
        skill = LoadDocumentsSkill()
        ctx = SkillContext(workspace_path=None)
        input_data = LoadDocumentsInput()

        result = skill.execute(input_data, ctx)

        assert result.success is False
        assert result.error == "missing_workspace_path"

    def test_fails_with_nonexistent_workspace(self, tmp_path: Path) -> None:
        """Fails gracefully when workspace doesn't exist."""
        skill = LoadDocumentsSkill()
        ctx = SkillContext(workspace_path=tmp_path / "nonexistent")
        input_data = LoadDocumentsInput()

        result = skill.execute(input_data, ctx)

        assert result.success is False
        assert result.error == "workspace_not_found"

    def test_fails_with_no_matching_files(self, tmp_path: Path) -> None:
        """Fails gracefully when no files match pattern or fallback."""
        # Create a binary-like file that won't match any text patterns
        (tmp_path / "data.bin").write_bytes(b"\x00\x01\x02")

        skill = LoadDocumentsSkill()
        ctx = SkillContext(workspace_path=tmp_path)
        # Use the fallback patterns themselves so no retry is triggered
        input_data = LoadDocumentsInput(patterns=["**/*.md", "**/*.txt"])

        result = skill.execute(input_data, ctx)

        assert result.success is False
        assert result.error == "no_files_found"

    def test_fallback_patterns_when_primary_finds_nothing(self, tmp_path: Path) -> None:
        """Falls back to default patterns when user patterns find nothing (AF-0107)."""
        # Only .md files exist, but planner asks for *.pdf
        (tmp_path / "readme.md").write_text("# Hello", encoding="utf-8")

        skill = LoadDocumentsSkill()
        ctx = SkillContext(workspace_path=tmp_path)
        input_data = LoadDocumentsInput(patterns=["**/*.pdf"])

        result = skill.execute(input_data, ctx)

        assert result.success is True
        assert result.file_count == 1
        assert result.documents[0].path == "readme.md"

    def test_no_fallback_when_primary_patterns_match(self, tmp_path: Path) -> None:
        """Fallback is not used when primary patterns find files."""
        (tmp_path / "readme.md").write_text("# Hello", encoding="utf-8")
        (tmp_path / "notes.txt").write_text("notes", encoding="utf-8")

        skill = LoadDocumentsSkill()
        ctx = SkillContext(workspace_path=tmp_path)
        input_data = LoadDocumentsInput(patterns=["**/*.txt"])

        result = skill.execute(input_data, ctx)

        assert result.success is True
        assert result.file_count == 1
        assert result.documents[0].path == "notes.txt"

    def test_document_schema(self, tmp_path: Path) -> None:
        """Documents have correct schema."""
        (tmp_path / "test.md").write_text("Hello World", encoding="utf-8")

        skill = LoadDocumentsSkill()
        ctx = SkillContext(workspace_path=tmp_path)
        input_data = LoadDocumentsInput()

        result = skill.execute(input_data, ctx)

        assert result.success is True
        doc = result.documents[0]
        assert doc.path == "test.md"
        assert doc.content == "Hello World"
        assert doc.size_bytes == len("Hello World".encode("utf-8"))


# ---------------------------------------------------------------------------
# EmitResultSkill Tests
# ---------------------------------------------------------------------------


class TestEmitResultSkill:
    """Tests for emit_result skill."""

    def test_skill_metadata(self) -> None:
        """Skill has correct metadata."""
        skill = EmitResultSkill()
        assert skill.name == "emit_result"
        assert skill.requires_llm is False
        assert skill.input_schema == EmitResultInput
        assert skill.output_schema == EmitResultOutput

    def test_emits_artifact_to_workspace(self, tmp_path: Path) -> None:
        """Successfully emits artifact to workspace."""
        skill = EmitResultSkill()
        ctx = SkillContext(workspace_path=tmp_path, run_id="test-run-123")
        input_data = EmitResultInput(
            document_summary="Test summary",
            key_points=["point 1"],
            artifact_name="result.json",
        )

        result = skill.execute(input_data, ctx)

        assert result.success is True
        assert result.bytes_written > 0
        assert "result.json" in result.artifact_path
        assert result.artifact_id.startswith("art-")

        # Verify file was created
        artifact_path = tmp_path / result.artifact_path
        assert artifact_path.exists()

        # Verify content
        content = json.loads(artifact_path.read_text())
        assert content["summary"] == "Test summary"
        assert content["run_id"] == "test-run-123"

    def test_creates_run_directory(self, tmp_path: Path) -> None:
        """Creates run directory if it doesn't exist."""
        skill = EmitResultSkill()
        ctx = SkillContext(workspace_path=tmp_path, run_id="new-run-456")
        input_data = EmitResultInput(document_summary="test")

        result = skill.execute(input_data, ctx)

        assert result.success is True
        assert (tmp_path / "runs" / "new-run-456").exists()

    def test_uses_artifacts_dir_without_run_id(self, tmp_path: Path) -> None:
        """Uses artifacts dir when no run_id provided."""
        skill = EmitResultSkill()
        ctx = SkillContext(workspace_path=tmp_path, run_id=None)
        input_data = EmitResultInput(document_summary="test")

        result = skill.execute(input_data, ctx)

        assert result.success is True
        # Use Path parts to avoid Windows/Unix path separator issues
        assert "artifacts" in result.artifact_path

    def test_fails_without_workspace(self) -> None:
        """Fails gracefully when no workspace provided."""
        skill = EmitResultSkill()
        ctx = SkillContext(workspace_path=None)
        input_data = EmitResultInput(document_summary="test")

        result = skill.execute(input_data, ctx)

        assert result.success is False
        assert result.error == "missing_workspace_path"

    def test_custom_artifact_name(self, tmp_path: Path) -> None:
        """Uses custom artifact name."""
        skill = EmitResultSkill()
        ctx = SkillContext(workspace_path=tmp_path, run_id="run-1")
        input_data = EmitResultInput(
            document_summary="value",
            artifact_name="custom-output.json",
        )

        result = skill.execute(input_data, ctx)

        assert result.success is True
        assert "custom-output.json" in result.artifact_path

    def test_artifact_metadata(self, tmp_path: Path) -> None:
        """Artifact contains proper metadata (JSON format)."""
        skill = EmitResultSkill()
        ctx = SkillContext(
            workspace_path=tmp_path,
            run_id="meta-run",
            step_number=2,
        )
        input_data = EmitResultInput(
            document_summary="test result",
            key_points=["point 1", "point 2"],
            sources=["file1.md"],
            artifact_name="metadata.json",  # Explicit JSON for this test
        )

        result = skill.execute(input_data, ctx)

        artifact_path = tmp_path / result.artifact_path
        content = json.loads(artifact_path.read_text())

        assert content["artifact_id"] == result.artifact_id
        assert content["run_id"] == "meta-run"
        assert content["step_number"] == 2
        assert content["summary"] == "test result"
        assert content["key_points"] == ["point 1", "point 2"]
        assert "created_at" in content

    def test_markdown_output_format(self, tmp_path: Path) -> None:
        """AF-0089: .md artifact writes markdown, not JSON."""
        skill = EmitResultSkill()
        ctx = SkillContext(
            workspace_path=tmp_path,
            run_id="md-run",
            step_number=1,
        )
        input_data = EmitResultInput(
            document_summary="This is the summary.",
            key_points=["First point", "Second point"],
            sources=["source1.txt", "source2.txt"],
            artifact_name="research_report.md",
        )

        result = skill.execute(input_data, ctx)

        assert result.success is True
        artifact_path = tmp_path / result.artifact_path
        content = artifact_path.read_text(encoding="utf-8")

        # Should be markdown, not JSON
        assert not content.startswith("{")
        assert "# Research Report" in content
        assert "## Summary" in content
        assert "This is the summary." in content
        assert "## Key Findings" in content
        assert "- First point" in content
        assert "- Second point" in content
        assert "## Sources" in content
        # AF-0082: Sources now in table format
        assert "| 1 | source1.txt |" in content
        assert "| 2 | source2.txt |" in content
        # Should have artifact_id in comment for traceability
        assert f"artifact_id: {result.artifact_id}" in content

    def test_json_output_for_json_extension(self, tmp_path: Path) -> None:
        """AF-0089: .json artifact writes JSON as expected."""
        skill = EmitResultSkill()
        ctx = SkillContext(workspace_path=tmp_path, run_id="json-run")
        input_data = EmitResultInput(
            document_summary="test",
            artifact_name="result.json",
        )

        result = skill.execute(input_data, ctx)

        artifact_path = tmp_path / result.artifact_path
        content = artifact_path.read_text(encoding="utf-8")

        # Should be valid JSON
        data = json.loads(content)
        assert data["summary"] == "test"

    def test_artifact_type_mime_for_markdown(self, tmp_path: Path) -> None:
        """AF-0089: artifact_type is text/markdown for .md files."""
        skill = EmitResultSkill()
        ctx = SkillContext(workspace_path=tmp_path, run_id="mime-md")
        input_data = EmitResultInput(
            document_summary="test",
            artifact_name="report.md",
        )

        result = skill.execute(input_data, ctx)

        assert result.success is True
        assert result.artifact_type == "text/markdown"

    def test_artifact_type_mime_for_json(self, tmp_path: Path) -> None:
        """AF-0089: artifact_type is application/json for .json files."""
        skill = EmitResultSkill()
        ctx = SkillContext(workspace_path=tmp_path, run_id="mime-json")
        input_data = EmitResultInput(
            document_summary="test",
            artifact_name="result.json",
        )

        result = skill.execute(input_data, ctx)

        assert result.success is True
        assert result.artifact_type == "application/json"

    def test_markdown_with_trace_metadata(self, tmp_path: Path) -> None:
        """AF-0082: Markdown report includes trace metadata when provided."""
        skill = EmitResultSkill()
        ctx = SkillContext(
            workspace_path=tmp_path,
            run_id="trace-md-run",
            step_number=3,
            trace_metadata={
                "elapsed_ms": 5500,
                "model": "gpt-4o-mini",
                "playbook_name": "research_v0",
                "playbook_version": "1.1.0",
                "steps_summary": [
                    {
                        "skill": "load_documents",
                        "duration_ms": 50,
                        "output_summary": "Loaded 2 docs",
                    },
                    {
                        "skill": "web_search",
                        "duration_ms": 1200,
                        "output_summary": "Found 5 URLs",
                    },
                    {
                        "skill": "fetch_web_content",
                        "duration_ms": 3500,
                        "output_summary": "Fetched 4/5",
                    },
                ],
            },
        )
        input_data = EmitResultInput(
            document_summary="Test summary content.",
            key_points=["Finding 1"],
            sources=["https://example.com/page1", "local_file.txt"],
            artifact_name="report.md",
        )

        result = skill.execute(input_data, ctx)

        assert result.success is True
        content = (tmp_path / result.artifact_path).read_text(encoding="utf-8")

        # Check metadata header
        assert "**Duration:** 5.5 seconds" in content
        assert "**Model:** gpt-4o-mini" in content
        assert "**Playbook:** research_v0@1.1.0" in content

        # Check sources with clickable links for URLs
        assert "[example.com/page1" in content  # URL should be linkified
        assert "](https://example.com/page1)" in content
        assert "local_file.txt" in content  # Non-URL stays plain

        # Check execution details table
        assert "## Execution Details" in content
        assert "| Step | Skill | Duration | Output |" in content
        assert "load_documents" in content
        assert "web_search" in content
        assert "fetch_web_content" in content
        assert "**Run ID:** `trace-md-run`" in content

    def test_markdown_without_trace_metadata(self, tmp_path: Path) -> None:
        """AF-0082: Markdown report works without trace_metadata (backwards compat)."""
        skill = EmitResultSkill()
        ctx = SkillContext(
            workspace_path=tmp_path,
            run_id="no-trace-run",
            step_number=1,
            # trace_metadata not provided
        )
        input_data = EmitResultInput(
            document_summary="Simple summary.",
            artifact_name="simple.md",
        )

        result = skill.execute(input_data, ctx)

        assert result.success is True
        content = (tmp_path / result.artifact_path).read_text(encoding="utf-8")

        # Basic structure should still work
        assert "# Research Report" in content
        assert "Simple summary." in content
        # No execution details table without trace_metadata
        assert "## Execution Details" not in content


# ---------------------------------------------------------------------------
# Integration Tests
# ---------------------------------------------------------------------------


class TestSummarizeV0Pipeline:
    """Integration tests for the complete summarize_v0 pipeline."""

    def test_full_pipeline_flow(self, tmp_path: Path) -> None:
        """Test documents flow through all three skills (AF-0108: uses synthesize_research)."""
        from ag.core.runtime import _adapt_document_to_source
        from ag.skills.synthesize_research import (
            SynthesizeResearchInput,
            SynthesizeResearchSkill,
        )

        # Setup: Create input files
        (tmp_path / "doc1.md").write_text("# Overview\nThis is content.", encoding="utf-8")
        (tmp_path / "doc2.md").write_text("# Details\nMore content here.", encoding="utf-8")

        # Step 1: Load documents
        load_skill = LoadDocumentsSkill()
        load_ctx = SkillContext(workspace_path=tmp_path)
        load_input = LoadDocumentsInput(patterns=["**/*.md"])
        load_result = load_skill.execute(load_input, load_ctx)

        assert load_result.success is True
        assert load_result.file_count == 2

        # Step 2: Synthesize (fallback mode - no LLM)
        # AF-0108: Use conversion adapter for Document → SourceDocument
        source_docs = [
            _adapt_document_to_source(doc.model_dump())
            for doc in load_result.documents
        ]
        synth_skill = SynthesizeResearchSkill()
        synth_ctx = SkillContext(provider=None)
        synth_input = SynthesizeResearchInput(
            documents=source_docs,
            prompt="Summarize the documents",
        )
        synth_result = synth_skill.execute(synth_input, synth_ctx)

        assert synth_result.success is True
        assert synth_result.source_count == 2

        # Step 3: Emit result
        emit_skill = EmitResultSkill()
        emit_ctx = SkillContext(workspace_path=tmp_path, run_id="pipeline-test")
        emit_input = EmitResultInput(
            document_summary=synth_result.report,
            key_points=synth_result.key_findings,
            sources=synth_result.sources_used,
            artifact_name="summary.json",
        )
        emit_result = emit_skill.execute(emit_input, emit_ctx)

        assert emit_result.success is True
        assert emit_result.bytes_written > 0

        # Verify final artifact
        artifact_path = tmp_path / emit_result.artifact_path
        assert artifact_path.exists()
        content = json.loads(artifact_path.read_text())
        assert "summary" in content
        assert len(content["sources"]) == 2


# ---------------------------------------------------------------------------
# Schema Validation Tests
# ---------------------------------------------------------------------------


class TestSchemaValidation:
    """Tests for input/output schema validation."""

    def test_load_documents_input_defaults(self) -> None:
        """LoadDocumentsInput has sensible defaults."""
        input_data = LoadDocumentsInput()
        assert input_data.patterns == ["**/*.md"]
        assert input_data.max_files == 10

    def test_load_documents_input_validation(self) -> None:
        """LoadDocumentsInput validates max_files bounds."""
        with pytest.raises(ValueError):
            LoadDocumentsInput(max_files=0)  # Below minimum
        with pytest.raises(ValueError):
            LoadDocumentsInput(max_files=101)  # Above maximum

    def test_emit_result_input_defaults(self) -> None:
        """EmitResultInput has sensible defaults (Markdown for human readability)."""
        input_data = EmitResultInput()
        assert input_data.document_summary == ""
        assert input_data.key_points == []
        assert input_data.artifact_name == "summary.md"
        assert input_data.artifact_type == "text/markdown"

    def test_document_schema(self) -> None:
        """Document schema works correctly."""
        doc = Document(path="test.md", content="Hello", size_bytes=5)
        assert doc.path == "test.md"
        assert doc.content == "Hello"
        assert doc.size_bytes == 5
