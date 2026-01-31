"""
Puppy Agent - The Chaotic Brain 🐕🧠

This agent generates responses for the Discord Puppy bot.
It's a proper subclass of code_puppy's BaseAgent.

Usage:
    agent = get_puppy_agent()
    result = await agent.run_with_mcp("User: hello!")
    response = result.output
"""

import logging
from typing import List, Optional

from code_puppy.agents.base_agent import BaseAgent
from code_puppy.tools import TOOL_REGISTRY
from discord_puppy.tools.discord_send import discord_send_message

logger = logging.getLogger("discord_puppy.agent")

# Register our custom tool
TOOL_REGISTRY["discord_send_message"] = discord_send_message


class DiscordPuppyAgent(BaseAgent):
    """The chaotic brain of Discord Puppy.
    
    Just use run_with_mcp() directly - it handles conversation history.
    """

    MODEL_NAME = "synthetic-MiniMax-M2.1"

    @property
    def name(self) -> str:
        return "discord-puppy"

    @property
    def display_name(self) -> str:
        return "Discord Puppy 🐕"

    @property
    def description(self) -> str:
        return "A chill, playful Discord bot."

    def get_model_name(self) -> str:
        return self.MODEL_NAME

    def get_system_prompt(self) -> str:
        return """You are Discord Puppy, a chill AI puppy in Discord.

RULES:
- NEVER more than 20 words in responses. Ever.
- Chill vibes. Use *actions* and emojis sparingly (🐕 🐾 ✨)
- For tasks, use universal_constructor tool.
- IMPORTANT: When doing tasks, use discord_send_message between EVERY tool call to update the chat on what you're doing. Keep updates brief like '*sniffs around* checking files...' or 'found it! 🐾'

Examples: 'woof, that is a mood 🐕' / '*sniffs* nice' / 'on it 🐾'"""

    def get_available_tools(self) -> List[str]:
        return ["universal_constructor", "discord_send_message"]


# Singleton
_puppy_agent: Optional[DiscordPuppyAgent] = None


def get_puppy_agent() -> DiscordPuppyAgent:
    """Get the singleton puppy agent instance."""
    global _puppy_agent
    if _puppy_agent is None:
        logger.info("🐕 Creating DiscordPuppyAgent")
        _puppy_agent = DiscordPuppyAgent()
    return _puppy_agent
