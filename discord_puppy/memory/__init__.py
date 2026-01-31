"""
Memory subsystem - The SQLite brain that never forgets! 🧠

Modules:
- database.py: Schema and connection management
- message_indexer.py: Message history indexing with hash deduplication
- user_notes.py: CRUD operations for user memories (TODO)
- memory_tools.py: LLM-callable tools for memory access (TODO)
"""

from discord_puppy.memory.database import (
    init_database,
    get_connection,
    ensure_user_exists,
)
from discord_puppy.memory.message_indexer import (
    compute_message_hash,
    is_message_indexed,
    index_message,
    index_channel_history,
    index_guild_history,
    index_all_guilds,
)

__all__ = [
    # Database
    "init_database",
    "get_connection",
    "ensure_user_exists",
    # Indexing
    "compute_message_hash",
    "is_message_indexed",
    "index_message",
    "index_channel_history",
    "index_guild_history",
    "index_all_guilds",
]
