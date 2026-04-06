from __future__ import annotations

from typing import Any


class ItineraryPlanner:
    """Builds an explainable day-by-day plan from ranked experiences."""

    def build(
        self,
        duration: int,
        attractions: list[dict[str, Any]],
        food: list[dict[str, Any]],
        favorites: list[dict[str, Any]],
        pace: str,
    ) -> list[dict[str, Any]]:
        itinerary: list[dict[str, Any]] = []
        activity_count = {"slow": 2, "balanced": 3, "fast": 4}.get(pace, 3)

        for day_index in range(duration):
            day_number = day_index + 1
            attraction = attractions[day_index % len(attractions)] if attractions else {}
            lunch = food[day_index % len(food)] if food else {}
            evening = favorites[day_index % len(favorites)] if favorites else attraction

            blocks = [
                {
                    "time": "Morning",
                    "title": attraction.get("name", "Neighborhood orientation walk"),
                    "description": attraction.get(
                        "why",
                        "Start the day with a grounded introduction to the destination.",
                    ),
                },
                {
                    "time": "Afternoon",
                    "title": lunch.get("name", "Local lunch discovery"),
                    "description": lunch.get(
                        "why",
                        "Use lunch as a cultural anchor while staying close to the main route.",
                    ),
                },
                {
                    "time": "Evening",
                    "title": evening.get("name", "Evening local favorite"),
                    "description": evening.get(
                        "why",
                        "Close the day with a low-friction, high-signal local experience.",
                    ),
                },
            ]

            if activity_count == 4 and favorites:
                extra = favorites[(day_index + 1) % len(favorites)]
                blocks.insert(
                    2,
                    {
                        "time": "Late Afternoon",
                        "title": extra.get("name", "Flexible exploration block"),
                        "description": extra.get(
                            "why",
                            "Add a flexible stop for neighborhood texture before dinner.",
                        ),
                    },
                )

            if activity_count == 2:
                blocks = [blocks[0], blocks[-1]]

            itinerary.append(
                {
                    "day": day_number,
                    "theme": attraction.get("theme", f"Day {day_number} exploration arc"),
                    "summary": f"Balanced around {attraction.get('name', 'city discovery')} and easy transitions.",
                    "blocks": blocks,
                }
            )

        return itinerary
