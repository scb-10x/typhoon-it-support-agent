"""Tests for configuration module."""

from src.typhoon_it_support.config import Settings, get_settings


def test_settings_initialization():
    """Test that settings can be initialized with defaults."""
    settings = Settings()
    assert settings.typhoon_model == "typhoon-v2.5-30b-a3b-instruct"
    assert settings.typhoon_base_url == "https://api.opentyphoon.ai/v1"
    assert settings.temperature == 0.7
    assert settings.max_tokens == 1024
    assert settings.max_iterations == 10
    assert settings.debug is False


def test_settings_custom_values():
    """Test that settings can be initialized with custom values."""
    settings = Settings(
        typhoon_model="typhoon-v2.5-30b-a3b",
        typhoon_base_url="https://custom.url/v1",
        temperature=0.5,
        max_tokens=512,
        max_iterations=20,
        debug=True,
    )
    assert settings.typhoon_model == "typhoon-v2.5-30b-a3b"
    assert settings.typhoon_base_url == "https://custom.url/v1"
    assert settings.temperature == 0.5
    assert settings.max_tokens == 512
    assert settings.max_iterations == 20
    assert settings.debug is True


def test_get_settings_singleton():
    """Test that get_settings returns the same instance."""
    settings1 = get_settings()
    settings2 = get_settings()
    assert settings1 is settings2

