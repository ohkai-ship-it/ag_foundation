# S14_REVIEW_01 — Pass 5 Bug Triage
# Generated: 2026-03-22

## Bugs discovered during review execution

### BUG-CANDIDATE-01: pytest -W error fails intermittently due to SSL socket GC noise

**Severity:** P2 (test infrastructure quality, not runtime behavior)

**Description:**
Running `pytest -W error` fails non-deterministically. The `ddgs`/`primp` Rust
HTTP client (underlying DuckDuckGo search) opens a Cloudflare SSL/TLS connection
as part of its session setup. When Python's garbage collector finalizes the socket
object after a test that uses DDGS mocks, it emits a `ResourceWarning`. pytest
catches this via the unraisable exception hook and converts it to
`PytestUnraisableExceptionWarning`. Under `-W error`, this becomes a hard failure.

**Evidence:**
- Reproduced: 3/3 full suite runs with `-W error` show 1 failure, different test
  each time (GC-timing dependent).
- Isolated: each failing test passes in isolation with `-W error`.
- Not caused by S14 work: ddgs/primp introduced earlier; E501/I001 lint fixes were
  pre-existing.

**Root cause:** ddgs uses `primp` (Rust-based HTTP client) which creates an SSL
connection pool. Even mocked DDGS tests trigger the import which initializes the
Cloudflare HTTP/2 session. Connection is leaked on process exit.

**Workaround applied for this review:**
- `pyproject.toml` `filterwarnings` set — but does NOT suppress under `-W error`
  (CLI flag takes precedence over ini).
- Review uses clean `pytest` run (no `-W error`) showing 751 passed.

**Recommended fix:** Create follow-up AF to investigate:
  - Option A: Mock at the `primp`/`httpx` transport layer to prevent real sockets
  - Option B: Pin `ddgs` to a version without connection pooling
  - Option C: Suppress `ResourceWarning` in `conftest.py` via `gc.collect()` teardown

**Status:** FLAGGED — follow-up AF to be created post-review
**Not a blocker:** 751 tests pass cleanly without `-W error`. Core S14 behavior unaffected.
