from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote_plus

from .source_adapters import RedditAdapter, YouTubeAdapter


@dataclass(slots=True)
class SocialReference:
    platform: str
    title: str
    url: str
    query: str
    reason: str
    category: str

    def as_dict(self) -> dict[str, str]:
        return {
            "platform": self.platform,
            "title": self.title,
            "url": self.url,
            "query": self.query,
            "reason": self.reason,
            "category": self.category,
        }


class SocialSignalEngine:
    """Builds compliance-friendly social references using official YouTube and Reddit surfaces."""

    VERSION = "social-signal-v1"
    YOUTUBE_SEARCH_URL = "https://www.youtube.com/results?search_query={query}"
    REDDIT_SEARCH_URL = "https://www.reddit.com/search/?q={query}&type=link"

    def __init__(
        self,
        youtube_adapter: YouTubeAdapter | None = None,
        reddit_adapter: RedditAdapter | None = None,
        live_query_budget: int = 5,
    ) -> None:
        self.youtube_adapter = youtube_adapter or YouTubeAdapter()
        self.reddit_adapter = reddit_adapter or RedditAdapter()
        self.live_query_budget = live_query_budget

    def build_bundle(
        self,
        *,
        destination: str,
        profile: dict[str, Any],
        attractions: list[dict[str, Any]],
        food: list[dict[str, Any]],
        favorites: list[dict[str, Any]],
        itinerary: list[dict[str, Any]],
    ) -> dict[str, Any]:
        destination_name = str(destination or profile.get("destination", "Destination")).strip()
        overview = self._build_overview_refs(destination_name)
        attractions_map = self._build_item_map(destination_name, attractions, category="attractions")
        food_map = self._build_item_map(destination_name, food, category="food")
        favorites_map = self._build_item_map(destination_name, favorites, category="favorites")
        itinerary_refs = self._build_itinerary_refs(destination_name, itinerary)
        bundle = {
            "version": self.VERSION,
            "policy": {
                "mode": "public-search-links-only",
                "legalNote": (
                    "This layer uses public outbound reference links and, when configured, official YouTube and Reddit "
                    "API metadata only. It does not scrape pages or mirror full third-party post content."
                ),
                "platforms": ["YouTube", "Reddit"],
                "liveRetrievalReady": self.youtube_adapter.is_enabled() or self.reddit_adapter.is_enabled(),
            },
            "overview": overview,
            "attractions": attractions_map,
            "foodAndCafes": food_map,
            "localFavorites": favorites_map,
            "itinerary": itinerary_refs,
        }
        self._enrich_with_live_results(
            bundle=bundle,
            destination=destination_name,
            attractions=attractions,
            food=food,
            favorites=favorites,
            itinerary=itinerary,
        )
        return bundle

    def attach_item_references(
        self,
        items: list[dict[str, Any]],
        *,
        references_by_name: dict[str, list[dict[str, Any]]],
    ) -> list[dict[str, Any]]:
        enriched: list[dict[str, Any]] = []
        for item in items:
            clone = deepcopy(item)
            clone["references"] = references_by_name.get(str(item.get("name", "")), [])[:2]
            enriched.append(clone)
        return enriched

    def attach_itinerary_references(
        self,
        itinerary: list[dict[str, Any]],
        *,
        itinerary_references: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        references_by_day = {
            int(item.get("day", 0)): deepcopy(item.get("references", []))
            for item in itinerary_references
        }
        enriched: list[dict[str, Any]] = []
        for day in itinerary:
            clone = deepcopy(day)
            clone["references"] = references_by_day.get(int(day.get("day", 0)), [])[:2]
            enriched.append(clone)
        return enriched

    def _build_overview_refs(self, destination: str) -> list[dict[str, Any]]:
        queries = [
            (
                "YouTube",
                f"{destination} travel guide itinerary",
                f"Watch destination walkthroughs and recent trip planning videos for {destination}.",
                "overview",
            ),
            (
                "Reddit",
                f"{destination} travel tips itinerary reddit",
                f"Read community advice and practical travel threads for {destination}.",
                "overview",
            ),
            (
                "YouTube",
                f"{destination} best cafes food guide",
                f"Review cafe and food coverage before locking in the trip food arc.",
                "food",
            ),
            (
                "Reddit",
                f"{destination} best local spots cafes reddit",
                f"Check traveler and local discussion around high-signal neighborhoods.",
                "local",
            ),
        ]
        return [self._make_reference(*entry) for entry in queries]

    def _build_item_map(
        self,
        destination: str,
        items: list[dict[str, Any]],
        *,
        category: str,
    ) -> dict[str, list[dict[str, Any]]]:
        references: dict[str, list[dict[str, Any]]] = {}
        for item in items[:3]:
            item_name = str(item.get("name", "")).strip()
            if not item_name:
                continue
            references[item_name] = [
                self._make_reference(
                    "YouTube",
                    self._youtube_query(destination, item_name, category),
                    self._youtube_reason(category, item_name),
                    category,
                ),
                self._make_reference(
                    "Reddit",
                    self._reddit_query(destination, item_name, category),
                    self._reddit_reason(category, item_name),
                    category,
                ),
            ]
        return references

    def _build_itinerary_refs(self, destination: str, itinerary: list[dict[str, Any]]) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for day in itinerary:
            day_number = int(day.get("day", 0))
            blocks = day.get("blocks", [])
            anchor_titles = [str(block.get("title", "")).strip() for block in blocks[:2] if block.get("title")]
            query_anchor = " ".join(anchor_titles) if anchor_titles else str(day.get("theme", destination))
            refs = [
                self._make_reference(
                    "YouTube",
                    f"{destination} {query_anchor} itinerary",
                    f"Watch route examples for Day {day_number} before finalizing transitions.",
                    "itinerary",
                ),
                self._make_reference(
                    "Reddit",
                    f"{destination} {query_anchor} itinerary reddit",
                    f"Check community feedback on pacing, queues, and route friction for Day {day_number}.",
                    "itinerary",
                ),
            ]
            results.append(
                {
                    "day": day_number,
                    "references": refs,
                }
            )
        return results

    def _youtube_query(self, destination: str, item_name: str, category: str) -> str:
        suffix_map = {
            "attractions": "travel guide walkthrough",
            "food": "food guide cafe review",
            "favorites": "local guide neighborhood tips",
            "itinerary": "itinerary route guide",
        }
        suffix = suffix_map.get(category, "travel guide")
        return f"{destination} {item_name} {suffix}"

    def _reddit_query(self, destination: str, item_name: str, category: str) -> str:
        suffix_map = {
            "attractions": "travel tips reddit",
            "food": "best food cafe reddit",
            "favorites": "local neighborhood reddit",
            "itinerary": "itinerary reddit",
        }
        suffix = suffix_map.get(category, "travel reddit")
        return f"{destination} {item_name} {suffix}"

    def _youtube_reason(self, category: str, item_name: str) -> str:
        if category == "food":
            return f"See recent video coverage for {item_name} before choosing the cafe or meal block."
        if category == "favorites":
            return f"Use video references to validate local atmosphere around {item_name}."
        return f"See recent travel video references for {item_name}."

    def _reddit_reason(self, category: str, item_name: str) -> str:
        if category == "food":
            return f"Read first-hand discussion on whether {item_name} still feels worth the stop."
        if category == "favorites":
            return f"Check discussion threads for local texture, timing, and crowd advice around {item_name}."
        return f"Read recent traveler discussion about {item_name}."

    def _make_reference(self, platform: str, query: str, reason: str, category: str) -> dict[str, str]:
        encoded_query = quote_plus(query)
        if platform.lower() == "youtube":
            url = self.YOUTUBE_SEARCH_URL.format(query=encoded_query)
            title = f"YouTube: {query}"
        else:
            url = self.REDDIT_SEARCH_URL.format(query=encoded_query)
            title = f"Reddit: {query}"
        return SocialReference(
            platform=platform,
            title=title,
            url=url,
            query=query,
            reason=reason,
            category=category,
        ).as_dict()

    def _enrich_with_live_results(
        self,
        *,
        bundle: dict[str, Any],
        destination: str,
        attractions: list[dict[str, Any]],
        food: list[dict[str, Any]],
        favorites: list[dict[str, Any]],
        itinerary: list[dict[str, Any]],
    ) -> None:
        if not (self.youtube_adapter.is_enabled() or self.reddit_adapter.is_enabled()):
            return

        query_plan: list[tuple[str, str, str, str]] = [
            ("overview", "", f"{destination} travel guide itinerary", "overview"),
        ]
        if attractions:
            query_plan.append(("attractions", str(attractions[0].get("name", "")), f"{destination} {attractions[0].get('name', '')} travel guide", "attractions"))
        if food:
            query_plan.append(("foodAndCafes", str(food[0].get("name", "")), f"{destination} {food[0].get('name', '')} food guide", "food"))
        if favorites:
            query_plan.append(("localFavorites", str(favorites[0].get("name", "")), f"{destination} {favorites[0].get('name', '')} local guide", "favorites"))
        if itinerary:
            first_day = itinerary[0]
            anchor_titles = [str(block.get("title", "")).strip() for block in first_day.get("blocks", [])[:2] if block.get("title")]
            anchor_query = " ".join(anchor_titles) if anchor_titles else str(first_day.get("theme", destination))
            query_plan.append(("itinerary", str(first_day.get("day", 1)), f"{destination} {anchor_query} itinerary", "itinerary"))

        for index, (bucket, key, query, category) in enumerate(query_plan[: self.live_query_budget]):
            live_refs = self._fetch_live_references(query=query, category=category)
            if not live_refs:
                continue
            if bucket == "overview":
                bundle["overview"] = self._merge_live_refs(live_refs, bundle["overview"])
            elif bucket == "itinerary":
                for day in bundle["itinerary"]:
                    if str(day.get("day", "")) == key:
                        day["references"] = self._merge_live_refs(live_refs, day.get("references", []))
                        break
            else:
                bucket_map = bundle.get(bucket, {})
                if key in bucket_map:
                    bucket_map[key] = self._merge_live_refs(live_refs, bucket_map[key])

    def _fetch_live_references(self, *, query: str, category: str) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for item in self.youtube_adapter.search(query=query, limit=1):
            results.append(
                {
                    "platform": item["platform"],
                    "title": item["title"],
                    "url": item["url"],
                    "query": query,
                    "reason": "Live YouTube metadata retrieved through the official search endpoint.",
                    "category": category,
                }
            )
        for item in self.reddit_adapter.search(query=query, limit=1):
            results.append(
                {
                    "platform": item["platform"],
                    "title": item["title"],
                    "url": item["url"],
                    "query": query,
                    "reason": "Live Reddit public metadata retrieved from the official JSON search endpoint.",
                    "category": category,
                }
            )
        return results

    def _merge_live_refs(self, live_refs: list[dict[str, Any]], fallback_refs: list[dict[str, Any]]) -> list[dict[str, Any]]:
        merged: list[dict[str, Any]] = []
        seen_urls: set[str] = set()
        for item in [*live_refs, *fallback_refs]:
            url = str(item.get("url", "")).strip()
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            merged.append(item)
        return merged[:3]
