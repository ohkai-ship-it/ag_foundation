# ADR008 — cli_global_flags
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - Manual mode remains dev/test-only
> - Interfaces remain swappable
> - See "Guardrails / invariants" section below

> **File naming (required):** `ADR008_ACCEPTED_cli_global_flags.md`
> Status values: `PROPOSED | ACCEPTED | SUPERSEDED | DEPRECATED`

---

## Metadata
- **ADR:** ADR008
- **Status:** ACCEPTED
- **Date:** 2026-03-12
- **Owners:** Kai
- **Reviewers:** Kai
- **Related backlog item(s):** AF0036, AF0012
- **Related bug(s):** —
- **Related PR(s):** —

---

## Context

The CLI currently supports global flags (`--workspace`, `--json`, `--quiet`, `--verbose`) that can be placed before any subcommand and are inherited by all subcommands. AF0036 proposed evaluating the removal of these global flags to simplify UX and reduce implementation complexity. Additionally, AF0012 needs to add new CLI options, and the decision here affects how those options should be structured.

The key tension:
- **Simplicity:** Removing globals means one pattern to learn (`ag <cmd> --flag`)
- **Convenience:** Global `--workspace` reduces repetition in scripts/sessions
- **Consistency:** Output formatting flags (`--json`, `--verbose`) apply uniformly

---

## Decision

**Adopt a hybrid approach:**

1. **Keep `--workspace` as global only** — it selects context and applies to all commands
2. **Move `--json`, `--quiet`, `--verbose` to command-level** — each command explicitly declares its output options

This mirrors industry patterns like `kubectl -n <namespace> get pods --output=json`.

---

## Options considered

### Option A — Remove all global flags
**Pros**
- Simpler mental model
- No precedence confusion
- Easier implementation (delete CLIContext)
- Better discoverability via `--help`

**Cons**
- More typing for multi-command workflows
- Workspace selection is semantically "global"
- Breaks existing scripts/docs

### Option B — Keep all global flags
**Pros**
- Less typing
- Already implemented and tested
- Matches industry patterns (git, kubectl, docker)

**Cons**
- Precedence rules add complexity
- Harder to discover inherited options
- UX confusion ("did I put `-w` before or after?")

### Option C — Hybrid (selected) ✅
**Pros**
- Workspace is naturally global (context selection)
- Output formatting is local (explicit per command)
- Eliminates most precedence confusion
- Reduces global options to just one

**Cons**
- Still one global flag to explain
- Migration effort for existing code

---

## Consequences

1. **Simplification:** `CLIContext` shrinks to just `workspace`; `_resolve_option()` simplified
2. **CLI_REFERENCE update:** Document that only `--workspace` is global
3. **Code changes:** Commands that use `--json`, `--quiet`, `--verbose` must declare them locally
4. **Testing:** Remove global/local interaction tests for output flags

Follow-up work:
- AF0012 implements new options following this pattern
- Existing commands updated to declare output flags locally

---

## Guardrails / invariants

- `--workspace` remains the only global flag
- All output-formatting flags must be command-local
- No new global flags without an ADR amendment

---

## Implementation notes

1. **main.py changes:**
   - `CLIContext` keeps only `workspace: str | None`
   - Remove `json_output`, `quiet`, `verbose` from global callback
   - Each command adds its own `--json`, `--quiet`, `--verbose` options
   - Delete or simplify `_resolve_option()` helper

2. **CLI_REFERENCE.md:**
   - Update "Global" section to show only `--workspace`
   - Document that `--json`, `--quiet`, `--verbose` are command-level

3. **Migration:** This is a breaking change for scripts using `ag --json <cmd>`. Document the migration path.

---

## Links
- CLI_REFERENCE.md section: Global / Command overview
- AF0036: Remove global CLI flags (this ADR resolves it)
- AF0012: CLI surface parity (implements per this decision)
