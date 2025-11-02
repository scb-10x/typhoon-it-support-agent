"""Event emitter for workflow tracking."""

import json
from datetime import datetime
from enum import Enum
from queue import Queue
from typing import Any, Callable, Dict, Optional, Union


class EventType(str, Enum):
    """Event types for workflow tracking."""

    WORKFLOW_START = "workflow_start"
    WORKFLOW_END = "workflow_end"
    WORKFLOW_ERROR = "workflow_error"
    NODE_START = "node_start"
    NODE_END = "node_end"
    NODE_ERROR = "node_error"
    TOOL_START = "tool_start"
    TOOL_END = "tool_end"
    TOOL_ERROR = "tool_error"
    AGENT_THINKING = "agent_thinking"
    AGENT_RESPONSE = "agent_response"
    ROUTER_DECISION = "router_decision"
    STATUS = "status"
    TOKEN = "token"
    DONE = "done"
    TICKET_CREATED = "ticket_created"


class Event:
    """Event object with serialization support."""

    def __init__(
        self,
        event_type: str,
        data: Optional[Dict[str, Any]] = None,
        timestamp: Optional[str] = None,
    ):
        """Initialize event.

        Args:
            event_type: Type of event.
            data: Event data.
            timestamp: Event timestamp (auto-generated if not provided).
        """
        self.type = event_type
        self.data = data or {}
        self.timestamp = timestamp or datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary.

        Returns:
            Dictionary representation of event.
        """
        return {
            "type": self.type,
            "timestamp": self.timestamp,
            "data": self.data,
        }

    def to_json(self) -> str:
        """Convert to JSON string.

        Returns:
            JSON string representation of event.
        """
        return json.dumps(self.to_dict())

    def __getitem__(self, key: str):
        """Allow dict-like access for backward compatibility."""
        return self.to_dict()[key]

    def get(self, key: str, default=None):
        """Get item with default for backward compatibility."""
        return self.to_dict().get(key, default)


class EventEmitter:
    """Event emitter for tracking workflow progress.

    Emits events for:
    - Node start/end
    - Tool execution
    - Status updates
    - Errors
    """

    def __init__(self):
        """Initialize event emitter."""
        self.listeners: Dict[str, list] = {}
        self.events: list = []
        self.queues: list = []  # List of subscribed queues

    def on(self, event_type: str, callback: Callable):
        """Register event listener.

        Args:
            event_type: Type of event to listen for.
            callback: Function to call when event occurs.
        """
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)

    def subscribe(
        self, event_type: Optional[str] = None, callback: Optional[Callable] = None
    ) -> Optional[Queue]:
        """Subscribe to events.

        Two modes:
        1. Callback mode: subscribe(event_type, callback) - Register callback for specific event
        2. Queue mode: subscribe() - Returns a Queue that receives all events

        Args:
            event_type: Optional event type to listen for (callback mode).
            callback: Optional callback function (callback mode).

        Returns:
            Queue object for queue mode, None for callback mode.
        """
        # Queue mode: subscribe() with no arguments
        if event_type is None and callback is None:
            queue = Queue()
            self.queues.append(queue)
            return queue

        # Callback mode: subscribe(event_type, callback)
        if event_type and callback:
            self.on(event_type, callback)
            return None

        raise ValueError(
            "subscribe() requires either no arguments (queue mode) or both event_type and callback (callback mode)"
        )

    def emit(self, event_type: str, data: Optional[Dict[str, Any]] = None):
        """Emit an event.

        Args:
            event_type: Type of event.
            data: Event data.
        """
        event = Event(event_type, data)

        # Store event (as dict for backward compatibility)
        self.events.append(event.to_dict())

        # Send to all queues (as Event object)
        for queue in self.queues:
            queue.put(event)

        # Call listeners (with Event object)
        if event_type in self.listeners:
            for callback in self.listeners[event_type]:
                callback(event)

    def get_events(self, event_type: Optional[str] = None) -> list:
        """Get all events or events of specific type.

        Args:
            event_type: Optional filter by event type.

        Returns:
            List of events.
        """
        if event_type:
            return [e for e in self.events if e["type"] == event_type]
        return self.events

    def clear(self):
        """Clear all events."""
        self.events = []

    def unsubscribe(
        self,
        event_type_or_queue: Union[str, Queue],
        callback: Optional[Callable] = None,
    ):
        """Unsubscribe from events.

        Two modes:
        1. Callback mode: unsubscribe(event_type, callback) - Remove specific callback
        2. Queue mode: unsubscribe(queue) - Remove queue subscription

        Args:
            event_type_or_queue: Event type string or Queue object.
            callback: Optional callback function (callback mode only).
        """
        # Queue mode: unsubscribe(queue)
        if isinstance(event_type_or_queue, Queue):
            if event_type_or_queue in self.queues:
                self.queues.remove(event_type_or_queue)
            return

        # Callback mode: unsubscribe(event_type, callback)
        event_type = event_type_or_queue
        if callback and event_type in self.listeners:
            if callback in self.listeners[event_type]:
                self.listeners[event_type].remove(callback)


def create_event_callbacks(emitter: EventEmitter) -> Dict[str, Callable]:
    """Create standard callback functions for workflow events.

    Args:
        emitter: EventEmitter instance.

    Returns:
        Dictionary of callback functions.
    """

    def on_node_start(node_name: str, **kwargs):
        """Emit node start event."""
        emitter.emit("node_start", {"node": node_name, **kwargs})

    def on_node_end(node_name: str, **kwargs):
        """Emit node end event."""
        emitter.emit("node_end", {"node": node_name, **kwargs})

    def on_tool_start(tool_name: str, **kwargs):
        """Emit tool start event."""
        emitter.emit("tool_start", {"tool": tool_name, **kwargs})

    def on_tool_end(tool_name: str, **kwargs):
        """Emit tool end event."""
        emitter.emit("tool_end", {"tool": tool_name, **kwargs})

    def on_status(message: str, **kwargs):
        """Emit status update event."""
        emitter.emit("status", {"message": message, **kwargs})

    def on_error(error: str, **kwargs):
        """Emit error event."""
        emitter.emit("error", {"error": error, **kwargs})

    def on_agent_thinking(**kwargs):
        """Emit agent thinking event."""
        emitter.emit("agent_thinking", kwargs)

    def on_agent_response(message: str, **kwargs):
        """Emit agent response event."""
        emitter.emit("agent_response", {"message": message, **kwargs})

    def on_router_decision(decision: str, **kwargs):
        """Emit router decision event."""
        emitter.emit("router_decision", {"decision": decision, **kwargs})

    def on_workflow_start(data: Optional[Dict[str, Any]] = None, **kwargs):
        """Emit workflow start event."""
        emitter.emit("workflow_start", {**(data or {}), **kwargs})

    def on_workflow_end(data: Optional[Dict[str, Any]] = None, **kwargs):
        """Emit workflow end event."""
        emitter.emit("workflow_end", {**(data or {}), **kwargs})

    def on_done(message: str = "", data: Optional[Dict[str, Any]] = None, **kwargs):
        """Emit workflow completion event."""
        emitter.emit("done", {"message": message, **(data or {}), **kwargs})

    def on_token(token: str, **kwargs):
        """Emit token streaming event."""
        emitter.emit("token", {"message": token, **kwargs})

    return {
        "on_node_start": on_node_start,
        "on_node_end": on_node_end,
        "on_tool_start": on_tool_start,
        "on_tool_end": on_tool_end,
        "on_status": on_status,
        "on_error": on_error,
        "on_agent_thinking": on_agent_thinking,
        "on_agent_response": on_agent_response,
        "on_router_decision": on_router_decision,
        "on_workflow_start": on_workflow_start,
        "on_workflow_end": on_workflow_end,
        "on_done": on_done,
        "on_token": on_token,
    }
