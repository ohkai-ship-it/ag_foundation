# PROJECT CONTROL
#### Description: Consumer-specific rules for <project_name> that extend the generic Governance Standard. Defines project invariants, CI commands, coverage thresholds, and PR type taxonomy. Copy into the consumer's `docs/project/` folder, rename to `PROJECT_CONTROL_0.1.md`, and fill all applicable sections.
#### Convergent: v1.3.2
#### File version: 0.1
#### governs: <project_name>

---

## GS:PO01 Non-Negotiable Invariants

Consumer-specific invariants for <project_name>. These rules are absolute. No PR may violate them without explicit escalation (E4).

> List invariants that are specific to this project. GS §PO01 provides the generic invariants (Commit & PR Discipline, CI Discipline). Server Immutability is defined in §IM08.4. This section adds project-specific ones.

---

## GS:PO05 Architectural Layering

> Code projects only. Docs-only projects may omit this section.

Describe the module structure, interface-first development rules, trace instrumentation requirements, error handling policy, configuration resolution order, and performance/overhead rules.

---

## GS:PO02 Testing Requirements

Consumer-specific coverage thresholds, assertion targets, and warnings policy.

**Coverage Thresholds:**

| Module | Minimum Coverage |
|--------|-----------------|
| Overall | <threshold> |

**What to Assert in Tests:**
- ...

**Warnings Policy:**
- ...

**Network Restrictions:**
- ...

---

## GS:PO06 Autonomy Gate

> Code projects only. Docs-only projects may omit this section.

This gate is mandatory when sprint scope touches autonomy-affecting components.

**Start Gate (Sprint Planning):**
- [ ] ...

**Close Gate (Sprint Review/Closure):**
- [ ] ...

**Decision Rule:**
- If any P0 Autonomy Gate item is unchecked: sprint cannot be closed.
- If only P1/P2 items remain: `ACCEPT WITH FOLLOW-UPS` is allowed only if follow-up AF/BUG items are created and indexed.

---

## GS:PO03 Violations & Escalation

> Consumer-specific blocking conditions and prohibited actions that extend the generic escalation framework in GS §PO03.

---

## GS:PO04 ADR Creation Criteria

> Consumer-specific ADR thresholds that override the defaults in GS §PO04. Omit this section to use defaults.

---

## GS:PO07 CI Commands

CI commands for <project_name>.

**C1 — Targeted CI (per AF commit):**
```bash
<command>
```

**C2 — Full CI + evidence (review):**
```bash
<command>
```

**C3 — Full CI (pre-merge):**

| Check | Command | Success Criteria |
|-------|---------|------------------|
| ... | `<command>` | ... |

---

## GS:PO08 Living Docs

Project-specific living documents for <project_name>.

| Document | Update if sprint changed... |
|----------|----------------------------|
| ... | ... |

These are checked during the sprint review living docs sweep.

---

## GS:PO09 PR Type Taxonomy

Evidence requirements by PR type for <project_name>.

| PR Type | Tests Required | RunTrace Required |
|---------|---------------|-------------------|
| Docs-only | No | No |
| ... | ... | ... |

---

## References

- Project roadmap: `docs/project/PROJECT_ROADMAP.md` <!-- generic name — use highest version on disk -->
