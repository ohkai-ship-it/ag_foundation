"""Tests for AF-0074: Research skills and playbook.

Tests:
- fetch_web_content skill functionality
- synthesize_research skill functionality  
- research_v0 playbook integration
- Registry registration
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from ag.core.playbook import Playbook
from ag.playbooks.registry import get_playbook, list_playbooks
from ag.skills.base import SkillContext
from ag.skills.fetch_web_content import (
    FetchedDocument,
    FetchWebContentInput,
    FetchWebContentOutput,
    FetchWebContentSkill,
)
from ag.skills.registry import create_default_registry
from ag.skills.synthesize_research import (
    SourceDocument,
    SynthesizeResearchInput,
    SynthesizeResearchOutput,
    SynthesizeResearchSkill,
)


# ---------------------------------------------------------------------------
# fetch_web_content tests
# ---------------------------------------------------------------------------


class TestFetchWebContentSkill:
    """Tests for FetchWebContentSkill."""

    def test_skill_metadata(self) -> None:
        """Test skill has correct metadata."""
        skill = FetchWebContentSkill()
        assert skill.name == "fetch_web_content"
        assert skill.description
        assert skill.requires_llm is False

    def test_input_schema(self) -> None:
        """Test input schema validation."""
        inp = FetchWebContentInput(
            urls=["https://example.com", "https://test.org"],
            timeout_seconds=10,
            max_content_length=5000,
        )
        assert len(inp.urls) == 2
        assert inp.timeout_seconds == 10
        assert inp.max_content_length == 5000

    def test_input_defaults(self) -> None:
        """Test input uses sensible defaults."""
        inp = FetchWebContentInput(urls=["https://example.com"])
        assert inp.timeout_seconds == 30
        assert inp.max_content_length == 100000  # DEFAULT_MAX_CONTENT_LENGTH

    def test_output_schema(self) -> None:
        """Test output schema structure."""
        doc = FetchedDocument(
            url="https://example.com",
            content="test content",
            content_type="text/html",
            status_code=200,
            error=None,
        )
        output = FetchWebContentOutput(
            success=True,
            summary="Fetched 1 document",
            documents=[doc],
            failed_urls=[],
        )
        assert output.success is True
        assert len(output.documents) == 1
        assert output.documents[0].url == "https://example.com"

    def test_fetched_document_with_error(self) -> None:
        """Test FetchedDocument with error state."""
        doc = FetchedDocument(
            url="https://invalid.example",
            content="",
            content_type="",
            status_code=0,
            error="Connection timeout",
        )
        assert doc.error == "Connection timeout"
        assert doc.status_code == 0

    @patch("ag.skills.fetch_web_content._fetch_url_sync")
    def test_execute_success(self, mock_fetch: MagicMock) -> None:
        """Test successful URL fetch."""
        mock_fetch.return_value = FetchedDocument(
            url="https://example.com",
            content="Hello World",
            content_type="text/plain",
            status_code=200,
            error=None,
        )

        skill = FetchWebContentSkill()
        ctx = SkillContext(
            workspace_path=".",
            run_id="test-run",
            provider=None,
        )

        inp = FetchWebContentInput(urls=["https://example.com"])
        output = skill.execute(inp, ctx)

        assert output.success is True
        assert len(output.documents) == 1
        assert output.documents[0].content == "Hello World"
        mock_fetch.assert_called_once()

    @patch("ag.skills.fetch_web_content._fetch_url_sync")
    def test_execute_with_failure(self, mock_fetch: MagicMock) -> None:
        """Test URL fetch with failure."""
        mock_fetch.return_value = FetchedDocument(
            url="https://bad.example",
            content="",
            content_type="",
            status_code=0,
            error="Connection refused",
        )

        skill = FetchWebContentSkill()
        ctx = SkillContext(
            workspace_path=".",
            run_id="test-run",
            provider=None,
        )

        inp = FetchWebContentInput(urls=["https://bad.example"])
        output = skill.execute(inp, ctx)

        # All URLs failed, so success is False
        assert output.success is False
        assert len(output.failed_urls) == 1
        assert "bad.example" in output.failed_urls[0]

    @patch("ag.skills.fetch_web_content._fetch_url_sync")
    def test_execute_multiple_urls(self, mock_fetch: MagicMock) -> None:
        """Test fetching multiple URLs."""
        mock_fetch.side_effect = [
            FetchedDocument(
                url="https://example1.com",
                content="Content 1",
                content_type="text/plain",
                status_code=200,
                error=None,
            ),
            FetchedDocument(
                url="https://example2.com",
                content="",
                content_type="",
                status_code=0,
                error="Timeout",
            ),
        ]

        skill = FetchWebContentSkill()
        ctx = SkillContext(
            workspace_path=".",
            run_id="test-run",
            provider=None,
        )

        inp = FetchWebContentInput(
            urls=["https://example1.com", "https://example2.com"]
        )
        output = skill.execute(inp, ctx)

        assert output.success is True  # At least one succeeded
        assert len(output.documents) == 2
        assert len(output.failed_urls) == 1
        assert mock_fetch.call_count == 2


# ---------------------------------------------------------------------------
# synthesize_research tests
# ---------------------------------------------------------------------------


class TestSynthesizeResearchSkill:
    """Tests for SynthesizeResearchSkill."""

    def test_skill_metadata(self) -> None:
        """Test skill has correct metadata."""
        skill = SynthesizeResearchSkill()
        assert skill.name == "synthesize_research"
        assert skill.description
        assert skill.requires_llm is True

    def test_input_schema(self) -> None:
        """Test input schema validation."""
        doc = SourceDocument(
            source="https://example.com",
            content="Some research content",
            source_type="web",
        )
        inp = SynthesizeResearchInput(
            documents=[doc],
            output_format="markdown",
            include_citations=True,
        )
        assert len(inp.documents) == 1
        assert inp.output_format == "markdown"
        assert inp.include_citations is True

    def test_input_defaults(self) -> None:
        """Test input uses sensible defaults."""
        inp = SynthesizeResearchInput(documents=[])
        assert inp.output_format == "markdown"
        assert inp.max_tokens == 4000
        assert inp.include_citations is True

    def test_output_schema(self) -> None:
        """Test output schema structure."""
        output = SynthesizeResearchOutput(
            success=True,
            summary="Synthesis complete",
            report="This is the synthesized research...",
            key_findings=["Finding 1", "Finding 2"],
            sources_used=["https://example.com"],
        )
        assert output.success is True
        assert len(output.key_findings) == 2
        assert len(output.sources_used) == 1
        assert output.report == "This is the synthesized research..."

    def test_source_document_types(self) -> None:
        """Test SourceDocument with different source types."""
        web_doc = SourceDocument(
            source="https://example.com",
            content="Web content",
            source_type="web",
        )
        file_doc = SourceDocument(
            source="docs/readme.md",
            content="File content",
            source_type="file",
        )
        assert web_doc.source_type == "web"
        assert file_doc.source_type == "file"

    def test_execute_with_mock_llm(self) -> None:
        """Test synthesis with mocked LLM provider."""
        # Mock provider - chat returns dict with "content" key
        mock_provider = MagicMock()
        mock_provider.chat.return_value = {
            "content": """
# Research Report

Based on the research, AI models are advancing rapidly.

## Key Findings
- LLMs have improved significantly
- Multimodal capabilities are expanding

## Sources
- https://example.com
"""
        }

        skill = SynthesizeResearchSkill()
        ctx = SkillContext(
            workspace_path=".",
            run_id="test-run",
            provider=mock_provider,
        )

        doc = SourceDocument(
            source="https://example.com",
            content="AI models are advancing rapidly with new capabilities.",
            source_type="web",
        )
        inp = SynthesizeResearchInput(
            documents=[doc],
            output_format="markdown",
        )

        output = skill.execute(inp, ctx)

        assert output.success is True
        assert output.report  # Has content
        mock_provider.chat.assert_called_once()


# ---------------------------------------------------------------------------
# research_v0 playbook tests
# ---------------------------------------------------------------------------


class TestResearchV0Playbook:
    """Tests for research_v0 playbook."""

    def test_playbook_registered(self) -> None:
        """Test playbook is in registry."""
        assert "research_v0" in list_playbooks()

    def test_playbook_alias(self) -> None:
        """Test playbook has 'research' alias."""
        playbook = get_playbook("research")
        assert playbook is not None
        assert playbook.name == "research_v0"

    def test_playbook_structure(self) -> None:
        """Test playbook has correct structure."""
        playbook = get_playbook("research_v0")
        assert playbook is not None
        assert isinstance(playbook, Playbook)
        assert playbook.name == "research_v0"
        assert len(playbook.steps) >= 3  # At least load, synthesize, emit

    def test_playbook_metadata(self) -> None:
        """Test playbook has correct metadata."""
        playbook = get_playbook("research_v0")
        assert playbook is not None
        assert playbook.metadata
        assert playbook.metadata.get("stability") == "experimental"
        assert playbook.metadata.get("af_item") == "AF-0074"

    def test_playbook_steps(self) -> None:
        """Test playbook has expected steps."""
        playbook = get_playbook("research_v0")
        assert playbook is not None

        step_names = [s.name for s in playbook.steps]
        # Should have synthesize and emit at minimum
        assert any("synthesize" in name for name in step_names)
        assert any("emit" in name for name in step_names)


# ---------------------------------------------------------------------------
# Registry integration tests
# ---------------------------------------------------------------------------


class TestResearchRegistration:
    """Tests for research skill/playbook registration."""

    def test_skills_registered(self) -> None:
        """Test new skills are in default registry."""
        registry = create_default_registry()
        skill_names = registry.list_skills()

        assert "fetch_web_content" in skill_names
        assert "synthesize_research" in skill_names

    def test_skill_info_available(self) -> None:
        """Test skill info is accessible."""
        registry = create_default_registry()

        fetch_info = registry.get_info("fetch_web_content")
        assert fetch_info is not None
        assert fetch_info["requires_llm"] is False

        synth_info = registry.get_info("synthesize_research")
        assert synth_info is not None
        assert synth_info["requires_llm"] is True

    def test_fetch_execution_via_registry(self) -> None:
        """Test fetch_web_content can be executed through registry."""
        registry = create_default_registry()
        ctx = SkillContext(
            workspace_path=".",
            run_id="test-run",
            provider=None,
        )

        # Execute fetch_web_content with empty URLs (doesn't need provider)
        success, summary, data = registry.execute(
            "fetch_web_content",
            {"urls": []},
            ctx,
        )

        assert success is True


# ---------------------------------------------------------------------------
# Edge cases and error handling
# ---------------------------------------------------------------------------


class TestResearchEdgeCases:
    """Edge case tests for research skills."""

    def test_fetch_empty_urls(self) -> None:
        """Test fetch with empty URL list."""
        skill = FetchWebContentSkill()
        ctx = SkillContext(
            workspace_path=".",
            run_id="test-run",
            provider=None,
        )

        inp = FetchWebContentInput(urls=[])
        output = skill.execute(inp, ctx)

        assert output.success is True
        assert len(output.documents) == 0

    def test_synthesize_requires_provider(self) -> None:
        """Test synthesis requires LLM provider."""
        registry = create_default_registry()
        ctx = SkillContext(
            workspace_path=".",
            run_id="test-run",
            provider=None,
        )

        # Without provider, should fail validation
        success, summary, data = registry.execute(
            "synthesize_research",
            {"documents": []},
            ctx,
        )

        # Should fail because requires_llm is True
        assert success is False
        assert "requires" in summary.lower() or "llm" in summary.lower()

    def test_output_formats(self) -> None:
        """Test different output formats are accepted."""
        for fmt in ["markdown", "plain", "json"]:
            inp = SynthesizeResearchInput(
                documents=[],
                output_format=fmt,
            )
            assert inp.output_format == fmt
