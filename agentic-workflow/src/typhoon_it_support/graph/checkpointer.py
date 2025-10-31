"""Checkpointer utilities for workflow memory management."""

from typing import Optional

from langgraph.checkpoint.memory import InMemorySaver


def create_checkpointer() -> InMemorySaver:
    """Create a checkpointer based on configuration.

    Returns:
        InMemorySaver for in-memory checkpointing.
    """
    return InMemorySaver()


_checkpointer: Optional[InMemorySaver] = None


def get_checkpointer() -> InMemorySaver:
    """Get singleton checkpointer instance.

    Returns:
        InMemorySaver checkpointer instance.
    """
    global _checkpointer
    if _checkpointer is None:
        _checkpointer = create_checkpointer()
    return _checkpointer
