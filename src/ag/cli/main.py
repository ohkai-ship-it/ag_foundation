"""
ag CLI — Main entrypoint for ag_foundation.

This is a stub implementation for AF-0010.
Real commands will be implemented in AF-0008.
"""

import os
import sys
from typing import Optional

import typer
from rich.console import Console

from ag import __version__

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
        None, "--workspace", "-w", help="Workspace ID (default: current)."
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
        _print_manual_mode_banner()

    # Stub: real implementation in AF-0008
    console.print(f"[dim]Prompt:[/dim] {prompt}")
    console.print(f"[dim]Mode:[/dim] {mode}")
    console.print(f"[dim]Workspace:[/dim] {workspace or 'default'}")
    console.print()
    console.print("[yellow]⚠ CLI stub — runtime not implemented yet (see AF-0007, AF-0008)[/yellow]")


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
    console.print("[yellow]⚠ Stub — not implemented yet (see AF-0008)[/yellow]")


@runs_app.command("show")
def runs_show(
    run_id: str = typer.Argument(..., help="The run ID to show."),
    json_output: bool = typer.Option(False, "--json", help="Output JSON."),
) -> None:
    """Show details of a specific run."""
    console.print(f"[dim]Run ID:[/dim] {run_id}")
    console.print("[yellow]⚠ Stub — not implemented yet (see AF-0008)[/yellow]")


@runs_app.command("trace")
def runs_trace(
    run_id: str = typer.Argument(..., help="The run ID to show trace for."),
    json_output: bool = typer.Option(False, "--json", help="Output JSON."),
) -> None:
    """Show the full trace of a run (alias for show with trace emphasis)."""
    console.print(f"[dim]Run ID:[/dim] {run_id}")
    console.print("[yellow]⚠ Stub — not implemented yet (see AF-0008)[/yellow]")


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
