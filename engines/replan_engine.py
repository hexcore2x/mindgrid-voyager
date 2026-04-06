from __future__ import annotations

import logging
from typing import Any, Callable

from .llm_gateway import LLMGateway
from .source_discovery import SourceDiscovery


class ReplanEngine:
    """Natural-language replan layer for iterative decision-making."""

    VERSION = "replan-engine-v1"

    def __init__(
        self,
        *,
        source_discovery: SourceDiscovery,
        llm_gateway: LLMGateway | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        self.source_discovery = source_discovery
        self.llm_gateway = llm_gateway or LLMGateway(logger=logger)
        self.logger = logger or logging.getLogger("mindgrid_voyager")
        self._known_destinations = [profile.get("destination", "") for profile in self.source_discovery.seed_profiles()]

    def replan(
        self,
        *,
        base_request: dict[str, Any],
        instruction: str,
        decision_runner: Callable[[dict[str, Any]], dict[str, Any]],
    ) -> dict[str, Any]:
        normalized_request = self._normalize_request(base_request)
        parsed_intent = {
            "goals": [],
            "constraints": [],
            "detectedDestinations": [],
        }
        applied_adjustments: list[str] = []
        instruction_lower = instruction.strip().lower()

        self._apply_destination_shift(normalized_request, instruction_lower, parsed_intent, applied_adjustments)
        self._apply_budget_shift(normalized_request, instruction_lower, parsed_intent, applied_adjustments)
        self._apply_style_shift(normalized_request, instruction_lower, parsed_intent, applied_adjustments)
        self._apply_pace_shift(normalized_request, instruction_lower, parsed_intent, applied_adjustments)
        self._apply_duration_shift(normalized_request, instruction_lower, parsed_intent, applied_adjustments)
        self._apply_interest_shift(normalized_request, instruction_lower, parsed_intent, applied_adjustments)

        if not applied_adjustments:
            applied_adjustments.append("Kept the base brief intact and generated a sharper explanation/verification pass.")
            parsed_intent["goals"].append("clarify-current-brief")

        normalized_request["interests"] = self._dedupe(normalized_request["interests"])[:6]
        recommendation = decision_runner(normalized_request)
        model_layer = self.llm_gateway.generate_replan_layer(
            base_request=base_request,
            updated_request=normalized_request,
            instruction=instruction,
            applied_adjustments=applied_adjustments,
            recommendation=recommendation,
        )

        assistant_reply = model_layer.get(
            "assistantReply",
            "The decision engine updated the brief and reran the recommendation.",
        )
        self.logger.info(
            "Replan generated | destination=%s | adjustments=%s | intent=%s",
            normalized_request["destination"],
            len(applied_adjustments),
            ",".join(parsed_intent["goals"]),
        )

        return {
            "instruction": instruction,
            "parsedIntent": parsed_intent,
            "appliedAdjustments": applied_adjustments,
            "assistantReply": assistant_reply,
            "updatedRequest": normalized_request,
            "recommendation": recommendation,
            "modelLayer": model_layer,
        }

    def _normalize_request(self, base_request: dict[str, Any]) -> dict[str, Any]:
        interests = base_request.get("interests", [])
        if isinstance(interests, str):
            interests = [item.strip().lower() for item in interests.split(",") if item.strip()]
        else:
            interests = [str(item).strip().lower() for item in interests if str(item).strip()]

        return {
            "destination": str(base_request.get("destination", "")).strip().title(),
            "budget": int(float(base_request.get("budget", 0) or 0)),
            "currency": str(base_request.get("currency", "USD")).strip().upper() or "USD",
            "duration": int(base_request.get("duration", 1) or 1),
            "interests": interests,
            "travelStyle": str(base_request.get("travelStyle", "Balanced Explorer")).strip() or "Balanced Explorer",
            "pace": str(base_request.get("pace", "balanced")).strip().lower() or "balanced",
        }

    def _apply_destination_shift(
        self,
        request: dict[str, Any],
        instruction_lower: str,
        parsed_intent: dict[str, Any],
        applied_adjustments: list[str],
    ) -> None:
        for destination in self._known_destinations:
            normalized = destination.lower()
            if normalized in instruction_lower and normalized != request["destination"].lower():
                request["destination"] = destination
                parsed_intent["detectedDestinations"].append(destination)
                applied_adjustments.append(f"Switched the destination to {destination} based on the follow-up instruction.")
                parsed_intent["goals"].append("destination-shift")
                return

    def _apply_budget_shift(
        self,
        request: dict[str, Any],
        instruction_lower: str,
        parsed_intent: dict[str, Any],
        applied_adjustments: list[str],
    ) -> None:
        if any(token in instruction_lower for token in ("cheaper", "budget", "affordable", "save money", "lower cost")):
            request["budget"] = max(300, round(request["budget"] * 0.82))
            request["travelStyle"] = "Budget Hunter"
            parsed_intent["goals"].append("optimize-budget")
            applied_adjustments.append("Reduced the budget target and shifted the travel style toward Budget Hunter.")
        elif any(token in instruction_lower for token in ("luxury", "premium", "upgrade", "high-end", "nicer")):
            request["budget"] = max(request["budget"], round(request["budget"] * 1.22))
            request["travelStyle"] = "Luxury Escape"
            parsed_intent["goals"].append("upgrade-budget")
            applied_adjustments.append("Raised the budget ceiling and shifted the travel style toward Luxury Escape.")

    def _apply_style_shift(
        self,
        request: dict[str, Any],
        instruction_lower: str,
        parsed_intent: dict[str, Any],
        applied_adjustments: list[str],
    ) -> None:
        if any(token in instruction_lower for token in ("food", "cafe", "coffee", "restaurant")):
            request["travelStyle"] = "Food Scout"
            parsed_intent["goals"].append("food-focus")
            applied_adjustments.append("Refocused the route toward food and cafe discovery.")
        elif any(token in instruction_lower for token in ("culture", "museum", "history", "art")):
            request["travelStyle"] = "Culture First"
            parsed_intent["goals"].append("culture-focus")
            applied_adjustments.append("Shifted the trip style toward cultural depth and museum-friendly routing.")

    def _apply_pace_shift(
        self,
        request: dict[str, Any],
        instruction_lower: str,
        parsed_intent: dict[str, Any],
        applied_adjustments: list[str],
    ) -> None:
        if any(token in instruction_lower for token in ("slow", "slower", "relaxed", "calm", "less rushed")):
            request["pace"] = "slow"
            parsed_intent["constraints"].append("lower-friction-pace")
            applied_adjustments.append("Reduced the trip pace to a slower, lower-friction rhythm.")
        elif any(token in instruction_lower for token in ("fast", "packed", "faster", "maximize", "intense")):
            request["pace"] = "fast"
            parsed_intent["constraints"].append("higher-density-pace")
            applied_adjustments.append("Increased the trip pace so the route can fit more high-signal blocks.")

    def _apply_duration_shift(
        self,
        request: dict[str, Any],
        instruction_lower: str,
        parsed_intent: dict[str, Any],
        applied_adjustments: list[str],
    ) -> None:
        if any(token in instruction_lower for token in ("weekend", "shorter", "quick trip", "fewer days")):
            request["duration"] = max(2, min(request["duration"], 3))
            parsed_intent["constraints"].append("short-trip")
            applied_adjustments.append("Compressed the itinerary window into a shorter trip.")
        elif any(token in instruction_lower for token in ("longer", "extend", "more days", "stay longer")):
            request["duration"] = min(30, request["duration"] + 2)
            parsed_intent["goals"].append("extended-trip")
            applied_adjustments.append("Extended the trip window to give the itinerary more breathing room.")

    def _apply_interest_shift(
        self,
        request: dict[str, Any],
        instruction_lower: str,
        parsed_intent: dict[str, Any],
        applied_adjustments: list[str],
    ) -> None:
        mappings = [
            ("safer", ["walkable", "calm"], "Added safer, walkable signals to the brief.", "safety-first"),
            ("safe", ["walkable", "calm"], "Added safer, walkable signals to the brief.", "safety-first"),
            ("solo", ["walkable", "culture"], "Adjusted the brief to be more solo-travel friendly.", "solo-friendly"),
            ("nightlife", ["nightlife", "food"], "Added nightlife emphasis to the decision brief.", "nightlife"),
            ("local", ["local", "market"], "Strengthened the local and neighborhood signal in the brief.", "local-discovery"),
            ("authentic", ["local", "culture"], "Strengthened the local and cultural signal in the brief.", "local-discovery"),
            ("wellness", ["wellness", "scenic"], "Shifted the brief toward wellness and scenic recovery moments.", "wellness"),
        ]

        for token, additions, message, goal in mappings:
            if token in instruction_lower:
                request["interests"].extend(additions)
                parsed_intent["goals"].append(goal)
                applied_adjustments.append(message)

    def _dedupe(self, items: list[str]) -> list[str]:
        seen: set[str] = set()
        output: list[str] = []
        for item in items:
            normalized = str(item).strip().lower()
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            output.append(normalized)
        return output
