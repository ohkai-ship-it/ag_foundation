"""V0 Verifier implementation.

Extracted from runtime.py (AF-0114).
"""

from __future__ import annotations

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
