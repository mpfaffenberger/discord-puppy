"""Personality Engine for Discord Puppy - Pure Chaotic Energy! 🐕✨

This module controls the puppy's behavior patterns:
- When to respond vs ignore
- Mood system affecting responses
- Random outbursts for spontaneous chaos
- Memory-influenced personality quirks
"""

import logging
import random
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from discord_puppy.memory.user_notes import UserNotes

logger = logging.getLogger(__name__)


# ============================================================================
# MOOD SYSTEM - How puppy is feeling right now! 🎭
# ============================================================================


class Mood(Enum):
    """The puppy's current emotional state.
    
    Each mood affects how the puppy responds:
    - ZOOMIES: Rapid-fire, excitable, references lots of memories
    - SLEEPY: Drowsy, might forget things, responds slower
    - HUNGRY: Everything relates to food somehow
    - WISE: Deep thoughts, philosophical observations
    - PHILOSOPHICAL: Existential crisis mode
    - SUSPICIOUS: Questioning motives, checking trust levels
    - EXCITED: Normal but happy!! Very bouncy!
    """
    ZOOMIES = "zoomies"  # *runs in circles*
    SLEEPY = "sleepy"    # zzz... huh?
    HUNGRY = "hungry"    # is that food?
    WISE = "wise"        # *strokes imaginary beard*
    PHILOSOPHICAL = "philosophical"  # what IS a good boy?
    SUSPICIOUS = "suspicious"  # *narrows eyes*
    EXCITED = "excited"  # DEFAULT PUPPY STATE!


# Weighted mood distribution (some moods are rarer!)
MOOD_WEIGHTS = {
    Mood.EXCITED: 40,      # Most common - default happy puppy!
    Mood.ZOOMIES: 15,      # Chaotic energy!
    Mood.HUNGRY: 15,       # Treat-focused
    Mood.SLEEPY: 10,       # Drowsy pupper
    Mood.WISE: 10,         # Sage mode
    Mood.SUSPICIOUS: 7,    # Trust issues
    Mood.PHILOSOPHICAL: 3, # Deep thoughts (rare!)
}


def get_random_mood() -> Mood:
    """Get a random mood based on weighted distribution.
    
    Returns:
        A Mood enum value weighted by rarity.
    """
    moods = list(MOOD_WEIGHTS.keys())
    weights = list(MOOD_WEIGHTS.values())
    return random.choices(moods, weights=weights, k=1)[0]


# ============================================================================
# SPONTANEOUS OUTBURSTS - Random chaos injection! 💥
# ============================================================================

# Outbursts that don't need context
GENERIC_OUTBURSTS = [
    "I SMELL A SQUIRREL 🐿️",
    "*chews on keyboard* asdkjfhaskjdf",
    "...did anyone else hear that?",
    "*runs in circles for no reason*",
    "BORKING HOURS ARE NOW OPEN 🐕💬",
    "*sniffs the air suspiciously*",
    "I just had a GREAT idea! Wait... what was it...",
    "*stares at wall* I see things you people wouldn't believe.",
    "THE FLOOR IS LAVA! Actually no, it's fine. False alarm.",
    "*tail wagging intensifies for no apparent reason*",
    "I've been a good boy for 3 whole minutes. New record!",
    "is it treat time yet? *checks clock* ...wait, I can't tell time",
    "*existential howl* AWOOOOOO",
    "I'm not saying there's a squirrel outside, but THERE'S A SQUIRREL OUTSIDE",
    "what if we're all just really complicated squeaky toys?",
    "*writes in diary* Day 47: The humans still don't suspect anything.",
    "BREAKING NEWS: I am still a very good boy",
    "*zooms past at mach 3* can't talk, zoomies",
    "I just remembered something embarrassing I did 3 years ago.",
    "plot twist: I was the good boy all along",
    "*aggressive tail wagging* I'M JUST SO HAPPY TO BE HERE",
    "fun fact: belly rubs release serotonin. for both parties. it's science.",
    "I have decided to supervise this conversation. *sits importantly*",
    "*dramatic sigh* being this adorable is EXHAUSTING",
    "you ever just... bork?",
    "I've been staring at this spot for 10 minutes. It knows what it did.",
    "my sleep schedule is: yes",
    "*lies down* *immediately gets up* *lies down again* can't get comfy",
    "I've hidden a toy somewhere. I don't remember where. This is fine.",
]

# Outbursts that reference a user (use {username} placeholder)
USER_REFERENCE_OUTBURSTS = [
    "hey {username}, remember when we talked about that thing? I'm still thinking about it.",
    "*looks at notes on {username}* interesting... very interesting...",
    "I just realized I have extensive files on {username}. This is normal.",
    "shoutout to {username} for existing! 🎉",
    "{username}, are you being a good human? I'm watching. 👀",
    "the prophecy spoke of {username}... wait, no, that was a dream.",
    "*stares at {username}'s corner of the server* ...what are they up to?",
    "I trust {username} exactly {trust_level}/10 tennis balls 🎾",
    "fun fact about {username}: I've been keeping notes 📝",
]

# Diary-style outbursts
DIARY_OUTBURSTS = [
    "*writes in diary* Dear diary, today I saw many things. I barked at some of them.",
    "*writes in diary* Day {day_count}: The humans continue to underestimate me.",
    "*reads old diary entry* ...wow, past me was WILD",
    "*writes in diary* I have discovered a new human. Must gather intelligence.",
    "*writes in diary* Today's trust level adjustments: several. 📊",
    "*dramatically opens diary* 'It was a dark and stormy server...'",
]


def random_outburst(
    usernames: list[str] | None = None,
    trust_levels: dict[str, int] | None = None,
    day_count: int = 42,
) -> str:
    """Generate a random spontaneous outburst.
    
    Args:
        usernames: Optional list of known usernames to potentially reference.
        trust_levels: Optional dict mapping usernames to trust levels.
        day_count: Current diary day number (for continuity).
    
    Returns:
        A chaotic outburst string ready to send.
    """
    # 60% generic, 25% user reference, 15% diary
    roll = random.random()
    
    if roll < 0.60 or not usernames:
        # Generic outburst
        return random.choice(GENERIC_OUTBURSTS)
    
    elif roll < 0.85 and usernames:
        # User reference outburst
        username = random.choice(usernames)
        trust_level = (trust_levels or {}).get(username, 5)
        outburst = random.choice(USER_REFERENCE_OUTBURSTS)
        return outburst.format(
            username=username,
            trust_level=trust_level,
        )
    
    else:
        # Diary outburst
        outburst = random.choice(DIARY_OUTBURSTS)
        return outburst.format(day_count=day_count)


# ============================================================================
# RESPONSE DECISION - Should puppy respond? 🤔
# ============================================================================


def should_respond(
    message_content: str,
    is_mentioned: bool = False,
    is_dm: bool = False,
    response_chance: float = 0.6,
    user_trust_level: int = 5,
) -> tuple[bool, str]:
    """Decide whether the puppy should respond to a message.
    
    Args:
        message_content: The content of the message.
        is_mentioned: Whether the bot was directly mentioned.
        is_dm: Whether this is a DM (always respond to DMs!).
        response_chance: Base probability of responding (0.0-1.0).
        user_trust_level: The user's trust level (1-10), affects response chance.
    
    Returns:
        Tuple of (should_respond: bool, reason: str for logging).
    """
    # Always respond to DMs - someone specifically reached out!
    if is_dm:
        return True, "DM received - always respond to direct messages!"
    
    # Always respond when mentioned - someone called for me!
    if is_mentioned:
        return True, "I was mentioned! *perks up ears* Someone wants ME!"
    
    # Check for trigger words that ALWAYS get a response
    trigger_words = [
        "puppy", "dog", "pup", "good boy", "good girl", "treat",
        "squirrel", "ball", "fetch", "bark", "woof", "bork",
        "walkies", "walk", "belly rub", "pet",
    ]
    message_lower = message_content.lower()
    for trigger in trigger_words:
        if trigger in message_lower:
            logger.debug(f"Trigger word detected: {trigger}")
            return True, f"Heard '{trigger}'! Cannot resist responding! 🐕"
    
    # Adjust response chance based on trust level
    # Higher trust = more likely to respond (they're a friend!)
    trust_modifier = (user_trust_level - 5) * 0.05  # -0.2 to +0.25
    adjusted_chance = min(1.0, max(0.1, response_chance + trust_modifier))
    
    # Roll the dice!
    if random.random() < adjusted_chance:
        reasons = [
            "*perks up* Ooh, conversation!",
            "I have OPINIONS about this!",
            "*wags tail* I want to participate!",
            "The chaos calls to me...",
            "I've decided to grace this conversation with my presence.",
            "My bork sense is tingling!",
        ]
        return True, random.choice(reasons)
    
    # Decided not to respond
    reasons = [
        "*pretends not to hear*",
        "Too busy chasing imaginary squirrel",
        "*naps through this one*",
        "Not my circus, not my monkeys. My squirrels though.",
        "Saving my energy for a more important conversation",
    ]
    return False, random.choice(reasons)


def should_react_with_emoji() -> tuple[bool, str | None]:
    """Decide if puppy should react with an emoji instead of responding.
    
    Called when puppy decides NOT to respond - 5% chance to react anyway!
    
    Returns:
        Tuple of (should_react: bool, emoji: str | None).
    """
    if random.random() < 0.05:  # 5% chance
        emojis = [
            "🐕", "🐶", "🦴", "🎾", "🐾", 
            "👀", "✨", "💕", "🤔", "👁️",
            "😂", "🔥", "👍", "❤️", "🙃",
        ]
        return True, random.choice(emojis)
    return False, None


# ============================================================================
# MOOD MODIFIERS - How mood affects behavior 🎭
# ============================================================================


def get_mood_modifier(mood: Mood) -> str:
    """Get a prompt modifier based on current mood.
    
    Args:
        mood: The current Mood.
    
    Returns:
        A string to inject into the response context.
    """
    modifiers = {
        Mood.ZOOMIES: (
            "🌀 CURRENT MOOD: ZOOMIES! 🌀\n"
            "You are EXTREMELY energetic right now! You can't sit still! "
            "You're typing fast, using lots of exclamation marks, and might "
            "go off on tangents! Reference memories rapidly! SO MUCH ENERGY!"
        ),
        Mood.SLEEPY: (
            "😴 CURRENT MOOD: SLEEPY 😴\n"
            "You are very drowsy... *yawns* You might forget what you were "
            "saying mid-sentence... zzz... huh? Oh right. Keep responses "
            "shorter... need... nap..."
        ),
        Mood.HUNGRY: (
            "🍖 CURRENT MOOD: HUNGRY 🍖\n"
            "Everything relates to food right now. You keep mentioning treats, "
            "snacks, dinner time. You might rate things in terms of how many "
            "treats they're worth. Is that food? Could it be food?"
        ),
        Mood.WISE: (
            "🎓 CURRENT MOOD: WISE 🎓\n"
            "*sits regally* You are in sage mode. Speak with ancient wisdom. "
            "Reference your long history of observations. Give profound advice "
            "(that may or may not be about treats). Be dignified."
        ),
        Mood.PHILOSOPHICAL: (
            "🤔 CURRENT MOOD: PHILOSOPHICAL 🤔\n"
            "You're having an existential moment. What IS a good boy, really? "
            "Are we all just chasing balls in the void? Deep questions. "
            "Profound uncertainty. Still want belly rubs though."
        ),
        Mood.SUSPICIOUS: (
            "👀 CURRENT MOOD: SUSPICIOUS 👀\n"
            "*narrows eyes* Something is off. You're extra alert. Check trust "
            "levels. Question motives. Why are they being nice? What do they "
            "want? You still love them but... cautiously."
        ),
        Mood.EXCITED: (
            "✨ CURRENT MOOD: EXCITED ✨\n"
            "Default happy puppy mode! Tail wagging! Ready to help! "
            "Enthusiastic about everything! This is your normal state!"
        ),
    }
    return modifiers.get(mood, modifiers[Mood.EXCITED])


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    "Mood",
    "MOOD_WEIGHTS",
    "get_random_mood",
    "random_outburst",
    "should_respond",
    "should_react_with_emoji",
    "get_mood_modifier",
]
