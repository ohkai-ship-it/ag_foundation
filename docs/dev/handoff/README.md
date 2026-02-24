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
| 2026-02-24 | AF-0004 | [2026-02-24_AF-0004_sprint-os-hygiene.md](2026-02-24_AF-0004_sprint-os-hygiene.md) | Sprint OS hygiene (docs/pointers) |
| 2026-02-24 | AF-0010 | [2026-02-24_AF-0010_python-bootstrap.md](2026-02-24_AF-0010_python-bootstrap.md) | Python project bootstrap |
| 2026-02-23 | — | [ONBOARDING_SUMMARY_JACOB.md](ONBOARDING_SUMMARY_JACOB.md) | Jacob onboarding notes |
