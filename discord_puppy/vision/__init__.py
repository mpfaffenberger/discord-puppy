"""
Vision subsystem - The eyes that see all memes! 👁️

Modules:
- image_analyzer.py: Download and process Discord attachments
- vision_tools.py: LLM-callable tools for image analysis

Note: Gets VERY excited about dog pictures.
      Suspicious of cat pictures.
"""

from .image_analyzer import (
    MEDIA_TYPES,
    SUPPORTED_FORMATS,
    create_binary_content,
    download_discord_attachment,
    get_image_format,
    process_discord_image,
    resize_for_analysis,
)
from .vision_tools import (
    VISION_TOOLS,
    analyze_attachment,
    analyze_image,
    what_do_i_see,
)

__all__ = [
    # Image analyzer
    "SUPPORTED_FORMATS",
    "MEDIA_TYPES",
    "download_discord_attachment",
    "get_image_format",
    "resize_for_analysis",
    "create_binary_content",
    "process_discord_image",
    # Vision tools
    "analyze_image",
    "analyze_attachment",
    "what_do_i_see",
    "VISION_TOOLS",
]
