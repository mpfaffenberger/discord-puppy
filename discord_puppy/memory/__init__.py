"""Memory subsystem - The SQLite brain that never forgets! 🧠

Modules:
- database.py: Schema and connection management
- user_notes.py: CRUD operations for user memories
- memory_tools.py: LLM-callable tools for memory access
"""

from discord_puppy.memory.database import (
    DEFAULT_DB_PATH,
    ensure_user_exists,
    get_connection,
    init_database,
    parse_json_field,
    serialize_json_field,
)
from discord_puppy.memory.user_notes import (
    InteractionMemory,
    UserNotes,
    get_recent_interactions,
    get_user_notes,
    get_user_summary,
    record_interaction,
    update_user_notes,
)

__all__ = [
    # Database
    "DEFAULT_DB_PATH",
    "get_connection",
    "init_database",
    "ensure_user_exists",
    "parse_json_field",
    "serialize_json_field",
    # User notes
    "UserNotes",
    "InteractionMemory",
    "get_user_notes",
    "update_user_notes",
    "record_interaction",
    "get_recent_interactions",
    "get_user_summary",
]
