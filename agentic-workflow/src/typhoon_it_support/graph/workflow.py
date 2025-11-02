"""Main workflow graph definition."""

from langgraph.graph import END, StateGraph

from ..agents import agent_node, tools_node
from ..config import get_settings
from ..events import EventEmitter
from ..models import AgentState
from .checkpointer import get_checkpointer


def route_after_agent(state: AgentState) -> str:
    """Route after agent decides to use tools or end.

    Args:
        state: Current agent state.

    Returns:
        Next node name: 'tools' or END.
    """
    settings = get_settings()

    # Check iteration limit
    if state.get("iteration", 0) >= settings.max_iterations:
        return END

    # Route based on agent's decision
    next_action = state.get("next_action", "end")
    if next_action == "tools":
        return "tools"
    return END


def create_workflow() -> StateGraph:
    """Create the IT support workflow graph.

    Implements a simple agent loop pattern:
    - agent: Decides to call tools OR provide final answer
    - tools: Executes tool calls and returns to agent

    The agent is fully responsible for deciding when to stop the loop
    by not calling tools and providing a final answer instead.

    Returns:
        Compiled workflow graph ready for execution.
    """
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tools_node)

    # Agent decides: call tools or end
    workflow.add_conditional_edges(
        "agent",
        route_after_agent,
        {
            "tools": "tools",
            END: END,
        },
    )

    # After tools: always return to agent
    workflow.add_edge("tools", "agent")

    # Set entry point
    workflow.set_entry_point("agent")

    # Compile graph with checkpointer for memory
    checkpointer = get_checkpointer()
    return workflow.compile(checkpointer=checkpointer)


def create_workflow_with_events(emitter: EventEmitter) -> StateGraph:
    """Create the IT support workflow graph with event tracking.

    This version wraps each node with event emission for live updates.

    Args:
        emitter: EventEmitter instance for emitting workflow events.

    Returns:
        Compiled workflow graph ready for execution.
    """
    from ..agents import (
        create_agent_node_with_events,
        create_tools_node_with_events,
    )

    workflow = StateGraph(AgentState)

    # Create event-aware nodes
    agent_node_with_events = create_agent_node_with_events(emitter)
    tools_node_with_events = create_tools_node_with_events(emitter)

    # Add nodes
    workflow.add_node("agent", agent_node_with_events)
    workflow.add_node("tools", tools_node_with_events)

    # Agent decides: call tools or end
    workflow.add_conditional_edges(
        "agent",
        route_after_agent,
        {
            "tools": "tools",
            END: END,
        },
    )

    # After tools: always return to agent
    workflow.add_edge("tools", "agent")

    # Set entry point
    workflow.set_entry_point("agent")

    # Compile graph with checkpointer for memory
    checkpointer = get_checkpointer()
    return workflow.compile(checkpointer=checkpointer)
