"""Tests for prompt templates."""

from src.typhoon_it_support.prompts import AGENT_SYSTEM_PROMPT, ROUTER_SYSTEM_PROMPT


def test_agent_prompt_exists():
    """Test that agent system prompt is defined."""
    assert AGENT_SYSTEM_PROMPT is not None
    assert len(AGENT_SYSTEM_PROMPT) > 0
    assert isinstance(AGENT_SYSTEM_PROMPT, str)


def test_agent_prompt_content():
    """Test that agent prompt contains key information."""
    assert "IT support" in AGENT_SYSTEM_PROMPT
    assert "assistant" in AGENT_SYSTEM_PROMPT.lower()


def test_router_prompt_exists():
    """Test that router system prompt is defined."""
    assert ROUTER_SYSTEM_PROMPT is not None
    assert len(ROUTER_SYSTEM_PROMPT) > 0
    assert isinstance(ROUTER_SYSTEM_PROMPT, str)


def test_router_prompt_content():
    """Test that router prompt contains routing logic."""
    assert "routing" in ROUTER_SYSTEM_PROMPT.lower() or "router" in ROUTER_SYSTEM_PROMPT.lower()
    assert "continue" in ROUTER_SYSTEM_PROMPT
    assert "end" in ROUTER_SYSTEM_PROMPT

