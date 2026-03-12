"""Drift detection tests for contract and schema documentation (AF0013, AF0063).

These tests ensure documentation stays in sync with implementation:
1. All Protocols in interface modules are documented in CONTRACT_INVENTORY.md
2. All Pydantic models are documented in SCHEMA_INVENTORY.md

Run these tests to catch documentation drift before it accumulates.
"""

from __future__ import annotations

import inspect
from pathlib import Path
from typing import Protocol

import pytest
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# Contract Drift Detection (AF0013)
# ---------------------------------------------------------------------------


class TestContractInventoryDrift:
    """Ensure all Protocols are documented in CONTRACT_INVENTORY.md."""

    @pytest.fixture
    def contract_inventory_content(self) -> str:
        """Load CONTRACT_INVENTORY.md content."""
        path = Path("docs/dev/additional/CONTRACT_INVENTORY.md")
        if not path.exists():
            pytest.skip("CONTRACT_INVENTORY.md not yet created")
        return path.read_text(encoding="utf-8")

    def _get_protocols_from_module(self, module: object) -> list[str]:
        """Extract Protocol class names from a module."""
        protocols = []
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # Check if it's a Protocol (has _is_protocol attribute or is Protocol subclass)
            if name == "Protocol":
                continue
            if hasattr(obj, "_is_protocol") and obj._is_protocol:
                protocols.append(name)
            elif hasattr(obj, "__mro__") and Protocol in obj.__mro__ and obj is not Protocol:
                protocols.append(name)
        return protocols

    def test_core_interfaces_documented(self, contract_inventory_content: str) -> None:
        """All Protocols in core/interfaces.py should be documented."""
        from ag.core import interfaces

        protocols = self._get_protocols_from_module(interfaces)
        assert protocols, "No protocols found in core/interfaces.py"

        missing = [p for p in protocols if p not in contract_inventory_content]
        assert not missing, f"Undocumented protocols in core/interfaces.py: {missing}"

    def test_storage_interfaces_documented(self, contract_inventory_content: str) -> None:
        """All Protocols in storage/interfaces.py should be documented."""
        from ag.storage import interfaces

        protocols = self._get_protocols_from_module(interfaces)
        assert protocols, "No protocols found in storage/interfaces.py"

        missing = [p for p in protocols if p not in contract_inventory_content]
        assert not missing, f"Undocumented protocols in storage/interfaces.py: {missing}"

    def test_provider_protocols_documented(self, contract_inventory_content: str) -> None:
        """LLMProvider Protocol should be documented."""
        from ag.providers import base

        protocols = self._get_protocols_from_module(base)
        # LLMProvider should be there
        assert "LLMProvider" in protocols or "LLMProvider" in contract_inventory_content

        missing = [p for p in protocols if p not in contract_inventory_content]
        assert not missing, f"Undocumented protocols in providers/base.py: {missing}"


# ---------------------------------------------------------------------------
# Schema Drift Detection (AF0063)
# ---------------------------------------------------------------------------


class TestSchemaInventoryDrift:
    """Ensure all Pydantic models are documented in SCHEMA_INVENTORY.md."""

    @pytest.fixture
    def schema_inventory_content(self) -> str:
        """Load SCHEMA_INVENTORY.md content."""
        path = Path("docs/dev/additional/SCHEMA_INVENTORY.md")
        if not path.exists():
            pytest.skip("SCHEMA_INVENTORY.md not yet created")
        return path.read_text(encoding="utf-8")

    def _get_pydantic_models_from_module(self, module: object) -> list[str]:
        """Extract Pydantic BaseModel class names from a module."""
        models = []
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name == "BaseModel":
                continue
            # Check if it's a Pydantic model
            if (
                hasattr(obj, "__mro__")
                and BaseModel in obj.__mro__
                and obj is not BaseModel
                # Exclude private classes
                and not name.startswith("_")
            ):
                models.append(name)
        return models

    def test_task_spec_schemas_documented(self, schema_inventory_content: str) -> None:
        """All Pydantic models in task_spec.py should be documented."""
        from ag.core import task_spec

        models = self._get_pydantic_models_from_module(task_spec)
        assert models, "No Pydantic models found in task_spec.py"

        missing = [m for m in models if m not in schema_inventory_content]
        assert not missing, f"Undocumented schemas in task_spec.py: {missing}"

    def test_run_trace_schemas_documented(self, schema_inventory_content: str) -> None:
        """All Pydantic models in run_trace.py should be documented."""
        from ag.core import run_trace

        models = self._get_pydantic_models_from_module(run_trace)
        assert models, "No Pydantic models found in run_trace.py"

        missing = [m for m in models if m not in schema_inventory_content]
        assert not missing, f"Undocumented schemas in run_trace.py: {missing}"

    def test_playbook_schemas_documented(self, schema_inventory_content: str) -> None:
        """All Pydantic models in playbook.py should be documented."""
        from ag.core import playbook

        models = self._get_pydantic_models_from_module(playbook)
        assert models, "No Pydantic models found in playbook.py"

        missing = [m for m in models if m not in schema_inventory_content]
        assert not missing, f"Undocumented schemas in playbook.py: {missing}"

    def test_schema_verifier_schemas_documented(self, schema_inventory_content: str) -> None:
        """All Pydantic models in schema_verifier.py should be documented."""
        from ag.core import schema_verifier

        models = self._get_pydantic_models_from_module(schema_verifier)
        assert models, "No Pydantic models found in schema_verifier.py"

        missing = [m for m in models if m not in schema_inventory_content]
        assert not missing, f"Undocumented schemas in schema_verifier.py: {missing}"

    def test_skill_base_schemas_documented(self, schema_inventory_content: str) -> None:
        """All Pydantic models in skills/base.py should be documented."""
        from ag.skills import base

        models = self._get_pydantic_models_from_module(base)
        assert models, "No Pydantic models found in skills/base.py"

        missing = [m for m in models if m not in schema_inventory_content]
        assert not missing, f"Undocumented schemas in skills/base.py: {missing}"

    def test_all_registered_skill_schemas_documented(
        self, schema_inventory_content: str
    ) -> None:
        """All Pydantic schemas from registered skills should be documented (AF0081).

        This test ensures that when new skills are added to the registry,
        their input/output schemas are also documented in SCHEMA_INVENTORY.md.
        """
        from ag.skills import get_default_registry

        registry = get_default_registry()
        missing: list[str] = []

        for skill_name in registry.list():
            info = registry.get_info(skill_name)
            if info is None:
                continue

            # Check input schema (info returns JSON schema dict with 'title' as class name)
            input_schema = info.get("input_schema")
            if input_schema and isinstance(input_schema, dict):
                input_name = input_schema.get("title", "")
                if input_name and input_name not in schema_inventory_content:
                    missing.append(f"{skill_name}:input:{input_name}")

            # Check output schema
            output_schema = info.get("output_schema")
            if output_schema and isinstance(output_schema, dict):
                output_name = output_schema.get("title", "")
                if output_name and output_name not in schema_inventory_content:
                    missing.append(f"{skill_name}:output:{output_name}")

        assert not missing, f"Undocumented skill schemas: {missing}"


# ---------------------------------------------------------------------------
# Contract Implementation Drift Detection (AF0081)
# ---------------------------------------------------------------------------


class TestContractImplementationDrift:
    """Ensure all registered skills are documented in CONTRACT_INVENTORY.md."""

    @pytest.fixture
    def contract_inventory_content(self) -> str:
        """Load CONTRACT_INVENTORY.md content."""
        path = Path("docs/dev/additional/CONTRACT_INVENTORY.md")
        if not path.exists():
            pytest.skip("CONTRACT_INVENTORY.md not yet created")
        return path.read_text(encoding="utf-8")

    def test_all_registered_skills_documented(
        self, contract_inventory_content: str
    ) -> None:
        """All skills in registry should be documented in CONTRACT_INVENTORY.md (AF0081).

        This test ensures that when new skills are registered, they are also
        documented in the Skill Implementations table.
        """
        from ag.skills import get_default_registry

        registry = get_default_registry()
        missing: list[str] = []

        for skill_name in registry.list():
            # Check if skill name appears in the contract inventory
            if skill_name not in contract_inventory_content:
                missing.append(skill_name)

        assert not missing, f"Undocumented skills in CONTRACT_INVENTORY.md: {missing}"
