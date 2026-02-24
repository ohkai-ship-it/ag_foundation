# Handoff — Index (ag_foundation)

This folder is the **canonical location for Jacob's (implementer) outputs**: completion notes, captured traces, and any supporting artifacts for PRs.

## Purpose
- Provide a single place for reviewers (Jeff, Kai) to find implementation evidence
- Keep PR descriptions lightweight by linking to detailed notes here
- Maintain a historical record of implementation decisions

## File Naming Convention
```
YYYY-MM-DD_AF-XXXX_<slug>.md     # Handoff/completion notes
YYYY-MM-DD_AF-XXXX_run_<id>.json # Captured RunTrace evidence (optional)
```

Examples:
- `2026-02-24_AF-0010_python-bootstrap.md`
- `2026-03-05_AF-0007_runtime-skeleton.md`
- `2026-03-05_AF-0007_run_abc123_trace.json`

## What Goes Here

### Required (for every PR)
- **Handoff note** (`.md`): Summary of what was done, test results, acceptance criteria checklist, commands to verify

### Optional (for behavior-change PRs)
- **Captured traces** (`.json`): RunTrace output from `ag runs show <run_id> --json`
- **Supporting artifacts**: Screenshots, diagrams, or other evidence

## Linking from PRs
Every PR description should include:
```markdown
## Evidence
- Handoff note: [docs/dev/handoff/YYYY-MM-DD_AF-XXXX_slug.md](link)
- Run trace: [docs/dev/handoff/YYYY-MM-DD_AF-XXXX_run_id.json](link) (if behavior change)
```

## Current Contents

| Date | AF Item | File | Description |
|------|---------|------|-------------|
| 2026-02-24 | AF-0009 | [2026-02-24_AF-0009_artifacts-v0.md](2026-02-24_AF-0009_artifacts-v0.md) | Artifact registry v0 |
| 2026-02-24 | AF-0008 | [2026-02-24_AF-0008_cli-v0-truthful.md](2026-02-24_AF-0008_cli-v0-truthful.md) | CLI v0 truthful labels |
| 2026-02-24 | AF-0007 | [2026-02-24_AF-0007_runtime-skeleton.md](2026-02-24_AF-0007_runtime-skeleton.md) | Core runtime skeleton v0 |
| 2026-02-24 | AF-0006 | [2026-02-24_AF-0006_storage-baseline.md](2026-02-24_AF-0006_storage-baseline.md) | Workspace + storage baseline |
| 2026-02-24 | AF-0005 | [2026-02-24_AF-0005_contracts.md](2026-02-24_AF-0005_contracts.md) | Contracts: TaskSpec + RunTrace + Playbook |
| 2026-02-24 | AF-0004 | [2026-02-24_AF-0004_sprint-os-hygiene.md](2026-02-24_AF-0004_sprint-os-hygiene.md) | Sprint OS hygiene (docs/pointers) |
| 2026-02-24 | AF-0010 | [2026-02-24_AF-0010_python-bootstrap.md](2026-02-24_AF-0010_python-bootstrap.md) | Python project bootstrap |
| 2026-02-23 | — | [ONBOARDING_SUMMARY_JACOB.md](ONBOARDING_SUMMARY_JACOB.md) | Jacob onboarding notes |
