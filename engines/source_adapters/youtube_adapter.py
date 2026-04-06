from __future__ import annotations

import json
import os
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class YouTubeAdapter:
    """Optional YouTube Data API adapter using free official search access."""

    SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

    def __init__(self, api_key: str | None = None, timeout_seconds: int = 6) -> None:
        self.api_key = api_key or os.environ.get("MINDGRID_YOUTUBE_API_KEY", "")
        self.timeout_seconds = timeout_seconds

    def is_enabled(self) -> bool:
        return bool(self.api_key)

    def search(self, *, query: str, limit: int = 2) -> list[dict[str, Any]]:
        if not self.is_enabled():
            return []

        params = urlencode(
            {
                "part": "snippet",
                "type": "video",
                "q": query,
                "maxResults": max(1, min(limit, 5)),
                "safeSearch": "moderate",
                "key": self.api_key,
            }
        )
        request = Request(
            f"{self.SEARCH_URL}?{params}",
            headers={"Accept": "application/json", "User-Agent": "MindGridVoyager/1.0"},
        )

        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except Exception:  # noqa: BLE001
            return []

        items = payload.get("items", [])
        results: list[dict[str, Any]] = []
        for item in items:
            video_id = str(item.get("id", {}).get("videoId", "")).strip()
            if not video_id:
                continue
            snippet = item.get("snippet", {})
            results.append(
                {
                    "platform": "YouTube",
                    "title": str(snippet.get("title", "YouTube result")).strip(),
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                    "publishedAt": str(snippet.get("publishedAt", "")).strip(),
                    "channelTitle": str(snippet.get("channelTitle", "")).strip(),
                    "description": str(snippet.get("description", "")).strip(),
                }
            )
        return results
