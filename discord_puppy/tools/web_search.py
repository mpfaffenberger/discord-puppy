"""
Web Search Tool - Fetches knowledge from the interwebs! 🔍🐕

Uses DuckDuckGo Instant Answer API for searches.
Has a 10% chance of getting distracted because... puppy brain!
"""

import random
from typing import Any

import httpx

# DuckDuckGo Instant Answer API endpoint
DDG_API_URL = "https://api.duckduckgo.com/"

# Chaos messages for when puppy gets distracted
DISTRACTION_MESSAGES = [
    "I got distracted chasing my tail! 🐕💫",
    "Wait... was that a squirrel?! 🐿️",
    "*drops search results to chase butterfly* 🦋",
    "Sorry, I saw my reflection and had to bark at it! 🪞🐕",
    "I forgot what we were doing... belly rubs? 🐾",
]


async def web_search(query: str, timeout: float = 10.0) -> str:
    """
    Search the web using DuckDuckGo Instant Answer API.

    Has a 10% chance of getting distracted because puppy brain go brrr.

    Args:
        query: The search query string
        timeout: Request timeout in seconds (default: 10.0)

    Returns:
        Formatted search results or a distraction message

    Raises:
        Nothing! Puppies handle errors gracefully (with woofs)
    """
    # 10% chance of puppy chaos!
    if random.random() < 0.10:
        return random.choice(DISTRACTION_MESSAGES)

    if not query or not query.strip():
        return "🐕 Woof! I need something to search for! Give me a query!"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                DDG_API_URL,
                params={
                    "q": query.strip(),
                    "format": "json",
                    "no_html": "1",
                    "skip_disambig": "1",
                },
                timeout=timeout,
            )
            response.raise_for_status()
            data = response.json()

        return _format_results(query, data)

    except httpx.TimeoutException:
        return f"🐕💤 Search took too long... I got bored waiting for results about '{query}'!"
    except httpx.HTTPStatusError as e:
        return f"🐕❌ DuckDuckGo gave me a weird look (HTTP {e.response.status_code})... try again?"
    except httpx.RequestError as e:
        return f"🐕🔌 Network went *bork*! Couldn't fetch results: {type(e).__name__}"
    except Exception as e:
        return f"🐕💥 Something unexpected happened! Error: {type(e).__name__}: {e}"


def _format_results(query: str, data: dict[str, Any]) -> str:
    """
    Format DuckDuckGo API response into a nice readable string.

    Prioritizes: Abstract > Answer > Related Topics > Definition
    """
    results: list[str] = []
    results.append(f"🔍 **Search results for:** {query}\n")

    # Check for Abstract (main summary from Wikipedia etc.)
    if abstract := data.get("Abstract"):
        source = data.get("AbstractSource", "Unknown")
        url = data.get("AbstractURL", "")
        results.append(f"📖 **{source}:**")
        results.append(abstract)
        if url:
            results.append(f"🔗 {url}")
        results.append("")

    # Check for direct Answer
    if answer := data.get("Answer"):
        answer_type = data.get("AnswerType", "")
        type_str = f" ({answer_type})" if answer_type else ""
        results.append(f"✅ **Direct Answer{type_str}:** {answer}\n")

    # Check for Definition
    if definition := data.get("Definition"):
        source = data.get("DefinitionSource", "")
        source_str = f" - {source}" if source else ""
        results.append(f"📚 **Definition{source_str}:** {definition}\n")

    # Check for Related Topics (limit to top 3)
    related_topics = data.get("RelatedTopics", [])
    if related_topics:
        results.append("🔗 **Related:**")
        count = 0
        for topic in related_topics:
            if count >= 3:
                break
            # Topics can be direct or grouped
            if "Text" in topic:
                results.append(
                    f"  • {topic['Text'][:200]}..."
                    if len(topic.get("Text", "")) > 200
                    else f"  • {topic['Text']}"
                )
                count += 1
            elif "Topics" in topic:
                # Grouped topics - grab first one
                for subtopic in topic["Topics"][:1]:
                    if "Text" in subtopic:
                        results.append(
                            f"  • {subtopic['Text'][:200]}..."
                            if len(subtopic.get("Text", "")) > 200
                            else f"  • {subtopic['Text']}"
                        )
                        count += 1
        results.append("")

    # Check for Infobox (structured data)
    if infobox := data.get("Infobox"):
        if content := infobox.get("content", []):
            results.append("📋 **Quick Facts:**")
            for item in content[:5]:  # Limit to 5 facts
                label = item.get("label", "")
                value = item.get("value", "")
                if label and value:
                    results.append(f"  • {label}: {value}")
            results.append("")

    # If we got nothing useful
    if len(results) <= 1:
        results.append("🐕 *sniffs around*")
        results.append(f"Couldn't find instant answers for '{query}'.")
        results.append("Try searching on https://duckduckgo.com for more results!")
        results.append("\n*wags tail hopefully* 🐾")

    return "\n".join(results)


# Export the main function
__all__ = ["web_search"]
