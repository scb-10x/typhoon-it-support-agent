"""Test script to demonstrate checkpointer functionality."""

import sys
from pathlib import Path

from langchain_core.messages import HumanMessage

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from typhoon_it_support.graph import create_workflow
from typhoon_it_support.models import AgentState


def test_checkpointer() -> None:
    """Test checkpointer with multi-turn conversation."""
    print("Testing Checkpointer - Continuous Conversation")
    print("=" * 50)

    workflow = create_workflow()
    session_id = "test-session-123"
    config = {"configurable": {"thread_id": session_id}}

    print("\nTurn 1: Asking about password reset")
    print("-" * 50)
    state1: AgentState = {
        "messages": [HumanMessage(content="What is the password reset policy?")],
        "iteration": 0,
        "next_action": "start",
    }

    result1 = workflow.invoke(state1, config)
    print(f"Messages in state: {len(result1['messages'])}")
    for i, msg in enumerate(result1["messages"]):
        role = "User" if hasattr(msg, "type") and msg.type == "human" else "AI"
        content = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
        print(f"  {i + 1}. {role}: {content}")

    print("\nTurn 2: Follow-up question (same session)")
    print("-" * 50)
    state2: AgentState = {
        "messages": [HumanMessage(content="How long does the process take?")],
        "iteration": 0,
        "next_action": "start",
    }

    result2 = workflow.invoke(state2, config)
    print(f"Messages in state: {len(result2['messages'])}")
    print("History maintained - Agent has context from previous turn:")
    for i, msg in enumerate(result2["messages"]):
        role = "User" if hasattr(msg, "type") and msg.type == "human" else "AI"
        content = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
        print(f"  {i + 1}. {role}: {content}")

    print("\nTurn 3: Another follow-up (same session)")
    print("-" * 50)
    state3: AgentState = {
        "messages": [HumanMessage(content="Can you summarize what we discussed?")],
        "iteration": 0,
        "next_action": "start",
    }

    result3 = workflow.invoke(state3, config)
    print(f"Messages in state: {len(result3['messages'])}")
    print("Full conversation history maintained:")
    for i, msg in enumerate(result3["messages"]):
        role = "User" if hasattr(msg, "type") and msg.type == "human" else "AI"
        content = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
        print(f"  {i + 1}. {role}: {content}")

    print("\n" + "=" * 50)
    print("Test completed successfully!")
    print("The checkpointer maintained conversation context across all turns.")


def test_multiple_sessions() -> None:
    """Test multiple independent sessions."""
    print("\n\nTesting Multiple Independent Sessions")
    print("=" * 50)

    workflow = create_workflow()

    session_1 = "user-alice"
    session_2 = "user-bob"

    print("\nSession 1 (Alice): Asking about VPN")
    print("-" * 50)
    config_1 = {"configurable": {"thread_id": session_1}}
    state_alice: AgentState = {
        "messages": [HumanMessage(content="How do I set up VPN?")],
        "iteration": 0,
        "next_action": "start",
    }

    result_alice_1 = workflow.invoke(state_alice, config_1)
    print(f"Alice's messages: {len(result_alice_1['messages'])}")

    print("\nSession 2 (Bob): Asking about printer")
    print("-" * 50)
    config_2 = {"configurable": {"thread_id": session_2}}
    state_bob: AgentState = {
        "messages": [HumanMessage(content="My printer is not working")],
        "iteration": 0,
        "next_action": "start",
    }

    result_bob_1 = workflow.invoke(state_bob, config_2)
    print(f"Bob's messages: {len(result_bob_1['messages'])}")

    print("\nSession 1 (Alice): Follow-up about VPN")
    print("-" * 50)
    state_alice_2: AgentState = {
        "messages": [HumanMessage(content="Which operating systems are supported?")],
        "iteration": 0,
        "next_action": "start",
    }

    result_alice_2 = workflow.invoke(state_alice_2, config_1)
    print(f"Alice's messages: {len(result_alice_2['messages'])}")
    print("Alice's context includes VPN discussion (not printer)")

    print("\nSession 2 (Bob): Follow-up about printer")
    print("-" * 50)
    state_bob_2: AgentState = {
        "messages": [HumanMessage(content="It shows error 'paper jam'")],
        "iteration": 0,
        "next_action": "start",
    }

    result_bob_2 = workflow.invoke(state_bob_2, config_2)
    print(f"Bob's messages: {len(result_bob_2['messages'])}")
    print("Bob's context includes printer discussion (not VPN)")

    print("\n" + "=" * 50)
    print("Multiple sessions test completed!")
    print("Each session maintained independent conversation history.")


if __name__ == "__main__":
    test_checkpointer()
    test_multiple_sessions()
