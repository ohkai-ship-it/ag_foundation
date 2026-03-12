"""Tests for AF-0074: Research skills and playbook.

Tests:
- fetch_web_content skill functionality
- synthesize_research skill functionality
- research_v0 playbook integration
- Registry registration
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

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

        inp = FetchWebContentInput(urls=["https://example1.com", "https://example2.com"])
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
        # AF-0080 changed af_item to af_items (list) to track multiple items
        af_items = playbook.metadata.get("af_items", [])
        assert "AF-0074" in af_items
        assert "AF-0080" in af_items

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

    def test_synthesize_accepts_fetched_documents(self) -> None:
        """Test synthesize accepts FetchedDocument format from pipeline."""
        # Simulate pipeline data from fetch_web_content
        fetched_docs = [
            {
                "url": "https://example.com/article",
                "content": "Article content here",
                "status_code": 200,
                "content_type": "text/html",
                "title": "Example Article",
                "error": None,
            },
            {
                "url": "https://test.org/page",
                "content": "Page content",
                "status_code": 200,
                "content_type": "text/html",
                "title": None,
                "error": None,
            },
        ]

        # Should convert FetchedDocument dicts to SourceDocument
        inp = SynthesizeResearchInput(
            documents=fetched_docs,
            output_format="markdown",
        )

        assert len(inp.documents) == 2
        assert inp.documents[0].source == "https://example.com/article"
        assert inp.documents[0].content == "Article content here"
        assert inp.documents[0].source_type == "url"
        assert inp.documents[0].title == "Example Article"

    def test_synthesize_accepts_loaded_documents(self) -> None:
        """Test synthesize accepts Document format from load_documents."""
        # Simulate pipeline data from load_documents
        loaded_docs = [
            {
                "path": "docs/readme.md",
                "content": "# README\nThis is a readme file.",
                "size_bytes": 30,
            },
        ]

        inp = SynthesizeResearchInput(
            documents=loaded_docs,
            output_format="markdown",
        )

        assert len(inp.documents) == 1
        assert inp.documents[0].source == "docs/readme.md"
        assert inp.documents[0].source_type == "file"

    def test_synthesize_ignores_extra_pipeline_fields(self) -> None:
        """Test synthesize ignores extra fields from pipeline (e.g., failed_urls)."""
        # Simulate full pipeline output from fetch_web_content
        pipeline_data = {
            "documents": [
                {
                    "url": "https://example.com",
                    "content": "Content",
                    "status_code": 200,
                    "content_type": "text/html",
                    "title": "Example",
                    "error": None,
                }
            ],
            "failed_urls": ["https://bad.example"],  # Extra field
            "total_fetched": 1,  # Extra field
            "total_failed": 1,  # Extra field
            "error": None,  # Extra field
        }

        # Should not raise ValidationError for extra fields
        inp = SynthesizeResearchInput(**pipeline_data)
        assert len(inp.documents) == 1

    def test_fetch_urls_from_file(self, tmp_path) -> None:
        """Test loading URLs from a file in workspace."""
        from ag.skills.fetch_web_content import _load_urls_from_file

        # Create urls file
        inputs_dir = tmp_path / "inputs"
        inputs_dir.mkdir()
        urls_file = inputs_dir / "urls.txt"
        urls_file.write_text(
            """# This is a comment
https://example.com
https://test.org/page

# Another comment
https://api.example.com/data
"""
        )

        urls = _load_urls_from_file(str(tmp_path), "inputs/urls.txt")

        assert len(urls) == 3
        assert "https://example.com" in urls
        assert "https://test.org/page" in urls
        assert "https://api.example.com/data" in urls

    def test_fetch_urls_from_missing_file(self, tmp_path) -> None:
        """Test loading URLs from non-existent file returns empty list."""
        from ag.skills.fetch_web_content import _load_urls_from_file

        urls = _load_urls_from_file(str(tmp_path), "inputs/urls.txt")
        assert urls == []

    def test_fetch_urls_file_integration(self, tmp_path) -> None:
        """Test fetch_web_content reads from file when urls not provided."""
        # Create urls file with a URL
        inputs_dir = tmp_path / "inputs"
        inputs_dir.mkdir()
        urls_file = inputs_dir / "urls.txt"
        urls_file.write_text("https://example.com\n")

        skill = FetchWebContentSkill()
        ctx = SkillContext(
            workspace_path=str(tmp_path),
            run_id="test-run",
            provider=None,
        )

        # No URLs in input - should load from file
        inp = FetchWebContentInput(urls=[])

        with patch("ag.skills.fetch_web_content._fetch_url_sync") as mock_fetch:
            mock_fetch.return_value = FetchedDocument(
                url="https://example.com",
                content="Test content",
                content_type="text/html",
                status_code=200,
                error=None,
            )

            output = skill.execute(inp, ctx)

            # Should have fetched the URL from the file
            assert output.total_fetched == 1
            assert mock_fetch.called
            mock_fetch.assert_called_once()


# ---------------------------------------------------------------------------
# AF-0093: Additional coverage tests for fetch_web_content
# ---------------------------------------------------------------------------


class TestExtractTextFromHtml:
    """Tests for _extract_text_from_html helper function."""

    def test_extracts_title_from_html(self) -> None:
        """Test title extraction from HTML."""
        from ag.skills.fetch_web_content import _extract_text_from_html

        html = "<html><head><title>Test Page</title></head><body>Content</body></html>"
        text, title = _extract_text_from_html(html, 1000)

        assert title == "Test Page"
        assert "Content" in text

    def test_extracts_title_case_insensitive(self) -> None:
        """Test title tag matching is case-insensitive."""
        from ag.skills.fetch_web_content import _extract_text_from_html

        html = "<html><HEAD><TITLE>Upper Case</TITLE></HEAD><body>Body</body></html>"
        text, title = _extract_text_from_html(html, 1000)

        assert title == "Upper Case"

    def test_returns_none_title_when_missing(self) -> None:
        """Test returns None when no title tag present."""
        from ag.skills.fetch_web_content import _extract_text_from_html

        html = "<html><body>No title here</body></html>"
        text, title = _extract_text_from_html(html, 1000)

        assert title is None
        assert "No title here" in text

    def test_removes_script_tags(self) -> None:
        """Test script tags and content are removed."""
        from ag.skills.fetch_web_content import _extract_text_from_html

        html = """<html><body>
            <p>Visible text</p>
            <script>alert('hidden');</script>
            <p>More visible</p>
        </body></html>"""
        text, _ = _extract_text_from_html(html, 1000)

        assert "Visible text" in text
        assert "More visible" in text
        assert "alert" not in text
        assert "hidden" not in text

    def test_removes_style_tags(self) -> None:
        """Test style tags and content are removed."""
        from ag.skills.fetch_web_content import _extract_text_from_html

        html = """<html><head>
            <style>.hidden { display: none; }</style>
        </head><body>
            <p>Visible content</p>
        </body></html>"""
        text, _ = _extract_text_from_html(html, 1000)

        assert "Visible content" in text
        assert "display" not in text
        assert ".hidden" not in text

    def test_removes_html_comments(self) -> None:
        """Test HTML comments are removed."""
        from ag.skills.fetch_web_content import _extract_text_from_html

        html = "<html><body><!-- secret comment -->Visible</body></html>"
        text, _ = _extract_text_from_html(html, 1000)

        assert "Visible" in text
        assert "secret" not in text
        assert "comment" not in text

    def test_decodes_html_entities(self) -> None:
        """Test common HTML entities are decoded."""
        from ag.skills.fetch_web_content import _extract_text_from_html

        html = (
            "<html><body>Tom &amp; Jerry &lt;3 &gt; "
            "&quot;quotes&quot; &#39;apos&#39;</body></html>"
        )
        text, _ = _extract_text_from_html(html, 1000)

        assert "Tom & Jerry" in text
        assert "<3" in text
        assert '"quotes"' in text
        assert "'apos'" in text

    def test_nbsp_replaced_with_space(self) -> None:
        """Test &nbsp; is replaced with regular space."""
        from ag.skills.fetch_web_content import _extract_text_from_html

        html = "<html><body>word1&nbsp;&nbsp;word2</body></html>"
        text, _ = _extract_text_from_html(html, 1000)

        assert "word1" in text
        assert "word2" in text
        # Whitespace should be normalized
        assert "&nbsp;" not in text

    def test_normalizes_whitespace(self) -> None:
        """Test excessive whitespace is normalized."""
        from ag.skills.fetch_web_content import _extract_text_from_html

        html = "<html><body>word1    \n\n\t  word2</body></html>"
        text, _ = _extract_text_from_html(html, 1000)

        assert text == "word1 word2"

    def test_truncates_long_content(self) -> None:
        """Test content is truncated at max_length."""
        from ag.skills.fetch_web_content import _extract_text_from_html

        html = "<html><body>" + "x" * 1000 + "</body></html>"
        text, _ = _extract_text_from_html(html, 100)

        assert len(text) < 150  # 100 + "... [truncated]"
        assert text.endswith("... [truncated]")

    def test_removes_all_html_tags(self) -> None:
        """Test all HTML tags are stripped."""
        from ag.skills.fetch_web_content import _extract_text_from_html

        html = """<html><body>
            <div class="wrapper">
                <h1>Header</h1>
                <p>Paragraph with <strong>bold</strong> and <em>italic</em>.</p>
                <a href="http://example.com">Link</a>
            </div>
        </body></html>"""
        text, _ = _extract_text_from_html(html, 1000)

        assert "Header" in text
        assert "Paragraph" in text
        assert "bold" in text
        assert "Link" in text
        assert "<" not in text
        assert ">" not in text
        assert "href" not in text


class TestFetchWebContentErrorPaths:
    """Tests for fetch_web_content error handling paths."""

    @patch("ag.skills.fetch_web_content._fetch_url_sync")
    def test_handles_timeout_error(self, mock_fetch: MagicMock) -> None:
        """Test timeout errors are captured gracefully."""
        mock_fetch.return_value = FetchedDocument(
            url="https://slow.example",
            content="",
            content_type="",
            status_code=0,
            error="ReadTimeout: Connection timed out after 30s",
        )

        skill = FetchWebContentSkill()
        ctx = SkillContext(workspace_path=".", run_id="test", provider=None)
        inp = FetchWebContentInput(urls=["https://slow.example"], timeout_seconds=30)

        output = skill.execute(inp, ctx)

        assert output.success is False
        assert "https://slow.example" in output.failed_urls

    @patch("ag.skills.fetch_web_content._fetch_url_sync")
    def test_handles_connection_refused(self, mock_fetch: MagicMock) -> None:
        """Test connection refused errors."""
        mock_fetch.return_value = FetchedDocument(
            url="https://down.example",
            content="",
            content_type="",
            status_code=0,
            error="ConnectError: Connection refused",
        )

        skill = FetchWebContentSkill()
        ctx = SkillContext(workspace_path=".", run_id="test", provider=None)
        inp = FetchWebContentInput(urls=["https://down.example"])

        output = skill.execute(inp, ctx)

        assert output.success is False
        assert len(output.failed_urls) == 1

    @patch("ag.skills.fetch_web_content._fetch_url_sync")
    def test_handles_http_404(self, mock_fetch: MagicMock) -> None:
        """Test 404 responses are captured with content still extracted."""
        mock_fetch.return_value = FetchedDocument(
            url="https://example.com/missing",
            content="Page not found",
            content_type="text/html",
            status_code=404,
            error="HTTP 404",
        )

        skill = FetchWebContentSkill()
        ctx = SkillContext(workspace_path=".", run_id="test", provider=None)
        inp = FetchWebContentInput(urls=["https://example.com/missing"])

        output = skill.execute(inp, ctx)

        # Has error, so counts as failed
        assert "missing" in output.failed_urls[0]
        # But document is still recorded
        assert len(output.documents) == 1
        assert output.documents[0].status_code == 404

    @patch("ag.skills.fetch_web_content._fetch_url_sync")
    def test_handles_http_500(self, mock_fetch: MagicMock) -> None:
        """Test 500 server errors."""
        mock_fetch.return_value = FetchedDocument(
            url="https://broken.example",
            content="Internal Server Error",
            content_type="text/html",
            status_code=500,
            error="HTTP 500",
        )

        skill = FetchWebContentSkill()
        ctx = SkillContext(workspace_path=".", run_id="test", provider=None)
        inp = FetchWebContentInput(urls=["https://broken.example"])

        output = skill.execute(inp, ctx)

        assert len(output.failed_urls) == 1
        assert output.documents[0].error == "HTTP 500"

    @patch("ag.skills.fetch_web_content._fetch_url_sync")
    def test_handles_non_text_content_type(self, mock_fetch: MagicMock) -> None:
        """Test non-text content types are handled."""
        mock_fetch.return_value = FetchedDocument(
            url="https://example.com/image.png",
            content="",
            content_type="image/png",
            status_code=200,
            error="Non-text content type: image/png",
        )

        skill = FetchWebContentSkill()
        ctx = SkillContext(workspace_path=".", run_id="test", provider=None)
        inp = FetchWebContentInput(urls=["https://example.com/image.png"])

        output = skill.execute(inp, ctx)

        assert output.documents[0].error is not None
        assert "image/png" in output.documents[0].error

    @patch("ag.skills.fetch_web_content._fetch_url_sync")
    def test_handles_json_content_type(self, mock_fetch: MagicMock) -> None:
        """Test JSON content is handled as text."""
        mock_fetch.return_value = FetchedDocument(
            url="https://api.example.com/data",
            content='{"key": "value"}',
            content_type="application/json",
            status_code=200,
            error=None,
        )

        skill = FetchWebContentSkill()
        ctx = SkillContext(workspace_path=".", run_id="test", provider=None)
        inp = FetchWebContentInput(urls=["https://api.example.com/data"])

        output = skill.execute(inp, ctx)

        assert output.success is True
        assert '{"key": "value"}' in output.documents[0].content

    @patch("ag.skills.fetch_web_content._fetch_url_sync")
    def test_partial_success_with_mixed_results(self, mock_fetch: MagicMock) -> None:
        """Test mixed success/failure URLs."""
        mock_fetch.side_effect = [
            FetchedDocument(
                url="https://good1.com",
                content="Good content 1",
                content_type="text/html",
                status_code=200,
                error=None,
            ),
            FetchedDocument(
                url="https://bad.com",
                content="",
                content_type="",
                status_code=0,
                error="Connection failed",
            ),
            FetchedDocument(
                url="https://good2.com",
                content="Good content 2",
                content_type="text/html",
                status_code=200,
                error=None,
            ),
        ]

        skill = FetchWebContentSkill()
        ctx = SkillContext(workspace_path=".", run_id="test", provider=None)
        inp = FetchWebContentInput(
            urls=["https://good1.com", "https://bad.com", "https://good2.com"]
        )

        output = skill.execute(inp, ctx)

        assert output.success is True  # At least one succeeded
        assert output.total_fetched == 2
        assert output.total_failed == 1
        assert len(output.failed_urls) == 1
        assert "bad.com" in output.failed_urls[0]


class TestFetchUrlSyncFunction:
    """Tests for _fetch_url_sync internal function for additional coverage."""

    @patch("httpx.Client")
    def test_fetch_html_success(self, mock_client_class: MagicMock) -> None:
        """Test successful HTML fetch with title extraction."""
        from ag.skills.fetch_web_content import _fetch_url_sync

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"content-type": "text/html; charset=utf-8"}
        mock_response.text = (
            "<html><head><title>Page Title</title></head>"
            "<body>Content</body></html>"
        )

        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client_class.return_value = mock_client

        result = _fetch_url_sync("https://example.com", timeout=30, max_length=10000)

        assert result.status_code == 200
        assert result.title == "Page Title"
        assert "Content" in result.content
        assert result.error is None

    @patch("httpx.Client")
    def test_fetch_json_success(self, mock_client_class: MagicMock) -> None:
        """Test successful JSON fetch."""
        from ag.skills.fetch_web_content import _fetch_url_sync

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"content-type": "application/json"}
        mock_response.text = '{"data": "value"}'

        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client_class.return_value = mock_client

        result = _fetch_url_sync("https://api.example.com/data", timeout=30, max_length=10000)

        assert result.status_code == 200
        assert '{"data": "value"}' in result.content
        assert result.title is None  # JSON has no title

    @patch("httpx.Client")
    def test_fetch_plain_text_success(self, mock_client_class: MagicMock) -> None:
        """Test successful plain text fetch."""
        from ag.skills.fetch_web_content import _fetch_url_sync

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"content-type": "text/plain"}
        mock_response.text = "Plain text content here"

        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client_class.return_value = mock_client

        result = _fetch_url_sync("https://example.com/file.txt", timeout=30, max_length=10000)

        assert result.status_code == 200
        assert result.content == "Plain text content here"
        assert result.title is None

    @patch("httpx.Client")
    def test_fetch_long_content_truncated(self, mock_client_class: MagicMock) -> None:
        """Test long content is truncated at max_length."""
        from ag.skills.fetch_web_content import _fetch_url_sync

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"content-type": "text/plain"}
        mock_response.text = "x" * 10000

        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client_class.return_value = mock_client

        result = _fetch_url_sync("https://example.com/large.txt", timeout=30, max_length=100)

        assert len(result.content) < 200  # max_length + truncation marker
        assert "truncated" in result.content.lower()

    @patch("httpx.Client")
    def test_fetch_non_text_content_type(self, mock_client_class: MagicMock) -> None:
        """Test non-text content types return error."""
        from ag.skills.fetch_web_content import _fetch_url_sync

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"content-type": "image/png"}

        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client_class.return_value = mock_client

        result = _fetch_url_sync("https://example.com/image.png", timeout=30, max_length=10000)

        assert result.content == ""
        assert result.error is not None
        assert "image/png" in result.error

    @patch("httpx.Client")
    def test_fetch_http_error_status(self, mock_client_class: MagicMock) -> None:
        """Test HTTP 4xx/5xx status codes set error."""
        from ag.skills.fetch_web_content import _fetch_url_sync

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.headers = {"content-type": "text/html"}
        mock_response.text = "<html><body>Internal Server Error</body></html>"

        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client_class.return_value = mock_client

        result = _fetch_url_sync("https://broken.example", timeout=30, max_length=10000)

        assert result.status_code == 500
        assert result.error == "HTTP 500"

    @patch("httpx.Client")
    def test_fetch_connection_exception(self, mock_client_class: MagicMock) -> None:
        """Test connection exceptions are captured."""
        from ag.skills.fetch_web_content import _fetch_url_sync

        mock_client = MagicMock()
        mock_client.get.side_effect = Exception("Connection refused")
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client_class.return_value = mock_client

        result = _fetch_url_sync("https://down.example", timeout=30, max_length=10000)

        assert result.status_code == 0
        assert result.content == ""
        assert "Connection refused" in result.error

    @patch("httpx.Client")
    def test_fetch_timeout_exception(self, mock_client_class: MagicMock) -> None:
        """Test timeout exceptions are captured."""
        import httpx

        from ag.skills.fetch_web_content import _fetch_url_sync

        mock_client = MagicMock()
        mock_client.get.side_effect = httpx.ReadTimeout("Timed out")
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client_class.return_value = mock_client

        result = _fetch_url_sync("https://slow.example", timeout=5, max_length=10000)

        assert result.status_code == 0
        assert result.error is not None

    @patch("httpx.Client")
    def test_fetch_default_content_type(self, mock_client_class: MagicMock) -> None:
        """Test missing content-type defaults to text/html."""
        from ag.skills.fetch_web_content import _fetch_url_sync

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {}  # No content-type header
        mock_response.text = "<html><body>No CT header</body></html>"

        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client_class.return_value = mock_client

        result = _fetch_url_sync("https://example.com", timeout=30, max_length=10000)

        # Default content_type is text/html
        assert "No CT header" in result.content


# ---------------------------------------------------------------------------
# AF-0093: Additional coverage tests for web_search
# ---------------------------------------------------------------------------


class TestWebSearchEngine:
    """Tests for web_search skill and engine implementations."""

    def test_input_query_fallback_to_prompt(self) -> None:
        """Test query falls back to prompt if empty."""
        from ag.skills.web_search import WebSearchInput

        inp = WebSearchInput(query="", prompt="fallback query")
        assert inp.query == "fallback query"

    def test_input_explicit_query_preferred(self) -> None:
        """Test explicit query takes precedence over prompt."""
        from ag.skills.web_search import WebSearchInput

        inp = WebSearchInput(query="explicit", prompt="fallback")
        # Explicit query should remain
        assert inp.query == "explicit"

    def test_empty_query_returns_error(self) -> None:
        """Test empty query without prompt returns error."""
        from ag.skills.base import SkillContext
        from ag.skills.web_search import WebSearchInput, WebSearchSkill

        skill = WebSearchSkill()
        ctx = SkillContext(workspace_path=".", run_id="test", provider=None)
        inp = WebSearchInput(query="", prompt="")

        output = skill.execute(inp, ctx)

        assert output.success is False
        assert "query" in output.error.lower() or "provided" in output.error.lower()

    @patch("ag.skills.web_search._search_duckduckgo")
    def test_duckduckgo_search_success(self, mock_ddg: MagicMock) -> None:
        """Test DuckDuckGo search returns results."""
        from ag.skills.base import SkillContext
        from ag.skills.web_search import (
            SearchResult,
            WebSearchInput,
            WebSearchSkill,
        )

        mock_ddg.return_value = [
            SearchResult(
                url="https://result1.com",
                title="Result 1",
                snippet="First result snippet",
                position=0,
            ),
            SearchResult(
                url="https://result2.com",
                title="Result 2",
                snippet="Second result snippet",
                position=1,
            ),
        ]

        skill = WebSearchSkill()
        ctx = SkillContext(workspace_path=".", run_id="test", provider=None)
        inp = WebSearchInput(query="test query", search_engine="duckduckgo")

        output = skill.execute(inp, ctx)

        assert output.success is True
        assert len(output.urls) == 2
        assert output.urls[0] == "https://result1.com"
        assert output.search_engine == "duckduckgo"
        assert output.total_results == 2
        mock_ddg.assert_called_once()

    @patch("ag.skills.web_search._search_duckduckgo")
    def test_duckduckgo_search_exception(self, mock_ddg: MagicMock) -> None:
        """Test DuckDuckGo search handles exceptions."""
        from ag.skills.base import SkillContext
        from ag.skills.web_search import WebSearchInput, WebSearchSkill

        mock_ddg.side_effect = RuntimeError("DuckDuckGo search failed: rate limited")

        skill = WebSearchSkill()
        ctx = SkillContext(workspace_path=".", run_id="test", provider=None)
        inp = WebSearchInput(query="test query", search_engine="duckduckgo")

        output = skill.execute(inp, ctx)

        assert output.success is False
        assert "failed" in output.error.lower()

    @patch("ag.skills.web_search._search_duckduckgo")
    def test_duckduckgo_import_error(self, mock_ddg: MagicMock) -> None:
        """Test handles missing ddgs package gracefully."""
        from ag.skills.base import SkillContext
        from ag.skills.web_search import WebSearchInput, WebSearchSkill

        mock_ddg.side_effect = ImportError("ddgs package not installed")

        skill = WebSearchSkill()
        ctx = SkillContext(workspace_path=".", run_id="test", provider=None)
        inp = WebSearchInput(query="test", search_engine="duckduckgo")

        output = skill.execute(inp, ctx)

        assert output.success is False
        assert "import" in output.summary.lower() or "missing" in output.summary.lower()

    @patch.dict("os.environ", {"SERPER_API_KEY": "test-key"})
    @patch("ag.skills.web_search._search_serper")
    def test_serper_search_with_api_key(self, mock_serper: MagicMock) -> None:
        """Test Serper search when API key is available."""
        from ag.skills.base import SkillContext
        from ag.skills.web_search import SearchResult, WebSearchInput, WebSearchSkill

        mock_serper.return_value = [
            SearchResult(
                url="https://serper-result.com",
                title="Serper Result",
                snippet="",
                position=0,
            )
        ]

        skill = WebSearchSkill()
        ctx = SkillContext(workspace_path=".", run_id="test", provider=None)
        inp = WebSearchInput(query="test", search_engine="serper")

        output = skill.execute(inp, ctx)

        assert output.success is True
        assert output.search_engine == "serper"
        mock_serper.assert_called_once()

    @patch.dict("os.environ", {}, clear=True)
    def test_serper_fallback_without_api_key(self) -> None:
        """Test Serper falls back to DuckDuckGo without API key."""
        # Ensure no API keys are set
        import os

        from ag.skills.web_search import _get_search_function

        os.environ.pop("SERPER_API_KEY", None)

        engine_name, _ = _get_search_function("serper")
        assert engine_name == "duckduckgo"

    @patch.dict("os.environ", {}, clear=True)
    def test_google_fallback_without_api_key(self) -> None:
        """Test Google falls back to DuckDuckGo without API key."""
        import os

        from ag.skills.web_search import _get_search_function

        os.environ.pop("GOOGLE_API_KEY", None)
        os.environ.pop("GOOGLE_SEARCH_ENGINE_ID", None)

        engine_name, _ = _get_search_function("google")
        assert engine_name == "duckduckgo"

    @patch.dict("os.environ", {}, clear=True)
    def test_bing_fallback_without_api_key(self) -> None:
        """Test Bing falls back to DuckDuckGo without API key."""
        import os

        from ag.skills.web_search import _get_search_function

        os.environ.pop("BING_API_KEY", None)

        engine_name, _ = _get_search_function("bing")
        assert engine_name == "duckduckgo"

    def test_unknown_engine_fallback(self) -> None:
        """Test unknown engine falls back to DuckDuckGo."""
        from ag.skills.web_search import _get_search_function

        engine_name, _ = _get_search_function("unknown_engine")
        assert engine_name == "duckduckgo"

    @patch("ag.skills.web_search._search_duckduckgo")
    def test_search_respects_max_results(self, mock_ddg: MagicMock) -> None:
        """Test max_results parameter is passed to search function."""
        from ag.skills.base import SkillContext
        from ag.skills.web_search import SearchResult, WebSearchInput, WebSearchSkill

        mock_ddg.return_value = [
            SearchResult(url=f"https://result{i}.com", title=f"Result {i}", snippet="", position=i)
            for i in range(3)
        ]

        skill = WebSearchSkill()
        ctx = SkillContext(workspace_path=".", run_id="test", provider=None)
        inp = WebSearchInput(query="test", max_results=3)

        skill.execute(inp, ctx)

        # Verify max_results was passed
        mock_ddg.assert_called_once()
        call_kwargs = mock_ddg.call_args[1]
        assert call_kwargs["max_results"] == 3

    @patch("ag.skills.web_search._search_duckduckgo")
    def test_search_empty_results(self, mock_ddg: MagicMock) -> None:
        """Test handling of empty search results."""
        from ag.skills.base import SkillContext
        from ag.skills.web_search import WebSearchInput, WebSearchSkill

        mock_ddg.return_value = []

        skill = WebSearchSkill()
        ctx = SkillContext(workspace_path=".", run_id="test", provider=None)
        inp = WebSearchInput(query="obscure query no results")

        output = skill.execute(inp, ctx)

        assert output.success is True  # No error, just no results
        assert output.urls == []
        assert output.total_results == 0

    @patch("ag.skills.web_search._search_duckduckgo")
    def test_search_filters_empty_urls(self, mock_ddg: MagicMock) -> None:
        """Test empty URLs are filtered from results."""
        from ag.skills.base import SkillContext
        from ag.skills.web_search import SearchResult, WebSearchInput, WebSearchSkill

        mock_ddg.return_value = [
            SearchResult(url="https://valid.com", title="Valid", snippet="", position=0),
            SearchResult(url="", title="Empty URL", snippet="", position=1),
            SearchResult(url="https://also-valid.com", title="Also Valid", snippet="", position=2),
        ]

        skill = WebSearchSkill()
        ctx = SkillContext(workspace_path=".", run_id="test", provider=None)
        inp = WebSearchInput(query="test")

        output = skill.execute(inp, ctx)

        assert len(output.urls) == 2
        assert "https://valid.com" in output.urls
        assert "https://also-valid.com" in output.urls
        assert "" not in output.urls


class TestWebSearchEngineImplementations:
    """Tests for individual search engine implementations."""

    @patch("ddgs.DDGS")
    def test_duckduckgo_implementation(self, mock_ddgs_class: MagicMock) -> None:
        """Test _search_duckduckgo implementation."""
        from ag.skills.web_search import _search_duckduckgo

        mock_ddgs_instance = MagicMock()
        mock_ddgs_class.return_value.__enter__ = MagicMock(return_value=mock_ddgs_instance)
        mock_ddgs_class.return_value.__exit__ = MagicMock(return_value=False)
        mock_ddgs_instance.text.return_value = [
            {"href": "https://ddg1.com", "title": "DDG 1", "body": "Snippet 1"},
            {"href": "https://ddg2.com", "title": "DDG 2", "body": "Snippet 2"},
        ]

        results = _search_duckduckgo(
            query="test query", max_results=5, region="wt-wt", safe_search=True
        )

        assert len(results) == 2
        assert results[0].url == "https://ddg1.com"
        assert results[0].title == "DDG 1"
        assert results[0].snippet == "Snippet 1"
        assert results[0].position == 0
        assert results[1].position == 1

    @patch.dict("os.environ", {"SERPER_API_KEY": "test-serper-key"})
    @patch("httpx.post")
    def test_serper_implementation(self, mock_post: MagicMock) -> None:
        """Test _search_serper implementation."""
        from ag.skills.web_search import _search_serper

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "organic": [
                {"link": "https://serper1.com", "title": "Serper 1", "snippet": "Snip 1"},
                {"link": "https://serper2.com", "title": "Serper 2", "snippet": "Snip 2"},
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        results = _search_serper(query="test", max_results=5, region="us-en", safe_search=True)

        assert len(results) == 2
        assert results[0].url == "https://serper1.com"
        mock_post.assert_called_once()
        # Verify API key header was set
        call_kwargs = mock_post.call_args[1]
        assert call_kwargs["headers"]["X-API-KEY"] == "test-serper-key"

    @patch.dict(
        "os.environ", {"GOOGLE_API_KEY": "google-key", "GOOGLE_SEARCH_ENGINE_ID": "cx-id"}
    )
    @patch("httpx.get")
    def test_google_implementation(self, mock_get: MagicMock) -> None:
        """Test _search_google implementation."""
        from ag.skills.web_search import _search_google

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "items": [
                {"link": "https://google1.com", "title": "Google 1", "snippet": "G Snip 1"},
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        results = _search_google(query="test", max_results=5, region="us-en", safe_search=True)

        assert len(results) == 1
        assert results[0].url == "https://google1.com"
        # Verify params
        call_kwargs = mock_get.call_args[1]
        assert call_kwargs["params"]["key"] == "google-key"
        assert call_kwargs["params"]["cx"] == "cx-id"

    @patch.dict("os.environ", {"BING_API_KEY": "bing-key"})
    @patch("httpx.get")
    def test_bing_implementation(self, mock_get: MagicMock) -> None:
        """Test _search_bing implementation."""
        from ag.skills.web_search import _search_bing

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "webPages": {
                "value": [
                    {"url": "https://bing1.com", "name": "Bing 1", "snippet": "B Snip 1"},
                ]
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        results = _search_bing(query="test", max_results=5, region="us-en", safe_search=True)

        assert len(results) == 1
        assert results[0].url == "https://bing1.com"
        assert results[0].title == "Bing 1"
        # Verify header
        call_kwargs = mock_get.call_args[1]
        assert call_kwargs["headers"]["Ocp-Apim-Subscription-Key"] == "bing-key"


# ---------------------------------------------------------------------------
# AF-0093: Additional coverage tests for synthesize_research
# ---------------------------------------------------------------------------


class TestSynthesizeResearchHelpers:
    """Tests for synthesize_research helper functions."""

    def test_build_synthesis_prompt(self) -> None:
        """Test _build_synthesis_prompt constructs valid prompt."""
        from ag.skills.synthesize_research import SourceDocument, _build_synthesis_prompt

        docs = [
            SourceDocument(source="https://src1.com", content="Content 1", source_type="url"),
            SourceDocument(source="docs/file.md", content="Content 2", source_type="file"),
        ]

        prompt = _build_synthesis_prompt(
            research_question="What is AI?",
            documents=docs,
            output_format="markdown",
            include_citations=True,
        )

        assert "What is AI?" in prompt
        assert "Content 1" in prompt
        assert "Content 2" in prompt
        assert "[Source 1]" in prompt
        assert "[Source 2]" in prompt
        assert "citation" in prompt.lower()
        assert "markdown" in prompt.lower()

    def test_build_synthesis_prompt_without_citations(self) -> None:
        """Test _build_synthesis_prompt with citations disabled."""
        from ag.skills.synthesize_research import SourceDocument, _build_synthesis_prompt

        docs = [SourceDocument(source="src", content="Content", source_type="url")]

        prompt = _build_synthesis_prompt(
            research_question="Question",
            documents=docs,
            output_format="plain",
            include_citations=False,
        )

        assert "Do not include explicit citations" in prompt

    def test_build_synthesis_prompt_json_format(self) -> None:
        """Test _build_synthesis_prompt with JSON output format."""
        from ag.skills.synthesize_research import SourceDocument, _build_synthesis_prompt

        docs = [SourceDocument(source="src", content="Content", source_type="url")]

        prompt = _build_synthesis_prompt(
            research_question="Question",
            documents=docs,
            output_format="json",
            include_citations=True,
        )

        assert "JSON" in prompt

    def test_extract_key_findings_bullets(self) -> None:
        """Test _extract_key_findings extracts bullet points."""
        from ag.skills.synthesize_research import _extract_key_findings

        report = """
# Report
Some intro text.

- Finding one is important
- Finding two is also key
- Finding three rounds it out
* Star bullet finding
• Unicode bullet finding

More text here.
"""
        findings = _extract_key_findings(report)

        assert len(findings) >= 3
        assert any("Finding one" in f for f in findings)
        assert any("Finding two" in f for f in findings)

    def test_extract_key_findings_numbered(self) -> None:
        """Test _extract_key_findings extracts numbered list."""
        from ag.skills.synthesize_research import _extract_key_findings

        report = """
# Key Findings

No bullets here, but we have:

1. First numbered finding
2) Second with different format
3. Third finding
"""
        findings = _extract_key_findings(report)

        assert len(findings) >= 1
        # Should find numbered items if no bullets

    def test_extract_key_findings_max_limit(self) -> None:
        """Test _extract_key_findings caps at 7."""
        from ag.skills.synthesize_research import _extract_key_findings

        report = "\n".join([f"- Finding {i}" for i in range(20)])
        findings = _extract_key_findings(report)

        assert len(findings) <= 7

    def test_extract_sources_used_with_citations(self) -> None:
        """Test _extract_sources_used finds cited sources."""
        from ag.skills.synthesize_research import SourceDocument, _extract_sources_used

        docs = [
            SourceDocument(source="https://src1.com", content="C1", source_type="url"),
            SourceDocument(source="https://src2.com", content="C2", source_type="url"),
            SourceDocument(source="https://src3.com", content="C3", source_type="url"),
        ]

        report = "Based on [Source 1] and [Source 3], we conclude..."

        sources = _extract_sources_used(report, docs)

        assert "https://src1.com" in sources
        assert "https://src3.com" in sources
        assert "https://src2.com" not in sources  # Not cited

    def test_extract_sources_used_no_citations(self) -> None:
        """Test _extract_sources_used returns all when no citations found."""
        from ag.skills.synthesize_research import SourceDocument, _extract_sources_used

        docs = [
            SourceDocument(source="src1", content="C1", source_type="url"),
            SourceDocument(source="src2", content="C2", source_type="url"),
        ]

        report = "A report without explicit source citations."

        sources = _extract_sources_used(report, docs)

        # Should return all sources as fallback
        assert len(sources) == 2

    def test_convert_to_source_document_fetched_format(self) -> None:
        """Test _convert_to_source_document handles FetchedDocument dict."""
        from ag.skills.synthesize_research import _convert_to_source_document

        fetched = {
            "url": "https://example.com",
            "content": "Page content",
            "title": "Page Title",
            "status_code": 200,
        }

        doc = _convert_to_source_document(fetched)

        assert doc.source == "https://example.com"
        assert doc.content == "Page content"
        assert doc.title == "Page Title"
        assert doc.source_type == "url"

    def test_convert_to_source_document_loaded_format(self) -> None:
        """Test _convert_to_source_document handles loaded Document dict."""
        from ag.skills.synthesize_research import _convert_to_source_document

        loaded = {"path": "docs/readme.md", "content": "# README", "size_bytes": 100}

        doc = _convert_to_source_document(loaded)

        assert doc.source == "docs/readme.md"
        assert doc.content == "# README"
        assert doc.source_type == "file"

    def test_convert_to_source_document_passthrough(self) -> None:
        """Test _convert_to_source_document passes through SourceDocument."""
        from ag.skills.synthesize_research import SourceDocument, _convert_to_source_document

        original = SourceDocument(source="src", content="content", source_type="custom")

        result = _convert_to_source_document(original)

        assert result is original


class TestSynthesizeResearchErrorPaths:
    """Tests for synthesize_research error handling."""

    def test_empty_documents_error(self) -> None:
        """Test error when no documents provided."""
        skill = SynthesizeResearchSkill()
        ctx = SkillContext(workspace_path=".", run_id="test", provider=None)
        inp = SynthesizeResearchInput(documents=[], prompt="Research question")

        output = skill.execute(inp, ctx)

        assert output.success is False
        assert "document" in output.error.lower()

    def test_fallback_synthesis_no_provider(self) -> None:
        """Test fallback synthesis when no LLM provider."""
        from ag.skills.synthesize_research import SourceDocument, _fallback_synthesis

        docs = [
            SourceDocument(source="src1", content="C1", title="Doc 1", source_type="file"),
            SourceDocument(source="src2", content="C2", source_type="url"),
        ]

        report, findings = _fallback_synthesis("Research question", docs)

        assert "Research question" in report
        assert "Doc 1" in report
        assert "2 source" in report.lower() or "2" in report
        assert len(findings) >= 1
        assert any("manual mode" in f.lower() for f in findings)

    def test_execute_without_provider_uses_fallback(self) -> None:
        """Test execute uses fallback when ctx.provider is None."""
        from ag.skills.synthesize_research import SourceDocument

        skill = SynthesizeResearchSkill()
        ctx = SkillContext(workspace_path=".", run_id="test", provider=None)
        inp = SynthesizeResearchInput(
            documents=[SourceDocument(source="s", content="c", source_type="url")],
            prompt="What is AI?",
        )

        output = skill.execute(inp, ctx)

        assert output.success is True
        assert "stub" in output.summary.lower() or "manual" in output.summary.lower()

    def test_llm_exception_handling(self) -> None:
        """Test LLM exception is captured gracefully."""
        from ag.skills.synthesize_research import SourceDocument

        mock_provider = MagicMock()
        mock_provider.chat.side_effect = RuntimeError("API rate limit exceeded")

        skill = SynthesizeResearchSkill()
        ctx = SkillContext(workspace_path=".", run_id="test", provider=mock_provider)
        inp = SynthesizeResearchInput(
            documents=[SourceDocument(source="s", content="c", source_type="url")],
            prompt="Question",
        )

        output = skill.execute(inp, ctx)

        assert output.success is False
        assert "rate limit" in output.error.lower() or "failed" in output.summary.lower()

    def test_execute_with_dataclass_response(self) -> None:
        """Test execute handles dataclass ChatResponse from provider."""
        from dataclasses import dataclass

        from ag.skills.synthesize_research import SourceDocument

        @dataclass
        class ChatResponse:
            content: str
            model: str = "test"

        mock_provider = MagicMock()
        mock_provider.chat.return_value = ChatResponse(content="# Generated Report\n- Finding 1")

        skill = SynthesizeResearchSkill()
        ctx = SkillContext(workspace_path=".", run_id="test", provider=mock_provider)
        inp = SynthesizeResearchInput(
            documents=[SourceDocument(source="s", content="c", source_type="url")],
            prompt="Question",
        )

        output = skill.execute(inp, ctx)

        assert output.success is True
        assert "Generated Report" in output.report
