"""Tests for Memory Tools - Testing the puppy brain! 🧠🐕

Tests the LLM-callable memory tools that let the puppy remember
and learn about users, plus the diary functionality.
"""

import tempfile
from pathlib import Path

import pytest
import pytest_asyncio

from discord_puppy.memory import init_database
from discord_puppy.memory.memory_tools import (
    MEMORY_TOOLS,
    _get_mood_emoji,
    _get_trust_description,
    add_nickname,
    adjust_trust,
    recall_diary,
    recall_user,
    update_memory,
    write_diary,
)


@pytest_asyncio.fixture
async def test_db(tmp_path: Path):
    """Create a fresh test database."""
    db_path = tmp_path / "test_brain.db"
    await init_database(db_path)
    return db_path


class TestMemoryToolsExport:
    """Test that all memory tools are properly exported."""

    def test_memory_tools_contains_all_functions(self):
        """MEMORY_TOOLS should contain all 6 functions."""
        tool_names = [t.__name__ for t in MEMORY_TOOLS]
        expected = [
            "recall_user",
            "update_memory",
            "add_nickname",
            "adjust_trust",
            "write_diary",
            "recall_diary",
        ]
        assert tool_names == expected

    def test_memory_tools_are_callable(self):
        """All memory tools should be callable."""
        for tool in MEMORY_TOOLS:
            assert callable(tool)

    def test_all_tools_are_async(self):
        """All memory tools should be async functions."""
        import asyncio

        for tool in MEMORY_TOOLS:
            assert asyncio.iscoroutinefunction(tool)


class TestRecallUser:
    """Tests for recall_user - remembering humans!"""

    @pytest.mark.asyncio
    async def test_recall_unknown_user(self, test_db: Path):
        """Recalling an unknown user should return a friendly message."""
        result = await recall_user("unknown_user_123", db_path=test_db)

        assert "don't know user unknown_user_123" in result
        assert "mystery human" in result.lower() or "stranger" in result.lower()

    @pytest.mark.asyncio
    async def test_recall_known_user(self, test_db: Path):
        """Recalling a known user should return their info."""
        # First, create a user by updating memory
        await update_memory("user_456", "Loves treats!", db_path=test_db)

        result = await recall_user("user_456", db_path=test_db)

        assert "tail wags" in result.lower() or "memories" in result.lower()
        assert "user_456" in result.lower() or "loves treats" in result.lower()


class TestUpdateMemory:
    """Tests for update_memory - writing observations!"""

    @pytest.mark.asyncio
    async def test_update_memory_success(self, test_db: Path):
        """Should successfully update memory and confirm."""
        result = await update_memory("user_789", "Is very friendly!", db_path=test_db)

        assert "scribbles" in result.lower() or "noted" in result.lower()
        assert "Is very friendly!" in result
        assert "user_789" in result

    @pytest.mark.asyncio
    async def test_update_memory_creates_user(self, test_db: Path):
        """Updating memory should create the user if they don't exist."""
        # This shouldn't error - should create user automatically
        result = await update_memory("new_user_abc", "First observation!", db_path=test_db)

        assert "memory saved" in result.lower() or "noted" in result.lower()


class TestAddNickname:
    """Tests for add_nickname - giving humans fun names!"""

    @pytest.mark.asyncio
    async def test_add_nickname_success(self, test_db: Path):
        """Should successfully add a nickname."""
        result = await add_nickname("user_111", "Treat Master", db_path=test_db)

        assert "Treat Master" in result
        assert "user_111" in result.lower() or "known as" in result.lower()

    @pytest.mark.asyncio
    async def test_add_duplicate_nickname(self, test_db: Path):
        """Adding the same nickname twice should be handled gracefully."""
        await add_nickname("user_222", "Best Friend", db_path=test_db)
        result = await add_nickname("user_222", "Best Friend", db_path=test_db)

        assert "already" in result.lower()
        assert "Best Friend" in result

    @pytest.mark.asyncio
    async def test_add_multiple_nicknames(self, test_db: Path):
        """Should be able to add multiple different nicknames."""
        await add_nickname("user_333", "First Name", db_path=test_db)
        result = await add_nickname("user_333", "Second Name", db_path=test_db)

        assert "Second Name" in result
        assert "First Name" in result  # Should list all nicknames


class TestAdjustTrust:
    """Tests for adjust_trust - tracking trust levels!"""

    @pytest.mark.asyncio
    async def test_adjust_trust_increase(self, test_db: Path):
        """Should increase trust level."""
        # First adjustment sets initial trust + delta
        result = await adjust_trust("user_444", 2, "Gave me treats!", db_path=test_db)

        assert "Trust Level Adjusted" in result
        assert "Gave me treats!" in result
        # New trust should be 7 (default 5 + 2)
        assert "7/10" in result

    @pytest.mark.asyncio
    async def test_adjust_trust_decrease(self, test_db: Path):
        """Should decrease trust level."""
        result = await adjust_trust("user_555", -2, "Mentioned cats suspiciously", db_path=test_db)

        assert "Trust Level Adjusted" in result
        # New trust should be 3 (default 5 - 2)
        assert "3/10" in result

    @pytest.mark.asyncio
    async def test_adjust_trust_bounded_max(self, test_db: Path):
        """Trust should not exceed 10."""
        result = await adjust_trust("user_666", 10, "Maximum friend!", db_path=test_db)

        # Should be capped at 10
        assert "10/10" in result

    @pytest.mark.asyncio
    async def test_adjust_trust_bounded_min(self, test_db: Path):
        """Trust should not go below 1."""
        result = await adjust_trust("user_777", -10, "Very suspicious!", db_path=test_db)

        # Should be capped at 1
        assert "1/10" in result


class TestWriteDiary:
    """Tests for write_diary - puppy's personal thoughts!"""

    @pytest.mark.asyncio
    async def test_write_diary_success(self, test_db: Path):
        """Should successfully write a diary entry."""
        result = await write_diary("Today I chased a squirrel!", "excited", db_path=test_db)

        assert "Diary Entry" in result
        assert "excited" in result.lower()
        assert "Today I chased a squirrel!" in result

    @pytest.mark.asyncio
    async def test_write_diary_includes_mood_emoji(self, test_db: Path):
        """Should include appropriate mood emoji."""
        result = await write_diary("Feeling sleepy...", "sleepy", db_path=test_db)

        # Should have sleepy emoji
        assert "😴" in result


class TestRecallDiary:
    """Tests for recall_diary - reading past thoughts!"""

    @pytest.mark.asyncio
    async def test_recall_empty_diary(self, test_db: Path):
        """Recalling empty diary should return friendly message."""
        result = await recall_diary(days=7, db_path=test_db)

        assert "no diary entries" in result.lower()

    @pytest.mark.asyncio
    async def test_recall_diary_with_entries(self, test_db: Path):
        """Should return recent diary entries."""
        # Write some entries
        await write_diary("First thought!", "happy", db_path=test_db)
        await write_diary("Second thought!", "curious", db_path=test_db)

        result = await recall_diary(days=7, db_path=test_db)

        assert "First thought!" in result
        assert "Second thought!" in result
        assert "2 entries found" in result


class TestHelperFunctions:
    """Tests for internal helper functions."""

    def test_get_trust_description_all_levels(self):
        """Should return descriptions for all trust levels."""
        for level in range(1, 11):
            desc = _get_trust_description(level)
            assert desc  # Should not be empty
            assert isinstance(desc, str)

    def test_get_trust_description_known_levels(self):
        """Test specific trust level descriptions."""
        assert "Maximum Suspicion" in _get_trust_description(1)
        assert "Neutral" in _get_trust_description(5)
        assert "ULTIMATE BEST FRIEND" in _get_trust_description(10)

    def test_get_mood_emoji_known_moods(self):
        """Should return correct emojis for known moods."""
        assert _get_mood_emoji("excited") == "🎉"
        assert _get_mood_emoji("sleepy") == "😴"
        assert _get_mood_emoji("suspicious") == "👀"
        assert _get_mood_emoji("zoomies") == "💨"

    def test_get_mood_emoji_case_insensitive(self):
        """Should work regardless of case."""
        assert _get_mood_emoji("EXCITED") == "🎉"
        assert _get_mood_emoji("Sleepy") == "😴"

    def test_get_mood_emoji_unknown_defaults(self):
        """Unknown moods should return default puppy emoji."""
        assert _get_mood_emoji("unknown_mood") == "🐕"
        assert _get_mood_emoji("") == "🐕"


class TestToolDocstrings:
    """Verify tools have proper puppy-personality docstrings."""

    def test_recall_user_docstring(self):
        """recall_user should have chaotic docstring."""
        assert "Remember everything about this human" in recall_user.__doc__
        assert "trust level" in recall_user.__doc__.lower()

    def test_update_memory_docstring(self):
        """update_memory should have chaotic docstring."""
        assert "Write a new observation" in update_memory.__doc__
        assert "forever" in update_memory.__doc__.lower()

    def test_add_nickname_docstring(self):
        """add_nickname should have chaotic docstring."""
        assert "nickname" in add_nickname.__doc__.lower()
        assert "might not like it" in add_nickname.__doc__.lower()

    def test_adjust_trust_docstring(self):
        """adjust_trust should have chaotic docstring."""
        assert "trust" in adjust_trust.__doc__.lower()
        assert "treats" in adjust_trust.__doc__.lower()

    def test_write_diary_docstring(self):
        """write_diary should have chaotic docstring."""
        assert "diary" in write_diary.__doc__.lower()
        assert "important puppy thoughts" in write_diary.__doc__.lower()

    def test_recall_diary_docstring(self):
        """recall_diary should have chaotic docstring."""
        assert "thinking about" in recall_diary.__doc__.lower()
