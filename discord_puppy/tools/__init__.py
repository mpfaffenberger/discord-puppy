"""
Discord Puppy Tools 🐕

Custom tools for the Discord Puppy agent.
"""

from discord_puppy.tools.discord_send import (
    register_discord_send_message,
    set_current_channel,
    get_current_channel,
)
from discord_puppy.tools.memory_tools import (
    register_search_messages,
    register_get_user_notes,
    register_record_user_note,
    register_list_users,
    register_get_recent_messages,
    get_recent_messages_standalone,
)

__all__ = [
    "register_discord_send_message",
    "set_current_channel",
    "get_current_channel",
    "register_search_messages",
    "register_get_user_notes",
    "register_record_user_note",
    "register_list_users",
    "register_get_recent_messages",
    "get_recent_messages_standalone",
]
