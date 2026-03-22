"""V0 and V1 Verifier implementations.

Extracted from runtime.py (AF-0114).
V1Verifier added (AF-0115): step-aware verification with required/optional distinction.
"""

from __future__ import annotations

from typing import Any

from ag.core.run_trace import FinalStatus, RunTrace, Step


class V0Verifier:
    """v0 Verifier: basic verification (checks for errors in trace)."""

    def verify(self, trace: RunTrace) -> tuple[str, str | None]:
        """Verify a run's results.

        v0 verification:
        - If any step has an error, return 'failed'
        - If final status is not success, return 'failed'
        - Otherwise return 'passed'
        """
        return self.verify_components(trace.steps, trace.final)

    def verify_components(
        self, steps: list[Step], final_status: FinalStatus
    ) -> tuple[str, str | None]:
        """Verify run components without requiring a full trace (AF-0029)."""
        # Check for step errors
        for step in steps:
            if step.error:
                return "failed", f"Step {step.step_number} failed: {step.error}"

        # Check final status
        if final_status != FinalStatus.SUCCESS:
            return "failed", f"Run ended with status: {final_status.value}"

        return "passed", "All steps completed successfully"


class V1Verifier:
    """V1 Verifier: step-aware verification (AF-0115).

    Respects the required/optional distinction on steps:
    - Required step failure → verifier fails
    - Optional step failure → verifier passes with warnings
    - Populates evidence dict with per-step breakdown
    """

    def verify(self, trace: RunTrace) -> tuple[str, str | None]:
        """Verify a run's results with step awareness."""
        return self.verify_components(trace.steps, trace.final)

    def verify_components(
        self, steps: list[Step], final_status: FinalStatus
    ) -> tuple[str, str | None]:
        """Verify run components with required/optional awareness."""
        failed_required: list[Step] = []
        failed_optional: list[Step] = []

        for step in steps:
            if step.error:
                if step.required:
                    failed_required.append(step)
                else:
                    failed_optional.append(step)

        if failed_required:
            msg = "; ".join(f"Step {s.step_number}: {s.error}" for s in failed_required)
            return "failed", f"Required step(s) failed: {msg}"

        if final_status != FinalStatus.SUCCESS:
            return "failed", f"Run ended with status: {final_status.value}"

        if failed_optional:
            msg = "; ".join(f"Step {s.step_number} (optional): {s.error}" for s in failed_optional)
            return "passed", f"Passed with optional step warnings: {msg}"

        return "passed", "All steps completed successfully"

    def build_evidence(self, steps: list[Step]) -> dict[str, Any]:
        """Build per-step evidence breakdown for the Verifier model."""
        required_passed = 0
        required_failed = 0
        optional_passed = 0
        optional_failed = 0
        per_step: list[dict[str, Any]] = []

        for step in steps:
            has_error = bool(step.error)
            if step.required:
                if has_error:
                    required_failed += 1
                else:
                    required_passed += 1
            else:
                if has_error:
                    optional_failed += 1
                else:
                    optional_passed += 1

            entry: dict[str, Any] = {
                "step": step.step_number,
                "required": step.required,
                "status": "failed" if has_error else "passed",
            }
            if has_error:
                entry["reason"] = step.error
            per_step.append(entry)

        return {
            "total_steps": len(steps),
            "required_passed": required_passed,
            "required_failed": required_failed,
            "optional_passed": optional_passed,
            "optional_skipped": optional_failed,
            "per_step": per_step,
        }
