"""Discord Puppy Bot - The Main Orchestrator! 🐕✨

This is where ALL the chaos comes together:
- Discord client handling messages
- Agent integration for intelligent responses
- Memory for remembering humans
- Vision for seeing images
- Personality engine for chaotic decisions
- Spontaneous outbursts via chaos_loop

Bring it all together. Maximum chaos. Professional chaos.
"""

import asyncio
import logging
import random
from datetime import datetime
from typing import Any

import discord

from discord_puppy.agents import DiscordPuppyAgent
from discord_puppy.config import Settings, get_settings
from discord_puppy.memory import (
    get_user_summary,
    init_database,
    recall_user,
    record_interaction,
)
from discord_puppy.personality import (
    Mood,
    get_mood_modifier,
    get_random_mood,
    random_outburst,
    should_react_with_emoji,
    should_respond,
)
from discord_puppy.vision import process_discord_image

logger = logging.getLogger(__name__)


# ============================================================================
# THE MAIN EVENT: DISCORD PUPPY BOT 🐕
# ============================================================================


class DiscordPuppy(discord.Client):
    """The main Discord bot that brings ALL the chaos together!

    This client handles:
    - Message events (deciding whether to respond)
    - Image processing with vision
    - Memory retrieval and injection
    - Spontaneous chaos via the chaos_loop
    - Emoji reactions for extra personality

    Example:
        ```python
        from discord_puppy.bot import DiscordPuppy
        from discord_puppy.config import get_settings

        settings = get_settings()
        puppy = DiscordPuppy(settings)
        puppy.run(settings.DISCORD_TOKEN)
        ```
    """

    def __init__(self, settings: Settings | None = None) -> None:
        """Initialize the Discord Puppy!

        Args:
            settings: Configuration settings. If None, loads from environment.
        """
        # Set up intents - we need messages, message content, and guilds!
        intents = discord.Intents.default()
        intents.message_content = True  # We need to read messages!
        intents.guilds = True  # We need guild info!
        intents.members = True  # We want to know about members!

        super().__init__(intents=intents)

        # Configuration
        self.settings = settings or get_settings()

        # The brain! 🧠
        self.agent = DiscordPuppyAgent()

        # Track startup time for diary entries
        self.start_time = datetime.now()
        self.day_count = 1  # For diary continuity

        # Current mood (changes periodically)
        self.current_mood: Mood = get_random_mood()
        self.mood_changed_at = datetime.now()

        # Track known users for chaos_loop outbursts
        self._known_users: dict[str, int] = {}  # username -> trust_level

        # Chaos channel (set in on_ready if configured)
        self._chaos_channel_id: int | None = None

        logger.info("🐕 Discord Puppy initialized! Ready to bring chaos!")

    # ========================================================================
    # DISCORD EVENTS
    # ========================================================================

    async def on_ready(self) -> None:
        """Called when the bot successfully connects to Discord!

        - Initializes the database
        - Prints a fun startup message
        - Starts the chaos_loop background task
        """
        logger.info(f"🐕 Logged in as {self.user} (ID: {self.user.id if self.user else 'unknown'})")

        # Initialize the brain! 🧠
        try:
            init_database(self.settings.DATABASE_PATH)
            logger.info(f"📚 Database initialized at {self.settings.DATABASE_PATH}")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            # Continue anyway - we can still function with degraded memory

        # Print fun startup message! ✨
        startup_messages = [
            "🐕 HELLO WORLD! Discord Puppy is ONLINE and ready to cause chaos! *wags tail aggressively*",
            "🐕 *bursts through digital door* I'M HERE! THE GOOD BOY HAS ARRIVED!",
            "🐕 Discord Puppy v1.0 activated! Warning: May contain excessive tail wagging.",
            "🐕 *boots up* Running chaos.exe... SUCCESS! All systems nominal! Bark bark!",
            "🐕 I HAVE AWAKENED! *knocks over metaphorical plant* Time to be helpful! Probably!",
        ]
        logger.info(random.choice(startup_messages))

        # Log guild membership
        guild_count = len(self.guilds)
        logger.info(f"🏠 Connected to {guild_count} guild(s)!")
        for guild in self.guilds:
            logger.info(f"   - {guild.name} (ID: {guild.id})")

        # Start the chaos loop! 🌪️
        self.loop.create_task(self.chaos_loop())
        logger.info("🌀 Chaos loop started! Spontaneous outbursts enabled!")

    async def on_message(self, message: discord.Message) -> None:
        """Handle incoming messages!

        This is where the magic happens:
        1. Skip our own messages
        2. Fetch user memory
        3. Check for images
        4. Decide if we should respond
        5. Build context and run agent
        6. Send response or maybe react

        Args:
            message: The Discord message to process.
        """
        # Skip our own messages - don't respond to yourself, that's weird!
        if message.author == self.user:
            return

        # Skip bot messages (other bots talking)
        if message.author.bot:
            logger.debug(f"Skipping bot message from {message.author}")
            return

        user_id = str(message.author.id)
        username = message.author.display_name

        logger.debug(f"📨 Message from {username} ({user_id}): {message.content[:100]}...")

        # Update mood occasionally (every 10-30 minutes)
        await self._maybe_change_mood()

        # Fetch user notes from memory! 🧠
        user_context = await self._build_user_context(user_id, username)
        user_trust = user_context.get("trust_level", 5)

        # Track this user for chaos_loop
        self._known_users[username] = user_trust

        # Check for image attachments 📸
        image_content = await self._process_image_attachments(message)
        has_image = image_content is not None

        # Is this a DM?
        is_dm = isinstance(message.channel, discord.DMChannel)

        # Were we mentioned?
        is_mentioned = self.user in message.mentions if self.user else False

        # SHOULD WE RESPOND? 🤔
        respond, reason = should_respond(
            message_content=message.content,
            is_mentioned=is_mentioned,
            is_dm=is_dm,
            response_chance=self.settings.RESPONSE_CHANCE,
            user_trust_level=user_trust,
        )

        logger.debug(f"Response decision: {respond} - {reason}")

        if respond:
            # WE'RE RESPONDING! 🎉
            await self._send_response(message, user_context, image_content, has_image)
        else:
            # Not responding, but maybe react with emoji?
            should_react, emoji = should_react_with_emoji()
            if should_react and emoji:
                try:
                    await message.add_reaction(emoji)
                    logger.debug(f"Reacted with {emoji} instead of responding")
                except discord.errors.Forbidden:
                    logger.debug("Can't add reactions in this channel")
                except Exception as e:
                    logger.warning(f"Failed to add reaction: {e}")

    async def _send_response(
        self,
        message: discord.Message,
        user_context: dict[str, Any],
        image_content: Any | None,
        has_image: bool,
    ) -> None:
        """Build and send a response to the message.

        Args:
            message: The original Discord message.
            user_context: User memory context to inject.
            image_content: Optional BinaryContent from image attachment.
            has_image: Whether an image was attached.
        """
        user_id = str(message.author.id)
        username = message.author.display_name

        try:
            # Show typing indicator while we think... 🤔
            async with message.channel.typing():
                # Build the full message with context
                mood_modifier = get_mood_modifier(self.current_mood)

                # Construct the prompt
                prompt_parts = []

                # Add mood context
                prompt_parts.append(mood_modifier)
                prompt_parts.append("")  # Blank line

                # Add user context
                if user_context:
                    context_str = self._format_user_context_for_prompt(user_context)
                    prompt_parts.append(context_str)
                    prompt_parts.append("")  # Blank line

                # Add image notification
                if has_image:
                    prompt_parts.append("📸 **An image was attached to this message!**")
                    prompt_parts.append("Use your vision to analyze it if relevant!")
                    prompt_parts.append("")  # Blank line

                # Add the actual message
                prompt_parts.append(f"**{username} says:** {message.content}")

                full_prompt = "\n".join(prompt_parts)

                # Run the agent! 🧠
                # TODO: When pydantic-ai supports images, include image_content
                result = await self.agent.run(
                    user_message=full_prompt,
                    user_id=user_id,
                    user_context=user_context,
                )

                response_text = str(result.data) if result.data else "*confused puppy noises*"

            # Send the response!
            # Discord has a 2000 character limit, so chunk if needed
            await self._send_chunked(message.channel, response_text)

            # Record this interaction in memory! 📝
            try:
                record_interaction(
                    user_id=user_id,
                    interaction_type="message",
                    summary=f"Responded to: {message.content[:100]}...",
                    db_path=self.settings.DATABASE_PATH,
                )
            except Exception as e:
                logger.warning(f"Failed to record interaction: {e}")

            logger.info(f"✅ Responded to {username}: {response_text[:100]}...")

        except Exception as e:
            logger.error(f"Failed to generate response: {e}", exc_info=True)
            # Send a fallback response
            fallbacks = [
                "*confused puppy head tilt* Something went wrong in my brain! 🐕💥",
                "Woof! My thoughts got tangled up like a leash! Try again? 🌀",
                "*error bork* I got distracted by a squirrel mid-thought! 🐿️",
                "My brain did a heckin' confuse! Could you repeat that? 🤔",
            ]
            try:
                await message.channel.send(random.choice(fallbacks))
            except Exception as send_error:
                logger.error(f"Failed to send fallback: {send_error}")

    async def _send_chunked(
        self,
        channel: discord.abc.Messageable,
        text: str,
        max_length: int = 2000,
    ) -> None:
        """Send a message, chunking if it exceeds Discord's limit.

        Args:
            channel: The channel to send to.
            text: The full message text.
            max_length: Maximum message length (Discord's limit is 2000).
        """
        if len(text) <= max_length:
            await channel.send(text)
            return

        # Chunk the message
        chunks = []
        current_chunk = ""

        for line in text.split("\n"):
            if len(current_chunk) + len(line) + 1 > max_length:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = line
            else:
                current_chunk = current_chunk + "\n" + line if current_chunk else line

        if current_chunk:
            chunks.append(current_chunk)

        # Send chunks with a small delay
        for i, chunk in enumerate(chunks):
            await channel.send(chunk)
            if i < len(chunks) - 1:
                await asyncio.sleep(0.5)  # Small delay between chunks

    # ========================================================================
    # CHAOS LOOP - Spontaneous Outbursts! 🌪️
    # ========================================================================

    async def chaos_loop(self) -> None:
        """The chaos loop! Sends random spontaneous messages periodically.

        This runs in the background and:
        - Sleeps for a random interval (60-300 seconds)
        - Generates a random outburst
        - Maybe references a known user
        - Sends to an appropriate channel
        """
        await self.wait_until_ready()

        logger.info("🌀 Chaos loop is running! *rubs paws together mischievously*")

        while not self.is_closed():
            try:
                # Sleep for random interval
                sleep_time = random.randint(
                    self.settings.SPONTANEOUS_MIN_SECONDS,
                    self.settings.SPONTANEOUS_MAX_SECONDS,
                )
                logger.debug(f"Chaos loop sleeping for {sleep_time} seconds...")
                await asyncio.sleep(sleep_time)

                # Check if we're still connected
                if self.is_closed():
                    break

                # Find a channel to send to
                channel = await self._get_chaos_channel()
                if not channel:
                    logger.debug("No suitable channel for chaos outburst")
                    continue

                # Generate the outburst!
                usernames = list(self._known_users.keys()) if self._known_users else None

                outburst = random_outburst(
                    usernames=usernames,
                    trust_levels=self._known_users if self._known_users else None,
                    day_count=self.day_count,
                )

                # Send it!
                await channel.send(outburst)
                logger.info(f"🌀 Spontaneous outburst sent: {outburst[:100]}...")

                # Increment day count occasionally
                if random.random() < 0.1:
                    self.day_count += 1

            except asyncio.CancelledError:
                logger.info("Chaos loop cancelled, shutting down...")
                break
            except Exception as e:
                logger.error(f"Error in chaos loop: {e}", exc_info=True)
                # Continue the loop even if one iteration fails
                await asyncio.sleep(60)

    async def _get_chaos_channel(self) -> discord.TextChannel | None:
        """Find a suitable channel for spontaneous outbursts.

        Priority:
        1. Configured chaos channel
        2. A general/chat channel
        3. Any text channel we can send to

        Returns:
            A text channel or None if no suitable channel found.
        """
        # If we have guilds, find a suitable channel
        for guild in self.guilds:
            # Try to find common channel names
            preferred_names = ["general", "chat", "bot", "puppy", "random", "off-topic"]

            for name in preferred_names:
                for channel in guild.text_channels:
                    if name in channel.name.lower():
                        # Check if we can send messages
                        if channel.permissions_for(guild.me).send_messages:
                            return channel

            # Fall back to any channel we can send to
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    return channel

        return None

    # ========================================================================
    # HELPER METHODS
    # ========================================================================

    async def _build_user_context(
        self,
        user_id: str,
        username: str,
    ) -> dict[str, Any]:
        """Build context dictionary from user memory.

        Args:
            user_id: Discord user ID.
            username: Display name.

        Returns:
            Dictionary with user context for prompt injection.
        """
        context = {
            "user_id": user_id,
            "username": username,
        }

        try:
            # Try to get user summary from memory
            summary = get_user_summary(user_id, db_path=self.settings.DATABASE_PATH)

            if summary:
                # Parse the summary for structured data
                context["notes"] = summary
                context["trust_level"] = 5  # Default, would parse from summary

                # Try to get more detailed notes
                user_notes_result = recall_user(
                    user_id=user_id,
                    db_path=self.settings.DATABASE_PATH,
                )

                if user_notes_result and "not found" not in user_notes_result.lower():
                    # We have detailed notes!
                    context["detailed_notes"] = user_notes_result

                    # Try to extract trust level from notes
                    if "Trust:" in user_notes_result:
                        try:
                            trust_part = user_notes_result.split("Trust:")[1].split()[0]
                            context["trust_level"] = int(trust_part.split("/")[0])
                        except (IndexError, ValueError):
                            pass

        except Exception as e:
            logger.warning(f"Failed to fetch user context: {e}")
            # Continue with minimal context

        return context

    def _format_user_context_for_prompt(self, context: dict[str, Any]) -> str:
        """Format user context for prompt injection.

        Args:
            context: User context dictionary.

        Returns:
            Formatted string for prompt.
        """
        parts = ["## 📋 Current User Context\n"]

        if context.get("username"):
            parts.append(f"**User:** {context['username']}")
        if context.get("user_id"):
            parts.append(f"**User ID:** {context['user_id']}")
        if context.get("trust_level") is not None:
            trust = context["trust_level"]
            balls = "🎾" * trust
            parts.append(f"**Trust level:** {trust}/10 {balls}")
        if context.get("notes"):
            parts.append(f"**Quick summary:** {context['notes']}")
        if context.get("detailed_notes"):
            parts.append(f"\n**Your detailed notes on them:**\n{context['detailed_notes']}")

        parts.append("\n*Remember: You can update your notes using update_memory()!*")

        return "\n".join(parts)

    async def _process_image_attachments(
        self,
        message: discord.Message,
    ) -> Any | None:
        """Process any image attachments in the message.

        Args:
            message: The Discord message.

        Returns:
            BinaryContent if image found, None otherwise.
        """
        if not message.attachments:
            return None

        for attachment in message.attachments:
            # Check if it's an image
            content_type = attachment.content_type or ""
            if content_type.startswith("image/") or attachment.filename.lower().endswith(
                (".png", ".jpg", ".jpeg", ".gif", ".webp")
            ):
                try:
                    logger.debug(f"Processing image attachment: {attachment.filename}")

                    # Download and process the image
                    binary_content = await process_discord_image(
                        attachment.url,
                        max_height=self.settings.MAX_IMAGE_HEIGHT,
                    )

                    logger.info(f"📸 Processed image: {attachment.filename}")
                    return binary_content

                except Exception as e:
                    logger.warning(f"Failed to process image {attachment.filename}: {e}")
                    continue

        return None

    async def _maybe_change_mood(self) -> None:
        """Maybe change the puppy's mood if enough time has passed.

        Mood changes every 10-30 minutes randomly.
        """
        now = datetime.now()
        minutes_since_change = (now - self.mood_changed_at).total_seconds() / 60

        # Change mood after 10-30 minutes
        if minutes_since_change > random.randint(10, 30):
            old_mood = self.current_mood
            self.current_mood = get_random_mood()
            self.mood_changed_at = now

            if old_mood != self.current_mood:
                logger.info(f"🎭 Mood changed: {old_mood.value} → {self.current_mood.value}")


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================


def create_puppy(settings: Settings | None = None) -> DiscordPuppy:
    """Create a new Discord Puppy bot instance.

    Args:
        settings: Optional settings. Loads from environment if not provided.

    Returns:
        Configured DiscordPuppy instance.

    Example:
        ```python
        puppy = create_puppy()
        puppy.run(settings.DISCORD_TOKEN)
        ```
    """
    return DiscordPuppy(settings)


def run_puppy() -> None:
    """Run the Discord Puppy bot!

    Loads settings from environment and starts the bot.
    This is the main entry point for running the bot.

    Example:
        ```python
        from discord_puppy.bot import run_puppy
        run_puppy()  # Blocks until bot shuts down
        ```
    """
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Load settings
    settings = get_settings()

    # Create and run the puppy!
    puppy = create_puppy(settings)

    logger.info("🐕 Starting Discord Puppy...")
    logger.info(f"   Chaos Level: {settings.CHAOS_LEVEL}")
    logger.info(f"   Response Chance: {settings.RESPONSE_CHANCE}")
    logger.info(
        f"   Spontaneous Interval: {settings.SPONTANEOUS_MIN_SECONDS}-{settings.SPONTANEOUS_MAX_SECONDS}s"
    )

    puppy.run(settings.DISCORD_TOKEN)


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    "DiscordPuppy",
    "create_puppy",
    "run_puppy",
]
