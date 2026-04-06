# CHANGELOG
# Convergent version: v1.3.1
# Format: Based on [Keep a Changelog](https://keepachangelog.com/)

> All notable changes to the GVS governance framework are documented in this file.
> Entries marked *(reconstructed)* were compiled retroactively from sprint records,
> INDEX files, and project observations — not from contemporaneous release notes.

---

## [v1.3.1] — 2026-04-06 (in progress)

Governance pit stop: fix contradictions, process gaps, and missing protocols accumulated through v1.0–v1.3 before proceeding to v1.4.

### Added
- HITL framework (FM §10) — gates G1–G15 with trigger, authority, examples
- Versioning conventions (FM §3.4) — convergent version vs. file version rules
- Mid-sprint scope change protocol (SM §6A) — trigger, approval, impact checklist, change log
- CHANGELOG.md (this file) — retroactive version history

### Changed
- Status values reconciled — single canonical set in FM §7.6 for all artifact types
- Sprint statuses simplified: `PLANNED | DONE | REJECTED` (was 6-state: Draft → Ready → In Progress → In Review → Accepted → Closed)
- Bug statuses simplified: `OPEN | FIXED | DROPPED` (removed `IN_PROGRESS`, `VERIFIED`)
- Merge strategy: regular merge (was squash merge) to preserve per-AF traceability
- §7 "Post-Merge Ritual" → "Pre-Merge Status Finalization" — all status updates on branch before merge
- PR creation protocol clarified — template filled as `S##_PULL_REQUEST.md`, used verbatim as GitHub PR body
- Legacy file rename instruction removed — immutability wins for all files

### Fixed
- BUG-0001: PR document contradiction in SM §6.0 ("no separate PR document" vs. template workflow)
- BUG-0002: Item timestamp format wrong in templates (included in AF-0011)
- FM §3.2 status values conflicted with FOLDER_STRUCTURE_0.3 and INDEX headers
- FM §7.6 sprint transition diagram conflicted with template and INDEX usage
- SM §6.0 commit granularity ("multiple commits per AF") conflicted with §1 ("1 commit per AF")
- SM §6.3/§8.6 review file timing ambiguity resolved
- FM version header corrected (was v1.0, should be v1.3) *(Sprint 00, C1)*
- FM §7.2 status alignment rule rewritten for new/legacy conventions *(Sprint 00, C2)*
- FM §3.2 naming conventions restructured *(Sprint 00, C3)*
- FM §3.2/§7.6 status value sets simplified *(Sprint 00, C4)*
- FM §3.1/§7.3 paths made relative *(Sprint 00, C5–C6)*

---

## [v1.3] — 2026-03-04 (effective) / 2026-04-05 (extracted)

Governance framework extracted from ag_foundation as a standalone server. Frozen after extraction — changes require formal patches via ADR-001.

### Added
- Server/client deployment model — governance docs maintained in `gvs_version_fixed/`, deployed to consumer projects
- New naming convention — immutable filenames without status tokens (coexists with legacy)
- FOLDER_STRUCTURE_0.3.md — codified layout with dual naming convention documentation
- PATCH_V1_3.md — audit trail for post-freeze corrections
- Docs-only client overrides (O1–O5) — for projects with no source code or CI pipeline
- ADR-001: v1.3 patch authorization
- ADR-002: v1.3.1 development strategy
- ADR-003: Convergent tracking model

### Changed
- Governance docs moved from embedded in ag_foundation to standalone governance server
- Status tracking: new files use 2-place model (metadata + INDEX); legacy files keep 3-place model (filename + metadata + INDEX)

### Known issues at freeze
- HITL gates G1–G15 referenced but undefined
- Status values inconsistent across FM, FOLDER_STRUCTURE, templates
- Git instructions contained 15 contradiction/ambiguity issues
- No CHANGELOG, no scope change protocol, no versioning conventions

---

## [v1.2] — *(date unknown, reconstructed)*

*(Limited documentation survives. Changes inferred from project timeline and folder structure evolution.)*

### Changed
- Folder structure refined — FOLDER_STRUCTURE_0.2.md documents intermediate layout
- INDEX schemas evolved

---

## [v1.1] — *(date unknown, reconstructed)*

*(Limited documentation survives.)*

### Changed
- Governance framework refinements during ag_foundation development sprints

---

## [v1.0] — ~early 2026 *(reconstructed)*

Initial governance framework, embedded in ag_foundation's `docs/dev/` folder.

### Added
- Foundation Manual — operating rules, core invariants, CI discipline
- Sprint Manual — step-by-step sprint execution protocol
- INDEX system — backlog (AFs), bugs, decisions, sprints
- Artifact naming convention with status tokens in filenames
- Templates — sprint description, PR, backlog item, bug report, ADR
- Status value sets for all artifact types
- Core invariants: Truthful UX, Workspace Isolation, Manual Mode Gating, Layer Separation
