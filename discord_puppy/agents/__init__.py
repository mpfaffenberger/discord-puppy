"""Agents subsystem - The brain behind the chaos! 🤖

Modules:
- discord_puppy_agent.py: Main agent with Universal Constructor
  - Can create its own tools!
  - Has memory access
  - Has vision capabilities
  - Maximum chaos energy
"""

from discord_puppy.agents.discord_puppy_agent import (
    AVAILABLE_TOOLS,
    DISCORD_PUPPY_SYSTEM_PROMPT,
    DiscordPuppyAgent,
    create_discord_puppy_agent,
    get_available_tools,
    get_system_prompt,
)

__all__ = [
    "AVAILABLE_TOOLS",
    "DISCORD_PUPPY_SYSTEM_PROMPT",
    "DiscordPuppyAgent",
    "create_discord_puppy_agent",
    "get_available_tools",
    "get_system_prompt",
]
