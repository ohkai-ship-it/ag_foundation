# BACKLOG ITEM — AF0085 — cli_consistency_audit
# Version number: v0.1

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CLI surface parity with reference

> **File naming (required):** `AF####_<STATUS>_<three_word_description>.md`
> Status values: `PROPOSED | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED`

---

## Metadata
- **ID:** AF0085
- **Type:** Architecture / CLI
- **Status:** PROPOSED
- **Priority:** P1
- **Area:** CLI
- **Owner:** TBD
- **Target sprint:** TBD
- **Depends on:** None

---

## Problem

The CLI has grown organically and now exhibits several consistency issues that affect usability and predictability.

### Observed Issues

#### 1. Verb Inconsistency: `show` vs `list` vs `info`

Commands use different verbs for similar operations:

| Command | Current | Expected Pattern |
|---------|---------|------------------|
| `ag skills list` | ✓ list | OK |
| `ag playbooks list` | ✓ list | OK |
| `ag runs list` | ✓ list | OK |
| `ag runs show <id>` | show | OK (single item) |
| `ag workspaces list` | ✓ list | OK |
| `ag config list` | ❓ | Not implemented |

**Proposed Convention:**
- `list` — Multiple items (collection)
- `show` — Single item by ID
- `info` — System/global information (no ID)

#### 2. Output Formatting Inconsistency

`ag skills list` and `ag playbooks list` produce differently formatted output:

```bash
# ag skills list
echo_tool
emit_result
fetch_web_content
...

# ag playbooks list  
default_v0 (1.0.0)
delegate_v0 (1.0.0)
research_v0 (1.1.0)
...
```

**Issues:**
- Skills: name only
- Playbooks: name + version in parentheses
- No alignment, no table format option
- No `--format json|table|plain` flag

#### 3. `ag runs list` Incomplete/Truncated

The `runs list` command doesn't show all runs. Unclear if:
- Pagination missing?
- Default limit too low?
- Filter applied implicitly?

**Expected:** 
- Show all runs or clear pagination
- `--limit N` flag documented
- `--all` flag to override default limit

#### 4. `ag config` Not Implemented

`ag config list` and related subcommands are referenced but not functional.

**Expected:**
- `ag config list` — Show current configuration
- `ag config get <key>` — Get specific value
- `ag config set <key> <value>` — Set value
- `ag config path` — Show config file location

#### 5. Workspace Precedence Inconsistency

Critical issue for isolation and information leak prevention.

**Current State (Inconsistent):**

| Command | Workspace Required | Behavior |
|---------|-------------------|----------|
| `ag run` | Implicit (default) | Uses persisted default |
| `ag runs list` | ❓ | Which workspace? |
| `ag artifacts list` | `--run` required | Needs run ID |
| `ag workspaces list` | N/A | Global |
| `ag skills list` | N/A | Global registry |

**Problem:**
- Some commands silently use default workspace
- Others require explicit `--workspace`
- Information can leak across workspaces if user forgets flag

**Proposed Workspace Declaration Policy:**

| Category | Workspace Handling |
|----------|-------------------|
| **Global commands** | No workspace needed: `skills list`, `playbooks list`, `config *` |
| **Workspace-scoped** | MUST specify OR use explicit default: `runs list`, `artifacts list` |
| **Run commands** | Inherit from persisted default OR explicit `--workspace` |

**Key Decision Needed:**
- Should `ag runs list` require `--workspace` or use default?
- Should we warn when using implicit default?

---

## Goal

Define a **CLI consistency standard** that ensures:

1. **Predictable verbs** — `list`, `show`, `info` used consistently
2. **Uniform output** — Same formatting across similar commands
3. **Complete data** — No silent truncation without pagination
4. **Working config** — `ag config *` commands functional
5. **Clear workspace scope** — Explicit policy on when workspace is required

---

## Non-goals (for this AF)

- Implementation of fixes (child AFs)
- New CLI commands
- Breaking changes to existing flags

---

## Proposed Standards

### Verb Convention

| Verb | Use Case | Example |
|------|----------|---------|
| `list` | Multiple items | `ag runs list`, `ag skills list` |
| `show` | Single item by ID | `ag runs show <id>` |
| `get` | Single config/setting | `ag config get <key>` |
| `set` | Modify config/setting | `ag config set <key> <value>` |
| `create` | Create new resource | `ag workspaces create <name>` |
| `delete` | Remove resource | `ag workspaces delete <name>` |

### Output Format Standard

All `list` commands should support:
```bash
--format plain   # Default: one item per line
--format table   # Aligned columns with headers
--format json    # Machine-readable
```

Example table format:
```
NAME                VERSION   DESCRIPTION
─────────────────────────────────────────────
research_v0         1.1.0     Web research pipeline
summarize_v0        1.0.0     Document summarization
```

### Pagination Standard

All `list` commands should:
- Show count: `Showing 10 of 47 runs`
- Support `--limit N` (default: 20)
- Support `--all` to show everything
- Support `--offset N` for pagination

### Workspace Scope Policy

| Scope | Commands | Workspace Handling |
|-------|----------|-------------------|
| **Global** | `skills *`, `playbooks *`, `config *`, `version` | Never requires workspace |
| **Workspace** | `runs *`, `artifacts *` | Requires `--workspace` OR uses default with notice |
| **Run** | `run` | Uses default, `--workspace` optional |

**Notice when using default:**
```
Using workspace 'skills01' (set via AG_WORKSPACE)
To use a different workspace: --workspace <name>
```

---

## Acceptance Criteria (High-Level)

- [ ] CLI consistency standards documented
- [ ] Verb convention finalized
- [ ] Output format standard defined
- [ ] Workspace scope policy decided
- [ ] Implementation roadmap created (child AFs)

---

## Implementation Roadmap (Child AFs)

1. **AF-TBD: CLI output formatting** — Implement `--format` flag across commands
2. **AF-TBD: CLI pagination** — Add `--limit`, `--all`, `--offset` to list commands
3. **AF-TBD: Config commands** — Implement `ag config *` subcommands
4. **AF-TBD: Workspace scope enforcement** — Consistent workspace handling
5. **AF-TBD: CLI reference sync** — Update CLI_REFERENCE.md to match implementation

---

## Related Items

| Item | Relationship |
|------|--------------|
| **CLI_REFERENCE.md** | Specification document |
| **BUG-0002** | Missing ag run options |
| **BUG-0003** | Missing CLI subcommands |
| **BUG-0011** | Default workspace name leaked |
| **AF-0012** | CLI reference surface parity |
| **AF-0036** | Remove global CLI flags |

---

## Open Questions

1. Should we adopt a CLI framework (e.g., rich-click) for consistent formatting?
2. Is `--workspace` required for `runs list` or should default be OK?
3. Should `--format json` be the default for scripting scenarios?
4. How do we handle backward compatibility for output format changes?

---

# Completion section (fill when done)

## 1) Metadata
- **Backlog item (primary):** AF0085
- **PR:** N/A (strategy document)
- **Author:** <name>
- **Date:** YYYY-MM-DD
- **Branch:** N/A
- **Risk level:** P1
- **Runtime mode used for verification:** N/A (design document)
