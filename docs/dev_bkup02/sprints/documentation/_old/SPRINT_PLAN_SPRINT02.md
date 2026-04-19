# Sprint Plan — Sprint 02 — Agent network v0 + LLM provider adapter (OpenAI first)
# Version number: v0.1

## Metadata
- **Sprint:** Sprint 02 — Agent network v0 + LLM provider adapter (OpenAI first)
- **Dates:** 25.02.2026
- **Owner:** Kai (PM)
- **Tech lead:** Jeff
- **Implementer:** Jacob

## Sprint goal
1) Extend the v0 runtime from a single linear “echo” playbook to a **multi-step delegated playbook** that demonstrates agent-network behavior (planner → subtask steps → verifier) with clear RunTrace evidence.
2) Add a **provider abstraction** and deliver the first real provider: **OpenAI API** (Claude/local remain behind the same interface; add stubs and config shape now).
### OpenAI-first policy (Sprint 02)
- **OpenAI is the only real provider** in this sprint.
- Claude and local providers are **stubs that fail fast** with a structured error and still produce a RunTrace (for observability).
- This prevents accidental scope creep while keeping the architecture future-ready.
## Scope selection (existing AF items)
### Included (must)
- **AF-0014** — Resolve Recorder interface discrepancy (required for clean delegation tracing)
- **AF-0016** — Resolve ReasoningMode enum + Artifact path/uri semantics (prevents drift in new playbooks)
- **AF-0011** — CLI global options truly global (unblocks consistent workspace/json handling across new commands)
- **AF-0017** — OpenAI provider integration (new)
- **AF-0018** — Provider abstraction + Claude/local stubs (future-ready)
- **AF-0019** — Agent network playbook v0 (delegation) (new)

### Included (should)
- **AF-0013** — Contract inventory hardening + consistency checks (lightweight; prevents repeat drift)
- **AF-0012** — CLI surface parity + config tests — **scope guard:** if capacity is tight, take only the **config tests slice** (supports provider work); defer broader CLI parity stubs

### Excluded / deferred
- **AF-0015** (DB filename) — defer unless it blocks provider/config work (pure naming)
- Remaining CLI surface stubs beyond what the playbook + providers need

## Definition of Done (Sprint-level)
- [ ] At least one “delegation” run produces a RunTrace with ≥5 steps (planner + ≥2 subtasks + verifier + recorder) in a single workspace.
- [ ] OpenAI provider can be used in LLM mode via config/env vars (no secrets committed).
- [ ] Manual mode remains dev/test-only and still passes all tests.
- [ ] Tests added for provider abstraction and for agent-network playbook behavior.- [ ] **Coverage stays ≥ 85% overall; CLI and config coverage improve** (CLI is currently the weak spot at ~64%).- [ ] Review bundle created under `/docs/dev/reviews/entries/REVIEW_S02_<date>/` and review entry completed.

## Evidence expectations
- For each merged PR: tests + run_id(s) + trace JSON snapshots stored in the review evidence folder.
- CLI outputs for at least one delegated run + one provider-backed run.

## Risks & mitigations
- Provider integration adds network flakiness:
  - Mitigation: provider calls are integration-tested behind a marker and mocked in CI; unit tests cover request/response mapping.
- Scope creep into “full multi-agent framework”:
  - Mitigation: keep orchestration linear; “delegation” means multiple planned steps with clear inputs/outputs.

## PR slicing (one PR ↔ one AF)
1. AF-0014 — Recorder Protocol reconcile (docs/code/tests)
2. AF-0016 — Enum + artifact field semantics reconcile (docs/code/tests)
3. AF-0018 — Provider interface + registry + config schema first (Claude/local stubs fail fast)
4. AF-0017 — OpenAI adapter as clean plug-in with minimal glue (mocked tests)
5. AF-0019 — Agent-network playbook v0 (delegation) + integration tests
6. AF-0011 — CLI global options (if not already done)
7. AF-0013 — Inventory hardening (optional)

> **Note:** AF-0018 defines the abstraction; AF-0017 plugs in. Keep OpenAI adapter minimal.
