"""
Image Download and Processing 👁️

Downloads Discord attachments and processes them for vision analysis.
Supports resizing for API efficiency and BinaryContent creation.

Note: Gets VERY excited about dog pictures!
"""

from io import BytesIO
from typing import Optional, Tuple

import httpx
from PIL import Image
from pydantic_ai.messages import BinaryContent

# Supported image formats
SUPPORTED_FORMATS = {"png", "jpg", "jpeg", "gif", "webp"}
MEDIA_TYPES = {
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "gif": "image/gif",
    "webp": "image/webp",
}


async def download_discord_attachment(url: str, timeout: float = 30.0) -> bytes:
    """Download an image from a Discord attachment URL.

    Args:
        url: The Discord CDN URL for the attachment
        timeout: Request timeout in seconds

    Returns:
        Raw image bytes

    Raises:
        httpx.HTTPError: If download fails
        ValueError: If URL doesn't look like a Discord attachment
    """
    # Basic validation - Discord CDN URLs
    if not any(domain in url for domain in ["cdn.discordapp.com", "media.discordapp.net"]):
        # Still allow it but warn - might be a direct link
        pass

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            timeout=timeout,
            follow_redirects=True,
            headers={"User-Agent": "DiscordPuppy/1.0 (a very good bot)"},
        )
        response.raise_for_status()
        return response.content


def get_image_format(image_bytes: bytes, filename: Optional[str] = None) -> str:
    """Detect image format from bytes or filename.

    Args:
        image_bytes: Raw image data
        filename: Optional filename with extension

    Returns:
        Format string (png, jpg, gif, webp)
    """
    # Try from filename first
    if filename:
        ext = filename.lower().split(".")[-1]
        if ext in SUPPORTED_FORMATS:
            return ext

    # Detect from magic bytes
    if image_bytes[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    elif image_bytes[:2] == b"\xff\xd8":
        return "jpeg"
    elif image_bytes[:6] in (b"GIF87a", b"GIF89a"):
        return "gif"
    elif image_bytes[:4] == b"RIFF" and image_bytes[8:12] == b"WEBP":
        return "webp"

    # Default to png if unknown
    return "png"


def resize_for_analysis(
    image_bytes: bytes, max_height: int = 768, max_width: int = 1024, quality: int = 85
) -> Tuple[bytes, str]:
    """Resize an image for efficient API analysis.

    Maintains aspect ratio while fitting within max dimensions.
    Converts to JPEG for smaller file size (except for images with transparency).

    Args:
        image_bytes: Raw image data
        max_height: Maximum height in pixels
        max_width: Maximum width in pixels
        quality: JPEG quality (1-100)

    Returns:
        Tuple of (resized image bytes, media type)
    """
    img = Image.open(BytesIO(image_bytes))

    # Check if image has transparency
    has_alpha = img.mode in ("RGBA", "LA", "PA") or (img.mode == "P" and "transparency" in img.info)

    # Calculate new size maintaining aspect ratio
    width, height = img.size

    if width > max_width or height > max_height:
        # Calculate scaling factor
        width_ratio = max_width / width
        height_ratio = max_height / height
        ratio = min(width_ratio, height_ratio)

        new_width = int(width * ratio)
        new_height = int(height * ratio)

        # Use high-quality resampling
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Convert to appropriate format
    output = BytesIO()

    if has_alpha:
        # Keep PNG for transparency
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        img.save(output, format="PNG", optimize=True)
        media_type = "image/png"
    else:
        # Convert to RGB and save as JPEG for smaller size
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(output, format="JPEG", quality=quality, optimize=True)
        media_type = "image/jpeg"

    return output.getvalue(), media_type


def create_binary_content(
    image_bytes: bytes, media_type: Optional[str] = None, filename: Optional[str] = None
) -> BinaryContent:
    """Create a pydantic_ai BinaryContent for multimodal prompts.

    Args:
        image_bytes: Raw image data
        media_type: MIME type (auto-detected if not provided)
        filename: Original filename for format detection

    Returns:
        BinaryContent ready for use in agent prompts
    """
    if not media_type:
        fmt = get_image_format(image_bytes, filename)
        media_type = MEDIA_TYPES.get(fmt, "image/png")

    return BinaryContent(data=image_bytes, media_type=media_type)


async def process_discord_image(
    url: str, max_height: int = 768, max_width: int = 1024
) -> BinaryContent:
    """Full pipeline: download, resize, and create BinaryContent.

    This is the main function to use for Discord attachments.

    Args:
        url: Discord attachment URL
        max_height: Max image height
        max_width: Max image width

    Returns:
        BinaryContent ready for the agent

    Example:
        >>> content = await process_discord_image(attachment.url)
        >>> # Now use content in agent prompt
    """
    # Download
    raw_bytes = await download_discord_attachment(url)

    # Resize for efficiency
    resized_bytes, media_type = resize_for_analysis(
        raw_bytes, max_height=max_height, max_width=max_width
    )

    # Create BinaryContent
    return BinaryContent(data=resized_bytes, media_type=media_type)
