# BUG REPORT — BUG-0015 — runs list count mismatch
# Version number: v0.2

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI discipline (ruff + pytest -W error + coverage)
> - INDEX update rule (status ↔ filename integrity)
> - Evidence capture requirement (RunTrace ID for CLI/runtime bugs)

---

## Metadata
- **ID:** BUG-0015
- **Status:** OPEN
- **Severity:** P2
- **Area:** Storage / CLI
- **Reported by:** Kai
- **Date:** 2026-03-12
- **Related backlog item(s):** —
- **Related ADR(s):** —
- **Related PR(s):** —

---

## Summary
`ag runs list --all` displays an inflated total count that doesn't match the number of runs actually shown. The CLI reports "46 total" but only displays 15 runs. The discrepancy is caused by orphaned entries in the SQLite index (`db.sqlite`) that reference runs whose trace files have been deleted from the filesystem.

---

## Expected behavior
The total count shown in `ag runs list` should match the number of runs that actually exist and can be displayed/retrieved.

---

## Actual behavior
The CLI shows "(46 total)" in the table header but only lists 15 runs. The `count()` method returns 46 (from SQLite index), while `list()` returns 15 (only runs with existing trace.json files).

---

## Reproduction steps
1. Have a workspace with runs that were partially deleted (trace files removed but SQLite index entries remain)
2. Run `ag runs list -w <workspace> --all`
3. Observe the count mismatch between "X total" and actual rows displayed

Evidence from `skills01` workspace:
- SQLite `runs` table has 46 entries
- Only 15 `trace.json` files exist in `runs/` directory

---

## Evidence
- **CLI output:**
```
ag runs list -w skills01 --all
                                       Runs in workspace 'skills01' (46 total)
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ Run ID                               ┃ Status  ┃ Verifier ┃ Mode       ┃ Model       ┃ Duration ┃ Started          ┃
...
└──────────────────────────────────────┴─────────┴──────────┴────────────┴─────────────┴──────────┴──────────────────┘
(only 15 rows displayed)
```

- **Database verification:**
```python
# db.sqlite has 46 entries
conn.execute('SELECT COUNT(*) FROM runs').fetchone()[0]  # → 46

# Only 15 trace.json files exist
Get-ChildItem "runs" -Recurse -Filter "trace.json" | Measure-Object  # → 15
```

- **Environment:** Windows, Python 3.12, commit TBD

---

## Impact
- **User confusion:** UX suggests 31 runs exist that cannot be viewed
- **Violates Truthful UX principle:** displayed count is misleading
- **No data loss:** the runs were already deleted, only stale index entries remain

---

## Suspected cause
The `list()` method in `SQLiteRunStore` queries run IDs from the database, then attempts to load each trace from the filesystem. If the file doesn't exist, the run is silently skipped. However, the `count()` method only queries the database without verifying file existence.

```python
# sqlite_store.py — list() silently skips missing files
for row in cursor:
    trace = self.get(workspace_id, row["run_id"])
    if trace:  # ← only appends if trace.json exists
        runs.append(trace)

# sqlite_store.py — count() doesn't verify files
def count(self, workspace_id: str) -> int:
    cursor = conn.execute("SELECT COUNT(*) FROM runs WHERE workspace_id = ?", ...)
    return cursor.fetchone()[0]  # ← returns stale count
```

---

## Proposed fix
Three possible approaches (choose one or combine):

### Option B: Purge orphaned entries during list (lazy cleanup)
When `list()` finds a missing trace file, delete the orphaned database entry. This self-heals the index over time.

We choose the lazy cleanup here

### Recommended: Option B
Lazy cleanup during `list()` provides automatic reconciliation with no UX change.

---

## Acceptance criteria (for verification)
- [ ] `ag runs list --all` shows accurate total count matching displayed rows
- [ ] Orphaned index entries are cleaned up (Option B) or reported (Option C)
- [ ] Tests added for index-filesystem consistency
- [ ] `pytest -W error` passes
- [ ] `ruff check src tests` passes

---

## Notes
- The stale `runs.db` file (0 bytes) in the workspace root is a leftover from an older schema. The current schema uses `db.sqlite`.
- Root cause of orphan entries is unknown — likely manual deletion of run folders.

---

## Status log
- 2026-03-12 — Opened by Kai
