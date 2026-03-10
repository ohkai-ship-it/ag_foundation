"""Web Search Skill — Search Engine API Capability (AF0080).

This skill performs web searches via search engine APIs and returns
URLs for the fetch_web_content skill. It is the discovery phase of
the research pipeline.

Schemas Defined (see docs/dev/additional/SCHEMA_INVENTORY.md):
    SearchResult — Single search result (url, title, snippet)
    WebSearchInput — Input schema (query, max_results, search_engine)
    WebSearchOutput — Output schema (urls, results, total_results)

Contracts Implemented (see docs/dev/additional/CONTRACT_INVENTORY.md):
    Skill[WebSearchInput, WebSearchOutput] — Web search capability

Pipeline Position:
    This is step 1 of the research_v0 playbook:
    load_documents → web_search → fetch_web_content → synthesize_research → emit_result

Design Decisions:
    - DuckDuckGo is the default (free, no API key required)
    - Serper API available for production-quality results (requires SERPER_API_KEY)
    - Output `urls` field matches FetchWebContentInput.urls for seamless chaining
    - Graceful failure: returns empty results, never raises exceptions
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, ClassVar

from pydantic import BaseModel, Field, model_validator

from ag.skills.base import Skill, SkillContext, SkillInput, SkillOutput

if TYPE_CHECKING:
    from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_MAX_RESULTS = 5
DEFAULT_SEARCH_ENGINE = "duckduckgo"
DEFAULT_REGION = "wt-wt"  # Worldwide


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------


class SearchResult(BaseModel):
    """A single search result.

    Schema: SCHEMA_INVENTORY.md#SearchResult
    """

    url: str = Field(..., description="Result URL")
    title: str = Field(default="", description="Result title")
    snippet: str = Field(default="", description="Result snippet/description")
    position: int = Field(default=0, description="Position in search results (0-indexed)")

    model_config = {"extra": "forbid"}


class WebSearchInput(SkillInput):
    """Input for web_search skill.

    Schema: SCHEMA_INVENTORY.md#WebSearchInput

    The query field can be empty; in that case, the skill will use the
    prompt field (injected by runtime) as the search query.
    """

    query: str = Field(
        default="",
        max_length=500,
        description="Search query; if empty, uses prompt",
    )
    max_results: int = Field(
        default=DEFAULT_MAX_RESULTS,
        ge=1,
        le=20,
        description="Maximum number of URLs to return",
    )
    search_engine: str = Field(
        default=DEFAULT_SEARCH_ENGINE,
        description="Search engine: 'duckduckgo' | 'serper' | 'google' | 'bing'",
    )
    region: str = Field(
        default=DEFAULT_REGION,
        description="Region code for localized results (e.g., 'us-en', 'de-de')",
    )
    safe_search: bool = Field(
        default=True,
        description="Enable safe search filtering",
    )

    model_config = {"extra": "ignore"}  # Ignore extra fields from pipeline (e.g., documents)

    @model_validator(mode="after")
    def ensure_query(self) -> "WebSearchInput":
        """Use prompt as fallback to satisfy runtime chaining contract.

        Runtime injects `prompt` by default for every skill step.
        This keeps playbook parameters minimal while ensuring query is always present.
        """
        if not self.query and self.prompt:
            object.__setattr__(self, "query", self.prompt)
        return self


class WebSearchOutput(SkillOutput):
    """Output from web_search skill.

    Schema: SCHEMA_INVENTORY.md#WebSearchOutput

    NOTE: The 'urls' field is the PRIMARY output for pipeline chaining.
    It matches FetchWebContentInput.urls directly.
    """

    urls: list[str] = Field(
        default_factory=list,
        description="URLs found (primary output for chaining to fetch_web_content)",
    )
    results: list[SearchResult] = Field(
        default_factory=list,
        description="Detailed search results with titles and snippets",
    )
    search_query: str = Field(
        default="",
        description="Actual query used",
    )
    search_engine: str = Field(
        default="",
        description="Search engine used",
    )
    total_results: int = Field(
        default=0,
        description="Number of results returned",
    )

    model_config = {"extra": "forbid"}


# ---------------------------------------------------------------------------
# Search Engine Implementations
# ---------------------------------------------------------------------------


def _search_duckduckgo(
    query: str,
    max_results: int,
    region: str,
    safe_search: bool,
) -> list[SearchResult]:
    """Search using DuckDuckGo (free, no API key required).

    Uses the duckduckgo-search package for unofficial API access.

    Args:
        query: Search query
        max_results: Maximum results to return
        region: Region code (e.g., 'wt-wt' for worldwide)
        safe_search: Enable safe search

    Returns:
        List of SearchResult objects
    """
    try:
        from ddgs import DDGS
    except ImportError:
        raise ImportError("ddgs package not installed. Install with: pip install ddgs")

    results: list[SearchResult] = []
    safesearch = "moderate" if safe_search else "off"

    try:
        with DDGS() as ddgs:
            search_results = list(
                ddgs.text(
                    query,
                    region=region,
                    safesearch=safesearch,
                    max_results=max_results,
                )
            )

            for i, r in enumerate(search_results):
                results.append(
                    SearchResult(
                        url=r.get("href", ""),
                        title=r.get("title", ""),
                        snippet=r.get("body", ""),
                        position=i,
                    )
                )
    except Exception as e:
        # Log but don't fail - return empty results
        # In production, this would use proper logging
        raise RuntimeError(f"DuckDuckGo search failed: {e}") from e

    return results


def _search_serper(
    query: str,
    max_results: int,
    region: str,
    safe_search: bool,
) -> list[SearchResult]:
    """Search using Serper API (Google results, requires API key).

    Requires SERPER_API_KEY environment variable.

    Args:
        query: Search query
        max_results: Maximum results to return
        region: Region code (ignored for Serper)
        safe_search: Enable safe search

    Returns:
        List of SearchResult objects
    """
    api_key = os.environ.get("SERPER_API_KEY")
    if not api_key:
        raise RuntimeError("SERPER_API_KEY environment variable not set")

    try:
        import httpx
    except ImportError:
        raise ImportError("httpx package not installed. Install with: pip install httpx")

    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json",
    }
    payload: dict[str, Any] = {
        "q": query,
        "num": max_results,
    }
    if safe_search:
        payload["safe"] = "active"

    try:
        response = httpx.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        results: list[SearchResult] = []
        for i, item in enumerate(data.get("organic", [])):
            results.append(
                SearchResult(
                    url=item.get("link", ""),
                    title=item.get("title", ""),
                    snippet=item.get("snippet", ""),
                    position=i,
                )
            )
        return results
    except Exception as e:
        raise RuntimeError(f"Serper API search failed: {e}") from e


def _search_google(
    query: str,
    max_results: int,
    region: str,
    safe_search: bool,
) -> list[SearchResult]:
    """Search using Google Custom Search API.

    Requires GOOGLE_API_KEY and GOOGLE_SEARCH_ENGINE_ID environment variables.

    Args:
        query: Search query
        max_results: Maximum results to return (max 10 per request)
        region: Region code (ignored for Google CSE)
        safe_search: Enable safe search

    Returns:
        List of SearchResult objects
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    cx = os.environ.get("GOOGLE_SEARCH_ENGINE_ID")

    if not api_key or not cx:
        raise RuntimeError(
            "GOOGLE_API_KEY and GOOGLE_SEARCH_ENGINE_ID environment variables required"
        )

    try:
        import httpx
    except ImportError:
        raise ImportError("httpx package not installed. Install with: pip install httpx")

    url = "https://www.googleapis.com/customsearch/v1"
    params: dict[str, Any] = {
        "key": api_key,
        "cx": cx,
        "q": query,
        "num": min(max_results, 10),  # Google CSE max is 10 per request
    }
    if safe_search:
        params["safe"] = "active"

    try:
        response = httpx.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        results: list[SearchResult] = []
        for i, item in enumerate(data.get("items", [])):
            results.append(
                SearchResult(
                    url=item.get("link", ""),
                    title=item.get("title", ""),
                    snippet=item.get("snippet", ""),
                    position=i,
                )
            )
        return results
    except Exception as e:
        raise RuntimeError(f"Google Custom Search failed: {e}") from e


def _search_bing(
    query: str,
    max_results: int,
    region: str,
    safe_search: bool,
) -> list[SearchResult]:
    """Search using Bing Web Search API.

    Requires BING_API_KEY environment variable.

    Args:
        query: Search query
        max_results: Maximum results to return
        region: Region code (used as market parameter)
        safe_search: Enable safe search

    Returns:
        List of SearchResult objects
    """
    api_key = os.environ.get("BING_API_KEY")
    if not api_key:
        raise RuntimeError("BING_API_KEY environment variable not set")

    try:
        import httpx
    except ImportError:
        raise ImportError("httpx package not installed. Install with: pip install httpx")

    url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    params: dict[str, Any] = {
        "q": query,
        "count": max_results,
    }
    if region and region != "wt-wt":
        # Convert region format (e.g., 'us-en' -> 'en-US')
        parts = region.split("-")
        if len(parts) == 2:
            params["mkt"] = f"{parts[1]}-{parts[0].upper()}"
    if safe_search:
        params["safeSearch"] = "Moderate"
    else:
        params["safeSearch"] = "Off"

    try:
        response = httpx.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        results: list[SearchResult] = []
        web_pages = data.get("webPages", {}).get("value", [])
        for i, item in enumerate(web_pages):
            results.append(
                SearchResult(
                    url=item.get("url", ""),
                    title=item.get("name", ""),
                    snippet=item.get("snippet", ""),
                    position=i,
                )
            )
        return results
    except Exception as e:
        raise RuntimeError(f"Bing Web Search failed: {e}") from e


# ---------------------------------------------------------------------------
# Engine Selection
# ---------------------------------------------------------------------------


def _get_search_function(engine: str) -> tuple[str, callable]:
    """Get the search function for the specified engine.

    Falls back to DuckDuckGo if specified engine is unavailable.

    Args:
        engine: Preferred search engine name

    Returns:
        Tuple of (actual_engine_name, search_function)
    """
    engines = {
        "duckduckgo": ("duckduckgo", _search_duckduckgo),
        "serper": ("serper", _search_serper),
        "google": ("google", _search_google),
        "bing": ("bing", _search_bing),
    }

    # If preferred engine requires API key, check if available
    if engine == "serper" and not os.environ.get("SERPER_API_KEY"):
        engine = "duckduckgo"
    elif engine == "google" and not (
        os.environ.get("GOOGLE_API_KEY") and os.environ.get("GOOGLE_SEARCH_ENGINE_ID")
    ):
        engine = "duckduckgo"
    elif engine == "bing" and not os.environ.get("BING_API_KEY"):
        engine = "duckduckgo"

    return engines.get(engine, ("duckduckgo", _search_duckduckgo))


# ---------------------------------------------------------------------------
# Skill Implementation
# ---------------------------------------------------------------------------


class WebSearchSkill(Skill[WebSearchInput, WebSearchOutput]):
    """Search the web for URLs matching a query.

    This skill calls search engine APIs to discover relevant URLs.
    It does NOT fetch content — that is handled by fetch_web_content.

    Contract: CONTRACT_INVENTORY.md#WebSearchSkill

    Supported search engines:
    - duckduckgo (default, free, no API key)
    - serper (requires SERPER_API_KEY)
    - google (requires GOOGLE_API_KEY + GOOGLE_SEARCH_ENGINE_ID)
    - bing (requires BING_API_KEY)

    Example:
        skill = WebSearchSkill()
        output = skill.execute(
            WebSearchInput(query="Düsseldorf meteorite", max_results=5),
            SkillContext()
        )
        # output.urls can be passed directly to fetch_web_content
    """

    name: ClassVar[str] = "web_search"
    description: ClassVar[str] = "Search the web for URLs matching a query"
    input_schema: ClassVar[type[WebSearchInput]] = WebSearchInput
    output_schema: ClassVar[type[WebSearchOutput]] = WebSearchOutput
    requires_llm: ClassVar[bool] = False

    def execute(self, input: WebSearchInput, ctx: SkillContext) -> WebSearchOutput:
        """Execute web search and return URLs.

        Args:
            input: Search query and parameters
            ctx: Skill context (unused for this skill)

        Returns:
            WebSearchOutput with urls list for pipeline chaining
        """
        # Determine actual query (input.query or fallback to prompt)
        query = input.query or input.prompt
        if not query:
            return WebSearchOutput(
                success=False,
                summary="No search query provided",
                urls=[],
                results=[],
                search_query="",
                search_engine=input.search_engine,
                total_results=0,
                error="Either query or prompt must be provided",
            )

        # Get search function for engine
        actual_engine, search_fn = _get_search_function(input.search_engine)

        try:
            results = search_fn(
                query=query,
                max_results=input.max_results,
                region=input.region,
                safe_search=input.safe_search,
            )

            urls = [r.url for r in results if r.url]

            return WebSearchOutput(
                success=True,
                summary=f"Found {len(results)} results for '{query}' using {actual_engine}",
                urls=urls,
                results=results,
                search_query=query,
                search_engine=actual_engine,
                total_results=len(results),
            )

        except ImportError as e:
            return WebSearchOutput(
                success=False,
                summary=f"Missing dependency: {e}",
                urls=[],
                results=[],
                search_query=query,
                search_engine=actual_engine,
                total_results=0,
                error=str(e),
            )
        except Exception as e:
            return WebSearchOutput(
                success=False,
                summary=f"Search failed: {e}",
                urls=[],
                results=[],
                search_query=query,
                search_engine=actual_engine,
                total_results=0,
                error=str(e),
            )
