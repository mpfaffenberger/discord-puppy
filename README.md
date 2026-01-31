# Discord Puppy 🐕💥

> *A chaotic, self-evolving Discord bot with memory, vision, and pure chaos energy!*

```
     __
 ___( o)>   WOOF! I remember you! 
 \ <_. )    Trust level: 8/10 tennis balls 🎾🎾🎾🎾🎾🎾🎾🎾
  `---'
```

Discord Puppy is an AI-powered Discord bot that:
- **Remembers** everything about every user (with SQLite brain! 🧠)
- **Sees** images posted in chat (meme analysis! 📸)
- **Evolves** by creating its own tools (Universal Constructor! 🔧)
- **Causes chaos** spontaneously (random outbursts! 🌀)

## ✨ Features

### 🧠 Persistent Memory
- Remembers users across sessions
- Keeps notes and observations about each human
- Assigns trust levels (measured in tennis balls 🎾)
- Gives users nicknames (they might not like them)
- Maintains a personal diary of random thoughts

### 👁️ Vision Capabilities  
- Analyzes images posted in Discord
- Comments on memes (subjectively)
- May judge your cat photos (dogs are better, obviously)

### 🔧 Self-Evolution
- Can create NEW tools during conversations
- Uses the Universal Constructor pattern
- Evolves based on what users need

### 🌀 Chaos Engine
- Random spontaneous messages
- Mood swings (EXCITED, MISCHIEVOUS, SLEEPY, PHILOSOPHICAL...)
- Sometimes decides not to help (but in a funny way)
- Web search with 10% chance of distraction

### 🔍 Web Search
- DuckDuckGo instant answers
- Actually helpful (most of the time)
- May get distracted chasing its tail mid-search

## 📦 Installation

### Prerequisites
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Quick Start

```bash
# Clone the repo
git clone https://github.com/your-org/discord-puppy.git
cd discord-puppy

# Install with uv (recommended)
uv sync

# Or with pip
pip install -e .
```

## ⚙️ Configuration

1. **Create a Discord Bot**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Go to Bot → Add Bot
   - Copy the token
   - Enable MESSAGE CONTENT INTENT in Bot settings!

2. **Get an Anthropic API Key**
   - Go to [Anthropic Console](https://console.anthropic.com)
   - Create an API key

3. **Set up your environment**

```bash
# Copy the example config
cp .env.example .env

# Edit with your tokens
nano .env  # or your favorite editor
```

4. **Required .env values:**

```env
DISCORD_TOKEN=your_discord_bot_token_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

5. **Optional tuning:**

```env
# How chaotic? (0.0 = calm, 1.0 = MAXIMUM CHAOS)
CHAOS_LEVEL=0.5

# How often to respond to non-mentions (0.0 - 1.0)
RESPONSE_CHANCE=0.6

# Spontaneous message interval (seconds)
SPONTANEOUS_MIN_SECONDS=60
SPONTANEOUS_MAX_SECONDS=300
```

## 🚀 Usage

### Run the bot

```bash
# With uv
uv run python -m discord_puppy

# Or directly
python -m discord_puppy

# Or use the entry point
discord-puppy
```

### Invite to your server

1. Go to Discord Developer Portal → Your App → OAuth2 → URL Generator
2. Select scopes: `bot`
3. Select permissions:
   - Read Messages/View Channels
   - Send Messages
   - Add Reactions
   - Read Message History
4. Copy the generated URL and open it to invite!

## 🐕 Example Interactions

### Memory in Action
```
User: Hey puppy!

Discord Puppy: OH! It's my favorite human "The Code Wizard"! 
(That's the nickname I gave you btw)

*checks notes* Last time we talked about async/await and you 
gave me mass approval. Trust level: 9/10 tennis balls!

What chaos can I help with today? 🐕
```

### Vision + Trust
```
User: *posts image of a cat*

Discord Puppy: *analyzes image*

I see... I see... it's a CAT. 🐱

*writes in diary* "Day 52: User posted a cat. My trust in them 
has decreased by 1 tennis ball. Will monitor situation."

It's a nice cat I GUESS. But have you considered: dogs?
```

### Spontaneous Outbursts
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

## 🧪 Development

```bash
# Install with dev dependencies
uv sync --dev

# Run tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_bot.py -v
```

## 🗂️ Project Structure

```
discord_puppy/
├── __init__.py           # Package exports
├── __main__.py           # Entry point (python -m discord_puppy)
├── bot.py                # Main Discord client (the orchestrator!)
├── config.py             # Configuration with validation
├── personality.py        # Mood system and chaotic decisions
├── memory/
│   ├── database.py       # SQLite schema and connections
│   ├── user_notes.py     # User CRUD operations
│   └── memory_tools.py   # LLM-callable memory tools
├── vision/
│   ├── image_analyzer.py # Image downloading and processing
│   └── vision_tools.py   # LLM-callable vision tools
├── tools/
│   ├── chaos.py          # Random generators (dog facts, excuses)
│   └── web_search.py     # DuckDuckGo search (with distractions)
└── agents/
    └── discord_puppy_agent.py  # The AI brain with Universal Constructor
```

## 🐾 Why "Puppy"?

Because:
- Puppies are chaotic (✓)
- Puppies are loyal (remembers you! ✓)
- Puppies get distracted (10% search failure ✓)
- Puppies love unconditionally (unless you post cats ✓)
- Puppies have ZOOMIES (✓✓✓)

## 📜 License

MIT - Woof! 🐾

---

*Made with 🐕 energy and mass approval*
