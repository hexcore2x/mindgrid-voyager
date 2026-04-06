from __future__ import annotations

import json
import os
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class RedditAdapter:
    """Optional Reddit public JSON search adapter with graceful fallback."""

    SEARCH_URL = "https://www.reddit.com/search.json"

    def __init__(self, timeout_seconds: int = 6, enabled: bool | None = None) -> None:
        self.timeout_seconds = timeout_seconds
        self.enabled = (
            enabled
            if enabled is not None
            else str(os.environ.get("MINDGRID_ENABLE_LIVE_REDDIT", "")).strip().lower() in {"1", "true", "yes"}
        )

    def is_enabled(self) -> bool:
        return self.enabled

    def search(self, *, query: str, limit: int = 2) -> list[dict[str, Any]]:
        if not self.is_enabled():
            return []
        params = urlencode(
            {
                "q": query,
                "sort": "relevance",
                "limit": max(1, min(limit, 5)),
                "raw_json": 1,
                "include_over_18": "off",
            }
        )
        request = Request(
            f"{self.SEARCH_URL}?{params}",
            headers={
                "Accept": "application/json",
                "User-Agent": "MindGridVoyager/1.0 (public metadata only)",
            },
        )

        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except Exception:  # noqa: BLE001
            return []

        children = payload.get("data", {}).get("children", [])
        results: list[dict[str, Any]] = []
        for child in children:
            data = child.get("data", {})
            permalink = str(data.get("permalink", "")).strip()
            if not permalink:
                continue
            results.append(
                {
                    "platform": "Reddit",
                    "title": str(data.get("title", "Reddit discussion")).strip(),
                    "url": f"https://www.reddit.com{permalink}",
                    "publishedAt": str(data.get("created_utc", "")).strip(),
                    "subreddit": str(data.get("subreddit", "")).strip(),
                    "selftext": str(data.get("selftext", "")).strip(),
                    "author": str(data.get("author", "")).strip(),
                }
            )
        return results
