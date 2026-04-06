from __future__ import annotations

from typing import Any


class RiskAnalyzer:
    """Produces lightweight destination and pace-aware safety guidance."""

    def analyze(self, profile: dict[str, Any], pace: str, budget_per_day: float) -> dict[str, Any]:
        base_level = profile.get("riskLevel", "Moderate awareness")
        notes = list(profile.get("safetyNotes", []))
        transport = profile.get("transportNote", "Keep one familiar return route saved offline.")

        if pace == "fast":
            notes.append("A faster pace can increase transition fatigue, so keep one recovery block each day.")
        elif pace == "slow":
            notes.append("Use the slower pace to avoid unnecessary late-night transfers and queue stress.")

        if budget_per_day < 100:
            notes.append("Budget-focused plans should prioritize well-lit transit corridors after dark.")
        elif budget_per_day > 250:
            notes.append("Premium dining or rooftop plans may require reservations to avoid last-minute route changes.")

        return {
            "riskLevel": base_level,
            "transportNote": transport,
            "notes": notes[:5],
            "confidence": profile.get("safetyConfidence", 82),
        }
