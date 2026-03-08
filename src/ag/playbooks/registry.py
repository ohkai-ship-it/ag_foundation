"""Playbook registry — centralized playbook access.

AF-0068: Playbooks folder restructure.
Provides get_playbook() and list_playbooks() functions.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ag.core.playbook import Playbook

from ag.playbooks.default_v0 import DEFAULT_V0
from ag.playbooks.delegate_v0 import DELEGATE_V0
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


def list_playbooks() -> list[str]:
    """List available playbook names (excluding aliases).

    Returns:
        List of canonical playbook names
    """
    return ["default_v0", "delegate_v0", "summarize_v0"]
