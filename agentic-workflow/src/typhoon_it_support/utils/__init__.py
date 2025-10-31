"""Utility modules for the Typhoon IT Support system."""

from .llm_factory import (
    create_llm,
    create_routing_llm,
    create_streaming_llm,
    create_tool_llm,
)
from .message_builder import (
    add_instruction,
    build_base_messages,
    build_conversation_summary,
    has_tool_results,
)
from .routing_constants import COMPLETION_PHRASES, ESCALATION_PHRASES
from .typhoon_patch import apply_typhoon_api_patch

__all__ = [
    "apply_typhoon_api_patch",
    "create_llm",
    "create_tool_llm",
    "create_routing_llm",
    "create_streaming_llm",
    "build_base_messages",
    "add_instruction",
    "build_conversation_summary",
    "has_tool_results",
    "COMPLETION_PHRASES",
    "ESCALATION_PHRASES",
]

