# ag_foundation

Modular agent network core runtime.

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
```

### Verify installation

```bash
# CLI should work
ag --help
ag --version

# Tests should pass
pytest -q
```

### Basic usage (stub)

```bash
# Run a task (default LLM mode - not implemented yet)
ag run "Hello world"

# Run in manual mode (dev/test only, requires AG_DEV=1)
$env:AG_DEV = "1"  # PowerShell
ag run --mode manual "Test the pipeline"

# Check diagnostics
ag doctor
```

## Project Structure

```
ag_foundation/
├── src/ag/                 # Main package
│   ├── cli/                # CLI adapter (Typer)
│   ├── core/               # Core runtime modules
│   ├── storage/            # Persistence layer
│   ├── skills/             # Skills/plugins registry
│   └── config.py           # Configuration contract
├── tests/                  # Test suite
├── docs/dev/               # Development documentation
└── pyproject.toml          # Project configuration
```

## Configuration

Config file location: `~/.ag/config.yaml` (or override via `AG_CONFIG_PATH`)

See [src/ag/config.py](src/ag/config.py) for the configuration contract and environment variable overrides.

## Development

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=ag

# Type checking
mypy src/ag

# Linting
ruff check src/ag tests
```

## Documentation

- [Architecture](docs/dev/cornerstone/ARCHITECTURE.md)
- [CLI Reference](docs/dev/cornerstone/CLI_REFERENCE.md)
- [Project Plan](docs/dev/cornerstone/PROJECT_PLAN.md)

## License

MIT
