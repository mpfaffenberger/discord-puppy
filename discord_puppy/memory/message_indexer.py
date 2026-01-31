"""
Message Indexer - The Memory Collector 🧠📨

This module handles indexing Discord message history on startup.
Messages are hashed for deduplication - we never process the same
message twice (we're not goldfish, we're puppies with MEMORY!).

Hashing Strategy:
- SHA256 hash of: message_id + channel_id + content + author_id
- This ensures we detect even edited messages as "different"
"""

import hashlib
from datetime import datetime, timedelta
from typing import Optional

import aiosqlite
import discord

from discord_puppy.memory.database import get_connection, ensure_user_exists


def compute_message_hash(message: discord.Message) -> str:
    """Compute a unique hash for a Discord message.

    The hash includes message ID, channel ID, content, and author ID.
    This means if a message is edited, it will get a new hash!

    Args:
        message: Discord message object

    Returns:
        SHA256 hex digest of the message
    """
    # Build a unique fingerprint
    fingerprint = f"{message.id}:{message.channel.id}:{message.content}:{message.author.id}"
    return hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()


async def is_message_indexed(conn: aiosqlite.Connection, message_hash: str) -> bool:
    """Check if we've already indexed a message.

    Args:
        conn: Active database connection
        message_hash: SHA256 hash of the message

    Returns:
        True if we've seen this message before
    """
    cursor = await conn.execute(
        "SELECT 1 FROM indexed_messages WHERE message_hash = ? LIMIT 1",
        (message_hash,)
    )
    result = await cursor.fetchone()
    return result is not None


async def index_message(
    conn: aiosqlite.Connection,
    message: discord.Message,
    message_hash: str,
) -> bool:
    """Index a single message in the database.

    Args:
        conn: Active database connection
        message: Discord message object
        message_hash: Pre-computed hash of the message

    Returns:
        True if message was newly indexed, False if already existed
    """
    # Truncate content for preview (we don't need the whole thing)
    content_preview = message.content[:200] if message.content else None

    try:
        await conn.execute(
            """
            INSERT INTO indexed_messages (
                message_hash, message_id, channel_id, guild_id,
                user_id, content_preview, message_timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                message_hash,
                str(message.id),
                str(message.channel.id),
                str(message.guild.id) if message.guild else None,
                str(message.author.id),
                content_preview,
                message.created_at.isoformat(),
            )
        )
        return True
    except aiosqlite.IntegrityError:
        # Hash already exists (race condition protection)
        return False


async def update_user_notes_from_message(
    conn: aiosqlite.Connection,
    message: discord.Message,
) -> None:
    """Update user notes based on a new message.

    This is where the puppy learns things about humans!
    For now, we just update the interaction count and last_seen.
    Future: Add topic extraction, sentiment analysis, etc.

    Args:
        conn: Active database connection
        message: Discord message to process
    """
    # Make sure the user exists in our brain
    await ensure_user_exists(
        conn,
        user_id=str(message.author.id),
        username=message.author.name,
        display_name=message.author.display_name,
        mood="indexing",  # We're in index mode!
    )


async def index_channel_history(
    channel: discord.TextChannel,
    limit: Optional[int] = 1000,
    days_back: int = 30,
) -> dict:
    """Index message history from a Discord channel.

    Fetches messages from the channel and indexes any we haven't seen.
    Uses hashing to skip messages we've already processed.

    Args:
        channel: Discord text channel to index
        limit: Maximum messages to fetch (None = no limit, be careful!)
        days_back: How many days back to look

    Returns:
        Dict with stats: {new_messages, skipped_messages, total_processed}
    """
    stats = {
        "new_messages": 0,
        "skipped_messages": 0,
        "total_processed": 0,
        "users_updated": set(),
    }

    # Calculate the cutoff date
    after_date = datetime.utcnow() - timedelta(days=days_back)

    conn = await get_connection()
    try:
        async for message in channel.history(limit=limit, after=after_date):
            stats["total_processed"] += 1

            # Skip bot messages (we don't index ourselves!)
            if message.author.bot:
                stats["skipped_messages"] += 1
                continue

            # Compute hash and check if we've seen it
            message_hash = compute_message_hash(message)

            if await is_message_indexed(conn, message_hash):
                stats["skipped_messages"] += 1
                continue

            # New message! Index it!
            if await index_message(conn, message, message_hash):
                stats["new_messages"] += 1
                stats["users_updated"].add(str(message.author.id))

                # Update user notes
                await update_user_notes_from_message(conn, message)

        await conn.commit()

    finally:
        await conn.close()

    # Convert set to count for return
    stats["users_updated"] = len(stats["users_updated"])
    return stats


async def index_guild_history(
    guild: discord.Guild,
    limit_per_channel: int = 500,
    days_back: int = 30,
) -> dict:
    """Index message history from all text channels in a guild.

    Args:
        guild: Discord guild to index
        limit_per_channel: Max messages per channel
        days_back: How many days back to look

    Returns:
        Dict with aggregated stats
    """
    total_stats = {
        "channels_processed": 0,
        "new_messages": 0,
        "skipped_messages": 0,
        "total_processed": 0,
        "users_updated": 0,
    }

    for channel in guild.text_channels:
        # Check if we have permission to read history
        if not channel.permissions_for(guild.me).read_message_history:
            print(f"  ⏭️  Skipping #{channel.name} (no read permission)")
            continue

        print(f"  📖 Indexing #{channel.name}...")

        try:
            stats = await index_channel_history(
                channel,
                limit=limit_per_channel,
                days_back=days_back,
            )

            total_stats["channels_processed"] += 1
            total_stats["new_messages"] += stats["new_messages"]
            total_stats["skipped_messages"] += stats["skipped_messages"]
            total_stats["total_processed"] += stats["total_processed"]
            total_stats["users_updated"] += stats["users_updated"]

            if stats["new_messages"] > 0:
                print(f"    ✨ Found {stats['new_messages']} new messages!")

        except discord.Forbidden:
            print(f"  ⏭️  Skipping #{channel.name} (forbidden)")
        except Exception as e:
            print(f"  ❌ Error indexing #{channel.name}: {e}")

    return total_stats


async def index_all_guilds(
    client: discord.Client,
    limit_per_channel: int = 500,
    days_back: int = 30,
) -> dict:
    """Index message history from all guilds the bot is in.

    This is the main entry point - call this on bot startup!

    Args:
        client: Discord client instance
        limit_per_channel: Max messages per channel
        days_back: How many days back to look

    Returns:
        Dict with aggregated stats across all guilds
    """
    total_stats = {
        "guilds_processed": 0,
        "channels_processed": 0,
        "new_messages": 0,
        "skipped_messages": 0,
        "total_processed": 0,
    }

    for guild in client.guilds:
        print(f"🏠 Indexing guild: {guild.name}")

        stats = await index_guild_history(
            guild,
            limit_per_channel=limit_per_channel,
            days_back=days_back,
        )

        total_stats["guilds_processed"] += 1
        total_stats["channels_processed"] += stats["channels_processed"]
        total_stats["new_messages"] += stats["new_messages"]
        total_stats["skipped_messages"] += stats["skipped_messages"]
        total_stats["total_processed"] += stats["total_processed"]

    return total_stats
