"""Web search integration - Brave, SearxNG, and optional premium APIs."""
import os
import aiohttp
from typing import List, Dict, Optional


class WebSearcher:
    """Search the web for fresh information."""

    def __init__(self):
        self.searxng_url = os.getenv("SEARXNG_URL", "https://searx.be")
        self.brave_api_key = os.getenv("BRAVE_API_KEY")
        self.serper_api_key = os.getenv("SERPER_API_KEY")
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")

    async def search(self, query: str, num_results: int = 5) -> List[Dict]:
        """Search web and return results.

        Priority order (tries in this order):
        1. Brave Search API (2,000/month free) - Best quality
        2. Serper API (2,500/month free) - Google results
        3. Tavily API (premium, $29/mo) - Optional
        4. SearxNG (unlimited free) - Always available fallback

        Args:
            query: Search query
            num_results: Number of results to return

        Returns:
            List of dicts with title, url, snippet
        """
        # Try Brave first (best free tier - 2,000/month)
        if self.brave_api_key:
            results = await self._search_brave(query, num_results)
            if results:
                return results

        # Try Serper (2,500/month free)
        if self.serper_api_key:
            results = await self._search_serper(query, num_results)
            if results:
                return results

        # Try Tavily (premium, optional)
        if self.tavily_api_key:
            results = await self._search_tavily(query, num_results)
            if results:
                return results

        # Fall back to SearxNG (always free)
        return await self._search_searxng(query, num_results)

    async def _search_brave(self, query: str, num_results: int) -> List[Dict]:
        """Search using Brave Search API (2,000 searches/month free)."""
        url = "https://api.search.brave.com/res/v1/web/search"
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.brave_api_key
        }
        params = {
            "q": query,
            "count": num_results
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params, timeout=10) as resp:
                    if resp.status != 200:
                        return []

                    data = await resp.json()
                    results = data.get("web", {}).get("results", [])

                    # Format results
                    formatted = []
                    for result in results[:num_results]:
                        formatted.append({
                            "title": result.get("title", ""),
                            "url": result.get("url", ""),
                            "snippet": result.get("description", ""),
                            "source": "Brave"
                        })

                    return formatted

        except Exception as e:
            print(f"Brave search error: {e}")
            return []

    async def _search_serper(self, query: str, num_results: int) -> List[Dict]:
        """Search using Serper API (2,500 searches/month free)."""
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": self.serper_api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "q": query,
            "num": num_results
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers, timeout=10) as resp:
                    if resp.status != 200:
                        return []

                    data = await resp.json()
                    results = data.get("organic", [])

                    # Format results
                    formatted = []
                    for result in results[:num_results]:
                        formatted.append({
                            "title": result.get("title", ""),
                            "url": result.get("link", ""),
                            "snippet": result.get("snippet", ""),
                            "source": "Serper"
                        })

                    return formatted

        except Exception as e:
            print(f"Serper search error: {e}")
            return []

    async def _search_searxng(self, query: str, num_results: int) -> List[Dict]:
        """Search using SearxNG public instance (unlimited free)."""
        url = f"{self.searxng_url}/search"
        params = {
            "q": query,
            "format": "json",
            "pageno": 1
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=10) as resp:
                    if resp.status != 200:
                        return []

                    data = await resp.json()
                    results = data.get("results", [])

                    # Format results
                    formatted = []
                    for result in results[:num_results]:
                        formatted.append({
                            "title": result.get("title", ""),
                            "url": result.get("url", ""),
                            "snippet": result.get("content", ""),
                            "source": "SearxNG"
                        })

                    return formatted

        except Exception as e:
            print(f"SearxNG search error: {e}")
            return []

    async def _search_tavily(self, query: str, num_results: int) -> List[Dict]:
        """Search using Tavily API (premium, optional)."""
        url = "https://api.tavily.com/search"
        headers = {"Content-Type": "application/json"}
        payload = {
            "api_key": self.tavily_api_key,
            "query": query,
            "max_results": num_results,
            "include_answer": True,
            "include_raw_content": False
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers, timeout=10) as resp:
                    if resp.status != 200:
                        # Fall back to SearxNG
                        return await self._search_searxng(query, num_results)

                    data = await resp.json()
                    results = data.get("results", [])

                    # Format results
                    formatted = []
                    for result in results:
                        formatted.append({
                            "title": result.get("title", ""),
                            "url": result.get("url", ""),
                            "snippet": result.get("content", ""),
                            "source": "Tavily"
                        })

                    return formatted

        except Exception as e:
            print(f"Tavily search error: {e}")
            # Fall back to SearxNG
            return await self._search_searxng(query, num_results)

    async def search_with_context(self, query: str, num_results: int = 5) -> Dict:
        """Search and return formatted context for Claude.ai."""
        results = await self.search(query, num_results)

        return {
            "query": query,
            "num_results": len(results),
            "results": results,
            "citation_format": "Use format: [Web: {title}, {url}]"
        }
