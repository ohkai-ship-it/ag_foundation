# Governance System (GVS) — Standalone Project Plan
# Version: v0.1
# Date: 2026-04-05
# Authors: Kai (human, PM), Jeff (Claude Opus 4.6, Tech Lead)
# Status: DRAFT
# Origin: Sprint 16 observations (S16_OBSERVATIONS_0.1.md §4)

---

## 1. Executive Summary

Extract the governance system currently embedded in ag_foundation's `docs/dev/` tree into a standalone, versioned project. The governance system (GVS) becomes an independent product that ag_foundation — and future projects — consume as a framework for sprint-based, agent-executed software development.

**Why now:** Sprint 16 revealed that governance improvements are blocked by ag_foundation's runtime development overhead. Decoupling lets the governance system iterate on its own cadence while consumers adopt versions at their own pace.

**Scope:** This plan covers the extraction, architecture, consumer model, and initial roadmap. It does NOT cover ag_foundation's runtime development — that stays in its own project plan.

---

## 2. Vision

A portable, versioned governance framework for AI-agent software development that provides:

- Deterministic sprint execution (manuals, templates, gates)
- Structured artifact management (INDEX schemas, item templates)
- Human-in-the-Loop (HITL) safety gates
- Version-controlled conventions that evolve without breaking consumers

**Design principle:** Governance system = framework. Consumer project = application. The framework ships structure and rules; the consumer fills them with content.

---

## 3. Current State (GSV v1.3)

The governance system exists today as files within ag_foundation:

| Component | Location | Version |
|---|---|---|
| Foundation Manual | `docs/dev/foundation/FOUNDATION_MANUAL.md` | v1.0 |
| Sprint Manual | `docs/dev/foundation/SPRINT_MANUAL.md` | v1.3 |
| Folder Structure | `docs/dev/foundation/FOLDER_STRUCTURE_0.3.md` | v0.3 |
| INDEX schemas (4) | `docs/dev/backlog/`, `bugs/`, `decisions/`, `sprints/` | v1.3 |
| Templates (6) | `docs/dev/foundation/templates/` | v1.3 (except PR template v0.2) |
| HITL Framework | FOUNDATION_MANUAL §10 + GOVERNANCE_SIMPLIFICATION_PLAN §2 | v1.3 |
| Copilot instructions | `.github/copilot-instructions.md` | — |

**Known issues at extraction time:**
- BUG-0026: PR template version gap (v0.2 → should be v1.3)
- PROJECT_PLAN staleness (Sprint 16 not reflected)
- No CHANGELOG for governance version bumps
- No formal scope change protocol
- INDEX files need cleanup (ag_foundation content must not leak into GVS development artifacts)

---

## 4. Architecture

### 4.1 Server / Client Model

GVS uses a **server/client** deployment model. A fixed governance version (the server) governs one or more client projects. The server is never edited — only replaced wholesale with a new version.

```
┌──────────────────────────────────┐     ┌──────────────────────────────┐
│  SERVER (gvs_version_fixed/)     │     │  CLIENT (any project)        │
│  ────────────────────────────    │     │  ──────────────────────────  │
│  Fixed, read-only.               │────▶│  Governed by the server.     │
│  Contains all governance rules.  │     │  Produces its own work       │
│  Replaced wholesale on upgrade.  │     │  product (code, docs, etc.)  │
└──────────────────────────────────┘     └──────────────────────────────┘
```

**Key properties:**
- The server is monolithic — a complete copy of governance at a specific version.
- Clients cannot edit the server. Version upgrades = deploy a new version folder.
- Multiple clients can use the same server version independently.
- Each client decides when to upgrade. No forced pushes.

### 4.2 Two-Layer Split (v1.4 Innovation)

v1.3 is monolithic — governance rules, templates, and development artifacts live in one flat tree (mirroring ag_foundation's `docs/dev/`). Starting with v1.4, the governance system introduces a **hidden_layer / user** split:

| Layer | Contains | Who edits it |
|---|---|---|
| `hidden_layer/` | System files: templates, manuals, schemas, folder structure specs | Only GVS development (the work product) |
| `user/` | Development artifacts: INDEX files, item files, sprint docs, observations | The agent during sprint execution |

This separation is the core deliverable of v1.4. Client projects (ag_foundation, future consumers) will adopt it when they upgrade to v1.4+.

### 4.3 Folder Structure

The convergent project lives alongside consumer projects under the Agents workspace:

```
Agents/                                         # Parent workspace
├── ag_foundation/                              # CLIENT — consumer project (runtime dev)
│   ├── docs/dev/                               #   Governed by gvs_version_fixed/version1.3
│   └── src/                                    #   Work product: agent runtime code
│
└── convergent/                                 # GVS umbrella project
    │
    ├── gvs_version_fixed/                      # SERVER — frozen, read-only governance
    │   └── version1.3/                         # Monolithic: mirrors ag_foundation docs/dev/
    │       ├── additional/                     #   Reference docs, observations, plans
    │       ├── backlog/                        #   INDEX_BACKLOG.md + items/ + templates/
    │       │   ├── INDEX_BACKLOG.md
    │       │   ├── items/                      #     All historical AF item files
    │       │   └── templates/
    │       │       └── BACKLOG_ITEM_TEMPLATE.md
    │       ├── bugs/                           #   INDEX_BUGS.md + reports/ + templates/
    │       │   ├── INDEX_BUGS.md
    │       │   ├── reports/                    #     All historical bug report files
    │       │   └── templates/
    │       │       └── BUG_REPORT_TEMPLATE.md
    │       ├── decisions/                      #   INDEX_DECISIONS.md + files/ + templates/
    │       │   ├── INDEX_DECISIONS.md
    │       │   ├── files/                      #     All historical ADR files
    │       │   └── templates/
    │       │       └── ADR_TEMPLATE.md
    │       ├── foundation/                     #   Manuals, folder structures, project plans
    │       │   ├── FOUNDATION_MANUAL.md
    │       │   ├── SPRINT_MANUAL.md
    │       │   ├── FOLDER_STRUCTURE_0.3.md
    │       │   └── PROJECT_PLAN_0.2.md
    │       └── sprints/                        #   INDEX_SPRINTS.md + documentation/ + templates/
    │           ├── INDEX_SPRINTS.md
    │           ├── documentation/              #     All sprint folders (Sprint04–Sprint16)
    │           └── templates/
    │               ├── SPRINT_DESCRIPTION_TEMPLATE.md
    │               ├── SPRINT_REVIEW_TEMPLATE.md
    │               ├── PULL_REQUEST_TEMPLATE.md
    │               └── archived/
    │
    └── gvs_development/                        # CLIENT — governance development project
        └── version1.4/                         # Work product: the next governance version
            │
            ├── hidden_layer/                   # SYSTEM FILES being built (v1.4 deliverable)
            │   ├── backlog/
            │   │   └── templates/              #   New/improved backlog item template
            │   │       └── BACKLOG_ITEM_TEMPLATE.md
            │   ├── bugs/
            │   │   └── templates/              #   New/improved bug report template
            │   │       └── BUG_REPORT_TEMPLATE.md
            │   ├── decisions/
            │   │   └── templates/              #   New/improved ADR template
            │   │       └── ADR_TEMPLATE.md
            │   ├── foundation/                 #   Updated manuals, folder structure, project plan
            │   │   ├── FOUNDATION_MANUAL.md
            │   │   ├── SPRINT_MANUAL.md
            │   │   ├── FOLDER_STRUCTURE_0.3.md
            │   │   └── PROJECT_PLAN_0.2.md
            │   └── sprints/
            │       └── templates/              #   Updated sprint/PR templates
            │           ├── SPRINT_DESCRIPTION_TEMPLATE.md
            │           ├── SPRINT_REVIEW_TEMPLATE.md
            │           ├── PULL_REQUEST_TEMPLATE.md
            │           └── archived/
            │
            └── user/                           # DEVELOPMENT ARTIFACTS (GVS's own sprints)
                ├── additional/                 #   Observations, plans, free-form docs
                ├── backlog/                    #   INDEX_BACKLOG.md + items/ (GVS's own AFs)
                │   ├── INDEX_BACKLOG.md
                │   └── items/
                ├── bugs/                       #   INDEX_BUGS.md + reports/ (GVS's own bugs)
                │   ├── INDEX_BUGS.md
                │   └── reports/
                ├── decisions/                  #   INDEX_DECISIONS.md + files/ (GVS's own ADRs)
                │   ├── INDEX_DECISIONS.md
                │   └── files/
                ├── external_inputs/            #   NEW in v1.4 — consumer feedback channel
                ├── foundation/                 #   GVS dev's own project plan, folder structure
                ├── sprints/                    #   INDEX_SPRINTS.md + documentation/ (GVS sprints)
                │   ├── INDEX_SPRINTS.md
                │   └── documentation/
                └── .github/
                    └── copilot-instructions.md #   GVS-specific agent instructions
```

### 4.4 How the Server Governs Clients

The server version is deployed to each client project as a read-only reference. The agent reads governance rules from the server folder and applies them to the client's own development artifacts.

**ag_foundation** currently has governance embedded in `docs/dev/`. Post-migration, it will have a separate `gvs_version_fixed/version1.3/` folder (or the equivalent path convention decided during Sprint 17).

**gvs_development** is governed by `gvs_version_fixed/version1.3/` — the same monolithic v1.3 rules. Its work product (`hidden_layer/`) is the v1.4 governance system, which introduces the two-layer split.

### 4.5 Version Lifecycle

```
v1.3 (server, frozen)  ──governs──▶  gvs_development/version1.4/ (client)
                       ──governs──▶  ag_foundation/ (client)

When v1.4 is done:
  gvs_development/version1.4/hidden_layer/  ──deploys as──▶  gvs_version_fixed/version1.4/
  
  Then:
  v1.4 (server, frozen)  ──governs──▶  gvs_development/version1.5/ (next cycle)
                         ──governs──▶  ag_foundation/ (when it upgrades)
```

Each version N is built under governance of version N-1. No self-modification.

---

## 5. Consumer Model

All clients — including gvs_development — relate to the server identically. There is no special mode.

### 5.1 How Clients Use GVS

1. **Deploy:** Place a fixed governance version folder in the client project (e.g., `gvs_version_fixed/version1.3/`).
2. **Operate:** Run sprints. The agent reads rules, templates, and gates from the fixed version folder. Development artifacts are written to the client's own development folders.
3. **Upgrade:** Deploy a new version folder. The old version can be removed or kept for reference.

### 5.2 Consumer → Governance Feedback

Consumer observations, bugs, and feature requests flow into gvs_development via the `external_inputs/` folder (new in v1.4).

| Channel | Purpose | Destination |
|---|---|---|
| Bug reports | Rule is broken, ambiguous, or missing | `gvs_development/version1.4/user/external_inputs/` |
| Feature requests | New convention, template, gate, artifact type | Filed as AF in gvs_development |
| Observations | Structured field experience artifacts | Consumer-local, actionable items filed upstream |

### 5.3 Governance → Consumer Feedback

| Channel | Purpose |
|---|---|
| Version releases | New `gvs_version_fixed/versionX.Y/` folder deployed to client |
| Migration guides | Breaking changes explained with client update steps |
| CHANGELOG | What's new, what's fixed, what's deprecated |

### 5.4 ag_foundation as Reference Consumer

ag_foundation is the first consumer and the project where GVS was born:

- **Consumer:** Runs sprints under GVS v1.3 rules, files feedback into gvs_development
- **Reference implementation:** Proves GVS works on a real project with real agents
- **Test bed:** New GVS versions can be validated against ag_foundation's sprint history

---

## 6. Bootstrap Strategy

The server/client model eliminates the bootstrap paradox entirely. There is no self-referential loop because gvs_development never modifies the version that governs it.

### 6.1 How It Works

- `gvs_version_fixed/version1.3/` — frozen server, governs gvs_development
- `gvs_development/version1.4/` — client, produces v1.4 as its work product
- The rules for how to run sprints come from v1.3. The output of those sprints is v1.4.
- This is the same pattern as a compiler written in its own language: version N compiles version N+1.

### 6.2 Practical Bootstrap Sequence

1. **Kai (human):** Create `convergent/` folder structure, copy v1.3 server files from ag_foundation's `docs/dev/`
2. **Kai (human):** Seed `gvs_development/version1.4/` with clean INDEX files and empty item folders
3. **Kai (human):** Write copilot instructions pointing the agent at `gvs_version_fixed/version1.3/` as the governance source
4. **Agent:** Execute GVS Sprint 1 governed by v1.3 — first AFs populate the `hidden_layer/` with improved system files
5. **Concurrent:** ag_foundation Sprint 17 runs independently, also governed by v1.3

### 6.3 What Kai Prepares Before the First Agent Session

| Step | Action | Owner |
|---|---|---|
| 1 | Create `convergent/` folder structure (empty dirs) | Kai |
| 2 | Copy ag_foundation `docs/dev/` → `gvs_version_fixed/version1.3/` | Kai |
| 3 | Seed system files, create clean INDEX files, write copilot instructions (AF-0139) | Agent |
| 4 | Write GVS Sprint 1 description (scope = Phase 1 items from §7) | Kai or Agent |

After step 4, the agent opens the project and executes Sprint 1. Everything from that point is governed.

---

## 7. Phased Roadmap

### Phase 0 — Extraction & Seed (Before GVS Sprint 1)

**Goal:** Folder structure exists, server populated, development scaffolded.

- [ ] Kai: Create `convergent/` folder structure (empty dirs)
- [ ] Kai: Copy ag_foundation `docs/dev/` → `gvs_version_fixed/version1.3/`
- [ ] **AF-0139:** Agent seeds `hidden_layer/` with v1.3 system files, creates clean INDEX files in `user/`, writes copilot instructions
- [ ] Write GVS Sprint 1 description

### Phase 1 — v1.4 Development (GVS Sprints 1–3)

**Goal:** v1.4 ships with the hidden_layer/user split, clean INDEX files, and external_inputs channel.

- [ ] Implement hidden_layer/user folder structure in governance spec
- [ ] Clean up INDEX files (no ag_foundation-specific content)
- [ ] Create CHANGELOG (retroactive v1.0–v1.3 entries)
- [ ] Fix BUG-0026 (PR template version gap)
- [ ] Codify versioning conventions (from S16_OBSERVATIONS §3)
- [ ] Codify scope change protocol (from S16_OBSERVATIONS §5)
- [ ] Add phase-anchored approval gates to SPRINT_MANUAL
- [ ] Add `external_inputs/` folder specification
- [ ] Write CONSUMER_QUICKSTART guide
- [ ] Write migration guide: v1.3 → v1.4
- [ ] Deploy v1.4 to `gvs_version_fixed/version1.4/`

### Phase 2 — Adoption & Maturity (GVS Sprints 4+)

**Goal:** ag_foundation upgrades to v1.4. Second consumer validates portability.

- [ ] ag_foundation upgrades from v1.3 to v1.4
- [ ] Portable governance tests (INDEX schema, template compliance, folder structure)
- [ ] Multi-consumer validation (second project adopts GVS)
- [ ] Scaffold generator (`gvs init`)
- [ ] Upgrade tooling (`gvs upgrade`)
- [ ] Agent-agnostic instructions (not Copilot-specific)

### Phase 3 — Runtime & Abstraction (Future)

**Goal:** GVS becomes a tool, not just a file collection.

- [ ] GVS runtime CLI (`gvs verify`, `gvs gate`, `gvs close`) — programmatic governance enforcement
- [ ] Pluggable verification passes — replace hardcoded pytest/ruff with project-type-appropriate checks
- [ ] Non-coding project support — governance for docs-only, design, research projects
- [ ] gvs_development gets its own CI gate via portable governance tests (dogfooding)

**Note:** A GVS runtime reintroduces the bootstrap paradox at the tooling layer — the runtime code is testable with pytest, so gvs_development becomes a hybrid (docs + code) project. The server/client architecture still holds, but the development project is no longer purely docs.

---

## 8. Success Criteria

| Criterion | Measured By |
|---|---|
| Self-governing | GVS Sprint 1 completed under v1.3 rules |
| v1.4 ships | `hidden_layer/user` split implemented, deployed to `gvs_version_fixed/version1.4/` |
| ag_foundation decoupled | ag_foundation runs with GVS as separate fixed-version folder |
| Clean INDEX files | GVS development INDEX files contain zero ag_foundation-specific content |
| Consumer feedback works | At least 1 bug or feature request flows via `external_inputs/` |
| Portable | A second project can bootstrap from v1.4 |

---

## 9. Open Decisions

1. **Git strategy:** Single repo for convergent/ or separate repos for server/development?
2. **Server deployment to ag_foundation:** How does ag_foundation receive its `gvs_version_fixed/` folder? Manual copy? Symlink?
3. **Testing framework:** Reuse pytest? Standalone linter? Both?
4. **GVS sprint cadence:** Same cadence as ag_foundation, or independent?
5. **Retroactive CHANGELOG depth:** Document v1.0–v1.3 from memory, or start clean at v1.3?
6. **Copilot instructions and vendor specificity:** `.github/copilot-instructions.md` is a VS Code / GitHub Copilot feature — convenient but vendor-specific. Open questions:
    - **Vendor lock-in:** GVS should not depend on a single AI tooling vendor. But copilot-instructions are currently the most practical way to give agents persistent workspace rules. Should GVS standardize on a vendor-neutral format and treat copilot-instructions as one possible delivery mechanism?
    - **Composition:** How do GVS base instructions compose with client-specific instructions? Does GVS ship a fragment clients include, or do clients write their own referencing GVS rules?
    - **Multi-workspace consistency:** ag_foundation and convergent/gvs_development both need copilot-instructions that work without contradicting each other. The governance references must point to the correct paths in each workspace.
    - **Near-term requirement:** For Sprint 17 / GVS Sprint 1, copilot-instructions must work on both sides (ag_foundation pointing to its local governance docs, convergent pointing to `gvs_version_fixed/version1.3/`) without conflict. Solve the pragmatic case first, design the general solution later.
7. **external_inputs/ format:** Free-form files? Structured template? What metadata is required?
8. **Verification gap:** gvs_development has no CI gate (no source code). Options: (a) skip CI passes, (b) test against ag_foundation as harness, (c) build portable governance tests. Option (c) recommended — creates gvs_development's own test suite.
9. **Project-type scope:** Should GVS support non-coding projects? If yes, verification passes must be pluggable (not hardcoded pytest/ruff).
10. **GVS runtime (Phase 3):** When to introduce `gvs verify` / `gvs gate` CLI tooling? This makes gvs_development a hybrid (docs + code) project and partially reintroduces the bootstrap paradox at the tooling layer.
11. **Client version upgrade path:** v1.3 and v1.4 have fundamentally different folder structures (v1.3 = monolithic flat `docs/dev/`, v1.4 = `hidden_layer/` + `user/` split). When a client like ag_foundation wants to upgrade from v1.3 → v1.4, how does that work cleanly? Key sub-questions:
    - **Migration tooling:** Is there a `gvs upgrade` command, a migration script per version pair, or a manual runbook?
    - **Content mapping:** Which v1.3 files map to `hidden_layer/` vs `user/` in v1.4? Who decides — the server ships a mapping, or the client figures it out?
    - **In-flight work:** Can a client upgrade mid-sprint, or only between sprints?
    - **Backward compatibility:** Must v1.4 server still accept v1.3-structured clients, or is upgrade mandatory?
    - **Rollback:** If the upgrade breaks something, can the client revert to v1.3 cleanly?
    - **Testing:** How does the client verify the upgrade succeeded? Governance test suite from v1.4 should validate the new structure.
    - **Precedent:** This is the FIRST version transition — whatever we do for v1.3→v1.4 sets the pattern for all future upgrades. Design it deliberately.

---

## 10. Immediate Next Steps

1. **Complete S16 review Section B** — prerequisite for sprint close
2. **Close Sprint 16** — all S16 work must be committed and closed before extraction
3. **Kai: Create convergent/ folder structure + copy v1.3 server** — manual step
4. **AF-0139: Seed gvs_development/version1.4/** — agent populates hidden_layer/, clean INDEX files, copilot instructions
5. **Write GVS Sprint 1 description** — scope from Phase 1 items in §7
6. **Agent: Execute GVS Sprint 1** — first governed sprint under v1.3 rules
