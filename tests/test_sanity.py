"""
Sanity tests for ag_foundation.

These tests verify that the package is properly installed and imports work.
"""

import pytest


def test_import_ag():
    """Test that the main package can be imported."""
    import ag

    assert ag.__version__ == "0.1.0"


def test_import_cli():
    """Test that the CLI module can be imported."""
    from ag.cli import main

    assert main.app is not None


def test_import_core():
    """Test that the core module can be imported."""
    from ag import core

    assert core is not None


def test_import_storage():
    """Test that the storage module can be imported."""
    from ag import storage

    assert storage is not None


def test_import_skills():
    """Test that the skills module can be imported."""
    from ag import skills

    assert skills is not None


def test_import_config():
    """Test that the config module can be imported and has expected constants."""
    from ag import config

    assert config.DEFAULT_CONFIG_DIR is not None
    assert config.DEFAULT_CONFIG_FILE is not None
    assert config.CONFIG_PATH_ENV_VAR == "AG_CONFIG_PATH"
