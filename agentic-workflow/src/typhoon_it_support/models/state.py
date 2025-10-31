"""State definitions for the agent workflow."""

from typing import Annotated, TypedDict, Optional, List, Dict

from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """State for the agent workflow.
    
    Attributes:
        messages: List of messages in the conversation.
        iteration: Current iteration count.
        next_action: The next action to take.
        active_tickets: List of ticket IDs created or referenced in this session.
        searched_documents: List of document sources that have been searched.
        user_info: Optional user information for ticket creation.
    """

    messages: Annotated[list, add_messages]
    iteration: int
    next_action: str
    active_tickets: List[int]
    searched_documents: List[str]
    user_info: Optional[Dict[str, str]]

