"""Playbooks module — orchestration playbook definitions.

AF-0068: Skills/playbooks folder restructure.

This module contains all playbook definitions and the playbook registry.
Each playbook is defined in its own file for maintainability.

Available playbooks:
- default_v0: Simple linear execution (analyze → execute → verify)
- delegate_v0: Multi-step delegation with subtask planning (AF-0019)
- summarize_v0: Document summarization pipeline (AF-0065)

Usage:
    from ag.playbooks import get_playbook, list_playbooks

    # Get a specific playbook
    playbook = get_playbook("default_v0")

    # List all available playbooks
    names = list_playbooks()  # ["default_v0", "delegate_v0", "summarize_v0"]
"""

from ag.playbooks.default_v0 import DEFAULT_V0
from ag.playbooks.delegate_v0 import DELEGATE_V0
from ag.playbooks.registry import get_playbook, list_playbooks
from ag.playbooks.summarize_v0 import SUMMARIZE_V0

__all__ = [
    # Playbook instances
    "DEFAULT_V0",
    "DELEGATE_V0",
    "SUMMARIZE_V0",
    # Registry functions
    "get_playbook",
    "list_playbooks",
]
