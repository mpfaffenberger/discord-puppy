#!/usr/bin/env python3
"""Discord Puppy Entry Point 🐕💥

Run with: python -m discord_puppy

This is where the chaos begins!
"""

import sys

# Fun ASCII art banner! 🐕
BANNER = r"""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║      🐕💥 DISCORD PUPPY 💥🐕                                       ║
║                                                                   ║
║         __                                                        ║
║     ___( o)>   WOOF! I'm awake!                                   ║
║     \ <_. )    Ready to bring CHAOS!                              ║
║      `---'                                                        ║
║                                                                   ║
║      Chaotic • Self-Evolving • Remembers Everything              ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
"""

GOODBYE_MESSAGE = r"""
🐕 *yawns* Okay, I'm going to sleep now...
   Remember: I'll remember EVERYTHING when I wake up! 🧠

   Goodbye, humans! *curls up into a ball*
"""


def main() -> None:
    """Main entry point for Discord Puppy.

    Prints a fun banner, initializes the bot, and handles
    graceful shutdown on keyboard interrupt.
    """
    # Print the glorious banner!
    print(BANNER)
    print("🐕 Starting Discord Puppy...")
    print("   Press Ctrl+C to send me to sleep!")
    print()

    try:
        # Import here to avoid circular imports and for cleaner errors
        from discord_puppy.bot import run_puppy

        # Let's GO! 🚀
        run_puppy()

    except KeyboardInterrupt:
        # Graceful shutdown! 💤
        print(GOODBYE_MESSAGE)
        sys.exit(0)

    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("\n💡 Make sure you've installed all dependencies:")
        print("   pip install -e .")
        print("   # or")
        print("   uv sync")
        sys.exit(1)

    except ValueError as e:
        # Usually a config validation error
        print(f"\n❌ Configuration error: {e}")
        print("\n💡 Check your .env file has valid values!")
        print("   See .env.example for reference.")
        sys.exit(1)

    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print("\n🐕 *confused puppy noises* Something went wrong!")
        print("   Check the logs for more details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
