"""Tests for router node."""

from langchain_core.messages import AIMessage, HumanMessage

from src.typhoon_it_support.agents.router_node import router_node, should_continue
from src.typhoon_it_support.models import AgentState


def test_router_node_max_iterations():
    """Test that router ends workflow at max iterations."""
    state: AgentState = {
        "messages": [],
        "iteration": 10,
        "next_action": "route",
    }
    result = router_node(state)
    assert result["next_action"] == "end"


def test_router_node_resolved():
    """Test router detects resolved status."""
    state: AgentState = {
        "messages": [AIMessage(content="The issue has been resolved successfully.")],
        "iteration": 2,
        "next_action": "route",
    }
    result = router_node(state)
    assert result["next_action"] == "end"


def test_router_node_escalate():
    """Test router detects escalation need."""
    state: AgentState = {
        "messages": [AIMessage(content="I cannot solve this issue, needs escalation.")],
        "iteration": 2,
        "next_action": "route",
    }
    result = router_node(state)
    assert result["next_action"] == "escalate"


def test_router_node_continue():
    """Test router continues workflow."""
    state: AgentState = {
        "messages": [AIMessage(content="Let me help you with that.")],
        "iteration": 2,
        "next_action": "route",
    }
    result = router_node(state)
    assert result["next_action"] == "continue"


def test_should_continue_agent():
    """Test conditional edge to agent."""
    state: AgentState = {
        "messages": [],
        "iteration": 1,
        "next_action": "continue",
    }
    result = should_continue(state)
    assert result == "agent"


def test_should_continue_end():
    """Test conditional edge to end."""
    state: AgentState = {
        "messages": [],
        "iteration": 1,
        "next_action": "end",
    }
    result = should_continue(state)
    assert result == "end"


def test_should_continue_escalate():
    """Test conditional edge to escalate."""
    state: AgentState = {
        "messages": [],
        "iteration": 1,
        "next_action": "escalate",
    }
    result = should_continue(state)
    assert result == "escalate"

