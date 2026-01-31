"""
SQLite Database Schema and Connection Management 🧠

The brain of Discord Puppy! Stores:
- User notes and observations
- Interaction memories
- Puppy's personal diary

Uses aiosqlite for async operations.
"""

import json
from pathlib import Path
from typing import Optional

import aiosqlite

# Default database path
DEFAULT_DB_PATH = Path.home() / ".discord_puppy" / "brain.db"


async def get_connection(db_path: Optional[Path] = None) -> aiosqlite.Connection:
    """Get an async database connection.

    Args:
        db_path: Path to database file. Defaults to ~/.discord_puppy/brain.db

    Returns:
        aiosqlite.Connection ready for queries
    """
    path = db_path or DEFAULT_DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)

    conn = await aiosqlite.connect(path)
    conn.row_factory = aiosqlite.Row
    await conn.execute("PRAGMA foreign_keys = ON")
    return conn


async def init_database(db_path: Optional[Path] = None) -> None:
    """Initialize the database with all required tables.

    Creates:
    - user_notes: Core table for user memories
    - interaction_memories: Specific interaction records
    - puppy_diary: Puppy's personal thoughts

    Args:
        db_path: Path to database file. Defaults to ~/.discord_puppy/brain.db
    """
    conn = await get_connection(db_path)

    try:
        # User notes table - the core memory about each human
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS user_notes (
                user_id TEXT PRIMARY KEY,
                discord_username TEXT,
                display_name TEXT,
                notes TEXT DEFAULT '',
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                interaction_count INTEGER DEFAULT 0,
                puppy_mood_when_met TEXT,
                favorite_topics TEXT DEFAULT '[]',
                trust_level INTEGER DEFAULT 5 CHECK (trust_level >= 1 AND trust_level <= 10),
                nicknames TEXT DEFAULT '[]',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Interaction memories - specific conversations and events
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS interaction_memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                summary TEXT NOT NULL,
                was_helpful BOOLEAN DEFAULT FALSE,
                mood TEXT,
                notable_quotes TEXT DEFAULT '[]',
                FOREIGN KEY (user_id) REFERENCES user_notes(user_id)
                    ON DELETE CASCADE
            )
        """)

        # Create index for faster user lookups
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_interaction_user
            ON interaction_memories(user_id, timestamp DESC)
        """)

        # Puppy diary - personal thoughts and observations
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS puppy_diary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                thought TEXT NOT NULL,
                mood TEXT,
                trigger TEXT
            )
        """)

        # Create index for recent diary entries
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_diary_timestamp
            ON puppy_diary(timestamp DESC)
        """)

        await conn.commit()
        print("🧠 Discord Puppy brain initialized!")

    finally:
        await conn.close()


async def ensure_user_exists(
    conn: aiosqlite.Connection,
    user_id: str,
    username: str = "",
    display_name: str = "",
    mood: str = "",
) -> None:
    """Ensure a user exists in the database, creating if needed.

    Args:
        conn: Active database connection
        user_id: Discord user ID
        username: Discord username
        display_name: Display name
        mood: Puppy's current mood when first meeting
    """
    await conn.execute(
        """
        INSERT INTO user_notes (user_id, discord_username, display_name, puppy_mood_when_met)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            discord_username = COALESCE(excluded.discord_username, discord_username),
            display_name = COALESCE(excluded.display_name, display_name),
            last_seen = CURRENT_TIMESTAMP,
            interaction_count = interaction_count + 1
    """,
        (user_id, username, display_name, mood),
    )
    await conn.commit()


# Helper functions for JSON fields
def parse_json_field(value: str) -> list:
    """Safely parse a JSON array field."""
    if not value:
        return []
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return []


def serialize_json_field(value: list) -> str:
    """Serialize a list to JSON for storage."""
    return json.dumps(value)
