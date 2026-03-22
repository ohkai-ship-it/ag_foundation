# ag_foundation — CLI Reference
# Version number: v0.4

This document defines the **CLI contract** for ag_foundation. The CLI is the primary interface in early iterations, but the core runtime is interface-agnostic and will later be callable via an internal API.

## Principles
- **Default runtime is LLM-first** (end-user behavior).
- **Manual mode is dev/test-only** (LLMs disabled). It exists for fast debugging and CI-style checks and must not become an end-user feature.
- **Truthful UX:** anything printed as a label (e.g., "verified", "used retrieval") must be derived from the persisted **RunTrace**.
- **Explicit workspace selection** (AF-0026): Workspaces must be explicitly selected; no implicit creation during runs.

---

## Command overview

### Global
- `--workspace <id>`: select workspace (required for run; see workspace selection policy)

> **Note (ADR008):** Only `--workspace` is a global flag. Output formatting options (`--json`, `--quiet`, `--verbose`) are command-level and must be specified after the subcommand.

### Command-level output options
The following options are available on most commands (specified after the subcommand):
- `--json`: emit machine-readable JSON (where supported)
- `--quiet`: reduce non-essential output
- `--verbose`: include trace pointers, timing, and debug details

### Workspace Selection Policy (AF-0026)

**Runs require an explicit workspace.** Implicit workspace creation is not allowed.

Precedence order:
1. `--workspace <id>` flag (highest priority)
2. `AG_WORKSPACE` environment variable
3. **Error** if neither is specified

When no workspace is selected, `ag run` fails with:
```
Error: No workspace specified.

Specify a workspace using one of:
  1. --workspace <name> flag
  2. AG_WORKSPACE environment variable

To create a workspace: ag ws create <name>
To list workspaces:    ag ws list
```

### Mode (runtime)
- **Default:** `llm`
- **Dev/test only:** `manual` (requires explicit dev gate; see below)

> Dev gate options (pick one and enforce consistently in code):
> - Environment gate: `AG_DEV=1` required for `--mode manual`
> - Or build-time/packaging: manual mode only available in dev installs

---

## `ag run` — execute a task

### Synopsis
- `ag run "<prompt>"`
- `ag run --plan <plan_id>` (execute pre-approved plan)
- `ag run --playbook <name>` (override playbook selection)
- `ag run --reasoning <mode>` (override default reasoning policy; applies to playbook unless overridden per role)
- `ag run --allow-web` (planned; default false)

> **Deferred options (not yet implemented):**
> - `--file <path>` — treat file as input prompt/content
> - `--task <task.json>` — explicit TaskSpec payload (dev-oriented)
> - `--confirm` / `--no-confirm` — confirmation behavior (safety hook)

### Plan execution mode (AF-0099)
When `--plan <plan_id>` is specified:
- The plan must exist and not be expired
- Steps execute in order as defined in the plan
- Trace records `plan_id` for audit
- `--plan` and `"<prompt>"` are mutually exclusive

### Output contract
On success:
- prints a **human-readable** summary
- prints the `run_id`
- prints a pointer to:
  - `RunTrace` (`ag runs show <run_id>`)
  - artifacts (`ag artifacts list --run <run_id>`)

On failure:
- prints failure summary + next action hint
- still prints `run_id` and trace pointer

### Truthful labels (examples)
The CLI may print labels like:
- `mode: llm`
- `verified: pass`
- `retrieval: used|not_used`
- `repairs: 0|1|...`

These values must come from the persisted RunTrace fields.

### Examples
- `ag run "Draft a sprint plan for Sprint 03"`
- `ag run --playbook balanced_default "Summarize these notes into bullets"`
- `ag run --reasoning deep "Critique this proposal and suggest fixes"`
- `ag run --plan plan_abc123 --workspace demo` (execute pre-approved plan)

---

## `ag plan` — execution plan management (AF-0098, AF-0099)

### Synopsis
- `ag plan generate --task "<prompt>" [--workspace <id>]`
- `ag plan show <plan_id> [--workspace <id>]`
- `ag plan list [--workspace <id>]`
- `ag plan delete <plan_id> [--workspace <id>]`

### Description
The plan commands support a **guided autonomy** workflow where:
1. User requests a plan for a task
2. LLM planner composes skill sequence
3. User reviews and approves/rejects
4. If approved, execute with `ag run --plan <plan_id>`

### Commands

#### `ag plan generate`
Generate an execution plan without executing it.

Options:
- `--task <prompt>`: Task description (required)
- `--workspace <id>`: Target workspace (uses default if not specified)

Output:
- Plan ID for later reference
- Proposed skill sequence with estimated tokens
- Policy flags (external_api, llm_call, file_write)
- Expiration time (default: 1 hour)

#### `ag plan show <plan_id>`
Display details of a saved plan.

#### `ag plan list`
List pending (non-expired) plans in a workspace.

#### `ag plan delete <plan_id>`
Remove a plan without executing it.

### V1Planner (AF-0102)
The V1Planner uses an LLM to compose skill sequences:
- Reads available skills from registry
- Generates JSON execution plan
- Validates skill references
- Estimates token usage
- Returns confidence score

### Examples
```bash
# Generate plan for research task
ag plan generate --task "Research Berlin weather" -w demo

# Review the plan
ag plan show plan_abc123 -w demo

# Execute if satisfied
ag run --plan plan_abc123 -w demo

# Or discard
ag plan delete plan_abc123 -w demo
```

---

## `ag ws` — workspace operations

### Synopsis
- `ag ws list`
- `ag ws create <name>`
- `ag ws use <id>`
- `ag ws show [<id>]`
- `ag ws config get <key>`
- `ag ws config set <key> <value>`

### Notes
Workspaces isolate:
- runs and traces
- artifacts
- memory/retrieval stores (optional)
- defaults (budgets, playbooks, tool allowlists)

**Important:** Workspaces must be created explicitly with `ag ws create` before use. `ag run` will not auto-create workspaces (AF-0026).

### Directory structure (AF0058)
```
<workspace>/
├── db.sqlite      # Index database
├── inputs/        # User content (place files here for skills to read)
└── runs/          # Run outputs
    └── <run_id>/
        ├── trace.json
        └── artifacts/
```

---

## `ag runs` — run inspection

### Synopsis
- `ag runs list [--limit N] [--status success|failure]`
- `ag runs show <run_id>` (human)
- `ag runs show <run_id> --json` (machine)
- `ag runs trace <run_id>` (alias for show, emphasizes trace output)
- `ag runs tail <run_id>` (planned: stream events while running)

### Required fields to display (human view)
- run_id, workspace_id
- mode (llm/manual)
- interface (cli/api/event)
- playbook name + version
- planning metadata: planner name, LLM tokens (input/output), duration, confidence (AF-0119)
- pipeline manifest: component versions used (planner, orchestrator, executor, verifier, recorder) (AF-0120)
- timestamps + duration
- final status + verifier status
- artifacts count + retrieval usage indicator
- top-level summary

### JSON output (`--json`)
The `--json` flag returns the full `RunTrace` schema, which includes:
- `planning`: planner name, duration_ms, llm_call (model, input_tokens, output_tokens, total_tokens), confidence
- `pipeline`: planner, orchestrator, executor, verifier, recorder class names
- `steps[]`: full step array with per-step verification, LLM attribution, input/output data
- All other RunTrace fields (see `run_trace.py`)

---

## `ag artifacts` — artifact registry

### Synopsis
- `ag artifacts list [--run <run_id>]`
- `ag artifacts show <artifact_id>`
- `ag artifacts open <artifact_id>` (platform-dependent; optional)
- `ag artifacts export <artifact_id> --to <path>` (copies file)

### Contract
Artifacts are referenced by:
- stable `artifact_id`
- `type` (markdown/json/csv/pdf/...)
- `uri` (e.g., `artifact://...`)
- `created_by_step`

---

## `ag skills` — skills/plugins

### Synopsis
- `ag skills list`
- `ag skills info <skill_name>`
- `ag skills test <skill_name>` (dev)
- `ag skills enable <skill_name>` / `disable <skill_name>` (workspace-scoped)

### Contract
A skill declares:
- version
- input/output schema
- required permissions
- tool dependencies

---

## `ag playbooks` — orchestration recipes

### Synopsis
- `ag playbooks list`
- `ag playbooks show <name>`
- `ag playbooks validate <path>` (dev)
- `ag playbooks set-default <name>` (workspace-scoped)

### Notes
Playbooks define:
- roles/agents
- step graph
- reasoning modes (per role/step)
- budgets and failure policies
- evidence/verification requirements

---

## `ag config` — global configuration (optional)

### Synopsis
- `ag config get <key>`
- `ag config set <key> <value>`
- `ag config list`

### Examples of keys (initial)
- `default_workspace`
- `default_playbook`
- `telemetry.enabled`
- `telemetry.export` (none|otel|langfuse)

---

## `ag doctor` — diagnostics (dev-focused)
Helps validate environment and detect common misconfigurations.

### Synopsis
- `ag doctor`
- `ag doctor --json`

### Checks (examples)
- workspace paths writable
- storage reachable (sqlite/file system)
- LLM provider configuration present (only in llm mode)
- telemetry export configured (if enabled)

---

## Manual mode (dev/test-only)

### Command usage
- `ag run --mode manual "<prompt>"`

### Restrictions
- Must require an explicit dev gate (e.g., `AG_DEV=1`)
- Must print a prominent banner:
  - `DEV MODE: manual (LLMs disabled)`
- Must still produce a RunTrace (so behavior is inspectable)

---

## API parity (planned)
The CLI commands map 1:1 to an internal API surface later:
- `ag run` ↔ `POST /tasks`
- `ag runs show` ↔ `GET /runs/{run_id}`
- `ag runs trace` ↔ `GET /runs/{run_id}/trace`
- `ag artifacts list` ↔ `GET /runs/{run_id}/artifacts`

This is a design constraint: CLI must not embed logic that cannot be exposed via the API adapter later.

---

## Exit criteria for “CLI v0”
The CLI is “v0 complete” when:
- `ag run` produces a valid RunTrace and at least one artifact or user-visible output reference
- `ag runs show --json` returns a stable machine-readable structure
- labels shown to the user match the trace (truthful UX)
