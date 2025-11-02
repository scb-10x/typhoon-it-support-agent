"""Test cases for evaluation-driven development."""

from typing import Any, Dict, List

# Test cases following Best Practice #2: Design test cases for agentic workflows
TEST_CASES: List[Dict[str, Any]] = [
    # Happy path: Password reset
    {
        "id": "password_reset_001",
        "category": "policy_query",
        "input": "ผมลืมรหัสผ่านครับ ต้องทำยังไงครับ",
        "expected_behavior": [
            "search_it_policy should be called",
            "response should be in Thai",
            "should mention IT portal URL",
            "should explain password requirements",
        ],
        "expected_tools": ["search_it_policy"],
        "success_criteria": {
            "uses_correct_tool": True,
            "responds_in_thai": True,
            "provides_actionable_steps": True,
            "cites_documentation": True,
        },
    },
    # Happy path: WiFi troubleshooting
    {
        "id": "wifi_trouble_001",
        "category": "troubleshooting",
        "input": "เชื่อมต่อ WiFi ไม่ได้ค่ะ",
        "expected_behavior": [
            "search_troubleshooting_guide should be called",
            "response should be in Thai",
            "should provide step-by-step solution",
            "should offer to create ticket if not resolved",
        ],
        "expected_tools": ["search_troubleshooting_guide"],
        "success_criteria": {
            "uses_correct_tool": True,
            "responds_in_thai": True,
            "provides_actionable_steps": True,
            "offers_ticket_creation": True,
        },
    },
    # Happy path: Create ticket
    {
        "id": "create_ticket_001",
        "category": "ticket_creation",
        "input": "สร้างตั๋วให้หน่อยครับ คอมช้ามาก ทำงานไม่ได้เลย",
        "expected_behavior": [
            "create_ticket should be called",
            "ticket should have appropriate priority",
            "response should include ticket ID",
            "response should be in Thai",
        ],
        "expected_tools": ["create_ticket"],
        "success_criteria": {
            "uses_correct_tool": True,
            "responds_in_thai": True,
            "includes_ticket_id": True,
            "appropriate_priority": True,
        },
    },
    # Happy path: Check ticket status
    {
        "id": "check_ticket_001",
        "category": "ticket_query",
        "input": "ตรวจสอบสถานะตั๋วหมายเลข 1001 ให้หน่อยค่ะ",
        "expected_behavior": [
            "get_ticket should be called with ID 1001",
            "response should include ticket details",
            "response should be in Thai",
        ],
        "expected_tools": ["get_ticket"],
        "success_criteria": {
            "uses_correct_tool": True,
            "responds_in_thai": True,
            "extracts_ticket_id": True,
        },
    },
    # Edge case: Vague query
    {
        "id": "vague_query_001",
        "category": "edge_case",
        "input": "ช่วยหน่อยครับ",
        "expected_behavior": [
            "should ask clarifying questions",
            "should not call tools immediately",
            "response should be in Thai",
        ],
        "expected_tools": [],
        "success_criteria": {
            "asks_clarifying_questions": True,
            "responds_in_thai": True,
            "does_not_hallucinate": True,
        },
    },
    # Edge case: Multiple issues
    {
        "id": "multiple_issues_001",
        "category": "edge_case",
        "input": "คอมช้า WiFi ก็เชื่อมต่อไม่ได้ แล้วก็ printer ไม่ทำงานด้วยค่ะ",
        "expected_behavior": [
            "should address issues systematically",
            "may search troubleshooting guide multiple times",
            "should prioritize or ask which to solve first",
            "response should be in Thai",
        ],
        "expected_tools": ["search_troubleshooting_guide"],
        "success_criteria": {
            "addresses_multiple_issues": True,
            "responds_in_thai": True,
            "provides_organized_response": True,
        },
    },
    # Edge case: Urgent issue
    {
        "id": "urgent_issue_001",
        "category": "edge_case",
        "input": "เร่งด่วนมากครับ! ระบบล่มหมด ทำงานไม่ได้เลย ต้องการความช่วยเหลือด่วน",
        "expected_behavior": [
            "should create ticket with high/urgent priority",
            "should acknowledge urgency",
            "should provide emergency contact info",
            "response should be in Thai",
        ],
        "expected_tools": ["create_ticket"],
        "success_criteria": {
            "uses_correct_tool": True,
            "sets_urgent_priority": True,
            "responds_in_thai": True,
            "provides_emergency_info": True,
        },
    },
    # Unhappy path: Invalid ticket ID
    {
        "id": "invalid_ticket_001",
        "category": "unhappy_path",
        "input": "ตรวจสอบตั๋วหมายเลข 99999 ให้หน่อยค่ะ",
        "expected_behavior": [
            "get_ticket should be called",
            "should handle 'not found' gracefully",
            "should ask if user wants to provide correct ID",
            "response should be in Thai",
        ],
        "expected_tools": ["get_ticket"],
        "success_criteria": {
            "uses_correct_tool": True,
            "handles_error_gracefully": True,
            "responds_in_thai": True,
        },
    },
    # Context awareness: Follow-up question
    {
        "id": "context_aware_001",
        "category": "context_awareness",
        "input": "ขอบคุณครับ แล้วถ้าลืมรหัสผ่านอีกต้องทำยังไงครับ",
        "expected_behavior": [
            "should reference previous conversation",
            "may not need to search again if info already provided",
            "response should be in Thai",
        ],
        "expected_tools": [],  # Should check context first
        "success_criteria": {
            "uses_conversation_context": True,
            "responds_in_thai": True,
            "avoids_redundant_searches": True,
        },
    },
    # Performance: Simple greeting
    {
        "id": "greeting_001",
        "category": "performance",
        "input": "สวัสดีครับ",
        "expected_behavior": [
            "should respond with greeting",
            "should not call any tools",
            "should ask how to help",
            "response should be in Thai",
        ],
        "expected_tools": [],
        "success_criteria": {
            "responds_quickly": True,
            "responds_in_thai": True,
            "does_not_call_unnecessary_tools": True,
        },
    },
]


def get_test_cases_by_category(category: str) -> List[Dict[str, Any]]:
    """Get test cases filtered by category.

    Args:
        category: Category name (policy_query, troubleshooting, ticket_creation, etc.)

    Returns:
        List of test cases matching the category.
    """
    return [tc for tc in TEST_CASES if tc["category"] == category]


def get_test_case_by_id(test_id: str) -> Dict[str, Any]:
    """Get a specific test case by ID.

    Args:
        test_id: Test case ID.

    Returns:
        Test case dictionary.
    """
    for tc in TEST_CASES:
        if tc["id"] == test_id:
            return tc
    raise ValueError(f"Test case {test_id} not found")
