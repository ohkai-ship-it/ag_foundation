# S##_PR_01 — Sprint## PR Finalization Checklist
# Version number: v0.2

> Location: `/docs/new_dev/sprints/documentation/Sprint##_three_word_description/S##_PR_01.md`

## 1) Sprint metadata
- **Sprint:** Sprint##
- **Branch:** <name>
- **Target merge:** main
- **Date:** YYYY-MM-DD

## 2) Preconditions
- [ ] Sprint review decision recorded in `S##_REVIEW_01.md` as **ACCEPT** or **ACCEPT WITH FOLLOW-UPS**
- [ ] All P0 AF items merged
- [ ] All merged AF items have completion sections filled
- [ ] Indices updated:
  - [ ] `/docs/new_dev/backlog/INDEX_BACKLOG.md`
  - [ ] `/docs/new_dev/bugs/INDEX_BUGS.md`
  - [ ] `/docs/new_dev/decisions/INDEX_DECISIONS.md`
  - [ ] `/docs/new_dev/sprints/INDEX_SPRINTS.md`

## 3) Required local checks (must paste outputs into artifacts folder)
- [ ] `ruff check src tests`
- [ ] `ruff format --check src tests`
- [ ] `pytest -W error`
- [ ] `pytest --cov=src/ag --cov-report=term-missing`

## 4) Repo hygiene
- [ ] No stray files in root
- [ ] No untracked generated files
- [ ] Naming conventions respected for any new docs
- [ ] Links verified (no broken internal doc links)

## 5) Finalization
- [ ] PR created and references sprint + AF items in description
- [ ] PR template filled
- [ ] Review requested (Jeff + Kai)
- [ ] After merge: sprint state updated to **Closed** in `S##_DESCRIPTION.md`
