# AF-0097 — runs commands should use default workspace
# Version number: v0.1
# Created: 2026-03-12
# Status: DONE
# Priority: P2
# Area: CLI/UX

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`

---

## Summary

The `ag runs` subcommand group requires `--workspace` flag explicitly, while other commands use the default workspace. This is inconsistent UX that makes the CLI harder to use.

---

## Problem

**Commands that require `--workspace` explicitly:**
```bash
ag runs list           # Error: --workspace is required for runs list
ag runs show <id>      # Error: --workspace is required for runs show
ag runs trace <id>     # Error: --workspace is required for runs show
ag runs stats          # Error: --workspace is required for runs stats
```

**Commands that use default workspace:**
```bash
ag run "prompt"        # Uses default workspace (skills02)
ag ws show             # Uses default workspace
ag artifacts list -r   # Uses default workspace
ag artifacts show -r   # Uses default workspace
ag artifacts export -r # Uses default workspace
```

This inconsistency is confusing. If a user has set a default workspace, they expect all commands to use it unless overridden.

---

## User impact

1. Users must always type `--workspace <name>` for runs commands
2. Tab completion and `ag ws use <name>` feel useless for runs inspection
3. Workflow friction when debugging runs in the default workspace

---

## Acceptance criteria

- [ ] `ag runs list` uses default workspace when `--workspace` not specified
- [ ] `ag runs show <id>` uses default workspace when `--workspace` not specified
- [ ] `ag runs trace <id>` uses default workspace when `--workspace` not specified
- [ ] `ag runs stats` uses default workspace when `--workspace` not specified
- [ ] Error message shown if no default workspace is set AND `--workspace` not provided
- [ ] Tests updated / added for default workspace fallback behavior
- [ ] CLI_REFERENCE.md updated if needed

---

## Implementation approach

The fix is likely in `src/ag/cli/main.py`. The `runs_list`, `runs_show`, `runs_trace`, and `runs_stats` functions should resolve the workspace using the same pattern as `ag run`:

```python
# Current (broken)
if not resolved_workspace:
    err_console.print("[bold red]Error:[/bold red] --workspace is required for runs list")
    raise typer.Exit(code=1)

# Should be (consistent with ag run)
if not resolved_workspace:
    resolved_workspace = get_default_workspace()  # Or similar
    if not resolved_workspace:
        err_console.print("[bold red]Error:[/bold red] No workspace specified and no default set")
        raise typer.Exit(code=1)
```

---

## Related

- ADR-0008: CLI global flags (established `--workspace` as global flag)
- AF-0012: CLI_REFERENCE surface parity

---

## Notes

This should be a quick fix since the pattern already exists in `ag run`. The inconsistency likely stems from the `runs` commands being added before the default workspace feature was fully implemented.
