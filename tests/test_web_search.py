"""Tests for AF-0080: Web Search Skill.

Tests:
- WebSearchSkill schema validation
- Input/output Pydantic models
- Search engine implementations (mocked)
- Pipeline integration with fetch_web_content
- Error handling and graceful degradation
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from ag.skills.base import SkillContext
from ag.skills.registry import create_default_registry
from ag.skills.web_search import (
    DEFAULT_MAX_RESULTS,
    DEFAULT_REGION,
    DEFAULT_SEARCH_ENGINE,
    SearchResult,
    WebSearchInput,
    WebSearchOutput,
    WebSearchSkill,
    _get_search_function,
)

# ---------------------------------------------------------------------------
# Schema Tests
# ---------------------------------------------------------------------------


class TestWebSearchSchemas:
    """Tests for web_search schema definitions."""

    def test_search_result_schema(self) -> None:
        """Test SearchResult schema."""
        result = SearchResult(
            url="https://example.com/page",
            title="Example Page",
            snippet="This is an example page about...",
            position=0,
        )
        assert result.url == "https://example.com/page"
        assert result.title == "Example Page"
        assert result.snippet == "This is an example page about..."
        assert result.position == 0

    def test_search_result_defaults(self) -> None:
        """Test SearchResult default values."""
        result = SearchResult(url="https://example.com")
        assert result.title == ""
        assert result.snippet == ""
        assert result.position == 0

    def test_input_schema_defaults(self) -> None:
        """Test WebSearchInput uses correct defaults."""
        inp = WebSearchInput(prompt="test query")
        assert inp.query == "test query"  # Populated from prompt by validator
        assert inp.max_results == DEFAULT_MAX_RESULTS
        assert inp.search_engine == DEFAULT_SEARCH_ENGINE
        assert inp.region == DEFAULT_REGION
        assert inp.safe_search is True

    def test_input_schema_custom_values(self) -> None:
        """Test WebSearchInput with custom values."""
        inp = WebSearchInput(
            query="Düsseldorf meteorite",
            max_results=10,
            search_engine="serper",
            region="de-de",
            safe_search=False,
        )
        assert inp.query == "Düsseldorf meteorite"
        assert inp.max_results == 10
        assert inp.search_engine == "serper"
        assert inp.region == "de-de"
        assert inp.safe_search is False

    def test_input_query_from_prompt_fallback(self) -> None:
        """Test that query falls back to prompt via model_validator."""
        inp = WebSearchInput(prompt="Research the meteorite")
        # After validation, query should be set from prompt
        assert inp.query == "Research the meteorite"

    def test_input_query_overrides_prompt(self) -> None:
        """Test that explicit query takes precedence over prompt."""
        inp = WebSearchInput(prompt="fallback", query="explicit query")
        assert inp.query == "explicit query"

    def test_input_max_results_validation(self) -> None:
        """Test max_results bounds validation."""
        # Valid bounds
        inp = WebSearchInput(query="test", max_results=1)
        assert inp.max_results == 1

        inp = WebSearchInput(query="test", max_results=20)
        assert inp.max_results == 20

        # Invalid: too small
        with pytest.raises(ValueError):
            WebSearchInput(query="test", max_results=0)

        # Invalid: too large
        with pytest.raises(ValueError):
            WebSearchInput(query="test", max_results=21)

    def test_output_schema(self) -> None:
        """Test WebSearchOutput schema."""
        output = WebSearchOutput(
            success=True,
            summary="Found 3 results",
            urls=["https://a.com", "https://b.com", "https://c.com"],
            results=[
                SearchResult(url="https://a.com", title="A", position=0),
                SearchResult(url="https://b.com", title="B", position=1),
                SearchResult(url="https://c.com", title="C", position=2),
            ],
            search_query="test query",
            search_engine="duckduckgo",
            total_results=3,
        )
        assert output.success is True
        assert len(output.urls) == 3
        assert len(output.results) == 3
        assert output.total_results == 3

    def test_output_schema_failed(self) -> None:
        """Test WebSearchOutput for failed search."""
        output = WebSearchOutput(
            success=False,
            summary="Search failed: API error",
            urls=[],
            results=[],
            search_query="test",
            search_engine="duckduckgo",
            total_results=0,
            error="API error",
        )
        assert output.success is False
        assert output.error == "API error"
        assert len(output.urls) == 0


# ---------------------------------------------------------------------------
# Skill Tests
# ---------------------------------------------------------------------------


class TestWebSearchSkill:
    """Tests for WebSearchSkill."""

    def test_skill_metadata(self) -> None:
        """Test skill has correct metadata."""
        skill = WebSearchSkill()
        assert skill.name == "web_search"
        assert skill.description
        assert skill.requires_llm is False

    def test_skill_registered(self) -> None:
        """Test skill is registered in default registry."""
        registry = create_default_registry()
        assert registry.has("web_search")

        info = registry.get_skill("web_search")
        assert info is not None
        assert info.name == "web_search"

    @patch("ag.skills.web_search._search_duckduckgo")
    def test_execute_success(self, mock_ddg: MagicMock) -> None:
        """Test successful search execution."""
        mock_ddg.return_value = [
            SearchResult(url="https://example.com", title="Example", position=0),
            SearchResult(url="https://test.org", title="Test", position=1),
        ]

        skill = WebSearchSkill()
        ctx = SkillContext()
        inp = WebSearchInput(query="test query", max_results=5)

        output = skill.execute(inp, ctx)

        assert output.success is True
        assert len(output.urls) == 2
        assert "https://example.com" in output.urls
        assert output.search_engine == "duckduckgo"
        mock_ddg.assert_called_once()

    @patch("ag.skills.web_search._search_duckduckgo")
    def test_execute_with_prompt_fallback(self, mock_ddg: MagicMock) -> None:
        """Test search using prompt as query fallback."""
        mock_ddg.return_value = [
            SearchResult(url="https://example.com", title="Example", position=0),
        ]

        skill = WebSearchSkill()
        ctx = SkillContext()
        # No explicit query, should use prompt
        inp = WebSearchInput(prompt="Research the meteorite")

        output = skill.execute(inp, ctx)

        assert output.success is True
        assert output.search_query == "Research the meteorite"

    def test_execute_no_query(self) -> None:
        """Test search fails gracefully without query or prompt."""
        skill = WebSearchSkill()
        ctx = SkillContext()
        # Create input manually to bypass validator (edge case)
        inp = WebSearchInput.__new__(WebSearchInput)
        object.__setattr__(inp, "query", "")
        object.__setattr__(inp, "prompt", "")
        object.__setattr__(inp, "max_results", 5)
        object.__setattr__(inp, "search_engine", "duckduckgo")
        object.__setattr__(inp, "region", "wt-wt")
        object.__setattr__(inp, "safe_search", True)

        output = skill.execute(inp, ctx)

        assert output.success is False
        assert "No search query" in output.summary

    @patch("ag.skills.web_search._search_duckduckgo")
    def test_execute_search_error(self, mock_ddg: MagicMock) -> None:
        """Test graceful error handling on search failure."""
        mock_ddg.side_effect = RuntimeError("API rate limited")

        skill = WebSearchSkill()
        ctx = SkillContext()
        inp = WebSearchInput(query="test query")

        output = skill.execute(inp, ctx)

        assert output.success is False
        assert "Search failed" in output.summary
        assert output.error is not None
        assert len(output.urls) == 0

    @patch("ag.skills.web_search._search_duckduckgo")
    def test_execute_import_error(self, mock_ddg: MagicMock) -> None:
        """Test handling of missing dependency."""
        mock_ddg.side_effect = ImportError("duckduckgo-search not installed")

        skill = WebSearchSkill()
        ctx = SkillContext()
        inp = WebSearchInput(query="test query")

        output = skill.execute(inp, ctx)

        assert output.success is False
        assert "Missing dependency" in output.summary


# ---------------------------------------------------------------------------
# Engine Selection Tests
# ---------------------------------------------------------------------------


class TestEngineSelection:
    """Tests for search engine selection logic."""

    def test_default_engine_selection(self) -> None:
        """Test DuckDuckGo is selected by default."""
        engine_name, _ = _get_search_function("duckduckgo")
        assert engine_name == "duckduckgo"

    def test_fallback_without_api_key(self) -> None:
        """Test fallback to DuckDuckGo when API key missing."""
        # Serper without API key should fall back to DuckDuckGo
        with patch.dict("os.environ", {}, clear=True):
            engine_name, _ = _get_search_function("serper")
            assert engine_name == "duckduckgo"

    @patch.dict("os.environ", {"SERPER_API_KEY": "test-key"})
    def test_serper_with_api_key(self) -> None:
        """Test Serper is selected when API key present."""
        engine_name, _ = _get_search_function("serper")
        assert engine_name == "serper"

    @patch.dict("os.environ", {"GOOGLE_API_KEY": "test", "GOOGLE_SEARCH_ENGINE_ID": "cx"})
    def test_google_with_api_keys(self) -> None:
        """Test Google is selected when both keys present."""
        engine_name, _ = _get_search_function("google")
        assert engine_name == "google"

    @patch.dict("os.environ", {"GOOGLE_API_KEY": "test"}, clear=True)
    def test_google_missing_cx(self) -> None:
        """Test fallback when Google CX is missing."""
        engine_name, _ = _get_search_function("google")
        assert engine_name == "duckduckgo"

    @patch.dict("os.environ", {"BING_API_KEY": "test-key"})
    def test_bing_with_api_key(self) -> None:
        """Test Bing is selected when API key present."""
        engine_name, _ = _get_search_function("bing")
        assert engine_name == "bing"

    def test_unknown_engine_fallback(self) -> None:
        """Test unknown engine falls back to DuckDuckGo."""
        engine_name, _ = _get_search_function("unknown_engine")
        assert engine_name == "duckduckgo"


# ---------------------------------------------------------------------------
# Pipeline Integration Tests
# ---------------------------------------------------------------------------


class TestPipelineIntegration:
    """Tests for web_search integration with fetch_web_content."""

    def test_output_urls_match_fetch_input(self) -> None:
        """Test that output urls field matches fetch_web_content input schema."""
        from ag.skills.fetch_web_content import FetchWebContentInput

        # Get urls from web_search output
        output = WebSearchOutput(
            success=True,
            summary="Found 3 results",
            urls=["https://a.com", "https://b.com"],
            results=[],
            search_query="test",
            search_engine="duckduckgo",
            total_results=2,
        )

        # Verify urls can be used in FetchWebContentInput
        fetch_input = FetchWebContentInput(urls=output.urls)
        assert fetch_input.urls == output.urls
        assert len(fetch_input.urls) == 2

    @patch("ag.skills.web_search._search_duckduckgo")
    def test_to_legacy_tuple_format(self, mock_ddg: MagicMock) -> None:
        """Test output converts to legacy tuple for runtime."""
        mock_ddg.return_value = [
            SearchResult(url="https://example.com", title="Example", position=0),
        ]

        skill = WebSearchSkill()
        ctx = SkillContext()
        inp = WebSearchInput(query="test")

        output = skill.execute(inp, ctx)
        success, summary, data = output.to_legacy_tuple()

        assert success is True
        assert "urls" in data
        assert data["urls"] == ["https://example.com"]


# ---------------------------------------------------------------------------
# DuckDuckGo Integration Tests (Mocked)
# ---------------------------------------------------------------------------


class TestDuckDuckGoSearch:
    """Tests for DuckDuckGo search implementation."""

    @patch("ddgs.DDGS")
    def test_duckduckgo_search(self, mock_ddgs_class: MagicMock) -> None:
        """Test DuckDuckGo search calls with correct parameters."""
        from ag.skills.web_search import _search_duckduckgo

        mock_ddgs = MagicMock()
        mock_ddgs_class.return_value.__enter__ = MagicMock(return_value=mock_ddgs)
        mock_ddgs_class.return_value.__exit__ = MagicMock(return_value=None)
        mock_ddgs.text.return_value = [
            {"href": "https://example.com", "title": "Example", "body": "Description"},
        ]

        results = _search_duckduckgo(
            query="test query",
            max_results=5,
            region="wt-wt",
            safe_search=True,
        )

        assert len(results) == 1
        assert results[0].url == "https://example.com"
        assert results[0].title == "Example"
        mock_ddgs.text.assert_called_once_with(
            "test query",
            region="wt-wt",
            safesearch="moderate",
            max_results=5,
        )

    @patch("ddgs.DDGS")
    def test_duckduckgo_safe_search_off(self, mock_ddgs_class: MagicMock) -> None:
        """Test DuckDuckGo with safe search disabled."""
        from ag.skills.web_search import _search_duckduckgo

        mock_ddgs = MagicMock()
        mock_ddgs_class.return_value.__enter__ = MagicMock(return_value=mock_ddgs)
        mock_ddgs_class.return_value.__exit__ = MagicMock(return_value=None)
        mock_ddgs.text.return_value = []

        _search_duckduckgo(
            query="test",
            max_results=5,
            region="wt-wt",
            safe_search=False,
        )

        mock_ddgs.text.assert_called_once()
        call_kwargs = mock_ddgs.text.call_args
        assert call_kwargs[1]["safesearch"] == "off"


# ---------------------------------------------------------------------------
# Serper Integration Tests (Mocked)
# ---------------------------------------------------------------------------


class TestSerperSearch:
    """Tests for Serper API search implementation."""

    @patch("httpx.post")
    @patch.dict("os.environ", {"SERPER_API_KEY": "test-api-key"})
    def test_serper_search(self, mock_post: MagicMock) -> None:
        """Test Serper API search calls."""
        from ag.skills.web_search import _search_serper

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "organic": [
                {"link": "https://example.com", "title": "Example", "snippet": "Desc"},
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        results = _search_serper(
            query="test query",
            max_results=5,
            region="wt-wt",
            safe_search=True,
        )

        assert len(results) == 1
        assert results[0].url == "https://example.com"
        mock_post.assert_called_once()

    @patch.dict("os.environ", {}, clear=True)
    def test_serper_missing_api_key(self) -> None:
        """Test Serper fails without API key."""
        from ag.skills.web_search import _search_serper

        with pytest.raises(RuntimeError, match="SERPER_API_KEY"):
            _search_serper("test", 5, "wt-wt", True)
