"""
Heartbeat Engine - The Chaos Pulse 💓🐕

This module controls when the puppy speaks! It implements a heartbeat
system that decides whether to bark based on:

- 5-second heartbeat interval
- 4% spontaneous message chance (if no one's talking)
- 20% base response chance (if there are new messages)
- 100% response chance (if directly mentioned)

Engagement System 📈:
- When a response roll fails, boost chance by +15% for next message
- Boost decays by -15% every 30 seconds of inactivity
- Max boost capped at +60% (so 80% total response chance)
- Boost resets to 0% when we actually respond

This makes the puppy more likely to respond the longer it stays quiet!
Pure chaos, but controlled chaos. Like a puppy on a leash.
"""

import asyncio
import random
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Callable, Awaitable

import discord


@dataclass
class PendingMessage:
    """A message waiting to potentially be responded to."""
    message: discord.Message
    is_mention: bool
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class HeartbeatConfig:
    """Configuration for the heartbeat engine."""
    interval_seconds: float = 5.0
    spontaneous_chance: float = 0.04  # 4% when no messages
    response_chance: float = 0.20     # 20% when there are messages
    mention_chance: float = 1.0       # 100% when directly mentioned
    
    # Engagement system - builds up when we stay quiet, decays over time
    engagement_boost_amount: float = 0.15   # +15% per failed roll
    engagement_decay_amount: float = 0.15   # -15% per decay tick
    engagement_decay_seconds: float = 30.0  # Decay every 30 seconds
    engagement_max_boost: float = 0.60      # Cap at +60% (so max 80% total)


class HeartbeatEngine:
    """The chaos pulse that controls when the puppy speaks.
    
    This engine runs a background loop that checks every N seconds
    whether the puppy should say something. The decision is based on:
    
    1. Were there any new messages since the last heartbeat?
    2. Was the puppy directly mentioned?
    3. Roll the dice based on the configured chances!
    """

    def __init__(
        self,
        client: discord.Client,
        config: Optional[HeartbeatConfig] = None,
        on_should_respond: Optional[Callable[[list[PendingMessage]], Awaitable[None]]] = None,
        on_spontaneous: Optional[Callable[[], Awaitable[None]]] = None,
    ):
        """Initialize the heartbeat engine.
        
        Args:
            client: Discord client instance
            config: Heartbeat configuration (uses defaults if None)
            on_should_respond: Callback when puppy should respond to messages
            on_spontaneous: Callback when puppy should say something random
        """
        self.client = client
        self.config = config or HeartbeatConfig()
        self.on_should_respond = on_should_respond
        self.on_spontaneous = on_spontaneous
        
        # Message queue - messages seen since last heartbeat
        self._pending_messages: deque[PendingMessage] = deque(maxlen=100)
        
        # State tracking
        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._last_heartbeat: Optional[datetime] = None
        
        # Track the last channel we saw activity in (for spontaneous messages)
        self._last_active_channel: Optional[discord.TextChannel] = None
        
        # Engagement system - builds up when ignored, decays over time
        self._engagement_boost: float = 0.0
        self._last_decay_time: datetime = datetime.utcnow()

    def queue_message(self, message: discord.Message, is_mention: bool = False) -> None:
        """Add a message to the pending queue.
        
        Called by the message handler whenever a new message comes in.
        
        Args:
            message: The Discord message
            is_mention: Whether the puppy was directly mentioned
        """
        self._pending_messages.append(PendingMessage(
            message=message,
            is_mention=is_mention,
        ))
        self._last_active_channel = message.channel

    def start(self) -> None:
        """Start the heartbeat loop."""
        if self._running:
            return
        
        self._running = True
        self._task = asyncio.create_task(self._heartbeat_loop())
        print(f"💓 Heartbeat started! Interval: {self.config.interval_seconds}s")

    def stop(self) -> None:
        """Stop the heartbeat loop."""
        self._running = False
        if self._task:
            self._task.cancel()
            self._task = None
        print("💔 Heartbeat stopped.")

    async def _heartbeat_loop(self) -> None:
        """The main heartbeat loop - runs every N seconds."""
        while self._running:
            try:
                await asyncio.sleep(self.config.interval_seconds)
                await self._process_heartbeat()
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"❌ Heartbeat error: {e}")
                # Don't crash the loop on errors
                continue

    def _apply_engagement_decay(self) -> None:
        """Decay the engagement boost over time."""
        now = datetime.utcnow()
        elapsed = (now - self._last_decay_time).total_seconds()
        
        # How many decay ticks have passed?
        decay_ticks = int(elapsed / self.config.engagement_decay_seconds)
        
        if decay_ticks > 0 and self._engagement_boost > 0:
            old_boost = self._engagement_boost
            decay_amount = decay_ticks * self.config.engagement_decay_amount
            self._engagement_boost = max(0.0, self._engagement_boost - decay_amount)
            self._last_decay_time = now
            
            if old_boost != self._engagement_boost:
                print(f"📉 Engagement decayed: {old_boost:.0%} → {self._engagement_boost:.0%}")

    def _boost_engagement(self) -> None:
        """Increase engagement boost after a failed roll."""
        old_boost = self._engagement_boost
        self._engagement_boost = min(
            self.config.engagement_max_boost,
            self._engagement_boost + self.config.engagement_boost_amount
        )
        print(f"📈 Engagement boosted: {old_boost:.0%} → {self._engagement_boost:.0%}")

    def _reset_engagement(self) -> None:
        """Reset engagement boost after responding."""
        if self._engagement_boost > 0:
            print(f"🔄 Engagement reset: {self._engagement_boost:.0%} → 0%")
            self._engagement_boost = 0.0

    @property
    def effective_response_chance(self) -> float:
        """Get the current response chance including engagement boost."""
        return min(1.0, self.config.response_chance + self._engagement_boost)

    async def _process_heartbeat(self) -> None:
        """Process a single heartbeat - decide whether to speak!"""
        self._last_heartbeat = datetime.utcnow()
        
        # Apply engagement decay first
        self._apply_engagement_decay()
        
        # Grab all pending messages and clear the queue
        pending = list(self._pending_messages)
        self._pending_messages.clear()
        
        # Check if we were directly mentioned in any message
        mentions = [m for m in pending if m.is_mention]
        non_mentions = [m for m in pending if not m.is_mention]
        
        # Decision time! 🎲
        should_respond = False
        response_messages: list[PendingMessage] = []
        
        # Rule 1: Direct mentions = 100% response
        if mentions:
            roll = random.random()
            if roll < self.config.mention_chance:
                should_respond = True
                response_messages = mentions  # Respond to all mentions
                print(f"💬 Mention detected! (roll={roll:.2f}, threshold={self.config.mention_chance})")
        
        # Rule 2: Non-mention messages = base chance + engagement boost
        if non_mentions and not should_respond:
            roll = random.random()
            effective_chance = self.effective_response_chance
            
            if roll < effective_chance:
                should_respond = True
                # Pick a random subset of messages to respond to (max 3)
                response_messages = random.sample(
                    non_mentions, 
                    min(len(non_mentions), 3)
                )
                print(f"🎲 Response roll succeeded! (roll={roll:.2f}, threshold={effective_chance:.0%} [base={self.config.response_chance:.0%} + boost={self._engagement_boost:.0%}])")
                # Reset engagement on successful response
                self._reset_engagement()
            else:
                print(f"🎲 Response roll failed. (roll={roll:.2f}, threshold={effective_chance:.0%} [base={self.config.response_chance:.0%} + boost={self._engagement_boost:.0%}])")
                # Boost engagement for next time!
                self._boost_engagement()
        
        # Rule 3: No messages = 4% spontaneous chance
        if not pending:
            roll = random.random()
            if roll < self.config.spontaneous_chance:
                print(f"✨ Spontaneous message! (roll={roll:.2f}, threshold={self.config.spontaneous_chance})")
                if self.on_spontaneous:
                    # Fire-and-forget so multiple can be in-flight!
                    asyncio.create_task(self.on_spontaneous())
                return
        
        # Execute the response if we should
        if should_respond and response_messages and self.on_should_respond:
            # Fire-and-forget so multiple responses can be in-flight!
            asyncio.create_task(self.on_should_respond(response_messages))

    @property
    def last_active_channel(self) -> Optional[discord.TextChannel]:
        """Get the last channel where activity was seen."""
        return self._last_active_channel

    @property
    def is_running(self) -> bool:
        """Check if the heartbeat is running."""
        return self._running
