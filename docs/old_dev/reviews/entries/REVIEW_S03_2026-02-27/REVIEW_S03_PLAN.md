# REVIEW PLAN --- Sprint 03 --- Observability & Truthful UX

# Version: v1.0

# Date: 2026-02-27

------------------------------------------------------------------------

## 1. Review Scope

Workspace Maturity - AF-0027 --- Default workspace policy - AF-0028 ---
Run ID formatting fix - AF-0029 --- RunTrace verification hardening

Observability & Truthful UX - AF-0030 --- RunTrace metadata
completeness - AF-0031 --- CLI truthfulness enforcement - AF-0032 ---
Observability command expansion

CLI UX Hardening - AF-0033 --- Early .env loading + manual mode gate
fix - AF-0034 --- Workspace error message hardening - AF-0035 ---
Clarify `--workspace` help text - AF-0036 --- Remove global CLI flags
(Proposed) - AF-0037 --- Standardize workspace-required errors - AF-0038
--- Ensure `--json` applies to error paths

------------------------------------------------------------------------

## 2. Review Objectives

Validate: - Workspace precedence correctness - No implicit workspace
creation - Manual mode gating integrity - RunTrace metadata
completeness - CLI truthfulness - Error path consistency -
JSON/verbosity contract - No architectural drift

------------------------------------------------------------------------

## 3. Verification Checklist

### Workspace

-   [ ] Precedence validated
-   [ ] No name leakage
-   [ ] Actionable guidance
-   [ ] No silent creation

### Manual Mode

-   [ ] AG_DEV enforced
-   [ ] dotenv loads early
-   [ ] Env override works
-   [ ] Error respects output flags

### RunTrace

-   [ ] Metadata complete
-   [ ] Verifier consistent
-   [ ] Workspace source correct

### CLI Output

-   [ ] JSON valid
-   [ ] Quiet works
-   [ ] Verbose works
-   [ ] Errors centralized

### Observability

-   [ ] Full run_id visible
-   [ ] JSON/text consistent

------------------------------------------------------------------------

## 4. Coverage & Tests

-   [ ] All tests pass
-   [ ] No warnings
-   [ ] Coverage maintained
-   [ ] New tests added for workspace + error paths

------------------------------------------------------------------------

## 5. Architectural Validation

-   [ ] CLI adapter-only
-   [ ] Resolution centralized
-   [ ] No runtime coupling
-   [ ] RunTrace single source of truth

------------------------------------------------------------------------

## 6. Open Items

-   AF-0036 remains Proposed
-   Potential CLI grammar refinement

------------------------------------------------------------------------

## 7. Sign-Off Criteria

Sprint 03 is approved when: - All P0/P1 complete - No P1 bugs open - No
regressions - Documentation updated

------------------------------------------------------------------------

## 8. Reviewer Notes

(To be completed during review)
