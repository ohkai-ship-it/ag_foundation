# ADR-0002 — TaskSpec & RunTrace versioning and compatibility rules
# Version number: v0.1

## Status
Proposed (write/merge with AF-0005)

## Date
2026-02-24

## Context
Truthful UX and evidence rules depend on persisted RunTrace facts. The trace schema will evolve, but we must avoid breaking CLI consumers, review workflows, and stored historical traces. We need explicit rules for how TaskSpec/RunTrace versions are declared, validated, and migrated (if at all).

## Decision
Adopt explicit, self-describing schema version fields and an additive-first evolution policy:

- `task_spec_version` and `trace_version` are required top-level fields.
- v0 schemas are **additive-only**: new optional fields may be added; renames/removals are not allowed within v0.
- Breaking changes require a new major version (v1) and an explicit migration plan.
- Parser/loader must accept older versions and normalize to an internal model where possible.
- CLI labels must only use fields guaranteed in the current supported versions; if absent, CLI must render `unknown`.
- Store traces as JSON files; the stored file always contains the original version fields.

## Alternatives considered
- No versioning until later (rejected: will cause silent breakage as features land).
- Full DB migrations + strict enforcement immediately (rejected: too heavy for early stage).
- Rely on git tags / release versions only (rejected: doesn’t help with persisted historical traces).

## Consequences
- Pros: minimizes churn; enables backward compatibility; protects truthful UX.
- Cons: requires discipline (no renames/removals in v0); occasional `unknown` in CLI output.
- Implementation: AF-0005 must include contract tests to lock in compatibility guarantees.

## Related docs / links
- AF-0005 — Contracts-first: TaskSpec + RunTrace v0 schemas and builders
- CLI_REFERENCE.md (truthful UX requirements)
- REVIEW_GUIDE.md (evidence + trace expectations)

