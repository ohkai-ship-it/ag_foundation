# ag_foundation

Modular agent network core runtime with LLM provider abstraction and multi-step delegation.

## Quick Start

### Installation (development)

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Activate (Unix/macOS)
source .venv/bin/activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Optional: Install LLM provider support (OpenAI)
pip install -e ".[llm]"
```

### Verify installation

```bash
# CLI should work
ag --help
ag --version

# Tests should pass (794 tests, 86% coverage)
pytest -q
```

### Basic usage

```bash
# Global options available on all commands
ag --help  # Shows --workspace, --json, --quiet, --verbose

# Run a task (LLM mode requires OPENAI_API_KEY)
ag run "Summarize this project"

# Run with JSON output
ag --json run "Hello world"

# Run in manual mode (dev/test only, requires AG_DEV=1)
$env:AG_DEV = "1"  # PowerShell
ag run --mode manual "Test the pipeline"

# Specify workspace
ag --workspace ./my_project run "Analyze code"

# Check diagnostics
ag doctor
```

## Project Structure

```
ag_foundation/
├── src/ag/                     # Main package
│   ├── cli/                    # CLI adapter (Typer)
│   │   └── main.py
│   ├── core/                   # Core runtime (modular pipeline)
│   │   ├── interfaces.py       # Protocols: Normalizer, Planner, Orchestrator, etc.
│   │   ├── task_spec.py        # TaskSpec schema
│   │   ├── planner.py          # V0–V3 Planner implementations
│   │   ├── orchestrator.py     # V0/V1 Orchestrator
│   │   ├── executor.py         # V0–V2 Executor
│   │   ├── verifier.py         # V0–V2 Verifier
│   │   ├── recorder.py         # V0/V1 Recorder
│   │   ├── runtime.py          # Composition root (wiring)
│   │   ├── run_trace.py        # RunTrace, Step, VerifierStatus models
│   │   ├── playbook.py         # Playbook, PlaybookStep
│   │   ├── execution_plan.py   # ExecutionPlan
│   │   └── schema_verifier.py  # SchemaValidator (repair loop)
│   ├── providers/              # LLM provider abstraction
│   │   ├── base.py             # LLMProvider Protocol, ChatMessage, errors
│   │   ├── registry.py         # Provider registry
│   │   ├── openai.py           # OpenAI adapter
│   │   └── stubs.py            # Anthropic/Local stubs (fail fast)
│   ├── skills/                 # Skills/plugins registry
│   │   ├── base.py             # Skill ABC
│   │   ├── registry.py         # Skill registry
│   │   ├── load_documents.py   # File I/O skill
│   │   ├── web_search.py       # Web search skill
│   │   ├── fetch_web_content.py # HTTP fetch skill
│   │   ├── synthesize_research.py # LLM synthesis skill
│   │   ├── emit_result.py      # Result emission skill
│   │   └── zero_skill.py       # No-op skill (testing)
│   ├── storage/                # Persistence layer
│   │   ├── interfaces.py       # RunStore, ArtifactStore protocols
│   │   ├── sqlite_store.py     # SQLite implementation
│   │   ├── plan_store.py       # Plan persistence
│   │   └── workspace.py        # Workspace management
│   └── config.py               # Configuration contract
├── tests/                      # Test suite (794 tests)
├── docs/dev/                   # Development documentation
└── pyproject.toml              # Project configuration
```

## LLM Providers

ag_foundation uses a provider abstraction for LLM calls. Currently supported:

| Provider | Status | Notes |
|----------|--------|-------|
| OpenAI | ✅ Ready | Set `OPENAI_API_KEY` env var |
| Anthropic | 🚧 Stub | Fails fast with structured error |
| Local | 🚧 Stub | Fails fast with structured error |

### OpenAI Setup

```bash
# Set API key (session only)
$env:OPENAI_API_KEY = "sk-your-key-here"  # PowerShell
export OPENAI_API_KEY="sk-your-key-here"  # Unix

# Verify
python -c "from ag.providers import get_provider; print(get_provider('openai'))"
```

## Playbooks

Playbooks define execution flow. Available playbooks:

| Name | Skills Used | Description |
|------|-------------|-------------|
| `summarize_v0` | load_documents, summarize_docs | Summarize documents from workspace |
| `research_v0` | web_search, fetch_web_content, synthesize_research | Research pipeline: discover, fetch, synthesize |
| `default_v0` | (echo-style) | Testing playbook execution |
| `delegate_v0` | (echo-style) | Testing multi-step delegation |

## Configuration

Config file location: `~/.ag/config.yaml` (or override via `AG_CONFIG_PATH`)

See [src/ag/config.py](src/ag/config.py) for the configuration contract and environment variable overrides.

## Development

```bash
# Run tests
pytest -W error

# Run tests with coverage
pytest --cov=src/ag --cov-report=term-missing

# Linting
ruff check src tests

# Format check
ruff format --check src tests
```

## Documentation

- [Architecture](ARCHITECTURE.md)
- [CLI Reference](CLI_REFERENCE.md)
- [Foundation Manual](docs/dev/foundation/FOUNDATION_MANUAL.md)
- [Sprint Manual](docs/dev/foundation/SPRINT_MANUAL.md)
- [Folder Structure](docs/dev/foundation/FOLDER_STRUCTURE_0.3.md)

## Governance

ag_foundation uses the **Governance System (GVS)** framework for sprint-based development.

- **Governance rules:** `convergent/gvs_version_fixed/version1.3/`
- **Governance development:** `convergent/gvs_development/`
- **Extraction plan:** [GVS Project Plan](docs/dev/additional/GVS_PROJECT_PLAN_0.1.md)

The governance system was extracted from this project after Sprint 16 into a standalone project.
Historical governance docs remain in `docs/dev/` for reference.

## Current Status

- **Sprint 17 — gvs_migration** (2026-04-05)
  - GVS extraction to standalone project
  - Governance System Version v1.3
  - Modular pipeline: V0–V3 Planner, V0/V1 Orchestrator, V0–V2 Executor/Verifier, V0/V1 Recorder
  - 7 skills, 4 playbooks
  - HITL framework (15 gates)
  - 794 tests, 86% coverage

## License

MIT
