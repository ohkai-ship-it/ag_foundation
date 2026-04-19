# BACKLOG ITEM — AF0148 — workspace_isolation_design
# Convergent version: v1.3.1
# Created: 2026-04-06
# Started:
# Completed:
# Status: PROPOSED
# Priority: P2
# Area: CLI / Storage / Architecture
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
- **ID:** AF-0148
- **Type:** Conceptual / Architecture
- **Status:** PROPOSED
- **Priority:** P2
- **Area:** CLI / Storage / Architecture
- **Owner:** (unassigned)
- **Target sprint:** (unassigned)
- **Origin:** Replaces BUG-0011 (default workspace name leaked in error)

---

## Problem

BUG-0011 reported that error messages leak the implicitly-resolved workspace name to users who never typed it. But this is a symptom of a broader issue: **workspace boundaries are not enforced**.

Known cross-workspace leakage:
1. **Error messages** — Implicit default workspace name shown in errors (BUG-0011 symptom)
2. **`ag ws list`** — Shows all workspaces to all users, regardless of context
3. **Storage path** — All workspaces share `~/.ag/workspaces/` with no access control or scoping

The current workspace model is single-user, flat-directory, global-visibility. This works for development but creates confusion as usage grows (multiple projects, shared machines, CI environments).

---

## Goal

Design a workspace isolation model that addresses cross-workspace leakage. This is a **conceptual AF** — the deliverable is a design document (or ADR), not code.

---

## Scope

1. **Audit** — Inventory all places where workspace boundaries are crossed (CLI commands, storage, error messages, config resolution)
2. **Design** — Propose an isolation model:
   - Should `ag ws list` be scoped? By what? (project directory, config, explicit scope?)
   - Should error messages distinguish implicit vs explicit workspace resolution?
   - Is per-project workspace binding the right model? (`.ag/workspace.json` in project root?)
   - What about CI environments? (ephemeral workspaces, no shared state)
3. **ADR** — Write an ADR (or update ADR-0006/ADR-0007 if relevant) with the chosen approach
4. **Follow-up AFs** — Propose 1–3 implementation AFs based on the design

---

## Non-Goals

- Do NOT implement the solution (this AF produces a design only)
- Do NOT change workspace storage format (that's a follow-up)
- Do NOT address multi-user/multi-tenant scenarios (out of scope for v0.x)

---

## Acceptance criteria

1. Design document or ADR written and reviewed
2. All known cross-workspace leakage points inventoried
3. Proposed model addresses BUG-0011 symptom and `ag ws list` scoping
4. Follow-up implementation AFs identified with rough scope
