# ADR007 — configuration_state_separation
# Version number: v0.2

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

> **File naming (required):** `ADR###_<three_word_description>.md`
> Status values: `Proposed | Accepted | Superseded | Deprecated`

---

## Metadata
- **ADR:** ADR007
- **Status:** Proposed
- **Date:** 2026-03-05
- **Owners:** Kai
- **Reviewers:** Kai, Jeff
- **Related backlog item(s):** (none yet)
- **Related bug(s):** (none)
- **Related PR(s):** (pending)

---

## Context

The CLI needs to persist user preferences that survive across sessions:
- Default workspace (currently implemented)
- Future: default provider, default model, last used run ID, etc.

Currently we have **two** configuration mechanisms:

| File | Purpose | Format | Managed by |
|------|---------|--------|------------|
| `~/.ag/config.yaml` | Static settings | YAML | Manual edit |
| `~/.ag/state.json` | Runtime state | JSON | CLI commands |

**Current state.json:**
```json
{"default_workspace": "dev02"}
```

**config.yaml:** Documented but mostly stubbed — not actively used.

**Problems with current approach:**
1. Two files in same directory may confuse users
2. Unclear which file to edit for what purpose
3. No schema for state.json — ad-hoc keys
4. config.yaml isn't actually implemented
5. Precedence between files is undefined if both contain same setting

As more defaults are needed (provider, model, etc.), we need a clear pattern.

---

## Decision

**Separate concerns into two files with distinct purposes:**

| File | Purpose | Edited by | Contains |
|------|---------|-----------|----------|
| `~/.ag/config.yaml` | User configuration | Manual edit | API keys, paths, provider settings |
| `~/.ag/state.json` | CLI-managed state | CLI commands only | Defaults set via `ag` commands |

**Precedence (highest to lowest):**
1. CLI flags (`--workspace`, `--provider`)
2. Environment variables (`AG_WORKSPACE`, `AG_LLM_PROVIDER`)
3. **state.json** — CLI-set defaults (`ag ws use`, `ag config set`)
4. **config.yaml** — User-edited configuration
5. Built-in defaults

**state.json schema:**
```json
{
  "schema_version": 1,
  "defaults": {
    "workspace": "dev01",
    "provider": "openai",
    "model": "gpt-4o-mini"
  }
}
```

**config.yaml schema:**
```yaml
# ~/.ag/config.yaml
providers:
  openai:
    api_key: "${OPENAI_API_KEY}"  # Can reference env vars
    default_model: "gpt-4o"
  anthropic:
    api_key: "${ANTHROPIC_API_KEY}"

workspaces:
  directory: "~/.ag/workspaces"  # Override storage location
```

---

## Options considered

### Option A — Single config.yaml for everything
Put both user config and CLI-managed state in one YAML file.

**Pros**
- Single source of truth
- Users know where to look

**Cons**
- CLI editing YAML risks corrupting user formatting/comments
- YAML round-tripping is fragile
- Mixing manual and automated edits in one file

### Option B — Separate files (chosen)
Keep `state.json` for CLI-managed state, `config.yaml` for user config.

**Pros**
- CLI can safely modify state.json without touching user's YAML
- Clear ownership: CLI owns state.json, user owns config.yaml
- JSON is easy to round-trip programmatically
- Each file has clear purpose

**Cons**
- Two files to understand
- Need to document precedence clearly

### Option C — SQLite for all state
Store config in the existing SQLite infrastructure.

**Pros**
- Single storage mechanism
- Queryable

**Cons**
- Overkill for simple key-value config
- Not human-readable/editable
- User can't easily inspect or backup config

---

## Consequences

**Easier:**
- CLI commands can safely persist defaults
- Users can edit config.yaml without fear of CLI overwriting
- Clear mental model: "state = CLI-managed, config = user-managed"

**Harder:**
- Must document precedence clearly
- Users need to know which file affects what

**Follow-up work:**
- Add schema version to state.json
- Implement config.yaml loading (currently stubbed)
- Add `ag config` subcommands for viewing/setting defaults
- Document precedence in CLI_REFERENCE.md

---

## Guardrails / invariants

1. **CLI never modifies config.yaml** — Only user edits config.yaml
2. **state.json is machine-managed** — Users can read but shouldn't edit
3. **Env vars always override files** — For CI/scripting flexibility
4. **Schema versioning** — state.json includes version for migrations
5. **Graceful degradation** — Missing files use defaults, no errors

---

## Implementation notes

### state.json management
```python
def _load_state() -> dict:
    """Load state, handling missing file and schema migration."""
    state_file = _get_state_file()
    if not state_file.exists():
        return {"schema_version": 1, "defaults": {}}
    
    state = json.loads(state_file.read_text())
    # Future: migrate if schema_version < CURRENT_VERSION
    return state

def get_default(key: str) -> str | None:
    """Get a CLI-managed default."""
    state = _load_state()
    return state.get("defaults", {}).get(key)

def set_default(key: str, value: str) -> None:
    """Set a CLI-managed default."""
    state = _load_state()
    state.setdefault("defaults", {})[key] = value
    _save_state(state)
```

### CLI commands
```bash
ag ws use dev01        # Sets defaults.workspace
ag config set provider openai  # Sets defaults.provider
ag config get provider  # Reads effective value (with precedence)
ag config list          # Shows all effective config with sources
```

---

## Links
- CLI_REFERENCE.md section: Configuration (to be updated)
- ARCHITECTURE.md section: Configuration (to be added)
- Related: ADR004 (Storage baseline) — workspace storage patterns
