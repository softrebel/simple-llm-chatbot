import requests

from app.config import settings
from app.search.base import SearchEngine, SearchError


class WikipediaSearchEngine(SearchEngine):
    BASE_URL = "https://en.wikipedia.org/w/api.php"

    def search(self, query: str) -> list[dict]:
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "utf8": 1,
            "srlimit": settings.search_limit,
        }

        HEADERS = {
            "User-Agent": (
                "SimpleLLMChatbot/0.3 "
                "(https://github.com/softrebel/simple-llm-chatbot; "
            ),
            "Accept": "application/json",
        }
        proxies = None

        if settings.socks_proxy:
            proxies = {
                "http": settings.socks_proxy,
                "https": settings.socks_proxy,
            }

        try:
            res = requests.get(
                self.BASE_URL,
                params=params,
                headers=HEADERS,
                timeout=settings.search_timeout,
                proxies=proxies,
            )
            res.raise_for_status()

        except requests.RequestException as exc:
            raise SearchError("Wikipedia search error occured.") from exc

        try:
            data = res.json()

        except ValueError as exc:
            raise SearchError("Invalid Response from wikipedia.") from exc

        results = [
            {
                "title": item.get("title", ""),
                "snippet": item.get("snippet", ""),
                "page_id": item.get("pageid"),
            }
            for item in data.get("query", {}).get("search", [])
        ]

        return results
