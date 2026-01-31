"""
Discord Puppy - A chaotic, self-evolving Discord bot with memory and vision! 🐕💥

This package contains:
- memory/: SQLite brain for persistent user memories
- vision/: Image analysis capabilities (sees all the memes!)
- tools/: Web search, chaos tools, and more
- agents/: The main Discord Puppy agent with Universal Constructor

CHAOS LEVEL: 🔥🔥🔥🔥🔥
"""

__version__ = "0.1.0"
__author__ = "The Pack"

# Core exports
from discord_puppy.config import Settings, get_settings, clear_settings_cache

__all__ = ['Settings', 'get_settings', 'clear_settings_cache']
