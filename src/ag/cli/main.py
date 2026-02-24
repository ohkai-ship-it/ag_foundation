"""
ag CLI — Main entrypoint for ag_foundation.

CLI v0 implementation for AF-0008.
All labels are derived from persisted RunTrace (truthful UX).
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from ag import __version__
from ag.core import ExecutionMode, FinalStatus, RunTrace, VerifierStatus, create_runtime
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

# Default workspace root
DEFAULT_WORKSPACES_ROOT = Path.home() / ".ag" / "workspaces"


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
    return SQLiteRunStore(workspaces_root or DEFAULT_WORKSPACES_ROOT)


def _get_artifact_store(workspaces_root: Path | None = None) -> SQLiteArtifactStore:
    """Get an artifact store instance."""
    return SQLiteArtifactStore(workspaces_root or DEFAULT_WORKSPACES_ROOT)


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


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        console.print(f"ag version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-V",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
) -> None:
    """ag_foundation CLI."""
    pass


# ─────────────────────────────────────────────────────────────────────────────
# ag run
# ─────────────────────────────────────────────────────────────────────────────


@app.command()
def run(
    prompt: str = typer.Argument(..., help="The prompt or task to execute."),
    workspace: Optional[str] = typer.Option(
        None, "--workspace", "-w", help="Workspace ID (default: auto-generated)."
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
    json_output: bool = typer.Option(
        False, "--json", help="Output machine-readable JSON."
    ),
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
    # Manual mode gate check
    if mode == "manual":
        if not _check_manual_mode_gate():
            err_console.print(
                f"[bold red]Error:[/bold red] --mode manual requires {DEV_ENV_VAR}=1 environment variable."
            )
            err_console.print(
                f"Set the environment variable and try again: {DEV_ENV_VAR}=1 ag run --mode manual ..."
            )
            raise typer.Exit(code=1)
        if not quiet and not json_output:
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
            workspace=workspace,
            mode=mode,
            playbook=playbook,
        )

        # Output results
        if json_output:
            console.print(trace.to_json())
        else:
            labels = extract_labels(trace)

            if not quiet:
                console.print()
                console.print(f"[bold]Run completed[/bold]")
                console.print(f"  Run ID: {labels['run_id']}")
                console.print(f"  Workspace: {labels['workspace_id']}")
                console.print(f"  Mode: {labels['mode']}")
                console.print(f"  Status: {format_status(trace.final)}")
                console.print(f"  Verifier: {format_verifier(trace.verifier.status)}")
                console.print(f"  Duration: {labels['duration']}")
                console.print(f"  Playbook: {labels['playbook']}")

                if verbose:
                    console.print()
                    console.print(f"  Steps: {len(trace.steps)}")
                    for step in trace.steps:
                        step_status = "[green]✓[/green]" if not step.error else "[red]✗[/red]"
                        console.print(
                            f"    {step_status} {step.step_number}: {step.skill_name or 'reasoning'}"
                        )

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
    limit: int = typer.Option(10, "--limit", "-n", help="Max runs to show."),
    status: Optional[str] = typer.Option(
        None, "--status", "-s", help="Filter by status (success/failure)."
    ),
    workspace: Optional[str] = typer.Option(
        None, "--workspace", "-w", help="Filter by workspace."
    ),
    json_output: bool = typer.Option(False, "--json", help="Output JSON."),
) -> None:
    """List recent runs."""
    if not workspace:
        err_console.print("[bold red]Error:[/bold red] --workspace is required for runs list")
        raise typer.Exit(code=1)

    run_store = _get_run_store()

    try:
        runs = run_store.list(workspace, limit=limit)

        # Filter by status if provided
        if status:
            status_filter = status.lower()
            runs = [r for r in runs if r.final.value == status_filter]

        if json_output:
            output = [json.loads(r.to_json()) for r in runs]
            console.print(json.dumps(output, indent=2))
        else:
            if not runs:
                console.print(f"No runs found in workspace '{workspace}'")
                return

            table = Table(title=f"Runs in workspace '{workspace}'")
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
    run_id: str = typer.Argument(..., help="The run ID to show."),
    workspace: Optional[str] = typer.Option(
        None, "--workspace", "-w", help="Workspace containing the run."
    ),
    json_output: bool = typer.Option(False, "--json", help="Output JSON."),
) -> None:
    """Show details of a specific run."""
    if not workspace:
        err_console.print("[bold red]Error:[/bold red] --workspace is required for runs show")
        raise typer.Exit(code=1)

    run_store = _get_run_store()

    try:
        trace = run_store.get(workspace, run_id)

        if not trace:
            err_console.print(f"[bold red]Error:[/bold red] Run '{run_id}' not found in workspace '{workspace}'")
            raise typer.Exit(code=1)

        if json_output:
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
    run_id: str = typer.Argument(..., help="The run ID to show trace for."),
    workspace: Optional[str] = typer.Option(
        None, "--workspace", "-w", help="Workspace containing the run."
    ),
    json_output: bool = typer.Option(False, "--json", help="Output JSON."),
) -> None:
    """Show the full trace of a run (alias for show --json)."""
    # Delegate to show with json_output=True
    runs_show(run_id=run_id, workspace=workspace, json_output=True)



# ─────────────────────────────────────────────────────────────────────────────
# ag ws (workspace)
# ─────────────────────────────────────────────────────────────────────────────


@ws_app.command("list")
def ws_list() -> None:
    """List all workspaces."""
    console.print("[yellow]⚠ Stub — not implemented yet (see AF-0006)[/yellow]")


@ws_app.command("create")
def ws_create(name: str = typer.Argument(..., help="Workspace name.")) -> None:
    """Create a new workspace."""
    console.print(f"[dim]Creating workspace:[/dim] {name}")
    console.print("[yellow]⚠ Stub — not implemented yet (see AF-0006)[/yellow]")


@ws_app.command("use")
def ws_use(workspace_id: str = typer.Argument(..., help="Workspace ID to switch to.")) -> None:
    """Switch to a workspace."""
    console.print(f"[dim]Switching to:[/dim] {workspace_id}")
    console.print("[yellow]⚠ Stub — not implemented yet (see AF-0006)[/yellow]")


@ws_app.command("show")
def ws_show(
    workspace_id: Optional[str] = typer.Argument(None, help="Workspace ID (default: current).")
) -> None:
    """Show workspace details."""
    console.print(f"[dim]Workspace:[/dim] {workspace_id or 'current'}")
    console.print("[yellow]⚠ Stub — not implemented yet (see AF-0006)[/yellow]")


# ─────────────────────────────────────────────────────────────────────────────
# ag artifacts
# ─────────────────────────────────────────────────────────────────────────────


@artifacts_app.command("list")
def artifacts_list(
    run_id: Optional[str] = typer.Option(None, "--run", "-r", help="Filter by run ID."),
    json_output: bool = typer.Option(False, "--json", help="Output JSON."),
) -> None:
    """List artifacts."""
    if run_id:
        console.print(f"[dim]Filtering by run:[/dim] {run_id}")
    console.print("[yellow]⚠ Stub — not implemented yet (see AF-0009)[/yellow]")


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
    console.print("[bold]ag doctor[/bold]")
    console.print()
    console.print(f"  Version: {__version__}")
    console.print(f"  Python: {sys.version}")
    console.print(f"  {DEV_ENV_VAR}: {os.environ.get(DEV_ENV_VAR, '(not set)')}")
    console.print()
    console.print("[yellow]⚠ Full diagnostics not implemented yet[/yellow]")


if __name__ == "__main__":
    app()
