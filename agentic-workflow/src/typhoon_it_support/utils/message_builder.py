"""Utilities for building message chains."""

from langchain_core.messages import SystemMessage

from ..models import AgentState


def build_base_messages(state: AgentState, system_prompt: str) -> list:
    """Build base message chain with system prompt and state messages.

    Args:
        state: Current agent state.
        system_prompt: System prompt to use.

    Returns:
        List of messages starting with system prompt.
    """
    messages = [SystemMessage(content=system_prompt)]
    messages.extend(state["messages"])
    return messages


def add_instruction(messages: list, instruction: str) -> list:
    """Add instruction message to message chain.

    Args:
        messages: Existing message chain.
        instruction: Instruction text to add.

    Returns:
        Updated message chain with instruction added.
    """
    messages.append(SystemMessage(content=instruction))
    return messages


def build_conversation_summary(state: AgentState, max_messages: int = 10) -> str:
    """Build conversation summary from state messages.

    Args:
        state: Current agent state.
        max_messages: Maximum number of recent messages to include.

    Returns:
        Formatted conversation summary.
    """
    conversation_summary = []

    for msg in state["messages"]:
        if hasattr(msg, "type"):
            if msg.type == "human":
                conversation_summary.append(f"User: {msg.content}")
            elif msg.type == "ai":
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    tool_names = [tc.get("name", "unknown") for tc in msg.tool_calls]
                    conversation_summary.append(f"Agent used tools: {', '.join(tool_names)}")
                elif msg.content:
                    conversation_summary.append(f"Agent: {msg.content[:200]}")
            elif msg.type == "tool":
                conversation_summary.append(f"Tool result: {msg.content[:200]}")

    return "\n".join(conversation_summary[-max_messages:])


def has_tool_results(state: AgentState, look_back: int = 5) -> bool:
    """Check if recent messages contain tool results.

    Args:
        state: Current agent state.
        look_back: Number of recent messages to check.

    Returns:
        True if tool results found, False otherwise.
    """
    for msg in reversed(state["messages"][-look_back:]):
        if hasattr(msg, "type") and msg.type == "tool":
            return True
    return False



