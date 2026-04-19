# BUG-0003 — Missing CLI subcommands per reference spec
# Version number: v0.1

## Metadata
- **ID:** BUG-0003
- **Status:** OPEN
- **Severity:** P2
- **Area:** CLI
- **Reported by:** Jacob
- **Date:** 2026-02-24
- **Related backlog item(s):** AF-0008
- **Related PR(s):** —

## Summary
Several CLI subcommands documented in CLI_REFERENCE.md do not exist in the current implementation. While existing commands work (or are stubs as expected), entire subcommands are missing from subcommand groups.

## Expected vs Actual

### ag ws
| Subcommand | CLI Reference | Current |
|------------|---------------|---------|
| `list` | ✅ | ⚠ Stub |
| `create <name>` | ✅ | ⚠ Stub |
| `use <id>` | ✅ | ⚠ Stub |
| `show [<id>]` | ✅ | ⚠ Stub |
| `config get <key>` | ✅ | ❌ Missing |
| `config set <key> <value>` | ✅ | ❌ Missing |

### ag artifacts
| Subcommand | CLI Reference | Current |
|------------|---------------|---------|
| `list [--run <run_id>]` | ✅ | ✅ Works |
| `show <artifact_id>` | ✅ | ⚠ Stub |
| `open <artifact_id>` | ✅ (optional) | ❌ Missing |
| `export <artifact_id> --to <path>` | ✅ | ❌ Missing |

### ag skills
| Subcommand | CLI Reference | Current |
|------------|---------------|---------|
| `list` | ✅ | ⚠ Stub |
| `info <skill_name>` | ✅ | ⚠ Stub |
| `test <skill_name>` | ✅ (dev) | ❌ Missing |
| `enable <skill_name>` | ✅ | ❌ Missing |
| `disable <skill_name>` | ✅ | ❌ Missing |

### ag playbooks
| Subcommand | CLI Reference | Current |
|------------|---------------|---------|
| `list` | ✅ | ⚠ Stub |
| `show <name>` | ✅ | ⚠ Stub |
| `validate <path>` | ✅ (dev) | ❌ Missing |
| `set-default <name>` | ✅ | ❌ Missing |

### ag runs
| Subcommand | CLI Reference | Current |
|------------|---------------|---------|
| `list` | ✅ | ✅ Works |
| `show` | ✅ | ✅ Works |
| `trace` | ✅ | ✅ Works |
| `tail <run_id>` | ✅ (planned) | ❌ Missing |

## Reproduction steps
1. Run `ag ws config --help`
2. Observe: `Error: No such command 'config'.`
3. Run `ag artifacts export --help`
4. Observe: `Error: No such command 'export'.`
5. Repeat for other missing subcommands.

## Evidence
- **CLI_REFERENCE.md:** Full synopsis for each command group
- **main.py:** Only subset of subcommands defined

## Impact
- Users cannot manage workspace configuration via CLI
- No way to export artifacts to local paths
- Skills cannot be enabled/disabled per workspace
- Playbooks cannot be validated before use
- CLI does not match documented contract

## Suspected cause
These were likely scoped out of CLI v0 (AF-0008) to keep initial implementation minimal. The reference spec represents the target state, not v0 scope.

## Proposed fix
Add stub implementations for all missing subcommands to establish the CLI surface. Each stub should:
1. Accept the correct arguments per CLI_REFERENCE.md
2. Print a descriptive stub message with the backlog item reference
3. Exit cleanly

Example for `ag ws config`:
```python
ws_config_app = typer.Typer(help="Workspace configuration.")
ws_app.add_typer(ws_config_app, name="config")

@ws_config_app.command("get")
def ws_config_get(key: str = typer.Argument(..., help="Config key.")) -> None:
    """Get a workspace configuration value."""
    console.print(f"[dim]Key:[/dim] {key}")
    console.print("[yellow]⚠ Stub — not implemented yet[/yellow]")

@ws_config_app.command("set")
def ws_config_set(
    key: str = typer.Argument(..., help="Config key."),
    value: str = typer.Argument(..., help="Config value."),
) -> None:
    """Set a workspace configuration value."""
    console.print(f"[dim]Setting:[/dim] {key} = {value}")
    console.print("[yellow]⚠ Stub — not implemented yet[/yellow]")
```

## Acceptance criteria (for verification)
- [ ] `ag ws config get <key>` exists (stub)
- [ ] `ag ws config set <key> <value>` exists (stub)
- [ ] `ag artifacts open <artifact_id>` exists (stub)
- [ ] `ag artifacts export <artifact_id> --to <path>` exists (stub)
- [ ] `ag skills test <skill_name>` exists (stub)
- [ ] `ag skills enable <skill_name>` exists (stub)
- [ ] `ag skills disable <skill_name>` exists (stub)
- [ ] `ag playbooks validate <path>` exists (stub)
- [ ] `ag playbooks set-default <name>` exists (stub)
- [ ] `ag runs tail <run_id>` exists (stub)
- [ ] All stubs print helpful messages indicating future implementation
- [ ] CLI help output matches CLI_REFERENCE.md structure

## Notes
- Stubs establish the API contract and allow early user feedback
- Each stub can reference a future backlog item when created
- This is separate from implementing the actual functionality

