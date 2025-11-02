"""Middleware and callbacks for workflow event tracking."""

from typing import Any, Dict, Optional

from .emitter import EventEmitter, EventType


def create_event_callbacks(emitter: EventEmitter) -> Dict[str, Any]:
    """Create callback functions for workflow event tracking.

    These callbacks can be used with LangGraph's callback system
    to emit events at various points in the workflow execution.

    Args:
        emitter: EventEmitter instance to emit events to.

    Returns:
        Dictionary of callback functions.
    """

    def on_workflow_start(data: Optional[Dict[str, Any]] = None) -> None:
        """Called when workflow starts."""
        emitter.emit(
            EventType.WORKFLOW_START,
            data={
                "message": "Workflow execution started",
                **(data or {}),
            },
        )

    def on_workflow_end(data: Optional[Dict[str, Any]] = None) -> None:
        """Called when workflow ends."""
        emitter.emit(
            EventType.WORKFLOW_END,
            data={
                "message": "Workflow execution completed",
                **(data or {}),
            },
        )

    def on_workflow_error(error: str, data: Optional[Dict[str, Any]] = None) -> None:
        """Called when workflow encounters an error."""
        emitter.emit(
            EventType.WORKFLOW_ERROR,
            data={
                "message": "Workflow execution error",
                "error": error,
                **(data or {}),
            },
        )

    def on_node_start(
        node_name: str,
        iteration: Optional[int] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Called when a node starts execution."""
        emitter.emit(
            EventType.NODE_START,
            data={
                "node_name": node_name,
                "message": f"Entering node: {node_name}",
                "iteration": iteration,
                **(data or {}),
            },
        )

    def on_node_end(
        node_name: str,
        iteration: Optional[int] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Called when a node finishes execution."""
        emitter.emit(
            EventType.NODE_END,
            data={
                "node_name": node_name,
                "message": f"Completed node: {node_name}",
                "iteration": iteration,
                **(data or {}),
            },
        )

    def on_node_error(
        node_name: str,
        error: str,
        iteration: Optional[int] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Called when a node encounters an error."""
        emitter.emit(
            EventType.NODE_ERROR,
            data={
                "node_name": node_name,
                "message": f"Error in node: {node_name}",
                "error": error,
                "iteration": iteration,
                **(data or {}),
            },
        )

    def on_tool_start(
        tool_name: str,
        iteration: Optional[int] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Called when a tool starts execution."""
        emitter.emit(
            EventType.TOOL_START,
            data={
                "tool_name": tool_name,
                "message": f"Executing tool: {tool_name}",
                "iteration": iteration,
                **(data or {}),
            },
        )

    def on_tool_end(
        tool_name: str,
        iteration: Optional[int] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Called when a tool finishes execution."""
        emitter.emit(
            EventType.TOOL_END,
            data={
                "tool_name": tool_name,
                "message": f"Tool completed: {tool_name}",
                "iteration": iteration,
                **(data or {}),
            },
        )

    def on_tool_error(
        tool_name: str,
        error: str,
        iteration: Optional[int] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Called when a tool encounters an error."""
        emitter.emit(
            EventType.TOOL_ERROR,
            data={
                "tool_name": tool_name,
                "message": f"Tool error: {tool_name}",
                "error": error,
                "iteration": iteration,
                **(data or {}),
            },
        )

    def on_agent_thinking(
        iteration: Optional[int] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Called when agent is thinking/processing."""
        emitter.emit(
            EventType.AGENT_THINKING,
            data={
                "node_name": "agent",
                "message": "Agent is analyzing the request...",
                "iteration": iteration,
                **(data or {}),
            },
        )

    def on_agent_response(
        message: str,
        iteration: Optional[int] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Called when agent generates a response."""
        emitter.emit(
            EventType.AGENT_RESPONSE,
            data={
                "node_name": "agent",
                "message": message,
                "iteration": iteration,
                **(data or {}),
            },
        )

    def on_router_decision(
        decision: str,
        iteration: Optional[int] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Called when router makes a decision."""
        emitter.emit(
            EventType.ROUTER_DECISION,
            data={
                "node_name": "router",
                "message": f"Router decision: {decision}",
                "iteration": iteration,
                "decision": decision,
                **(data or {}),
            },
        )

    def on_status(
        message: str,
        node_name: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Called to send a status update."""
        emitter.emit(
            EventType.STATUS,
            data={
                "node_name": node_name,
                "message": message,
                **(data or {}),
            },
        )

    def on_token(
        token: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Called when streaming a token."""
        emitter.emit(
            EventType.TOKEN,
            data={
                "message": token,
                **(data or {}),
            },
        )

    def on_done(
        message: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Called when processing is complete."""
        emitter.emit(
            EventType.DONE,
            data={
                "message": message or "Processing complete",
                **(data or {}),
            },
        )

    return {
        "on_workflow_start": on_workflow_start,
        "on_workflow_end": on_workflow_end,
        "on_workflow_error": on_workflow_error,
        "on_node_start": on_node_start,
        "on_node_end": on_node_end,
        "on_node_error": on_node_error,
        "on_tool_start": on_tool_start,
        "on_tool_end": on_tool_end,
        "on_tool_error": on_tool_error,
        "on_agent_thinking": on_agent_thinking,
        "on_agent_response": on_agent_response,
        "on_router_decision": on_router_decision,
        "on_status": on_status,
        "on_token": on_token,
        "on_done": on_done,
    }
