"""
Memory Tools for Discord Puppy 🧠

Tools to query and update the puppy's memory database.
"""

from typing import Any
from pydantic_ai import RunContext

from discord_puppy.memory.database import get_connection


def register_search_messages(agent):
    """Register the search_messages tool."""
    
    @agent.tool
    async def search_messages(context: RunContext, query: str = "", limit: int = 20) -> dict[str, Any]:
        """Search indexed Discord messages.
        
        Args:
            context: The pydantic-ai runtime context.
            query: Search term to find in messages.
            limit: Max results (default 20).
            
        Returns:
            List of matching messages with user and content preview.
        """
        conn = await get_connection()
        try:
            cursor = await conn.execute("""
                SELECT m.content_preview, m.message_timestamp, u.display_name, u.discord_username
                FROM indexed_messages m
                LEFT JOIN user_notes u ON m.user_id = u.user_id
                WHERE m.content_preview LIKE ?
                ORDER BY m.message_timestamp DESC
                LIMIT ?
            """, (f"%{query}%", limit))
            rows = await cursor.fetchall()
            return {
                "success": True,
                "count": len(rows),
                "messages": [
                    {
                        "user": row["display_name"] or row["discord_username"] or "unknown",
                        "content": row["content_preview"],
                        "when": row["message_timestamp"]
                    }
                    for row in rows
                ]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            await conn.close()


def register_get_user_notes(agent):
    """Register the get_user_notes tool."""
    
    @agent.tool
    async def get_user_notes(context: RunContext, username: str = "") -> dict[str, Any]:
        """Get notes and info about a user.
        
        Args:
            context: The pydantic-ai runtime context.
            username: Username or display name to look up.
            
        Returns:
            User info including notes, trust level, favorite topics, etc.
        """
        conn = await get_connection()
        try:
            cursor = await conn.execute("""
                SELECT * FROM user_notes
                WHERE discord_username LIKE ? OR display_name LIKE ?
                LIMIT 5
            """, (f"%{username}%", f"%{username}%"))
            rows = await cursor.fetchall()
            if not rows:
                return {"success": True, "found": False, "message": f"No user found matching '{username}'"}
            
            return {
                "success": True,
                "found": True,
                "users": [
                    {
                        "username": row["discord_username"],
                        "display_name": row["display_name"],
                        "notes": row["notes"],
                        "trust_level": row["trust_level"],
                        "favorite_topics": row["favorite_topics"],
                        "interaction_count": row["interaction_count"],
                        "first_seen": row["first_seen"],
                        "last_seen": row["last_seen"]
                    }
                    for row in rows
                ]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            await conn.close()


def register_record_user_note(agent):
    """Register the record_user_note tool."""
    
    @agent.tool
    async def record_user_note(context: RunContext, username: str = "", note: str = "") -> dict[str, Any]:
        """Add or update notes about a user.
        
        Args:
            context: The pydantic-ai runtime context.
            username: Username to add note for.
            note: The note to record (appends to existing notes).
            
        Returns:
            Success status.
        """
        if not username or not note:
            return {"success": False, "error": "Need both username and note"}
        
        conn = await get_connection()
        try:
            cursor = await conn.execute("""
                SELECT user_id, notes FROM user_notes
                WHERE discord_username LIKE ? OR display_name LIKE ?
                LIMIT 1
            """, (f"%{username}%", f"%{username}%"))
            row = await cursor.fetchone()
            
            if not row:
                return {"success": False, "error": f"User '{username}' not found"}
            
            existing = row["notes"] or ""
            new_notes = f"{existing}\n- {note}".strip()
            
            await conn.execute("""
                UPDATE user_notes SET notes = ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """, (new_notes, row["user_id"]))
            await conn.commit()
            
            return {"success": True, "message": f"Note recorded for {username}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            await conn.close()


def register_list_users(agent):
    """Register the list_users tool."""
    
    @agent.tool
    async def list_users(context: RunContext, limit: int = 20) -> dict[str, Any]:
        """List known users.
        
        Args:
            context: The pydantic-ai runtime context.
            limit: Max users to return.
            
        Returns:
            List of users with basic info.
        """
        conn = await get_connection()
        try:
            cursor = await conn.execute("""
                SELECT display_name, discord_username, interaction_count, last_seen, notes
                FROM user_notes
                ORDER BY last_seen DESC
                LIMIT ?
            """, (limit,))
            rows = await cursor.fetchall()
            return {
                "success": True,
                "count": len(rows),
                "users": [
                    {
                        "name": row["display_name"] or row["discord_username"],
                        "interactions": row["interaction_count"],
                        "last_seen": row["last_seen"],
                        "notes": row["notes"] or "(no notes)"
                    }
                    for row in rows
                ]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            await conn.close()


def register_get_recent_messages(agent):
    """Register the get_recent_messages tool."""
    
    @agent.tool
    async def get_recent_messages(context: RunContext, limit: int = 10) -> dict[str, Any]:
        """Get recent messages from the database.
        
        Args:
            context: The pydantic-ai runtime context.
            limit: Number of recent messages.
            
        Returns:
            Recent messages.
        """
        conn = await get_connection()
        try:
            cursor = await conn.execute("""
                SELECT m.content_preview, m.message_timestamp, u.display_name
                FROM indexed_messages m
                LEFT JOIN user_notes u ON m.user_id = u.user_id
                ORDER BY m.message_timestamp DESC
                LIMIT ?
            """, (limit,))
            rows = await cursor.fetchall()
            return {
                "success": True,
                "messages": [
                    {
                        "user": row["display_name"] or "unknown",
                        "content": row["content_preview"],
                        "when": row["message_timestamp"]
                    }
                    for row in rows
                ]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            await conn.close()


# Standalone function for use outside agent (e.g., spontaneous messages)
async def get_recent_messages_standalone(limit: int = 10) -> dict[str, Any]:
    """Get recent messages (standalone async version for non-agent use)."""
    conn = await get_connection()
    try:
        cursor = await conn.execute("""
            SELECT m.content_preview, m.message_timestamp, u.display_name
            FROM indexed_messages m
            LEFT JOIN user_notes u ON m.user_id = u.user_id
            ORDER BY m.message_timestamp DESC
            LIMIT ?
        """, (limit,))
        rows = await cursor.fetchall()
        return {
            "success": True,
            "messages": [
                {
                    "user": row["display_name"] or "unknown",
                    "content": row["content_preview"],
                    "when": row["message_timestamp"]
                }
                for row in rows
            ]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        await conn.close()
