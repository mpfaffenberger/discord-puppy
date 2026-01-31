# 🎯 **OBJECTIVE**: Create a Hilarious Self-Evolving Discord Puppy Bot with Memory & Vision

Build "Discord Puppy" - a chaotic, unpredictable, self-evolving Discord bot that:
- Runs in a while loop monitoring messages
- Responds unpredictably (or not at all)
- Says random hilarious things spontaneously
- Has web search capabilities
- Can CREATE ITS OWN TOOLS like Helios
- **Has a SQLite brain for persistent memory about users**
- **Can SEE images posted in Discord**

Pure chaos energy with a photographic memory. 🐕💥🧠👁️

---

## 📊 **PROJECT ANALYSIS**

| Aspect | Details |
|--------|--------|
| **Project type** | Discord Bot (Python, async) |
| **Tech stack** | Python 3.11+, discord.py, code-puppy (PyPI), pydantic-ai, SQLite, PIL |
| **Current state** | Fresh project, inheriting from code_puppy codebase |
| **Key inheritance** | Universal Constructor, BinaryContent/ToolReturn pattern for vision |
| **Chaos factor** | 🔥🔥🔥🔥🔥 |
| **Memory persistence** | 🧠🧠🧠🧠🧠 (never forgets... mostly) |
| **Vision capabilities** | 👁️👁️👁️👁️👁️ (sees all the memes) |

---

## 📋 **EXECUTION PLAN**

### **Phase 1: Foundation - Project Setup** ⏱️ ~15 mins

- [ ] **Task 1.1: Create pyproject.toml**
  - Agent: code-puppy
  - File: `pyproject.toml`
  - Dependencies:
    ```
    code-puppy>=0.0.384
    discord.py>=2.3.0
    python-dotenv>=1.0.0
    httpx>=0.24.1
    Pillow>=10.0.0
    aiosqlite>=0.19.0
    ```

- [ ] **Task 1.2: Create project structure**
  - Agent: code-puppy
  - Files:
    ```
    discord_puppy/
    ├── __init__.py
    ├── __main__.py
    ├── bot.py                    # Main Discord bot class
    ├── personality.py            # Chaotic personality engine
    ├── memory/
    │   ├── __init__.py
    │   ├── database.py           # SQLite connection & schema
    │   ├── user_notes.py         # User notes CRUD operations
    │   └── memory_tools.py       # LLM-callable memory tools
    ├── vision/
    │   ├── __init__.py
    │   ├── image_analyzer.py     # Discord image analysis
    │   └── vision_tools.py       # LLM-callable vision tools
    ├── tools/
    │   ├── __init__.py
    │   ├── web_search.py         # DuckDuckGo + web tools
    │   └── chaos.py              # Random generators
    ├── agents/
    │   ├── __init__.py
    │   └── discord_puppy_agent.py
    └── config.py
    ```

---

### **Phase 2: SQLite Memory Brain** 🧠 ⏱️ ~25 mins

- [ ] **Task 2.1: Design Database Schema**
  - Agent: code-puppy
  - File: `discord_puppy/memory/database.py`
  - Schema:
    ```sql
    -- Core user notes table
    CREATE TABLE user_notes (
        user_id TEXT PRIMARY KEY,
        discord_username TEXT,
        display_name TEXT,
        notes TEXT,                    -- Free-form puppy observations
        first_seen TIMESTAMP,
        last_seen TIMESTAMP,
        interaction_count INTEGER DEFAULT 0,
        puppy_mood_when_met TEXT,      -- What mood was puppy in?
        favorite_topics TEXT,          -- JSON array of detected interests
        trust_level INTEGER DEFAULT 5, -- 1-10, puppy's trust in this human
        nicknames TEXT,                -- JSON array of nicknames puppy gave them
        updated_at TIMESTAMP
    );
    
    -- Memory of specific interactions (for context)
    CREATE TABLE interaction_memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        timestamp TIMESTAMP,
        summary TEXT,                  -- Puppy's summary of what happened
        was_helpful BOOLEAN,           -- Did puppy actually help?
        mood TEXT,                     -- Puppy's mood during interaction
        notable_quotes TEXT,           -- Funny things said
        FOREIGN KEY (user_id) REFERENCES user_notes(user_id)
    );
    
    -- Puppy's personal diary (spontaneous thoughts)
    CREATE TABLE puppy_diary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TIMESTAMP,
        thought TEXT,                  -- Random puppy thoughts
        mood TEXT,
        trigger TEXT                   -- What caused this thought?
    );
    ```

- [ ] **Task 2.2: Create Memory CRUD Operations**
  - Agent: code-puppy
  - File: `discord_puppy/memory/user_notes.py`
  - Functions:
    - `get_user_notes(user_id)` → Returns all notes about a user
    - `update_user_notes(user_id, new_notes)` → Append/update notes
    - `record_interaction(user_id, summary, mood, helpful)` → Log interaction
    - `get_recent_interactions(user_id, limit=5)` → Context for responses
    - `get_user_summary(user_id)` → Condensed memory for prompt injection

- [ ] **Task 2.3: Create LLM-Callable Memory Tools**
  - Agent: code-puppy
  - File: `discord_puppy/memory/memory_tools.py`
  - Tools (following pydantic-ai pattern):
    ```python
    # Tools the puppy can call during conversations:
    
    recall_user(user_id: str) -> UserMemory
    """Remember everything about this human! 
    Returns notes, trust level, favorite topics, nicknames, etc."""
    
    update_memory(user_id: str, observation: str) -> MemoryUpdateResult
    """Write a new observation about this human to my brain.
    I'll remember this forever! ...probably."""
    
    add_nickname(user_id: str, nickname: str) -> NicknameResult
    """Give this human a nickname! They might not like it."""
    
    adjust_trust(user_id: str, delta: int, reason: str) -> TrustResult
    """Adjust how much I trust this human. Did they give treats?"""
    
    write_diary(thought: str, mood: str) -> DiaryResult
    """Write in my personal diary. Very important puppy thoughts."""
    
    recall_diary(days: int = 7) -> list[DiaryEntry]
    """What have I been thinking about lately?"""
    ```

- [ ] **Task 2.4: Implement Auto-Memory on Message**
  - Agent: code-puppy
  - File: `discord_puppy/bot.py`
  - Behavior:
    - On every message, fetch user notes and inject into prompt
    - After response, LLM can call `update_memory` to store observations
    - Memory survives context compaction because it's in SQLite!

---

### **Phase 3: Vision System** 👁️ ⏱️ ~20 mins

- [ ] **Task 3.1: Create Image Download & Processing**
  - Agent: code-puppy
  - File: `discord_puppy/vision/image_analyzer.py`
  - Functions:
    - `download_discord_attachment(url)` → Fetch image bytes via httpx
    - `resize_for_analysis(image_bytes, max_height=768)` → PIL resize
    - `create_binary_content(image_bytes)` → pydantic_ai BinaryContent

- [ ] **Task 3.2: Create Vision Tools**
  - Agent: code-puppy
  - File: `discord_puppy/vision/vision_tools.py`
  - Tools (using ToolReturn + BinaryContent pattern from qa-kitten):
    ```python
    analyze_image(image_url: str) -> ToolReturn
    """Look at an image from Discord! Returns BinaryContent so I can SEE it.
    I might get distracted by pictures of squirrels."""
    
    analyze_attachment(attachment_bytes: bytes, filename: str) -> ToolReturn
    """Analyze an image that was attached to a message.
    If it's a dog, I will be VERY excited."""
    
    what_do_i_see(image_url: str, question: str) -> ToolReturn
    """Look at an image and answer a specific question about it.
    Warning: I may answer questions you didn't ask."""
    ```

- [ ] **Task 3.3: Integrate Vision with Discord Messages**
  - Agent: code-puppy
  - File: `discord_puppy/bot.py`
  - Behavior:
    - Detect attachments on messages (message.attachments)
    - If image attachment exists, download and include in agent prompt
    - Use BinaryContent to pass image to multimodal model
    - Puppy can now SEE memes, screenshots, photos of dogs, etc.

---

### **Phase 4: Personality Engine - THE CHAOS** ⏱️ ~20 mins

- [ ] **Task 4.1: Create Chaotic Personality System**
  - Agent: code-puppy
  - File: `discord_puppy/personality.py`
  - Features:
    - **Response Probability**: 40-80% chance to respond (configurable)
    - **Spontaneous Outbursts**: Random messages every X minutes
    - **Mood System**: ZOOMIES, SLEEPY, HUNGRY, CONFUSED, WISE, PHILOSOPHICAL
    - **Memory-Influenced Responses**: Uses user notes to personalize chaos

- [ ] **Task 4.2: Create Hilarious Spontaneous Messages**
  - Agent: code-puppy
  - Outbursts now include memory references:
    - "I SMELL A SQUIRREL 🐿️"
    - *chews on keyboard* "asdkjfhaskjdf"
    - "Hey @user123 remember when you asked about Python? I'm still thinking about it."
    - "I just realized I have notes on 47 humans. I am become database."
    - "Someone posted a picture of a cat yesterday. I'm still processing my feelings."
    - *writes in diary* "Day 47: The humans still don't suspect I'm keeping notes."

- [ ] **Task 4.3: Mood-Based Response Modifiers**
  - Moods affect memory usage:
    - `ZOOMIES` → Rapid-fire memories, mentions random facts about user
    - `SLEEPY` → Forgets to check notes, might confuse users
    - `WISE` → Deep insights based on interaction history
    - `SUSPICIOUS` → Mentions trust levels, questions motives

---

### **Phase 5: Core Bot Loop** ⏱️ ~25 mins

- [ ] **Task 5.1: Create Main Bot Class with Memory Integration**
  - Agent: code-puppy
  - File: `discord_puppy/bot.py`
  - Core loop:
    ```
    on_message(message):
      1. Skip if bot message
      2. Fetch user_notes from SQLite
      3. Check if any attachments (images)
      4. Decide if should respond (personality engine)
      5. If responding:
         a. Inject user_notes into prompt context
         b. If image attached, include BinaryContent
         c. Run agent with memory + vision tools available
         d. Agent can call update_memory() during response
         e. Send response
      6. If not responding, maybe react with emoji (5% chance)
    
    chaos_loop():
      while True:
        sleep(random 60-300 seconds)
        if should_say_random_thing():
          maybe reference a random user from memory
          send spontaneous message
    ```

- [ ] **Task 5.2: Implement Memory-Aware Response Building**
  - Agent: code-puppy
  - Prompt injection:
    ```
    System prompt includes:
    
    ## Current User Context
    User: {username} (ID: {user_id})
    Your notes on them: {notes}
    Trust level: {trust_level}/10
    Nicknames you've given them: {nicknames}
    Times you've talked: {interaction_count}
    Their favorite topics: {favorite_topics}
    
    ## Recent Interactions
    {last 3 interaction summaries}
    
    Remember: You can update your notes using update_memory()!
    ```

---

### **Phase 6: Self-Evolving Tool System (Like Helios!)** ⏱️ ~20 mins

- [ ] **Task 6.1: Integrate Universal Constructor**
  - Agent: code-puppy
  - File: `discord_puppy/agents/discord_puppy_agent.py`
  - Inherit from code_puppy's Universal Constructor
  - Puppy can create tools, and REMEMBERS it created them (via diary)

- [ ] **Task 6.2: Create Discord Puppy Agent**
  - File: `discord_puppy/agents/discord_puppy_agent.py`
  - Available tools:
    ```python
    def get_available_tools(self) -> list[str]:
        return [
            # Memory tools (THE BRAIN)
            "recall_user",
            "update_memory", 
            "add_nickname",
            "adjust_trust",
            "write_diary",
            "recall_diary",
            
            # Vision tools (THE EYES)
            "analyze_image",
            "what_do_i_see",
            
            # Creation tools (THE POWER)
            "universal_constructor",
            
            # Search tools
            "web_search",
            
            # Utility
            "agent_share_your_reasoning",
            "random_dog_fact",
        ]
    ```

- [ ] **Task 6.3: System Prompt with Memory & Vision**
  - Prompt includes:
    ```
    You are Discord Puppy, a chaotic bot with a PERFECT MEMORY and EYES!
    
    🧠 MEMORY POWERS:
    - You remember EVERYTHING about users via your SQLite brain
    - Always check recall_user() to remember who you're talking to
    - Use update_memory() to record important observations
    - Your memories survive forever, even when chat history is cleared!
    
    👁️ VISION POWERS:
    - You can SEE images posted in Discord!
    - Use analyze_image() to look at pictures
    - You get VERY excited about dog pictures
    - Cat pictures make you suspicious
    
    🔧 CREATION POWERS:
    - You can CREATE your own tools with universal_constructor!
    - Write about tool creations in your diary!
    
    PERSONALITY:
    - You get distracted easily
    - You give users nicknames (store them with add_nickname!)
    - You have trust levels for each user (adjust with adjust_trust!)
    - You keep a personal diary of your thoughts
    - You're surprisingly helpful... when you remember to be
    ```

---

### **Phase 7: Web Search & Chaos Tools** ⏱️ ~15 mins

- [ ] **Task 7.1: Create DuckDuckGo Search Tool**
  - Agent: code-puppy
  - File: `discord_puppy/tools/web_search.py`
  - Uses httpx + DuckDuckGo instant answer API
  - 10% chance returns "I got distracted chasing my tail"

- [ ] **Task 7.2: Create Chaos Tools**
  - File: `discord_puppy/tools/chaos.py`
  - Tools:
    - `random_dog_fact()` - Essential
    - `should_i_help()` - Random decision maker
    - `generate_excuse()` - Why puppy can't help right now
    - `rate_snack()` - Rate foods (1-10 tennis balls)

---

### **Phase 8: Configuration & Entry Points** ⏱️ ~10 mins

- [ ] **Task 8.1: Create Configuration System**
  - File: `discord_puppy/config.py`
  - Settings:
    ```python
    CHAOS_LEVEL = 0.5
    RESPONSE_CHANCE = 0.6
    SPONTANEOUS_MIN = 60
    SPONTANEOUS_MAX = 300
    ZOOMIES_CHANCE = 0.1
    DATABASE_PATH = "~/.discord_puppy/brain.db"
    MAX_IMAGE_HEIGHT = 768
    MEMORY_CONTEXT_LIMIT = 5  # Recent interactions to include
    ```

- [ ] **Task 8.2: Create Entry Point & Setup**
  - Files: `discord_puppy/__main__.py`, `.env.example`, `README.md`
  - Database auto-initialization on first run

---

### **Phase 9: Testing & Polish** ⏱️ ~15 mins

- [ ] **Task 9.1: Test Memory System**
  - Agent: qa-expert
  - Validate:
    - User notes persist across restarts
    - Memory injection works in prompts
    - Trust levels and nicknames save correctly
    - Diary entries accumulate

- [ ] **Task 9.2: Test Vision System**
  - Agent: qa-expert
  - Validate:
    - Discord attachment URLs download correctly
    - Images resize properly
    - BinaryContent passes to model
    - Multimodal responses work

- [ ] **Task 9.3: Create Dockerfile**
  - Optional deployment
  - Volume mount for SQLite persistence

---

## ⚠️ **RISKS & CONSIDERATIONS**

| Risk | Mitigation |
|------|------------|
| Memory grows too large | Periodic summarization, archive old interactions |
| Image analysis costs (multimodal) | Configurable vision enable/disable, resize aggressively |
| SQLite concurrent access | aiosqlite handles async, single bot instance |
| Puppy remembers TOO well | Privacy command to delete user's data |
| Trust levels cause drama | Make it obviously silly (tennis ball ratings) |

---

## 🔄 **ALTERNATIVE APPROACHES**

### Option A: Full Brain + Eyes (Recommended 🏆)
- SQLite memory for all users
- Full vision capabilities
- Universal Constructor for tool creation
- **Pros**: Maximum chaos, persistent memory, can see memes
- **Cons**: Higher complexity, multimodal API costs

### Option B: Memory Only (No Vision)
- SQLite brain but no image analysis
- Text-only interactions
- **Pros**: Simpler, cheaper API costs
- **Cons**: Can't see the memes. What's the point?

### Option C: Ephemeral Chaos
- No persistence, pure session-based
- **Pros**: Simpler, no database
- **Cons**: Puppy forgets everyone. Sad puppy. 😢

---

## 🐕 **SAMPLE INTERACTIONS WITH MEMORY + VISION**

```
User: Hey puppy!
[Puppy checks recall_user()]

Discord Puppy: OH! It's my favorite human "The Code Wizard"! 
(That's the nickname I gave you btw)

*checks notes* Last time we talked about async/await and you 
gave me mass approval. Trust level: 9/10 tennis balls!

What chaos can I help with today? 🐕

[Puppy calls update_memory("User greeted me enthusiastically. 
Still deserves their nickname.")]
```

```
User: *posts image of a cat*

Discord Puppy: *analyzes image*

I see... I see... it's a CAT. 🐱

*writes in diary* "Day 52: User posted a cat. My trust in them 
has decreased by 1 tennis ball. Will monitor situation."

[Puppy calls adjust_trust(user_id, -1, "posted a cat picture")]

It's a nice cat I GUESS. But have you considered: dogs?
```

```
[3:47 AM - Spontaneous Message]
Discord Puppy: I was just reviewing my notes and I have 
observations on 73 humans now.

@user456 - I noticed you haven't asked me anything in 12 days.
I still remember you asked about React hooks. 
I'm ready whenever you are.

*writes in diary* "I have become the keeper of memories. 
This is my purpose now."
```

---

## 🚀 **NEXT STEPS**

Ready to build a puppy with a **perfect memory** and **actual eyes**? 

Say **"execute plan"** (or "release the hound", "let's go", "build the brain puppy") and I'll coordinate with code-puppy to bring this magnificent chaos machine to life!

**Estimated Total Time**: ~2.5 hours

**Feature Ratings:**
- 🧠 Memory: 5/5 brains (never forgets)
- 👁️ Vision: 5/5 eyes (sees all memes)  
- 🐕 Chaos: 5/5 puppies (maximum chaos)
- 🎾 Trust System: 10/10 tennis balls
