import requests
import logging
from app.config import settings
from app.search.base import SearchEngine, SearchError


logger = logging.getLogger(__name__)


class WikipediaSearchEngine(SearchEngine):
    BASE_URL = "https://en.wikipedia.org/w/api.php"
    HEADERS = {
        "User-Agent": (
            "SimpleLLMChatbot/0.3 (https://github.com/softrebel/simple-llm-chatbot; "
        ),
        "Accept": "application/json",
    }

    def search(self, query: str) -> list[dict]:
        logger.info(f"Wikipedia search started | query= {query}")
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "utf8": 1,
            "srlimit": settings.search_limit,
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
                headers=self.HEADERS,
                timeout=settings.search_timeout,
                proxies=proxies,
            )
            res.raise_for_status()

        except requests.RequestException as exc:
            logger.exception(f"Wikipedia request failed | error= {exc}")
            raise SearchError("Wikipedia search error occured.") from exc

        try:
            data = res.json()

        except ValueError as exc:
            logger.exception("Invalid Response from wikipedia.")
            raise SearchError("Invalid Response from wikipedia.") from exc

        search_items = data.get("query", {}).get("search", [])

        results = []
        for item in search_items:
            page_id = item.get("pageid")
            page_details = self.fetch_page(page_id)
            results.append(page_details)

        logger.info(
            "Wikipedia search completed | results=%d",
            len(results),
        )
        return results

    def fetch_page(self, page_id: int) -> dict:
        logger.info(f"Wikipedia fetch page started | page_id= {page_id}")
        params = {
            "action": "query",
            "pageids": page_id,
            "prop": "extracts",
            "explaintext": 1,
            "exsectionformat": "plain",
            "format": "json",
            "utf8": 1,
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
                headers=self.HEADERS,
                timeout=settings.search_timeout,
                proxies=proxies,
            )
            res.raise_for_status()

        except requests.RequestException as exc:
            logger.error("Wikipedia page fetch error occurred.")
            raise SearchError("Wikipedia page fetch error occurred.") from exc

        try:
            data = res.json()

        except ValueError as exc:
            raise SearchError("Invalid response from Wikipedia.") from exc

        page = data.get("query", {}).get("pages", {}).get(str(page_id), {})

        logger.info("Wikipedia fetch page completed")
        return {
            "page_id": page.get("pageid"),
            "title": page.get("title", ""),
            "content": page.get("extract", ""),
        }
