"""Tool execution node for the agent workflow."""

from typing import Callable

from langgraph.prebuilt import ToolNode

from ..events import EventEmitter, create_event_callbacks
from ..models import AgentState
from .agent_node import TOOLS

# Create tool execution node
tool_executor = ToolNode(TOOLS)


def tools_node(state: AgentState) -> AgentState:
    """Act phase: Execute tool calls.

    This node represents the "Act" phase of the agent loop.
    It executes the tools that the agent decided to use.

    Args:
        state: Current agent state with tool calls.

    Returns:
        Updated agent state with tool results.
    """
    # Execute tools
    result = tool_executor.invoke(state)

    # Track which documents were searched (for context awareness)
    searched_docs = state.get("searched_documents", [])
    for message in result.get("messages", []):
        if hasattr(message, "name"):
            if "search" in message.name and message.name not in searched_docs:
                searched_docs.append(message.name)

    # Track active tickets (for context awareness)
    active_tickets = state.get("active_tickets", [])
    for message in result.get("messages", []):
        if hasattr(message, "content") and "#" in str(message.content):
            # Extract ticket IDs from tool results
            import re

            ticket_ids = re.findall(r"#(\d+)", str(message.content))
            for tid in ticket_ids:
                ticket_id = int(tid)
                if ticket_id not in active_tickets:
                    active_tickets.append(ticket_id)

    return {
        "messages": result["messages"],
        "searched_documents": searched_docs,
        "active_tickets": active_tickets,
        "next_action": "observe",
    }


def create_tools_node_with_events(
    emitter: EventEmitter,
) -> Callable[[AgentState], AgentState]:
    """Create a tools node with event emission.

    Args:
        emitter: EventEmitter instance for emitting events.

    Returns:
        Tools node function with event emission.
    """
    callbacks = create_event_callbacks(emitter)

    def tools_node_with_events(state: AgentState) -> AgentState:
        """Tools node with event emission."""
        iteration = state.get("iteration", 0)

        # Emit node start event
        callbacks["on_node_start"]("tools", iteration=iteration)

        # Extract tool names from state
        tool_names = []
        if state.get("messages"):
            for msg in state["messages"]:
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tc in msg.tool_calls:
                        tool_name = tc.get("name", "unknown")
                        tool_names.append(tool_name)
                        # Emit tool start event
                        callbacks["on_tool_start"](
                            tool_name,
                            iteration=iteration,
                            data={"args": tc.get("args", {})},
                        )

        # Execute tools
        result = tools_node(state)

        # Check for ticket creation and emit ticket_created event
        import re

        for msg in result.get("messages", []):
            if hasattr(msg, "name") and msg.name == "create_ticket":
                # Extract ticket ID from the result
                content = str(msg.content)
                ticket_match = re.search(r"Ticket ID\*\*:\s*#(\d+)", content)
                if ticket_match:
                    ticket_id = int(ticket_match.group(1))
                    # Extract subject if available
                    subject_match = re.search(r"Subject\*\*:\s*([^\n]+)", content)
                    subject = subject_match.group(1) if subject_match else "New Ticket"

                    # Emit ticket created event
                    emitter.emit(
                        "ticket_created",
                        {
                            "ticket_id": ticket_id,
                            "subject": subject,
                            "message": f"Ticket #{ticket_id} created successfully",
                        },
                    )

        # Emit tool end events
        for tool_name in tool_names:
            callbacks["on_tool_end"](tool_name, iteration=iteration)

        # Emit summary status
        if tool_names:
            callbacks["on_status"](
                f"Executed {len(tool_names)} tool(s): {', '.join(tool_names)}",
                node_name="tools",
                data={"tool_count": len(tool_names)},
            )

        # Emit node end event
        callbacks["on_node_end"]("tools", iteration=iteration)

        return result

    return tools_node_with_events
