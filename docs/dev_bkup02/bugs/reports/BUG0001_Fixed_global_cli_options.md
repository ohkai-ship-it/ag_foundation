# BUG-0001 — Global CLI options not implemented as global
# Version number: v0.1

## Metadata
- **ID:** BUG-0001
- **Status:** FIXED
- **Severity:** P1
- **Area:** CLI
- **Reported by:** Jacob
- **Date:** 2026-02-24
- **Resolved:** 2026-02-26
- **Resolved by:** AF-0011
- **Related backlog item(s):** AF-0008, AF-0011
- **Related PR(s):** —

## Summary
The CLI_REFERENCE.md specifies global options (`--workspace`, `--json`, `--quiet`, `--verbose`) that should be available on the main `ag` app and inherited by all subcommands. Currently, these options are only implemented on specific commands inconsistently.

## Expected behavior
Per CLI_REFERENCE.md § "Command overview > Global":
- `--workspace <id>`: select workspace (default: current or configured default)
- `--json`: emit machine-readable JSON (where supported)
- `--quiet`: reduce non-essential output
- `--verbose`: include trace pointers, timing, and debug details

These should be global options on the main `ag` app callback, making them available to all subcommands.

## Actual behavior
| Option | `ag run` | `ag runs list` | `ag runs show` | `ag artifacts list` | `ag doctor` | Others |
|--------|----------|----------------|----------------|---------------------|-------------|--------|
| `--workspace` | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| `--json` | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| `--quiet` | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `--verbose` | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

Running `ag --help` shows only:
```
--version  -V
--install-completion
--show-completion
--help
```

No global `--workspace`, `--json`, `--quiet`, or `--verbose`.

## Reproduction steps
1. Run `ag --help`
2. Observe missing global options
3. Compare with CLI_REFERENCE.md § Global options

## Evidence
- **CLI_REFERENCE.md:** Lines 8-13 specify global options
- **main.py:** Lines 136-152 show `main()` callback has only `--version`

## Impact
- Inconsistent CLI experience across commands
- Users must remember which commands support which options
- Spec divergence creates confusion

## Suspected cause
Global options were only added to individual commands where immediately needed, rather than to the main app callback with context propagation.

## Proposed fix
1. Add global options to `main()` callback in `main.py`
2. Store values in Typer context (e.g., `ctx.obj`)
3. Read from context in subcommands, falling back to command-specific overrides if needed
4. Update stubs to respect `--json` and `--quiet` where sensible

Example pattern:
```python
@app.callback()
def main(
    ctx: typer.Context,
    workspace: Optional[str] = typer.Option(None, "--workspace", "-w"),
    json_output: bool = typer.Option(False, "--json"),
    quiet: bool = typer.Option(False, "--quiet", "-q"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
    version: Optional[bool] = typer.Option(None, "--version", "-V", ...),
) -> None:
    ctx.ensure_object(dict)
    ctx.obj["workspace"] = workspace
    ctx.obj["json"] = json_output
    ctx.obj["quiet"] = quiet
    ctx.obj["verbose"] = verbose
```

## Acceptance criteria (for verification)
- [ ] `ag --help` shows `--workspace`, `--json`, `--quiet`, `--verbose` as global options
- [ ] `ag runs list --workspace foo` still works (backward compatible)
- [ ] Global `--json` propagates to subcommands that support JSON output
- [ ] Global `--quiet` reduces output on all commands
- [ ] Tests validate global option propagation

## Notes
Typer supports context-based option inheritance. See: https://typer.tiangolo.com/tutorial/commands/context/

