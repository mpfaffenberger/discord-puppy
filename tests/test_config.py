"""Tests for Discord Puppy configuration module."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from discord_puppy.config import Settings, clear_settings_cache, get_settings


class TestSettings:
    """Test the Settings model."""

    def test_settings_with_required_fields(self):
        """Settings should work with just required fields."""
        settings = Settings(
            DISCORD_TOKEN="test-token",
            ANTHROPIC_API_KEY="test-key",
        )
        assert settings.DISCORD_TOKEN == "test-token"
        assert settings.ANTHROPIC_API_KEY == "test-key"

    def test_settings_default_values(self):
        """Settings should have correct default values."""
        settings = Settings(
            DISCORD_TOKEN="test-token",
            ANTHROPIC_API_KEY="test-key",
        )
        assert settings.CHAOS_LEVEL == 0.5
        assert settings.RESPONSE_CHANCE == 0.6
        assert settings.SPONTANEOUS_MIN_SECONDS == 60
        assert settings.SPONTANEOUS_MAX_SECONDS == 300
        assert settings.ZOOMIES_CHANCE == 0.1
        assert settings.MAX_IMAGE_HEIGHT == 768
        assert settings.MEMORY_CONTEXT_LIMIT == 5

    def test_database_path_expands_tilde(self):
        """DATABASE_PATH should expand ~ to home directory."""
        settings = Settings(
            DISCORD_TOKEN="test-token",
            ANTHROPIC_API_KEY="test-key",
            DATABASE_PATH="~/.discord_puppy/brain.db",
        )
        assert "~" not in settings.DATABASE_PATH
        assert str(Path.home()) in settings.DATABASE_PATH

    def test_custom_database_path(self):
        """Should accept custom database paths."""
        settings = Settings(
            DISCORD_TOKEN="test-token",
            ANTHROPIC_API_KEY="test-key",
            DATABASE_PATH="/custom/path/brain.db",
        )
        assert settings.DATABASE_PATH == "/custom/path/brain.db"

    def test_chaos_level_validation_too_high(self):
        """CHAOS_LEVEL above 1.0 should raise error."""
        with pytest.raises(ValidationError):
            Settings(
                DISCORD_TOKEN="test-token",
                ANTHROPIC_API_KEY="test-key",
                CHAOS_LEVEL=1.5,
            )

    def test_chaos_level_validation_too_low(self):
        """CHAOS_LEVEL below 0.0 should raise error."""
        with pytest.raises(ValidationError):
            Settings(
                DISCORD_TOKEN="test-token",
                ANTHROPIC_API_KEY="test-key",
                CHAOS_LEVEL=-0.1,
            )

    def test_response_chance_validation(self):
        """RESPONSE_CHANCE must be between 0 and 1."""
        with pytest.raises(ValidationError):
            Settings(
                DISCORD_TOKEN="test-token",
                ANTHROPIC_API_KEY="test-key",
                RESPONSE_CHANCE=2.0,
            )

    def test_zoomies_chance_validation(self):
        """ZOOMIES_CHANCE must be between 0 and 1."""
        with pytest.raises(ValidationError):
            Settings(
                DISCORD_TOKEN="test-token",
                ANTHROPIC_API_KEY="test-key",
                ZOOMIES_CHANCE=-0.5,
            )

    def test_positive_int_validation(self):
        """Integer settings must be positive."""
        with pytest.raises(ValidationError):
            Settings(
                DISCORD_TOKEN="test-token",
                ANTHROPIC_API_KEY="test-key",
                SPONTANEOUS_MIN_SECONDS=0,
            )

    def test_settings_immutable(self):
        """Settings should be immutable (frozen)."""
        settings = Settings(
            DISCORD_TOKEN="test-token",
            ANTHROPIC_API_KEY="test-key",
        )
        with pytest.raises(ValidationError):
            settings.CHAOS_LEVEL = 1.0

    def test_edge_case_valid_probabilities(self):
        """Probability of exactly 0.0 and 1.0 should be valid."""
        settings = Settings(
            DISCORD_TOKEN="test-token",
            ANTHROPIC_API_KEY="test-key",
            CHAOS_LEVEL=0.0,
            RESPONSE_CHANCE=1.0,
            ZOOMIES_CHANCE=0.0,
        )
        assert settings.CHAOS_LEVEL == 0.0
        assert settings.RESPONSE_CHANCE == 1.0
        assert settings.ZOOMIES_CHANCE == 0.0


class TestGetSettings:
    """Test the get_settings function."""

    def setup_method(self):
        """Clear cache before each test."""
        clear_settings_cache()

    def test_get_settings_from_env(self):
        """get_settings should load from environment variables."""
        env_vars = {
            "DISCORD_TOKEN": "env-token",
            "ANTHROPIC_API_KEY": "env-key",
            "CHAOS_LEVEL": "0.8",
            "RESPONSE_CHANCE": "0.3",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            settings = get_settings()
            assert settings.DISCORD_TOKEN == "env-token"
            assert settings.ANTHROPIC_API_KEY == "env-key"
            assert settings.CHAOS_LEVEL == 0.8
            assert settings.RESPONSE_CHANCE == 0.3

    def test_get_settings_cached(self):
        """get_settings should return cached instance."""
        env_vars = {
            "DISCORD_TOKEN": "token1",
            "ANTHROPIC_API_KEY": "key1",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            settings1 = get_settings()
            settings2 = get_settings()
            assert settings1 is settings2

    def test_clear_settings_cache(self):
        """clear_settings_cache should allow reloading settings."""
        env_vars1 = {
            "DISCORD_TOKEN": "token1",
            "ANTHROPIC_API_KEY": "key1",
        }
        with patch.dict(os.environ, env_vars1, clear=False):
            settings1 = get_settings()

        clear_settings_cache()

        env_vars2 = {
            "DISCORD_TOKEN": "token2",
            "ANTHROPIC_API_KEY": "key2",
        }
        with patch.dict(os.environ, env_vars2, clear=False):
            settings2 = get_settings()

        assert settings1.DISCORD_TOKEN == "token1"
        assert settings2.DISCORD_TOKEN == "token2"
