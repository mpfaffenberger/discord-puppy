"""Tools subsystem - Utilities for chaos and helpfulness! 🔧

Modules:
- web_search.py: DuckDuckGo search (with 10% chaos chance)
- chaos.py: Random dog facts, excuses, snack ratings, etc.
"""

from discord_puppy.tools.web_search import web_search
from discord_puppy.tools.chaos import (
    CHAOS_TOOLS,
    generate_excuse,
    random_dog_fact,
    rate_snack,
    should_i_help,
)

__all__ = [
    "web_search",
    "random_dog_fact",
    "should_i_help",
    "generate_excuse",
    "rate_snack",
    "CHAOS_TOOLS",
]
