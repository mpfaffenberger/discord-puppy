"""
Tests for vision/vision_tools.py 👁️🐕

Tests the LLM-callable vision tools with mocked network calls.
No squirrels were harmed in the making of these tests. 🐿️
"""

from io import BytesIO
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
from PIL import Image
from pydantic_ai.messages import BinaryContent

from discord_puppy.vision.vision_tools import (
    VISION_TOOLS,
    analyze_attachment,
    analyze_image,
    what_do_i_see,
)


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def sample_png_bytes():
    """Create a small PNG image for testing."""
    img = Image.new("RGB", (100, 100), color="red")
    output = BytesIO()
    img.save(output, format="PNG")
    return output.getvalue()


@pytest.fixture
def sample_jpeg_bytes():
    """Create a small JPEG image for testing."""
    img = Image.new("RGB", (100, 100), color="blue")
    output = BytesIO()
    img.save(output, format="JPEG")
    return output.getvalue()


@pytest.fixture
def mock_binary_content(sample_jpeg_bytes):
    """Create a mock BinaryContent for testing."""
    return BinaryContent(data=sample_jpeg_bytes, media_type="image/jpeg")


# =============================================================================
# Test VISION_TOOLS Export
# =============================================================================


def test_vision_tools_contains_all_functions():
    """VISION_TOOLS export contains all 3 vision functions."""
    assert len(VISION_TOOLS) == 3
    
    tool_names = [t.__name__ for t in VISION_TOOLS]
    assert "analyze_image" in tool_names
    assert "analyze_attachment" in tool_names
    assert "what_do_i_see" in tool_names


def test_vision_tools_are_callable():
    """All tools in VISION_TOOLS are callable."""
    for tool in VISION_TOOLS:
        assert callable(tool)


# =============================================================================
# Test analyze_image()
# =============================================================================


@pytest.mark.asyncio
async def test_analyze_image_happy_path(sample_png_bytes, mock_binary_content):
    """analyze_image returns ToolReturn with BinaryContent on success."""
    with patch(
        "discord_puppy.vision.vision_tools.process_discord_image"
    ) as mock_process:
        mock_process.return_value = mock_binary_content

        result = await analyze_image("https://cdn.discordapp.com/test.png")

        # Should return a list (ToolReturn)
        assert isinstance(result, list)
        assert len(result) == 2

        # First element is the excited message
        assert "I CAN SEE IT" in result[0]
        assert "🐕" in result[0]

        # Second element is the BinaryContent
        assert isinstance(result[1], BinaryContent)
        assert result[1].media_type == "image/jpeg"

        # Verify the mock was called correctly
        mock_process.assert_called_once_with("https://cdn.discordapp.com/test.png")


@pytest.mark.asyncio
async def test_analyze_image_network_error():
    """analyze_image returns error message on network failure."""
    with patch(
        "discord_puppy.vision.vision_tools.process_discord_image"
    ) as mock_process:
        mock_process.side_effect = httpx.RequestError("Connection failed")

        result = await analyze_image("https://cdn.discordapp.com/broken.png")

        # Should still return a list
        assert isinstance(result, list)
        assert len(result) == 1

        # Should contain error info with puppy flair
        error_msg = result[0]
        assert "RequestError" in error_msg
        assert "🐕💥" in error_msg
        assert "squirrel" in error_msg.lower()  # Chaotic error message!


@pytest.mark.asyncio
async def test_analyze_image_timeout_error():
    """analyze_image handles timeout gracefully."""
    with patch(
        "discord_puppy.vision.vision_tools.process_discord_image"
    ) as mock_process:
        mock_process.side_effect = httpx.TimeoutException("Request timed out")

        result = await analyze_image("https://cdn.discordapp.com/slow.png")

        assert isinstance(result, list)
        assert len(result) == 1
        assert "TimeoutException" in result[0]
        assert "🐕💥" in result[0]


# =============================================================================
# Test analyze_attachment()
# =============================================================================


@pytest.mark.asyncio
async def test_analyze_attachment_happy_path(sample_png_bytes):
    """analyze_attachment returns ToolReturn with BinaryContent for valid bytes."""
    result = await analyze_attachment(sample_png_bytes, "cute_dog.png")

    # Should return a list (ToolReturn)
    assert isinstance(result, list)
    assert len(result) == 2

    # First element contains the filename
    assert "cute_dog.png" in result[0]
    assert "🐕" in result[0]

    # Second element is BinaryContent
    assert isinstance(result[1], BinaryContent)
    # PNG without alpha gets converted to JPEG for efficiency
    assert result[1].media_type in ["image/jpeg", "image/png"]


@pytest.mark.asyncio
async def test_analyze_attachment_with_jpeg(sample_jpeg_bytes):
    """analyze_attachment handles JPEG input correctly."""
    result = await analyze_attachment(sample_jpeg_bytes, "photo.jpg")

    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[1], BinaryContent)
    assert result[1].media_type == "image/jpeg"


@pytest.mark.asyncio
async def test_analyze_attachment_invalid_bytes():
    """analyze_attachment returns error for invalid image bytes."""
    invalid_bytes = b"this is not an image at all!"

    result = await analyze_attachment(invalid_bytes, "fake_image.png")

    # Should return error list
    assert isinstance(result, list)
    assert len(result) == 1

    # Should contain error info
    error_msg = result[0]
    assert "🐕💔" in error_msg
    assert "fake_image.png" in error_msg


@pytest.mark.asyncio
async def test_analyze_attachment_empty_bytes():
    """analyze_attachment handles empty bytes gracefully."""
    result = await analyze_attachment(b"", "empty.png")

    assert isinstance(result, list)
    assert len(result) == 1
    assert "🐕💔" in result[0]


# =============================================================================
# Test what_do_i_see()
# =============================================================================


@pytest.mark.asyncio
async def test_what_do_i_see_happy_path(mock_binary_content):
    """what_do_i_see returns question + BinaryContent on success."""
    with patch(
        "discord_puppy.vision.vision_tools.process_discord_image"
    ) as mock_process:
        mock_process.return_value = mock_binary_content

        result = await what_do_i_see(
            "https://cdn.discordapp.com/meme.png",
            "Is there a squirrel in this image?"
        )

        # Should return a list (ToolReturn)
        assert isinstance(result, list)
        assert len(result) == 2

        # First element contains the question
        text_content = result[0]
        assert "Is there a squirrel in this image?" in text_content
        assert "The human asks" in text_content
        assert "detective" in text_content.lower()

        # Second element is BinaryContent
        assert isinstance(result[1], BinaryContent)


@pytest.mark.asyncio
async def test_what_do_i_see_includes_question_in_response(mock_binary_content):
    """what_do_i_see properly includes the user's question."""
    with patch(
        "discord_puppy.vision.vision_tools.process_discord_image"
    ) as mock_process:
        mock_process.return_value = mock_binary_content

        question = "How many dogs are in this picture?"
        result = await what_do_i_see("https://example.com/dogs.jpg", question)

        # The question should be in the text part
        assert question in result[0]


@pytest.mark.asyncio
async def test_what_do_i_see_network_error():
    """what_do_i_see returns error with question context on failure."""
    with patch(
        "discord_puppy.vision.vision_tools.process_discord_image"
    ) as mock_process:
        mock_process.side_effect = httpx.RequestError("Network down")

        question = "What breed is this dog?"
        result = await what_do_i_see(
            "https://cdn.discordapp.com/unreachable.png",
            question
        )

        # Should return error list
        assert isinstance(result, list)
        assert len(result) == 1

        # Error should reference the question
        error_msg = result[0]
        assert "🐕❌" in error_msg
        assert question in error_msg
        assert "RequestError" in error_msg


@pytest.mark.asyncio
async def test_what_do_i_see_bad_url():
    """what_do_i_see handles invalid URLs gracefully."""
    with patch(
        "discord_puppy.vision.vision_tools.process_discord_image"
    ) as mock_process:
        mock_process.side_effect = httpx.HTTPStatusError(
            "404 Not Found",
            request=MagicMock(),
            response=MagicMock(status_code=404)
        )

        result = await what_do_i_see(
            "https://cdn.discordapp.com/deleted.png",
            "What's in this image?"
        )

        assert isinstance(result, list)
        assert len(result) == 1
        assert "🐕❌" in result[0]


# =============================================================================
# Test Docstrings (because they're chaotic and important!)
# =============================================================================


def test_analyze_image_has_chaotic_docstring():
    """analyze_image has the required chaotic docstring."""
    docstring = analyze_image.__doc__
    assert docstring is not None
    assert "squirrel" in docstring.lower()
    assert "🐿️" in docstring


def test_analyze_attachment_has_chaotic_docstring():
    """analyze_attachment has the required chaotic docstring."""
    docstring = analyze_attachment.__doc__
    assert docstring is not None
    assert "dog" in docstring.lower()
    assert "cat" in docstring.lower()
    assert "suspicious" in docstring.lower()


def test_what_do_i_see_has_chaotic_docstring():
    """what_do_i_see has the required chaotic docstring."""
    docstring = what_do_i_see.__doc__
    assert docstring is not None
    assert "warning" in docstring.lower()
    assert "🐕" in docstring
