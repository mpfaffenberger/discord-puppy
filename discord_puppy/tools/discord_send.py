"""
Discord Send Message Tool 🐕

Allows the puppy to send messages to the current Discord channel.
"""

import asyncio
from typing import Optional, Any
import discord
from pydantic_ai import RunContext

# Global channel context
_current_channel: Optional[discord.abc.Messageable] = None
_event_loop: Optional[asyncio.AbstractEventLoop] = None


def set_current_channel(channel: discord.abc.Messageable, loop: asyncio.AbstractEventLoop = None) -> None:
    """Set the current channel for sending messages."""
    global _current_channel, _event_loop
    _current_channel = channel
    _event_loop = loop or asyncio.get_event_loop()


def get_current_channel() -> Optional[discord.abc.Messageable]:
    """Get the current channel."""
    return _current_channel


def register_discord_send_message(agent):
    """Register the discord_send_message tool."""
    
    @agent.tool
    def discord_send_message(context: RunContext, message: str = "") -> dict[str, Any]:
        """Send a message to the current Discord channel.
        
        Use this to update the chat about what you're doing between tool calls.
        Keep updates SHORT - just a few words about current status.
        
        Args:
            context: The pydantic-ai runtime context.
            message: The message to send (keep it brief!)
            
        Returns:
            Success status and any error message.
        """
        global _current_channel, _event_loop
        
        if not _current_channel:
            return {"success": False, "error": "No channel set"}
        
        if not message or not str(message).strip():
            return {"success": False, "error": "Empty message"}
        
        message = str(message).strip()
        
        # Truncate if too long
        if len(message) > 200:
            message = message[:197] + "..."
        
        try:
            # Schedule the coroutine on the event loop
            future = asyncio.run_coroutine_threadsafe(
                _current_channel.send(message),
                _event_loop
            )
            # Wait for it to complete (with timeout)
            future.result(timeout=5.0)
            return {"success": True, "message": message}
        except Exception as e:
            return {"success": False, "error": str(e)}
