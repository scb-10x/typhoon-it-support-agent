"""Tests for data models."""

from langchain_core.messages import HumanMessage

from src.typhoon_it_support.models import AgentState


def test_agent_state_structure():
    """Test that AgentState has the correct structure."""
    state: AgentState = {
        "messages": [],
        "iteration": 0,
        "next_action": "start",
    }
    assert "messages" in state
    assert "iteration" in state
    assert "next_action" in state


def test_agent_state_with_messages():
    """Test AgentState with actual messages."""
    message = HumanMessage(content="Test message")
    state: AgentState = {
        "messages": [message],
        "iteration": 1,
        "next_action": "continue",
    }
    assert len(state["messages"]) == 1
    assert state["messages"][0].content == "Test message"
    assert state["iteration"] == 1
    assert state["next_action"] == "continue"

