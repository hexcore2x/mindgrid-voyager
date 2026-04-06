from __future__ import annotations

import hashlib
import re
from datetime import UTC, datetime
from typing import Any

from .evidence_cache import LiveEvidenceCache
from .grounding_corpus import GROUNDING_CORPUS
from .source_adapters import RedditAdapter, YouTubeAdapter


TOKEN_RE = re.compile(r"[a-z0-9]+")


class GroundingEngine:
    """Retrieves hybrid passage-grounded evidence with graceful offline fallback."""

    VERSION = "grounding-engine-v3-passage-grounded"

    def __init__(
        self,
        corpus: dict[str, list[dict[str, Any]]] | None = None,
        evidence_cache: LiveEvidenceCache | None = None,
        youtube_adapter: YouTubeAdapter | None = None,
        reddit_adapter: RedditAdapter | None = None,
        live_query_budget: int = 4,
    ) -> None:
        self.corpus = corpus or GROUNDING_CORPUS
        self.evidence_cache = evidence_cache or LiveEvidenceCache()
        self.youtube_adapter = youtube_adapter or YouTubeAdapter()
        self.reddit_adapter = reddit_adapter or RedditAdapter()
        self.live_query_budget = live_query_budget

    def retrieve(
        self,
        *,
        destination: str,
        interests: list[str],
        travel_style: str,
        pace: str,
        ranked_attractions: list[dict[str, Any]],
        ranked_food: list[dict[str, Any]],
        ranked_favorites: list[dict[str, Any]],
    ) -> dict[str, Any]:
        seeded_docs = self._documents_for(destination)
        live_docs = self._live_documents_for(
            destination=destination,
            interests=interests,
            travel_style=travel_style,
            pace=pace,
            ranked_attractions=ranked_attractions,
            ranked_food=ranked_food,
            ranked_favorites=ranked_favorites,
        )
        docs = self._dedupe_documents([*live_docs, *seeded_docs])
        destination_query = " ".join([destination, travel_style, pace, *interests])
        destination_evidence = self._rank_documents(docs, destination_query, [], limit=4)

        attraction_map = self._rank_item_bucket(destination, docs, ranked_attractions, limit=2)
        food_map = self._rank_item_bucket(destination, docs, ranked_food, limit=2)
        favorite_map = self._rank_item_bucket(destination, docs, ranked_favorites, limit=2)

        all_selected = [
            *destination_evidence,
            *[item for values in attraction_map.values() for item in values],
            *[item for values in food_map.values() for item in values],
            *[item for values in favorite_map.values() for item in values],
        ]
        unique_selected = self._dedupe_by_id(all_selected)

        average_trust = round(
            sum(float(item.get("trust", 0)) for item in unique_selected) / max(len(unique_selected), 1),
            3,
        )
        average_recency_days = round(
            sum(float(item.get("recencyDays", 365)) for item in unique_selected) / max(len(unique_selected), 1),
            2,
        )
        coverage_score = round(min(99.0, 58 + len(unique_selected) * 4.8 + average_trust * 18), 2)
        trust_score = round(min(99.0, average_trust * 100), 2)
        recency_score = round(max(35.0, min(99.0, 100 - (average_recency_days / 8))), 2)
        retrieval_mode = "hybrid-live-cached-retrieval" if live_docs else "seeded-evidence-retrieval"

        return {
            "version": self.VERSION,
            "method": retrieval_mode,
            "contentGroundingMode": "hybrid-official-snippets-and-seeded-passages" if live_docs else "seeded-passages",
            "destinationEvidence": destination_evidence,
            "itemEvidence": {
                "attractions": attraction_map,
                "foodAndCafes": food_map,
                "localFavorites": favorite_map,
            },
            "metrics": {
                "coverageScore": coverage_score,
                "trustScore": trust_score,
                "recencyScore": recency_score,
                "averageTrust": average_trust,
                "averageRecencyDays": average_recency_days,
                "documentsUsed": len(unique_selected),
                "contentGroundedDocuments": sum(1 for item in unique_selected if item.get("contentGrounded")),
                "metadataOnlyDocuments": sum(1 for item in unique_selected if not item.get("contentGrounded")),
                "seededDocumentsAvailable": len(seeded_docs),
                "liveDocumentsAvailable": len(live_docs),
                "liveRefreshEnabled": self.youtube_adapter.is_enabled() or self.reddit_adapter.is_enabled(),
            },
            "retrieval": {
                "cache": self.evidence_cache.summary(destination),
                "liveRefreshEnabled": self.youtube_adapter.is_enabled() or self.reddit_adapter.is_enabled(),
                "sourceAdapters": {
                    "youtube": self.youtube_adapter.is_enabled(),
                    "reddit": self.reddit_adapter.is_enabled(),
                },
                "contentPolicy": {
                    "mode": "seeded-passages-plus-official-api-snippets",
                    "legalNote": (
                        "Grounding uses curated local passages and short attributed snippets returned by official "
                        "YouTube and Reddit endpoints when enabled. It does not scrape pages or mirror full posts."
                    ),
                },
            },
        }

    def _rank_item_bucket(
        self,
        destination: str,
        docs: list[dict[str, Any]],
        items: list[dict[str, Any]],
        *,
        limit: int,
    ) -> dict[str, list[dict[str, Any]]]:
        ranked: dict[str, list[dict[str, Any]]] = {}
        for item in items[:3]:
            name = str(item.get("name", "")).strip()
            if not name:
                continue
            query = f"{destination} {name} {' '.join(item.get('tags', []))}"
            ranked[name] = self._rank_documents(docs, query, item.get("tags", []), limit=limit)
        return ranked

    def _rank_documents(
        self,
        docs: list[dict[str, Any]],
        query: str,
        item_tags: list[str],
        *,
        limit: int,
    ) -> list[dict[str, Any]]:
        query_tokens = self._tokenize(query)
        tag_tokens = {str(tag).strip().lower() for tag in item_tags if str(tag).strip()}
        scored: list[tuple[float, dict[str, Any]]] = []

        for doc in docs:
            doc_tokens = self._tokenize(str(doc.get("text", "")))
            tag_overlap = len(tag_tokens.intersection({str(tag).lower() for tag in doc.get("tags", [])}))
            text_overlap = len(query_tokens.intersection(doc_tokens))
            entity_bonus = self._entity_bonus(query, doc.get("entities", []))
            trust = float(doc.get("trust", 0.7))
            recency_days = self._recency_days(str(doc.get("published", "")))
            recency_score = max(0.2, 1 - (recency_days / 730))
            lexical_score = text_overlap * 7 + tag_overlap * 9 + entity_bonus * 14
            final_score = lexical_score + (trust * 28) + (recency_score * 18)

            if final_score <= 0:
                continue

            scored.append(
                (
                    final_score,
                    {
                        "id": doc.get("id"),
                        "title": str(doc.get("sourceName", "Evidence")).strip(),
                        "sourceType": str(doc.get("sourceType", "seeded")).strip(),
                        "url": str(doc.get("url", "")).strip(),
                        "excerpt": str(doc.get("text", "")).strip(),
                        "trust": round(trust, 3),
                        "recencyDays": round(recency_days, 2),
                        "score": round(final_score, 2),
                        "groundedClaim": self._grounded_claim(str(doc.get("text", "")).strip()),
                        "contentGrounded": bool(doc.get("contentGrounded", bool(str(doc.get("text", "")).strip()))),
                        "contentMode": str(doc.get("contentMode", "seeded-passage")).strip(),
                        "attribution": str(doc.get("attribution", "")).strip(),
                        "legalBasis": str(doc.get("legalBasis", "curated-local-passage")).strip(),
                    },
                )
            )

        scored.sort(key=lambda item: item[0], reverse=True)
        return [item[1] for item in scored[:limit]]

    def _documents_for(self, destination: str) -> list[dict[str, Any]]:
        slug = str(destination or "").strip().lower()
        docs = self.corpus.get(slug) or self.corpus.get("fallback", [])
        normalized_docs: list[dict[str, Any]] = []
        for item in docs:
            clone = dict(item)
            clone.setdefault("contentGrounded", bool(str(clone.get("text", "")).strip()))
            clone.setdefault("contentMode", "seeded-passage")
            clone.setdefault("legalBasis", "curated-local-passage")
            clone.setdefault("attribution", str(clone.get("sourceName", "Seeded evidence")).strip())
            normalized_docs.append(clone)
        return normalized_docs

    def _live_documents_for(
        self,
        *,
        destination: str,
        interests: list[str],
        travel_style: str,
        pace: str,
        ranked_attractions: list[dict[str, Any]],
        ranked_food: list[dict[str, Any]],
        ranked_favorites: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        cached_docs = self.evidence_cache.get(destination)
        should_refresh = (
            (self.youtube_adapter.is_enabled() or self.reddit_adapter.is_enabled())
            and self.evidence_cache.needs_refresh(destination)
        )
        if should_refresh:
            live_docs = self._fetch_live_documents(
                destination=destination,
                interests=interests,
                travel_style=travel_style,
                pace=pace,
                ranked_attractions=ranked_attractions,
                ranked_food=ranked_food,
                ranked_favorites=ranked_favorites,
            )
            if live_docs:
                cached_docs = self.evidence_cache.upsert(destination, live_docs)
        return cached_docs

    def _fetch_live_documents(
        self,
        *,
        destination: str,
        interests: list[str],
        travel_style: str,
        pace: str,
        ranked_attractions: list[dict[str, Any]],
        ranked_food: list[dict[str, Any]],
        ranked_favorites: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        queries = [
            f"{destination} travel guide {travel_style} {pace}",
            f"{destination} {' '.join(interests[:3])} itinerary",
        ]
        for bucket in (ranked_attractions, ranked_food, ranked_favorites):
            if bucket:
                queries.append(f"{destination} {bucket[0].get('name', '')} guide")

        live_docs: list[dict[str, Any]] = []
        for query in list(dict.fromkeys(queries))[: self.live_query_budget]:
            live_docs.extend(self._search_youtube(query, destination))
            live_docs.extend(self._search_reddit(query, destination))
        return self._dedupe_documents(live_docs)

    def _search_youtube(self, query: str, destination: str) -> list[dict[str, Any]]:
        documents: list[dict[str, Any]] = []
        for item in self.youtube_adapter.search(query=query, limit=2):
            documents.append(
                self._live_doc_from_result(
                    destination=destination,
                    query=query,
                    platform="youtube",
                    title=str(item.get("title", "YouTube travel reference")).strip(),
                    url=str(item.get("url", "")).strip(),
                    published=str(item.get("publishedAt", "")).strip(),
                    trust=0.84,
                    excerpt=str(item.get("description", "")).strip(),
                    attribution=str(item.get("channelTitle", "")).strip() or "YouTube creator",
                )
            )
        return documents

    def _search_reddit(self, query: str, destination: str) -> list[dict[str, Any]]:
        documents: list[dict[str, Any]] = []
        for item in self.reddit_adapter.search(query=query, limit=2):
            documents.append(
                self._live_doc_from_result(
                    destination=destination,
                    query=query,
                    platform="reddit",
                    title=str(item.get("title", "Reddit travel discussion")).strip(),
                    url=str(item.get("url", "")).strip(),
                    published=self._normalize_published(str(item.get("publishedAt", "")).strip()),
                    trust=0.76,
                    excerpt=str(item.get("selftext", "")).strip(),
                    attribution=(
                        f"r/{str(item.get('subreddit', '')).strip()}" if str(item.get("subreddit", "")).strip() else "Reddit thread"
                    ),
                )
            )
        return documents

    def _live_doc_from_result(
        self,
        *,
        destination: str,
        query: str,
        platform: str,
        title: str,
        url: str,
        published: str,
        trust: float,
        excerpt: str,
        attribution: str,
    ) -> dict[str, Any]:
        doc_id = hashlib.sha1(f"{platform}|{url}|{query}".encode("utf-8")).hexdigest()[:14]
        query_tokens = sorted(self._tokenize(query))
        sanitized_excerpt = self._sanitize_excerpt(excerpt)
        content_grounded = bool(sanitized_excerpt)
        evidence_text = (
            sanitized_excerpt
            if sanitized_excerpt
            else f"{title}. Retrieved as live public metadata for {destination} using the query '{query}'."
        )
        return {
            "id": f"{platform}-{doc_id}",
            "sourceName": title or f"{platform.title()} travel reference",
            "sourceType": f"live-{platform}",
            "url": url,
            "published": published or datetime.now(UTC).date().isoformat(),
            "trust": trust,
            "text": evidence_text,
            "tags": query_tokens[:8],
            "entities": [destination, *query.split()[:4]],
            "retrievedAt": datetime.now(UTC).isoformat(),
            "retrievalMode": "live-official-api-search",
            "contentGrounded": content_grounded,
            "contentMode": "official-api-snippet" if content_grounded else "official-api-metadata",
            "attribution": attribution or platform.title(),
            "legalBasis": "official-public-api-short-snippet" if content_grounded else "official-public-api-metadata",
        }

    def _normalize_published(self, value: str) -> str:
        if not value:
            return ""
        if value.isdigit():
            return datetime.fromtimestamp(int(value), tz=UTC).date().isoformat()
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()
        except ValueError:
            return value

    def _tokenize(self, value: str) -> set[str]:
        return {match.group(0) for match in TOKEN_RE.finditer(value.lower())}

    def _entity_bonus(self, query: str, entities: list[Any]) -> int:
        query_lower = query.lower()
        bonus = 0
        for entity in entities:
            normalized = str(entity).strip().lower()
            if normalized and normalized in query_lower:
                bonus += 1
        return bonus

    def _recency_days(self, published_value: str) -> float:
        try:
            published = datetime.fromisoformat(published_value).replace(tzinfo=UTC)
        except ValueError:
            return 365.0
        delta = datetime.now(UTC) - published
        return max(1.0, delta.total_seconds() / 86400)

    def _grounded_claim(self, text: str) -> str:
        if not text:
            return "Grounded evidence unavailable."
        sentence = text.split(".")[0].strip()
        return sentence + ("." if not sentence.endswith(".") else "")

    def _sanitize_excerpt(self, value: str, max_length: int = 220) -> str:
        normalized = " ".join(str(value or "").split())
        if not normalized:
            return ""
        clipped = normalized[:max_length].rsplit(" ", 1)[0] if len(normalized) > max_length else normalized
        clipped = clipped.strip(" .,-")
        return clipped + ("..." if len(normalized) > max_length else "")

    def _dedupe_by_id(self, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        seen: set[str] = set()
        unique: list[dict[str, Any]] = []
        for item in items:
            item_id = str(item.get("id", "")).strip()
            if not item_id or item_id in seen:
                continue
            seen.add(item_id)
            unique.append(item)
        return unique

    def _dedupe_documents(self, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        seen: set[str] = set()
        unique: list[dict[str, Any]] = []
        for item in items:
            key = str(item.get("url") or item.get("id") or "").strip()
            if not key or key in seen:
                continue
            seen.add(key)
            unique.append(item)
        return unique
