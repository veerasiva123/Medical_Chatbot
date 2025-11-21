from typing import List
from ddgs import DDGS  


def web_search_with_duckduckgo(query: str, max_results: int = 3) -> str:
    """Perform a free web search using DuckDuckGo (no API key required)."""
    results: List[str] = []

    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results, safesearch="moderate"):
                title = r.get("title", "")
                snippet = r.get("body", "")
                link = r.get("href", "")
                if snippet:
                    results.append(f"- **{title}** — {snippet} (Source: {link})")
    except Exception as e:
        raise RuntimeError(f"DuckDuckGo search failed: {e}")

    if not results:
        return "No relevant web results found from DuckDuckGo."

    return "\n".join(results)