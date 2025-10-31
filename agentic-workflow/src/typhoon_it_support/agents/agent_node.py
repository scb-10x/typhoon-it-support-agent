"""Main agent node implementation."""

from typing import Callable

from ..events import EventEmitter, create_event_callbacks
from ..models import AgentState
from ..prompts import AGENT_SYSTEM_PROMPT
from ..tools import (
    add_ticket_comment,
    add_tags_to_ticket,
    assign_ticket,
    create_ticket,
    delete_ticket,
    get_current_time,
    get_my_open_tickets,
    get_ticket,
    search_all_documents,
    search_it_policy,
    search_tickets,
    search_troubleshooting_guide,
    set_ticket_category,
    set_ticket_due_date,
    update_ticket_priority,
    update_ticket_status,
)
from ..utils import add_instruction, build_base_messages, create_tool_llm

TOOLS = [
    # Time and document search tools
    get_current_time,
    search_it_policy,
    search_troubleshooting_guide,
    search_all_documents,
    # Ticket CRUD operations
    create_ticket,
    get_ticket,
    search_tickets,
    get_my_open_tickets,
    delete_ticket,
    # Ticket updates
    update_ticket_status,
    update_ticket_priority,
    add_ticket_comment,
    assign_ticket,
    add_tags_to_ticket,
    set_ticket_category,
    set_ticket_due_date,
]

def agent_node(state: AgentState) -> AgentState:
    """Agent decides to use tools OR provide final answer.

    This is the main agent loop node. The agent analyzes the conversation
    and decides whether to:
    1. Call tools to gather more information
    2. Provide a final answer if it has enough information

    Args:
        state: Current agent state.

    Returns:
        Updated agent state with either tool calls or final answer.
    """
    llm_with_tools = create_tool_llm(TOOLS)

    messages = build_base_messages(state, AGENT_SYSTEM_PROMPT)

    response = llm_with_tools.invoke(messages)
    new_iteration = state.get("iteration", 0) + 1

    return {
        "messages": [response],
        "iteration": new_iteration,
        "next_action": "tools" if response.tool_calls else "end",
    }


def _emit_agent_decision(callbacks: dict, response, iteration: int) -> str:
    """Emit event based on agent decision.

    Args:
        callbacks: Event callbacks dictionary.
        response: LLM response with potential tool calls or answer.
        iteration: Current iteration number.

    Returns:
        Next action based on tool calls.
    """
    if response.tool_calls:
        tool_names = [tc.get("name", "unknown") for tc in response.tool_calls]
        tool_list = ", ".join(tool_names) if tool_names else "unknown"
        callbacks["on_status"](
            f"Agent calling tools: {tool_list}",
            node_name="agent",
            data={"tool_names": tool_names},
        )
        return "tools"
    else:
        callbacks["on_status"](
            "Agent providing final answer",
            node_name="agent",
        )
        return "end"


def create_agent_node_with_events(
    emitter: EventEmitter,
) -> Callable[[AgentState], AgentState]:
    """Create an agent node with event emission.

    Args:
        emitter: EventEmitter instance for emitting events.

    Returns:
        Agent node function with event emission.
    """
    callbacks = create_event_callbacks(emitter)

    def agent_node_with_events(state: AgentState) -> AgentState:
        """Agent node with event emission."""
        iteration = state.get("iteration", 0) + 1

        callbacks["on_node_start"]("agent", iteration=iteration)
        callbacks["on_agent_thinking"](iteration=iteration)

        llm_with_tools = create_tool_llm(TOOLS)

        messages = build_base_messages(state, AGENT_SYSTEM_PROMPT)

        response = llm_with_tools.invoke(messages)
        new_iteration = state.get("iteration", 0) + 1

        next_action = _emit_agent_decision(callbacks, response, iteration)

        callbacks["on_node_end"]("agent", iteration=iteration)

        return {
            "messages": [response],
            "iteration": new_iteration,
            "next_action": next_action,
        }

    return agent_node_with_events
