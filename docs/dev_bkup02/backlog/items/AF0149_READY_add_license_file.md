# BACKLOG ITEM — AF0149 — add_license_file
# Convergent version: v1.3.1
# Created: 2026-04-12
# Started:
# Completed:
# Status: READY
# Priority: P1
# Area: Governance / IP
# Models:

> **FOUNDATION GOVERNANCE**
> This file is governed by:
> `/docs/dev/foundation/FOUNDATION_MANUAL.md`
>
> Critical invariants in this context:
> - Truthful UX (trace-derived labels)
> - Workspace isolation
> - CI workflow (two-phase — see below)
> - 1 PR = 1 sprint
> - INDEX update rule (status ↔ filename integrity)
>
> **CI workflow (CRITICAL):**
> - **During AF development:** run targeted tests only
> - **Before commit (full gate):** run the complete CI gate

---

## Metadata
- **ID:** AF-0149
- **Type:** Governance / IP
- **Status:** READY
- **Priority:** P1
- **Area:** Governance / IP
- **Owner:** (unassigned)
- **Target sprint:** (unassigned)
- **Origin:** M&A Audit Report 2026-04-12 — Part I §2, Part VI Phase 1 item #2

---

## Problem

`pyproject.toml` declares `license = "MIT"` but no `LICENSE` file exists at the repository root. This creates an ambiguity: the metadata claims MIT but there is no legally binding license text. Package consumers, auditors, and automated license scanners (e.g., FOSSA, Snyk) that inspect the file tree will flag this as "license unknown" or "no license."

---

## Acceptance Criteria

1. A `LICENSE` file exists at the repository root containing the full MIT License text
2. The copyright holder and year match the project metadata
3. `pyproject.toml` `license` field remains consistent (`"MIT"`)

---

## Scope

- Add `LICENSE` file with standard MIT License text at repo root
- Verify `pyproject.toml` `license` field still matches

---

## Out of Scope

- IP assignment agreements (separate governance concern, not a code artifact)
- CLA setup (not needed until external contributors exist)
- License header injection into source files (not required by MIT)

---

## Estimate

**XS** — single file creation, no code changes, no tests needed.
