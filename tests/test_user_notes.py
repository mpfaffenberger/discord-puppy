"""Tests for user_notes CRUD operations 🧪🐕

Tests all the memory functions for Discord Puppy's user tracking.
"""

import tempfile
from pathlib import Path

import pytest
import pytest_asyncio

from discord_puppy.memory.database import init_database
from discord_puppy.memory.user_notes import (
    InteractionMemory,
    UserNotes,
    get_recent_interactions,
    get_user_notes,
    get_user_summary,
    record_interaction,
    update_user_notes,
)


@pytest_asyncio.fixture
async def temp_db():
    """Create a temporary database for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_brain.db"
        await init_database(db_path)
        yield db_path


class TestUserNotesModel:
    """Tests for the UserNotes Pydantic model."""

    def test_create_user_notes_minimal(self):
        """Can create UserNotes with just user_id."""
        notes = UserNotes(user_id="123")
        assert notes.user_id == "123"
        assert notes.discord_username == ""
        assert notes.display_name == ""
        assert notes.notes == ""
        assert notes.trust_level == 5
        assert notes.nicknames == []
        assert notes.favorite_topics == []

    def test_create_user_notes_full(self):
        """Can create UserNotes with all fields."""
        notes = UserNotes(
            user_id="456",
            discord_username="cooldog",
            display_name="Cool Dog",
            notes="Very cool!",
            trust_level=8,
            nicknames=["doggo", "pupper"],
            favorite_topics=["memes", "dogs"],
        )
        assert notes.user_id == "456"
        assert notes.discord_username == "cooldog"
        assert notes.display_name == "Cool Dog"
        assert notes.notes == "Very cool!"
        assert notes.trust_level == 8
        assert notes.nicknames == ["doggo", "pupper"]
        assert notes.favorite_topics == ["memes", "dogs"]

    def test_trust_level_validation(self):
        """Trust level must be between 1 and 10."""
        with pytest.raises(ValueError):
            UserNotes(user_id="123", trust_level=0)

        with pytest.raises(ValueError):
            UserNotes(user_id="123", trust_level=11)

        # Valid edge cases
        notes_min = UserNotes(user_id="123", trust_level=1)
        assert notes_min.trust_level == 1

        notes_max = UserNotes(user_id="123", trust_level=10)
        assert notes_max.trust_level == 10


class TestInteractionMemoryModel:
    """Tests for the InteractionMemory Pydantic model."""

    def test_create_interaction_memory(self):
        """Can create InteractionMemory with required fields."""
        from datetime import datetime

        memory = InteractionMemory(
            id=1,
            user_id="123",
            timestamp=datetime.now(),
            summary="Helped with code",
        )
        assert memory.id == 1
        assert memory.user_id == "123"
        assert memory.summary == "Helped with code"
        assert memory.was_helpful is False
        assert memory.mood == ""
        assert memory.notable_quotes == []

    def test_create_interaction_memory_full(self):
        """Can create InteractionMemory with all fields."""
        from datetime import datetime

        memory = InteractionMemory(
            id=42,
            user_id="456",
            timestamp=datetime(2024, 1, 15, 10, 30),
            summary="Epic debugging session",
            was_helpful=True,
            mood="excited",
            notable_quotes=["That's awesome!", "WOOF!"],
        )
        assert memory.id == 42
        assert memory.was_helpful is True
        assert memory.mood == "excited"
        assert len(memory.notable_quotes) == 2


class TestGetUserNotes:
    """Tests for get_user_notes function."""

    @pytest.mark.asyncio
    async def test_get_nonexistent_user_returns_none(self, temp_db):
        """Getting notes for unknown user returns None."""
        result = await get_user_notes("nonexistent", db_path=temp_db)
        assert result is None

    @pytest.mark.asyncio
    async def test_get_user_notes_after_update(self, temp_db):
        """Can retrieve notes after creating them."""
        # First create a user by updating notes
        await update_user_notes("user123", "First note", db_path=temp_db)

        # Now retrieve
        notes = await get_user_notes("user123", db_path=temp_db)
        assert notes is not None
        assert notes.user_id == "user123"
        assert "First note" in notes.notes


class TestUpdateUserNotes:
    """Tests for update_user_notes function."""

    @pytest.mark.asyncio
    async def test_update_notes_creates_user(self, temp_db):
        """Updating notes for new user creates the user."""
        result = await update_user_notes("newuser", "Hello!", db_path=temp_db)
        assert result is True

        # Verify user was created
        notes = await get_user_notes("newuser", db_path=temp_db)
        assert notes is not None
        assert notes.notes == "Hello!"

    @pytest.mark.asyncio
    async def test_update_notes_appends(self, temp_db):
        """Updating notes appends to existing notes."""
        await update_user_notes("user1", "First", db_path=temp_db)
        await update_user_notes("user1", "Second", db_path=temp_db)

        notes = await get_user_notes("user1", db_path=temp_db)
        assert notes is not None
        assert "First" in notes.notes
        assert "Second" in notes.notes
        # Should be separated by newline
        assert "First\nSecond" in notes.notes


class TestRecordInteraction:
    """Tests for record_interaction function."""

    @pytest.mark.asyncio
    async def test_record_interaction_returns_id(self, temp_db):
        """Recording an interaction returns a valid ID."""
        interaction_id = await record_interaction(
            user_id="user1",
            summary="Helped with Python",
            mood="happy",
            was_helpful=True,
            db_path=temp_db,
        )
        assert interaction_id > 0

    @pytest.mark.asyncio
    async def test_record_multiple_interactions(self, temp_db):
        """Can record multiple interactions, IDs increment."""
        id1 = await record_interaction("user1", "First", "happy", True, db_path=temp_db)
        id2 = await record_interaction("user1", "Second", "calm", False, db_path=temp_db)

        assert id1 > 0
        assert id2 > id1

    @pytest.mark.asyncio
    async def test_record_interaction_creates_user(self, temp_db):
        """Recording interaction for new user creates user record."""
        await record_interaction("newbie", "First meeting", "excited", True, db_path=temp_db)

        notes = await get_user_notes("newbie", db_path=temp_db)
        assert notes is not None


class TestGetRecentInteractions:
    """Tests for get_recent_interactions function."""

    @pytest.mark.asyncio
    async def test_get_interactions_empty(self, temp_db):
        """Getting interactions for user with none returns empty list."""
        result = await get_recent_interactions("nobody", db_path=temp_db)
        assert result == []

    @pytest.mark.asyncio
    async def test_get_interactions_returns_list(self, temp_db):
        """Getting interactions returns list of InteractionMemory."""
        await record_interaction("user1", "Test 1", "happy", True, db_path=temp_db)
        await record_interaction("user1", "Test 2", "calm", False, db_path=temp_db)

        interactions = await get_recent_interactions("user1", db_path=temp_db)

        assert len(interactions) == 2
        assert all(isinstance(i, InteractionMemory) for i in interactions)

    @pytest.mark.asyncio
    async def test_get_interactions_respects_limit(self, temp_db):
        """Limit parameter restricts number of results."""
        for i in range(10):
            await record_interaction("user1", f"Test {i}", "calm", True, db_path=temp_db)

        interactions = await get_recent_interactions("user1", limit=3, db_path=temp_db)
        assert len(interactions) == 3

    @pytest.mark.asyncio
    async def test_get_interactions_ordered_recent_first(self, temp_db):
        """Interactions are returned most recent first."""
        await record_interaction("user1", "First", "calm", True, db_path=temp_db)
        await record_interaction("user1", "Second", "calm", True, db_path=temp_db)
        await record_interaction("user1", "Third", "calm", True, db_path=temp_db)

        interactions = await get_recent_interactions("user1", db_path=temp_db)

        assert interactions[0].summary == "Third"
        assert interactions[1].summary == "Second"
        assert interactions[2].summary == "First"


class TestGetUserSummary:
    """Tests for get_user_summary function."""

    @pytest.mark.asyncio
    async def test_summary_unknown_user_returns_empty(self, temp_db):
        """Summary for unknown user returns empty string."""
        result = await get_user_summary("nobody", db_path=temp_db)
        assert result == ""

    @pytest.mark.asyncio
    async def test_summary_contains_user_info(self, temp_db):
        """Summary contains user information."""
        await update_user_notes("user1", "Loves coding", db_path=temp_db)

        summary = await get_user_summary("user1", db_path=temp_db)

        assert "User:" in summary
        assert "trust:" in summary
        assert "Loves coding" in summary

    @pytest.mark.asyncio
    async def test_summary_includes_interactions(self, temp_db):
        """Summary includes recent interactions."""
        await update_user_notes("user1", "Test user", db_path=temp_db)
        await record_interaction("user1", "Helped debug", "happy", True, db_path=temp_db)

        summary = await get_user_summary("user1", db_path=temp_db)

        assert "Helped debug" in summary

    @pytest.mark.asyncio
    async def test_summary_truncates_long_notes(self, temp_db):
        """Long notes are truncated in summary."""
        long_notes = "A" * 500  # Very long notes
        await update_user_notes("user1", long_notes, db_path=temp_db)

        summary = await get_user_summary("user1", db_path=temp_db)

        # Summary should be shorter than original notes
        assert len(summary) < 500
        assert "..." in summary
