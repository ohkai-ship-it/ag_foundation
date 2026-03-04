# ag_foundation — Review Guide
# Version number: v0.1

This guide defines how we review changes and how we validate system behavior in ag_foundation.  
It is optimized for an agent-network system where correctness and **truthful observability** matter as much as features.

## Core review principles
1) **Truthfulness first:** anything the CLI/API claims must be provable from the persisted `RunTrace`.
2) **Interface-agnostic core:** changes must not couple logic to CLI-only paths.
3) **Modularity:** new behavior should land behind interfaces (core modules, skills, adapters).
4) **Safe defaults:** risky actions must be gated (permission/confirmation hooks), even if only simulated today.
5) **Evidence-driven:** every PR ships with evidence (tests, traces, or review notes) appropriate to its risk.

---

## Review artifacts (where to put things)
- **PR summary:** short description, scope, and evidence links.
- **Review entries:** `/docs/dev/reviews/entries/YYYY-MM-DD-<topic>.md`
- **Bugs:** `/docs/dev/bugs/reports/BUG-xxxx-<title>.md`
- **Backlog items:** `/docs/dev/backlog/items/AF-xxxx-<title>.md`

---

## Severity rubric (what kind of review is required)

### P0 / Critical
- Breaks truthful UX (labels don’t match trace)
- Breaks workspace isolation / data leakage
- Executes actions without required safety hooks
- Corrupts run storage / artifacts / traces

**Required:** tests + review entry + at least one real run trace captured (LLM or manual).

### P1 / High
- Changes planner/orchestrator/executor/verifier interfaces
- Changes trace schema fields
- Adds a new skill with tool access
- Adds or changes persistence

**Required:** tests + review entry (or expanded PR notes) + example trace.

### P2 / Normal
- Doc updates, refactors without behavior change, non-critical skills
- CLI UX improvements that are trace-derived

**Required:** basic checks + PR notes; tests if behavior touched.

---

## Review checklist (PR-level)

### 1) Scope & intent
- [ ] Clear goal and non-goals stated
- [ ] PR size is reasonable (or split plan exists)
- [ ] Backlog item(s) referenced (AF-xxxx)

### 2) Architecture alignment
- [ ] Logic added in the right layer (adapter vs core vs skill)
- [ ] Interfaces respected (no hard coupling)
- [ ] Playbook/reasoning modes unchanged unless explicitly intended

### 3) Truthful UX (mandatory for user-visible changes)
- [ ] Any CLI label (“verified”, “used retrieval”, “mode”) is derived from RunTrace
- [ ] No hardcoded “computed/verified” claims
- [ ] `--json` outputs are machine-readable and stable

### 4) Trace and observability
- [ ] RunTrace includes enough metadata to explain behavior
- [ ] New trace fields are documented and backwards compatible (or migration noted)
- [ ] Steps contain tool/skill calls with outcomes and timing

### 5) Safety hooks
- [ ] Permission/confirmation hooks are present where actions could be high-impact
- [ ] Defaults are safe (no implicit escalation)
- [ ] Manual mode remains dev/test-only (if touched)

### 6) Tests & evidence
- [ ] Unit tests cover core logic changes
- [ ] Integration tests cover end-to-end `ag run` if pipeline changed
- [ ] At least one captured run trace demonstrates the change

### 7) Docs and templates
- [ ] Cornerstone docs updated if architecture contract changed
- [ ] New configs/flags documented in CLI_REFERENCE

---

## How to validate a run (RunTrace-based)

### Minimum “run validation” steps
1) Identify the run:
- `ag runs show <run_id>` (human) or `--json`

2) Verify the mode and interface:
- `mode` must match what was requested (default llm)
- `interface` should be `cli` unless running via API later

3) Validate steps:
- Steps present and ordered
- Each step has role + reasoning_mode
- Tool/skill calls recorded (or explicitly absent)

4) Validate truth claims:
- If CLI says “verified: pass” → `verifier.status == pass`
- If CLI says “retrieval used” → evidence/tool calls show Retriever invoked
- If repairs occurred → trace shows retries/repair steps

5) Validate artifacts:
- artifact registry lists created outputs
- artifact references include `created_by_step`

### What “good” looks like
- A reviewer can explain the run outcome solely from the trace + artifacts.
- The trace makes failures actionable (where and why it failed).

---

## Required evidence by change type

### A) Docs-only changes
- PR notes referencing updated files
- Optional: review entry if it changes canonical contracts

### B) CLI-only changes
- Screenshot or captured output
- Corresponding RunTrace snippet proving labels match

### C) Core runtime changes
- Unit tests
- Example run trace (manual ok for speed)
- Review entry summarizing impact and invariants

### D) New skill/plugin
- Contract doc (inputs/outputs/permissions)
- Tests (at least happy-path + failure-path)
- Example trace showing skill invocation + results

### E) Retrieval / memory changes (RAG-ready)
- Evidence bundle format documented
- Trace includes evidence references
- Tests for “retrieval on/off” behavior

---

## Definition of Done (DoD) for a PR
A PR is done when:
- [ ] It meets acceptance criteria of its backlog item
- [ ] It passes required checks (tests, lint, etc.)
- [ ] It includes evidence appropriate to risk level
- [ ] It does not break truthful UX
- [ ] It does not introduce cross-workspace leakage
