"""Fetch web content skill — HTTP fetching capability (AF0074).

This skill fetches content from user-provided URLs and extracts text.
It is a pure capability skill (HTTP I/O) without decision-making.

Schemas Defined (see docs/dev/additional/SCHEMA_INVENTORY.md):
    FetchedDocument — Schema for fetched URL content
    FetchWebContentInput — Input schema (urls, timeout, max_content_length)
    FetchWebContentOutput — Output schema (documents, failed_urls)

Contracts Implemented (see docs/dev/additional/CONTRACT_INVENTORY.md):
    Skill[FetchWebContentInput, FetchWebContentOutput] — HTTP fetching capability

Design Decisions:
    - User provides specific URLs (not a search engine)
    - Graceful failure handling (timeouts, 404s recorded, not exceptions)
    - Text extraction from HTML (simple tag stripping)
    - Content truncation to prevent memory issues
"""

from __future__ import annotations

import re
from typing import Any, ClassVar

from pydantic import BaseModel, Field

from ag.skills.base import Skill, SkillContext, SkillInput, SkillOutput

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_TIMEOUT = 30
DEFAULT_MAX_CONTENT_LENGTH = 100_000  # ~100KB per page
DEFAULT_USER_AGENT = "AG-Foundation-Research/1.0"


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------


class FetchedDocument(BaseModel):
    """A document fetched from a URL.

    Schema: SCHEMA_INVENTORY.md#FetchedDocument
    """

    url: str = Field(..., description="Source URL")
    content: str = Field(..., description="Extracted text content")
    status_code: int = Field(..., description="HTTP status code")
    content_type: str = Field(default="text/html", description="Content-Type header")
    title: str | None = Field(default=None, description="Page title if found")
    error: str | None = Field(default=None, description="Error message if fetch failed")

    model_config = {"extra": "forbid"}


class FetchWebContentInput(SkillInput):
    """Input for fetch_web_content skill.

    Schema: SCHEMA_INVENTORY.md#FetchWebContentInput
    """

    urls: list[str] = Field(default_factory=list, description="URLs to fetch")
    timeout_seconds: int = Field(
        default=DEFAULT_TIMEOUT, ge=1, le=120, description="Request timeout in seconds"
    )
    max_content_length: int = Field(
        default=DEFAULT_MAX_CONTENT_LENGTH,
        ge=1000,
        le=1_000_000,
        description="Max content length per page (bytes)",
    )

    model_config = {"extra": "forbid"}


class FetchWebContentOutput(SkillOutput):
    """Output from fetch_web_content skill.

    Schema: SCHEMA_INVENTORY.md#FetchWebContentOutput
    """

    documents: list[FetchedDocument] = Field(
        default_factory=list, description="Successfully fetched documents"
    )
    failed_urls: list[str] = Field(
        default_factory=list, description="URLs that failed to fetch"
    )
    total_fetched: int = Field(default=0, description="Number of successfully fetched URLs")
    total_failed: int = Field(default=0, description="Number of failed URLs")

    model_config = {"extra": "forbid"}


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------


def _extract_text_from_html(html: str, max_length: int) -> tuple[str, str | None]:
    """Extract plain text from HTML content.

    Simple implementation using regex. For production, consider using
    libraries like beautifulsoup4 or readability-lxml.

    Args:
        html: Raw HTML content
        max_length: Maximum content length

    Returns:
        Tuple of (extracted_text, title_or_none)
    """
    # Extract title
    title_match = re.search(r"<title[^>]*>([^<]+)</title>", html, re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else None

    # Remove script and style tags with content
    text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)

    # Remove HTML comments
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)

    # Remove all HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Decode common HTML entities
    text = text.replace("&nbsp;", " ")
    text = text.replace("&amp;", "&")
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    text = text.replace("&quot;", '"')
    text = text.replace("&#39;", "'")

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)
    text = text.strip()

    # Truncate if needed
    if len(text) > max_length:
        text = text[:max_length] + "... [truncated]"

    return text, title


async def _fetch_url(
    url: str,
    timeout: int,
    max_length: int,
) -> FetchedDocument:
    """Fetch a single URL and extract content.

    Args:
        url: URL to fetch
        timeout: Request timeout in seconds
        max_length: Max content length

    Returns:
        FetchedDocument with content or error
    """
    try:
        import httpx

        async with httpx.AsyncClient(
            timeout=timeout,
            follow_redirects=True,
            headers={"User-Agent": DEFAULT_USER_AGENT},
        ) as client:
            response = await client.get(url)

            content_type = response.headers.get("content-type", "text/html")

            # Check if content is text-based
            if "text" not in content_type and "json" not in content_type:
                return FetchedDocument(
                    url=url,
                    content="",
                    status_code=response.status_code,
                    content_type=content_type,
                    error=f"Non-text content type: {content_type}",
                )

            raw_content = response.text

            # Extract text from HTML
            if "html" in content_type.lower():
                text, title = _extract_text_from_html(raw_content, max_length)
            else:
                # Plain text or JSON - use as-is
                text = raw_content[:max_length]
                if len(raw_content) > max_length:
                    text += "... [truncated]"
                title = None

            return FetchedDocument(
                url=url,
                content=text,
                status_code=response.status_code,
                content_type=content_type,
                title=title,
                error=None if response.status_code < 400 else f"HTTP {response.status_code}",
            )

    except ImportError:
        return FetchedDocument(
            url=url,
            content="",
            status_code=0,
            error="httpx not installed - run: pip install httpx",
        )
    except Exception as e:
        return FetchedDocument(
            url=url,
            content="",
            status_code=0,
            error=str(e),
        )


def _fetch_url_sync(
    url: str,
    timeout: int,
    max_length: int,
) -> FetchedDocument:
    """Synchronous URL fetch (fallback when asyncio not available).

    Args:
        url: URL to fetch
        timeout: Request timeout in seconds
        max_length: Max content length

    Returns:
        FetchedDocument with content or error
    """
    try:
        import httpx

        with httpx.Client(
            timeout=timeout,
            follow_redirects=True,
            headers={"User-Agent": DEFAULT_USER_AGENT},
        ) as client:
            response = client.get(url)

            content_type = response.headers.get("content-type", "text/html")

            # Check if content is text-based
            if "text" not in content_type and "json" not in content_type:
                return FetchedDocument(
                    url=url,
                    content="",
                    status_code=response.status_code,
                    content_type=content_type,
                    error=f"Non-text content type: {content_type}",
                )

            raw_content = response.text

            # Extract text from HTML
            if "html" in content_type.lower():
                text, title = _extract_text_from_html(raw_content, max_length)
            else:
                text = raw_content[:max_length]
                if len(raw_content) > max_length:
                    text += "... [truncated]"
                title = None

            return FetchedDocument(
                url=url,
                content=text,
                status_code=response.status_code,
                content_type=content_type,
                title=title,
                error=None if response.status_code < 400 else f"HTTP {response.status_code}",
            )

    except ImportError:
        return FetchedDocument(
            url=url,
            content="",
            status_code=0,
            error="httpx not installed - run: pip install httpx",
        )
    except Exception as e:
        return FetchedDocument(
            url=url,
            content="",
            status_code=0,
            error=str(e),
        )


# ---------------------------------------------------------------------------
# Skill Implementation
# ---------------------------------------------------------------------------


class FetchWebContentSkill(Skill[FetchWebContentInput, FetchWebContentOutput]):
    """Fetch content from URLs.

    This skill fetches web pages and extracts text content.
    It handles errors gracefully, recording failures without raising exceptions.

    Contract: CONTRACT_INVENTORY.md#FetchWebContentSkill

    Args:
        urls: List of URLs to fetch
        timeout_seconds: Request timeout (default 30s)
        max_content_length: Max content per page (default 100KB)

    Returns:
        FetchWebContentOutput with documents and failed_urls lists

    Example:
        skill = FetchWebContentSkill()
        output = skill.execute(
            FetchWebContentInput(urls=["https://example.com"]),
            SkillContext()
        )
        for doc in output.documents:
            print(f"{doc.title}: {len(doc.content)} chars")
    """

    name: ClassVar[str] = "fetch_web_content"
    description: ClassVar[str] = "Fetch and extract text content from URLs"
    input_schema: ClassVar[type[FetchWebContentInput]] = FetchWebContentInput
    output_schema: ClassVar[type[FetchWebContentOutput]] = FetchWebContentOutput
    requires_llm: ClassVar[bool] = False

    def execute(
        self, input: FetchWebContentInput, ctx: SkillContext
    ) -> FetchWebContentOutput:
        """Fetch content from the provided URLs.

        Args:
            input: URLs and fetch parameters
            ctx: Skill context (not used for this capability)

        Returns:
            Output with fetched documents and failure list
        """
        if not input.urls:
            return FetchWebContentOutput(
                success=True,
                summary="No URLs provided",
                documents=[],
                failed_urls=[],
                total_fetched=0,
                total_failed=0,
            )

        documents: list[FetchedDocument] = []
        failed_urls: list[str] = []

        # Fetch each URL synchronously (simple implementation)
        for url in input.urls:
            doc = _fetch_url_sync(
                url=url,
                timeout=input.timeout_seconds,
                max_length=input.max_content_length,
            )
            if doc.error:
                failed_urls.append(url)
            documents.append(doc)

        total_fetched = len([d for d in documents if not d.error])
        total_failed = len(failed_urls)

        return FetchWebContentOutput(
            success=total_fetched > 0 or len(input.urls) == 0,
            summary=f"Fetched {total_fetched}/{len(input.urls)} URLs",
            documents=documents,
            failed_urls=failed_urls,
            total_fetched=total_fetched,
            total_failed=total_failed,
        )
