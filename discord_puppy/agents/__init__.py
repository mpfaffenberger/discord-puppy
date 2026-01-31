"""
Agents subsystem - The brain behind the chaos! 🤖

Modules:
- puppy_agent.py: Main agent that generates responses
  - Chaotic personality
  - Fallback responses when AI not available
  - Spontaneous message generation
"""

from discord_puppy.agents.puppy_agent import DiscordPuppyAgent, get_puppy_agent

__all__ = ["DiscordPuppyAgent", "get_puppy_agent"]
