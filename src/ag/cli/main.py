"""
ag CLI — Main entrypoint for ag_foundation.

CLI v0 implementation for AF-0008.
All labels are derived from persisted RunTrace (truthful UX).
"""

# AF-0033: Load .env early, before any env var checks
# This must happen before other imports that might check env vars
from dotenv import load_dotenv

load_dotenv()  # Load .env from current directory or parents

import json  # noqa: E402
import os  # noqa: E402
import sys  # noqa: E402
from dataclasses import dataclass  # noqa: E402
from pathlib import Path  # noqa: E402
from typing import Annotated, Optional  # noqa: E402

import typer  # noqa: E402
from rich.console import Console  # noqa: E402
from rich.table import Table  # noqa: E402

from ag import __version__  # noqa: E402
from ag.config import get_workspace_dir  # noqa: E402
from ag.core import FinalStatus, RunTrace, VerifierStatus, create_runtime  # noqa: E402
from ag.core.task_spec import ExecutionMode  # noqa: E402
from ag.skills import get_default_registry  # noqa: E402
from ag.storage import SQLiteArtifactStore, SQLiteRunStore  # noqa: E402

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


def _not_implemented(
    cmd_name: str,
    json_mode: bool = False,
    extra_msg: str | None = None,
) -> None:
    """Print stub message and exit with error code.

    Centralized helper for consistent "Not implemented in v0" behavior (AF-0012).

    Args:
        cmd_name: Name of the command (e.g., "ag runs tail")
        json_mode: If True, output JSON error structure
        extra_msg: Optional additional message (e.g., workaround)
    """
    if json_mode:
        error_data = {
            "error": "not_implemented",
            "command": cmd_name,
            "message": f"{cmd_name} is not implemented in v0",
            "version": "v0",
        }
        if extra_msg:
            error_data["hint"] = extra_msg
        console.print(json.dumps(error_data, indent=2))
    else:
        err_console.print(f"[yellow]⚠ {cmd_name}[/yellow] is not implemented in v0")
        if extra_msg:
            err_console.print(f"  [dim]{extra_msg}[/dim]")
    raise typer.Exit(code=1)


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
        Dict with keys: mode, status, verifier_status, duration, playbook,
        run_id, workspace_id, workspace_source
    """
    return {
        "mode": trace.mode.value,
        "status": trace.final.value,
        "verifier_status": trace.verifier.status.value,
        "duration": f"{trace.duration_ms}ms" if trace.duration_ms else "unknown",
        "playbook": f"{trace.playbook.name}@{trace.playbook.version}",
        "run_id": trace.run_id,
        "workspace_id": trace.workspace_id,
        "workspace_source": trace.workspace_source.value if trace.workspace_source else "unknown",
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
    skill: Optional[str] = typer.Option(
        None, "--skill", "-s", help="Run a specific skill directly (bypasses playbook)."
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

    # AF-0027: Workspace selection policy with new precedence
    # 1. --workspace flag (highest priority)
    # 2. Persisted default workspace (CLI-set via `ag ws use`)
    # 3. AG_WORKSPACE env var
    # 4. Bootstrap: create 'default' workspace if no workspaces exist
    # 5. Error with guidance
    from ag.config import get_persisted_default_workspace
    from ag.storage import Workspace

    workspace_source = None  # Track where the workspace came from (for AF-0030)
    resolved_workspace = workspace if workspace is not None else cli_ctx.workspace

    if resolved_workspace is not None:
        workspace_source = "cli"
    else:
        # Try persisted default workspace
        persisted_default = get_persisted_default_workspace()
        if persisted_default:
            resolved_workspace = persisted_default
            workspace_source = "persisted"
        else:
            # Try AG_WORKSPACE env var
            env_workspace = os.environ.get("AG_WORKSPACE")
            if env_workspace:
                resolved_workspace = env_workspace
                workspace_source = "env"

    # If still no workspace, check for bootstrap case
    if resolved_workspace is None:
        workspaces_root = get_workspace_dir()
        existing_workspaces = []
        if workspaces_root.exists():
            existing_workspaces = [d for d in workspaces_root.iterdir() if d.is_dir()]

        if not existing_workspaces:
            # Bootstrap case: no workspaces exist, create 'default'
            resolved_workspace = "default"
            workspace_source = "bootstrap"
            ws = Workspace(resolved_workspace, workspaces_root)
            ws.ensure_exists()
            if not resolved_quiet and not resolved_json:
                console.print(f"[dim]Created default workspace:[/dim] {resolved_workspace}")
        else:
            # Workspaces exist but none selected
            err_console.print("[bold red]Error:[/bold red] No workspace specified.")
            err_console.print()
            err_console.print("Specify a workspace using one of:")
            err_console.print("  1. [cyan]--workspace <name>[/cyan] flag")
            err_console.print("  2. [cyan]ag ws use <name>[/cyan] to set a default")
            err_console.print("  3. [cyan]AG_WORKSPACE[/cyan] environment variable")
            err_console.print()
            err_console.print("Available workspaces:")
            for ws_dir in sorted(existing_workspaces)[:5]:
                err_console.print(f"  - {ws_dir.name}")
            if len(existing_workspaces) > 5:
                err_console.print(f"  ... and {len(existing_workspaces) - 5} more")
            raise typer.Exit(code=1)

    # Validate workspace exists (unless we just created it)
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

    # Validate playbook if specified (AF-0072: no silent fallback)
    if playbook:
        from ag.playbooks import get_playbook, list_playbooks

        if get_playbook(playbook) is None:
            available = list_playbooks()
            err_console.print(f"[bold red]Error:[/bold red] Playbook '{playbook}' not found.")
            err_console.print(f"Available playbooks: {', '.join(available)}")
            err_console.print("Run [cyan]ag playbooks list[/cyan] for details.")
            raise typer.Exit(code=1)

    # Direct skill execution mode (bypasses playbook)
    if skill:
        from datetime import UTC, datetime
        from uuid import uuid4

        from ag.core.run_trace import PlaybookMetadata, Step, StepType, Verifier

        registry = get_default_registry()
        if not registry.has(skill):
            err_console.print(f"[bold red]Error:[/bold red] Skill not found: {skill}")
            err_console.print("\nAvailable skills:")
            for name in sorted(registry.list()):
                err_console.print(f"  - {name}")
            raise typer.Exit(code=1)

        # Generate run ID and timestamps
        run_id = str(uuid4())
        started_at = datetime.now(UTC)

        try:
            # Execute skill directly with prompt and workspace path
            skill_params = {
                "prompt": prompt,
                "workspace": resolved_workspace,
                "workspace_path": str(ws.path),  # Full path for skills that need it
            }
            success, output_summary, result = registry.execute(skill, skill_params)

            ended_at = datetime.now(UTC)
            duration_ms = int((ended_at - started_at).total_seconds() * 1000)

            # BUG0010: Extract evidence_refs from skill result (if present)
            from ag.core.run_trace import Artifact, EvidenceRef

            evidence_refs: list[EvidenceRef] = []
            if result and "brief" in result:
                # Strategic brief skill returns nested structure with citations
                brief_data = result.get("brief", {})
                sections = brief_data.get("sections", [])

                # Build source map for excerpt lookup
                sources = brief_data.get("sources", [])
                source_map: dict[str, dict] = {s.get("path", ""): s for s in sources}

                seen_refs: set[str] = set()  # Deduplicate by source_path
                for section in sections:
                    citations = section.get("citations", [])
                    for citation in citations:
                        source_path = citation.get("source_path", "")
                        if source_path and source_path not in seen_refs:
                            seen_refs.add(source_path)

                            # Look up excerpt details from source
                            excerpt: str | None = None
                            line_start: int | None = None
                            line_end: int | None = None

                            source_data = source_map.get(source_path, {})
                            excerpt_idx = citation.get("excerpt_index")
                            if excerpt_idx is not None:
                                excerpts = source_data.get("excerpts", [])
                                if 0 <= excerpt_idx < len(excerpts):
                                    exc = excerpts[excerpt_idx]
                                    excerpt = exc.get("content", "")[:200]
                                    line_start = exc.get("line_start")
                                    line_end = exc.get("line_end")

                            evidence_refs.append(
                                EvidenceRef(
                                    ref_id=f"cite-{len(evidence_refs)}",
                                    source_type="file",
                                    source_path=source_path,
                                    excerpt=excerpt,
                                    line_start=line_start,
                                    line_end=line_end,
                                    relevance=citation.get("context") or None,
                                )
                            )

            # Create step record for the skill execution
            step = Step(
                step_id=f"{run_id}-step-0",
                step_number=0,
                step_type=StepType.SKILL_CALL,
                skill_name=skill,
                input_summary=prompt[:100] if prompt else "",
                output_summary=output_summary,
                started_at=started_at,
                ended_at=ended_at,
                duration_ms=duration_ms,
                error=None if success else output_summary,
                evidence_refs=evidence_refs if evidence_refs else None,
            )

            # BUG0009: Run verifier on step (not skipped)
            from ag.core.runtime import V0Verifier

            verifier = V0Verifier()
            final_status = FinalStatus.SUCCESS if success else FinalStatus.FAILURE
            verify_status, verify_message = verifier.verify_components([step], final_status)

            # Create RunTrace for persistence (artifacts will be updated after saving)
            trace = RunTrace(
                run_id=run_id,
                workspace_id=resolved_workspace,
                workspace_source=None,
                mode=ExecutionMode.SUPERVISED,
                playbook=PlaybookMetadata(name=f"skill:{skill}", version="1.0.0"),
                started_at=started_at,
                ended_at=ended_at,
                duration_ms=duration_ms,
                steps=[step],
                artifacts=[],  # Will be updated after artifact save
                verifier=Verifier(
                    status=VerifierStatus(verify_status),
                    checked_at=ended_at,
                    message=verify_message,
                ),
                final=final_status,
                error=None if success else output_summary,
            )

            # Persist run to storage
            run_store = _get_run_store()
            artifact_store = _get_artifact_store()

            # Save skill result as artifacts
            artifacts_saved: list[Artifact] = []
            artifact_ids: list[str] = []
            if result:
                # Save JSON result
                json_artifact_id = f"{run_id}-{skill}_result"
                json_content = json.dumps(result, indent=2, default=str).encode("utf-8")
                json_artifact = Artifact(
                    artifact_id=json_artifact_id,
                    path=f"{skill}_result.json",
                    artifact_type="application/json",
                    size_bytes=len(json_content),
                )
                artifact_store.save(
                    workspace_id=resolved_workspace,
                    run_id=run_id,
                    artifact=json_artifact,
                    content=json_content,
                )
                artifacts_saved.append(json_artifact)
                artifact_ids.append(json_artifact_id)

                # If result has markdown output, save that too
                if "brief_md" in result:
                    md_artifact_id = f"{run_id}-{skill}_brief"
                    md_content = result["brief_md"].encode("utf-8")
                    md_artifact = Artifact(
                        artifact_id=md_artifact_id,
                        path=f"{skill}_brief.md",
                        artifact_type="text/markdown",
                        size_bytes=len(md_content),
                    )
                    artifact_store.save(
                        workspace_id=resolved_workspace,
                        run_id=run_id,
                        artifact=md_artifact,
                        content=md_content,
                    )
                    artifacts_saved.append(md_artifact)
                    artifact_ids.append(md_artifact_id)

            # BUG0010: Update trace with Artifact objects before saving
            trace.artifacts = artifacts_saved
            run_store.save(trace)

            if resolved_json:
                console.print(
                    json.dumps(
                        {
                            "run_id": run_id,
                            "skill": skill,
                            "success": success,
                            "verified": verify_status,
                            "verification_message": verify_message,
                            "output": output_summary,
                            "result": result,
                            "artifacts": artifact_ids,
                        },
                        indent=2,
                    )
                )
            else:
                status = "[green]✓ Success[/green]" if success else "[red]✗ Failed[/red]"
                verified_display = (
                    f"[green]{verify_status}[/green]"
                    if verify_status == "PASS"
                    else f"[yellow]{verify_status}[/yellow]"
                )
                if not resolved_quiet:
                    console.print()
                    console.print(f"[bold]Skill executed:[/bold] {skill}")
                    console.print(f"  Run ID: {run_id}")
                    console.print(f"  Status: {status}")
                    console.print(f"  Verified: {verified_display}")
                    console.print(f"  Output: {output_summary}")
                    console.print(f"  Duration: {duration_ms}ms")
                    if artifact_ids:
                        console.print(f"  Artifacts: {len(artifact_ids)} saved")

                    if resolved_verbose and result:
                        console.print()
                        console.print("[dim]Result data:[/dim]")
                        console.print(json.dumps(result, indent=2, default=str))

            raise typer.Exit(code=0 if success else 1)

        except typer.Exit:
            raise  # Re-raise typer.Exit unchanged
        except Exception as e:
            err_console.print(f"[bold red]Error executing skill:[/bold red] {e}")
            raise typer.Exit(code=1)

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
            workspace_source=workspace_source,
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
    limit: int = typer.Option(10, "--limit", "-n", help="Max runs to show (default: 10)."),
    all_runs: bool = typer.Option(False, "--all", "-a", help="Show all runs (ignores --limit)."),
    status: Optional[str] = typer.Option(
        None, "--status", "-s", help="Filter by status (success/failure)."
    ),
    workspace: Optional[str] = typer.Option(None, "--workspace", "-w", help="Filter by workspace."),
    json_output: bool = typer.Option(False, "--json", help="Output JSON."),
) -> None:
    """List recent runs.

    Shows most recent runs first. By default shows 10 runs.
    Use --all to show all runs, or --limit N to show N runs.
    """
    # Resolve global options
    cli_ctx = get_cli_ctx(ctx)
    resolved_workspace = workspace if workspace is not None else cli_ctx.workspace
    resolved_json = json_output or cli_ctx.json_output

    if not resolved_workspace:
        err_console.print("[bold red]Error:[/bold red] --workspace is required for runs list")
        raise typer.Exit(code=1)

    run_store = _get_run_store()

    try:
        # Get total count for pagination info
        total_count = run_store.count(resolved_workspace)

        # Use high limit when --all is specified
        effective_limit = 10000 if all_runs else limit
        runs = run_store.list(resolved_workspace, limit=effective_limit)

        # Filter by status if provided
        if status:
            status_filter = status.lower()
            runs = [r for r in runs if r.final.value == status_filter]

        if resolved_json:
            output = {
                "total": total_count,
                "showing": len(runs),
                "runs": [json.loads(r.to_json()) for r in runs],
            }
            console.print(json.dumps(output, indent=2))
        else:
            if not runs:
                console.print(f"No runs found in workspace '{resolved_workspace}'")
                return

            # Show pagination info in title
            if all_runs or len(runs) >= total_count:
                title = f"Runs in workspace '{resolved_workspace}' ({total_count} total)"
            else:
                title = (
                    f"Runs in workspace '{resolved_workspace}' "
                    f"(showing {len(runs)} of {total_count})"
                )

            table = Table(title=title)
            table.add_column("Run ID", style="cyan", no_wrap=True)
            table.add_column("Status")
            table.add_column("Verifier")
            table.add_column("Mode")
            table.add_column("Model")  # AF-0062: Add model column
            table.add_column("Duration")
            table.add_column("Started")

            for run in runs:
                labels = extract_labels(run)
                # AF-0062: Show model or "manual" for manual runs
                model = run.llm.model if run.llm else "manual"
                table.add_row(
                    run.run_id,
                    format_status(run.final),
                    format_verifier(run.verifier.status),
                    labels["mode"],
                    model,
                    labels["duration"],
                    run.started_at.strftime("%Y-%m-%d %H:%M"),
                )

            console.print(table)

            # Show hint if truncated
            if not all_runs and len(runs) < total_count:
                console.print(
                    f"[dim]Use --all to show all {total_count} runs, "
                    f"or --limit N to show more.[/dim]"
                )

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
            console.print(f"  Workspace Source: {labels['workspace_source']}")
            console.print(f"  Mode: {labels['mode']}")
            console.print(f"  Status: {format_status(trace.final)}")
            console.print(f"  Verifier: {format_verifier(trace.verifier.status)}")
            if trace.verifier.message:
                console.print(f"    Message: {trace.verifier.message}")
            console.print(f"  Duration: {labels['duration']}")
            console.print(f"  Playbook: {labels['playbook']}")
            # AF-0062: Show LLM provider info
            if trace.llm:
                console.print(f"  LLM: {trace.llm.provider}/{trace.llm.model}")
            else:
                console.print("  LLM: manual (no LLM)")
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


@runs_app.command("stats")
def runs_stats(
    ctx: typer.Context,
    workspace: Optional[str] = typer.Option(
        None, "--workspace", "-w", help="Workspace to get stats for."
    ),
    json_output: bool = typer.Option(False, "--json", help="Output JSON."),
) -> None:
    """Show aggregate statistics for runs (AF-0032)."""
    cli_ctx = get_cli_ctx(ctx)
    resolved_workspace = workspace if workspace is not None else cli_ctx.workspace
    resolved_json = json_output or cli_ctx.json_output

    if not resolved_workspace:
        err_console.print("[bold red]Error:[/bold red] --workspace is required for runs stats")
        raise typer.Exit(code=1)

    run_store = _get_run_store()

    try:
        # Get all runs (use high limit for stats)
        runs = run_store.list(resolved_workspace, limit=1000)

        if not runs:
            if resolved_json:
                console.print(json.dumps({"total_runs": 0}))
            else:
                console.print(f"No runs found in workspace '{resolved_workspace}'")
            return

        # Calculate statistics
        total = len(runs)
        by_status: dict[str, int] = {}
        by_verifier: dict[str, int] = {}
        by_mode: dict[str, int] = {}
        total_duration_ms = 0
        runs_with_duration = 0

        for run in runs:
            # Count by status
            status = run.final.value
            by_status[status] = by_status.get(status, 0) + 1

            # Count by verifier status
            vstat = run.verifier.status.value
            by_verifier[vstat] = by_verifier.get(vstat, 0) + 1

            # Count by mode
            mode = run.mode.value
            by_mode[mode] = by_mode.get(mode, 0) + 1

            # Sum durations
            if run.duration_ms:
                total_duration_ms += run.duration_ms
                runs_with_duration += 1

        avg_duration_ms = total_duration_ms // runs_with_duration if runs_with_duration else 0

        if resolved_json:
            stats = {
                "workspace": resolved_workspace,
                "total_runs": total,
                "by_status": by_status,
                "by_verifier_status": by_verifier,
                "by_mode": by_mode,
                "avg_duration_ms": avg_duration_ms,
            }
            console.print(json.dumps(stats, indent=2))
        else:
            console.print(f"[bold]Statistics for workspace '{resolved_workspace}'[/bold]")
            console.print()
            console.print(f"  Total runs: {total}")
            console.print(f"  Average duration: {avg_duration_ms}ms")
            console.print()
            console.print("[bold]By Status:[/bold]")
            for status, count in sorted(by_status.items()):
                console.print(f"  {status}: {count}")
            console.print()
            console.print("[bold]By Verifier Status:[/bold]")
            for vstat, count in sorted(by_verifier.items()):
                console.print(f"  {vstat}: {count}")
            console.print()
            console.print("[bold]By Mode:[/bold]")
            for mode, count in sorted(by_mode.items()):
                console.print(f"  {mode}: {count}")

    finally:
        run_store.close()


@runs_app.command("tail")
def runs_tail(
    run_id: Annotated[str, typer.Argument(help="Run ID to stream logs from")],
    json_output: Annotated[
        bool, typer.Option("--json", help="Output as JSON")
    ] = False,
) -> None:
    """Stream live output from a running agent session (stub)."""
    _not_implemented("ag runs tail", json_mode=json_output)


# ─────────────────────────────────────────────────────────────────────────────
# ag ws (workspace)
# ─────────────────────────────────────────────────────────────────────────────


@ws_app.command("list")
def ws_list() -> None:
    """List all workspaces."""
    from ag.config import get_persisted_default_workspace

    workspaces_root = get_workspace_dir()
    default_ws = get_persisted_default_workspace()

    if not workspaces_root.exists():
        console.print("[dim]No workspaces found.[/dim]")
        console.print("Create one with: [cyan]ag ws create <name>[/cyan]")
        return

    workspace_dirs = [d for d in workspaces_root.iterdir() if d.is_dir()]
    if not workspace_dirs:
        console.print("[dim]No workspaces found.[/dim]")
        console.print("Create one with: [cyan]ag ws create <name>[/cyan]")
        return

    table = Table(title="Workspaces")
    table.add_column("Workspace ID", style="cyan")
    table.add_column("Default", style="green")
    table.add_column("Path")

    for ws_dir in sorted(workspace_dirs):
        is_default = "✓" if ws_dir.name == default_ws else ""
        table.add_row(ws_dir.name, is_default, str(ws_dir))

    console.print(table)

    if default_ws:
        console.print(f"\n[dim]Default workspace:[/dim] {default_ws}")


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
    """Switch to a workspace (sets as default for future commands)."""
    from ag.config import get_persisted_default_workspace, set_persisted_default_workspace
    from ag.storage import Workspace

    # Validate workspace exists
    ws = Workspace(workspace_id, get_workspace_dir())
    if not ws.exists():
        err_console.print(f"[bold red]Error:[/bold red] Workspace '{workspace_id}' does not exist.")
        err_console.print(f"Create it first: [cyan]ag ws create {workspace_id}[/cyan]")
        raise typer.Exit(code=1)

    # Set as persisted default
    set_persisted_default_workspace(workspace_id)
    console.print(f"[green]Default workspace set to:[/green] {workspace_id}")

    # Show current default
    current = get_persisted_default_workspace()
    if current == workspace_id:
        console.print("  Future commands will use this workspace by default.")


@ws_app.command("show")
def ws_show(
    workspace_id: Optional[str] = typer.Argument(None, help="Workspace ID (default: current)."),
) -> None:
    """Show workspace details."""
    from ag.config import get_persisted_default_workspace
    from ag.storage import Workspace

    # If no workspace specified, use the default
    if workspace_id is None:
        workspace_id = get_persisted_default_workspace()

    if workspace_id is None:
        err_console.print("[bold red]Error:[/bold red] No workspace specified and no default set.")
        err_console.print("Specify a workspace: [cyan]ag ws show <workspace_id>[/cyan]")
        err_console.print("Or set a default:    [cyan]ag ws use <workspace_id>[/cyan]")
        raise typer.Exit(code=1)

    ws = Workspace(workspace_id, get_workspace_dir())
    if not ws.exists():
        err_console.print(f"[bold red]Error:[/bold red] Workspace '{workspace_id}' does not exist.")
        raise typer.Exit(code=1)

    default_ws = get_persisted_default_workspace()
    is_default = workspace_id == default_ws

    console.print(f"[bold]Workspace:[/bold] {workspace_id}")
    console.print(f"  Path: {ws.path}")
    console.print(f"  Default: {'Yes' if is_default else 'No'}")

    # Count runs if store exists
    runs_db = ws.path / "runs.db"
    if runs_db.exists():
        console.print(f"  Database: {runs_db}")
    else:
        console.print("  Database: [dim]not created yet[/dim]")


# Create ws config sub-app for workspace-level configuration
ws_config_app = typer.Typer(help="Workspace configuration commands.")
ws_app.add_typer(ws_config_app, name="config")


@ws_config_app.command("get")
def ws_config_get(
    key: Annotated[str, typer.Argument(help="Configuration key to retrieve")],
    workspace_id: Annotated[
        Optional[str], typer.Option("--workspace", "-w", help="Workspace ID (default: current)")
    ] = None,
    json_output: Annotated[
        bool, typer.Option("--json", help="Output as JSON")
    ] = False,
) -> None:
    """Get a workspace configuration value (stub)."""
    _not_implemented("ag ws config get", json_mode=json_output)


@ws_config_app.command("set")
def ws_config_set(
    key: Annotated[str, typer.Argument(help="Configuration key to set")],
    value: Annotated[str, typer.Argument(help="Value to set")],
    workspace_id: Annotated[
        Optional[str], typer.Option("--workspace", "-w", help="Workspace ID (default: current)")
    ] = None,
    json_output: Annotated[
        bool, typer.Option("--json", help="Output as JSON")
    ] = False,
) -> None:
    """Set a workspace configuration value (stub)."""
    _not_implemented("ag ws config set", json_mode=json_output)


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
def artifacts_show(
    ctx: typer.Context,
    artifact_id: str = typer.Argument(..., help="Artifact ID."),
    run_id: str = typer.Option(..., "--run", "-r", help="Run ID."),
    workspace: Optional[str] = typer.Option(None, "--workspace", "-w", help="Workspace ID."),
    json_output: bool = typer.Option(False, "--json", help="Output JSON."),
) -> None:
    """Show artifact details and preview content."""
    from ag.core import ArtifactCategory

    cli_ctx = get_cli_ctx(ctx)
    resolved_workspace = workspace if workspace is not None else cli_ctx.workspace
    resolved_json = json_output or cli_ctx.json_output

    if not resolved_workspace:
        err_console.print("[bold red]Error:[/bold red] --workspace is required for artifact show.")
        raise typer.Exit(code=1)

    artifact_store = _get_artifact_store()

    result = artifact_store.get(resolved_workspace, run_id, artifact_id)
    if result is None:
        err_console.print(f"[bold red]Error:[/bold red] Artifact {artifact_id} not found.")
        artifact_store.close()
        raise typer.Exit(code=1)

    artifact, content = result

    if resolved_json:
        json_data = {
            "artifact_id": artifact.artifact_id,
            "path": artifact.path,
            "artifact_type": artifact.artifact_type,
            "category": artifact.get_category().value,
            "size_bytes": artifact.size_bytes,
            "checksum": artifact.checksum,
            "created_at": artifact.created_at.isoformat() if artifact.created_at else None,
            "metadata": artifact.metadata,
        }
        print(json.dumps(json_data, indent=2))
    else:
        category = artifact.get_category()
        console.print(f"[bold]Artifact:[/bold] {artifact.artifact_id}")
        console.print(f"  [dim]Path:[/dim] {artifact.path}")
        console.print(f"  [dim]Type:[/dim] {artifact.artifact_type}")
        console.print(f"  [dim]Category:[/dim] {category.value}")
        if artifact.size_bytes is not None:
            console.print(f"  [dim]Size:[/dim] {artifact.size_bytes} bytes")
        if artifact.checksum:
            console.print(f"  [dim]Checksum:[/dim] {artifact.checksum}")
        if artifact.created_at:
            console.print(f"  [dim]Created:[/dim] {artifact.created_at.isoformat()}")

        # Preview content for text-based artifacts
        if category in (
            ArtifactCategory.RESULT,
            ArtifactCategory.DOCUMENT,
            ArtifactCategory.LOG,
            ArtifactCategory.CODE,
            ArtifactCategory.DATA,
            ArtifactCategory.CONFIG,
        ):
            try:
                text = content.decode("utf-8")
                lines = text.split("\n")
                preview_lines = lines[:20]
                console.print("\n[bold]Content preview:[/bold]")
                for line in preview_lines:
                    console.print(f"  {line}")
                if len(lines) > 20:
                    console.print(f"  [dim]... ({len(lines) - 20} more lines)[/dim]")
            except UnicodeDecodeError:
                console.print("\n[dim]Binary content - cannot preview[/dim]")
        else:
            console.print(f"\n[dim]Binary content ({len(content)} bytes)[/dim]")

    artifact_store.close()


@artifacts_app.command("export")
def artifacts_export(
    ctx: typer.Context,
    artifact_id: str = typer.Argument(..., help="Artifact ID to export."),
    run_id: str = typer.Option(..., "--run", "-r", help="Run ID."),
    workspace: Optional[str] = typer.Option(None, "--workspace", "-w", help="Workspace ID."),
    output_path: str = typer.Option(..., "--to", "-o", help="Destination path for export."),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite if file exists."),
) -> None:
    """Export artifact content to a local file.

    Copies the artifact content to the specified destination path.
    Use --force to overwrite existing files.
    """
    cli_ctx = get_cli_ctx(ctx)
    resolved_workspace = workspace if workspace is not None else cli_ctx.workspace

    if not resolved_workspace:
        err_console.print(
            "[bold red]Error:[/bold red] --workspace is required for artifact export."
        )
        raise typer.Exit(code=1)

    # Check if output path already exists
    output = Path(output_path)
    if output.exists() and not force:
        err_console.print(
            f"[bold red]Error:[/bold red] {output_path} already exists. Use --force to overwrite."
        )
        raise typer.Exit(code=1)

    artifact_store = _get_artifact_store()

    result = artifact_store.get(resolved_workspace, run_id, artifact_id)
    if result is None:
        err_console.print(f"[bold red]Error:[/bold red] Artifact {artifact_id} not found.")
        artifact_store.close()
        raise typer.Exit(code=1)

    artifact, content = result

    # Create parent directories if needed
    output.parent.mkdir(parents=True, exist_ok=True)

    # Write content to file
    output.write_bytes(content)

    console.print(f"[green]✓[/green] Exported {artifact.artifact_id} to {output_path}")
    console.print(f"  [dim]Size: {len(content)} bytes[/dim]")
    console.print(f"  [dim]Category: {artifact.get_category().value}[/dim]")

    artifact_store.close()


@artifacts_app.command("open")
def artifacts_open(
    artifact_id: Annotated[str, typer.Argument(help="Artifact ID to open")],
    run_id: Annotated[str, typer.Option("--run", "-r", help="Run ID")],
    workspace: Annotated[
        Optional[str], typer.Option("--workspace", "-w", help="Workspace ID")
    ] = None,
    json_output: Annotated[
        bool, typer.Option("--json", help="Output as JSON")
    ] = False,
) -> None:
    """Open artifact in system viewer (stub)."""
    _not_implemented("ag artifacts open", json_mode=json_output)


# ─────────────────────────────────────────────────────────────────────────────
# ag skills
# ─────────────────────────────────────────────────────────────────────────────


@skills_app.command("list")
def skills_list() -> None:
    """List available skills."""
    registry = get_default_registry()
    skills = sorted(registry.list())

    if not skills:
        console.print("[dim]No skills registered.[/dim]")
        return

    table = Table(title="Registered Skills")
    table.add_column("Name", style="cyan")
    table.add_column("Source", style="dim")
    table.add_column("Description")

    for name in skills:
        info = registry.get_info(name)
        desc = info["description"] if info else ""
        source = info["source"] if info else "unknown"
        table.add_row(name, source, desc)

    console.print(table)


@skills_app.command("info")
def skills_info(skill_name: str = typer.Argument(..., help="Skill name.")) -> None:
    """Show skill details."""
    registry = get_default_registry()
    info = registry.get_info(skill_name)

    if not info:
        err_console.print(f"[bold red]Error:[/bold red] Skill not found: {skill_name}")
        err_console.print("\nAvailable skills:")
        for name in sorted(registry.list()):
            err_console.print(f"  - {name}")
        raise typer.Exit(code=1)

    console.print(f"[bold]Skill:[/bold] {info['name']}")
    console.print(f"[bold]Source:[/bold] {info['source']}")
    console.print(f"[bold]Description:[/bold] {info['description']}")


@skills_app.command("test")
def skills_test(
    skill_name: Annotated[str, typer.Argument(help="Skill name to test")],
    json_output: Annotated[
        bool, typer.Option("--json", help="Output as JSON")
    ] = False,
) -> None:
    """Run skill unit tests (stub)."""
    _not_implemented("ag skills test", json_mode=json_output)


@skills_app.command("enable")
def skills_enable(
    skill_name: Annotated[str, typer.Argument(help="Skill name to enable")],
    json_output: Annotated[
        bool, typer.Option("--json", help="Output as JSON")
    ] = False,
) -> None:
    """Enable a skill for agent sessions (stub)."""
    _not_implemented("ag skills enable", json_mode=json_output)


@skills_app.command("disable")
def skills_disable(
    skill_name: Annotated[str, typer.Argument(help="Skill name to disable")],
    json_output: Annotated[
        bool, typer.Option("--json", help="Output as JSON")
    ] = False,
) -> None:
    """Disable a skill for agent sessions (stub)."""
    _not_implemented("ag skills disable", json_mode=json_output)


# ─────────────────────────────────────────────────────────────────────────────
# ag playbooks
# ─────────────────────────────────────────────────────────────────────────────


@playbooks_app.command("list")
def playbooks_list(
    json_output: bool = typer.Option(False, "--json", help="Output as JSON."),
) -> None:
    """List available playbooks."""
    from ag.playbooks.registry import list_playbooks_detailed

    playbooks = list_playbooks_detailed()

    if json_output:
        import json

        print(json.dumps(playbooks, indent=2))
        return

    # Build Rich table
    from rich.table import Table

    table = Table(title="Available Playbooks")
    table.add_column("Name", style="cyan")
    table.add_column("Version", style="dim")
    table.add_column("Source", style="dim")
    table.add_column("Stability", style="yellow")
    table.add_column("Description")

    for pb in playbooks:
        stability = pb.get("stability", "unknown")
        source = pb.get("source", "unknown")

        # Color coding for stability
        if stability == "production":
            stability_display = f"[green]{stability}[/green]"
        elif stability in ("test", "experimental"):
            stability_display = f"[yellow]{stability}[/yellow]"
        else:
            stability_display = f"[dim]{stability}[/dim]"

        table.add_row(
            pb.get("name", ""),
            pb.get("version", ""),
            source,
            stability_display,
            pb.get("description", ""),
        )

    console.print(table)


@playbooks_app.command("show")
def playbooks_show(
    name: Annotated[str, typer.Argument(help="Playbook name")],
    json_output: Annotated[
        bool, typer.Option("--json", help="Output as JSON")
    ] = False,
) -> None:
    """Show playbook details (stub)."""
    _not_implemented("ag playbooks show", json_mode=json_output)


@playbooks_app.command("validate")
def playbooks_validate(
    name: Annotated[str, typer.Argument(help="Playbook name or path to validate")],
    json_output: Annotated[
        bool, typer.Option("--json", help="Output as JSON")
    ] = False,
) -> None:
    """Validate playbook syntax and semantics (stub)."""
    _not_implemented("ag playbooks validate", json_mode=json_output)


@playbooks_app.command("set-default")
def playbooks_set_default(
    name: Annotated[str, typer.Argument(help="Playbook name to set as default")],
    json_output: Annotated[
        bool, typer.Option("--json", help="Output as JSON")
    ] = False,
) -> None:
    """Set the default playbook for new agent sessions (stub)."""
    _not_implemented("ag playbooks set-default", json_mode=json_output)


# ─────────────────────────────────────────────────────────────────────────────
# ag config
# ─────────────────────────────────────────────────────────────────────────────


@config_app.command("list")
def config_list(
    json_output: Annotated[
        bool, typer.Option("--json", help="Output as JSON")
    ] = False,
) -> None:
    """List all configuration values (stub)."""
    _not_implemented("ag config list", json_mode=json_output)


@config_app.command("get")
def config_get(
    key: Annotated[str, typer.Argument(help="Config key")],
    json_output: Annotated[
        bool, typer.Option("--json", help="Output as JSON")
    ] = False,
) -> None:
    """Get a configuration value (stub)."""
    _not_implemented("ag config get", json_mode=json_output)


@config_app.command("set")
def config_set(
    key: Annotated[str, typer.Argument(help="Config key")],
    value: Annotated[str, typer.Argument(help="Config value")],
    json_output: Annotated[
        bool, typer.Option("--json", help="Output as JSON")
    ] = False,
) -> None:
    """Set a configuration value (stub)."""
    _not_implemented("ag config set", json_mode=json_output)


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
