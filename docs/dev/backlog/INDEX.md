# ag_foundation Backlog Index

Status legend: Proposed → Ready → In Progress → Done (or Blocked / Dropped)

## Backlog

| ID | Priority | Status | Title | Area | Owner |
|---:|:--:|:--|---|---|---|
| AF-0012 | P2 | Ready | CLI_REFERENCE surface parity v0.1 (partial — if capacity) | CLI | Jacob |
| AF-0013 | P1 | Ready | Contract inventory hardening: reconcile docs ↔ implementation | Contracts | Jacob |
| AF-0015 | P2 | Ready | Resolve storage DB filename mismatch (docs vs code) | Storage | Jacob |

## Sprint 02 Items (Agent network v0 + LLM provider) — COMPLETED

| ID | Priority | Status | Title | Area | Owner |
|---:|:--:|:--|---|---|---|
| AF-0017 | P0 | Done | OpenAI API integration (provider adapter) + config wiring | Providers | Jacob |
| AF-0019 | P0 | Done | Agent network playbook v0: delegation with multi-step trace | Kernel | Jacob |
| AF-0011 | P1 | Done | CLI global options: --workspace/--json/--quiet/--verbose truly global | CLI | Jacob |
| AF-0014 | P1 | Done | Resolve Recorder interface discrepancy (docs vs implementation) | Kernel | Jacob |
| AF-0018 | P1 | Done | Provider abstraction + Claude/local stubs | Providers | Jacob |
| AF-0016 | P2 | Done | Resolve contract drift: ReasoningMode enum vs examples; Artifact semantics | Contracts | Jacob |

## Sprint 02 Hardening Extension — COMPLETED

Hardening follow-up items triggered by SQLite connection leak bug discovery.

| ID | Priority | Status | Title | Area | Owner |
|---:|:--:|:--|---|---|---|
| BUG-0004 | P1 | Fixed | SQLite connections not closed → ResourceWarning | Storage | Jacob |
| BUG-0005 | P0 | Fixed | Implicit workspace creation on ag run | CLI/Storage | Jacob |
| AF-0021 | P1 | Done | Storage lifecycle hardening (SQLite deterministic closure) | Storage | Jacob |
| AF-0022 | P1 | Done | Provider coverage hardening (≥95% target) | Providers | Jacob |
| AF-0023 | P1 | Done | Environment & configuration hardening | Config | Jacob |
| AF-0024 | P1 | Done | Workspace lifecycle correction (ag ws create/list) | CLI | Jacob |
| AF-0025 | P1 | Done | Test discipline enforcement (Ruff + docs) | Testing | Jacob |
| AF-0026 | P0 | Done | Workspace selection policy enforcement | CLI/Runtime | Jacob |

## Sprint 01 Items (2026-03-02 → 2026-03-15)

| ID | Priority | Status | Title | Area | Owner |
|---:|:--:|:--|---|---|---|
| AF-0004 | P0 | Done | Sprint OS hygiene: sprint log + docs/dev pointers + handoff rules | Docs | Jeff |
| AF-0010 | P0 | Done | Python project bootstrap (packaging + CLI stub + pytest) | Repo | Jacob |
| AF-0005 | P0 | Done | Contracts: TaskSpec + RunTrace + Playbook schemas v0.1 | Kernel | Jeff |
| AF-0006 | P0 | Done | Workspace + storage baseline (sqlite + filesystem) | Storage | Jacob |
| AF-0007 | P0 | Done | Core runtime skeleton v0 (interfaces + playbook + stub skills) | Kernel | Jacob |
| AF-0008 | P0 | Done | CLI v0: ag run + runs show --json, truthful labels, manual gate | CLI | Jacob |
| AF-0009 | P1 | Done | Artifact registry v0 + ag artifacts list | Storage | Jacob |

## Sprint 00 Items (Completed)

| ID | Priority | Status | Title | Area | Owner |
|---:|:--:|:--|---|---|---|
| AF-0001 | P0 | Done | Kick-off: establish new docs/dev foundation | Docs/Process | Kai/Jeff |
| AF-0002 | P0 | Done | New cornerstone docs (IoT-in-space vision) | Docs/Architecture | Jeff |
| AF-0003 | P0 | Done | Core runtime skeleton (request + event driven) — docs only | Architecture/Kernel | Jeff/Jacob |

## Item Details
See individual files in [items/](items/) for full acceptance criteria and implementation notes.

## Completion Notes
See [completion/](completion/) for detailed completion notes documenting what was implemented, test results, and acceptance criteria verification.