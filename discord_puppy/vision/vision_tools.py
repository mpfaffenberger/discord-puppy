"""Vision Tools for Discord Puppy - I CAN SEE! 👁️🐕

These tools let the puppy actually LOOK at images!
Warning: May get extremely excited about dog pictures.
May become suspicious at cat pictures.
Will definitely chase any squirrels. 🐿️

Uses pydantic-ai's ToolReturn pattern with BinaryContent
so the LLM can actually SEE the images, not just read about them.
"""

from pydantic_ai.messages import ToolReturn

from .image_analyzer import (
    create_binary_content,
    process_discord_image,
    resize_for_analysis,
)


async def analyze_image(image_url: str) -> ToolReturn:
    """Look at an image! I might get distracted by pictures of squirrels. 🐿️

    Downloads an image from a URL and returns it so I can ACTUALLY SEE IT
    with my puppy eyes! This is incredible technology! I love the future!

    WARNING: If the image contains:
    - Dogs: I WILL lose my mind with excitement 🐕
    - Cats: *suspicious squinting* 🐱
    - Squirrels: SQUIRREL SQUIRREL SQUIR— *crashes*
    - Food: Is that for me? It should be for me.

    Args:
        image_url: URL of the image to analyze. Can be Discord CDN or any
            accessible image URL. I'm not picky, I'll look at anything!

    Returns:
        ToolReturn containing BinaryContent of the image for LLM vision.
        Like giving the LLM actual eyeballs! Science! 🔬
    """
    try:
        # Use the full pipeline - download, resize, create BinaryContent
        binary_content = await process_discord_image(image_url)

        return [
            "🐕👁️ *stares at image with great intensity* I CAN SEE IT!",
            binary_content,
        ]

    except Exception as e:
        # Even when things break, stay in character!
        return [
            f"🐕💥 Uh oh! My eyeballs encountered an error: {type(e).__name__}: {e}\n"
            "*bonks head against screen* The image won't load! "
            "Maybe it ran away like a squirrel? 🐿️"
        ]


async def analyze_attachment(attachment_bytes: bytes, filename: str) -> ToolReturn:
    """If it's a dog, I will be VERY excited. If it's a cat... suspicious. 🐱

    Processes raw image bytes (like from a Discord attachment) and prepares
    them for my eager puppy vision! No URL needed, just pure image data!

    Perfect for when Discord gives us the bytes directly. Less fetching
    required! ...wait, fetching is one of my favorite activities. Hmm.

    Args:
        attachment_bytes: Raw bytes of the image. Yummy delicious image bytes!
            (I don't actually eat them, I just look at them. Mostly.)
        filename: The original filename, helps me understand what format
            this mysterious byte soup is supposed to be. Like "cute_dog.png"
            or "definitely_not_a_cat.jpg" (suspicious...)

    Returns:
        ToolReturn with BinaryContent ready for LLM vision analysis.
        My brain will then tell you EXACTLY what I think about this image.
        Whether you asked or not. 🐕
    """
    try:
        # Resize for efficiency (we're good doggos who don't waste tokens)
        resized_bytes, media_type = resize_for_analysis(attachment_bytes)

        # Create the BinaryContent for vision
        binary_content = create_binary_content(
            resized_bytes, media_type=media_type, filename=filename
        )

        return [
            f"🐕👁️ *inspects {filename} with laser focus* Processing... processing...",
            binary_content,
        ]

    except Exception as e:
        return [
            f"🐕💔 Oh no! Couldn't process the attachment: {type(e).__name__}: {e}\n"
            f"The file '{filename}' is being difficult! "
            "*paws at screen helplessly* Is it corrupted? Is it shy? "
            "Does it not like dogs?! 😢"
        ]


async def what_do_i_see(image_url: str, question: str) -> ToolReturn:
    """Warning: I may answer questions you didn't ask. 🐕

    Look at an image AND consider a specific question about it!
    This is like analyze_image but with CONTEXT! I'm a sophisticated
    puppy who can answer questions! Sometimes even the right ones!

    I will:
    1. Look at the image (EXCITING!)
    2. Read your question (hmm, interesting...)
    3. Provide my professional puppy opinion (unsolicited advice included free!)

    Disclaimer: My answers may include:
    - Dog-related tangents (unavoidable)
    - Snack ratings if food is visible (my expertise)
    - Suspicious commentary on cats (they know what they did)
    - Random barking at nothing (sometimes the vibes are just wrong)

    Args:
        image_url: URL of the image to examine with my detective eyes 🔍
        question: What you want to know about the image. I'll try to answer
            this, but I make no promises about staying on topic.

    Returns:
        ToolReturn containing the image and your question bundled together.
        The LLM will see both and hopefully answer correctly!
        Or get distracted by a squirrel in the background. Either way. 🐿️
    """
    try:
        # Download and process the image
        binary_content = await process_discord_image(image_url)

        return [
            f"🐕🔍 *puts on tiny detective glasses*\n\n"
            f"**The human asks:** {question}\n\n"
            "*examines image with great seriousness* Hmm yes, interesting...",
            binary_content,
        ]

    except Exception as e:
        return [
            f"🐕❌ My vision quest has failed: {type(e).__name__}: {e}\n"
            f"I really wanted to answer '{question}' but the image won't cooperate!\n"
            "*whimpers* Maybe try a different URL? Or bribe me with treats "
            "and I'll try harder! 🦴"
        ]


# =============================================================================
# Export tools for pydantic-ai registration
# =============================================================================

VISION_TOOLS = [
    analyze_image,
    analyze_attachment,
    what_do_i_see,
]

__all__ = [
    "analyze_image",
    "analyze_attachment",
    "what_do_i_see",
    "VISION_TOOLS",
]
