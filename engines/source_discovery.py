from __future__ import annotations

from copy import deepcopy
from typing import Any


class SourceDiscovery:
    """Provides destination seed data and a graceful fallback profile."""

    def __init__(self, seed_data: dict[str, dict[str, Any]], fallback_profile: dict[str, Any]) -> None:
        self._seed_data = {key.lower(): deepcopy(value) for key, value in seed_data.items()}
        self._fallback_profile = deepcopy(fallback_profile)

    def discover(self, destination: str) -> tuple[dict[str, Any], bool]:
        normalized = destination.strip().lower()
        if normalized in self._seed_data:
            return deepcopy(self._seed_data[normalized]), True
        profile = deepcopy(self._fallback_profile)
        profile["destination"] = destination.strip().title() or "Custom Journey"
        return profile, False

    def seed_profiles(self) -> list[dict[str, Any]]:
        return [deepcopy(profile) for profile in self._seed_data.values()]

    def seed_count(self) -> int:
        return len(self._seed_data)
