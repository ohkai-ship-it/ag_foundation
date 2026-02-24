"""
ag configuration contract.

This module defines the configuration contract for ag_foundation.
Actual config file parsing is NOT implemented in v0 (AF-0010).
This file documents:
  - Config file location(s)
  - Expected schema structure
  - Environment variable overrides

Future AF items will implement real parsing.
"""

import os
from pathlib import Path
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────────
# Config file locations (contract)
# ─────────────────────────────────────────────────────────────────────────────

# Default config file location: ~/.ag/config.yaml
# Can be overridden via AG_CONFIG_PATH environment variable.

DEFAULT_CONFIG_DIR = Path.home() / ".ag"
DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / "config.yaml"
CONFIG_PATH_ENV_VAR = "AG_CONFIG_PATH"


def get_config_path() -> Path:
    """
    Return the config file path.

    Resolution order:
    1. AG_CONFIG_PATH environment variable (if set)
    2. ~/.ag/config.yaml (default)
    """
    env_path = os.environ.get(CONFIG_PATH_ENV_VAR)
    if env_path:
        return Path(env_path)
    return DEFAULT_CONFIG_FILE


# ─────────────────────────────────────────────────────────────────────────────
# Config schema contract (placeholder — not parsed yet)
# ─────────────────────────────────────────────────────────────────────────────

# Expected YAML structure (v0.1):
#
# ```yaml
# # ag_foundation config file
# # Location: ~/.ag/config.yaml
#
# version: "0.1"
#
# # Default workspace (created on first run if not exists)
# workspaces:
#   default: "ws_default"
#   directory: "~/.ag/workspaces"  # where workspace data is stored
#
# # LLM provider configuration (placeholder — not used in manual mode)
# providers:
#   llm:
#     # Provider type: openai, anthropic, azure, local, etc.
#     provider: "openai"
#     api_key: ""           # placeholder, set via env var preferred: AG_LLM_API_KEY
#     model: "gpt-4"        # default model
#     # Optional overrides
#     base_url: null        # for custom endpoints
#     timeout: 60           # seconds
#
# # Telemetry (optional)
# telemetry:
#   enabled: false
#   export: "none"          # none | otel | langfuse
#
# # Defaults applied to TaskSpec when not overridden
# defaults:
#   playbook: "default_v0"
#   reasoning_mode: "balanced"
#   budgets:
#     max_steps: 12
#     max_retries: 2
#     max_tool_calls: 40
#     max_tokens_estimate: 60000
# ```

# ─────────────────────────────────────────────────────────────────────────────
# Environment variable overrides (contract)
# ─────────────────────────────────────────────────────────────────────────────

# These environment variables override config file values:
#
# AG_CONFIG_PATH     — Override config file location
# AG_WORKSPACE       — Override default workspace
# AG_WORKSPACE_DIR   — Override workspace storage directory
# AG_LLM_API_KEY     — Override LLM provider API key (preferred over config file)
# AG_LLM_MODEL       — Override default model
# AG_DEV             — Enable dev mode (required for --mode manual)
# AG_TELEMETRY       — Enable/disable telemetry (0/1)

ENV_VARS = {
    "AG_CONFIG_PATH": "Override config file location",
    "AG_WORKSPACE": "Override default workspace",
    "AG_WORKSPACE_DIR": "Override workspace storage directory",
    "AG_LLM_API_KEY": "LLM provider API key",
    "AG_LLM_MODEL": "Override default model",
    "AG_DEV": "Enable dev mode (required for --mode manual)",
    "AG_TELEMETRY": "Enable/disable telemetry (0/1)",
}


# ─────────────────────────────────────────────────────────────────────────────
# Placeholder functions (stubs for future implementation)
# ─────────────────────────────────────────────────────────────────────────────


def load_config() -> dict:
    """
    Load and parse config file.

    NOT IMPLEMENTED in v0 (AF-0010).
    Returns empty dict as placeholder.
    """
    # TODO: Implement in future AF item
    # - Parse YAML file from get_config_path()
    # - Apply environment variable overrides
    # - Validate against schema
    # - Return typed config object
    return {}


def get_workspace_dir() -> Path:
    """
    Return the workspace storage directory.

    Resolution order:
    1. AG_WORKSPACE_DIR environment variable
    2. Config file workspaces.directory
    3. ~/.ag/workspaces (default)
    """
    env_dir = os.environ.get("AG_WORKSPACE_DIR")
    if env_dir:
        return Path(env_dir)
    # TODO: Check config file when implemented
    return DEFAULT_CONFIG_DIR / "workspaces"


def get_default_workspace() -> str:
    """
    Return the default workspace ID.

    Resolution order:
    1. AG_WORKSPACE environment variable
    2. Config file workspaces.default
    3. "ws_default" (default)
    """
    env_ws = os.environ.get("AG_WORKSPACE")
    if env_ws:
        return env_ws
    # TODO: Check config file when implemented
    return "ws_default"
