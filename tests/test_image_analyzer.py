"""
Tests for vision/image_analyzer.py 👁️

Tests image download, resizing, and BinaryContent creation.
"""

import pytest
from io import BytesIO
from unittest.mock import AsyncMock, patch, MagicMock
from PIL import Image

from discord_puppy.vision.image_analyzer import (
    SUPPORTED_FORMATS,
    MEDIA_TYPES,
    download_discord_attachment,
    get_image_format,
    resize_for_analysis,
    create_binary_content,
    process_discord_image,
)


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def sample_png_bytes():
    """Create a small PNG image for testing."""
    img = Image.new('RGB', (100, 100), color='red')
    output = BytesIO()
    img.save(output, format='PNG')
    return output.getvalue()


@pytest.fixture
def sample_jpeg_bytes():
    """Create a small JPEG image for testing."""
    img = Image.new('RGB', (100, 100), color='blue')
    output = BytesIO()
    img.save(output, format='JPEG')
    return output.getvalue()


@pytest.fixture
def sample_rgba_png_bytes():
    """Create a PNG with transparency."""
    img = Image.new('RGBA', (100, 100), color=(255, 0, 0, 128))
    output = BytesIO()
    img.save(output, format='PNG')
    return output.getvalue()


@pytest.fixture
def large_image_bytes():
    """Create a large image that needs resizing."""
    img = Image.new('RGB', (2000, 1500), color='green')
    output = BytesIO()
    img.save(output, format='PNG')
    return output.getvalue()


# =============================================================================
# Test Constants
# =============================================================================

def test_supported_formats():
    """SUPPORTED_FORMATS contains expected image types."""
    assert "png" in SUPPORTED_FORMATS
    assert "jpg" in SUPPORTED_FORMATS
    assert "jpeg" in SUPPORTED_FORMATS
    assert "gif" in SUPPORTED_FORMATS
    assert "webp" in SUPPORTED_FORMATS


def test_media_types():
    """MEDIA_TYPES maps formats to MIME types."""
    assert MEDIA_TYPES["png"] == "image/png"
    assert MEDIA_TYPES["jpg"] == "image/jpeg"
    assert MEDIA_TYPES["jpeg"] == "image/jpeg"
    assert MEDIA_TYPES["gif"] == "image/gif"
    assert MEDIA_TYPES["webp"] == "image/webp"


# =============================================================================
# Test get_image_format
# =============================================================================

def test_get_image_format_from_filename():
    """Detects format from filename extension."""
    assert get_image_format(b"", filename="photo.png") == "png"
    assert get_image_format(b"", filename="photo.jpg") == "jpg"
    assert get_image_format(b"", filename="photo.JPEG") == "jpeg"
    assert get_image_format(b"", filename="animation.gif") == "gif"
    assert get_image_format(b"", filename="modern.webp") == "webp"


def test_get_image_format_from_png_magic_bytes(sample_png_bytes):
    """Detects PNG from magic bytes."""
    assert get_image_format(sample_png_bytes) == "png"


def test_get_image_format_from_jpeg_magic_bytes(sample_jpeg_bytes):
    """Detects JPEG from magic bytes."""
    assert get_image_format(sample_jpeg_bytes) == "jpeg"


def test_get_image_format_defaults_to_png():
    """Unknown format defaults to PNG."""
    assert get_image_format(b"unknown data") == "png"


# =============================================================================
# Test resize_for_analysis
# =============================================================================

def test_resize_small_image_unchanged(sample_png_bytes):
    """Small images don't get resized (but may be re-encoded)."""
    result_bytes, media_type = resize_for_analysis(sample_png_bytes)
    
    # Check we got valid output
    result_img = Image.open(BytesIO(result_bytes))
    # Original was 100x100, should be unchanged or close
    assert result_img.size[0] <= 100
    assert result_img.size[1] <= 100


def test_resize_large_image(large_image_bytes):
    """Large images get resized to fit within max dimensions."""
    result_bytes, media_type = resize_for_analysis(
        large_image_bytes, 
        max_height=768, 
        max_width=1024
    )
    
    result_img = Image.open(BytesIO(result_bytes))
    width, height = result_img.size
    
    # Should fit within max dimensions
    assert width <= 1024
    assert height <= 768


def test_resize_maintains_aspect_ratio(large_image_bytes):
    """Resizing maintains original aspect ratio."""
    # Original is 2000x1500 = 4:3 ratio
    original_ratio = 2000 / 1500
    
    result_bytes, media_type = resize_for_analysis(
        large_image_bytes,
        max_height=768,
        max_width=1024
    )
    
    result_img = Image.open(BytesIO(result_bytes))
    width, height = result_img.size
    result_ratio = width / height
    
    # Aspect ratio should be preserved (with small tolerance for rounding)
    assert abs(original_ratio - result_ratio) < 0.02


def test_resize_preserves_transparency(sample_rgba_png_bytes):
    """Transparent images stay as PNG."""
    result_bytes, media_type = resize_for_analysis(sample_rgba_png_bytes)
    
    assert media_type == "image/png"
    # Verify it's a valid PNG
    result_img = Image.open(BytesIO(result_bytes))
    assert result_img.mode == "RGBA"


def test_resize_converts_opaque_to_jpeg(sample_png_bytes):
    """Opaque images get converted to JPEG for smaller size."""
    result_bytes, media_type = resize_for_analysis(sample_png_bytes)
    
    assert media_type == "image/jpeg"


# =============================================================================
# Test create_binary_content
# =============================================================================

def test_create_binary_content_with_explicit_type(sample_png_bytes):
    """Creates BinaryContent with explicit media type."""
    content = create_binary_content(
        sample_png_bytes, 
        media_type="image/png"
    )
    
    assert content.data == sample_png_bytes
    assert content.media_type == "image/png"


def test_create_binary_content_auto_detect(sample_jpeg_bytes):
    """Auto-detects media type from bytes."""
    content = create_binary_content(sample_jpeg_bytes)
    
    assert content.data == sample_jpeg_bytes
    assert content.media_type == "image/jpeg"


def test_create_binary_content_from_filename(sample_png_bytes):
    """Uses filename for format detection."""
    content = create_binary_content(
        sample_png_bytes, 
        filename="image.png"
    )
    
    assert content.media_type == "image/png"


# =============================================================================
# Test download_discord_attachment
# =============================================================================

@pytest.mark.asyncio
async def test_download_discord_attachment_success(sample_png_bytes):
    """Successfully downloads from Discord CDN."""
    mock_response = MagicMock()
    mock_response.content = sample_png_bytes
    mock_response.raise_for_status = MagicMock()
    
    with patch('discord_puppy.vision.image_analyzer.httpx.AsyncClient') as mock_client:
        mock_instance = AsyncMock()
        mock_instance.get.return_value = mock_response
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.__aexit__.return_value = None
        mock_client.return_value = mock_instance
        
        result = await download_discord_attachment(
            "https://cdn.discordapp.com/attachments/123/456/image.png"
        )
        
        assert result == sample_png_bytes
        mock_instance.get.assert_called_once()


# =============================================================================
# Test process_discord_image (integration)
# =============================================================================

@pytest.mark.asyncio
async def test_process_discord_image_full_pipeline(large_image_bytes):
    """Full pipeline: download, resize, create content."""
    mock_response = MagicMock()
    mock_response.content = large_image_bytes
    mock_response.raise_for_status = MagicMock()
    
    with patch('discord_puppy.vision.image_analyzer.httpx.AsyncClient') as mock_client:
        mock_instance = AsyncMock()
        mock_instance.get.return_value = mock_response
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.__aexit__.return_value = None
        mock_client.return_value = mock_instance
        
        result = await process_discord_image(
            "https://cdn.discordapp.com/attachments/123/456/large.png",
            max_height=768,
            max_width=1024
        )
        
        # Should return BinaryContent
        assert hasattr(result, 'data')
        assert hasattr(result, 'media_type')
        
        # Should be resized
        result_img = Image.open(BytesIO(result.data))
        assert result_img.size[0] <= 1024
        assert result_img.size[1] <= 768
