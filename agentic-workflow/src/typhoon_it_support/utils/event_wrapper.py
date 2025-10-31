"""Generic event wrapper utilities for node functions."""

from functools import wraps
from typing import Callable

from ..events import EventEmitter, create_event_callbacks
from ..models import AgentState


def with_node_events(
    node_name: str, emitter: EventEmitter
) -> Callable[[Callable], Callable]:
    """Decorator to wrap a node function with event emission.

    Args:
        node_name: Name of the node for event tracking.
        emitter: EventEmitter instance.

    Returns:
        Decorator function.
    """
    callbacks = create_event_callbacks(emitter)

    def decorator(node_func: Callable[[AgentState], AgentState]) -> Callable:
        @wraps(node_func)
        def wrapper(state: AgentState) -> AgentState:
            iteration = state.get("iteration", 0)

            callbacks["on_node_start"](node_name, iteration=iteration)

            result = node_func(state, callbacks=callbacks)

            callbacks["on_node_end"](node_name, iteration=iteration)

            return result

        return wrapper

    return decorator



