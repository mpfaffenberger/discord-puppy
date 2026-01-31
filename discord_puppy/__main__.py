"""
Discord Puppy Entry Point 🐕

This is where the chaos begins! Run with:
    discord-puppy
    # or
    python -m discord_puppy

Requires DISCORD_TOKEN environment variable.
"""

import asyncio
import os
import random
import sys
from typing import Optional

import discord
from dotenv import load_dotenv

from discord_puppy.memory.database import init_database, get_connection, ensure_user_exists
from discord_puppy.memory.message_indexer import index_all_guilds, index_message, compute_message_hash
from discord_puppy.heartbeat import HeartbeatEngine, HeartbeatConfig, PendingMessage
from discord_puppy.agents.puppy_agent import get_puppy_agent
from discord_puppy.tools.discord_send import set_current_channel

# Load .env file if present
load_dotenv()

# Intents - we need message content to see what people are saying!
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# The bot client
client = discord.Client(intents=intents)

# Heartbeat engine (initialized on ready)
heartbeat: Optional[HeartbeatEngine] = None


async def handle_should_respond(pending_messages: list[PendingMessage]) -> None:
    """Callback when the heartbeat decides we should respond."""
    if not pending_messages:
        return
    
    # Get the puppy agent
    agent = get_puppy_agent()
    
    # Set current channel so discord_send_message tool works
    channel = pending_messages[-1].message.channel
    set_current_channel(channel, asyncio.get_event_loop())
    
    # Build prompt from messages - agent history handles context
    prompt_parts = [f"{pm.message.author.display_name}: {pm.message.content}" for pm in pending_messages]
    prompt = "\n".join(prompt_parts)
    
    # Generate response via run_with_mcp
    result = await agent.run_with_mcp(prompt)
    response = result.output if result else "*tilts head confused* 🐕"
    
    # Reply to the most recent message (or the mention if there is one)
    target_message = pending_messages[-1].message
    for pm in pending_messages:
        if pm.is_mention:
            target_message = pm.message
            break
    
    try:
        await target_message.reply(response)
        print(f"🐕 Responded to {target_message.author.display_name}!")
    except discord.HTTPException as e:
        print(f"❌ Failed to send response: {e}")


async def handle_spontaneous() -> None:
    """Callback when the heartbeat decides we should say something random."""
    global heartbeat
    
    if not heartbeat or not heartbeat.last_active_channel:
        return
    
    channel = heartbeat.last_active_channel
    
    # Set current channel so discord_send_message tool works
    set_current_channel(channel, asyncio.get_event_loop())
    
    # Generate spontaneous message via run_with_mcp
    agent = get_puppy_agent()
    result = await agent.run_with_mcp("*wakes up* say something random and chill")
    message = result.output if result else "*yawns* 🐕"
    
    try:
        await channel.send(message)
        print(f"✨ Spontaneous message sent to #{channel.name}!")
    except discord.HTTPException as e:
        print(f"❌ Failed to send spontaneous message: {e}")


@client.event
async def on_ready() -> None:
    """Called when the puppy wakes up and is ready to cause chaos!"""
    global heartbeat
    
    print(f"🐕 WOOF! Discord Puppy is online as {client.user}!")
    print(f"🧠 Initializing brain...")
    await init_database()

    # Index message history from all guilds!
    print(f"📚 Indexing message history (this might take a bit)...")
    stats = await index_all_guilds(
        client,
        limit_per_channel=500,  # Reasonable default
        days_back=30,  # Last month of messages
    )

    print(f"📊 Indexing complete!")
    print(f"   🏠 Guilds: {stats['guilds_processed']}")
    print(f"   📺 Channels: {stats['channels_processed']}")
    print(f"   ✨ New messages: {stats['new_messages']}")
    print(f"   ⏭️  Skipped (already indexed): {stats['skipped_messages']}")
    print(f"   📨 Total processed: {stats['total_processed']}")

    # Initialize and start the heartbeat engine!
    heartbeat = HeartbeatEngine(
        client=client,
        config=HeartbeatConfig(
            interval_seconds=5.0,      # 5-second heartbeat
            spontaneous_chance=0.04,   # 4% when quiet
            response_chance=0.20,      # 20% when there are messages
            mention_chance=1.0,        # 100% when mentioned
        ),
        on_should_respond=handle_should_respond,
        on_spontaneous=handle_spontaneous,
    )
    heartbeat.start()

    print(f"✨ Ready to cause chaos in {len(client.guilds)} server(s)!")


@client.event
async def on_message(message: discord.Message) -> None:
    """Handle incoming messages with maximum chaos energy."""
    global heartbeat
    
    # Don't respond to ourselves (infinite loop = bad puppy!)
    if message.author == client.user:
        return

    # Don't respond to other bots (we're not that desperate for friends)
    if message.author.bot:
        return

    # Track the user in our brain!
    conn = await get_connection()
    try:
        await ensure_user_exists(
            conn,
            user_id=str(message.author.id),
            username=message.author.name,
            display_name=message.author.display_name,
            mood="curious",  # We're always curious when meeting someone!
        )
        
        # Index this message too!
        message_hash = compute_message_hash(message)
        await index_message(conn, message, message_hash)
        await conn.commit()
    finally:
        await conn.close()

    # Check if we were mentioned
    is_mention = client.user is not None and client.user.mentioned_in(message)
    
    # Queue the message for the heartbeat to consider
    if heartbeat:
        heartbeat.queue_message(message, is_mention=is_mention)


def main() -> None:
    """Main entry point for the Discord Puppy bot."""
    token = os.getenv("DISCORD_TOKEN")

    if not token:
        print("❌ ERROR: No DISCORD_TOKEN found!")
        print("")
        print("Please set your Discord bot token:")
        print("  export DISCORD_TOKEN='your-token-here'")
        print("")
        print("Or create a .env file with:")
        print("  DISCORD_TOKEN=your-token-here")
        print("")
        print("Get a token from: https://discord.com/developers/applications")
        sys.exit(1)

    print("🐕 Starting Discord Puppy...")
    print("🔑 Token found, connecting to Discord...")

    try:
        client.run(token)
    except discord.LoginFailure:
        print("❌ ERROR: Invalid Discord token!")
        print("Make sure your DISCORD_TOKEN is correct.")
        sys.exit(1)
    except discord.PrivilegedIntentsRequired:
        print("❌ ERROR: Missing required intents!")
        print("")
        print("Please enable these intents in Discord Developer Portal:")
        print("  1. Go to https://discord.com/developers/applications")
        print("  2. Select your bot -> Bot -> Privileged Gateway Intents")
        print("  3. Enable 'MESSAGE CONTENT INTENT' and 'SERVER MEMBERS INTENT'")
        sys.exit(1)


if __name__ == "__main__":
    main()
