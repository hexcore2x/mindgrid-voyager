from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CACHE_PATH = ROOT / "data" / "live_evidence_cache.json"


class LiveEvidenceCache:
    """Stores small cached evidence snapshots from free public-source retrieval."""

    def __init__(self, cache_path: Path | None = None) -> None:
        self.cache_path = cache_path or CACHE_PATH
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.cache_path.exists():
            self.cache_path.write_text("{}\n", encoding="utf-8")

    def get(self, destination: str) -> list[dict[str, Any]]:
        payload = self._load()
        bucket = payload.get(self._slug(destination), [])
        if not isinstance(bucket, list):
            return []
        return [dict(item) for item in bucket if isinstance(item, dict)]

    def upsert(self, destination: str, records: list[dict[str, Any]], *, limit: int = 30) -> list[dict[str, Any]]:
        slug = self._slug(destination)
        payload = self._load()
        existing = payload.get(slug, [])
        if not isinstance(existing, list):
            existing = []

        merged: list[dict[str, Any]] = []
        seen_keys: set[str] = set()
        for item in [*records, *existing]:
            if not isinstance(item, dict):
                continue
            key = str(item.get("url") or item.get("id") or "").strip()
            if not key or key in seen_keys:
                continue
            seen_keys.add(key)
            merged.append(item)

        merged.sort(
            key=lambda item: str(item.get("retrievedAt") or item.get("published") or ""),
            reverse=True,
        )
        payload[slug] = merged[:limit]
        self._save(payload)
        return [dict(item) for item in payload[slug]]

    def needs_refresh(
        self,
        destination: str,
        *,
        max_age_hours: int = 72,
        min_records: int = 4,
    ) -> bool:
        records = self.get(destination)
        if len(records) < min_records:
            return True

        newest = records[0]
        timestamp = str(newest.get("retrievedAt", "")).strip()
        if not timestamp:
            return True
        try:
            retrieved_at = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError:
            return True
        return datetime.now(UTC) - retrieved_at > timedelta(hours=max_age_hours)

    def summary(self, destination: str) -> dict[str, Any]:
        records = self.get(destination)
        live_sources = sorted(
            {
                str(item.get("sourceType", "")).strip()
                for item in records
                if str(item.get("retrievalMode", "")).strip().startswith("live")
            }
        )
        return {
            "cachedDocumentCount": len(records),
            "liveSourceTypes": live_sources,
            "hasCache": bool(records),
            "cachePath": str(self.cache_path),
        }

    def _slug(self, destination: str) -> str:
        return str(destination or "").strip().lower()

    def _load(self) -> dict[str, Any]:
        try:
            payload = json.loads(self.cache_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}
        return payload if isinstance(payload, dict) else {}

    def _save(self, payload: dict[str, Any]) -> None:
        self.cache_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
