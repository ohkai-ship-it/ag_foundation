# Continuation Prompt — Jacob (Implementer) — ag_foundation — Sprint 02 → 03 Transition

**Role:** Implementer ("Jacob")  
**Goal:** Complete Sprint 02 review + extensive testing, then start Sprint 03 implementation.

---

## 1) Project snapshot

- **Project:** ag_foundation  
- **Prior sprint:** Sprint 02 — Agent network v0 + LLM provider adapter (OpenAI first)  
- **Current sprint:** Sprint 03 — (to be planned after Sprint 02 wrap-up)  
- **Runtime stance:** LLM-first end-user behavior; manual mode dev/test-only  
- **Test stats at handoff:** 173 passed, 1 deselected (integration), 89% coverage  
- **CLI coverage:** 72% (was 64%)

---

## 2) Sprint 02 summary — what was completed

All Sprint 02 items were implemented with tests:

| AF ID | Title | Tests Added | Files Created/Modified |
|-------|-------|-------------|----------------------|
| AF-0014 | Recorder Protocol audit | docs | CONTRACT_INVENTORY.md (Protocol count 5→6) |
| AF-0016 | ReasoningMode + Artifact semantics fix | docs | CONTRACT_INVENTORY.md (BALANCED→DIRECT) |
| AF-0018 | Provider interface + registry + stubs | 34 tests | `src/ag/providers/` module (base, registry, stubs, openai) |
| AF-0017 | OpenAI adapter with mocked tests | (in above) | `src/ag/providers/openai.py` |
| AF-0019 | Delegation playbook v0 | 23 tests | playbooks.py, run_trace.py, runtime.py, registry.py |
| AF-0011 | CLI global options | 13 tests | cli/main.py |

**New modules created:**
- `src/ag/providers/__init__.py` — Package exports
- `src/ag/providers/base.py` — LLMProvider Protocol, ProviderConfig, ChatMessage, ChatResponse, ProviderError
- `src/ag/providers/registry.py` — PROVIDER_REGISTRY, get_provider(), register_provider(), list_providers()
- `src/ag/providers/stubs.py` — AnthropicStubProvider, LocalStubProvider (fail fast)
- `src/ag/providers/openai.py` — OpenAIProvider with chat(), validate_config()
- `tests/test_providers.py` — 34 tests
- `tests/test_delegation.py` — 23 tests
- `tests/test_cli_global_options.py` — 13 tests

**Core modifications:**
- `src/ag/core/playbooks.py` — Added `DELEGATE_V0` playbook (6 steps)
- `src/ag/core/run_trace.py` — Added `Subtask` model, `StepType.PLANNING`
- `src/ag/core/runtime.py` — Subtask tracking in orchestrator
- `src/ag/skills/registry.py` — 5 delegation skills
- `src/ag/cli/main.py` — Global options via `@app.callback()`, `CLIContext`, precedence logic

---

## 3) Non-negotiable rules (still apply)

1. **One PR = one primary backlog item (AF-000x).**  
2. **Truthful UX:** any CLI label must be provable from `RunTrace`.  
3. **No business logic in adapters:** CLI just calls the core pipeline.  
4. **Workspace isolation is strict:** never read/write outside active workspace.  
5. **Manual mode is dev/test-only:** gated by `AG_DEV=1` env var.

---

## 4) IMMEDIATE TASK — Sprint 02 extensive testing

Before starting Sprint 03, you MUST complete comprehensive testing of Sprint 02 features. This has two phases: automated testing (no human needed) and interactive testing (with human support).

### Phase A: Automated testing (no human support needed)

Run these tests and capture all output. Fix any failures before proceeding.

#### A1. Full test suite
```powershell
pytest tests/ -v --tb=short 2>&1 | Tee-Object -FilePath sprint02_test_full.txt
```

#### A2. Coverage report
```powershell
pytest --cov=ag --cov-report=term-missing --cov-report=html 2>&1 | Tee-Object -FilePath sprint02_coverage.txt
```

#### A3. Provider module isolation tests
```powershell
pytest tests/test_providers.py -v --tb=long 2>&1 | Tee-Object -FilePath sprint02_providers.txt
```

#### A4. Delegation playbook tests
```powershell
pytest tests/test_delegation.py -v --tb=long 2>&1 | Tee-Object -FilePath sprint02_delegation.txt
```

#### A5. CLI global options tests
```powershell
pytest tests/test_cli_global_options.py -v --tb=long 2>&1 | Tee-Object -FilePath sprint02_cli_global.txt
```

#### A6. Schema validation tests
```powershell
pytest tests/test_schemas.py tests/test_run_trace.py -v --tb=long 2>&1 | Tee-Object -FilePath sprint02_schemas.txt
```

#### A7. Integration test (if API key available)
```powershell
# Only if OPENAI_API_KEY is set:
pytest tests/test_providers.py -v -m integration --tb=long 2>&1 | Tee-Object -FilePath sprint02_integration.txt
```

#### A8. Edge case and error path exploration
Run Python REPL tests for provider edge cases:
```python
# In Python REPL (pytest not needed)
from ag.providers.base import ProviderConfig, ChatMessage, ProviderError, ProviderNotFoundError
from ag.providers.registry import get_provider, list_providers, register_provider
from ag.providers.stubs import AnthropicStubProvider, LocalStubProvider

# Test 1: List available providers
print("Available providers:", list_providers())

# Test 2: Get OpenAI provider (should work)
try:
    p = get_provider("openai")
    print("OpenAI provider type:", type(p).__name__)
except Exception as e:
    print("OpenAI get error:", e)

# Test 3: Anthropic stub should fail fast with structured error
try:
    stub = AnthropicStubProvider()
    stub.chat([ChatMessage(role="user", content="test")])
except ProviderError as e:
    print("Anthropic stub error (expected):", e)

# Test 4: Local stub should fail fast
try:
    local = LocalStubProvider()
    local.chat([ChatMessage(role="user", content="test")])
except ProviderError as e:
    print("Local stub error (expected):", e)

# Test 5: Unknown provider should raise ProviderNotFoundError
try:
    get_provider("unknown_provider")
except ProviderNotFoundError as e:
    print("Unknown provider error (expected):", e)

# Test 6: ChatMessage validation
try:
    bad_msg = ChatMessage(role="invalid_role", content="test")
except Exception as e:
    print("Bad role error (expected):", e)

# Test 7: ProviderConfig validation
cfg = ProviderConfig(provider="openai", api_key="test-key", model="gpt-4")
print("Config provider:", cfg.provider, "model:", cfg.model)
```

#### A9. Delegation playbook REPL tests
```python
from ag.core.playbooks import get_playbook, list_playbooks
from ag.core.run_trace import Subtask, StepType

# Test 1: List all playbooks
print("Playbooks:", list_playbooks())

# Test 2: Get delegate_v0 playbook
pb = get_playbook("delegate_v0")
print("Delegate playbook steps:", [s.name for s in pb.steps])
print("Step count:", len(pb.steps))

# Test 3: Subtask model
st = Subtask(subtask_id="sub-001", description="Test subtask", status="pending")
print("Subtask:", st.subtask_id, st.status)
st.status = "completed"
st.result_summary = "Done"
print("Updated subtask:", st.status, st.result_summary)

# Test 4: StepType.PLANNING exists
print("StepType.PLANNING:", StepType.PLANNING)
print("All step types:", [s.value for s in StepType])
```

#### A10. CLI global options REPL tests
```python
from typer.testing import CliRunner
from ag.cli.main import app

runner = CliRunner()

# Test 1: --help shows global options
result = runner.invoke(app, ["--help"])
print("Global --help exit code:", result.exit_code)
assert "--workspace" in result.stdout
assert "--json" in result.stdout
assert "--quiet" in result.stdout
assert "--verbose" in result.stdout
print("Global options present in --help: OK")

# Test 2: run --help shows inherited options
result = runner.invoke(app, ["run", "--help"])
print("run --help exit code:", result.exit_code)
print("'workspace' in run help:", "--workspace" in result.stdout or "-w" in result.stdout)

# Test 3: --json mode on run
import os
os.environ["AG_DEV"] = "1"
result = runner.invoke(app, ["--json", "run", "test prompt"])
print("--json run exit code:", result.exit_code)
import json
try:
    data = json.loads(result.stdout)
    print("JSON parse OK, has run_id:", "run_id" in data)
except:
    print("JSON parse failed, stdout:", result.stdout[:200])
```

### Phase B: Interactive testing (WITH human support)

These tests require human judgment or real API access. Ask the human to help.

#### B1. Real OpenAI API test (requires OPENAI_API_KEY)
Ask human:
> "Do you have an OPENAI_API_KEY available? If yes, please set it and I'll run the integration test."

If yes, run:
```powershell
$env:OPENAI_API_KEY = "<provided by human>"
pytest tests/test_providers.py -v -m integration --tb=long
```

Capture the actual API response and verify:
- Model name in response matches request
- Usage tokens are reported
- Response content is non-empty

#### B2. End-to-end delegation run
```powershell
$env:AG_DEV = "1"
ag run "Summarize the architecture of this project" --json
```

Human verification:
- Run completes without error
- RunTrace has ≥5 steps (normalize, plan, execute×2, verify, finalize)
- Each step has timing and result

#### B3. CLI workspace isolation test
```powershell
# Create temp workspace
mkdir C:\temp\test_ws_sprint02
$env:AG_DEV = "1"
ag --workspace C:\temp\test_ws_sprint02 run "test workspace" --json
```

Human verification:
- Files created ONLY in C:\temp\test_ws_sprint02
- No files created in current directory
- DB file exists in workspace

#### B4. Global options precedence test
```powershell
$env:AG_DEV = "1"
# Test: CLI --workspace overrides default
ag --workspace C:\temp\ws_a run "test a" --json
ag --workspace C:\temp\ws_b run "test b" --json
```

Human verification:
- Two separate workspaces created
- Runs are isolated to their workspaces

#### B5. Provider stub behavior (manual verification)
```powershell
$env:AG_DEV = "1"
# Try to use anthropic provider (should fail with structured error)
# This requires modifying config or using direct Python call
python -c "from ag.providers.stubs import AnthropicStubProvider; AnthropicStubProvider().chat([])"
```

Human verification:
- Error message is clear and actionable
- Error includes provider name and reason

#### B6. Quiet and verbose mode test
```powershell
$env:AG_DEV = "1"
ag --quiet run "quiet test"
ag --verbose run "verbose test"
```

Human verification:
- Quiet mode: minimal output (just run_id or essential info)
- Verbose mode: detailed step-by-step output

#### B7. Review evidence collection
After all tests pass, create review evidence folder:
```powershell
mkdir docs\dev\reviews\entries\REVIEW_S02_2026-02-26
# Copy test outputs
Copy-Item sprint02_*.txt docs\dev\reviews\entries\REVIEW_S02_2026-02-26\
```

---

## 5) Sprint 02 Definition of Done checklist

Verify all these before moving to Sprint 03:

- [ ] At least one "delegation" run produces a RunTrace with ≥5 steps
- [ ] OpenAI provider can be used via config/env vars (mocked tests pass)
- [ ] Manual mode remains dev/test-only (`AG_DEV=1` gate)
- [ ] Tests added for provider abstraction (34 tests)
- [ ] Tests added for delegation playbook (23 tests)
- [ ] Tests added for CLI global options (13 tests)
- [ ] Coverage ≥ 85% overall (currently 89% ✓)
- [ ] CLI coverage improved (64% → 72% ✓)
- [ ] Review evidence folder created with test outputs

---

## 6) Sprint 03 backlog candidates

After Sprint 02 wrap-up, these items are ready for Sprint 03:

| ID | Priority | Title | Notes |
|----|----------|-------|-------|
| AF-0012 | P2 | CLI surface parity + config tests | Large; may split into PRs |
| AF-0013 | P1 | Contract inventory hardening | Lightweight; prevents drift |
| AF-0015 | P2 | DB filename mismatch | Small; pure naming |

**Potential new items for Sprint 03:**
- Provider config from file (build on AF-0017/0018)
- Multi-agent orchestration v0.1 (build on AF-0019)
- Real LLM integration testing framework

---

## 7) Where to look (docs as system-of-record)

### Cornerstone docs
1. `/docs/dev/cornerstone/PROJECT_PLAN.md`
2. `/docs/dev/cornerstone/ARCHITECTURE.md`
3. `/docs/dev/cornerstone/CLI_REFERENCE.md`
4. `/docs/dev/cornerstone/REVIEW_GUIDE.md`

### How we work
- Backlog ↔ PR workflow: `/docs/dev/backlog/WORKFLOW.md`
- Sprint process: `/docs/dev/sprints/PLAYBOOK.md` or `/docs/dev/sprints/PROCESS.md`
- Engineering rules: `/docs/dev/engineering/`
- Contract inventory: `/docs/dev/reviews/entries/REVIEW_S01_2026-02-24/CONTRACT_INVENTORY.md`
- Test inventory: `/docs/dev/reviews/entries/REVIEW_S01_2026-02-24/TEST_INVENTORY.md`

---

## 8) Key code locations (Sprint 02 artifacts)

### Provider module
- `src/ag/providers/__init__.py` — exports
- `src/ag/providers/base.py` — Protocol + models + errors
- `src/ag/providers/registry.py` — registry pattern
- `src/ag/providers/stubs.py` — Anthropic/Local stubs
- `src/ag/providers/openai.py` — OpenAI implementation
- `tests/test_providers.py` — 34 tests

### Delegation playbook
- `src/ag/core/playbooks.py` — `DELEGATE_V0` (6 steps)
- `src/ag/core/run_trace.py` — `Subtask` model, `StepType.PLANNING`
- `src/ag/core/runtime.py` — orchestrator subtask tracking
- `src/ag/skills/registry.py` — 5 delegation skills
- `tests/test_delegation.py` — 23 tests

### CLI global options
- `src/ag/cli/main.py` — `CLIContext`, `get_cli_ctx()`, `@app.callback()`
- `tests/test_cli_global_options.py` — 13 tests

---

## 9) Output format (how you respond)

### For Sprint 02 testing phase:
1. **Test execution summary** — command + pass/fail + any failures
2. **Issues found** — with file/line if applicable
3. **Fixes applied** — if any tests fail
4. **Evidence captured** — file paths for review

### For Sprint 03 planning:
1. **Sprint 02 DoD status** — all items checked
2. **Proposed Sprint 03 scope** — AF items + rationale
3. **Sprint 03 PR slicing plan** — sequence and dependencies

---

## 10) Environment setup verification

Before starting, verify:
```powershell
python --version   # Should be 3.14.x
pytest --version   # Should be 9.0.x
ag --version       # Should work
pytest tests/ -q   # Quick sanity check
```

If any fail, fix environment first.

---

## 11) OpenAI API setup for live testing

To enable real LLM integration tests (Phase B), you need an OpenAI API key.

### Step 1: Get your API key
1. Go to https://platform.openai.com/api-keys
2. Create a new API key (or use existing)
3. Copy the key (starts with `sk-`)

### Step 2: Set environment variable (session only)
```powershell
# PowerShell - current session only (recommended for testing)
$env:OPENAI_API_KEY = "sk-your-key-here"

# Verify it's set
$env:OPENAI_API_KEY.Substring(0, 7)  # Should show "sk-your"
```

### Step 3: Alternative - persistent environment variable
```powershell
# PowerShell - persist across sessions (use with caution)
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-your-key-here", "User")

# Restart terminal for it to take effect
```

### Step 4: Verify OpenAI SDK is installed
```powershell
# Check if openai package is installed
pip show openai

# If not installed:
pip install openai
# Or install with project extras:
pip install -e ".[llm]"
```

### Step 5: Test API connectivity
```python
# Quick Python test (run in REPL or as script)
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Minimal test call
response = client.chat.completions.create(
    model="gpt-4o-mini",  # Cheapest model for testing
    messages=[{"role": "user", "content": "Say 'API working' in exactly 2 words"}],
    max_tokens=10
)
print("Response:", response.choices[0].message.content)
print("Model:", response.model)
print("Tokens used:", response.usage.total_tokens)
```

### Step 6: Run integration tests with real API
```powershell
# Run only integration-marked tests (requires API key)
pytest tests/test_providers.py -v -m integration --tb=long

# Expected output: test_openai_real_api_call should PASS
```

### Security reminders
- **NEVER commit API keys** to git
- **NEVER paste keys in chat** — ask human to set them
- Use session-only env vars for testing
- Rotate keys if accidentally exposed
- Set spending limits in OpenAI dashboard

### Troubleshooting
| Issue | Solution |
|-------|----------|
| `AuthenticationError` | Check key is correct and not expired |
| `RateLimitError` | Wait and retry, or check OpenAI quota |
| `openai not found` | Run `pip install openai` |
| Key not found | Restart terminal after setting env var |
| `ProviderNotFoundError` | OpenAI SDK not installed; provider registry empty |

### Cost awareness
- Integration tests use `gpt-4o-mini` by default (cheapest)
- Each test call costs ~$0.001 or less
- Full integration suite: < $0.01 total
- Monitor usage at https://platform.openai.com/usage

---

## 12) Success criteria for this session

This session is successful when:
1. All Phase A automated tests pass with captured output
2. Phase B interactive tests completed with human verification
3. Review evidence folder created at `docs/dev/reviews/entries/REVIEW_S02_2026-02-26/`
4. Sprint 02 DoD checklist fully verified
5. Sprint 03 plan proposed and ready for next session
