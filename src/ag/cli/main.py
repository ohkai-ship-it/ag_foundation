"""
ag CLI — Main entrypoint for ag_foundation.

CLI v0 implementation for AF-0008.
All labels are derived from persisted RunTrace (truthful UX).
"""

import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from ag import __version__
from ag.config import get_workspace_dir
from ag.core import FinalStatus, RunTrace, VerifierStatus, create_runtime
from ag.storage import SQLiteArtifactStore, SQLiteRunStore

# Console for rich output
console = Console()
err_console = Console(stderr=True)

# Main app
app = typer.Typer(
    name="ag",
    help="ag_foundation — Modular agent network core runtime.",
    no_args_is_help=True,
)

# Sub-apps for command groups
runs_app = typer.Typer(help="Inspect and manage runs.")
ws_app = typer.Typer(help="Workspace operations.")
artifacts_app = typer.Typer(help="Artifact registry operations.")
skills_app = typer.Typer(help="Skills and plugins.")
playbooks_app = typer.Typer(help="Orchestration playbooks.")
config_app = typer.Typer(help="Global configuration.")

app.add_typer(runs_app, name="runs")
app.add_typer(ws_app, name="ws")
app.add_typer(artifacts_app, name="artifacts")
app.add_typer(skills_app, name="skills")
app.add_typer(playbooks_app, name="playbooks")
app.add_typer(config_app, name="config")


# ─────────────────────────────────────────────────────────────────────────────
# Constants and helpers
# ─────────────────────────────────────────────────────────────────────────────

DEV_ENV_VAR = "AG_DEV"
MANUAL_MODE_BANNER = "DEV MODE: manual (LLMs disabled)"


def _check_manual_mode_gate() -> bool:
    """
    Check if manual mode is allowed via AG_DEV=1.
    Returns True if gate passes, False otherwise.
    """
    return os.environ.get(DEV_ENV_VAR, "").lower() in ("1", "true", "yes")


def _print_manual_mode_banner() -> None:
    """Print the manual mode warning banner."""
    console.print(f"[bold yellow]{MANUAL_MODE_BANNER}[/bold yellow]")


def _get_run_store(workspaces_root: Path | None = None) -> SQLiteRunStore:
    """Get a run store instance."""
    return SQLiteRunStore(workspaces_root or get_workspace_dir())


def _get_artifact_store(workspaces_root: Path | None = None) -> SQLiteArtifactStore:
    """Get an artifact store instance."""
    return SQLiteArtifactStore(workspaces_root or get_workspace_dir())


# ─────────────────────────────────────────────────────────────────────────────
# Label extraction helpers (truthful UX)
# ─────────────────────────────────────────────────────────────────────────────


def extract_labels(trace: RunTrace) -> dict[str, str]:
    """Extract display labels from a RunTrace.

    All labels are derived from the actual trace data (truthful UX).

    Returns:
        Dict with keys: mode, status, verifier_status, duration, playbook
    """
    return {
        "mode": trace.mode.value,
        "status": trace.final.value,
        "verifier_status": trace.verifier.status.value,
        "duration": f"{trace.duration_ms}ms" if trace.duration_ms else "unknown",
        "playbook": f"{trace.playbook.name}@{trace.playbook.version}",
        "run_id": trace.run_id,
        "workspace_id": trace.workspace_id,
    }


def format_status(status: FinalStatus) -> str:
    """Format status with color."""
    colors = {
        FinalStatus.SUCCESS: "green",
        FinalStatus.FAILURE: "red",
        FinalStatus.ABORTED: "yellow",
        FinalStatus.TIMEOUT: "yellow",
    }
    return f"[{colors.get(status, 'white')}]{status.value}[/{colors.get(status, 'white')}]"


def format_verifier(status: VerifierStatus) -> str:
    """Format verifier status with color."""
    colors = {
        VerifierStatus.PASSED: "green",
        VerifierStatus.FAILED: "red",
        VerifierStatus.PENDING: "yellow",
        VerifierStatus.SKIPPED: "dim",
    }
    return f"[{colors.get(status, 'white')}]{status.value}[/{colors.get(status, 'white')}]"


# ─────────────────────────────────────────────────────────────────────────────
# Global options
# ─────────────────────────────────────────────────────────────────────────────


@dataclass
class CLIContext:
    """Global CLI context for propagating options to subcommands."""

    workspace: Optional[str] = None
    json_output: bool = False
    quiet: bool = False
    verbose: bool = False


def get_cli_ctx(ctx: typer.Context) -> CLIContext:
    """Get CLI context from Typer context, or create empty one."""
    if ctx.obj is None:
        return CLIContext()
    return ctx.obj


def resolve_option(
    local: Optional[bool] | Optional[str],
    ctx: typer.Context,
    key: str,
) -> Optional[bool] | Optional[str]:
    """Resolve an option with precedence: local flag > global flag > default.

    Args:
        local: Value from subcommand option
        ctx: Typer context
        key: Attribute name in CLIContext

    Returns:
        Resolved value with proper precedence
    """
    cli_ctx = get_cli_ctx(ctx)
    global_value = getattr(cli_ctx, key, None)

    # Local always wins if explicitly set (not None for optionals, not False for bools)
    if isinstance(local, bool):
        # For bools: local True wins, else use global
        return local if local else global_value
    else:
        # For strings: local if set, else global
        return local if local is not None else global_value


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        console.print(f"ag version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-V",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
    workspace: Optional[str] = typer.Option(
        None,
        "--workspace",
        "-w",
        help="Default workspace ID for all commands.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output machine-readable JSON (where supported).",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Reduce non-essential output.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Include extra debug details.",
    ),
) -> None:
    """ag_foundation CLI.

    Global options like --workspace, --json, --quiet, --verbose can be set
    here and will be inherited by all subcommands. Subcommand-level options
    take precedence over global options.

    Examples:
        ag --workspace my_ws runs list
        ag --json runs show <run_id> --workspace my_ws
        ag --quiet run "Task"
    """
    # Store global options in context for subcommands
    ctx.obj = CLIContext(
        workspace=workspace,
        json_output=json_output,
        quiet=quiet,
        verbose=verbose,
    )


# ─────────────────────────────────────────────────────────────────────────────
# ag run
# ─────────────────────────────────────────────────────────────────────────────


@app.command()
def run(
    ctx: typer.Context,
    prompt: str = typer.Argument(..., help="The prompt or task to execute."),
    workspace: Optional[str] = typer.Option(
        None, "--workspace", "-w", help="Workspace ID (uses AG_WORKSPACE env if not specified)."
    ),
    mode: str = typer.Option(
        "llm", "--mode", "-m", help="Runtime mode: llm (default) or manual (dev-only)."
    ),
    playbook: Optional[str] = typer.Option(
        None, "--playbook", "-p", help="Override playbook selection."
    ),
    reasoning: Optional[str] = typer.Option(
        None, "--reasoning", "-r", help="Override reasoning mode."
    ),
    json_output: bool = typer.Option(False, "--json", help="Output machine-readable JSON."),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Reduce output."),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Include trace pointers and debug details."
    ),
) -> None:
    """
    Execute a task.

    Example:
        ag run "Draft a project plan"
        ag run --mode manual "Test the pipeline"
    """
    # Resolve global options with precedence: local > global > default
    cli_ctx = get_cli_ctx(ctx)
    resolved_json = json_output or cli_ctx.json_output
    resolved_quiet = quiet or cli_ctx.quiet
    resolved_verbose = verbose or cli_ctx.verbose

    # AF-0026: Workspace selection policy enforcement
    # Precedence: --workspace flag > AG_WORKSPACE env > error
    from ag.config import get_default_workspace
    from ag.storage import Workspace

    resolved_workspace = workspace if workspace is not None else cli_ctx.workspace
    if resolved_workspace is None:
        # Try AG_WORKSPACE env var via get_default_workspace()
        env_workspace = os.environ.get("AG_WORKSPACE")
        if env_workspace:
            resolved_workspace = env_workspace

    # Fail if no workspace selected
    if resolved_workspace is None:
        err_console.print(
            "[bold red]Error:[/bold red] No workspace specified."
        )
        err_console.print()
        err_console.print("Specify a workspace using one of:")
        err_console.print("  1. [cyan]--workspace <name>[/cyan] flag")
        err_console.print("  2. [cyan]AG_WORKSPACE[/cyan] environment variable")
        err_console.print()
        err_console.print("To create a workspace: [cyan]ag ws create <name>[/cyan]")
        err_console.print("To list workspaces:    [cyan]ag ws list[/cyan]")
        raise typer.Exit(code=1)

    # Validate workspace exists
    ws = Workspace(resolved_workspace, get_workspace_dir())
    if not ws.exists():
        err_console.print(
            f"[bold red]Error:[/bold red] Workspace '{resolved_workspace}' does not exist."
        )
        err_console.print(f"Create it first: [cyan]ag ws create {resolved_workspace}[/cyan]")
        raise typer.Exit(code=1)

    # Manual mode gate check
    if mode == "manual":
        if not _check_manual_mode_gate():
            err_console.print(
                f"[bold red]Error:[/bold red] --mode manual requires "
                f"{DEV_ENV_VAR}=1 environment variable."
            )
            err_console.print(
                f"Set the environment variable and try again: "
                f"{DEV_ENV_VAR}=1 ag run --mode manual ..."
            )
            raise typer.Exit(code=1)
        if not resolved_quiet and not resolved_json:
            _print_manual_mode_banner()

    # Create and execute runtime
    run_store = _get_run_store()
    artifact_store = _get_artifact_store()

    try:
        runtime = create_runtime(
            run_store=run_store,
            artifact_store=artifact_store,
        )

        trace = runtime.execute(
            prompt=prompt,
            workspace=resolved_workspace,
            mode=mode,
            playbook=playbook,
        )

        # Output results
        if resolved_json:
            console.print(trace.to_json())
        else:
            labels = extract_labels(trace)

            if not resolved_quiet:
                console.print()
                console.print("[bold]Run completed[/bold]")
                console.print(f"  Run ID: {labels['run_id']}")
                console.print(f"  Workspace: {labels['workspace_id']}")
                console.print(f"  Mode: {labels['mode']}")
                console.print(f"  Status: {format_status(trace.final)}")
                console.print(f"  Verifier: {format_verifier(trace.verifier.status)}")
                console.print(f"  Duration: {labels['duration']}")
                console.print(f"  Playbook: {labels['playbook']}")

                if resolved_verbose:
                    console.print()
                    console.print(f"  Steps: {len(trace.steps)}")
                    for step in trace.steps:
                        status_mark = "[green]✓[/green]" if not step.error else "[red]✗[/red]"
                        skill = step.skill_name or "reasoning"
                        console.print(f"    {status_mark} {step.step_number}: {skill}")

                if trace.error:
                    console.print()
                    console.print(f"[red]Error: {trace.error}[/red]")

        # Exit with error code if run failed
        if trace.final != FinalStatus.SUCCESS:
            raise typer.Exit(code=1)

    finally:
        run_store.close()
        artifact_store.close()


# ─────────────────────────────────────────────────────────────────────────────
# ag runs
# ─────────────────────────────────────────────────────────────────────────────


@runs_app.command("list")
def runs_list(
    ctx: typer.Context,
    limit: int = typer.Option(10, "--limit", "-n", help="Max runs to show."),
    status: Optional[str] = typer.Option(
        None, "--status", "-s", help="Filter by status (success/failure)."
    ),
    workspace: Optional[str] = typer.Option(None, "--workspace", "-w", help="Filter by workspace."),
    json_output: bool = typer.Option(False, "--json", help="Output JSON."),
) -> None:
    """List recent runs."""
    # Resolve global options
    cli_ctx = get_cli_ctx(ctx)
    resolved_workspace = workspace if workspace is not None else cli_ctx.workspace
    resolved_json = json_output or cli_ctx.json_output

    if not resolved_workspace:
        err_console.print("[bold red]Error:[/bold red] --workspace is required for runs list")
        raise typer.Exit(code=1)

    run_store = _get_run_store()

    try:
        runs = run_store.list(resolved_workspace, limit=limit)

        # Filter by status if provided
        if status:
            status_filter = status.lower()
            runs = [r for r in runs if r.final.value == status_filter]

        if resolved_json:
            output = [json.loads(r.to_json()) for r in runs]
            console.print(json.dumps(output, indent=2))
        else:
            if not runs:
                console.print(f"No runs found in workspace '{resolved_workspace}'")
                return

            table = Table(title=f"Runs in workspace '{resolved_workspace}'")
            table.add_column("Run ID", style="cyan")
            table.add_column("Status")
            table.add_column("Verifier")
            table.add_column("Mode")
            table.add_column("Duration")
            table.add_column("Started")

            for run in runs:
                labels = extract_labels(run)
                table.add_row(
                    run.run_id[:12] + "...",
                    format_status(run.final),
                    format_verifier(run.verifier.status),
                    labels["mode"],
                    labels["duration"],
                    run.started_at.strftime("%Y-%m-%d %H:%M"),
                )

            console.print(table)

    finally:
        run_store.close()


@runs_app.command("show")
def runs_show(
    ctx: typer.Context,
    run_id: str = typer.Argument(..., help="The run ID to show."),
    workspace: Optional[str] = typer.Option(
        None, "--workspace", "-w", help="Workspace containing the run."
    ),
    json_output: bool = typer.Option(False, "--json", help="Output JSON."),
) -> None:
    """Show details of a specific run."""
    # Resolve global options
    cli_ctx = get_cli_ctx(ctx)
    resolved_workspace = workspace if workspace is not None else cli_ctx.workspace
    resolved_json = json_output or cli_ctx.json_output

    if not resolved_workspace:
        err_console.print("[bold red]Error:[/bold red] --workspace is required for runs show")
        raise typer.Exit(code=1)

    run_store = _get_run_store()

    try:
        trace = run_store.get(resolved_workspace, run_id)

        if not trace:
            err_console.print(
                f"[bold red]Error:[/bold red] Run '{run_id}' not found "
                f"in workspace '{resolved_workspace}'"
            )
            raise typer.Exit(code=1)

        if resolved_json:
            # Output conforms to RunTrace schema
            console.print(trace.to_json())
        else:
            labels = extract_labels(trace)

            console.print(f"[bold]Run {trace.run_id}[/bold]")
            console.print()
            console.print(f"  Workspace: {labels['workspace_id']}")
            console.print(f"  Mode: {labels['mode']}")
            console.print(f"  Status: {format_status(trace.final)}")
            console.print(f"  Verifier: {format_verifier(trace.verifier.status)}")
            if trace.verifier.message:
                console.print(f"    Message: {trace.verifier.message}")
            console.print(f"  Duration: {labels['duration']}")
            console.print(f"  Playbook: {labels['playbook']}")
            console.print(f"  Started: {trace.started_at.isoformat()}")
            console.print(f"  Ended: {trace.ended_at.isoformat() if trace.ended_at else 'N/A'}")
            console.print()

            # Steps
            console.print(f"[bold]Steps ({len(trace.steps)}):[/bold]")
            for step in trace.steps:
                step_status = "[green]✓[/green]" if not step.error else "[red]✗[/red]"
                console.print(
                    f"  {step_status} Step {step.step_number}: {step.skill_name or 'reasoning'}"
                )
                console.print(f"      Output: {step.output_summary[:60]}...")
                if step.error:
                    console.print(f"      [red]Error: {step.error}[/red]")

            # Artifacts
            if trace.artifacts:
                console.print()
                console.print(f"[bold]Artifacts ({len(trace.artifacts)}):[/bold]")
                for artifact in trace.artifacts:
                    console.print(f"  - {artifact.artifact_id}: {artifact.path}")

            # Error
            if trace.error:
                console.print()
                console.print(f"[bold red]Error:[/bold red] {trace.error}")

    finally:
        run_store.close()


@runs_app.command("trace")
def runs_trace(
    ctx: typer.Context,
    run_id: str = typer.Argument(..., help="The run ID to show trace for."),
    workspace: Optional[str] = typer.Option(
        None, "--workspace", "-w", help="Workspace containing the run."
    ),
    json_output: bool = typer.Option(False, "--json", help="Output JSON."),
) -> None:
    """Show the full trace of a run (alias for show --json)."""
    # Delegate to show with json_output=True, passing ctx
    runs_show(ctx=ctx, run_id=run_id, workspace=workspace, json_output=True)


# ─────────────────────────────────────────────────────────────────────────────
# ag ws (workspace)
# ─────────────────────────────────────────────────────────────────────────────


@ws_app.command("list")
def ws_list() -> None:
    """List all workspaces."""
    workspaces_root = get_workspace_dir()
    if not workspaces_root.exists():
        console.print("[dim]No workspaces found.[/dim]")
        return

    workspace_dirs = [d for d in workspaces_root.iterdir() if d.is_dir()]
    if not workspace_dirs:
        console.print("[dim]No workspaces found.[/dim]")
        return

    table = Table(title="Workspaces")
    table.add_column("Workspace ID", style="cyan")
    table.add_column("Path")

    for ws_dir in sorted(workspace_dirs):
        table.add_row(ws_dir.name, str(ws_dir))

    console.print(table)


@ws_app.command("create")
def ws_create(name: str = typer.Argument(..., help="Workspace name.")) -> None:
    """Create a new workspace."""
    from ag.storage import Workspace

    ws = Workspace(name, get_workspace_dir())
    if ws.exists():
        err_console.print(f"[bold red]Error:[/bold red] Workspace '{name}' already exists.")
        raise typer.Exit(code=1)

    ws.ensure_exists()
    console.print(f"[green]Created workspace:[/green] {name}")
    console.print(f"  Path: {ws.path}")


@ws_app.command("use")
def ws_use(workspace_id: str = typer.Argument(..., help="Workspace ID to switch to.")) -> None:
    """Switch to a workspace."""
    console.print(f"[dim]Switching to:[/dim] {workspace_id}")
    console.print("[yellow]⚠ Stub — not implemented yet (see AF-0006)[/yellow]")


@ws_app.command("show")
def ws_show(
    workspace_id: Optional[str] = typer.Argument(None, help="Workspace ID (default: current)."),
) -> None:
    """Show workspace details."""
    console.print(f"[dim]Workspace:[/dim] {workspace_id or 'current'}")
    console.print("[yellow]⚠ Stub — not implemented yet (see AF-0006)[/yellow]")


# ─────────────────────────────────────────────────────────────────────────────
# ag artifacts
# ─────────────────────────────────────────────────────────────────────────────


@artifacts_app.command("list")
def artifacts_list(
    ctx: typer.Context,
    run_id: str = typer.Option(..., "--run", "-r", help="Run ID to list artifacts for."),
    workspace: Optional[str] = typer.Option(
        None, "--workspace", "-w", help="Workspace ID (derived from run if not provided)."
    ),
    json_output: bool = typer.Option(False, "--json", help="Output JSON."),
) -> None:
    """List artifacts for a run.

    Returns artifacts registered during the run, including result.md
    which contains step summaries.
    """
    # Resolve global options
    cli_ctx = get_cli_ctx(ctx)
    resolved_workspace = workspace if workspace is not None else cli_ctx.workspace
    resolved_json = json_output or cli_ctx.json_output

    # Get run to find workspace_id if not provided
    run_store = _get_run_store()
    artifact_store = _get_artifact_store()

    # If no workspace provided, we need to find the run
    if not resolved_workspace:
        # Try to find the run in all workspaces - for now just use a simple approach
        # In a real implementation, we'd have a global index
        err_console.print(
            "[bold red]Error:[/bold red] --workspace is required for artifact listing."
        )
        err_console.print("Example: ag artifacts list --run <run_id> --workspace <workspace_id>")
        raise typer.Exit(code=1)

    artifacts = artifact_store.list(resolved_workspace, run_id)

    if resolved_json:
        # Output as JSON array
        json_data = [
            {
                "artifact_id": a.artifact_id,
                "path": a.path,
                "artifact_type": a.artifact_type,
                "size_bytes": a.size_bytes,
                "checksum": a.checksum,
            }
            for a in artifacts
        ]
        print(json.dumps(json_data, indent=2))
    else:
        if not artifacts:
            console.print(f"[dim]No artifacts found for run {run_id}[/dim]")
        else:
            table = Table(title=f"Artifacts for run {run_id}")
            table.add_column("ID", style="cyan")
            table.add_column("Type", style="green")
            table.add_column("Size", justify="right")
            table.add_column("Path")

            for a in artifacts:
                size_str = f"{a.size_bytes} B" if a.size_bytes is not None else "-"
                # Extract just the filename from path for display
                path_display = Path(a.path).name if a.path else "-"
                table.add_row(a.artifact_id, a.artifact_type, size_str, path_display)

            console.print(table)

    run_store.close()
    artifact_store.close()


@artifacts_app.command("show")
def artifacts_show(artifact_id: str = typer.Argument(..., help="Artifact ID.")) -> None:
    """Show artifact details."""
    console.print(f"[dim]Artifact:[/dim] {artifact_id}")
    console.print("[yellow]⚠ Stub — not implemented yet (see AF-0009)[/yellow]")


# ─────────────────────────────────────────────────────────────────────────────
# ag skills
# ─────────────────────────────────────────────────────────────────────────────


@skills_app.command("list")
def skills_list() -> None:
    """List available skills."""
    console.print("[yellow]⚠ Stub — not implemented yet[/yellow]")


@skills_app.command("info")
def skills_info(skill_name: str = typer.Argument(..., help="Skill name.")) -> None:
    """Show skill details."""
    console.print(f"[dim]Skill:[/dim] {skill_name}")
    console.print("[yellow]⚠ Stub — not implemented yet[/yellow]")


# ─────────────────────────────────────────────────────────────────────────────
# ag playbooks
# ─────────────────────────────────────────────────────────────────────────────


@playbooks_app.command("list")
def playbooks_list() -> None:
    """List available playbooks."""
    console.print("[yellow]⚠ Stub — not implemented yet[/yellow]")


@playbooks_app.command("show")
def playbooks_show(name: str = typer.Argument(..., help="Playbook name.")) -> None:
    """Show playbook details."""
    console.print(f"[dim]Playbook:[/dim] {name}")
    console.print("[yellow]⚠ Stub — not implemented yet[/yellow]")


# ─────────────────────────────────────────────────────────────────────────────
# ag config
# ─────────────────────────────────────────────────────────────────────────────


@config_app.command("list")
def config_list() -> None:
    """List all configuration values."""
    console.print("[yellow]⚠ Stub — not implemented yet[/yellow]")


@config_app.command("get")
def config_get(key: str = typer.Argument(..., help="Config key.")) -> None:
    """Get a configuration value."""
    console.print(f"[dim]Key:[/dim] {key}")
    console.print("[yellow]⚠ Stub — not implemented yet[/yellow]")


@config_app.command("set")
def config_set(
    key: str = typer.Argument(..., help="Config key."),
    value: str = typer.Argument(..., help="Config value."),
) -> None:
    """Set a configuration value."""
    console.print(f"[dim]Setting:[/dim] {key} = {value}")
    console.print("[yellow]⚠ Stub — not implemented yet[/yellow]")


# ─────────────────────────────────────────────────────────────────────────────
# ag doctor
# ─────────────────────────────────────────────────────────────────────────────


@app.command()
def doctor(
    json_output: bool = typer.Option(False, "--json", help="Output JSON."),
) -> None:
    """
    Run diagnostics to validate environment setup.
    """
    from ag.config import (
        ENV_VARS,
        get_config_path,
        get_default_workspace,
        get_workspace_dir,
    )

    issues: list[str] = []
    warnings: list[str] = []

    # Check basic info
    console.print("[bold]ag doctor[/bold]")
    console.print()
    console.print("[bold cyan]System Info[/bold cyan]")
    console.print(f"  Version:     {__version__}")
    console.print(f"  Python:      {sys.version.split()[0]}")
    console.print()

    # Check environment variables
    console.print("[bold cyan]Environment Variables[/bold cyan]")
    for var, desc in ENV_VARS.items():
        value = os.environ.get(var)
        if value:
            # Mask API keys
            if "KEY" in var or "SECRET" in var:
                display_value = value[:4] + "..." + value[-4:] if len(value) > 8 else "****"
            else:
                display_value = value
            console.print(f"  {var}: [green]{display_value}[/green]")
        else:
            console.print(f"  {var}: [dim](not set)[/dim]")
    console.print()

    # Check config resolution
    console.print("[bold cyan]Configuration[/bold cyan]")
    config_path = get_config_path()
    console.print(f"  Config file:       {config_path}")
    if config_path.exists():
        console.print("                     [green]✓ exists[/green]")
    else:
        console.print("                     [dim](not created)[/dim]")
    console.print()

    # Check workspace directory
    console.print("[bold cyan]Workspace Storage[/bold cyan]")
    workspace_dir = get_workspace_dir()
    console.print(f"  Workspace root:    {workspace_dir}")

    if workspace_dir.exists():
        console.print("                     [green]✓ exists[/green]")
        # List workspaces
        workspace_dirs = [d for d in workspace_dir.iterdir() if d.is_dir()]
        console.print(f"  Workspaces found:  {len(workspace_dirs)}")
    else:
        console.print("                     [yellow]○ not created yet[/yellow]")
        warnings.append(f"Workspace directory does not exist: {workspace_dir}")

    # Check if directory is writable
    try:
        workspace_dir.mkdir(parents=True, exist_ok=True)
        test_file = workspace_dir / ".ag_doctor_test"
        test_file.touch()
        test_file.unlink()
        console.print("  Writable:          [green]✓ yes[/green]")
    except Exception as e:
        console.print(f"  Writable:          [red]✗ no ({e})[/red]")
        issues.append(f"Cannot write to workspace directory: {e}")

    console.print()
    console.print(f"  Default workspace: {get_default_workspace()}")
    console.print()

    # Check config resolution order
    console.print("[bold cyan]Config Resolution Order[/bold cyan]")
    console.print("  1. TaskSpec (runtime)")
    console.print("  2. Workspace settings")
    console.print("  3. Environment variables (.env)")
    console.print("  4. Config file (~/.ag/config.yaml)")
    console.print("  5. Defaults")
    console.print()

    # Summary
    if issues:
        console.print("[bold red]Issues Found[/bold red]")
        for issue in issues:
            console.print(f"  [red]✗[/red] {issue}")
        console.print()

    if warnings:
        console.print("[bold yellow]Warnings[/bold yellow]")
        for warning in warnings:
            console.print(f"  [yellow]○[/yellow] {warning}")
        console.print()

    if not issues and not warnings:
        console.print("[bold green]✓ All checks passed[/bold green]")
    elif not issues:
        console.print("[bold yellow]○ No critical issues[/bold yellow]")


if __name__ == "__main__":
    app()
