from __future__ import annotations

import logging
from typing import Any

from .llm_gateway import LLMGateway


class GenerativeExperienceEngine:
    """Builds local-first generated narratives and next-step guidance.

    The current implementation is intentionally rule-based so the project
    remains runnable without external APIs. The output contract is designed so
    a real LLM adapter can replace or augment these methods later.
    """

    VERSION = "generated-experience-v1"

    def __init__(
        self,
        logger: logging.Logger | None = None,
        llm_gateway: LLMGateway | None = None,
    ) -> None:
        self.logger = logger or logging.getLogger("mindgrid_voyager")
        self.llm_gateway = llm_gateway or LLMGateway(logger=self.logger)

    def generate(
        self,
        request: dict[str, Any],
        recommendation: dict[str, Any],
        destination_landscape: dict[str, Any],
    ) -> dict[str, Any]:
        decision = recommendation.get("decisionEngine", {})
        summary = recommendation.get("destinationSummary", {})
        safety = recommendation.get("safetyAndRisk", {})
        budget = recommendation.get("budgetGuidance", {})
        supporting = recommendation.get("supportingSignals", {})
        itinerary = recommendation.get("dayWiseItinerary", [])

        ranked_match = self._ranked_match(request["destination"], destination_landscape.get("rankings", []))
        stage_contribution = ranked_match.get("stageContribution", self._fallback_stage_contribution(recommendation))
        leading_stage = ranked_match.get("leadingStage", self._leading_stage(stage_contribution))

        top_attraction = self._first_name(recommendation.get("topAttractions", []), "one strong anchor attraction")
        top_food = self._first_name(recommendation.get("foodAndCafes", []), "one high-signal food stop")
        top_favorite = self._first_name(recommendation.get("localFavorites", []), "one flexible local detour")
        best_for = self._string_list(supporting.get("bestFor", []), limit=3)
        style_indicators = self._string_list(supporting.get("styleIndicators", []), limit=3)
        budget_note = str(budget.get("destinationNote", "")).strip()
        best_moment = self._best_moment(itinerary, top_attraction, top_food)
        confidence_percent = self._confidence_percent(decision.get("confidence", 0))
        score_text = f"{float(decision.get('decision_score', 0)):.2f}"

        mission_summary = (
            f"{request['destination']} is positioned as a {decision.get('priority_level', 'Medium').lower()}-priority "
            f"mission with a {score_text} decision score, {confidence_percent}% confidence, and a stronger edge in "
            f"{leading_stage.lower()} than the other decision stages."
        )
        operator_note = (
            f"Open with {top_attraction}, use {top_food} as the main food anchor, and keep {top_favorite} available "
            f"as the flexible local layer if pace or energy changes."
        )
        why_selected = (
            f"{request['destination']} won because destination fit, safety confidence, and itinerary relevance stayed "
            f"aligned under the current budget, duration, and travel-style constraints."
        )
        confidence_narrative = (
            f"The engine can defend this recommendation with {confidence_percent}% confidence because the local signal, "
            f"risk profile, and ranking evidence all supported the same direction."
        )

        generated = {
            "mode": "local-template-generation",
            "version": self.VERSION,
            "missionBrief": {
                "title": f"{request['destination']} mission brief",
                "summary": mission_summary,
                "operatorNote": operator_note,
                "focusLabel": leading_stage,
                "bestMoment": best_moment,
                "bestFor": best_for,
                "styleIndicators": style_indicators,
            },
            "decisionNarrative": {
                "shortSummary": summary.get("explanationSummary", why_selected),
                "whyThisWon": why_selected,
                "confidenceNarrative": confidence_narrative,
                "stageContribution": [
                    {
                        "label": label,
                        "score": value,
                        "summary": self._stage_summary(label, value),
                    }
                    for label, value in stage_contribution.items()
                ],
            },
            "agentPlaybook": {
                "nextActions": self._build_next_actions(
                    request=request,
                    top_attraction=top_attraction,
                    top_food=top_food,
                    top_favorite=top_favorite,
                    best_moment=best_moment,
                ),
                "verificationChecklist": self._build_verification_checklist(
                    request=request,
                    safety=safety,
                    budget=budget,
                    budget_note=budget_note,
                ),
                "replanTriggers": self._build_replan_triggers(request, safety, itinerary),
                "followUpQuestions": self._build_follow_up_questions(request, best_for, style_indicators),
            },
            "memoryDraft": {
                "journalTitle": f"{request['destination']} | {summary.get('headline', 'AI travel brief')}",
                "journalPreview": self._build_journal_preview(
                    request=request,
                    best_moment=best_moment,
                    top_attraction=top_attraction,
                    top_food=top_food,
                    best_for=best_for,
                ),
                "shareableSummary": self._build_shareable_summary(
                    destination=request["destination"],
                    best_for=best_for,
                    score_text=score_text,
                    confidence_percent=confidence_percent,
                ),
                "memoryMoments": self._build_memory_moments(
                    best_moment=best_moment,
                    top_attraction=top_attraction,
                    top_food=top_food,
                    top_favorite=top_favorite,
                ),
            },
        }
        generated["modelLayer"] = self.llm_gateway.generate_decision_layer(
            request=request,
            recommendation=recommendation,
            destination_landscape=destination_landscape,
        )

        self.logger.info(
            "Generated experience companion | destination=%s | focus=%s | mode=%s | provider=%s",
            request["destination"],
            leading_stage,
            generated["mode"],
            generated["modelLayer"].get("provider", "mindgrid-local"),
        )
        return generated

    def _build_next_actions(
        self,
        *,
        request: dict[str, Any],
        top_attraction: str,
        top_food: str,
        top_favorite: str,
        best_moment: str,
    ) -> list[str]:
        return [
            f"Lock day one around {top_attraction} so the mission starts with the strongest verified signal cluster.",
            f"Use {top_food} as the main culinary anchor and keep {top_favorite} as the flexible local layer.",
            f"Protect {best_moment.lower()} as the emotional high point instead of overpacking every block.",
            f"Keep the route aligned to a {request['pace']} pace so the plan stays defendable in real-world conditions.",
        ]

    def _build_verification_checklist(
        self,
        *,
        request: dict[str, Any],
        safety: dict[str, Any],
        budget: dict[str, Any],
        budget_note: str,
    ) -> list[str]:
        transport_note = str(safety.get("transportNote", "Keep one reliable return route available each day.")).strip()
        budget_per_day = int(round(float(budget.get("budgetPerDay", 0)))) if budget.get("budgetPerDay") else 0
        currency = str(budget.get("currency", request.get("currency", "USD"))).strip().upper() or "USD"

        return [
            transport_note,
            f"Keep daily spend close to {budget_per_day} {currency}/day so the {budget.get('tier', 'balanced')} budget model stays intact.",
            budget_note or "Concentrate spend in high-signal districts instead of scattering time across long transfers.",
            f"Reconfirm the first and last movement block each day for a {request['duration']}-day mission.",
        ]

    def _build_replan_triggers(
        self,
        request: dict[str, Any],
        safety: dict[str, Any],
        itinerary: list[dict[str, Any]],
    ) -> list[str]:
        triggers = [
            "Replan immediately if transit friction or queue time starts eroding two or more core blocks in a day.",
            "Swap to a lower-movement neighborhood plan if weather or energy makes the original route feel forced.",
        ]

        if "fast" in request["pace"]:
            triggers.append("If the pace starts to feel rushed by mid-afternoon, cut one secondary stop and protect dinner or sunset.")
        else:
            triggers.append("If the day is moving faster than expected, spend the recovered time on one premium local detour instead of adding random hops.")

        if len(itinerary) >= 4 or str(safety.get("riskLevel", "")).lower().startswith("urban"):
            triggers.append("Trigger a low-friction fallback for the final evening block if crowd density or late returns feel noisy.")

        return triggers[:4]

    def _build_follow_up_questions(
        self,
        request: dict[str, Any],
        best_for: list[str],
        style_indicators: list[str],
    ) -> list[str]:
        questions = [
            f"Do you want the plan pushed further toward {best_for[0].lower()} or kept balanced?" if best_for else "Do you want a more focused version of this route?",
            f"Should the next iteration lean more into {style_indicators[0].lower()}?" if style_indicators else "Should the next iteration favor a calmer travel rhythm?",
            "Would you like a weather-proof version of the itinerary for low-friction days?",
            "Should the engine generate a solo-friendly or premium-upgrade variant next?",
        ]
        return questions[:4]

    def _build_journal_preview(
        self,
        *,
        request: dict[str, Any],
        best_moment: str,
        top_attraction: str,
        top_food: str,
        best_for: list[str],
    ) -> str:
        trip_angle = best_for[0].lower() if best_for else request["travelStyle"].lower()
        return (
            f"{request['destination']} felt strongest when the trip stayed centered on {trip_angle}, opened with "
            f"{top_attraction}, and saved {best_moment.lower()} for the moment that made the route feel memorable "
            f"instead of merely efficient. {top_food} gave the plan its social and sensory anchor."
        )

    def _build_shareable_summary(
        self,
        *,
        destination: str,
        best_for: list[str],
        score_text: str,
        confidence_percent: int,
    ) -> str:
        angle = best_for[0] if best_for else "balanced exploration"
        return (
            f"{destination} ranked best for {angle.lower()} with a {score_text} decision score and "
            f"{confidence_percent}% confidence from the local-first decision engine."
        )

    def _build_memory_moments(
        self,
        *,
        best_moment: str,
        top_attraction: str,
        top_food: str,
        top_favorite: str,
    ) -> list[str]:
        return [
            best_moment,
            top_attraction,
            top_food,
            top_favorite,
        ]

    def _ranked_match(self, destination: str, rankings: list[dict[str, Any]]) -> dict[str, Any]:
        normalized = destination.strip().lower()
        return next(
            (item for item in rankings if str(item.get("destination", "")).strip().lower() == normalized),
            {},
        )

    def _fallback_stage_contribution(self, recommendation: dict[str, Any]) -> dict[str, float]:
        meta_scores = recommendation.get("meta", {}).get("scores", {})
        reason = recommendation.get("reasoningWorkflow", {}).get("reason", {})
        decision = recommendation.get("decisionEngine", {})

        discover = self._average(
            [
                meta_scores.get("destinationIntelligence"),
                meta_scores.get("localSignal"),
                reason.get("popularityScore"),
            ]
        )
        verify = self._average([meta_scores.get("safetyConfidence"), reason.get("safetyScore")])
        prioritize = self._average([meta_scores.get("budgetFit"), reason.get("relevanceScore")])
        explain = self._average([decision.get("decision_score"), self._confidence_percent(decision.get("confidence", 0))])

        return {
            "Discover": round(discover, 2),
            "Verify": round(verify, 2),
            "Prioritize": round(prioritize, 2),
            "Explain": round(explain, 2),
        }

    def _average(self, values: list[Any]) -> float:
        numbers = [float(value) for value in values if value not in (None, "")]
        if not numbers:
            return 0.0
        return sum(numbers) / len(numbers)

    def _leading_stage(self, stage_contribution: dict[str, float]) -> str:
        if not stage_contribution:
            return "Discover"
        return max(stage_contribution, key=stage_contribution.get)

    def _best_moment(self, itinerary: list[dict[str, Any]], top_attraction: str, top_food: str) -> str:
        if itinerary:
            for day in itinerary:
                blocks = day.get("blocks", [])
                if blocks:
                    candidate = blocks[-1]
                    title = str(candidate.get("title", "")).strip()
                    time = str(candidate.get("time", "Later")).strip()
                    if title:
                        return f"{time}: {title}"
        return f"Late day around {top_attraction} followed by {top_food}"

    def _first_name(self, items: list[dict[str, Any]], fallback: str) -> str:
        if not items:
            return fallback
        first = items[0]
        return str(first.get("name") or first.get("title") or fallback).strip() or fallback

    def _string_list(self, values: list[Any], *, limit: int) -> list[str]:
        output: list[str] = []
        for value in values:
            normalized = str(value).strip()
            if normalized:
                output.append(normalized)
            if len(output) >= limit:
                break
        return output

    def _confidence_percent(self, value: Any) -> int:
        numeric = float(value or 0)
        if numeric <= 1:
            return round(numeric * 100)
        return round(numeric)

    def _stage_summary(self, label: str, score: float) -> str:
        if label == "Discover":
            return f"Destination fit and signal discovery stayed strong at {round(score)}."
        if label == "Verify":
            return f"Safety and trust validation contributed {round(score)} to the final decision."
        if label == "Prioritize":
            return f"Budget fit and route relevance combined into a {round(score)} prioritization score."
        return f"Explainability and confidence landed at {round(score)} for the final handoff."
