"""Pytest configuration and shared fixtures (AF-0096, AF-0125).

Session-level workspace isolation: redirects all workspace I/O away
from ~/.ag/workspaces/ so no test artifacts leak into the user's
real workspace directory.

AF-0125: Deterministic test provider — autouse fixture patches get_provider
globally so no test makes real LLM calls by default.
"""

from __future__ import annotations

import os
import warnings
from unittest.mock import patch

import pytest

# Suppress SSL-socket GC noise from ddgs/DuckDuckGo Cloudflare connections.
# These sockets are created by tests that mock DDGS but the underlying
# primp/httpx client may still open a connection on import; when Python's GC
# finalizes the socket, pytest turns the ResourceWarning into
# PytestUnraisableExceptionWarning — even under `-W error`.
# This filter is inserted early (before CLI flags) so it wins.
warnings.filterwarnings(
    "ignore",
    message="unclosed.*ssl",
    category=pytest.PytestUnraisableExceptionWarning,
)


@pytest.fixture(autouse=True, scope="session")
def isolated_workspace_dir(tmp_path_factory: pytest.TempPathFactory) -> None:
    """Redirect all workspace storage to a temp dir for the entire test session.

    Any code that calls get_workspace_dir() (SQLiteRunStore, SQLiteArtifactStore,
    Workspace, etc.) will receive the temp path instead of ~/.ag/workspaces/.
    This prevents test artifacts from polluting the user's real workspace listing.
    """
    tmpdir = tmp_path_factory.mktemp("ag_workspaces")
    prev = os.environ.get("AG_WORKSPACE_DIR")
    os.environ["AG_WORKSPACE_DIR"] = str(tmpdir)
    yield
    if prev is None:
        del os.environ["AG_WORKSPACE_DIR"]
    else:
        os.environ["AG_WORKSPACE_DIR"] = prev


@pytest.fixture(autouse=True)
def _fake_llm_provider(request):
    """Patch get_provider globally so no test makes real LLM calls (AF-0125).

    Tests marked @pytest.mark.integration or @pytest.mark.manual opt out
    and receive the real provider selection logic.
    """
    markers = {m.name for m in request.node.iter_markers()}
    if "integration" in markers or "manual" in markers:
        yield
        return

    from ag.providers.stubs import FakeLLMProvider

    fake = FakeLLMProvider()
    with (
        patch("ag.providers.registry.get_provider", return_value=fake),
        patch("ag.providers.get_provider", return_value=fake),
        patch("ag.core.orchestrator.get_provider", return_value=fake),
    ):
        yield
