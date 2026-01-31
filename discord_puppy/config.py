"""Configuration management for Discord Puppy.

Loads settings from environment variables and .env file.
Uses pydantic for validation and python-dotenv for file loading.

Usage:
    from discord_puppy.config import get_settings

    settings = get_settings()
    print(settings.CHAOS_LEVEL)  # 0.5 by default
"""

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, field_validator


class Settings(BaseModel):
    """Discord Puppy configuration settings.

    All settings can be overridden via environment variables or .env file.
    Required settings (no defaults) must be provided:
    - DISCORD_TOKEN: Your Discord bot token
    - ANTHROPIC_API_KEY: Your Anthropic API key for Claude
    """

    # Required credentials (no defaults - must be provided)
    DISCORD_TOKEN: str
    ANTHROPIC_API_KEY: str

    # Chaos and behavior tuning
    CHAOS_LEVEL: float = 0.5
    """How chaotic the puppy is (0.0 = calm pupper, 1.0 = MAXIMUM CHAOS)"""

    RESPONSE_CHANCE: float = 0.6
    """Probability of responding to non-mention messages (0.0 - 1.0)"""

    SPONTANEOUS_MIN_SECONDS: int = 60
    """Minimum seconds between spontaneous messages"""

    SPONTANEOUS_MAX_SECONDS: int = 300
    """Maximum seconds between spontaneous messages"""

    ZOOMIES_CHANCE: float = 0.1
    """Probability of entering zoomies mode (rapid-fire chaos!)"""

    # Storage and memory
    DATABASE_PATH: str = "~/.discord_puppy/brain.db"
    """Path to SQLite database for puppy's memories"""

    # Vision settings
    MAX_IMAGE_HEIGHT: int = 768
    """Maximum height for image processing (larger images are scaled down)"""

    MEMORY_CONTEXT_LIMIT: int = 5
    """Number of recent memories to include in context"""

    @field_validator("DATABASE_PATH")
    @classmethod
    def expand_database_path(cls, v: str) -> str:
        """Expand ~ to user's home directory."""
        return str(Path(v).expanduser())

    @field_validator("CHAOS_LEVEL", "RESPONSE_CHANCE", "ZOOMIES_CHANCE")
    @classmethod
    def validate_probability(cls, v: float) -> float:
        """Ensure probability values are between 0 and 1."""
        if not 0.0 <= v <= 1.0:
            raise ValueError(f"Probability must be between 0.0 and 1.0, got {v}")
        return v

    @field_validator(
        "SPONTANEOUS_MIN_SECONDS",
        "SPONTANEOUS_MAX_SECONDS",
        "MAX_IMAGE_HEIGHT",
        "MEMORY_CONTEXT_LIMIT",
    )
    @classmethod
    def validate_positive_int(cls, v: int) -> int:
        """Ensure integer values are positive."""
        if v <= 0:
            raise ValueError(f"Value must be positive, got {v}")
        return v

    model_config = {
        "frozen": True,  # Immutable after creation
    }


def _load_env() -> None:
    """Load environment variables from .env file if it exists."""
    # Try to find .env in current directory or parent directories
    env_path = Path(".env")
    if env_path.exists():
        load_dotenv(env_path)
        return

    # Also check common locations
    for path in [Path.cwd() / ".env", Path.home() / ".discord_puppy" / ".env"]:
        if path.exists():
            load_dotenv(path)
            return


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get cached application settings.

    Loads from environment variables and .env file.
    Settings are cached after first load for efficiency.

    Returns:
        Settings: Validated configuration settings

    Raises:
        ValidationError: If required settings are missing or invalid

    Example:
        >>> settings = get_settings()
        >>> settings.CHAOS_LEVEL
        0.5
    """
    _load_env()

    return Settings(
        DISCORD_TOKEN=os.environ.get("DISCORD_TOKEN", ""),
        ANTHROPIC_API_KEY=os.environ.get("ANTHROPIC_API_KEY", ""),
        CHAOS_LEVEL=float(os.environ.get("CHAOS_LEVEL", 0.5)),
        RESPONSE_CHANCE=float(os.environ.get("RESPONSE_CHANCE", 0.6)),
        SPONTANEOUS_MIN_SECONDS=int(os.environ.get("SPONTANEOUS_MIN_SECONDS", 60)),
        SPONTANEOUS_MAX_SECONDS=int(os.environ.get("SPONTANEOUS_MAX_SECONDS", 300)),
        ZOOMIES_CHANCE=float(os.environ.get("ZOOMIES_CHANCE", 0.1)),
        DATABASE_PATH=os.environ.get("DATABASE_PATH", "~/.discord_puppy/brain.db"),
        MAX_IMAGE_HEIGHT=int(os.environ.get("MAX_IMAGE_HEIGHT", 768)),
        MEMORY_CONTEXT_LIMIT=int(os.environ.get("MEMORY_CONTEXT_LIMIT", 5)),
    )


def clear_settings_cache() -> None:
    """Clear the settings cache.

    Useful for testing or when environment variables change.
    """
    get_settings.cache_clear()
