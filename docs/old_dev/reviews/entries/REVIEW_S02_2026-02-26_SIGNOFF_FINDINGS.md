# Sprint 02 Hardening Sign-Off — Verification Findings

**Date:** 2026-02-26  
**Reviewer:** Jacob  
**Purpose:** Provide evidence and precise answers to unblock architectural sign-off

---

## 1) Coverage Results

### Summary Table

```
Name                             Stmts   Miss  Cover
------------------------------------------------------
TOTAL                             1301    130    90%

CLI (main.py):                     367     99    73%
Providers (aggregate):             180      7    96%
  - openai.py                       60      4    93%
  - base.py                         61      0   100%
  - stubs.py                        32      3    91%
  - registry.py                     22      0   100%
Storage (aggregate):               232      9    96%
  - sqlite_store.py                156      7    96%
  - workspace.py                    60      2    97%
```

### Threshold Verification

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Overall | ≥85% | **90%** | ✅ PASS |
| CLI | ≥72% | **73%** | ✅ PASS |
| Providers | ≥95% | **96%** | ✅ PASS |
| Storage | ≥95% | **96%** | ✅ PASS |

### Test Failures Noted

⚠️ **2 tests failed** in `test_providers.py`:
- `test_openai_validate_without_key_raises`
- `test_openai_chat_without_key_raises`

**Root cause:** OPENAI_API_KEY is set in the test environment, causing tests expecting `ProviderError` to not raise.

**Assessment:** Environment-dependent test issue, not a code defect. Tests pass when OPENAI_API_KEY is unset.

---

## 2) Workspace Behavior

### Question: What happens when no workspace exists and user runs `ag run "test"`?

**Answer: C) Silently creates new workspace per run**

### Evidence

```powershell
> $env:AG_WORKSPACE_DIR = "$env:TEMP\ag_test_verify"
> Remove-Item -Recurse -Force $env:AG_WORKSPACE_DIR
> ag run "test"

Run completed
  Run ID: 71f9db65-8946-440f-836b-baedd58cb2da
  Workspace: ws-96a0f3e2
  
> ag run "second test"

Run completed
  Run ID: d08da3ae-d246-4220-a36d-9bfc4ea23612
  Workspace: ws-3cde21e0

> ag ws list
┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Workspace ID ┃ Path                                                       ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ ws-3cde21e0  │ C:\Users\Kai\AppData\Local\Temp\ag_test_verify\ws-3cde21e0 │
│ ws-96a0f3e2  │ C:\Users\Kai\AppData\Local\Temp\ag_test_verify\ws-96a0f3e2 │
└──────────────┴────────────────────────────────────────────────────────────┘
```

### Details

| Item | Value |
|------|-------|
| CLI output | Shows "Run completed" with auto-generated workspace ID |
| ws list output | **2 workspaces** created by 2 runs (not reused) |
| DB path | `$AG_WORKSPACE_DIR/ws-{id}/db.sqlite` |
| RunTrace workspace_id | `ws-96a0f3e2` (first run), `ws-3cde21e0` (second run) |

### Architectural Issue

❌ **Each `ag run` creates a NEW workspace** when no `--workspace` is specified.

This violates AF-0024 architectural intent:
- Runs should reuse an existing workspace (via `AG_WORKSPACE` env var or `--workspace` flag)
- Or require explicit workspace creation via `ag ws create`

**Current behavior:** If no workspace specified, Runtime generates a new `ws-{uuid}` per run, causing workspace proliferation.

---

## 3) Configuration Precedence

### Expected Precedence Order

1. TaskSpec override
2. Workspace config
3. `.env` file
4. Defaults

### Implementation Status

| Layer | Implemented | Tested |
|-------|-------------|--------|
| TaskSpec override | ❌ No | ❌ No |
| Workspace config | ❌ No | ❌ No |
| .env → defaults | ✅ Yes | ✅ Yes |

### Code Location

- `src/ag/config.py` — `get_workspace_dir()`, `get_config_path()`, `get_default_workspace()`

### Test Coverage

Tests in `tests/test_config.py`:
- ✅ `test_env_var_overrides_default` (workspace dir)
- ✅ `test_env_var_overrides_default_workspace` (workspace ID)
- ✅ `test_env_var_overrides_config_path` (config path)

### Gaps

⚠️ **No full precedence test exists**

- `load_config()` is a stub returning `{}`
- TaskSpec override mechanism not implemented
- Workspace config file parsing not implemented
- No test verifies full chain: TaskSpec → Workspace config → .env → Defaults

---

## 4) SQLite Connection Lifetime Model

### Connection Lifetime

**Model:** Once per workspace (cached in store instance)

### Lifecycle Flow

1. **Creation:** `SQLiteRunStore._get_conn()` / `SQLiteArtifactStore._get_conn()`
   - Lazily created on first access to a workspace
   
2. **Caching:** `_connections: dict[str, sqlite3.Connection]`
   - Keyed by workspace_id
   - Reused for all operations within same store instance

3. **Closure:** `close()` method or `__exit__` context manager
   - Iterates `_connections` and closes all
   - Clears the dictionary

### Global/Static Connections

**No** — Connections are instance-scoped, not module-level or static.

### Code Evidence

```python
class SQLiteRunStore:
    def __init__(self, workspaces_root: Path | None = None) -> None:
        self._root = workspaces_root or get_workspace_dir()
        self._connections: dict[str, sqlite3.Connection] = {}

    def _get_conn(self, workspace_id: str) -> sqlite3.Connection:
        if workspace_id not in self._connections:
            ws = self._get_workspace(workspace_id)
            self._connections[workspace_id] = _init_db(ws.db_path)
        return self._connections[workspace_id]

    def close(self) -> None:
        for conn in self._connections.values():
            conn.close()
        self._connections.clear()

    def __enter__(self) -> "SQLiteRunStore":
        return self

    def __exit__(self, ...):
        self.close()
```

---

## Summary

| Area | Status | Notes |
|------|--------|-------|
| Coverage | ✅ **All thresholds met** | 2 env-dependent test failures (not code defects) |
| Workspace Behavior | ❌ **Issue** | Creates new workspace per run instead of reusing |
| Config Precedence | ⚠️ **Partial** | Only env→default implemented; full chain missing |
| SQLite Lifecycle | ✅ **Correct** | Properly scoped per workspace instance |

---

## Recommendations

### Blocking Issues

1. **Workspace proliferation** — `ag run` without `--workspace` should:
   - Use `AG_WORKSPACE` env var if set
   - Or use a configured default workspace
   - Or fail with explicit message requiring workspace specification

### Non-Blocking (Future Work)

2. **Config precedence** — Implement full chain when config file parsing lands
3. **Test environment** — Consider skipping OpenAI tests when API key is set in CI/local env

---

**Sign-off Decision:** Pending Architect review of workspace behavior issue.
