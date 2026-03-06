# ADR-0004 — Storage baseline: workspace-scoped SQLite + filesystem layout
# Version number: v0.1

## Status
ACCEPTED (merged with AF-0006)

## Date
2026-02-24

## Context
We need durable run persistence, artifact indexing, and strict workspace isolation. Early stage requires a simple, local-first baseline that works in CI and on developer machines, while remaining swappable behind interfaces later.

## Decision
Adopt workspace-scoped storage with:

- Filesystem for immutable-ish objects: RunTrace JSON files and artifact payloads.
- SQLite for indices and queryable metadata (runs, artifacts, timestamps, statuses).
- One SQLite file per workspace; all paths are resolved relative to workspace root.
- Workspace isolation enforced by: (a) workspace_id required in APIs, (b) path joins disallow traversal, (c) queries scoped to workspace DB handle only.
- Storage is accessed through interfaces (`RunStore`, `ArtifactStore`, etc.) to enable future backends.

## Alternatives considered
- Postgres from day one (rejected: operational overhead too early).
- Filesystem-only (rejected: slow/awkward queries; poor listing/filters).
- SQLite global DB across workspaces (rejected: increases risk of cross-workspace leakage).

## Consequences
- Pros: simple, local-first, CI-friendly; supports listing/inspection; strong isolation by construction.
- Cons: requires careful schema evolution; concurrency limits if later parallelism increases.
- Implementation: AF-0006 must include isolation tests and path-traversal hardening.

## Related docs / links
- AF-0006 — Workspace + storage baseline (sqlite + filesystem) with strict isolation
- ARCHITECTURE.md (storage & workspace isolation sections)




