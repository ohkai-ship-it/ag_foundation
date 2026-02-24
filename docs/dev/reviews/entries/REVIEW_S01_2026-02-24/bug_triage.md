# Pass 8 — Bug Triage (BUG-0001..BUG-0003)
# Date: 2026-02-24
# Reviewer: Jacob

## BUG-0001 — Global CLI options not implemented as global

### Reproduction
> ag --help | Select-String "workspace|json|quiet|verbose"
(no output - options not present in main help)

### Expected vs Actual
| Expected | Actual |
|----------|--------|
| `--workspace`, `--json`, `--quiet`, `--verbose` as global options | Only `--version`, `--install-completion`, `--show-completion`, `--help` |

### Classification
| Attribute | Value |
|-----------|-------|
| Severity | P1 |
| Type | Defect (spec non-compliance) |
| Blocking | No (workaround: use per-command options) |
| Root cause | Global options not added to main callback |

### Recommendation
Create AF-0011 to implement global options using Typer context propagation.

---

## BUG-0002 — Missing ag run options per CLI reference

### Reproduction
> ag run --file test.txt "test"

Error: No such option: --file Did you mean --quiet?

### Expected vs Actual
| Expected | Actual |
|----------|--------|
| `--file`, `--task`, `--confirm` options | Not implemented |

### Classification
| Attribute | Value |
|-----------|-------|
| Severity | P2 |
| Type | Deferred scope (not a regression) |
| Blocking | No (core functionality works) |
| Root cause | Options scoped out of v0 |

### Recommendation
These are "nice to have" for v0. Can be addressed in Sprint 02 or later.

---

## BUG-0003 — Missing CLI subcommands per reference spec

### Reproduction
> ag ws config get test_key

Error: No such command 'config'.

### Expected vs Actual
| Expected | Actual |
|----------|--------|
| `ag ws config get/set` | Not implemented |
| `ag artifacts open/export` | Not implemented |
| `ag skills test/enable/disable` | Not implemented |
| `ag playbooks validate/set-default` | Not implemented |
| `ag runs tail` | Not implemented |

### Classification
| Attribute | Value |
|-----------|-------|
| Severity | P2 |
| Type | Deferred scope (not a regression) |
| Blocking | No (existing commands work) |
| Root cause | Subcommands scoped out of v0 |

### Recommendation
Add stubs for all missing subcommands to establish API surface. Actual implementation can follow.

---

## Spec Compliance Summary

### CLI_REFERENCE.md vs Implementation

| Command | Subcommands Expected | Subcommands Implemented | Gap |
|---------|---------------------|-------------------------|-----|
| ag (global) | --workspace, --json, --quiet, --verbose | None (only --version) | ⚠️ BUG-0001 |
| ag run | --file, --task, --confirm | None of these | ⚠️ BUG-0002 |
| ag runs | list, show, trace, tail | list, show, trace | tail missing |
| ag ws | list, create, use, show, config get/set | list, create, use, show (stubs) | config missing |
| ag artifacts | list, show, open, export | list, show (stub) | open, export missing |
| ag skills | list, info, test, enable, disable | list, info (stubs) | test, enable, disable missing |
| ag playbooks | list, show, validate, set-default | list, show (stubs) | validate, set-default missing |
| ag config | list, get, set | list, get, set (stubs) | ✅ |
| ag doctor | (main) | ✅ (partial) | ✅ |

---

## Follow-up Recommendations

| Bug | Action | Priority | New Item |
|-----|--------|----------|----------|
| BUG-0001 | Fix global options | P1 | AF-0011 (proposed) |
| BUG-0002 | Add --file, --task, --confirm to run | P2 | Can batch with BUG-0003 |
| BUG-0003 | Add stub subcommands | P2 | AF-0012 (proposed) |

---

## Result
✅ All bugs reproduced and classified.

**Verdict:** These are spec gaps, not regressions. The core v0 functionality (run → trace → artifacts) works correctly. The gaps represent features deferred from Sprint 01 scope.

**Blocking assessment:** No blockers for Sprint 01 completion. Gaps should be tracked as follow-up work.
