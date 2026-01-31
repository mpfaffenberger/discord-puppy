"""User Notes CRUD Operations 🐕📝

Async functions for managing puppy's memories about users.
This is how Discord Puppy remembers all the wonderful humans it meets!

Usage:
    from discord_puppy.memory.user_notes import get_user_notes, record_interaction

    notes = await get_user_notes("123456789")
    if notes:
        print(f"I remember {notes.display_name}!")
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

from discord_puppy.memory.database import (
    ensure_user_exists,
    get_connection,
    parse_json_field,
    serialize_json_field,
)


class InteractionMemory(BaseModel):
    """A single interaction memory with a user.

    Captures the essence of a conversation or event with a human.
    """

    id: int
    """Unique interaction ID from database."""

    user_id: str
    """Discord user ID this interaction was with."""

    timestamp: datetime
    """When this interaction occurred."""

    summary: str
    """Brief summary of what happened."""

    was_helpful: bool = False
    """Did puppy help this human?"""

    mood: str = ""
    """Puppy's mood during this interaction."""

    notable_quotes: list[str] = Field(default_factory=list)
    """Any memorable things said."""


class UserNotes(BaseModel):
    """Complete memory profile for a user.

    Everything puppy knows about a human friend!
    """

    user_id: str
    """Discord user ID (primary identifier)."""

    discord_username: str = ""
    """Their Discord username."""

    display_name: str = ""
    """Their display name (what to call them)."""

    notes: str = ""
    """Free-form notes about this user."""

    first_seen: datetime | None = None
    """When puppy first met this human."""

    last_seen: datetime | None = None
    """When puppy last saw this human."""

    interaction_count: int = 0
    """How many times we've interacted."""

    trust_level: int = Field(default=5, ge=1, le=10)
    """How much puppy trusts this human (1-10)."""

    nicknames: list[str] = Field(default_factory=list)
    """Fun nicknames for this human."""

    favorite_topics: list[str] = Field(default_factory=list)
    """Topics this human likes to discuss."""


async def get_user_notes(
    user_id: str, db_path: Optional[Path] = None
) -> UserNotes | None:
    """Get all notes about a user.

    Retrieves the complete memory profile for a user from the database.

    Args:
        user_id: Discord user ID to look up
        db_path: Optional path to database (for testing)

    Returns:
        UserNotes if user exists, None otherwise

    Example:
        >>> notes = await get_user_notes("123456789")
        >>> if notes:
        ...     print(f"I know {notes.display_name}!")
    """
    conn = await get_connection(db_path)

    try:
        cursor = await conn.execute(
            """
            SELECT user_id, discord_username, display_name, notes,
                   first_seen, last_seen, interaction_count,
                   trust_level, nicknames, favorite_topics
            FROM user_notes
            WHERE user_id = ?
            """,
            (user_id,),
        )
        row = await cursor.fetchone()

        if not row:
            return None

        return UserNotes(
            user_id=row["user_id"],
            discord_username=row["discord_username"] or "",
            display_name=row["display_name"] or "",
            notes=row["notes"] or "",
            first_seen=_parse_timestamp(row["first_seen"]),
            last_seen=_parse_timestamp(row["last_seen"]),
            interaction_count=row["interaction_count"] or 0,
            trust_level=row["trust_level"] or 5,
            nicknames=parse_json_field(row["nicknames"]),
            favorite_topics=parse_json_field(row["favorite_topics"]),
        )

    finally:
        await conn.close()


async def update_user_notes(
    user_id: str, new_notes: str, db_path: Optional[Path] = None
) -> bool:
    """Append or update notes about a user.

    Adds new information to existing notes (appends with newline separator).
    Creates the user record if it doesn't exist.

    Args:
        user_id: Discord user ID to update
        new_notes: New notes to append
        db_path: Optional path to database (for testing)

    Returns:
        True if update succeeded, False otherwise

    Example:
        >>> success = await update_user_notes("123", "Loves dogs!")
        >>> if success:
        ...     print("Memory saved! 🐕")
    """
    conn = await get_connection(db_path)

    try:
        # Ensure user exists first
        await ensure_user_exists(conn, user_id)

        # Get existing notes to append to
        cursor = await conn.execute(
            "SELECT notes FROM user_notes WHERE user_id = ?", (user_id,)
        )
        row = await cursor.fetchone()
        existing_notes = row["notes"] if row and row["notes"] else ""

        # Append new notes with separator
        if existing_notes:
            updated_notes = f"{existing_notes}\n{new_notes}"
        else:
            updated_notes = new_notes

        # Update the notes
        await conn.execute(
            """
            UPDATE user_notes
            SET notes = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
            """,
            (updated_notes, user_id),
        )
        await conn.commit()
        return True

    except Exception:
        return False

    finally:
        await conn.close()


async def record_interaction(
    user_id: str,
    summary: str,
    mood: str,
    was_helpful: bool,
    db_path: Optional[Path] = None,
) -> int:
    """Log an interaction with a user.

    Records a new interaction in the database and returns the interaction ID.

    Args:
        user_id: Discord user ID
        summary: Brief summary of the interaction
        mood: Puppy's mood during interaction
        was_helpful: Whether puppy was helpful
        db_path: Optional path to database (for testing)

    Returns:
        The ID of the newly created interaction record, or -1 on failure

    Example:
        >>> interaction_id = await record_interaction(
        ...     "123", "Helped debug code", "excited", True
        ... )
        >>> print(f"Recorded interaction #{interaction_id}")
    """
    conn = await get_connection(db_path)

    try:
        # Ensure user exists first
        await ensure_user_exists(conn, user_id)

        # Insert the interaction
        cursor = await conn.execute(
            """
            INSERT INTO interaction_memories (user_id, summary, mood, was_helpful)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, summary, mood, was_helpful),
        )
        await conn.commit()

        # Return the new interaction ID
        return cursor.lastrowid or -1

    except Exception:
        return -1

    finally:
        await conn.close()


async def get_recent_interactions(
    user_id: str, limit: int = 5, db_path: Optional[Path] = None
) -> list[InteractionMemory]:
    """Get recent interactions with a user.

    Retrieves the most recent interactions for context in conversations.

    Args:
        user_id: Discord user ID to look up
        limit: Maximum number of interactions to return (default 5)
        db_path: Optional path to database (for testing)

    Returns:
        List of InteractionMemory objects, most recent first

    Example:
        >>> interactions = await get_recent_interactions("123", limit=3)
        >>> for i in interactions:
        ...     print(f"{i.timestamp}: {i.summary}")
    """
    conn = await get_connection(db_path)

    try:
        cursor = await conn.execute(
            """
            SELECT id, user_id, timestamp, summary, was_helpful, mood, notable_quotes
            FROM interaction_memories
            WHERE user_id = ?
            ORDER BY timestamp DESC, id DESC
            LIMIT ?
            """,
            (user_id, limit),
        )
        rows = await cursor.fetchall()

        return [
            InteractionMemory(
                id=row["id"],
                user_id=row["user_id"],
                timestamp=_parse_timestamp(row["timestamp"]) or datetime.now(),
                summary=row["summary"],
                was_helpful=bool(row["was_helpful"]),
                mood=row["mood"] or "",
                notable_quotes=parse_json_field(row["notable_quotes"]),
            )
            for row in rows
        ]

    finally:
        await conn.close()


async def get_user_summary(user_id: str, db_path: Optional[Path] = None) -> str:
    """Get a condensed memory string for prompt injection.

    Creates a compact summary suitable for including in LLM prompts.

    Args:
        user_id: Discord user ID to summarize
        db_path: Optional path to database (for testing)

    Returns:
        A formatted string with key user information, or empty string if unknown

    Example:
        >>> summary = await get_user_summary("123")
        >>> print(summary)
        "User: CoolDog (trust: 8/10, seen 42 times). Notes: Loves memes..."
    """
    notes = await get_user_notes(user_id, db_path)

    if not notes:
        return ""

    # Build the summary parts
    parts = []

    # Name and basic info
    name = notes.display_name or notes.discord_username or "Unknown"
    parts.append(f"User: {name}")

    # Trust and interaction count
    parts.append(f"(trust: {notes.trust_level}/10, seen {notes.interaction_count} times)")

    # Nicknames if any
    if notes.nicknames:
        nicknames_str = ", ".join(notes.nicknames[:3])  # Limit to 3
        parts.append(f"Nicknames: {nicknames_str}")

    # Favorite topics if any
    if notes.favorite_topics:
        topics_str = ", ".join(notes.favorite_topics[:5])  # Limit to 5
        parts.append(f"Likes: {topics_str}")

    # Notes (truncated if long)
    if notes.notes:
        truncated_notes = notes.notes[:200] + "..." if len(notes.notes) > 200 else notes.notes
        parts.append(f"Notes: {truncated_notes}")

    # Get recent interactions for extra context
    interactions = await get_recent_interactions(user_id, limit=3, db_path=db_path)
    if interactions:
        interaction_summaries = [f"- {i.summary}" for i in interactions]
        parts.append("Recent interactions:")
        parts.extend(interaction_summaries)

    return ". ".join(parts[:3]) + "\n" + "\n".join(parts[3:]) if len(parts) > 3 else ". ".join(parts)


def _parse_timestamp(value: str | None) -> datetime | None:
    """Parse a SQLite timestamp string to datetime.

    Args:
        value: Timestamp string from SQLite or None

    Returns:
        datetime object or None if parsing fails
    """
    if not value:
        return None

    try:
        # SQLite default format
        return datetime.fromisoformat(value.replace(" ", "T"))
    except (ValueError, AttributeError):
        return None
