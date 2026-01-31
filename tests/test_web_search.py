"""
Tests for the web search tool! 🔍🐕

Tests cover:
- Successful searches with various result types
- Error handling for network issues
- Empty query handling
- Chaos/distraction feature (mocked for determinism)
"""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from discord_puppy.tools.web_search import DISTRACTION_MESSAGES, _format_results, web_search

# Sample DuckDuckGo API responses for testing
SAMPLE_ABSTRACT_RESPONSE = {
    "Abstract": "Python is a high-level programming language.",
    "AbstractSource": "Wikipedia",
    "AbstractURL": "https://en.wikipedia.org/wiki/Python",
    "Answer": "",
    "Definition": "",
    "RelatedTopics": [],
    "Infobox": {},
}

SAMPLE_ANSWER_RESPONSE = {
    "Abstract": "",
    "Answer": "42",
    "AnswerType": "calc",
    "Definition": "",
    "RelatedTopics": [],
    "Infobox": {},
}

SAMPLE_EMPTY_RESPONSE = {
    "Abstract": "",
    "Answer": "",
    "Definition": "",
    "RelatedTopics": [],
    "Infobox": {},
}

SAMPLE_RELATED_TOPICS_RESPONSE = {
    "Abstract": "",
    "Answer": "",
    "Definition": "",
    "RelatedTopics": [
        {"Text": "First related topic about dogs"},
        {"Text": "Second related topic about puppies"},
        {"Text": "Third related topic about treats"},
        {"Text": "Fourth topic we should skip"},
    ],
    "Infobox": {},
}


class TestWebSearch:
    """Test suite for web_search function."""

    @pytest.mark.asyncio
    async def test_successful_search_with_abstract(self):
        """Test that abstract results are formatted correctly."""
        with patch("discord_puppy.tools.web_search.random.random", return_value=0.5):  # No chaos
            with patch("discord_puppy.tools.web_search.httpx.AsyncClient") as mock_client:
                mock_response = MagicMock()
                mock_response.json.return_value = SAMPLE_ABSTRACT_RESPONSE
                mock_response.raise_for_status = MagicMock()

                mock_instance = AsyncMock()
                mock_instance.get.return_value = mock_response
                mock_instance.__aenter__.return_value = mock_instance
                mock_instance.__aexit__.return_value = None
                mock_client.return_value = mock_instance

                result = await web_search("python programming")

                assert "python programming" in result
                assert "Wikipedia" in result
                assert "Python is a high-level programming language" in result

    @pytest.mark.asyncio
    async def test_successful_search_with_answer(self):
        """Test that direct answers are formatted correctly."""
        with patch("discord_puppy.tools.web_search.random.random", return_value=0.5):
            with patch("discord_puppy.tools.web_search.httpx.AsyncClient") as mock_client:
                mock_response = MagicMock()
                mock_response.json.return_value = SAMPLE_ANSWER_RESPONSE
                mock_response.raise_for_status = MagicMock()

                mock_instance = AsyncMock()
                mock_instance.get.return_value = mock_response
                mock_instance.__aenter__.return_value = mock_instance
                mock_instance.__aexit__.return_value = None
                mock_client.return_value = mock_instance

                result = await web_search("6 * 7")

                assert "42" in result
                assert "Direct Answer" in result

    @pytest.mark.asyncio
    async def test_chaos_distraction(self):
        """Test that 10% chaos chance returns distraction message."""
        with patch(
            "discord_puppy.tools.web_search.random.random", return_value=0.05
        ):  # < 0.10 triggers chaos
            with patch("discord_puppy.tools.web_search.random.choice") as mock_choice:
                mock_choice.return_value = "I got distracted chasing my tail! 🐕💫"

                result = await web_search("anything")

                assert result == "I got distracted chasing my tail! 🐕💫"
                mock_choice.assert_called_once()

    @pytest.mark.asyncio
    async def test_no_chaos_above_threshold(self):
        """Test that chaos doesn't trigger above 10% threshold."""
        with patch(
            "discord_puppy.tools.web_search.random.random", return_value=0.15
        ):  # > 0.10, no chaos
            with patch("discord_puppy.tools.web_search.httpx.AsyncClient") as mock_client:
                mock_response = MagicMock()
                mock_response.json.return_value = SAMPLE_ABSTRACT_RESPONSE
                mock_response.raise_for_status = MagicMock()

                mock_instance = AsyncMock()
                mock_instance.get.return_value = mock_response
                mock_instance.__aenter__.return_value = mock_instance
                mock_instance.__aexit__.return_value = None
                mock_client.return_value = mock_instance

                result = await web_search("test")

                # Should get real results, not distraction
                assert result not in DISTRACTION_MESSAGES

    @pytest.mark.asyncio
    async def test_empty_query(self):
        """Test handling of empty query strings."""
        with patch("discord_puppy.tools.web_search.random.random", return_value=0.5):
            result = await web_search("")
            assert "need something to search" in result.lower()

            result2 = await web_search("   ")
            assert "need something to search" in result2.lower()

    @pytest.mark.asyncio
    async def test_timeout_error_handling(self):
        """Test graceful handling of timeout errors."""
        with patch("discord_puppy.tools.web_search.random.random", return_value=0.5):
            with patch("discord_puppy.tools.web_search.httpx.AsyncClient") as mock_client:
                mock_instance = AsyncMock()
                mock_instance.get.side_effect = httpx.TimeoutException("Timed out")
                mock_instance.__aenter__.return_value = mock_instance
                mock_instance.__aexit__.return_value = None
                mock_client.return_value = mock_instance

                result = await web_search("slow query")

                assert "too long" in result.lower() or "bored" in result.lower()

    @pytest.mark.asyncio
    async def test_network_error_handling(self):
        """Test graceful handling of network errors."""
        with patch("discord_puppy.tools.web_search.random.random", return_value=0.5):
            with patch("discord_puppy.tools.web_search.httpx.AsyncClient") as mock_client:
                mock_instance = AsyncMock()
                mock_instance.get.side_effect = httpx.ConnectError("Connection failed")
                mock_instance.__aenter__.return_value = mock_instance
                mock_instance.__aexit__.return_value = None
                mock_client.return_value = mock_instance

                result = await web_search("network test")

                assert "bork" in result.lower() or "network" in result.lower()


class TestFormatResults:
    """Test suite for _format_results helper."""

    def test_format_abstract(self):
        """Test formatting of abstract results."""
        result = _format_results("test", SAMPLE_ABSTRACT_RESPONSE)

        assert "test" in result
        assert "Wikipedia" in result
        assert "Python is a high-level" in result

    def test_format_answer(self):
        """Test formatting of direct answers."""
        result = _format_results("math", SAMPLE_ANSWER_RESPONSE)

        assert "42" in result
        assert "calc" in result

    def test_format_empty_results(self):
        """Test formatting when no results found."""
        result = _format_results("obscure query", SAMPLE_EMPTY_RESPONSE)

        assert "couldn't find" in result.lower()
        assert "duckduckgo.com" in result.lower()

    def test_format_related_topics_limit(self):
        """Test that related topics are limited to 3."""
        result = _format_results("dogs", SAMPLE_RELATED_TOPICS_RESPONSE)

        assert "First related topic" in result
        assert "Second related topic" in result
        assert "Third related topic" in result
        assert "Fourth topic" not in result  # Should be skipped
