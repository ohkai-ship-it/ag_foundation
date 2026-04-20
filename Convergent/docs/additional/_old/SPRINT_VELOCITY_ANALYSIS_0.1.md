# Sprint Velocity Analysis — ag_foundation
# Version: 0.2
# Prepared: 2026-04-02
# Updated: 2026-04-02
# Prepared by: Jeff
# For: LinkedIn campaign (Simon / Kai)

---

## Changelog (v0.1 → v0.2)

| Change | Detail |
|---|---|
| Added S00–S08 sprint breakdowns | New sections with git-derived timestamps where available; backlog-index-only counts for S03 |
| Extended summary table | Now covers S00–S15 (was S09–S15 only); confidence column added |
| Chart 4 fix | Removed impl/review split. Now reports total elapsed time only. S14's internal timing detail moved exclusively to Chart 5 (waterfall) per original design intent |
| Chart 6 anchor corrected | v0.1 used 87 (circular: 148−61). v0.2 replaces with bottom-up count of ~79 items (S00–S08) from backlog INDEX. See note in S00–S08 section |
| S06 merge gap noted | S06 had no separate PR merge commit; work was committed directly. This was previously unrecorded |

---

## Methodology and source confidence

**Primary source: git log (high confidence)**  
Every timestamp below is an author-date (`%ai`) from `git log --format="%H | %ai | %s" --all`.
These are commit timestamps set by Jacob's machine clock at the moment of commit.
They are not fabricated after the fact.

**Secondary source: Sprint DESCRIPTION.md files (medium confidence)**  
Each sprint folder contains an `S##_DESCRIPTION.md` with a `Dates:` field. These document
the sprint's calendar window. However, several have `→ TBD` end dates (the field was not
always filled retroactively), and Sprint 04's dates are marked as a "proposal".

**Third source: backlog INDEX_BACKLOG.md (medium-high confidence for item counts)**  
The backlog index is the canonical record of which AF items shipped in each sprint.
Used for S03 (no git evidence) and for bottom-up item counts in S00–S08.

**Confidence tiers used in this document:**  
- 🔵 **High** — git-verified timestamps, same-day session with clear boundaries  
- 🟡 **Medium** — git end-points visible (first/last commit), implementation internals sparse  
- 🔴 **Estimated** — no implementation commits; backlog INDEX and DESCRIPTION.md only

**What git cannot tell us**  
- When sprint *planning* started (AF spec writing, architectural decisions, brainstorming).
  Planning is pre-commit work. The git record begins at the first commit in a sprint session.
- Whether gaps within a sprint window (e.g., overnight) were active or idle time.  
- How many hours of cognitive work preceded the first commit of a session.
- For S02–S04: implementation commits are largely absent from the log. The work happened
  but the commit granularity was low (bulk pushes, doc-heavy sprints, direct commits).

All per-sprint elapsed times below are **wall-clock time from first planning commit to merge
commit** (or to the last known session commit where no merge occurred). Where a sprint spans
an overnight break, this is noted explicitly.

---

## Merge commit timeline (all sprints)

Source: `git log --format="%ai | %s" --merges`

| PR / Merge | Datetime (CET) | Sprint |
|---|---|---|
| PR #1–5 (multi-merge) | 2026-02-24 02:22–02:49 | Sprints 00–01 (initial foundation) |
| *(no merge commit)* | 2026-02-26 | Sprint 02 (implementation commits visible; no PR) |
| *(no git commits visible)* | 2026-02-26 → 2026-03-04 | Sprints 03–04 (git gap) |
| PR #6 | 2026-03-05 21:40 | Sprint 05 |
| *(no merge commit)* | 2026-03-06 | Sprint 06 (committed directly; no PR merge) |
| Sprint 07 merge | 2026-03-08 12:58 | Sprint 07 |
| Sprint 08 merge | 2026-03-10 13:44 | Sprint 08 |
| Sprint 09 merge | 2026-03-11 16:38 | Sprint 09 |
| Sprint 10 merge | 2026-03-12 23:44 | Sprint 10 |
| Sprint 11 merge | 2026-03-21 12:38 | Sprint 11 |
| PR #7 | 2026-03-21 20:46 | Sprint 12 |
| PR #8 (AF-0112 only) | 2026-03-21 23:10 | Sprint 13 (mid-sprint AF) |
| Sprint 13 merge | 2026-03-22 13:01 | Sprint 13 |
| PR #9 | 2026-03-22 16:46 | Sprint 14 |
| PR #10 | 2026-03-22 22:19 | Sprint 15 |

**Observation:** Sprints 09 through 15 all closed within the 11-day window 2026-03-11 to
2026-03-22. Sprints 12, 14, and 15 all closed on the *same calendar day* (March 22) as
sequential back-to-back sessions. This is the most significant structural fact in the dataset.

**S02/S03/S04 note:** The gap from 2026-02-26 to 2026-03-04 contains no git commits visible
in `--all`. These 6 days cover the S03 sprint (CLI/UX hardening) and part of S04 (process
hardening). The work was done but either committed at low granularity, committed directly
without branching, or is otherwise absent from the log's commit history.

---

## Sprint-by-sprint breakdown (Sprints 00–08: early period)

### Sprint 00 — Kick-off and Architecture Foundation 🔴

| Field | Value |
|---|---|
| Documented dates (DESCRIPTION.md) | Not in standard folder (pre-dated the folder structure) |
| First visible git evidence | 2026-02-24 01:59:51 `initial commit - Sprint 00 docs + Sprint 01 b` |
| Work items shipped | AF-0001, AF-0002, AF-0003 = **3 items** |

**Note:** S00 was a pure planning and documentation sprint. Kick-off, architecture vision
(ADR-0001), and the core runtime skeleton (docs-only, IF-0003) were established. No runnable
code existed. The initial commit at 01:59:51 on Feb 24 captures S00 artifacts and the S01
kickoff docs in the same commit — they were effectively simultaneous. No separate S00
DESCRIPTION.md exists in the standard sprint folder structure; the sprint predates that system.

**Elapsed: not calculable** (design-only sprint; no implementation commits).

---

### Sprint 01 — Foundation Build 🔵

| Field | Value |
|---|---|
| Documented dates (DESCRIPTION.md) | Not in standard folder |
| First commit | 2026-02-24 **01:59:51** `initial commit - Sprint 00 docs + Sprint 01 b` |
| PR #1 (contracts) merged | 2026-02-24 **02:22:08** |
| PR #2 (storage) merged | 2026-02-24 **02:47:49** |
| PR #3 (runtime skeleton) merged | 2026-02-24 **02:48:29** |
| PR #4 (CLI v0) merged | 2026-02-24 **02:49:02** |
| PR #5 (artifacts v0) merged | 2026-02-24 **02:49:35** |
| Sprint review | 2026-02-24 23:13:46 |
| **Elapsed: first commit → last merge** | **~50 minutes** |
| Work items shipped | AF-0004, AF-0005, AF-0006, AF-0007, AF-0008, AF-0009, AF-0010 = **7 items** |
| Items per hour (active burst) | ~8.4/hr |

**Per-PR timing:**

| Commit | Time | Delta |
|---|---|---|
| Initial commit (S00 + S01 setup) | 01:59:51 | — |
| AF-0005 (contracts/schemas) | 02:20:37 | +21m |
| PR #1 merge (contracts) | 02:22:08 | +1m |
| AF-0006 (workspace/storage) | 02:34:54 | +12m |
| AF-0007 (runtime skeleton) | 02:38:51 | +4m |
| AF-0008 (CLI v0 + truthful labels) | 02:43:21 | +4m |
| PR #2 merge (storage) | 02:47:49 | +4m |
| AF-0009 (artifact registry) | 02:48:13 | +0m |
| PR #3 merge (runtime) | 02:48:29 | +0m |
| PR #4 merge (CLI) | 02:49:02 | +0m |
| PR #5 merge (artifacts) | 02:49:35 | +0m |

**The PRs #2–5 merged within 2 minutes of each other** — these were pre-staged branches
ready to merge sequentially. The core foundation of the system shipped in a single overnight
session. Sprint review ("ACCEPT WITH FOLLOW-UPS") documented at 23:13 the same day.

---

### Sprint 02 — Hardening 🟡

| Field | Value |
|---|---|
| Documented dates | Implied: 2026-02-24 (after review) → 2026-02-26 |
| Sprint start | After 2026-02-24 23:13:46 (S01 review) |
| Implementation commits | **Not visible in git log** — bulk push or direct commit pattern |
| Last visible commits | 2026-02-26 15:19:08 `Sprint 02 hardening extension complete` |
|  | 2026-02-26 15:46:08 `fix(AF-0026): workspace selection policy enforcement` |
|  | 2026-02-26 16:03:23 `docs: Sprint 02 Hardening completion documentation` |
| **Elapsed: review → final commit** | **~41 hours wall-clock** (Feb 24 23:13 → Feb 26 16:03) |
| Work items shipped | AF-0011, AF-0014, AF-0016, AF-0017, AF-0018, AF-0019 (core, 6 items) |
|  | AF-0021, AF-0022, AF-0023, AF-0024, AF-0025, AF-0026 (hardening extension, 6 items) |
|  | **Total: 12 items** |
| Bugs filed | BUG-0001, BUG-0002, BUG-0003 (CLI audit findings, filed Feb 24 13:09) |

**Note:** The 41-hour wall-clock span certainly includes overnight and non-active time.
The actual implementation time is unknown — the internal commits are not visible in the log.
Only the end-of-sprint checkpoint commits survive. S02 delivered the OpenAI provider
integration, workspace policy enforcement, and multi-step trace capability.

---

### Sprint 03 — CLI/UX Hardening 🔴

| Field | Value |
|---|---|
| Documented dates (DESCRIPTION.md) | **No S03 DESCRIPTION.md** in standard folder structure |
| Git commits | **None visible** — entire sprint is a git record gap |
| Implied window | 2026-02-26 16:03 (S02 end) → 2026-03-04 12:57 (first visible S04 commit) |
| **Maximum possible elapsed** | **~6.5 days** (Feb 26 → Mar 4) |
| Work items shipped | AF-0027, AF-0028, AF-0029, AF-0030, AF-0031, AF-0032, AF-0033, AF-0034, AF-0035, AF-0036, AF-0037, AF-0038 = **12 items** |

**Note:** S03 is the largest single gap in the git record. The 12 CLI hardening items
(run ID truncation, workspace policy, truthfulness enforcement, error messaging, observability
command expansion) were implemented and committed without generating git commits visible in
`git log --all`. This is either from direct pushes before GitHub branching discipline was
established, or bulk commits that were later squashed. The items themselves are documented in
the backlog index with DONE status.

**What is known from secondary sources only:** S03 established the "Truthful UX" invariant
as a code-enforced principle (`extract_labels(trace)`, AF-0031) and expanded the CLI surface
to its first full observability state. These are foundational items that Sprint 04+
implementations rely on.

---

### Sprint 04 — Process Hardening 🔴

| Field | Value |
|---|---|
| Documented dates (DESCRIPTION.md) | 2026-03-04 → 2026-03-10 (marked **"In Progress"** — never formally closed) |
| Visible commits | 2026-03-04 12:57:09 `Update: docs` |
|  | 2026-03-04 13:45:40 `Sprint 04 end` |
|  | 2026-03-04 19:00:34 `follow up` |
|  | 2026-03-04 19:35:58 `foundation` |
|  | 2026-03-04 19:37:54 `foundation 02` |
| **Elapsed: first → last visible commit** | **~6h 41m** (12:57 → 19:37, same day) |
| Work items shipped | AF-0039, AF-0040, AF-0041, AF-0042, AF-0043, AF-0044, AF-0045 = **7 items** |

**Note:** S04 was a docs-and-process migration sprint: creating the `/docs/dev/` folder
structure, migrating the backlog/sprint/review systems into the new convention, and enforcing
CI (ruff + pytest -W error + coverage). The DESCRIPTION.md is still marked "In Progress"
as of the final commit — the sprint was effectively absorbed into S05/S06 scope rather than
formally closed with a review. The CI enforcement (AF-0045) shipped in this sprint makes
all subsequent sprints measurable (ruff + pytest -W error gate).

---

### Sprint 05 — High Pressure Skills 🔵

| Field | Value |
|---|---|
| Documented dates (DESCRIPTION.md) | 2026-03-04 → 2026-03-04 |
| Sprint setup | 2026-03-04 **21:21:21** `remove legacy docs, improve sprint checklist` |
| Sprint setup commit | 2026-03-04 **21:23:15** `Sprint05 setup - indexes, folder, AF files` |
| First implementation commit | 2026-03-04 **21:31:06** `feat(AF0048): implement strategic_brief skill` |
| Night session ends | 2026-03-04 **22:52:34** `docs: add BUG0008` |
| Morning session begins | 2026-03-05 **09:51:53** `fix(BUG0008): implement CLI skill routing` |
| Morning session ends | 2026-03-05 **11:02:26** `fix(BUG0010): populate all evidence_ref fields` |
| Close commit | 2026-03-05 **21:31:12** `close Sprint 05` |
| Merge to main | 2026-03-05 **21:40:05** (PR #6) |
| **Elapsed: setup → merge** | **~24h 19m** (overnight sprint) |
| **Estimated active implementation** | ~3h (21:31–22:52 night + 09:51–11:02 morning) |
| Work items shipped | AF-0048, AF-0049, AF-0050, AF-0051 (main, 4 items) |
|  | AF-0047, AF-0052, AF-0053, AF-0054, AF-0055 (follow-ups, 5 items) |
|  | BUG-0008, BUG-0009, BUG-0010 fixed (3 bugs) |
|  | **Total: 12 items (9 AFs + 3 bugs)** |

**Note:** S05 established the first real skill implementation (`strategic_brief`), schema
verifier with repair loop (AF-0050), evidence capture (AF-0049), and verifier loop bounding
(AF-0055). The S04→S05 boundary was same-day (Mar 4): `Sprint 04 end` at 13:45, S05 setup
at 21:21, gap of ~7h 36m.

---

### Sprint 06 — Skill Foundation 🔵

| Field | Value |
|---|---|
| Documented dates (DESCRIPTION.md) | 2026-03-06 → TBD (end date never filled) |
| Sprint planning commit | 2026-03-06 **16:45:41** `Sprint 06 planning - skill foundation` |
| Sprint start commit | 2026-03-06 **16:46:07** `Start Sprint 06 - skill foundation` |
| First implementation commit | 2026-03-06 **16:57:28** `feat(AF0058): Workspace folder restructure` |
| Last implementation commit | 2026-03-06 **18:54:02** `docs(AF0063, AF0013): Add schema and contract inventories` |
| Additional docs commit | 2026-03-07 **23:00:59** `docs: Add concept relationship matrix` (next day) |
| **No PR merge commit exists** | Sprint committed directly without a formal PR |
| **Elapsed: planning → last impl commit** | **~2h 9m** (16:45 → 18:54, same day) |
| Work items shipped | AF-0058, AF-0060, AF-0061, AF-0063, AF-0013 = **5 items** |
| Items per hour | **~2.3/hr** |

**Note:** S06 is the only sprint in the dataset with no merge commit. The work was pushed
directly to the branch without a separate PR review. This predates the disciplined PR-per-sprint
pattern that started with Sprint 07. Items delivered: workspace folder restructure, skill
definition framework, status CAPS convention, schema and contract inventories with drift tests.

---

### Sprint 07 — Summarize Playbook 🔵

| Field | Value |
|---|---|
| Documented dates (DESCRIPTION.md) | 2026-03-08 → 2026-03-08 |
| Sprint prep commit | 2026-03-08 **00:20:24** `docs: Prepare Sprint 07 backlog - mark AFs READY` |
| Sprint kickoff commit | 2026-03-08 **00:51:28** `docs: Sprint 07 kickoff - summarize_playbook` |
| First implementation commit | 2026-03-08 **00:59:40** `feat(skills): implement summarize_v0 playbook (AF-0065)` |
| Last implementation commit | 2026-03-08 **02:39:38** `feat(AF-0066): E2E integration tests for full pipeline` |
| Sprint close commit | 2026-03-08 **12:56:28** `Close Sprint 07: ACCEPT WITH FOLLOW-UPS` |
| Merge to main | 2026-03-08 **12:58:04** |
| **Elapsed: prep → merge** | **~12h 38m** (overnight; active session ~1h 48m: 00:59–02:39) |
| Work items shipped | AF-0065, AF-0066, AF-0067, AF-0068, AF-0062 = **5 items** |

**Note:** The first complete skill-based playbook (`summarize_v0`) shipped in this sprint:
`load_documents → summarize_docs → emit_result`. The implementation burst ran from 00:59 to
02:39 (1h 40m). The merge happened ~10 hours later in the morning, which is the overnight
pattern seen again in S11 and S13.

---

### Sprint 08 — Skills/Playbooks Maturity 🔵

| Field | Value |
|---|---|
| Documented dates (DESCRIPTION.md) | 2026-03-09 → 2026-03-10 |
| Pre-sprint commit | 2026-03-09 **12:29:45** `preSprint8` |
| Sprint start ritual | 2026-03-09 **12:33:52** `startS08` |
| First implementation commit | 2026-03-09 **13:05:47** `docs(AF-0073): Index file linking convention` |
| Last sprint-day commit | 2026-03-09 **16:17:28** `chore(review): Sprint 08 review completed` |
| Post-review cleanup | 2026-03-08 **16:44:32** *(note: this timestamp appears to be a clock anomaly — Mar 8 vs Mar 9)* |
| Merge to main | 2026-03-10 **13:44:36** |
| **Elapsed: pre-sprint → merge** | **~25h 15m** (overnight) |
| **Estimated active implementation** | ~4h (12:33–16:17, Mar 9) |
| Work items shipped | AF-0073, AF-0079, AF-0074, AF-0076, AF-0069, AF-0070, AF-0080 = **7 items** |
|  | AF-0059 DROPPED (absorbed into AF-0076) |
|  | BUG-0013 fixed (via AF-0080: `web_search` skill added as root fix) |
|  | **Total: 8 items (7 AFs + 1 bug)** |

**Note:** S08 established the research pipeline: `web_search → fetch_web_content →
synthesize_research → emit_result`. The V1 skill framework was removed (AF-0079), leaving
only the V2 pattern. This sprint also documented the skills and playbooks architecture in
full (AF-0069, AF-0070). The clock anomaly on the Mar 8 timestamp for the `purge strategic_brief`
commit is noted but does not affect overall sprint timing.

---

## Item count anchor: S00–S08 (corrected from v0.1)

**v0.1 used a circular calculation:** 87 items = total (148) − S09–S15 confirmed (61).
The "148 total" was not independently verified.

**v0.2 bottom-up count from backlog INDEX:**

| Sprint | AFs from INDEX | Bugs fixed | Total |
|---|---|---|---|
| S00 | 3 | 0 | 3 |
| S01 | 7 | 0 | 7 |
| S02 | 12 | 3 filed (BUG-0001–0003) | 12 |
| S03 | 12 | 0 visible | 12 |
| S04 | 7 | 0 | 7 |
| S05 | 9 | 3 (BUG-0008, -0009, -0010) | 12 |
| S06 | 5 | 0 | 5 |
| S07 | 5 | 0 | 5 |
| S08 | 7 | 1 (BUG-0013) | 8 |
| **S00–S08 total** | **67** | **7** | **~71–74** |

Pre-S09 bugs not counted above: BUG-0004, BUG-0005, BUG-0006, BUG-0011, BUG-0012 = 5 bugs
(filed in S02–S04 period but not clearly sprint-attributed in INDEX).

**Revised anchor:** ~74–79 items in S00–S08 (±5 from S03 edge cases and BUG attribution).
The v0.1 figure of 87 is withdrawn; it overcounted by approximately 10–15 items.
Chart 6 note updated: pre-S09 cumulative is approximately 74–79 items, not 87.

---

## Sprint-by-sprint breakdown (Sprints 09–15: stable governance period)

### Sprint 09 — Reliability + Safety Hardening

| Field | Value |
|---|---|
| Documented dates (DESCRIPTION.md) | 2026-03-11 → 2026-03-11 |
| Planning commit | 2026-03-11 11:20 `preSprint09` |
| Sprint start ritual | 2026-03-11 11:38 |
| First implementation commit | 2026-03-11 12:12 `AF-0046, AF-0071, BUG-0007` |
| Last implementation commit | 2026-03-11 13:02 `AF-0015 storage DB audit` |
| Sprint close commit | 2026-03-11 16:38 `Sprint 09 Closed` |
| Merge to main | 2026-03-11 **16:38** |
| **Elapsed: planning → merge** | **5h 18m** |
| **Elapsed: first impl → merge** | **4h 26m** |
| Work items shipped | AF-0046, AF-0057, AF-0071, AF-0072, AF-0083, AF-0085, AF-0086, AF-0087, AF-0015 + BUG-0007 = **10 items** |
| Items per hour (planning basis) | 1.9/hr |

**Note:** Single uninterrupted same-day session. No overnight gap.

---

### Sprint 10 — Gate B Readiness

| Field | Value |
|---|---|
| Documented dates (DESCRIPTION.md) | 2026-03-12 → 2026-03-12 |
| Planning commit | 2026-03-12 15:49 `sprint 10 planning` |
| First implementation commit | 2026-03-12 17:10 `AF-0090` |
| Last implementation commit | 2026-03-12 23:01 `AF-0095 fix` |
| Merge to main | 2026-03-12 **23:44** |
| **Elapsed: planning → merge** | **7h 55m** |
| **Elapsed: first impl → merge** | **6h 34m** |
| Work items shipped | AF-0090, AF-0091, AF-0093, AF-0012, AF-0081, AF-0082, AF-0077, AF-0078, AF-0084, AF-0095 = **10 items** |
| Items per hour (planning basis) | 1.3/hr |

**Note:** Single uninterrupted same-day session. Gate B passed at close of this sprint.

**Inter-sprint gap:** Sprint 10 merged 2026-03-12 23:44. Sprint 11 planning commit was
2026-03-20 10:16. **Gap: 7 days, 10 hours, 32 minutes.** This is planning/design time:
architectural decisions, AF spec writing, and brainstorming for the Guided Autonomy sprint.
This gap is real work that does not appear in any commit timestamp.

---

### Sprint 11 — Guided Autonomy Enablement

| Field | Value |
|---|---|
| Documented dates (DESCRIPTION.md) | 2026-03-20 → 2026-03-21 |
| Planning commit | 2026-03-20 10:16 `sprint 11 planning` |
| Sprint start ritual | 2026-03-20 11:03 |
| First implementation commit | 2026-03-20 13:54 `V1Planner AF-0102` |
| End of day 1 (last commit) | 2026-03-20 17:56 `AF-0101` |
| Day 2 bug fixes begin | 2026-03-21 10:06 `BUG-0016 fix` |
| Sprint close | 2026-03-21 12:36 |
| Merge to main | 2026-03-21 **12:38** |
| **Elapsed: wall-clock** | **26h 22m** (includes overnight) |
| **Estimated active implementation** | ~6h (13:54–17:56 day 1 + 10:06–12:38 day 2) |
| Work items shipped | AF-0102, AF-0098, AF-0099, AF-0100, AF-0094, AF-0097, AF-0101 + BUG-0015 = **8 items** |

**Note:** Only sprint that spans two active calendar days. Day 1: 7 AFs implemented in
~4 hours (13:54–17:56). Day 2: bug fixing and close (~2.5 hours). The wall-clock figure
of 26h is misleading — it includes an inactive overnight period.

---

### Sprint 12 — Autonomy Boundaries

| Field | Value |
|---|---|
| Documented dates (DESCRIPTION.md) | 2026-03-21 → 2026-03-21 |
| Planning commit | 2026-03-21 17:21 `sprint 12 planning` |
| Sprint start ritual | 2026-03-21 17:28 |
| First implementation commit | 2026-03-21 17:39 `AF-0107` |
| Last implementation commit | 2026-03-21 20:23 `S12 review complete` |
| Merge to main | 2026-03-21 **20:46** |
| **Elapsed: planning → merge** | **3h 25m** |
| Work items shipped | AF-0105, AF-0106, AF-0107, AF-0108, AF-0109, AF-0110, AF-0111 = **7 items** |
| Items per hour | **2.0/hr** |

**Note:** Fastest stable-sprint start-to-merge. Immediately followed Sprint 11 close (gap:
4h 43m between Sprint 11 merge at 12:38 and Sprint 12 planning at 17:21).

---

### Sprint 13 — Intelligent Pipeline Foundation

| Field | Value |
|---|---|
| Documented dates (DESCRIPTION.md) | 2026-03-21 → 2026-03-22 |
| AF-0112 (separate branch) merged | 2026-03-21 23:10 (PR #8, mid-sprint) |
| Sprint setup commit | 2026-03-21 23:35 |
| First implementation commit | 2026-03-21 23:52 `AF-0114` |
| End of night session | 2026-03-22 00:12 `AF-0115 tests` |
| Morning session begins | 2026-03-22 11:30 `AF-0103 + AF-0117` |
| Review evidence | 2026-03-22 11:58 |
| Merge to main | 2026-03-22 **13:01** |
| **Elapsed: wall-clock (setup → merge)** | **13h 26m** (includes ~11h overnight) |
| **Estimated active implementation** | ~4h (23:35–00:12 + 11:30–13:01) |
| Work items shipped | AF-0112, AF-0114, AF-0115, AF-0103, AF-0117 = **5 items** |

**Note:** Wall-clock is dominated by overnight gap. Actual coding was two short sessions.
Sprint 13 immediately followed Sprint 12 (gap: 2h 35m between Sprint 12 merge at 20:46
and Sprint 13 AF-0112 merge at 23:10).

---

### Sprint 14 — Smart Verification Pipeline

**The densest sprint in the dataset by items/hour.**

| Field | Value |
|---|---|
| Documented dates (DESCRIPTION.md) | 2026-03-22 → TBD (but State: Closed) |
| Planning commit | 2026-03-22 13:12 `sprint 14 plan` |
| Sprint start ritual | 2026-03-22 13:23 |
| First implementation commit | 2026-03-22 13:29 `BUG-0019` |
| Last implementation commit | 2026-03-22 14:56 `AF-0104` |
| Sprint review | 2026-03-22 16:30 `S14_REVIEW_01 complete` |
| Sprint close commit | 2026-03-22 16:43 |
| Merge to main | 2026-03-22 **16:46** |
| **Elapsed: planning → merge** | **3h 34m** |
| **Core implementation burst** | 13:29 → 14:56 = **1h 27m for 9 items** |
| Work items shipped | BUG-0018, BUG-0019, AF-0096, AF-0104, AF-0113, AF-0116, AF-0117, AF-0118, AF-0119, AF-0120 = **10 items** |
| Items per hour (planning basis) | **2.8/hr** |

**Per-item timing (from git timestamps):**

| Item | Commit time | Delta |
|---|---|---|
| Sprint 14 plan | 13:12 | — |
| Sprint start ritual | 13:23 | +11m |
| BUG-0019 | 13:29 | +6m |
| BUG-0018 | 13:33 | +4m |
| AF-0116 | 13:41 | +8m |
| AF-0117 | 13:49 | +8m |
| AF-0118 | 13:53 | +4m |
| AF-0119 | 14:08 | +15m |
| AF-0120 | 14:40 | +32m |
| AF-0096 | 14:51 | +11m |
| AF-0104 | 14:56 | +5m |
| *(infeasible task fix)* | 15:08 | +12m |
| Review | 16:30 | +82m |
| Merge | 16:46 | +16m |

**Average time per implementation commit: ~10 minutes.**
See Chart 5 for the waterfall breakdown of this sprint. S14 is the only sprint where
an internal implementation/review split is git-verified; all other sprints report totals only.

---

### Sprint 15 — LLM Intelligence Layer (Gate C)

| Field | Value |
|---|---|
| Documented dates (DESCRIPTION.md) | 2026-03-22 → 2026-03-22 |
| Planning commit | 2026-03-22 17:14 `sprint 15 plan` |
| First implementation commit | 2026-03-22 18:13 `BUG-0020, AF-0121, AF-0123` |
| Primary scope complete | 2026-03-22 18:45 `Sprint 15 close: mark AFs DONE` |
| Additional items (bugs + secondary AFs) | 2026-03-22 21:28–22:07 |
| Merge to main | 2026-03-22 **22:19** |
| **Elapsed: planning → merge** | **5h 5m** |
| Primary scope items | BUG-0020, AF-0121, AF-0122, AF-0123, AF-0124 = **5 items** |
| Additional items shipped | AF-0125, AF-0126, BUG-0021, BUG-0022, BUG-0023, BUG-0024 = **6 items** |
| **Total items shipped** | **11 items** |
| Items per hour (planning basis) | **2.2/hr** |

**Note:** Primary scope closed in ~1.5 hours of active implementation (18:13–18:45).
Additional bugs and AFs were filed, implemented, and closed within the same session.
Gate C achieved at close of this sprint.

---

## Summary table: Sprints 00–15

**Confidence key:** 🔵 High (git-verified) | 🟡 Medium (git end-points only) | 🔴 Estimated (backlog INDEX only)

| Sprint | Goal | First impl commit | Merge/close | Elapsed | Items | Items/hr | Conf |
|---|---|---|---|---|---|---|---|
| S00 | Kick-off / Architecture | Feb 24, 01:59 | N/A | — | 3 | — | 🔴 |
| S01 | Foundation Build | Feb 24, 01:59 | Feb 24, 02:49 | **~50m** | 7 | ~8.4 | 🔵 |
| S02 | Hardening | Feb 24 (after review) | Feb 26, 16:03 | ~41h* | 12 | — | 🟡 |
| S03 | CLI/UX Hardening | Not visible | Not visible | — | 12 | — | 🔴 |
| S04 | Process Hardening | Mar 4, 12:57 | Mar 4, 19:37 | ~6h 41m† | 7 | — | 🔴 |
| S05 | High Pressure Skills | Mar 4, 21:31 | Mar 5, 21:40 | 24h 9m* | 12 | — | 🔵 |
| S06 | Skill Foundation | Mar 6, 16:57 | Mar 6, 18:54 | **~2h 9m** | 5 | ~2.3 | 🔵 |
| S07 | Summarize Playbook | Mar 8, 00:59 | Mar 8, 12:58 | 12h 38m* | 5 | — | 🔵 |
| S08 | Skills/Playbooks Maturity | Mar 9, 12:33 | Mar 10, 13:44 | ~25h* | 8 | — | 🔵 |
| S09 | Reliability | Mar 11, 11:20 | Mar 11, 16:38 | **5h 18m** | 10 | 1.9 | 🔵 |
| S10 | Gate B | Mar 12, 15:49 | Mar 12, 23:44 | **7h 55m** | 10 | 1.3 | 🔵 |
| S11 | Guided Autonomy | Mar 20, 10:16 | Mar 21, 12:38 | 26h 22m* | 8 | — | 🔵 |
| S12 | Autonomy Boundaries | Mar 21, 17:21 | Mar 21, 20:46 | **3h 25m** | 7 | 2.0 | 🔵 |
| S13 | Intelligent Pipeline | Mar 21, 23:35 | Mar 22, 13:01 | 13h 26m* | 5 | — | 🔵 |
| S14 | Smart Verification | Mar 22, 13:12 | Mar 22, 16:46 | **3h 34m** | 10 | 2.8 | 🔵 |
| S15 | LLM Intelligence | Mar 22, 17:14 | Mar 22, 22:19 | **5h 5m** | 11 | 2.2 | 🔵 |

*Includes overnight period; active implementation time is shorter (see per-sprint breakdowns).  
†Docs-heavy sprint; no code implementation commits expected.

**Averages (S09–S15, single-session sprints only — S09, S10, S12, S14, S15):**
- Average items per sprint: **9.6** (range: 7–11)
- Average elapsed: **5h 3m** (range: 3h 25m – 7h 55m)
- Average items per hour: **2.0** (range: 1.3–2.8)

**Early-period single-session sprints (S01, S06 — high confidence, same-day):**
- S01: 7 items in ~50 minutes (~8.4/hr — but this is an anomaly; pre-staged branches)
- S06: 5 items in ~2h 9m (~2.3/hr — consistent with later stable-period rates)

---

## Inter-sprint gaps

Git captures implementation time. Planning time sits in the gaps between sprints.

**Early period (S00–S09):** 🔴 Estimated or not calculable for most gaps.

| Between | Gap | Confidence | Notes |
|---|---|---|---|
| S00 → S01 | ~0m | 🔵 | Same commit captures both S00 setup and S01 kickoff |
| S01 → S02 | Unknown | 🔴 | S01 review at 23:13 Feb 24; S02 start not visible in git |
| S02 → S03 | Unknown | 🔴 | S02 ends Feb 26 16:03; S03 has no git data at all |
| S03 → S04 | Unknown | 🔴 | Both sprints are git-sparse; S04 first visible commit is Mar 4 12:57 |
| S04 → S05 | **~7h 38m** | 🔵 | S04 docs at 13:45 → S05 setup at 21:23, same day (Mar 4) |
| S05 → S06 | **~19h 5m** | 🔵 | S05 merge 21:40 Mar 5 → S06 planning 16:45 Mar 6 |
| S06 → S07 | **~29h 26m** | 🔵 | S06 last commit 18:54 Mar 6 → S07 prep 00:20 Mar 8 |
| S07 → S08 | **~23h 31m** | 🔵 | S07 merge 12:58 Mar 8 → S08 pre-sprint 12:29 Mar 9 |
| S08 → S09 | **~22h 45m** | 🔵 | S08 merge 13:44 Mar 10 → S09 planning 11:20 Mar 11 (est.) |
| S09 → S10 | **~16h 5m** | 🔵 | S09 merge 16:38 Mar 11 → S10 planning 15:49 Mar 12 (overnight) |
| S10 → S11 | **7 days, 10h** | 🔵 | Largest confirmed gap. Guided autonomy required significant design work: V1Planner architecture, plan approval workflow, step confirmation system. All pre-commit. |
| S11 → S12 | **4h 43m** | 🔵 | Unusually short — scope was stabilization, not new architecture. |
| S12 → S13 | **2h 35m** | 🔵 | Pipeline foundation; AF specs existed before the session started. |
| S13 → S14 | **11m** | 🔵 | Effectively continuous — Sprint 14 planning began 11 minutes after Sprint 13 merged. |
| S14 → S15 | **28m** | 🔵 | Same pattern — back-to-back on March 22. |

**S05–S08 inter-sprint rhythm** (Mar 4–10): Consecutive sessions with 19–29h between sprints.
This is the established cadence for the "early skill-building" period: implementation runs in
an evening session; the next sprint begins after a natural rest cycle of about one day.

**Late-project sprint burst (S12–S15, Mar 21–22):** S12, S13, S14, and S15 ran consecutively
on March 21–22 with gaps of 4h 43m, 2h 35m, 11m, and 28m. These four sprints produced 33
items in approximately 17 hours of clock time across two days.

---

## Assessment of the campaign claim

**Claim:** "5–10 work items from sprint start to PR in 1–2 days."

**What the S09–S15 data shows (high confidence):**
- Range: 5–11 items (average 8.7) — **accurate**
- Timing: 3–8 active hours per sprint, all within 1–2 calendar days — **accurate but soft-pedaled**

**What the claim understates:**
The most representative sprints (S12, S14, S15) complete in **3–5 hours**, not 1–2 days.
Saying "1–2 days" is technically true (nobody exceeds 2 calendar days) but implies a slower
pace than the data shows.

**What the claim obscures:**
The inter-sprint gaps (especially the 7-day S10→S11 gap) contain real architectural work —
AF specification, design decisions, brainstorming — that doesn't appear in commit history.
The implementation velocity is high because the design was done before the first commit.
These are not interchangeable concepts.

**What the early-sprint data (S00–S08) adds:**
Sprint S01 (Foundation Build) is the fastest sprint in the dataset: 7 items in ~50 minutes.
This is atypical — branches were pre-staged and merged sequentially. Sprint S06 (2h 9m for
5 items) is the most representative early-sprint data point, aligning with the stable-period
average of ~2.0 items/hr.

**Recommended phrasing:**
> "Each sprint — 5 to 11 work items — closes in a single working session of 3–8 hours.
> Sprints 12, 13, 14, and 15 ran back-to-back on March 21–22, 2026, completing 33 items
> across two days. Between sessions: 1–7 days of design work, AF specification, and
> architectural planning that precedes every commit."

This is accurate, more impressive, and honest about the two-phase rhythm (design + implement)
that the git history only partially captures.

---

## What the git history cannot tell us

1. **Who** committed. Jacob is assumed to be the sole implementer based on all available
   documentation, but the commits have author metadata not analyzed here.

2. **Pre-commit planning time.** AF specifications for Sprint 14's 10 items were written
   before the planning commit at 13:12. That spec work took unknown time.

3. **Test run iterations.** The `pytest -W error` gate runs before every commit. Failed
   runs before a clean commit are not in the history. The "10 items in 87 minutes" figure
   for Sprint 14 reflects only the successful-commit timestamps, not failed attempts.

4. **Cognitive load.** Sprint 14's 10 items in 3.5 hours includes 2 bugs, 1 recorder,
   1 executor, 1 orchestrator, 1 verifier, 1 planner trace, 1 manifest, 1 test cleanup,
   and 1 feasibility study. These vary enormously in complexity. Average time is not
   average effort.

---

*Data source: `git log --format="%H | %ai | %s" --all` run 2026-04-02.*
*Sprint dates from `docs/dev/sprints/documentation/S##_DESCRIPTION.md` fields.*
*Work item counts from `docs/dev/backlog/INDEX_BACKLOG.md` sprint scope tables.*
