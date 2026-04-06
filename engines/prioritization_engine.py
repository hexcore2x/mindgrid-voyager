from __future__ import annotations

from typing import Any


class PrioritizationEngine:
    """Ranks candidate experiences with lightweight explainable scoring."""

    INTEREST_BONUS = 16
    STYLE_BONUS = 11

    def score_item(
        self,
        item: dict[str, Any],
        interests: list[str],
        travel_style: str,
        pace: str,
        budget_per_day: float,
    ) -> int:
        tags = [tag.lower() for tag in item.get("tags", [])]
        budget_band = item.get("budgetBand", "mid")
        score = 50

        for interest in interests:
            if interest in tags:
                score += self.INTEREST_BONUS

        if travel_style and travel_style.lower() in tags:
            score += self.STYLE_BONUS

        if pace == "slow" and "relaxed" in tags:
            score += 8
        elif pace == "fast" and "high-energy" in tags:
            score += 8
        elif pace == "balanced":
            score += 5

        if budget_per_day <= 120 and budget_band == "budget":
            score += 10
        elif 120 < budget_per_day <= 240 and budget_band == "mid":
            score += 10
        elif budget_per_day > 240 and budget_band == "premium":
            score += 10

        if item.get("indoor") and "rainy-day" in tags:
            score += 4

        return score

    def rank_items(
        self,
        items: list[dict[str, Any]],
        interests: list[str],
        travel_style: str,
        pace: str,
        budget_per_day: float,
        limit: int,
    ) -> list[dict[str, Any]]:
        scored_items = sorted(
            items,
            key=lambda item: self.score_item(item, interests, travel_style, pace, budget_per_day),
            reverse=True,
        )
        return scored_items[:limit]
