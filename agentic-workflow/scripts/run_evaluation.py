#!/usr/bin/env python3
"""Run evaluation suite on the agentic workflow.

This script implements Evaluation-Driven Development (Best Practice #1).
"""

import json
import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from langchain_core.messages import HumanMessage

from typhoon_it_support.evaluation import (
    TEST_CASES,
    calculate_aggregate_metrics,
    evaluate_response,
)
from typhoon_it_support.graph import create_workflow


def extract_tools_from_messages(messages):
    """Extract tool names from messages."""
    tools = []
    for msg in messages:
        if hasattr(msg, "name") and msg.name:
            tools.append(msg.name)
    return tools


def run_evaluation(test_ids: list = None, category: str = None, verbose: bool = True):
    """Run evaluation on test cases.

    Args:
        test_ids: Optional list of specific test IDs to run.
        category: Optional category filter.
        verbose: Print detailed output.
    """
    # Filter test cases
    test_cases = TEST_CASES
    if test_ids:
        test_cases = [tc for tc in test_cases if tc["id"] in test_ids]
    if category:
        test_cases = [tc for tc in test_cases if tc["category"] == category]

    if not test_cases:
        print("No test cases found matching criteria")
        return

    print(f"Running {len(test_cases)} test cases...")
    print("=" * 80)

    # Create workflow
    workflow = create_workflow()

    # Run evaluations
    results = []

    for i, test_case in enumerate(test_cases, 1):
        if verbose:
            print(f"\nTest {i}/{len(test_cases)}: {test_case['id']}")
            print(f"Category: {test_case['category']}")
            print(f"Input: {test_case['input']}")

        # Prepare state
        initial_state = {
            "messages": [HumanMessage(content=test_case["input"])],
            "iteration": 0,
            "next_action": "start",
            "active_tickets": [],
            "searched_documents": [],
            "user_info": None,
        }

        # Run workflow
        start_time = time.time()
        result = workflow.invoke(initial_state)
        execution_time = time.time() - start_time

        # Extract response and tools
        final_message = result["messages"][-1]
        response = (
            final_message.content
            if hasattr(final_message, "content")
            else str(final_message)
        )
        tools_called = extract_tools_from_messages(result["messages"])

        # Evaluate
        eval_result = evaluate_response(
            test_case, response, tools_called, execution_time
        )
        results.append(eval_result)

        if verbose:
            print(f"Tools called: {tools_called}")
            print(f"Execution time: {execution_time:.2f}s")
            print(f"Score: {eval_result.overall_score:.2%}")
            print(f"Status: {'✅ PASSED' if eval_result.passed else '❌ FAILED'}")
            if not eval_result.passed:
                print(f"Notes: {eval_result.notes}")
            print(f"Response preview: {response[:200]}...")

    # Calculate aggregate metrics
    print("\n" + "=" * 80)
    print("EVALUATION SUMMARY")
    print("=" * 80)

    metrics = calculate_aggregate_metrics(results)

    print("\nOverall Results:")
    print(f"  Total tests: {metrics['total_tests']}")
    print(f"  Passed: {metrics['passed']}")
    print(f"  Failed: {metrics['failed']}")
    print(f"  Pass rate: {metrics['pass_rate']:.2%}")
    print(f"  Average score: {metrics['average_score']:.2%}")
    print(f"  Average execution time: {metrics['average_execution_time']:.2f}s")

    print("\nCategory Breakdown:")
    for cat, stats in metrics["category_breakdown"].items():
        print(f"  {cat}:")
        print(
            f"    Pass rate: {stats['pass_rate']:.2%} ({stats['passed']}/{stats['total']})"
        )

    # Save results
    output_dir = Path(__file__).parent.parent / "evaluation_results"
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / f"eval_{int(time.time())}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "summary": metrics,
                "results": [r.to_dict() for r in results],
            },
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(f"\n✅ Results saved to: {output_file}")

    return metrics, results


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(description="Run evaluation suite")
    parser.add_argument("--test-ids", nargs="+", help="Specific test IDs to run")
    parser.add_argument("--category", help="Filter by category")
    parser.add_argument("--quiet", action="store_true", help="Minimal output")

    args = parser.parse_args()

    run_evaluation(
        test_ids=args.test_ids, category=args.category, verbose=not args.quiet
    )


if __name__ == "__main__":
    main()
