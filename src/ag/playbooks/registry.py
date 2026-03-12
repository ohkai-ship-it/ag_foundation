"""Playbook registry — centralized playbook access.

AF-0068: Playbooks folder restructure.
AF-0074: Added research_v0 playbook.
AF-0078: Plugin architecture — entry point discovery and YAML loading.

Provides get_playbook() and list_playbooks() functions.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from importlib.metadata import entry_points
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ag.core.playbook import Playbook

logger = logging.getLogger(__name__)

# Entry point group name for playbook plugins
PLAYBOOK_ENTRY_POINT_GROUP = "ag.playbooks"


@dataclass
class PlaybookInfo:
    """Metadata about a registered playbook (AF0078).

    Attributes:
        name: Playbook name (canonical, without alias)
        playbook: The Playbook instance
        source: Origin - "built-in", "entry-point", or "yaml"
        source_path: Path to YAML file (for yaml source), None otherwise
    """

    name: str
    playbook: "Playbook"
    source: str = "built-in"
    source_path: Path | None = None
    aliases: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Playbook Registry (AF0078: Plugin Architecture)
# ---------------------------------------------------------------------------

# Internal registry: canonical name -> PlaybookInfo
_REGISTRY: dict[str, PlaybookInfo] = {}

# Alias mapping: alias -> canonical name
_ALIASES: dict[str, str] = {}

# Initialization flag
_INITIALIZED = False


def _register_playbook(
    playbook: "Playbook",
    *,
    source: str = "built-in",
    source_path: Path | None = None,
    aliases: list[str] | None = None,
) -> None:
    """Register a playbook in the registry.

    Args:
        playbook: The Playbook instance
        source: Origin - "built-in", "entry-point", or "yaml"
        source_path: Path to source file (for yaml)
        aliases: Optional list of alias names
    """
    canonical_name = playbook.name
    alias_list = aliases or []

    # Check for conflicts
    if canonical_name in _REGISTRY:
        logger.warning(
            "Playbook %r already registered, skipping (source: %s)",
            canonical_name,
            source,
        )
        return

    # Register canonical name
    _REGISTRY[canonical_name] = PlaybookInfo(
        name=canonical_name,
        playbook=playbook,
        source=source,
        source_path=source_path,
        aliases=alias_list,
    )

    # Register aliases
    for alias in alias_list:
        if alias in _ALIASES or alias in _REGISTRY:
            logger.warning(
                "Alias %r conflicts with existing name/alias, skipping",
                alias,
            )
            continue
        _ALIASES[alias] = canonical_name


def _discover_entrypoint_playbooks() -> None:
    """Discover and register playbooks from Python entry points (AF0078).

    Entry points allow external packages to register playbooks via pyproject.toml:

        [project.entry-points."ag.playbooks"]
        my_playbook = "my_package.playbooks:MY_PLAYBOOK_V0"

    After `pip install`, the playbook is automatically discovered.
    """
    from ag.core.playbook import Playbook

    eps = entry_points(group=PLAYBOOK_ENTRY_POINT_GROUP)

    for ep in eps:
        try:
            playbook = ep.load()

            # Validate it's a Playbook
            if not isinstance(playbook, Playbook):
                logger.warning(
                    "Entry point %r is not a Playbook instance, skipping",
                    ep.name,
                )
                continue

            # Derive alias from name (remove _v0 suffix if present)
            aliases = []
            if playbook.name.endswith("_v0"):
                aliases.append(playbook.name[:-3])

            _register_playbook(playbook, source="entry-point", aliases=aliases)
            logger.debug("Registered entry-point playbook: %s", playbook.name)

        except Exception:
            logger.warning(
                "Failed to load playbook entry point %r",
                ep.name,
                exc_info=True,
            )


def _load_yaml_playbook(path: Path) -> "Playbook | None":
    """Load a playbook from a YAML file.

    Args:
        path: Path to the YAML file

    Returns:
        Playbook instance if valid, None if invalid
    """
    try:
        import yaml
    except ImportError:
        logger.warning("PyYAML not installed, cannot load YAML playbooks")
        return None

    from ag.core.playbook import Playbook

    try:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict):
            logger.warning("YAML file %s does not contain a mapping", path)
            return None

        return Playbook.model_validate(data)

    except Exception as e:
        logger.warning("Failed to load YAML playbook from %s: %s", path, e)
        return None


def _discover_yaml_playbooks() -> None:
    """Discover and register playbooks from ~/.ag/playbooks/ directory."""
    playbooks_dir = Path.home() / ".ag" / "playbooks"

    if not playbooks_dir.exists():
        return

    for yaml_file in playbooks_dir.glob("*.yaml"):
        playbook = _load_yaml_playbook(yaml_file)
        if playbook is None:
            continue

        # Derive alias from name
        aliases = []
        if playbook.name.endswith("_v0"):
            aliases.append(playbook.name[:-3])

        _register_playbook(
            playbook,
            source="yaml",
            source_path=yaml_file,
            aliases=aliases,
        )
        logger.debug("Registered YAML playbook: %s from %s", playbook.name, yaml_file)


def _initialize_registry() -> None:
    """Initialize the playbook registry (lazy initialization)."""
    global _INITIALIZED

    if _INITIALIZED:
        return

    # 1. Discover entry-point playbooks (includes built-in via pyproject.toml)
    _discover_entrypoint_playbooks()

    # 2. Discover user YAML playbooks (can override entry-point playbooks)
    _discover_yaml_playbooks()

    _INITIALIZED = True


def reset_registry() -> None:
    """Reset the registry (for testing)."""
    global _INITIALIZED
    _REGISTRY.clear()
    _ALIASES.clear()
    _INITIALIZED = False


def get_playbook(name: str) -> "Playbook | None":
    """Get a playbook by name or alias.

    Args:
        name: Playbook name or alias (e.g., "default_v0" or "default")

    Returns:
        Playbook if found, None otherwise
    """
    _initialize_registry()

    # Try canonical name first
    if name in _REGISTRY:
        return _REGISTRY[name].playbook

    # Try alias
    canonical = _ALIASES.get(name)
    if canonical and canonical in _REGISTRY:
        return _REGISTRY[canonical].playbook

    return None


def get_playbook_entry(name: str) -> PlaybookInfo | None:
    """Get playbook info entry by name or alias.

    Args:
        name: Playbook name or alias

    Returns:
        PlaybookInfo if found, None otherwise
    """
    _initialize_registry()

    if name in _REGISTRY:
        return _REGISTRY[name]

    canonical = _ALIASES.get(name)
    if canonical and canonical in _REGISTRY:
        return _REGISTRY[canonical]

    return None


def list_playbooks() -> list[str]:
    """List available playbook names (excluding aliases).

    Returns:
        Sorted list of canonical playbook names
    """
    _initialize_registry()
    return sorted(_REGISTRY.keys())


def get_playbook_info(name: str) -> dict[str, Any] | None:
    """Get playbook metadata for display.

    Args:
        name: Canonical playbook name or alias

    Returns:
        Dict with name, version, description, stability, source, or None if not found
    """
    entry = get_playbook_entry(name)
    if entry is None:
        return None

    playbook = entry.playbook
    return {
        "name": playbook.name,
        "version": playbook.version,
        "description": playbook.description or "",
        "stability": (
            playbook.metadata.get("stability", "unknown") if playbook.metadata else "unknown"
        ),
        "source": entry.source,
        "source_path": str(entry.source_path) if entry.source_path else None,
    }


def list_playbooks_detailed() -> list[dict[str, Any]]:
    """List all playbooks with metadata.

    Returns:
        List of playbook info dicts, sorted by name
    """
    _initialize_registry()
    result = []
    for name in list_playbooks():
        info = get_playbook_info(name)
        if info:
            result.append(info)
    return result


def register_playbook(
    playbook: "Playbook",
    *,
    source: str = "built-in",
) -> None:
    """Register a playbook (public API for tests and dynamic registration).

    Args:
        playbook: The Playbook instance
        source: Origin - "built-in", "test", etc.
    """
    _initialize_registry()

    # Derive alias from name
    aliases = []
    if playbook.name.endswith("_v0"):
        aliases.append(playbook.name[:-3])

    _register_playbook(playbook, source=source, aliases=aliases)


def unregister_playbook(name: str) -> bool:
    """Unregister a playbook by name (for test cleanup).

    Args:
        name: Canonical playbook name

    Returns:
        True if playbook was removed, False if not found
    """
    _initialize_registry()

    if name not in _REGISTRY:
        return False

    info = _REGISTRY[name]

    # Remove aliases
    for alias in info.aliases:
        if alias in _ALIASES:
            del _ALIASES[alias]

    # Remove canonical entry
    del _REGISTRY[name]
    return True
