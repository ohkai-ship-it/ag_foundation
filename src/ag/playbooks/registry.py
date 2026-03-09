"""Playbook registry — centralized playbook access.

AF-0068: Playbooks folder restructure.
AF-0074: Added research_v0 playbook.
Provides get_playbook() and list_playbooks() functions.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ag.core.playbook import Playbook

from ag.playbooks.default_v0 import DEFAULT_V0
from ag.playbooks.delegate_v0 import DELEGATE_V0
from ag.playbooks.research_v0 import RESEARCH_V0
from ag.playbooks.summarize_v0 import SUMMARIZE_V0

# ---------------------------------------------------------------------------
# Playbook Registry
# ---------------------------------------------------------------------------

_REGISTRY: dict[str, "Playbook"] = {
    # Default playbook
    "default_v0": DEFAULT_V0,
    "default": DEFAULT_V0,  # Alias
    # Delegation playbook
    "delegate_v0": DELEGATE_V0,
    "delegate": DELEGATE_V0,  # Alias
    # Research playbook (AF-0074)
    "research_v0": RESEARCH_V0,
    "research": RESEARCH_V0,  # Alias
    # Summarization playbook
    "summarize_v0": SUMMARIZE_V0,
    "summarize": SUMMARIZE_V0,  # Alias
}


def get_playbook(name: str) -> "Playbook | None":
    """Get a playbook by name.

    Args:
        name: Playbook name or alias (e.g., "default_v0" or "default")

    Returns:
        Playbook if found, None otherwise
    """
    return _REGISTRY.get(name)


def _is_alias(name: str) -> bool:
    """Check if name is an alias (doesn't end with _v0)."""
    return not name.endswith("_v0")


def list_playbooks() -> list[str]:
    """List available playbook names (excluding aliases).

    Returns:
        Sorted list of canonical playbook names (auto-derived from registry)
    """
    return sorted(name for name in _REGISTRY if not _is_alias(name))


def get_playbook_info(name: str) -> dict[str, str | None] | None:
    """Get playbook metadata for display.

    Args:
        name: Canonical playbook name (not alias)

    Returns:
        Dict with name, version, description, stability, or None if not found
    """
    playbook = _REGISTRY.get(name)
    if playbook is None:
        return None

    return {
        "name": playbook.name,
        "version": playbook.version,
        "description": playbook.description or "",
        "stability": (
            playbook.metadata.get("stability", "unknown") if playbook.metadata else "unknown"
        ),
    }


def list_playbooks_detailed() -> list[dict[str, str | None]]:
    """List all playbooks with metadata.

    Returns:
        List of playbook info dicts, sorted by name
    """
    result = []
    for name in list_playbooks():
        info = get_playbook_info(name)
        if info:
            result.append(info)
    return result
