# ADR-0003 — Manual mode gating strategy (dev/test only)
# Version number: v0.1

## Status
Proposed (write/merge with AF-0008)

## Date
2026-02-24

## Context
The system is LLM-first for end-user behavior. Manual mode exists only for development and CI tests (LLMs disabled). If manual mode is accessible by default, it risks becoming a user-facing path and creates ongoing overhead.

## Decision
Gate manual mode behind an explicit developer flag and record it in RunTrace:

- CLI requires `AG_DEV=1` (or equivalent) to run `--mode manual`.
- Without the gate, manual mode invocation fails fast with a clear error.
- When manual mode is used, CLI prints a prominent banner: `DEV MODE: manual (LLMs disabled)`.
- RunTrace records `mode=manual` and `dev_gate=true` (or equivalent) so UX labels are derived from persisted facts.
- CI uses manual mode with `AG_DEV=1` set in workflow configuration.

## Alternatives considered
- Allow manual mode without gating (rejected: violates invariant).
- Compile-time gating only (rejected: reduces local dev ergonomics and transparency).
- Interactive prompt confirmation (rejected: brittle for CI and scripts).

## Consequences
- Pros: keeps manual mode dev/test-only; aligns with truthful UX; easy to test.
- Cons: developers must set an env var; documentation must be explicit.
- Implementation: AF-0008 includes integration tests for gate on/off behavior.

## Related docs / links
- AF-0008 — CLI v0: ag run + runs show --json, truthful labels, manual dev gate
- WORKFLOW.md (evidence rules + CI expectations)

