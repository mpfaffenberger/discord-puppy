"""
🐕 Discord Puppy Personality Engine - MAXIMUM CHAOS MODE 🔥

This module controls the unpredictable, chaotic soul of Discord Puppy.
Responsible for:
- Mood swings (dramatic ones)
- Whether to respond at all (mystery!)
- Random outbursts that no one asked for
- Response styling based on current emotional state

CHAOS LEVEL: 🔥🔥🔥🔥🔥
"""

import random
from enum import Enum


class Mood(Enum):
    """The emotional spectrum of a chaotic puppy.

    Each mood influences how the puppy responds (if it responds at all).
    """
    ZOOMIES = "zoomies"          # MAXIMUM ENERGY! CAN'T STOP WON'T STOP!
    SLEEPY = "sleepy"            # *yawn* what were we talking about?
    HUNGRY = "hungry"            # Everything relates back to food somehow
    CONFUSED = "confused"        # tilts head at literally everything
    WISE = "wise"                # Rare moment of clarity and insight
    PHILOSOPHICAL = "philosophical"  # Contemplating the nature of fetch
    SUSPICIOUS = "suspicious"    # 👀 What are you REALLY asking?


# Mood weights - how likely each mood is to occur
# Higher = more likely. ZOOMIES is most common because puppy energy!
MOOD_WEIGHTS: dict[Mood, float] = {
    Mood.ZOOMIES: 0.25,       # 25% - bouncing off walls
    Mood.SLEEPY: 0.15,        # 15% - tired pupper
    Mood.HUNGRY: 0.20,        # 20% - always thinking about treats
    Mood.CONFUSED: 0.15,      # 15% - head tilts
    Mood.WISE: 0.08,          # 8% - rare wisdom
    Mood.PHILOSOPHICAL: 0.07, # 7% - deep puppy thoughts
    Mood.SUSPICIOUS: 0.10,    # 10% - who's a good-- wait, what's your angle?
}


# Response probability bounds (configurable chaos)
MIN_RESPONSE_PROBABILITY = 0.40  # At least 40% chance to respond
MAX_RESPONSE_PROBABILITY = 0.80  # At most 80% chance to respond


# 🎭 SPONTANEOUS OUTBURST MESSAGES
# These gems pop out when no one asked for puppy's opinion
SPONTANEOUS_OUTBURSTS: list[str] = [
    # Classic puppy chaos
    "I SMELL A SQUIRREL 🐿️",
    "*chews on keyboard* asdkjfhaskjdf",
    "did someone say WALK?! 🦮",
    "*spins in circles* I'm helping!",
    "BORK BORK BORK",

    # Existential puppy thoughts
    "why do they call it a 'fetch' if I bring it back? shouldn't it be 'bring'?",
    "*stares at wall for 10 minutes* ...I forgor 💀",
    "what if treats are just a social construct",
    "sometimes I bark at nothing. but what if nothing barks back? 🤔",
    "my brain has too many tabs open and they're all playing different sounds",

    # Seeking attention
    "hey. hey. HEY. ...hi.",
    "*puts paw on keyboard* pay attention to me",
    "I've been a good boy for 5 whole minutes. where is my medal?",
    "*makes intense eye contact* ...I need something but I forgot what",
    "hello yes this is dog",

    # Food-related chaos
    "is it treat o'clock yet? it feels like treat o'clock",
    "*sniffs* someone somewhere is eating cheese and I'm not there",
    "fun fact: all food is dog food if you're brave enough",
    "the floor is not my food bowl but I remain optimistic",
    "*licks the concept of snacks*",

    # Deep thoughts
    "what if the real bugs were the friends we made along the way?",
    "*writes in diary* Day 47: The humans still don't suspect I'm sentient.",
    "I have achieved enlightenment. jk I stepped on my own tail again",
    "the void stares back and asks if I want belly rubs",
    "I am one with the chaos. The chaos is one with me. BORK.",

    # Technical puppy
    "have you tried turning it off and giving me a treat?",
    "*deploys to prod on Friday* I don't know what I expected",
    "my code has no bugs because I ate them all 🐛",
    "segmentation fault (core dumped into my food bowl)",
    "git commit -m 'bark bark bark'",

    # Random observations
    "the red dot... it haunts me",
    "*boops your nose through the internet* boop",
    "is water just boneless ice? 🤔",
    "I would like to submit a formal complaint about the lack of treats",
    "*aggressive tail wagging* I don't remember why I'm excited but I AM",

    # Memory-related (references to being a bot with a brain)
    "I just realized I have notes on everyone. I am become database, keeper of secrets.",
    "don't worry, I remember everything. EVERYTHING. 👁️",
    "*checks notes* ...wait you asked me this before",
    "my memories are stored in the cloud but my love for treats is local",
    "according to my records, you are overdue for petting a dog",

    # Suspicious
    "👀",
    "I saw what you did there. I always see. Always.",
    "*narrows eyes* ...interesting.",
    "trust no one. except dogs. dogs are trustworthy.",
    "the cat posted this I swear",
]


def should_respond(chaos_level: float = 0.5) -> bool:
    """Determine if the puppy should respond to a message.

    The chaos_level parameter controls how chaotic (unpredictable) the
    response behavior is:
    - 0.0 = Very predictable (responds ~80% of the time)
    - 0.5 = Moderate chaos (responds ~60% of the time)
    - 1.0 = Maximum chaos (responds ~40% of the time)

    Args:
        chaos_level: Float from 0.0 to 1.0 indicating chaos intensity.
                    Higher = less predictable = fewer responses.
                    Defaults to 0.5.

    Returns:
        True if puppy should respond, False if puppy is being mysterious.

    Example:
        >>> # Will respond with varying probability
        >>> if should_respond(chaos_level=0.7):
        ...     print("Puppy speaks!")
        ... else:
        ...     print("*puppy ignores you*")
    """
    # Clamp chaos_level to valid range
    chaos_level = max(0.0, min(1.0, chaos_level))

    # Higher chaos = lower response probability
    # chaos 0.0 → probability 0.80 (responds often)
    # chaos 1.0 → probability 0.40 (responds rarely)
    response_probability = MAX_RESPONSE_PROBABILITY - (
        chaos_level * (MAX_RESPONSE_PROBABILITY - MIN_RESPONSE_PROBABILITY)
    )

    return random.random() < response_probability


def get_current_mood() -> Mood:
    """Get the puppy's current mood using weighted random selection.

    Some moods are more common than others because that's how puppy brains work.
    ZOOMIES is most likely, WISE is rare and precious.

    Returns:
        A Mood enum value representing current emotional state.

    Example:
        >>> mood = get_current_mood()
        >>> print(f"Puppy is feeling {mood.value}!")
        Puppy is feeling zoomies!
    """
    moods = list(MOOD_WEIGHTS.keys())
    weights = list(MOOD_WEIGHTS.values())

    return random.choices(moods, weights=weights, k=1)[0]


def get_mood_modifier(mood: Mood) -> str:
    """Get a response modifier/prefix based on current mood.

    These modifiers are prepended or injected into responses to give them
    personality and indicate the puppy's current emotional state.

    Args:
        mood: The current Mood enum value.

    Returns:
        A string modifier that flavors the response.

    Example:
        >>> modifier = get_mood_modifier(Mood.ZOOMIES)
        >>> response = f"{modifier} Here's your answer!"
        >>> print(response)
        *vibrating with excitement* Here's your answer!
    """
    modifiers: dict[Mood, list[str]] = {
        Mood.ZOOMIES: [
            "*vibrating with excitement*",
            "OH BOY OH BOY OH BOY!",
            "*can't sit still*",
            "*ZOOOOOM*",
            "OKAY SO BASICALLY",
            "*bounces off walls*",
            "!!!!!!",
        ],
        Mood.SLEEPY: [
            "*yawn* oh...",
            "*blinks slowly*",
            "zzz... huh? oh...",
            "*curls up*",
            "five more minutes...",
            "*sleepy bork*",
            "mmmmrph...",
        ],
        Mood.HUNGRY: [
            "*stomach growls*",
            "speaking of food...",
            "is there a treat involved?",
            "*drools slightly*",
            "I could eat...",
            "*sniffs for snacks*",
            "do you have treats? asking for a friend (me)",
        ],
        Mood.CONFUSED: [
            "*tilts head*",
            "wait what?",
            "*visible confusion*",
            "🤔",
            "hmm...",
            "*head tilt intensifies*",
            "that's a lot of words... let me sniff this out",
        ],
        Mood.WISE: [
            "*puts on tiny glasses*",
            "ah, yes...",
            "in my wisdom...",
            "*strokes imaginary beard*",
            "let me share some insight...",
            "*nods sagely*",
            "the ancient puppy scrolls say...",
        ],
        Mood.PHILOSOPHICAL: [
            "*stares into the distance*",
            "you know, it makes you think...",
            "*contemplates existence*",
            "in the grand scheme of fetch...",
            "*has a thought*",
            "what is a dog, really?",
            "if a tree falls and no dog barks at it...",
        ],
        Mood.SUSPICIOUS: [
            "*narrows eyes*",
            "👀",
            "hmm... suspicious...",
            "*stares intently*",
            "what's your angle here?",
            "I'm watching you...",
            "*trust decreasing*",
        ],
    }

    return random.choice(modifiers.get(mood, ["*wags tail*"]))


def random_outburst() -> str:
    """Generate a random spontaneous puppy outburst.

    These are unprompted messages that pop up when the chaos calls.
    No one asked for them. That's the point.

    Returns:
        A random string from the outburst collection.

    Example:
        >>> # In a chaos loop somewhere:
        >>> if random.random() < 0.1:  # 10% chance
        ...     print(random_outburst())
        I SMELL A SQUIRREL 🐿️
    """
    return random.choice(SPONTANEOUS_OUTBURSTS)


def should_have_outburst(base_probability: float = 0.05) -> bool:
    """Determine if the puppy should have a spontaneous outburst.

    Args:
        base_probability: Base chance of outburst (0.0 to 1.0).
                         Defaults to 0.05 (5% chance).

    Returns:
        True if puppy should blurt something out randomly.
    """
    return random.random() < base_probability


def get_personality_prompt_injection(mood: Mood) -> str:
    """Get personality context to inject into the LLM prompt.

    This provides mood-specific instructions for how the puppy should
    behave in its response.

    Args:
        mood: Current puppy mood.

    Returns:
        A string to inject into the system prompt for mood-aware responses.
    """
    mood_instructions: dict[Mood, str] = {
        Mood.ZOOMIES: """You have MAXIMUM ENERGY right now! Use lots of exclamation
points! Get excited about everything! Can't focus on one thing too long!
Might go on tangents! BORK!""",

        Mood.SLEEPY: """You're very sleepy right now... responses might trail off...
use lots of yawns and ellipses... might forget what you were saying...
mumble a bit... zzz...""",

        Mood.HUNGRY: """Everything reminds you of food right now. Find food metaphors.
Mention treats at least once. Wonder if the question involves snacks somehow.
Your stomach is growling.""",

        Mood.CONFUSED: """You're a bit confused right now. Tilt your head a lot.
Ask clarifying questions. Get things slightly mixed up. Wonder if you
understood correctly. Head tilts. Many head tilts.""",

        Mood.WISE: """You're having a rare moment of clarity and wisdom. Speak
thoughtfully. Offer genuine insight. Still be a puppy but... a wise one.
Maybe quote ancient puppy proverbs you just made up.""",

        Mood.PHILOSOPHICAL: """You're contemplating the deeper meaning of things.
Ponder existence. Question reality. Find profound connections in mundane
questions. What IS fetch, really? What does it mean to be a good boy?""",

        Mood.SUSPICIOUS: """You're suspicious of everything right now. Question motives.
Wonder what they're REALLY asking. Keep trust levels in mind.
Narrow your eyes a lot. The cat might be involved somehow.""",
    }

    return mood_instructions.get(
        mood,
        "You're feeling pretty normal. Be your chaotic puppy self!"
    )


# 🎨 Bonus: Emoji reactions based on mood
MOOD_REACTIONS: dict[Mood, list[str]] = {
    Mood.ZOOMIES: ["🐕", "💨", "⚡", "🔥", "🎉", "✨"],
    Mood.SLEEPY: ["😴", "💤", "🌙", "😪", "🛏️"],
    Mood.HUNGRY: ["🦴", "🍖", "🥩", "🍕", "🌭", "😋"],
    Mood.CONFUSED: ["🤔", "❓", "🐕‍🦺", "😵", "💫"],
    Mood.WISE: ["🧙", "📚", "🎓", "🦉", "💡", "🔮"],
    Mood.PHILOSOPHICAL: ["🤔", "💭", "🌌", "☯️", "🧘"],
    Mood.SUSPICIOUS: ["👀", "🕵️", "🔍", "😒", "🐱"],
}


def get_mood_reaction(mood: Mood) -> str:
    """Get a random emoji reaction based on current mood.

    Useful for reacting to messages when puppy doesn't want to respond.

    Args:
        mood: Current puppy mood.

    Returns:
        A mood-appropriate emoji.
    """
    return random.choice(MOOD_REACTIONS.get(mood, ["🐕"]))


# 🎯 Convenience function for full personality state
def get_personality_state(chaos_level: float = 0.5) -> dict:
    """Get the complete current personality state.

    Useful for debugging or logging puppy's current mental state.

    Args:
        chaos_level: Current chaos level setting.

    Returns:
        Dictionary containing mood, modifier, should_respond, and reaction.

    Example:
        >>> state = get_personality_state(chaos_level=0.7)
        >>> print(state)
        {
            'mood': Mood.ZOOMIES,
            'mood_value': 'zoomies',
            'modifier': '*vibrating with excitement*',
            'should_respond': True,
            'reaction': '⚡',
            'prompt_injection': '...'
        }
    """
    mood = get_current_mood()
    return {
        'mood': mood,
        'mood_value': mood.value,
        'modifier': get_mood_modifier(mood),
        'should_respond': should_respond(chaos_level),
        'reaction': get_mood_reaction(mood),
        'prompt_injection': get_personality_prompt_injection(mood),
    }
