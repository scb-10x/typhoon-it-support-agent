"""Application settings and configuration."""

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    """Application settings."""

    typhoon_api_key: Optional[str] = None
    typhoon_base_url: str = "https://api.opentyphoon.ai/v1"
    typhoon_model: str = "typhoon-v2.5-30b-a3b-instruct"
    temperature: float = 0.7
    max_tokens: int = 8192
    max_iterations: int = 30
    debug: bool = False
    checkpointer_type: str = "memory"
    sqlite_checkpoint_path: str = "./checkpoints.db"

    def __post_init__(self) -> None:
        """Load settings from environment variables."""
        self.typhoon_api_key = os.getenv("TYPHOON_API_KEY", self.typhoon_api_key)
        self.typhoon_base_url = os.getenv("TYPHOON_BASE_URL", self.typhoon_base_url)
        self.typhoon_model = os.getenv("TYPHOON_MODEL", self.typhoon_model)
        self.temperature = float(os.getenv("TEMPERATURE", str(self.temperature)))
        self.max_tokens = int(os.getenv("MAX_TOKENS", str(self.max_tokens)))
        self.max_iterations = int(os.getenv("MAX_ITERATIONS", str(self.max_iterations)))
        self.checkpointer_type = os.getenv("CHECKPOINTER_TYPE", self.checkpointer_type)
        self.sqlite_checkpoint_path = os.getenv(
            "SQLITE_CHECKPOINT_PATH", self.sqlite_checkpoint_path
        )

        # Only override debug from env if explicitly set
        debug_env = os.getenv("DEBUG")
        if debug_env is not None:
            self.debug = debug_env.lower() == "true"


_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get application settings singleton."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
