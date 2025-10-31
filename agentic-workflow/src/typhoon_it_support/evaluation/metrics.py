"""Evaluation metrics for agentic workflow."""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class EvaluationResult:
    """Result of an evaluation run."""
    
    test_id: str
    category: str
    input_text: str
    response: str
    tools_called: List[str]
    execution_time: float
    success_criteria: Dict[str, bool]
    overall_score: float
    passed: bool
    notes: str
    timestamp: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "test_id": self.test_id,
            "category": self.category,
            "input_text": self.input_text,
            "response": self.response,
            "tools_called": self.tools_called,
            "execution_time": self.execution_time,
            "success_criteria": self.success_criteria,
            "overall_score": self.overall_score,
            "passed": self.passed,
            "notes": self.notes,
            "timestamp": self.timestamp,
        }


def check_thai_language(text: str) -> bool:
    """Check if text contains Thai characters.
    
    Args:
        text: Text to check.
        
    Returns:
        True if Thai characters found.
    """
    thai_chars = set(range(0x0E00, 0x0E7F))
    return any(ord(char) in thai_chars for char in text)


def check_tools_used(expected_tools: List[str], actual_tools: List[str]) -> bool:
    """Check if expected tools were used.
    
    Args:
        expected_tools: List of expected tool names.
        actual_tools: List of actually called tool names.
        
    Returns:
        True if all expected tools were called.
    """
    return all(tool in actual_tools for tool in expected_tools)


def check_actionable_steps(text: str) -> bool:
    """Check if response contains actionable steps.
    
    Args:
        text: Response text.
        
    Returns:
        True if steps are present (looks for numbered lists or step indicators).
    """
    step_indicators = ["1.", "2.", "ขั้นตอน", "วิธี", "step"]
    return any(indicator in text.lower() for indicator in step_indicators)


def check_ticket_id(text: str) -> bool:
    """Check if response contains ticket ID.
    
    Args:
        text: Response text.
        
    Returns:
        True if ticket ID pattern found.
    """
    import re
    return bool(re.search(r"#\d+", text))


def evaluate_response(
    test_case: Dict[str, Any],
    response: str,
    tools_called: List[str],
    execution_time: float,
    additional_checks: Optional[Dict[str, bool]] = None,
) -> EvaluationResult:
    """Evaluate a response against test case criteria.
    
    Args:
        test_case: Test case definition.
        response: Agent response.
        tools_called: List of tool names that were called.
        execution_time: Time taken to generate response.
        additional_checks: Additional criteria checks from evaluator.
        
    Returns:
        Evaluation result with scores.
    """
    criteria = test_case["success_criteria"]
    results = {}
    
    # Check each criterion
    if "uses_correct_tool" in criteria:
        results["uses_correct_tool"] = check_tools_used(
            test_case["expected_tools"],
            tools_called
        )
    
    if "responds_in_thai" in criteria:
        results["responds_in_thai"] = check_thai_language(response)
    
    if "provides_actionable_steps" in criteria:
        results["provides_actionable_steps"] = check_actionable_steps(response)
    
    if "includes_ticket_id" in criteria:
        results["includes_ticket_id"] = check_ticket_id(response)
    
    if "does_not_call_unnecessary_tools" in criteria:
        results["does_not_call_unnecessary_tools"] = len(tools_called) == 0
    
    if "asks_clarifying_questions" in criteria:
        question_indicators = ["?", "ไหม", "หรือ", "อะไร", "ช่วย"]
        results["asks_clarifying_questions"] = any(
            ind in response for ind in question_indicators
        )
    
    # Add additional checks if provided
    if additional_checks:
        results.update(additional_checks)
    
    # Calculate overall score
    total_criteria = len(criteria)
    passed_criteria = sum(1 for v in results.values() if v)
    overall_score = passed_criteria / total_criteria if total_criteria > 0 else 0.0
    
    # Determine if passed (80% threshold)
    passed = overall_score >= 0.8
    
    # Generate notes
    notes = []
    for criterion, result in results.items():
        if not result:
            notes.append(f"Failed: {criterion}")
    
    return EvaluationResult(
        test_id=test_case["id"],
        category=test_case["category"],
        input_text=test_case["input"],
        response=response,
        tools_called=tools_called,
        execution_time=execution_time,
        success_criteria=results,
        overall_score=overall_score,
        passed=passed,
        notes="; ".join(notes) if notes else "All criteria passed",
        timestamp=datetime.now().isoformat(),
    )


def calculate_aggregate_metrics(results: List[EvaluationResult]) -> Dict[str, Any]:
    """Calculate aggregate metrics across multiple evaluation results.
    
    Args:
        results: List of evaluation results.
        
    Returns:
        Dictionary of aggregate metrics.
    """
    if not results:
        return {}
    
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    
    avg_score = sum(r.overall_score for r in results) / total
    avg_time = sum(r.execution_time for r in results) / total
    
    # Category breakdown
    category_stats = {}
    for result in results:
        cat = result.category
        if cat not in category_stats:
            category_stats[cat] = {"total": 0, "passed": 0}
        category_stats[cat]["total"] += 1
        if result.passed:
            category_stats[cat]["passed"] += 1
    
    for cat in category_stats:
        stats = category_stats[cat]
        stats["pass_rate"] = stats["passed"] / stats["total"]
    
    return {
        "total_tests": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": passed / total,
        "average_score": avg_score,
        "average_execution_time": avg_time,
        "category_breakdown": category_stats,
    }

