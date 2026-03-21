"""Tests for ExecutionPlan schema, plan storage, and plan CLI commands (AF-0098)."""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from ag.cli.main import app
from ag.core import (
    ExecutionPlan,
    PlannedStep,
    PlanStatus,
    Playbook,
    PlaybookStep,
    PlaybookStepType,
    PolicyFlag,
    create_execution_plan,
)
from ag.storage import FilePlanStore, Workspace

runner = CliRunner()


# ---------------------------------------------------------------------------
# ExecutionPlan Schema Tests
# ---------------------------------------------------------------------------


class TestExecutionPlanSchema:
    """Tests for ExecutionPlan schema."""

    def test_execution_plan_minimal(self) -> None:
        """ExecutionPlan can be created with minimal fields."""
        playbook = Playbook(name="test", version="1.0")
        plan = ExecutionPlan(
            plan_id="plan_123",
            workspace_id="test-ws",
            task_prompt="Test task",
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
            playbook=playbook,
        )
        assert plan.plan_id == "plan_123"
        assert plan.status == PlanStatus.PENDING
        assert plan.plan_version == "0.1"

    def test_execution_plan_full(self) -> None:
        """ExecutionPlan with all fields."""
        playbook = Playbook(name="test", version="1.0")
        now = datetime.now(timezone.utc)
        plan = ExecutionPlan(
            plan_id="plan_456",
            workspace_id="demo",
            task_prompt="Research Berlin history",
            status=PlanStatus.PENDING,
            created_at=now,
            expires_at=now + timedelta(hours=2),
            planned_steps=[
                PlannedStep(
                    step_number=1,
                    skill_name="web_search",
                    description="Find sources",
                    estimated_tokens=500,
                    policy_flags=[PolicyFlag.EXTERNAL_API],
                )
            ],
            total_estimated_tokens=5000,
            confidence=0.85,
            warnings=["Consider rate limits"],
            playbook=playbook,
        )
        assert len(plan.planned_steps) == 1
        assert plan.planned_steps[0].skill_name == "web_search"
        assert plan.confidence == 0.85

    def test_plan_is_expired_false(self) -> None:
        """is_expired returns False when not expired."""
        playbook = Playbook(name="test", version="1.0")
        plan = ExecutionPlan(
            plan_id="plan_123",
            workspace_id="test-ws",
            task_prompt="Test",
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
            playbook=playbook,
        )
        assert plan.is_expired() is False

    def test_plan_is_expired_true(self) -> None:
        """is_expired returns True when expired."""
        playbook = Playbook(name="test", version="1.0")
        plan = ExecutionPlan(
            plan_id="plan_123",
            workspace_id="test-ws",
            task_prompt="Test",
            expires_at=datetime.now(timezone.utc) - timedelta(hours=1),
            playbook=playbook,
        )
        assert plan.is_expired() is True

    def test_plan_is_actionable(self) -> None:
        """is_actionable returns True for pending non-expired plans."""
        playbook = Playbook(name="test", version="1.0")
        plan = ExecutionPlan(
            plan_id="plan_123",
            workspace_id="test-ws",
            task_prompt="Test",
            status=PlanStatus.PENDING,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
            playbook=playbook,
        )
        assert plan.is_actionable() is True

    def test_plan_is_actionable_false_when_expired(self) -> None:
        """is_actionable returns False when plan is expired."""
        playbook = Playbook(name="test", version="1.0")
        plan = ExecutionPlan(
            plan_id="plan_123",
            workspace_id="test-ws",
            task_prompt="Test",
            status=PlanStatus.PENDING,
            expires_at=datetime.now(timezone.utc) - timedelta(hours=1),
            playbook=playbook,
        )
        assert plan.is_actionable() is False

    def test_plan_serialization(self) -> None:
        """ExecutionPlan serializes to JSON and back."""
        playbook = Playbook(name="test", version="1.0")
        plan = ExecutionPlan(
            plan_id="plan_serialize",
            workspace_id="test-ws",
            task_prompt="Test serialization",
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
            playbook=playbook,
            planned_steps=[
                PlannedStep(
                    step_number=1,
                    skill_name="test_skill",
                    estimated_tokens=100,
                )
            ],
        )

        json_str = plan.to_json()
        restored = ExecutionPlan.from_json(json_str)

        assert restored.plan_id == plan.plan_id
        assert restored.task_prompt == plan.task_prompt
        assert len(restored.planned_steps) == 1


class TestCreateExecutionPlan:
    """Tests for create_execution_plan helper."""

    def test_create_from_playbook(self) -> None:
        """create_execution_plan builds plan from playbook."""
        playbook = Playbook(
            name="test_playbook",
            version="1.0",
            steps=[
                PlaybookStep(
                    step_id="s1",
                    name="Search",
                    step_type=PlaybookStepType.SKILL,
                    skill_name="web_search",
                    parameters={"estimated_tokens": 500},
                ),
                PlaybookStep(
                    step_id="s2",
                    name="Emit",
                    step_type=PlaybookStepType.SKILL,
                    skill_name="emit_result",
                    parameters={"estimated_tokens": 100},
                ),
            ],
        )

        plan = create_execution_plan(
            plan_id="plan_test",
            workspace_id="test-ws",
            task_prompt="Test task",
            playbook=playbook,
            confidence=0.9,
            warnings=["Test warning"],
        )

        assert plan.plan_id == "plan_test"
        assert len(plan.planned_steps) == 2
        assert plan.planned_steps[0].skill_name == "web_search"
        assert plan.confidence == 0.9
        assert plan.warnings == ["Test warning"]

    def test_create_with_policy_flags(self) -> None:
        """create_execution_plan applies policy flags from map."""
        playbook = Playbook(
            name="flagged",
            version="1.0",
            steps=[
                PlaybookStep(
                    step_id="s1",
                    name="Search",
                    step_type=PlaybookStepType.SKILL,
                    skill_name="web_search",
                ),
            ],
        )

        skill_flags = {
            "web_search": [PolicyFlag.EXTERNAL_API, PolicyFlag.NETWORK],
        }

        plan = create_execution_plan(
            plan_id="plan_flags",
            workspace_id="test-ws",
            task_prompt="Test",
            playbook=playbook,
            skill_policy_flags=skill_flags,
        )

        assert PolicyFlag.EXTERNAL_API in plan.planned_steps[0].policy_flags
        assert PolicyFlag.NETWORK in plan.planned_steps[0].policy_flags

    def test_create_with_custom_ttl(self) -> None:
        """create_execution_plan respects custom TTL."""
        playbook = Playbook(name="test", version="1.0")

        plan = create_execution_plan(
            plan_id="plan_ttl",
            workspace_id="test-ws",
            task_prompt="Test",
            playbook=playbook,
            ttl_seconds=7200,  # 2 hours
        )

        # Plan should expire approximately 2 hours from now
        expected_delta = timedelta(seconds=7200)
        actual_delta = plan.expires_at - plan.created_at
        assert abs((actual_delta - expected_delta).total_seconds()) < 5


# ---------------------------------------------------------------------------
# FilePlanStore Tests
# ---------------------------------------------------------------------------


class TestFilePlanStore:
    """Tests for FilePlanStore."""

    @pytest.fixture
    def temp_workspaces(self, tmp_path: Path) -> Path:
        """Create temp workspaces directory."""
        ws_root = tmp_path / "workspaces"
        ws_root.mkdir()
        return ws_root

    @pytest.fixture
    def plan_store(self, temp_workspaces: Path) -> FilePlanStore:
        """Create plan store with temp directory."""
        return FilePlanStore(temp_workspaces)

    @pytest.fixture
    def sample_plan(self) -> ExecutionPlan:
        """Create a sample plan for testing."""
        playbook = Playbook(name="test", version="1.0")
        return ExecutionPlan(
            plan_id="plan_test123",
            workspace_id="test-workspace",
            task_prompt="Test task",
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
            playbook=playbook,
        )

    def test_save_and_get(self, plan_store: FilePlanStore, sample_plan: ExecutionPlan) -> None:
        """save persists plan, get retrieves it."""
        plan_store.save(sample_plan)
        retrieved = plan_store.get(sample_plan.workspace_id, sample_plan.plan_id)

        assert retrieved is not None
        assert retrieved.plan_id == sample_plan.plan_id
        assert retrieved.task_prompt == sample_plan.task_prompt

    def test_get_nonexistent_returns_none(self, plan_store: FilePlanStore) -> None:
        """get returns None for non-existent plan."""
        result = plan_store.get("nonexistent-ws", "nonexistent-plan")
        assert result is None

    def test_list_returns_plans(self, plan_store: FilePlanStore, temp_workspaces: Path) -> None:
        """list returns all non-expired plans."""
        ws_id = "list-test"
        playbook = Playbook(name="test", version="1.0")

        # Create multiple plans
        for i in range(3):
            plan = ExecutionPlan(
                plan_id=f"plan_{i}",
                workspace_id=ws_id,
                task_prompt=f"Task {i}",
                expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
                playbook=playbook,
            )
            plan_store.save(plan)

        plans = plan_store.list(ws_id)
        assert len(plans) == 3

    def test_list_excludes_expired(self, plan_store: FilePlanStore) -> None:
        """list excludes expired plans by default."""
        ws_id = "expire-test"
        playbook = Playbook(name="test", version="1.0")

        # Create one valid and one expired plan
        valid_plan = ExecutionPlan(
            plan_id="valid_plan",
            workspace_id=ws_id,
            task_prompt="Valid",
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
            playbook=playbook,
        )
        expired_plan = ExecutionPlan(
            plan_id="expired_plan",
            workspace_id=ws_id,
            task_prompt="Expired",
            expires_at=datetime.now(timezone.utc) - timedelta(hours=1),
            playbook=playbook,
        )

        plan_store.save(valid_plan)
        plan_store.save(expired_plan)

        plans = plan_store.list(ws_id, include_expired=False)
        assert len(plans) == 1
        assert plans[0].plan_id == "valid_plan"

    def test_list_includes_expired_when_requested(self, plan_store: FilePlanStore) -> None:
        """list includes expired plans when include_expired=True."""
        ws_id = "include-expired-test"
        playbook = Playbook(name="test", version="1.0")

        valid_plan = ExecutionPlan(
            plan_id="valid",
            workspace_id=ws_id,
            task_prompt="Valid",
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
            playbook=playbook,
        )
        expired_plan = ExecutionPlan(
            plan_id="expired",
            workspace_id=ws_id,
            task_prompt="Expired",
            expires_at=datetime.now(timezone.utc) - timedelta(hours=1),
            playbook=playbook,
        )

        plan_store.save(valid_plan)
        plan_store.save(expired_plan)

        plans = plan_store.list(ws_id, include_expired=True)
        assert len(plans) == 2

    def test_delete(self, plan_store: FilePlanStore, sample_plan: ExecutionPlan) -> None:
        """delete removes plan."""
        plan_store.save(sample_plan)
        deleted = plan_store.delete(sample_plan.workspace_id, sample_plan.plan_id)
        assert deleted is True

        # Verify deleted
        result = plan_store.get(sample_plan.workspace_id, sample_plan.plan_id)
        assert result is None

    def test_delete_nonexistent_returns_false(self, plan_store: FilePlanStore) -> None:
        """delete returns False for non-existent plan."""
        deleted = plan_store.delete("any-ws", "nonexistent")
        assert deleted is False

    def test_update_status(self, plan_store: FilePlanStore, sample_plan: ExecutionPlan) -> None:
        """update_status changes plan status."""
        plan_store.save(sample_plan)
        updated = plan_store.update_status(
            sample_plan.workspace_id,
            sample_plan.plan_id,
            PlanStatus.APPROVED.value,
        )
        assert updated is True

        retrieved = plan_store.get(sample_plan.workspace_id, sample_plan.plan_id)
        assert retrieved is not None
        assert retrieved.status == PlanStatus.APPROVED


# ---------------------------------------------------------------------------
# CLI Plan Commands Tests
# ---------------------------------------------------------------------------


class TestPlanCLI:
    """Tests for ag plan CLI commands."""

    @pytest.fixture
    def temp_workspaces(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
        """Create temp workspaces directory and patch config."""
        ws_root = tmp_path / "workspaces"
        ws_root.mkdir()
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(ws_root))
        return ws_root

    @pytest.fixture
    def test_workspace(self, temp_workspaces: Path) -> str:
        """Create a test workspace."""
        ws = Workspace("test-ws", temp_workspaces)
        ws.ensure_exists()
        return "test-ws"

    def test_plan_help(self) -> None:
        """ag plan --help shows available commands."""
        result = runner.invoke(app, ["plan", "--help"])
        assert result.exit_code == 0
        assert "generate" in result.output
        assert "show" in result.output
        assert "delete" in result.output
        assert "list" in result.output

    def test_plan_list_empty(self, temp_workspaces: Path, test_workspace: str) -> None:
        """ag plan list shows no plans when empty."""
        result = runner.invoke(app, ["plan", "list", "--workspace", test_workspace])
        assert result.exit_code == 0
        assert "No plans found" in result.output

    def test_plan_show_not_found(self, temp_workspaces: Path, test_workspace: str) -> None:
        """ag plan show with invalid plan_id fails."""
        result = runner.invoke(
            app,
            ["plan", "show", "nonexistent", "--workspace", test_workspace],
        )
        assert result.exit_code == 1
        assert "Error" in result.output

    def test_plan_delete_not_found(self, temp_workspaces: Path, test_workspace: str) -> None:
        """ag plan delete with invalid plan_id fails."""
        result = runner.invoke(
            app,
            ["plan", "delete", "nonexistent", "--workspace", test_workspace],
        )
        assert result.exit_code == 1
        assert "Error" in result.output

    def test_plan_list_requires_workspace(self) -> None:
        """ag plan list requires --workspace."""
        result = runner.invoke(app, ["plan", "list"])
        assert result.exit_code == 1
        assert "workspace" in result.output.lower()

    def test_plan_generate_requires_workspace(self) -> None:
        """ag plan generate requires --workspace."""
        result = runner.invoke(app, ["plan", "generate", "--task", "test task"])
        assert result.exit_code == 1
        assert "workspace" in result.output.lower()


class TestPlanCLIWithMockedPlanner:
    """Tests for ag plan generate with mocked V1Planner."""

    @pytest.fixture
    def temp_workspaces(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
        """Create temp workspaces directory and patch config."""
        ws_root = tmp_path / "workspaces"
        ws_root.mkdir()
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(ws_root))
        return ws_root

    @pytest.fixture
    def test_workspace(self, temp_workspaces: Path) -> str:
        """Create a test workspace."""
        ws = Workspace("plan-test-ws", temp_workspaces)
        ws.ensure_exists()
        return "plan-test-ws"

    def test_plan_generate_creates_plan(self, temp_workspaces: Path, test_workspace: str) -> None:
        """ag plan generate creates and saves a plan."""
        # Create a mock playbook response
        mock_playbook = Playbook(
            name="v1plan_test",
            version="1.0",
            steps=[
                PlaybookStep(
                    step_id="s1",
                    name="Search",
                    step_type=PlaybookStepType.SKILL,
                    skill_name="web_search",
                    parameters={"estimated_tokens": 500},
                ),
            ],
            metadata={"confidence": 0.85, "warnings": []},
        )

        with (
            patch("ag.providers.registry.get_provider") as mock_get_provider,
            patch("ag.core.planner.V1Planner") as mock_planner_cls,
        ):
            mock_provider = MagicMock()
            mock_get_provider.return_value = mock_provider
            mock_planner = MagicMock()
            mock_planner.plan.return_value = mock_playbook
            mock_planner_cls.return_value = mock_planner

            result = runner.invoke(
                app,
                [
                    "plan",
                    "generate",
                    "--task",
                    "Test task",
                    "--workspace",
                    test_workspace,
                ],
            )

            assert result.exit_code == 0
            assert "Plan saved" in result.output
            assert "plan_" in result.output

    def test_plan_generate_json_output(self, temp_workspaces: Path, test_workspace: str) -> None:
        """ag plan generate --json outputs JSON."""
        mock_playbook = Playbook(
            name="v1plan_test",
            version="1.0",
            metadata={"confidence": 0.9, "warnings": []},
        )

        with (
            patch("ag.providers.registry.get_provider") as mock_get_provider,
            patch("ag.core.planner.V1Planner") as mock_planner_cls,
        ):
            mock_provider = MagicMock()
            mock_get_provider.return_value = mock_provider
            mock_planner = MagicMock()
            mock_planner.plan.return_value = mock_playbook
            mock_planner_cls.return_value = mock_planner

            result = runner.invoke(
                app,
                [
                    "plan",
                    "generate",
                    "--task",
                    "Test task",
                    "--workspace",
                    test_workspace,
                    "--json",
                ],
            )

            assert result.exit_code == 0
            # Should be valid JSON
            data = json.loads(result.output)
            assert "plan_id" in data
            assert "task_prompt" in data

    def test_plan_show_after_generate(self, temp_workspaces: Path, test_workspace: str) -> None:
        """ag plan show displays generated plan."""
        mock_playbook = Playbook(
            name="v1plan_test",
            version="1.0",
            metadata={"confidence": 0.75, "warnings": []},
        )

        with (
            patch("ag.providers.registry.get_provider") as mock_get_provider,
            patch("ag.core.planner.V1Planner") as mock_planner_cls,
        ):
            mock_provider = MagicMock()
            mock_get_provider.return_value = mock_provider
            mock_planner = MagicMock()
            mock_planner.plan.return_value = mock_playbook
            mock_planner_cls.return_value = mock_planner

            # Generate plan first
            gen_result = runner.invoke(
                app,
                [
                    "plan",
                    "generate",
                    "--task",
                    "Show test",
                    "--workspace",
                    test_workspace,
                    "--json",
                ],
            )
            assert gen_result.exit_code == 0
            plan_data = json.loads(gen_result.output)
            plan_id = plan_data["plan_id"]

            # Now show the plan
            show_result = runner.invoke(
                app,
                ["plan", "show", plan_id, "--workspace", test_workspace],
            )

            assert show_result.exit_code == 0
            assert plan_id in show_result.output
            assert "Show test" in show_result.output

    def test_plan_delete_after_generate(self, temp_workspaces: Path, test_workspace: str) -> None:
        """ag plan delete removes generated plan."""
        mock_playbook = Playbook(
            name="v1plan_test",
            version="1.0",
            metadata={"confidence": 0.8, "warnings": []},
        )

        with (
            patch("ag.providers.registry.get_provider") as mock_get_provider,
            patch("ag.core.planner.V1Planner") as mock_planner_cls,
        ):
            mock_provider = MagicMock()
            mock_get_provider.return_value = mock_provider
            mock_planner = MagicMock()
            mock_planner.plan.return_value = mock_playbook
            mock_planner_cls.return_value = mock_planner

            # Generate plan first
            gen_result = runner.invoke(
                app,
                [
                    "plan",
                    "generate",
                    "--task",
                    "Delete test",
                    "--workspace",
                    test_workspace,
                    "--json",
                ],
            )
            assert gen_result.exit_code == 0
            plan_data = json.loads(gen_result.output)
            plan_id = plan_data["plan_id"]

            # Delete the plan
            del_result = runner.invoke(
                app,
                ["plan", "delete", plan_id, "--workspace", test_workspace],
            )

            assert del_result.exit_code == 0
            assert "Deleted" in del_result.output

            # Verify plan is gone
            show_result = runner.invoke(
                app,
                ["plan", "show", plan_id, "--workspace", test_workspace],
            )
            assert show_result.exit_code == 1

    def test_plan_list_shows_generated_plans(
        self, temp_workspaces: Path, test_workspace: str
    ) -> None:
        """ag plan list shows generated plans."""
        mock_playbook = Playbook(
            name="v1plan_test",
            version="1.0",
            steps=[
                PlaybookStep(
                    step_id="s1",
                    name="Test",
                    skill_name="emit_result",
                ),
            ],
            metadata={"confidence": 0.7, "warnings": []},
        )

        with (
            patch("ag.providers.registry.get_provider") as mock_get_provider,
            patch("ag.core.planner.V1Planner") as mock_planner_cls,
        ):
            mock_provider = MagicMock()
            mock_get_provider.return_value = mock_provider
            mock_planner = MagicMock()
            mock_planner.plan.return_value = mock_playbook
            mock_planner_cls.return_value = mock_planner

            # Generate a plan
            gen_result = runner.invoke(
                app,
                [
                    "plan",
                    "generate",
                    "--task",
                    "List test",
                    "--workspace",
                    test_workspace,
                    "--json",
                ],
            )
            assert gen_result.exit_code == 0
            plan_data = json.loads(gen_result.output)
            plan_id = plan_data["plan_id"]

            # List plans
            list_result = runner.invoke(
                app,
                ["plan", "list", "--workspace", test_workspace],
            )

            assert list_result.exit_code == 0
            assert plan_id in list_result.output
            assert "pending" in list_result.output.lower()


# ---------------------------------------------------------------------------
# Plan Execution Tests (AF-0099)
# ---------------------------------------------------------------------------


class TestPlanExecution:
    """Tests for ag run --plan execution (AF-0099)."""

    @pytest.fixture
    def temp_workspaces(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
        """Create temp workspaces directory and patch config."""
        ws_root = tmp_path / "workspaces"
        ws_root.mkdir()
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(ws_root))
        return ws_root

    @pytest.fixture
    def test_workspace(self, temp_workspaces: Path) -> str:
        """Create a test workspace."""
        ws = Workspace("test-ws", temp_workspaces)
        ws.ensure_exists()
        return "test-ws"

    def test_run_plan_not_found(self, temp_workspaces: Path, test_workspace: str) -> None:
        """ag run --plan with invalid plan ID fails."""
        result = runner.invoke(
            app,
            ["run", "--plan", "nonexistent_plan", "--workspace", test_workspace],
        )
        assert result.exit_code == 1
        assert "not found" in result.output.lower()

    def test_run_plan_mutually_exclusive_with_prompt(
        self, temp_workspaces: Path, test_workspace: str
    ) -> None:
        """ag run --plan cannot be combined with a prompt."""
        result = runner.invoke(
            app,
            ["run", "--plan", "plan_123", "--workspace", test_workspace, "Some prompt"],
        )
        assert result.exit_code == 1
        assert "cannot be combined" in result.output.lower()

    def test_run_plan_mutually_exclusive_with_playbook(
        self, temp_workspaces: Path, test_workspace: str
    ) -> None:
        """ag run --plan cannot be combined with --playbook."""
        result = runner.invoke(
            app,
            [
                "run",
                "--plan",
                "plan_123",
                "--playbook",
                "research",
                "--workspace",
                test_workspace,
            ],
        )
        assert result.exit_code == 1
        assert "cannot be combined" in result.output.lower()

    def test_run_plan_mutually_exclusive_with_skill(
        self, temp_workspaces: Path, test_workspace: str
    ) -> None:
        """ag run --plan cannot be combined with --skill."""
        result = runner.invoke(
            app,
            [
                "run",
                "--plan",
                "plan_123",
                "--skill",
                "emit_result",
                "--workspace",
                test_workspace,
            ],
        )
        assert result.exit_code == 1
        assert "cannot be combined" in result.output.lower()

    def test_run_requires_prompt_or_plan(self, temp_workspaces: Path, test_workspace: str) -> None:
        """ag run requires either a prompt or --plan."""
        result = runner.invoke(
            app,
            ["run", "--workspace", test_workspace],
        )
        assert result.exit_code == 1
        assert "required" in result.output.lower()

    def test_run_plan_expired(self, temp_workspaces: Path, test_workspace: str) -> None:
        """ag run --plan with expired plan fails."""
        # Create an expired plan directly
        plan_store = FilePlanStore(temp_workspaces)

        expired_plan = ExecutionPlan(
            plan_id="expired_plan",
            workspace_id=test_workspace,
            task_prompt="Test task",
            expires_at=datetime.now(timezone.utc) - timedelta(hours=1),  # Already expired
            playbook=Playbook(name="test", version="1.0"),
        )
        plan_store.save(expired_plan)

        result = runner.invoke(
            app,
            ["run", "--plan", "expired_plan", "--workspace", test_workspace],
        )
        assert result.exit_code == 1
        assert "expired" in result.output.lower()

    def test_run_plan_workspace_mismatch(self, temp_workspaces: Path, test_workspace: str) -> None:
        """ag run --plan with workspace mismatch fails."""
        plan_store = FilePlanStore(temp_workspaces)

        # Create plan for different workspace
        plan = ExecutionPlan(
            plan_id="mismatch_plan",
            workspace_id="different_workspace",  # Different workspace
            task_prompt="Test task",
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
            playbook=Playbook(name="test", version="1.0"),
        )
        plan_store.save(plan)

        result = runner.invoke(
            app,
            ["run", "--plan", "mismatch_plan", "--workspace", test_workspace],
        )
        assert result.exit_code == 1
        assert "mismatch" in result.output.lower()


class TestPlanExecutionWithMockedRuntime:
    """Tests for plan execution with mocked runtime."""

    @pytest.fixture
    def temp_workspaces(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
        """Create temp workspaces directory and patch config."""
        ws_root = tmp_path / "workspaces"
        ws_root.mkdir()
        monkeypatch.setenv("AG_WORKSPACE_DIR", str(ws_root))
        return ws_root

    @pytest.fixture
    def test_workspace(self, temp_workspaces: Path) -> str:
        """Create a test workspace."""
        ws = Workspace("test-ws", temp_workspaces)
        ws.ensure_exists()
        return "test-ws"

    def test_run_plan_executes_successfully(
        self, temp_workspaces: Path, test_workspace: str
    ) -> None:
        """ag run --plan executes plan and updates status."""
        from ag.core.run_trace import (
            ExecutionMode,
            FinalStatus,
            PlaybookMetadata,
            RunTrace,
            Verifier,
            VerifierStatus,
        )

        # Create a valid plan
        plan_store = FilePlanStore(temp_workspaces)

        playbook = Playbook(
            name="test_playbook",
            version="1.0",
            steps=[
                PlaybookStep(
                    step_id="s1",
                    name="Test",
                    skill_name="emit_result",
                ),
            ],
        )
        plan = ExecutionPlan(
            plan_id="exec_plan",
            workspace_id=test_workspace,
            task_prompt="Execute this test task",
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
            playbook=playbook,
            planned_steps=[
                PlannedStep(step_number=1, skill_name="emit_result", description="Test"),
            ],
        )
        plan_store.save(plan)

        # Mock the runtime execution
        mock_trace = RunTrace(
            run_id="mock_run_123",
            workspace_id=test_workspace,
            mode=ExecutionMode.SUPERVISED,
            playbook=PlaybookMetadata(name="test_playbook", version="1.0"),
            started_at=datetime.now(timezone.utc),
            ended_at=datetime.now(timezone.utc),
            duration_ms=100,
            verifier=Verifier(
                status=VerifierStatus.PASSED,
                checked_at=datetime.now(timezone.utc),
            ),
            final=FinalStatus.SUCCESS,
        )

        with (
            patch("ag.cli.main.create_runtime") as mock_create_runtime,
            patch("ag.cli.main._get_run_store") as mock_run_store,
            patch("ag.cli.main._get_artifact_store") as mock_artifact_store,
        ):
            mock_runtime = MagicMock()
            mock_runtime.execute.return_value = mock_trace
            mock_create_runtime.return_value = mock_runtime

            mock_store = MagicMock()
            mock_run_store.return_value = mock_store
            mock_artifact_store.return_value = MagicMock()

            result = runner.invoke(
                app,
                ["run", "--plan", "exec_plan", "--workspace", test_workspace],
            )

            assert result.exit_code == 0
            assert "Plan executed" in result.output
            assert "exec_plan" in result.output

            # Verify runtime was called with plan's task prompt and playbook
            mock_runtime.execute.assert_called_once()
            call_kwargs = mock_runtime.execute.call_args.kwargs
            assert call_kwargs["prompt"] == "Execute this test task"
            # BUG-0016 FIX: Verify playbook_object is passed (not just name)
            assert "playbook_object" in call_kwargs
            assert call_kwargs["playbook_object"].name == "test_playbook"
            assert len(call_kwargs["playbook_object"].steps) == 1
            assert call_kwargs["playbook_object"].steps[0].skill_name == "emit_result"

        # Verify plan status was updated
        updated_plan = plan_store.get(test_workspace, "exec_plan")
        assert updated_plan is not None
        assert updated_plan.status == PlanStatus.EXECUTED
        assert updated_plan.run_id == "mock_run_123"
        assert updated_plan.executed_at is not None

    def test_run_plan_json_output(self, temp_workspaces: Path, test_workspace: str) -> None:
        """ag run --plan --json returns proper JSON output."""
        from ag.core.run_trace import (
            ExecutionMode,
            FinalStatus,
            PlaybookMetadata,
            RunTrace,
            Verifier,
            VerifierStatus,
        )

        plan_store = FilePlanStore(temp_workspaces)

        plan = ExecutionPlan(
            plan_id="json_plan",
            workspace_id=test_workspace,
            task_prompt="JSON test",
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
            playbook=Playbook(name="test", version="1.0"),
        )
        plan_store.save(plan)

        mock_trace = RunTrace(
            run_id="json_run_123",
            workspace_id=test_workspace,
            mode=ExecutionMode.SUPERVISED,
            playbook=PlaybookMetadata(name="test", version="1.0"),
            started_at=datetime.now(timezone.utc),
            ended_at=datetime.now(timezone.utc),
            duration_ms=50,
            verifier=Verifier(
                status=VerifierStatus.PASSED,
                checked_at=datetime.now(timezone.utc),
            ),
            final=FinalStatus.SUCCESS,
        )

        with (
            patch("ag.cli.main.create_runtime") as mock_create_runtime,
            patch("ag.cli.main._get_run_store"),
            patch("ag.cli.main._get_artifact_store"),
        ):
            mock_runtime = MagicMock()
            mock_runtime.execute.return_value = mock_trace
            mock_create_runtime.return_value = mock_runtime

            result = runner.invoke(
                app,
                ["run", "--plan", "json_plan", "--workspace", test_workspace, "--json"],
            )

            assert result.exit_code == 0
            output = json.loads(result.output)
            assert output["plan_id"] == "json_plan"
            assert output["plan_executed"] is True
            assert output["run_id"] == "json_run_123"
