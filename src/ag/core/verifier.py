"""V0, V1, and V2 Verifier implementations.

Extracted from runtime.py (AF-0114).
V1Verifier added (AF-0115): step-aware verification with required/optional distinction.
V2Verifier added (AF-0123): LLM semantic quality checks layered on V1.
"""

from __future__ import annotations

import json
import logging
import re
import time
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
        # BUG-0020: A run with zero executed steps is never a success
        if not steps:
            return "failed", "No steps executed"

        # Check for step errors
        for step in steps:
            if step.error:
                return "failed", f"Step {step.step_number} failed: {step.error}"

        # Check final status
        if final_status != FinalStatus.SUCCESS:
            return "failed", f"Run ended with status: {final_status.value}"

        return "passed", "All steps completed successfully"


class V1Verifier:
    """V1 Verifier: step-aware verification (AF-0115, AF-0117).

    Respects the required/optional distinction on steps:
    - Required step failure → verifier fails
    - Optional step failure → verifier passes with warnings
    - Populates evidence dict with per-step breakdown

    AF-0117: Adds verify_step() for per-step verification in V1Orchestrator.
    """

    def verify_step(self, step: Step) -> tuple[bool, str]:
        """Verify a single step (AF-0117).

        Args:
            step: The step to verify

        Returns:
            Tuple of (passed, message) where:
            - passed: True if step succeeded or is optional failure
            - message: Description of verification result
        """
        if step.error:
            if step.required:
                return False, f"Required step {step.step_number} failed: {step.error}"
            else:
                return True, f"Optional step {step.step_number} skipped: {step.error}"
        return True, f"Step {step.step_number} passed"

    def verify(self, trace: RunTrace) -> tuple[str, str | None]:
        """Verify a run's results with step awareness."""
        return self.verify_components(trace.steps, trace.final)

    def verify_components(
        self, steps: list[Step], final_status: FinalStatus
    ) -> tuple[str, str | None]:
        """Verify run components with required/optional awareness."""
        # BUG-0020: A run with zero executed steps is never a success
        if not steps:
            return "failed", "No steps executed"

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
        """Build per-step evidence breakdown for the Verifier model (AF-0118).

        Returns a structured evidence dict with version, counts, and per-step detail.
        """
        required_passed = 0
        required_failed = 0
        optional_passed = 0
        optional_failed = 0
        per_step: list[dict[str, Any]] = []
        retries: dict[str, dict[str, Any]] = {}

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
                "skill": step.skill_name,  # AF-0118: Include skill name
                "required": step.required,
                "status": "failed" if has_error else "passed",
            }
            if has_error:
                entry["reason"] = step.error

            # AF-0118: Extract retry info from output_data
            if step.output_data and "_validation_attempts" in step.output_data:
                attempts = step.output_data["_validation_attempts"]
                entry["attempts"] = attempts
                if attempts > 1:
                    retries[f"step_{step.step_number}"] = {
                        "attempts": attempts,
                        "skill": step.skill_name,
                    }

            per_step.append(entry)

        return {
            "version": "v1",  # AF-0118: Evidence schema version
            "total_steps": len(steps),
            "required_passed": required_passed,
            "required_failed": required_failed,
            "optional_passed": optional_passed,
            "optional_skipped": optional_failed,
            "retries": retries,  # AF-0118: Retry summary
            "per_step": per_step,
        }


logger = logging.getLogger(__name__)

# Default semantic check thresholds (AF-0123)
DEFAULT_RELEVANCE_THRESHOLD = 0.6
DEFAULT_COMPLETENESS_THRESHOLD = 0.5
DEFAULT_CONSISTENCY_THRESHOLD = 0.7


class V2Verifier(V1Verifier):
    """LLM-powered semantic verification layered on V1 mechanical checks (AF-0123).

    Three semantic checks: relevance, completeness, consistency.
    If LLM is unavailable, V1 result stands (graceful degradation).
    """

    def __init__(
        self,
        provider: Any | None = None,
        relevance_threshold: float = DEFAULT_RELEVANCE_THRESHOLD,
        completeness_threshold: float = DEFAULT_COMPLETENESS_THRESHOLD,
        consistency_threshold: float = DEFAULT_CONSISTENCY_THRESHOLD,
    ) -> None:
        super().__init__()
        self._provider = provider
        self._relevance_threshold = relevance_threshold
        self._completeness_threshold = completeness_threshold
        self._consistency_threshold = consistency_threshold

    def verify(self, trace: RunTrace) -> tuple[str, str | None]:
        """Verify with V1 mechanical checks, then LLM semantic checks."""
        # Step 1: V1 mechanical checks (always runs)
        status, message = super().verify(trace)

        # Step 2: LLM semantic checks (additive, skippable)
        if self._provider is None:
            return status, message

        # Only run semantic checks on steps that passed V1
        semantic_results = self._run_semantic_checks(trace)
        if semantic_results is None:
            # LLM failed — graceful degradation
            return status, message

        return self._merge_results(status, message, semantic_results)

    def verify_components(
        self, steps: list[Step], final_status: FinalStatus
    ) -> tuple[str, str | None]:
        """Verify components — V1 only (semantic checks need full trace)."""
        return super().verify_components(steps, final_status)

    def _run_semantic_checks(self, trace: RunTrace) -> list[dict[str, Any]] | None:
        """Run semantic checks on passed steps via LLM.

        Returns list of per-step semantic results, or None on LLM failure.
        """
        from ag.providers.base import ChatMessage, MessageRole

        # Collect passed steps (no error, required or optional)
        passed_steps = [s for s in trace.steps if not s.error]
        if not passed_steps:
            return []

        prompt = self._build_semantic_prompt(trace, passed_steps)
        try:
            response = self._provider.chat(
                messages=[
                    ChatMessage(
                        role=MessageRole.SYSTEM,
                        content=self._get_semantic_system_prompt(),
                    ),
                    ChatMessage(role=MessageRole.USER, content=prompt),
                ],
            )
        except Exception as e:
            logger.warning(f"Semantic verification LLM call failed: {e}")
            return None

        try:
            return self._parse_semantic_response(response.content, len(passed_steps))
        except Exception as e:
            logger.warning(f"Failed to parse semantic response: {e}")
            return None

    def _get_semantic_system_prompt(self) -> str:
        """System prompt for semantic verification."""
        return """You are a quality evaluator for an agent system. For each step output,
evaluate three dimensions:

1. **Relevance** (0.0–1.0): Does the output address the original task?
2. **Completeness** (0.0–1.0): Are expected elements present in the output?
3. **Consistency** (0.0–1.0): Is the output internally consistent and factually coherent?

Respond with valid JSON — an array with one object per step:
[
  {
    "step_number": 0,
    "relevance_score": 0.9,
    "relevance_reason": "Output directly addresses the task",
    "completeness_score": 0.8,
    "completeness_missing": [],
    "consistency_score": 0.95,
    "consistency_issues": []
  }
]"""

    def _build_semantic_prompt(self, trace: RunTrace, passed_steps: list[Step]) -> str:
        """Build user prompt for semantic evaluation."""
        task_prompt = trace.metadata.get("prompt", "")
        # Try to find the prompt in the trace — it's often in the first step's input
        if not task_prompt and passed_steps:
            task_prompt = passed_steps[0].input_summary

        step_summaries = []
        for step in passed_steps:
            output = step.output_summary or "(no output)"
            if step.output_data:
                # Include structured output for richer evaluation
                output_data_str = json.dumps(step.output_data, default=str)
                if len(output_data_str) > 2000:
                    output_data_str = output_data_str[:2000] + "..."
                output = f"{output}\n\nStructured output: {output_data_str}"
            step_summaries.append(
                f"### Step {step.step_number} ({step.skill_name or 'unknown'})\n"
                f"Input: {step.input_summary}\n"
                f"Output: {output}"
            )

        steps_text = "\n\n".join(step_summaries)
        return f"""Evaluate the quality of these step outputs for the given task.

**Task:** {task_prompt}

**Steps to evaluate:**

{steps_text}

Provide relevance, completeness, and consistency scores for each step."""

    def _parse_semantic_response(self, content: str, expected_count: int) -> list[dict[str, Any]]:
        """Parse LLM semantic evaluation response."""
        json_str = content.strip()
        if json_str.startswith("```"):
            lines = json_str.split("\n")
            json_lines = []
            in_block = False
            for line in lines:
                if line.startswith("```") and not in_block:
                    in_block = True
                    continue
                if line.startswith("```") and in_block:
                    break
                if in_block:
                    json_lines.append(line)
            json_str = "\n".join(json_lines)

        # Clean comments
        cleaned_lines: list[str] = []
        for line in json_str.split("\n"):
            stripped = line.lstrip()
            if stripped.startswith("//"):
                continue
            comment_pos = line.find("//")
            if comment_pos > 0:
                prefix = line[:comment_pos]
                if prefix.count('"') % 2 == 0:
                    line = prefix.rstrip()
            cleaned_lines.append(line)
        json_str = "\n".join(cleaned_lines)
        json_str = re.sub(r",\s*([}\]])", r"\1", json_str)

        data = json.loads(json_str)
        if not isinstance(data, list):
            data = [data]
        return data

    def _merge_results(
        self,
        v1_status: str,
        v1_message: str | None,
        semantic_results: list[dict[str, Any]],
    ) -> tuple[str, str | None]:
        """Merge V1 mechanical + V2 semantic results."""
        if not semantic_results:
            return v1_status, v1_message

        failed_checks: list[str] = []
        for result in semantic_results:
            step_num = result.get("step_number", "?")
            rel = result.get("relevance_score", 1.0)
            comp = result.get("completeness_score", 1.0)
            cons = result.get("consistency_score", 1.0)

            if rel < self._relevance_threshold:
                reason = result.get("relevance_reason", "low relevance")
                failed_checks.append(f"Step {step_num} relevance {rel:.2f}: {reason}")
            if comp < self._completeness_threshold:
                missing = result.get("completeness_missing", [])
                missing_str = ", ".join(missing) if missing else "incomplete"
                failed_checks.append(f"Step {step_num} completeness {comp:.2f}: {missing_str}")
            if cons < self._consistency_threshold:
                issues = result.get("consistency_issues", [])
                issues_str = ", ".join(issues) if issues else "inconsistent"
                failed_checks.append(f"Step {step_num} consistency {cons:.2f}: {issues_str}")

        if failed_checks:
            semantic_msg = "Semantic check failures: " + "; ".join(failed_checks)
            if v1_status == "failed":
                return "failed", f"{v1_message}; {semantic_msg}"
            return "failed", semantic_msg

        if v1_message and "optional" in v1_message.lower():
            return v1_status, v1_message
        return v1_status, v1_message

    def build_semantic_evidence(self, trace: RunTrace) -> dict[str, Any] | None:
        """Build semantic evidence for trace recording.

        Returns semantic verification dict or None if LLM unavailable.
        """
        from ag.core.run_trace import SemanticVerification

        if self._provider is None:
            return None

        start_ms = time.monotonic_ns() // 1_000_000
        results = self._run_semantic_checks(trace)
        elapsed_ms = (time.monotonic_ns() // 1_000_000) - start_ms

        if results is None:
            return None

        # Aggregate scores across steps
        if not results:
            return SemanticVerification(
                relevance_score=1.0,
                completeness_score=1.0,
                consistency_score=1.0,
                overall_pass=True,
                evaluation_ms=elapsed_ms,
            ).model_dump()

        rel_scores = [r.get("relevance_score", 1.0) for r in results]
        comp_scores = [r.get("completeness_score", 1.0) for r in results]
        cons_scores = [r.get("consistency_score", 1.0) for r in results]

        avg_rel = sum(rel_scores) / len(rel_scores)
        avg_comp = sum(comp_scores) / len(comp_scores)
        avg_cons = sum(cons_scores) / len(cons_scores)

        all_missing = []
        all_issues = []
        reasons = []
        for r in results:
            all_missing.extend(r.get("completeness_missing", []))
            all_issues.extend(r.get("consistency_issues", []))
            if r.get("relevance_reason"):
                reasons.append(r["relevance_reason"])

        overall_pass = (
            avg_rel >= self._relevance_threshold
            and avg_comp >= self._completeness_threshold
            and avg_cons >= self._consistency_threshold
        )

        return SemanticVerification(
            relevance_score=round(avg_rel, 3),
            relevance_reason="; ".join(reasons) if reasons else "",
            completeness_score=round(avg_comp, 3),
            completeness_missing=all_missing,
            consistency_score=round(avg_cons, 3),
            consistency_issues=all_issues,
            overall_pass=overall_pass,
            evaluation_ms=elapsed_ms,
        ).model_dump()
