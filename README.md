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

# Tests should pass (173 tests, 89% coverage)
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
├── src/ag/                 # Main package
│   ├── cli/                # CLI adapter (Typer)
│   ├── core/               # Core runtime modules
│   │   ├── interfaces.py   # Protocols: Normalizer, Planner, etc.
│   │   ├── playbooks.py    # Playbook definitions (echo, delegate_v0)
│   │   ├── run_trace.py    # RunTrace, Step, Subtask models
│   │   └── runtime.py      # V0 runtime implementation
│   ├── providers/          # LLM provider abstraction
│   │   ├── base.py         # LLMProvider Protocol, ChatMessage, errors
│   │   ├── registry.py     # Provider registry
│   │   ├── openai.py       # OpenAI adapter
│   │   └── stubs.py        # Anthropic/Local stubs (fail fast)
│   ├── storage/            # Persistence layer (SQLite + filesystem)
│   ├── skills/             # Skills/plugins registry
│   └── config.py           # Configuration contract
├── tests/                  # Test suite (173 tests)
├── docs/dev/               # Development documentation
└── pyproject.toml          # Project configuration
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

| Name | Steps | Description |
|------|-------|-------------|
| `echo` | 4 | Simple linear flow (normalize→plan→execute→verify) |
| `delegate_v0` | 6 | Multi-step delegation (normalize→plan→execute×2→verify→finalize) |

## Configuration

Config file location: `~/.ag/config.yaml` (or override via `AG_CONFIG_PATH`)

See [src/ag/config.py](src/ag/config.py) for the configuration contract and environment variable overrides.

## Development

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=ag

# Run only unit tests (skip integration)
pytest -m "not integration"

# Run integration tests (requires OPENAI_API_KEY)
pytest -m integration

# Type checking
mypy src/ag

# Linting
ruff check src/ag tests
```

## Documentation

- [Architecture](docs/dev/cornerstone/ARCHITECTURE.md)
- [CLI Reference](docs/dev/cornerstone/CLI_REFERENCE.md)
- [Project Plan](docs/dev/cornerstone/PROJECT_PLAN.md)
- [Sprint Log](docs/dev/sprints/SPRINT_LOG.md)

## Current Status

- **Sprint 02 Complete** (2026-02-26)
  - Provider abstraction + OpenAI adapter
  - Delegation playbook v0 (multi-step)
  - CLI global options
  - 173 tests, 89% coverage

## License

MIT
