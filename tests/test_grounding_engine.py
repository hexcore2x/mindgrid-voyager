from __future__ import annotations

from pathlib import Path

from engines.evidence_cache import LiveEvidenceCache
from engines.grounding_engine import GroundingEngine


class StubYouTubeAdapter:
    def is_enabled(self) -> bool:
        return True

    def search(self, *, query: str, limit: int = 2) -> list[dict[str, str]]:
        return [
            {
                "platform": "YouTube",
                "title": "Tokyo cafe route video",
                "url": "https://www.youtube.com/watch?v=test-video",
                "publishedAt": "2026-03-20T12:00:00Z",
                "channelTitle": "City Walks Lab",
                "description": (
                    "This walk covers Kiyosumi-Shirakawa coffee stops, an early bakery window, and a slow riverfront "
                    "loop that works well for a balanced Tokyo cafe day."
                ),
            }
        ][:limit]


class StubRedditAdapter:
    def is_enabled(self) -> bool:
        return True

    def search(self, *, query: str, limit: int = 2) -> list[dict[str, str]]:
        return [
            {
                "platform": "Reddit",
                "title": "Tokyo cafe pacing advice",
                "url": "https://www.reddit.com/r/JapanTravel/comments/test-thread",
                "publishedAt": "1710931200",
                "subreddit": "JapanTravel",
                "author": "traveler_01",
                "selftext": (
                    "We had the best results clustering Kiyosumi-Shirakawa cafes with one museum stop instead of "
                    "jumping across the city. The slower pacing kept the day relaxed."
                ),
            }
        ][:limit]


def test_grounding_engine_uses_official_api_snippets_as_passages(tmp_path: Path) -> None:
    engine = GroundingEngine(
        evidence_cache=LiveEvidenceCache(cache_path=tmp_path / "live_evidence_cache.json"),
        youtube_adapter=StubYouTubeAdapter(),
        reddit_adapter=StubRedditAdapter(),
        live_query_budget=2,
    )

    result = engine.retrieve(
        destination="Tokyo",
        interests=["food", "cafe", "walkable"],
        travel_style="Balanced Explorer",
        pace="balanced",
        ranked_attractions=[{"name": "Asakusa and Senso-ji", "tags": ["culture", "walkable"]}],
        ranked_food=[{"name": "Koffee Mameya Kakeru", "tags": ["cafe", "coffee"]}],
        ranked_favorites=[{"name": "Kiyosumi-Shirakawa cafe pocket", "tags": ["cafe", "local"]}],
    )

    assert result["method"] == "hybrid-live-cached-retrieval"
    assert result["contentGroundingMode"] == "hybrid-official-snippets-and-seeded-passages"
    assert result["metrics"]["contentGroundedDocuments"] >= 1

    live_evidence = [
        item for item in result["destinationEvidence"] if str(item.get("sourceType", "")).startswith("live-")
    ]
    assert live_evidence
    assert any(item["contentGrounded"] is True for item in live_evidence)
    assert any(item["contentMode"] == "official-api-snippet" for item in live_evidence)
    assert any("Kiyosumi-Shirakawa" in item["excerpt"] for item in live_evidence)
    assert any(item["legalBasis"] == "official-public-api-short-snippet" for item in live_evidence)
