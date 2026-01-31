"""Memory Tools for Discord Puppy - My Brain on Demand! 🧠🐕

These tools let the LLM access and modify the puppy's memory!
Remember all the humans! Store all the thoughts! Never forget a treat giver!

Usage:
    These tools are registered with pydantic-ai and called by the LLM
    when the puppy needs to remember or learn something about users.
"""

from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from discord_puppy.memory.database import (
    ensure_user_exists,
    get_connection,
    parse_json_field,
    serialize_json_field,
)
from discord_puppy.memory.user_notes import (
    get_user_summary,
    update_user_notes,
)

# =============================================================================
# USER MEMORY TOOLS 🧠
# =============================================================================


async def recall_user(user_id: str, db_path: Optional[Path] = None) -> str:
    """Remember everything about this human! Returns notes, trust level, nicknames...

    *rummages through brain files* Let me see what I know about this person!
    I remember EVERYONE. Especially the ones who give treats. And the ones
    who don't give treats (I remember that too, with suspicion).

    Args:
        user_id: The Discord user ID to remember. Numbers that identify humans!
        db_path: Optional database path (for testing, ignore this usually)

    Returns:
        Everything I know about this human, formatted nicely!
        Or a sad message if I've never met them. 😢
    """
    summary = await get_user_summary(user_id, db_path)

    if not summary:
        return (
            f"🐕❓ *scratches head* I don't know user {user_id}!\n"
            "They're a mystery human! A stranger! A potential new friend!\n"
            "...or a potential cat person. We'll have to investigate. 🔍"
        )

    return (
        f"🐕💭 *tail wags as memories flood back*\n\n"
        f"{summary}\n\n"
        "*looks proud of my excellent memory* I remember EVERYTHING!"
    )


async def update_memory(user_id: str, observation: str, db_path: Optional[Path] = None) -> str:
    """Write a new observation about this human to my brain. I'll remember this forever! ...probably.

    Time to add something to my mental file on this human!
    *opens filing cabinet in brain, papers fly everywhere*

    Good things to observe:
    - Treat giving behavior (VERY IMPORTANT)
    - Favorite topics (so I can talk about them!)
    - Whether they pet me enough (probably not)
    - Any suspicious cat-related activities

    Args:
        user_id: The Discord user ID. Their permanent record!
        observation: What I noticed about them. Keep it short but memorable!
        db_path: Optional database path (for testing)

    Returns:
        Confirmation that my brain has been updated! Or an error. Hopefully not an error.
    """
    # Add timestamp to observation for context
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    timestamped_observation = f"[{timestamp}] {observation}"

    success = await update_user_notes(user_id, timestamped_observation, db_path)

    if success:
        return (
            f"🐕✍️ *scribbles furiously in brain notebook*\n\n"
            f"Noted about user {user_id}:\n"
            f"'{observation}'\n\n"
            "Memory saved! I'll remember this! Probably! My brain is very big "
            "(for a puppy) and very full (of important thoughts about treats)."
        )
    else:
        return (
            f"🐕💥 *brain notebook catches fire*\n\n"
            f"Uh oh! Failed to save memory about user {user_id}!\n"
            "My brain is having technical difficulties! This is concerning!\n"
            "Maybe I need more treats to fuel my memory systems? 🦴"
        )


async def add_nickname(user_id: str, nickname: str, db_path: Optional[Path] = None) -> str:
    """Give this human a nickname! They might not like it.

    Humans love nicknames! Especially the ones I come up with!
    *tail wags mischievously*

    Previous hits include:
    - "Treat Dispenser #7"
    - "The One Who Pets Good"
    - "Suspicious Cat Ally"
    - "Belly Rub Champion 2024"

    Args:
        user_id: The human who is about to receive greatness
        nickname: The magnificent nickname I'm bestowing upon them
        db_path: Optional database path (for testing)

    Returns:
        Confirmation of their new nickname! They should feel honored!
    """
    conn = await get_connection(db_path)

    try:
        # Ensure user exists
        await ensure_user_exists(conn, user_id)

        # Get current nicknames
        cursor = await conn.execute(
            "SELECT nicknames FROM user_notes WHERE user_id = ?", (user_id,)
        )
        row = await cursor.fetchone()
        current_nicknames = parse_json_field(row["nicknames"] if row else "[]")

        # Check if nickname already exists
        if nickname in current_nicknames:
            return (
                f"🐕🤔 *checks notes*\n\n"
                f"I already call them '{nickname}'! Great minds think alike!\n"
                f"Current nicknames: {', '.join(current_nicknames) or 'none yet'}\n\n"
                "...wait, I'm the one who thought of it both times. I'm the great mind!"
            )

        # Add new nickname
        current_nicknames.append(nickname)

        await conn.execute(
            """
            UPDATE user_notes
            SET nicknames = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
            """,
            (serialize_json_field(current_nicknames), user_id),
        )
        await conn.commit()

        return (
            f"🐕🏷️ *stamps nickname on human's forehead (metaphorically)*\n\n"
            f"User {user_id} shall now also be known as: '{nickname}'!\n\n"
            f"All their nicknames: {', '.join(current_nicknames)}\n\n"
            "This is a great honor! They should put it on their resume!"
        )

    except Exception as e:
        return (
            f"🐕💥 Nickname machine broke!\n\n"
            f"Error: {type(e).__name__}: {e}\n\n"
            "The nickname remains in my heart, if not in the database. 💔"
        )

    finally:
        await conn.close()


async def adjust_trust(
    user_id: str, delta: int, reason: str, db_path: Optional[Path] = None
) -> str:
    """Adjust how much I trust this human. Did they give treats?

    Trust is earned, not given! (Well, sometimes it's given. I'm a puppy.
    I trust most people by default. Except suspicious ones.)

    Trust scale:
    - 1-3: I'm watching you 👀 (probably a cat person)
    - 4-6: Normal human trust (you're okay I guess)
    - 7-8: Good human! (treat giver detected)
    - 9-10: BEST FRIEND FOREVER (maximum tail wags)

    Args:
        user_id: The human whose trust score I'm adjusting
        delta: How much to change (-3 to +3 typically). Positive = more trust!
        reason: Why I'm adjusting. This is important for my records!
        db_path: Optional database path (for testing)

    Returns:
        The new trust level and my feelings about it!
    """
    conn = await get_connection(db_path)

    try:
        # Ensure user exists
        await ensure_user_exists(conn, user_id)

        # Get current trust level
        cursor = await conn.execute(
            "SELECT trust_level, display_name FROM user_notes WHERE user_id = ?",
            (user_id,),
        )
        row = await cursor.fetchone()
        current_trust = row["trust_level"] if row else 5
        display_name = row["display_name"] if row else f"User {user_id}"

        # Calculate new trust (bounded 1-10)
        new_trust = max(1, min(10, current_trust + delta))

        # Update trust level
        await conn.execute(
            """
            UPDATE user_notes
            SET trust_level = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
            """,
            (new_trust, user_id),
        )
        await conn.commit()

        # Generate appropriate response based on change
        if delta > 0:
            emoji = "📈" if new_trust < 10 else "🏆"
            mood = "*tail wags faster*" if new_trust >= 7 else "*cautiously optimistic tail wag*"
        elif delta < 0:
            emoji = "📉" if new_trust > 1 else "⚠️"
            mood = "*suspicious squinting*" if new_trust <= 3 else "*concerned head tilt*"
        else:
            emoji = "➡️"
            mood = "*confused puppy noises*"

        trust_description = _get_trust_description(new_trust)

        return (
            f"🐕{emoji} Trust Level Adjusted!\n\n"
            f"**{display_name}**: {current_trust} → {new_trust}/10\n"
            f"**Reason:** {reason}\n"
            f"**Status:** {trust_description}\n\n"
            f"{mood}\n\n"
            "I never forget who gives treats. Or who doesn't. 👀"
        )

    except Exception as e:
        return (
            f"🐕💥 Trust calibration error!\n\n"
            f"Error: {type(e).__name__}: {e}\n\n"
            "My trust-o-meter is malfunctioning! This is very concerning!"
        )

    finally:
        await conn.close()


def _get_trust_description(trust_level: int) -> str:
    """Get a puppy-appropriate description of a trust level."""
    descriptions = {
        1: "Maximum Suspicion 🚨 (are they a cat??)",
        2: "Very Suspicious 👀 (watching closely)",
        3: "Suspicious 🤔 (something's off)",
        4: "Cautious 🐕 (we'll see)",
        5: "Neutral 🐾 (default human trust)",
        6: "Friendly 😊 (seems nice!)",
        7: "Good Human! 🦴 (treat potential detected)",
        8: "Great Human! 🎾 (definitely a friend)",
        9: "Best Friend! 💕 (maximum tail wags)",
        10: "ULTIMATE BEST FRIEND 🏆 (would share my toy with them)",
    }
    return descriptions.get(trust_level, "Unknown trust level?!")


# =============================================================================
# DIARY TOOLS 📔
# =============================================================================


async def write_diary(thought: str, mood: str, db_path: Optional[Path] = None) -> str:
    """Write in my personal diary. Very important puppy thoughts.

    Dear Diary,
    Today I had THOUGHTS. Big ones! Small ones! Thoughts about treats!
    Thoughts about squirrels! Thoughts about the meaning of being a good boy!

    This is where I record my innermost puppy feelings.
    It's very personal. No peeking! (Unless you're reading this docstring,
    in which case... hello! 👋🐕)

    Args:
        thought: My very important thought to record for posterity
        mood: How I'm feeling (excited, sleepy, suspicious, zoomies, etc.)
        db_path: Optional database path (for testing)

    Returns:
        Confirmation that my thought has been immortalized!
    """
    conn = await get_connection(db_path)

    try:
        await conn.execute(
            """
            INSERT INTO puppy_diary (thought, mood)
            VALUES (?, ?)
            """,
            (thought, mood),
        )
        await conn.commit()

        # Get the entry ID for reference
        cursor = await conn.execute("SELECT last_insert_rowid()")
        row = await cursor.fetchone()
        entry_id = row[0] if row else "???"

        mood_emoji = _get_mood_emoji(mood)

        return (
            f"🐕📔 *opens diary with tiny paws*\n\n"
            f"**Diary Entry #{entry_id}**\n"
            f"**Mood:** {mood} {mood_emoji}\n\n"
            f"'{thought}'\n\n"
            "*closes diary and hides it under bed*\n\n"
            "My innermost thoughts have been recorded! Future me will appreciate "
            "this wisdom! (Or be confused by it. Either way!)"
        )

    except Exception as e:
        return (
            f"🐕💔 Diary malfunction!\n\n"
            f"Error: {type(e).__name__}: {e}\n\n"
            "My thoughts will just have to live in my head rent-free!"
        )

    finally:
        await conn.close()


async def recall_diary(days: int = 7, db_path: Optional[Path] = None) -> str:
    """What have I been thinking about lately?

    *blows dust off diary* Let me see what past-me was up to!
    Reading old diary entries is like visiting a wiser, more confused version
    of myself. Or a less wise, equally confused version. It varies.

    Args:
        days: How many days back to look (default 7). Don't go too far back,
              some of those thoughts are embarrassing!
        db_path: Optional database path (for testing)

    Returns:
        My recent diary entries, formatted for maximum nostalgia!
    """
    conn = await get_connection(db_path)

    try:
        # Calculate the cutoff date
        cutoff = datetime.now() - timedelta(days=days)

        cursor = await conn.execute(
            """
            SELECT id, timestamp, thought, mood
            FROM puppy_diary
            WHERE timestamp >= ?
            ORDER BY timestamp DESC
            LIMIT 20
            """,
            (cutoff.isoformat(),),
        )
        rows = await cursor.fetchall()

        if not rows:
            return (
                f"🐕📔 *flips through empty pages*\n\n"
                f"No diary entries in the last {days} days!\n"
                "I must have been too busy chasing squirrels to write!\n"
                "Or sleeping. Probably sleeping. 😴"
            )

        entries = []
        for row in rows:
            timestamp = row["timestamp"] or "sometime"
            thought = row["thought"]
            mood = row["mood"] or "unknown"
            mood_emoji = _get_mood_emoji(mood)

            entries.append(f"**[{timestamp}]** ({mood} {mood_emoji})\n{thought}")

        entries_text = "\n\n".join(entries)

        return (
            f"🐕📖 *reads diary with great interest*\n\n"
            f"**My thoughts from the last {days} days:**\n\n"
            f"{entries_text}\n\n"
            "*closes diary thoughtfully*\n\n"
            f"Wow, past-me sure had a lot of feelings! ({len(rows)} entries found)"
        )

    except Exception as e:
        return (
            f"🐕💥 Diary reading error!\n\n"
            f"Error: {type(e).__name__}: {e}\n\n"
            "My diary is being difficult! Maybe it needs treats too?"
        )

    finally:
        await conn.close()


def _get_mood_emoji(mood: str) -> str:
    """Get an appropriate emoji for a mood."""
    mood_lower = mood.lower()
    mood_emojis = {
        "excited": "🎉",
        "happy": "😊",
        "sleepy": "😴",
        "hungry": "🍖",
        "suspicious": "👀",
        "zoomies": "💨",
        "contemplative": "🤔",
        "sad": "😢",
        "playful": "🎾",
        "confused": "❓",
        "alert": "⚡",
        "curious": "🔍",
        "mischievous": "😈",
        "content": "☺️",
        "anxious": "😰",
        "proud": "🏆",
        "loving": "💕",
        "chaotic": "🌀",
    }

    for mood_key, emoji in mood_emojis.items():
        if mood_key in mood_lower:
            return emoji

    return "🐕"  # Default puppy emoji


# =============================================================================
# Export tools for pydantic-ai registration
# =============================================================================

MEMORY_TOOLS = [
    recall_user,
    update_memory,
    add_nickname,
    adjust_trust,
    write_diary,
    recall_diary,
]

__all__ = [
    "recall_user",
    "update_memory",
    "add_nickname",
    "adjust_trust",
    "write_diary",
    "recall_diary",
    "MEMORY_TOOLS",
]
