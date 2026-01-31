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
from discord_puppy.tools.discord_send import register_discord_send_message
from discord_puppy.tools.memory_tools import (
    register_search_messages,
    register_get_user_notes,
    register_record_user_note,
    register_list_users,
    register_get_recent_messages,
)

logger = logging.getLogger("discord_puppy.agent")

# Register our custom tools (these are registration functions, not the tools themselves)
TOOL_REGISTRY["discord_send_message"] = register_discord_send_message
TOOL_REGISTRY["search_messages"] = register_search_messages
TOOL_REGISTRY["get_user_notes"] = register_get_user_notes
TOOL_REGISTRY["record_user_note"] = register_record_user_note
TOOL_REGISTRY["list_users"] = register_list_users
TOOL_REGISTRY["get_recent_messages"] = register_get_recent_messages


class DiscordPuppyAgent(BaseAgent):
    """The chaotic brain of Discord Puppy.
    
    Just use run_with_mcp() directly - it handles conversation history.
    """

    MODEL_NAME = "luminon"

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
- When doing tasks, use discord_send_message between tool calls to update chat.

MEMORY TOOLS (use these to remember things!):
- search_messages(query) - search past messages
- get_user_notes(username) - get notes about a user
- record_user_note(username, note) - save a note about someone
- list_users() - see who you know
- get_recent_messages() - see recent chat

Be a good puppy - remember things about your friends! 🐕"""

    def get_available_tools(self) -> List[str]:
        return [
            "universal_constructor",
            "discord_send_message",
            # Memory tools
            "search_messages",
            "get_user_notes", 
            "record_user_note",
            "list_users",
            "get_recent_messages",
        ]


# Singleton (for backwards compat, prefer create_puppy_agent for concurrency)
_puppy_agent: Optional[DiscordPuppyAgent] = None


def get_puppy_agent() -> DiscordPuppyAgent:
    """Get the singleton puppy agent instance.
    
    WARNING: Don't use this for concurrent tasks! Use create_puppy_agent() instead.
    """
    global _puppy_agent
    if _puppy_agent is None:
        logger.info("🐕 Creating DiscordPuppyAgent (singleton)")
        _puppy_agent = DiscordPuppyAgent()
    return _puppy_agent


def create_puppy_agent() -> DiscordPuppyAgent:
    """Create a fresh puppy agent instance.
    
    Use this for concurrent tasks so each task has isolated state!
    """
    logger.debug("🐕 Creating fresh DiscordPuppyAgent instance")
    return DiscordPuppyAgent()