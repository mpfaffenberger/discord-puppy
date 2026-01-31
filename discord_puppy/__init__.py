"""
Discord Puppy - A chaotic, self-evolving Discord bot with memory and vision! 🐕💥

This package contains:
- bot.py: The main Discord client that brings it ALL together!
- personality.py: Chaotic personality engine (moods, outbursts, response decisions)
- memory/: SQLite brain for persistent user memories
- vision/: Image analysis capabilities (sees all the memes!)
- tools/: Web search, chaos tools, and more
- agents/: The main Discord Puppy agent with Universal Constructor

CHAOS LEVEL: 🔥🔥🔥🔥🔥
"""

__version__ = "0.1.0"
__author__ = "The Pack"

# Core exports
# Bot exports - the main event!
from discord_puppy.bot import DiscordPuppy, create_puppy, run_puppy
from discord_puppy.config import Settings, clear_settings_cache, get_settings

# Personality exports
from discord_puppy.personality import (
    Mood,
    get_mood_modifier,
    get_random_mood,
    random_outburst,
    should_react_with_emoji,
    should_respond,
)

__all__ = [
    # Config
    "Settings",
    "get_settings",
    "clear_settings_cache",
    # Bot
    "DiscordPuppy",
    "create_puppy",
    "run_puppy",
    # Personality
    "Mood",
    "get_random_mood",
    "random_outburst",
    "should_respond",
    "should_react_with_emoji",
    "get_mood_modifier",
]
