from __future__ import annotations

import re
from statistics import mean
from typing import Any


TOKEN_RE = re.compile(r"[a-z0-9]+")


class FeatureEngineeringEngine:
    """Builds request-to-destination features for the ranking model."""

    VERSION = "feature-engineering-v1"

    TOKEN_SYNONYMS: dict[str, set[str]] = {
        "food": {"food", "cafe", "coffee", "market", "hawker", "bistro", "seafood", "dining", "izakaya"},
        "culture": {"culture", "history", "heritage", "museum", "art", "temple", "shrine", "ritual"},
        "walkable": {"walkable", "walk", "stroll", "district", "neighborhood", "backstreets", "promenade"},
        "design": {"design", "creative", "architecture", "fashion", "gallery", "retail"},
        "scenic": {"scenic", "sunset", "waterfront", "view", "river", "coastline", "beach", "cliff", "skyline"},
        "wellness": {"wellness", "slow", "calm", "relaxed", "sunrise", "spa", "reset"},
        "nightlife": {"nightlife", "social", "rooftop", "late", "high", "energy", "cocktail", "bar"},
        "safe": {"safe", "safety", "solo", "trust", "reliable", "low", "risk"},
        "budget": {"budget", "value", "cheap", "saver", "affordable"},
        "premium": {"premium", "luxury", "comfort", "iconic", "polished", "hospitality"},
        "technology": {"technology", "tech", "immersive", "innovation", "digital"},
        "beach": {"beach", "coastline", "shore", "surf", "island"},
        "local": {"local", "community", "resident", "texture", "favorite"},
        "efficient": {"efficient", "logistics", "precision", "mrt", "rail", "metro", "transit"},
        "balanced": {"balanced", "versatile", "mix", "variety"},
    }

    TRAVEL_STYLE_HINTS: dict[str, set[str]] = {
        "food scout": {"food", "local", "market", "cafe"},
        "balanced explorer": {"balanced", "local"},
        "budget hunter": {"budget", "value", "efficient"},
        "culture first": {"culture", "art", "cafe"},
        "luxury escape": {"premium", "comfort", "iconic", "scenic"},
    }

    def build(
        self,
        *,
        request: dict[str, Any],
        profile: dict[str, Any],
        budget_per_day: float,
        attraction_scores: list[dict[str, Any]],
        food_scores: list[dict[str, Any]],
        favorite_scores: list[dict[str, Any]],
        grounding_metrics: dict[str, Any],
    ) -> dict[str, Any]:
        request_tokens = self._request_tokens(request)
        profile_tokens = self._profile_tokens(profile, attraction_scores, food_scores, favorite_scores)
        best_for_tokens = self._best_for_tokens(profile)
        style_tokens = self._style_tokens(request)
        pace_targets = self._pace_targets(str(request.get("pace", "balanced")).lower())

        interest_alignment = self._overlap_score(request_tokens["interest"], profile_tokens)
        best_for_alignment = self._overlap_score(request_tokens["interest"].union(style_tokens), best_for_tokens)
        style_alignment = self._overlap_score(style_tokens, profile_tokens)
        pace_alignment = self._overlap_score(pace_targets, profile_tokens)
        budget_realism = self._budget_realism(profile, budget_per_day)

        matched_interest_tokens = sorted(request_tokens["interest"].intersection(profile_tokens))
        missing_interest_tokens = sorted(request_tokens["interest"].difference(profile_tokens))
        matched_style_tokens = sorted(style_tokens.intersection(profile_tokens))

        coverage = float(grounding_metrics.get("coverageScore", 0))
        trust = float(grounding_metrics.get("trustScore", 0))
        evidence_support = round(min(99.0, mean([coverage, trust, interest_alignment])), 2)

        return {
            "version": self.VERSION,
            "features": {
                "intent_alignment": interest_alignment,
                "best_for_alignment": best_for_alignment,
                "style_alignment": style_alignment,
                "pace_alignment": pace_alignment,
                "budget_realism": budget_realism,
                "evidence_support": evidence_support,
            },
            "diagnostics": {
                "matchedInterestTokens": matched_interest_tokens[:8],
                "missingInterestTokens": missing_interest_tokens[:8],
                "matchedStyleTokens": matched_style_tokens[:8],
                "requestIntentTokens": sorted(request_tokens["interest"])[:12],
                "profileIntentTokens": sorted(profile_tokens)[:18],
            },
        }

    def _request_tokens(self, request: dict[str, Any]) -> dict[str, set[str]]:
        interest_tokens: set[str] = set()
        interests = request.get("interests", [])
        if isinstance(interests, str):
            interests = [item.strip() for item in interests.split(",") if item.strip()]
        for interest in interests:
            interest_tokens.update(self._canonicalize(str(interest)))

        return {
            "interest": interest_tokens,
        }

    def _profile_tokens(
        self,
        profile: dict[str, Any],
        attraction_scores: list[dict[str, Any]],
        food_scores: list[dict[str, Any]],
        favorite_scores: list[dict[str, Any]],
    ) -> set[str]:
        values: list[str] = []
        for key in ("signals", "bestFor", "styleIndicators"):
            raw = profile.get(key, [])
            if isinstance(raw, list):
                values.extend(str(item) for item in raw)
            else:
                values.append(str(raw))

        tokens: set[str] = set()
        for value in values:
            tokens.update(self._canonicalize(value))
        return tokens

    def _best_for_tokens(self, profile: dict[str, Any]) -> set[str]:
        values: list[str] = []
        for key in ("bestFor", "styleIndicators"):
            raw = profile.get(key, [])
            if isinstance(raw, list):
                values.extend(str(item) for item in raw)
            else:
                values.append(str(raw))

        tokens: set[str] = set()
        for value in values:
            tokens.update(self._canonicalize(value))
        return tokens

    def _style_tokens(self, request: dict[str, Any]) -> set[str]:
        travel_style = str(request.get("travelStyle", "")).strip().lower()
        base = set(self.TRAVEL_STYLE_HINTS.get(travel_style, set()))
        base.update(self._canonicalize(travel_style))
        return base

    def _pace_targets(self, pace: str) -> set[str]:
        if pace == "slow":
            return {"relaxed", "wellness", "scenic", "calm", "walkable"}
        if pace == "fast":
            return {"efficient", "high", "energy", "iconic", "logistics"}
        return {"balanced", "mix", "versatile", "walkable"}

    def _canonicalize(self, value: str) -> set[str]:
        raw_tokens = {match.group(0) for match in TOKEN_RE.finditer(value.lower())}
        canonical_tokens: set[str] = set()
        for canonical, variants in self.TOKEN_SYNONYMS.items():
            if raw_tokens.intersection(variants | {canonical}):
                canonical_tokens.add(canonical)
        if not canonical_tokens:
            canonical_tokens.update(token for token in raw_tokens if len(token) > 4)
        return canonical_tokens

    def _overlap_score(self, query_tokens: set[str], profile_tokens: set[str]) -> float:
        if not query_tokens:
            return 72.0
        overlap = len(query_tokens.intersection(profile_tokens))
        ratio = overlap / max(len(query_tokens), 1)
        return round(min(99.0, 36 + ratio * 58 + min(overlap, 4) * 1.5), 2)

    def _budget_realism(self, profile: dict[str, Any], budget_per_day: float) -> float:
        value_window = str(profile.get("budgetIndicators", {}).get("valueWindow", "")).strip()
        low, high = self._parse_budget_window(value_window)
        if low is None or high is None:
            average_cost = self._average_seed_cost(profile)
            if average_cost <= 18:
                low, high = 80.0, 180.0
            elif average_cost <= 28:
                low, high = 120.0, 260.0
            else:
                low, high = 180.0, 360.0

        if low <= budget_per_day <= high:
            return 96.0
        if budget_per_day < low:
            gap = low - budget_per_day
            return round(max(48.0, 92.0 - gap * 0.18), 2)
        gap = budget_per_day - high
        return round(max(58.0, 94.0 - gap * 0.08), 2)

    def _parse_budget_window(self, value: str) -> tuple[float | None, float | None]:
        numbers = [float(item) for item in re.findall(r"\d+(?:\.\d+)?", value)]
        if len(numbers) >= 2:
            return numbers[0], numbers[1]
        return None, None

    def _average_seed_cost(self, profile: dict[str, Any]) -> float:
        values: list[float] = []
        for key in ("attractions", "food", "favorites"):
            for item in profile.get(key, []):
                values.append(float(item.get("estimatedCost", 0)))
        return mean(values) if values else 20.0
