"""Tests for the Discord Puppy bot! 🐕

These tests focus on testable parts of the bot without requiring
a real Discord connection.
"""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch

from discord_puppy.config import Settings


class TestBotImports:
    """Test that bot module imports correctly."""

    def test_import_discord_puppy_class(self):
        """DiscordPuppy class should be importable."""
        from discord_puppy.bot import DiscordPuppy
        assert DiscordPuppy is not None

    def test_import_create_puppy(self):
        """create_puppy function should be importable."""
        from discord_puppy.bot import create_puppy
        assert callable(create_puppy)

    def test_import_run_puppy(self):
        """run_puppy function should be importable."""
        from discord_puppy.bot import run_puppy
        assert callable(run_puppy)

    def test_main_package_exports_bot(self):
        """Bot should be exported from main package."""
        from discord_puppy import DiscordPuppy, create_puppy, run_puppy
        assert DiscordPuppy is not None
        assert callable(create_puppy)
        assert callable(run_puppy)


class TestBotInitialization:
    """Test bot initialization."""

    @pytest.fixture
    def mock_settings(self) -> Settings:
        """Create mock settings for testing."""
        return Settings(
            DISCORD_TOKEN="test_token_12345",
            ANTHROPIC_API_KEY="test_api_key_12345",
            CHAOS_LEVEL=0.5,
            RESPONSE_CHANCE=0.6,
            SPONTANEOUS_MIN_SECONDS=60,
            SPONTANEOUS_MAX_SECONDS=300,
            DATABASE_PATH="/tmp/test_puppy.db",
        )

    def test_bot_creates_with_settings(self, mock_settings: Settings):
        """Bot should initialize with provided settings."""
        from discord_puppy.bot import DiscordPuppy
        
        puppy = DiscordPuppy(settings=mock_settings)
        
        assert puppy.settings == mock_settings
        assert puppy.settings.CHAOS_LEVEL == 0.5

    def test_bot_has_agent(self, mock_settings: Settings):
        """Bot should have an agent instance."""
        from discord_puppy.bot import DiscordPuppy
        from discord_puppy.agents import DiscordPuppyAgent
        
        puppy = DiscordPuppy(settings=mock_settings)
        
        assert puppy.agent is not None
        assert isinstance(puppy.agent, DiscordPuppyAgent)

    def test_bot_has_mood(self, mock_settings: Settings):
        """Bot should have a current mood."""
        from discord_puppy.bot import DiscordPuppy
        from discord_puppy.personality import Mood
        
        puppy = DiscordPuppy(settings=mock_settings)
        
        assert puppy.current_mood is not None
        assert isinstance(puppy.current_mood, Mood)

    def test_bot_tracks_known_users(self, mock_settings: Settings):
        """Bot should initialize user tracking."""
        from discord_puppy.bot import DiscordPuppy
        
        puppy = DiscordPuppy(settings=mock_settings)
        
        assert hasattr(puppy, '_known_users')
        assert isinstance(puppy._known_users, dict)

    def test_create_puppy_function(self, mock_settings: Settings):
        """create_puppy should return a DiscordPuppy instance."""
        from discord_puppy.bot import create_puppy, DiscordPuppy
        
        puppy = create_puppy(settings=mock_settings)
        
        assert isinstance(puppy, DiscordPuppy)
        assert puppy.settings == mock_settings


class TestBotHelpers:
    """Test bot helper methods."""

    @pytest.fixture
    def mock_settings(self) -> Settings:
        """Create mock settings for testing."""
        return Settings(
            DISCORD_TOKEN="test_token_12345",
            ANTHROPIC_API_KEY="test_api_key_12345",
            DATABASE_PATH="/tmp/test_puppy.db",
        )

    @pytest.fixture
    def puppy(self, mock_settings: Settings):
        """Create a bot instance for testing."""
        from discord_puppy.bot import DiscordPuppy
        return DiscordPuppy(settings=mock_settings)

    def test_format_user_context_basic(self, puppy):
        """Test user context formatting with minimal data."""
        context = {
            "username": "TestUser",
            "user_id": "123456789",
        }
        
        formatted = puppy._format_user_context_for_prompt(context)
        
        assert "TestUser" in formatted
        assert "123456789" in formatted
        assert "Current User Context" in formatted

    def test_format_user_context_full(self, puppy):
        """Test user context formatting with full data."""
        context = {
            "username": "FullUser",
            "user_id": "987654321",
            "trust_level": 8,
            "notes": "Loves treats",
            "detailed_notes": "Very friendly human, always shares snacks",
        }
        
        formatted = puppy._format_user_context_for_prompt(context)
        
        assert "FullUser" in formatted
        assert "987654321" in formatted
        assert "8/10" in formatted
        assert "🎾" in formatted  # Trust balls
        assert "Loves treats" in formatted
        assert "Very friendly" in formatted
        assert "update_memory" in formatted  # Should remind to use memory

    def test_format_user_context_empty(self, puppy):
        """Test user context formatting with empty data."""
        context = {}
        
        formatted = puppy._format_user_context_for_prompt(context)
        
        assert "Current User Context" in formatted
        # Should still work, just be minimal


class TestBotMoodSystem:
    """Test mood-related functionality."""

    @pytest.fixture
    def mock_settings(self) -> Settings:
        """Create mock settings for testing."""
        return Settings(
            DISCORD_TOKEN="test_token_12345",
            ANTHROPIC_API_KEY="test_api_key_12345",
            DATABASE_PATH="/tmp/test_puppy.db",
        )

    @pytest.fixture
    def puppy(self, mock_settings: Settings):
        """Create a bot instance for testing."""
        from discord_puppy.bot import DiscordPuppy
        return DiscordPuppy(settings=mock_settings)

    @pytest.mark.asyncio
    async def test_maybe_change_mood_doesnt_crash(self, puppy):
        """Mood change logic should not crash."""
        from discord_puppy.personality import Mood
        
        # Should not raise
        await puppy._maybe_change_mood()
        
        # Should still have a valid mood
        assert isinstance(puppy.current_mood, Mood)


class TestBotChunking:
    """Test message chunking for long responses."""

    @pytest.fixture
    def mock_settings(self) -> Settings:
        """Create mock settings for testing."""
        return Settings(
            DISCORD_TOKEN="test_token_12345",
            ANTHROPIC_API_KEY="test_api_key_12345",
            DATABASE_PATH="/tmp/test_puppy.db",
        )

    @pytest.fixture
    def puppy(self, mock_settings: Settings):
        """Create a bot instance for testing."""
        from discord_puppy.bot import DiscordPuppy
        return DiscordPuppy(settings=mock_settings)

    @pytest.mark.asyncio
    async def test_send_chunked_short_message(self, puppy):
        """Short messages should be sent as single message."""
        mock_channel = AsyncMock()
        
        await puppy._send_chunked(mock_channel, "Hello world!")
        
        mock_channel.send.assert_called_once_with("Hello world!")

    @pytest.mark.asyncio
    async def test_send_chunked_long_message(self, puppy):
        """Long messages should be split into chunks."""
        mock_channel = AsyncMock()
        
        # Create a message longer than max_length with newlines
        # (chunking splits on newlines to preserve formatting)
        long_message = "\n".join(["Line " + str(i) + " " + "A" * 50 for i in range(50)])
        
        await puppy._send_chunked(mock_channel, long_message, max_length=500)
        
        # Should have been called multiple times
        assert mock_channel.send.call_count > 1

    @pytest.mark.asyncio
    async def test_send_chunked_respects_newlines(self, puppy):
        """Chunking should try to respect line boundaries."""
        mock_channel = AsyncMock()
        
        # Create a message with newlines
        message = "Line 1\n" * 50 + "Line 2\n" * 50
        
        await puppy._send_chunked(mock_channel, message, max_length=200)
        
        # Should have been called multiple times
        assert mock_channel.send.call_count > 1
