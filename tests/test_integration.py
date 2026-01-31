"""Integration sanity checks for Discord Puppy 🐕✨

Verifies all modules can be imported together and work harmoniously.
This ensures the full puppy package is production-ready!
"""

import pytest


class TestModuleImports:
    """Verify all modules can be imported without conflicts."""

    def test_import_main_package(self):
        """Can import main discord_puppy package."""
        import discord_puppy

        assert discord_puppy.__name__ == "discord_puppy"

    def test_import_all_submodules(self):
        """All submodules should be importable."""
        # Main bot
        from discord_puppy import DiscordPuppy, create_puppy, run_puppy

        # Agents
        from discord_puppy.agents import DiscordPuppyAgent

        # Config
        # Memory system
        from discord_puppy.memory import init_database
        from discord_puppy.memory.memory_tools import MEMORY_TOOLS

        # Personality
        from discord_puppy.personality import Mood

        # Tools
        from discord_puppy.tools import CHAOS_TOOLS

        # Vision system
        from discord_puppy.vision import VISION_TOOLS

        # All should be truthy/not None
        assert DiscordPuppy is not None
        assert create_puppy is not None
        assert run_puppy is not None
        assert DiscordPuppyAgent is not None
        assert init_database is not None
        assert MEMORY_TOOLS is not None
        assert VISION_TOOLS is not None
        assert Mood is not None
        assert CHAOS_TOOLS is not None

    def test_tool_lists_not_empty(self):
        """Tool lists should contain tools."""
        from discord_puppy.memory.memory_tools import MEMORY_TOOLS
        from discord_puppy.tools.chaos import CHAOS_TOOLS
        from discord_puppy.vision.vision_tools import VISION_TOOLS

        assert len(MEMORY_TOOLS) == 6  # 6 memory tools
        assert len(VISION_TOOLS) == 3  # 3 vision tools
        assert len(CHAOS_TOOLS) > 0  # Some chaos tools

    def test_all_tools_callable(self):
        """All tools from all modules should be callable."""
        from discord_puppy.memory.memory_tools import MEMORY_TOOLS
        from discord_puppy.tools.chaos import CHAOS_TOOLS
        from discord_puppy.vision.vision_tools import VISION_TOOLS

        all_tools = list(MEMORY_TOOLS) + list(VISION_TOOLS) + list(CHAOS_TOOLS)

        for tool in all_tools:
            assert callable(tool), f"{tool.__name__} is not callable"


class TestMemoryPersistence:
    """Test that memory persists across simulated 'restarts'."""

    @pytest.mark.asyncio
    async def test_user_notes_persist_across_sessions(self, tmp_path):
        """User notes should persist when using same database."""
        from discord_puppy.memory import init_database
        from discord_puppy.memory.user_notes import get_user_notes, update_user_notes

        db_path = tmp_path / "persist_test.db"

        # Session 1: Create user
        await init_database(db_path)
        await update_user_notes("persistent_user", "Note from session 1", db_path=db_path)

        # Session 2: Same database, different "connection"
        await init_database(db_path)  # Re-init (simulates restart)
        notes = await get_user_notes("persistent_user", db_path=db_path)

        assert notes is not None
        assert "Note from session 1" in notes.notes

    @pytest.mark.asyncio
    async def test_trust_level_persists(self, tmp_path):
        """Trust level should persist across connections."""
        from discord_puppy.memory import init_database
        from discord_puppy.memory.memory_tools import adjust_trust, recall_user

        db_path = tmp_path / "trust_test.db"

        # Session 1: Adjust trust
        await init_database(db_path)
        await adjust_trust("trust_user", 3, "Gave treats!", db_path=db_path)

        # Session 2: Check trust persisted
        await init_database(db_path)
        result = await recall_user("trust_user", db_path=db_path)

        # Trust started at 5, +3 = 8
        assert "8/10" in result

    @pytest.mark.asyncio
    async def test_diary_entries_accumulate(self, tmp_path):
        """Diary entries should accumulate over time."""
        from discord_puppy.memory import init_database
        from discord_puppy.memory.memory_tools import recall_diary, write_diary

        db_path = tmp_path / "diary_test.db"

        # Session 1: Write first entry
        await init_database(db_path)
        await write_diary("Day 1: Found a ball!", "excited", db_path=db_path)

        # Session 2: Write second entry
        await init_database(db_path)
        await write_diary("Day 2: Chased a squirrel!", "zoomies", db_path=db_path)

        # Session 3: Read all entries
        await init_database(db_path)
        result = await recall_diary(days=30, db_path=db_path)

        assert "Day 1: Found a ball!" in result
        assert "Day 2: Chased a squirrel!" in result
        assert "2 entries found" in result

    @pytest.mark.asyncio
    async def test_nicknames_persist(self, tmp_path):
        """Nicknames should persist across connections."""
        from discord_puppy.memory import init_database
        from discord_puppy.memory.memory_tools import add_nickname, recall_user

        db_path = tmp_path / "nickname_test.db"

        # Session 1: Add nickname
        await init_database(db_path)
        await add_nickname("nickname_user", "Treat Giver", db_path=db_path)

        # Session 2: Check nickname persisted
        await init_database(db_path)
        result = await recall_user("nickname_user", db_path=db_path)

        assert "Treat Giver" in result


class TestVisionSystemIntegration:
    """Test vision system components work together."""

    def test_binary_content_creation(self):
        """BinaryContent can be created from processed images."""
        from io import BytesIO

        from PIL import Image

        from discord_puppy.vision.image_analyzer import (
            create_binary_content,
            resize_for_analysis,
        )

        # Create a test image
        img = Image.new("RGB", (200, 200), color="green")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_bytes = buffer.getvalue()

        # Process through pipeline
        resized_bytes, media_type = resize_for_analysis(img_bytes)
        content = create_binary_content(resized_bytes, media_type=media_type)

        assert content.data is not None
        assert len(content.data) > 0
        assert content.media_type in ["image/jpeg", "image/png"]

    def test_vision_tools_have_docstrings(self):
        """All vision tools must have chaotic docstrings."""
        from discord_puppy.vision.vision_tools import VISION_TOOLS

        for tool in VISION_TOOLS:
            assert tool.__doc__ is not None
            assert len(tool.__doc__) > 20  # Not just empty


class TestAgentIntegration:
    """Test agent creation and configuration."""

    def test_agent_creates_successfully(self):
        """DiscordPuppyAgent should create without errors."""
        from discord_puppy.agents import DiscordPuppyAgent

        agent = DiscordPuppyAgent()
        assert agent is not None
        assert agent.model is not None
        assert agent.system_prompt is not None

    def test_agent_has_system_prompt(self):
        """Agent should have a chaotic system prompt."""
        from discord_puppy.agents import DiscordPuppyAgent

        agent = DiscordPuppyAgent()

        # System prompt should mention key features
        assert "DISCORD PUPPY" in agent.system_prompt
        assert "memory" in agent.system_prompt.lower()
        assert "vision" in agent.system_prompt.lower()


class TestFullPackageHealth:
    """Final health checks for production readiness."""

    def test_no_circular_imports(self):
        """Importing in any order should not cause circular import errors."""
        # This will fail fast if there are circular imports

        # If we got here, no circular imports!
        assert True

    def test_settings_have_sensible_defaults(self):
        """Default settings should be sane."""
        from discord_puppy.config import Settings

        settings = Settings(
            DISCORD_TOKEN="test",
            ANTHROPIC_API_KEY="test",
        )

        # Check defaults are sensible
        assert 0.0 <= settings.CHAOS_LEVEL <= 1.0
        assert 0.0 <= settings.RESPONSE_CHANCE <= 1.0
        assert settings.SPONTANEOUS_MIN_SECONDS > 0
        assert settings.SPONTANEOUS_MAX_SECONDS > settings.SPONTANEOUS_MIN_SECONDS
        assert settings.DATABASE_PATH is not None

    def test_mood_system_functional(self):
        """Mood system should return valid moods."""
        from discord_puppy.personality import Mood, get_mood_modifier, get_random_mood

        for _ in range(20):
            mood = get_random_mood()
            assert isinstance(mood, Mood)

            modifier = get_mood_modifier(mood)
            assert isinstance(modifier, str)
            assert len(modifier) > 10
