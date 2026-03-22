"""Pytest configuration and shared fixtures (AF-0096).

Session-level workspace isolation: redirects all workspace I/O away
from ~/.ag/workspaces/ so no test artifacts leak into the user's
real workspace directory.
"""

from __future__ import annotations

import os
import warnings

import pytest

# Suppress SSL-socket GC noise from ddgs/DuckDuckGo Cloudflare connections.
# These sockets are created by tests that mock DDGS but the underlying
# primp/httpx client may still open a connection on import; when Python's GC
# finalizes the socket, pytest turns the ResourceWarning into
# PytestUnraisableExceptionWarning — even under `-W error`.
# This filter is inserted early (before CLI flags) so it wins.
warnings.filterwarnings("ignore", category=pytest.PytestUnraisableExceptionWarning)


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
