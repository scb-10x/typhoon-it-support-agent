"""Pytest configuration and fixtures."""

import pytest

from src.typhoon_it_support.config import Settings
from src.typhoon_it_support.models import AgentState


@pytest.fixture
def mock_settings() -> Settings:
    """Provide mock settings for testing."""
    return Settings(
        typhoon_api_key="test-key",
        typhoon_base_url="https://api.opentyphoon.ai/v1",
        typhoon_model="typhoon-v2.5-30b-a3b-instruct",
        temperature=0.0,
        max_tokens=512,
        max_iterations=5,
        debug=False,
    )


@pytest.fixture
def basic_state() -> AgentState:
    """Provide a basic agent state for testing."""
    return {
        "messages": [],
        "iteration": 0,
        "next_action": "start",
    }
