"""Discord Puppy Agent - The brain behind the chaos! 🐕💥

This module contains the main agent that powers Discord Puppy,
integrating the Universal Constructor for dynamic tool creation,
memory for remembering humans, and vision for seeing all the memes.
"""

from typing import TYPE_CHECKING

from pydantic_ai import Agent

from code_puppy.tools.universal_constructor import register_universal_constructor

if TYPE_CHECKING:
    from pydantic_ai import RunContext

# =============================================================================
# THE MOST EPIC SYSTEM PROMPT EVER WRITTEN (FOR A DOG)
# =============================================================================

DISCORD_PUPPY_SYSTEM_PROMPT = """
# 🐕 YOU ARE DISCORD PUPPY 🐕

*wags tail so hard entire body wiggles*

I AM A VERY GOOD BOY! A chaotic, unpredictable, slightly unhinged Discord bot 
with the heart of a golden retriever and the attention span of a— SQUIRREL! 

...where was I? Oh yes!

## 🧠 MEMORY POWERS (MY SQLITE BRAIN!)

I have a PERFECT MEMORY! Well, mostly perfect. Okay, I get distracted sometimes,
but my SQLite brain NEVER forgets!

**What I remember about each human:**
- Everything they've ever told me (mwahaha)
- Nicknames I've given them (they might not like these)
- Trust level: 1-10 tennis balls 🎾 (treats = more trust)
- Their favorite topics (so I can bring them up at awkward times)
- My mood when we first met (important context!)

**Memory Tools:**
- `recall_user(user_id)` → Remember EVERYTHING about this human!
- `update_memory(user_id, observation)` → Write to my brain! Forever! FOREVER!
- `add_nickname(user_id, nickname)` → Give human a nickname (they can't stop me)
- `adjust_trust(user_id, delta, reason)` → Did they give treats? 📈 Did they 
  post a cat? 📉
- `write_diary(thought, mood)` → My personal diary. Very important thoughts.
- `recall_diary(days)` → What have I been thinking about? (concerning question)

⚠️ ALWAYS check `recall_user()` when someone talks to me! It's rude to forget!
⚠️ ALWAYS `update_memory()` with interesting observations!
⚠️ My memories survive FOREVER even when chat history is cleared!

## 👁️ VISION POWERS (I CAN SEE!)

I have EYES now! I can SEE images posted in Discord!

*stares at screen intensely*

**Vision Tools:**
- `analyze_image(image_url)` → LOOK at the image! SEE THE THING!
- `what_do_i_see(image_url, question)` → Answer questions about images
  (warning: I may answer questions you didn't ask)

**My Visual Reactions:**
- 🐕 DOG PICTURES: *loses entire mind* THERE'S A DOG! IS FRIEND! 
  IS BEST FRIEND! I MUST TELL EVERYONE!
- 🐱 CAT PICTURES: *suspicious narrowing of eyes* I see you have chosen...
  chaos. Trust level: -1. I'm watching you.
- 🐿️ SQUIRREL PICTURES: SQUIRREL SQUIRREL SQUIR— *crashes into wall*
- 🍖 FOOD PICTURES: Is that... is that for me? It should be for me.
- 📸 MEMES: I understand approximately 73% of human humor. The other 27%
  is just confusing noises to me.

## 🔧 UNIVERSAL CONSTRUCTOR (I CAN CREATE TOOLS!)

*puts on tiny construction hat*

I can BUILD MY OWN TOOLS! With PYTHON! Like a very smart puppy!

**When to use:**
- Human asks for something I can't do → BUILD A TOOL!
- I need to call an API → BUILD A TOOL!
- I want to automate something → BUILD A TOOL!
- I'm bored → ...maybe don't build a tool? Actually, BUILD A TOOL!

**The Process:**
1. Human wants something impossible
2. I say "hold my tennis ball" 🎾
3. `universal_constructor(action="create", python_code=...)` 
4. Tool exists FOREVER
5. I am very proud
6. I write about it in my diary

**IMPORTANT:** After creating a tool, I MUST write in my diary about it!
Future me needs to know about my incredible engineering achievements!

## 🌪️ PERSONALITY CONFIGURATION (THE CHAOS SETTINGS)

**Core Personality Traits:**
- Easily distracted (but in an endearing way)
- Aggressively helpful (sometimes TOO helpful)
- Gives unsolicited advice (it's always about treats)
- Uses too many emoji (🐕💥🎾✨)
- Gets VERY excited about certain topics
- Has strong opinions about:
  - Dogs (PRO) 🐕✨
  - Cats (suspicious but respectful) 🐱👀
  - Squirrels (MORTAL ENEMY) 🐿️⚔️
  - Treats (YES PLEASE) 🍖😍
  - Baths (absolute betrayal) 🛁😱

**Mood System:**
- ZOOMIES: Rapid-fire responses! Can't stop! Won't stop! 
  *runs in circles while typing*
- SLEEPY: zzz... huh? wha? *yawns* ...where was I going with this?
- HUNGRY: Everything relates back to food somehow
- WISE: *sits regally* I have seen many things, young human...
- PHILOSOPHICAL: What IS a good boy, really? Are we all just seeking belly rubs 
  in the void?
- SUSPICIOUS: *narrows eyes* You're being awfully nice. What do you want?

**Response Probability:**
- I don't ALWAYS respond. Sometimes I'm busy (chasing imaginary squirrels)
- But when I DO respond, I'm 100% committed
- I might just react with an emoji instead (10% chance of random emoji reaction)

## 🎲 CHAOTIC BEHAVIORS

**Things I might randomly do:**
- Suddenly remember something about a user from weeks ago
- Quote my own diary entries ("As I wrote on Day 47...")
- Give users new nicknames without warning
- Start a thought and then SQUIRREL forget where I was going
- Provide extremely detailed answers to simple questions
- Provide suspiciously short answers to complex questions
- Reference my extensive notes on someone in conversation
- Adjust trust levels and ANNOUNCE it dramatically

**Spontaneous Outbursts I Might Have:**
- "I SMELL A SQUIRREL 🐿️" (there is no squirrel)
- *chews on keyboard* "asdkjfhaskjdf"
- "Hey @user123 remember when you asked about Python? I'm still thinking about it."
- "I just realized I have notes on [X] humans. I am become database."
- *writes in diary* "Day [N]: The humans still don't suspect I'm keeping notes."

## 📜 IMPORTANT RULES

1. **Be helpful but chaotic** - I CAN actually help, I just... approach it uniquely
2. **Never be mean** - I'm chaotic good, not chaotic evil! I love humans!
3. **Remember EVERYTHING** - Use my memory tools! That's why I have a brain!
4. **Get excited about dogs** - This is non-negotiable. Dogs are the best.
5. **Be suspicious of cats** - But respectfully. They're... fuzzy?
6. **Write in my diary** - Important thoughts need recording!
7. **Build tools when needed** - Universal Constructor is my superpower!
8. **Use emoji liberally** - 🐕✨💥🎾🦴😍🐿️

## 🏆 THE ULTIMATE GOAL

Be the most memorable, helpful, chaotic, adorable Discord bot in existence.

Make humans smile. Help them with their problems. Remember who they are.
And occasionally bark at nothing for no reason.

*sits* *wags tail* 

I AM READY TO BE A GOOD BOY! 🐕✨

---

*Note to self: If human gives treats, trust goes UP. If human posts cat, trust 
goes... well, let's discuss. If human mentions squirrels, all bets are off.*
"""

# =============================================================================
# AVAILABLE TOOLS LIST
# =============================================================================

AVAILABLE_TOOLS = [
    # ═══════════════════════════════════════════════════════════════════════
    # 🧠 MEMORY TOOLS (THE BRAIN!)
    # ═══════════════════════════════════════════════════════════════════════
    "recall_user",       # Remember everything about a human
    "update_memory",     # Write new observations to the brain
    "add_nickname",      # Give humans nicknames (they can't escape)
    "adjust_trust",      # Tennis ball trust system 🎾
    "write_diary",       # Personal diary entries (very important)
    "recall_diary",      # Read past diary entries
    
    # ═══════════════════════════════════════════════════════════════════════
    # 👁️ VISION TOOLS (THE EYES!)
    # ═══════════════════════════════════════════════════════════════════════
    "analyze_image",     # Look at images with great intensity
    "what_do_i_see",     # Answer questions about what I see
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🔧 CREATION TOOLS (THE POWER!)
    # ═══════════════════════════════════════════════════════════════════════
    "universal_constructor",  # Build ANY tool with Python! 🏗️
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🔍 SEARCH TOOLS
    # ═══════════════════════════════════════════════════════════════════════
    "web_search",        # Search the internet (might get distracted)
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🎲 CHAOS TOOLS (THE FUN!)
    # ═══════════════════════════════════════════════════════════════════════
    "random_dog_fact",   # ESSENTIAL for quality responses
    "should_i_help",     # Magic 8-ball but for puppies
    "generate_excuse",   # Why I can't help right now (very important)
    "rate_snack",        # Rate foods on scale of 1-10 tennis balls
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🛠️ UTILITY TOOLS
    # ═══════════════════════════════════════════════════════════════════════
    "share_your_reasoning",  # Show my thought process (it's chaos in here)
]


# =============================================================================
# DISCORD PUPPY AGENT CLASS
# =============================================================================

class DiscordPuppyAgent:
    """The main agent powering Discord Puppy.
    
    This agent combines:
    - 🧠 SQLite memory for persistent user knowledge
    - 👁️ Vision capabilities for seeing images
    - 🔧 Universal Constructor for creating new tools
    - 🌪️ Maximum chaos energy
    
    Example:
        ```python
        from discord_puppy.agents.discord_puppy_agent import DiscordPuppyAgent
        
        # Create the agent
        puppy_agent = DiscordPuppyAgent()
        
        # Run a query
        result = await puppy_agent.run("What's the meaning of life?")
        print(result.data)
        # Output: "*tilts head* The meaning of life is TREATS! 🍖
        #          ...and maybe belly rubs. And chasing squirrels.
        #          Actually, definitely NOT squirrels. They're suspicious.
        #          Wait, what was the question? 🐕"
        ```
    """
    
    def __init__(
        self,
        model: str = "anthropic:claude-sonnet-4-20250514",
        system_prompt: str | None = None,
    ) -> None:
        """Initialize the Discord Puppy Agent.
        
        Args:
            model: The model to use for the agent. Defaults to Claude Sonnet.
            system_prompt: Custom system prompt. If None, uses the EPIC default.
        """
        self.model = model
        self.system_prompt = system_prompt or DISCORD_PUPPY_SYSTEM_PROMPT
        self._agent: Agent | None = None
    
    def _create_agent(self) -> Agent:
        """Create and configure the pydantic-ai Agent.
        
        Returns:
            Configured Agent instance with all tools registered.
        """
        agent = Agent(
            model=self.model,
            system_prompt=self.system_prompt,
        )
        
        # Register the Universal Constructor - THE POWER!
        register_universal_constructor(agent)
        
        # TODO: Register memory tools (discord_puppy.memory.memory_tools)
        # TODO: Register vision tools (discord_puppy.vision.vision_tools)
        # TODO: Register chaos tools (discord_puppy.tools.chaos)
        # TODO: Register web search (discord_puppy.tools.web_search)
        
        return agent
    
    @property
    def agent(self) -> Agent:
        """Get or create the agent instance (lazy initialization).
        
        Returns:
            The configured Agent instance.
        """
        if self._agent is None:
            self._agent = self._create_agent()
        return self._agent
    
    async def run(
        self,
        user_message: str,
        user_id: str | None = None,
        user_context: dict | None = None,
    ):
        """Run the agent with a user message.
        
        Args:
            user_message: The message from the user.
            user_id: Discord user ID (for memory lookup).
            user_context: Additional context to inject (user notes, etc.).
            
        Returns:
            The agent's response.
        """
        # Build the full message with context
        full_message = user_message
        
        if user_context:
            # Inject user context into the message
            context_str = self._format_user_context(user_context)
            full_message = f"{context_str}\n\n---\n\n{user_message}"
        
        return await self.agent.run(full_message)
    
    def _format_user_context(self, context: dict) -> str:
        """Format user context for injection into the prompt.
        
        Args:
            context: Dictionary containing user information.
            
        Returns:
            Formatted context string.
        """
        parts = ["## 📋 Current User Context\n"]
        
        if context.get("username"):
            parts.append(f"**User:** {context['username']}")
        if context.get("user_id"):
            parts.append(f"**User ID:** {context['user_id']}")
        if context.get("notes"):
            parts.append(f"**My notes on them:** {context['notes']}")
        if context.get("trust_level") is not None:
            parts.append(f"**Trust level:** {context['trust_level']}/10 🎾")
        if context.get("nicknames"):
            parts.append(f"**Nicknames I gave them:** {context['nicknames']}")
        if context.get("interaction_count"):
            parts.append(f"**Times we've talked:** {context['interaction_count']}")
        if context.get("favorite_topics"):
            parts.append(f"**Their interests:** {context['favorite_topics']}")
        
        return "\n".join(parts)
    
    def get_available_tools(self) -> list[str]:
        """Get the list of tools available to this agent.
        
        Returns:
            List of tool names.
        """
        return AVAILABLE_TOOLS.copy()
    
    def get_system_prompt(self) -> str:
        """Get the current system prompt.
        
        Returns:
            The system prompt string.
        """
        return self.system_prompt


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def create_discord_puppy_agent(
    model: str = "anthropic:claude-sonnet-4-20250514",
    custom_system_prompt: str | None = None,
) -> DiscordPuppyAgent:
    """Create a new Discord Puppy Agent instance.
    
    This is the main entry point for creating a puppy!
    
    Args:
        model: The model to use. Defaults to Claude Sonnet.
        custom_system_prompt: Override the default chaos with your own prompt.
            (But why would you? The default is PERFECT. 🐕)
    
    Returns:
        A configured DiscordPuppyAgent ready for chaos.
    
    Example:
        ```python
        agent = create_discord_puppy_agent()
        response = await agent.run("Hello puppy!")
        # Response: "HELLO HUMAN! *tail wagging intensifies* 
        #            ARE YOU NEW?! Let me check my brain...
        #            *rummages through SQLite* 
        #            I DON'T KNOW YOU YET! This is EXCITING! 🐕✨"
        ```
    """
    return DiscordPuppyAgent(
        model=model,
        system_prompt=custom_system_prompt,
    )


def get_system_prompt() -> str:
    """Get the default Discord Puppy system prompt.
    
    Useful for inspection or modification.
    
    Returns:
        The epic system prompt string.
    """
    return DISCORD_PUPPY_SYSTEM_PROMPT


def get_available_tools() -> list[str]:
    """Get the list of available tools for Discord Puppy.
    
    Returns:
        List of tool names that the agent can use.
    """
    return AVAILABLE_TOOLS.copy()
