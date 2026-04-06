from __future__ import annotations

import json
import logging
import threading
from collections import deque
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4
from typing import Any, Callable

from .ai_recommendation_engine import RecommendationEngine
from .calibration_engine import CalibrationEngine
from .evaluation_benchmarks import BENCHMARK_CASES
from .feature_engineering import FeatureEngineeringEngine
from .generative_experience_engine import GenerativeExperienceEngine
from .grounding_engine import GroundingEngine
from .itinerary_planner import ItineraryPlanner
from .prioritization_engine import PrioritizationEngine
from .ranking_model import RankingModel
from .risk_analyzer import RiskAnalyzer
from .source_verification_engine import SourceVerificationEngine
from .source_discovery import SourceDiscovery


def explain_recommendation(destination: str, data: dict[str, Any]) -> dict[str, Any]:
    meta = data.get("meta", {})
    scores = meta.get("scores", {})
    safety = data.get("safetyAndRisk", {})
    reasoning = data.get("reasoningWorkflow", {}).get("reason", {})

    safety_confidence = float(scores.get("safetyConfidence", safety.get("confidence", 80)))
    destination_intelligence = float(scores.get("destinationIntelligence", 72))
    budget_fit = float(scores.get("budgetFit", 75))
    local_signal = float(scores.get("localSignal", 74))
    popularity_score = float(reasoning.get("popularityScore", 72))
    relevance_score = float(reasoning.get("relevanceScore", 76))

    diagnostics = data.get("modelDiagnostics", {})
    decision_score = float(diagnostics.get("score", 0)) or round(
        (
            destination_intelligence * 0.18
            + budget_fit * 0.16
            + local_signal * 0.16
            + safety_confidence * 0.20
            + popularity_score * 0.12
            + relevance_score * 0.18
        ),
        2,
    )

    if decision_score >= 88:
        priority_level = "High"
    elif decision_score >= 76:
        priority_level = "Medium"
    else:
        priority_level = "Low"

    risk_level = _normalize_risk_level(str(safety.get("riskLevel", "Moderate awareness")))
    confidence = round(float(diagnostics.get("confidence", 0)) or min(0.98, max(0.58, decision_score / 100)), 2)

    recognized = bool(meta.get("recognizedDestination", False))
    summary_bits = []
    if recognized:
        summary_bits.append(f"{destination} matched a seeded destination intelligence profile")
    else:
        summary_bits.append(f"{destination} was handled through the adaptive fallback intelligence path")

    summary_bits.append(f"safety came back at {risk_level.lower()} risk")
    summary_bits.append(f"relevance scored {round(relevance_score)} based on the user's interests and travel style")
    summary_bits.append(f"the final decision score reached {decision_score}")

    sources_used = list(dict.fromkeys(data.get("reasoningWorkflow", {}).get("perceive", {}).get("sourcesUsed", [])))
    if not sources_used:
        sources_used = [
            "source_discovery",
            "risk_analyzer",
            "prioritization_engine",
            "itinerary_planner",
            "ai_recommendation_engine",
        ]

    return {
        "decision_score": decision_score,
        "priority_level": priority_level,
        "risk_level": risk_level,
        "reason_summary": "; ".join(summary_bits) + ".",
        "sources_used": sources_used,
        "confidence": confidence,
        "calibration_band": diagnostics.get("calibrationBand", "Medium"),
        "feature_breakdown": diagnostics.get("featureBreakdown", []),
    }


class ReasoningEngine:
    """Central agentic orchestrator for destination intelligence and explainable planning."""

    VERSION = "agentic-orchestrator-v3"

    def __init__(
        self,
        recommendation_engine: RecommendationEngine | None = None,
        source_discovery: SourceDiscovery | None = None,
        prioritization_engine: PrioritizationEngine | None = None,
        itinerary_planner: ItineraryPlanner | None = None,
        risk_analyzer: RiskAnalyzer | None = None,
        generative_experience_engine: GenerativeExperienceEngine | None = None,
        source_verification_engine: SourceVerificationEngine | None = None,
        grounding_engine: GroundingEngine | None = None,
        feature_engineering_engine: FeatureEngineeringEngine | None = None,
        ranking_model: RankingModel | None = None,
        calibration_engine: CalibrationEngine | None = None,
        feedback_training_provider: Callable[[], list[dict[str, Any]]] | None = None,
        logger: logging.Logger | None = None,
        history_path: Path | None = None,
        max_history: int = 100,
    ) -> None:
        self.recommendation_engine = recommendation_engine or RecommendationEngine()
        self.source_discovery = source_discovery or self.recommendation_engine.source_discovery
        self.prioritization_engine = prioritization_engine or self.recommendation_engine.prioritization_engine
        self.itinerary_planner = itinerary_planner or self.recommendation_engine.itinerary_planner
        self.risk_analyzer = risk_analyzer or self.recommendation_engine.risk_analyzer
        self.logger = logger or logging.getLogger("mindgrid_voyager")
        self.generative_experience_engine = generative_experience_engine or GenerativeExperienceEngine(
            logger=self.logger,
        )
        self.source_verification_engine = source_verification_engine or SourceVerificationEngine()
        self.grounding_engine = grounding_engine or GroundingEngine()
        self.feature_engineering_engine = feature_engineering_engine or FeatureEngineeringEngine()
        self.ranking_model = ranking_model or RankingModel()
        self.calibration_engine = calibration_engine or CalibrationEngine()
        self.feedback_training_provider = feedback_training_provider
        default_history_path = Path(__file__).resolve().parents[1] / "logs" / "reasoning_history.jsonl"
        self.history_path = history_path or default_history_path
        self._history: deque[dict[str, Any]] = deque(maxlen=max_history)
        self._runtime_feedback_events: deque[dict[str, Any]] = deque(maxlen=200)
        self._learning_lock = threading.RLock()
        self.learning_summary: dict[str, Any] = {
            "status": "bootstrap-priors",
            "benchmarkSamples": 0,
            "feedbackSamples": 0,
        }
        self._ensure_history_path()
        self.refresh_learning_artifacts()

    def orchestrate(self, payload: dict[str, Any]) -> dict[str, Any]:
        request = self._normalize_request(payload)
        trace_id = uuid4().hex[:12]
        self.logger.info(
            "Reasoning workflow started | traceId=%s | destination=%s | budget=%s | duration=%s",
            trace_id,
            request["destination"],
            request["budget"],
            request["duration"],
        )

        perceive_data = self._perceive(request, trace_id)
        reason_data = self._reason(request, perceive_data, trace_id)
        plan_data = self._plan(request, perceive_data, reason_data, trace_id)
        destination_landscape = self._build_destination_landscape(request, trace_id)
        response = self._act(request, perceive_data, reason_data, plan_data, destination_landscape, trace_id)

        self.logger.info(
            "Reasoning workflow completed | traceId=%s | destination=%s | decisionScore=%s",
            trace_id,
            request["destination"],
            response["decisionEngine"]["decision_score"],
        )
        return response

    def get_recent_history(self, limit: int = 10) -> list[dict[str, Any]]:
        items = list(self._history)
        return list(reversed(items[-limit:]))

    def refresh_learning_artifacts(self) -> dict[str, Any]:
        with self._learning_lock:
            return self._refresh_learning_artifacts_locked()

    def apply_feedback_event(self, *, record: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
        with self._learning_lock:
            event = self._normalize_feedback_event(record=record, payload=payload)
            if event:
                self._upsert_runtime_feedback_event(event)
            refresh_summary = self._refresh_learning_artifacts_locked()
            learning_refresh = {
                "status": "refreshed",
                "feedbackApplied": bool(event),
                "feedbackTrainable": bool(event and isinstance(event.get("requestPayload"), dict)),
                "runtimeFeedbackEvents": len(self._runtime_feedback_events),
                "benchmarkSamples": refresh_summary["benchmarkSamples"],
                "feedbackSamples": refresh_summary["feedbackSamples"],
                "totalSamples": refresh_summary["totalSamples"],
                "rankingModelStatus": refresh_summary["rankingModel"].get("status", "unknown"),
                "calibrationStatus": refresh_summary["calibration"].get("status", "unknown"),
                "refreshedAt": datetime.now(UTC).isoformat(),
            }
            self.logger.info(
                "Learning refresh completed | feedbackApplied=%s | trainable=%s | feedbackSamples=%s | totalSamples=%s",
                learning_refresh["feedbackApplied"],
                learning_refresh["feedbackTrainable"],
                learning_refresh["feedbackSamples"],
                learning_refresh["totalSamples"],
            )
            return learning_refresh

    def _refresh_learning_artifacts_locked(self) -> dict[str, Any]:
        dataset = self.build_learning_dataset()
        ranking_summary = self.ranking_model.fit(dataset["samples"])
        calibration_samples = [
            {
                "rawProbability": self.ranking_model.predict_probability(sample["features"]),
                "label": sample["label"],
                "sampleWeight": sample["sampleWeight"],
                "source": sample["source"],
            }
            for sample in dataset["samples"]
        ]
        calibration_summary = self.calibration_engine.fit(calibration_samples)
        self.learning_summary = {
            "status": "trained",
            "benchmarkSamples": dataset["benchmarkSampleCount"],
            "feedbackSamples": dataset["feedbackSampleCount"],
            "totalSamples": len(dataset["samples"]),
            "runtimeFeedbackEvents": len(self._runtime_feedback_events),
            "rankingModel": ranking_summary,
            "calibration": calibration_summary,
            "lastRefreshedAt": datetime.now(UTC).isoformat(),
        }
        return self.learning_summary

    def learning_diagnostics(self) -> dict[str, Any]:
        with self._learning_lock:
            return {
                "version": self.VERSION,
                "summary": self.learning_summary,
                "rankingModel": self.ranking_model.summary(),
                "calibration": self.calibration_engine.summary(),
            }

    def build_learning_dataset(
        self,
        *,
        cases: list[dict[str, Any]] | None = None,
        include_feedback: bool = True,
    ) -> dict[str, Any]:
        with self._learning_lock:
            return self._build_learning_dataset(cases=cases, include_feedback=include_feedback)

    def _perceive(self, request: dict[str, Any], trace_id: str) -> dict[str, Any]:
        profile, recognized = self.source_discovery.discover(request["destination"])
        budget_per_day = round(request["budget"] / max(request["duration"], 1), 2)
        safety = self.risk_analyzer.analyze(profile, request["pace"], budget_per_day)
        sources_used = [
            "source_discovery",
            "risk_analyzer",
            *profile.get("signals", []),
        ]

        perceive_data = {
            "profile": profile,
            "recognized": recognized,
            "budgetPerDay": budget_per_day,
            "currency": request.get("currency", "USD"),
            "safety": safety,
            "sourcesUsed": sources_used,
        }
        self.logger.info(
            "Reasoning step | traceId=%s | stage=perceive | recognized=%s | risk=%s | budgetPerDay=%s",
            trace_id,
            recognized,
            safety.get("riskLevel", "unknown"),
            budget_per_day,
        )
        return perceive_data

    def _reason(
        self,
        request: dict[str, Any],
        perceive_data: dict[str, Any],
        trace_id: str,
    ) -> dict[str, Any]:
        profile = perceive_data["profile"]
        budget_per_day = perceive_data["budgetPerDay"]

        attraction_scores = self._rank_with_scores(
            profile.get("attractions", []),
            request,
            budget_per_day,
            limit=3,
        )
        food_scores = self._rank_with_scores(
            profile.get("food", []),
            request,
            budget_per_day,
            limit=3,
        )
        favorite_scores = self._rank_with_scores(
            profile.get("favorites", []),
            request,
            budget_per_day,
            limit=3,
        )

        all_scores = attraction_scores + food_scores + favorite_scores
        average_rank_score = sum(item["score"] for item in all_scores) / max(len(all_scores), 1)
        popularity_score = self._calculate_popularity(profile, perceive_data["recognized"])
        relevance_score = round(min(98, max(62, average_rank_score)), 2)
        safety_score = float(perceive_data["safety"].get("confidence", 82))

        reason_data = {
            "safetyScore": safety_score,
            "popularityScore": popularity_score,
            "relevanceScore": relevance_score,
            "attractionScores": attraction_scores,
            "foodScores": food_scores,
            "favoriteScores": favorite_scores,
            "topSignals": self._top_reason_signals(attraction_scores, food_scores, favorite_scores),
        }
        self.logger.info(
            "Reasoning step | traceId=%s | stage=reason | safetyScore=%s | popularityScore=%s | relevanceScore=%s",
            trace_id,
            safety_score,
            popularity_score,
            relevance_score,
        )
        return reason_data

    def _plan(
        self,
        request: dict[str, Any],
        perceive_data: dict[str, Any],
        reason_data: dict[str, Any],
        trace_id: str,
    ) -> dict[str, Any]:
        top_attractions = [entry["item"] for entry in reason_data["attractionScores"]]
        top_food = [entry["item"] for entry in reason_data["foodScores"]]
        top_favorites = [entry["item"] for entry in reason_data["favoriteScores"]]
        itinerary = self.itinerary_planner.build(
            request["duration"],
            top_attractions,
            top_food,
            top_favorites,
            request["pace"],
        )

        plan_data = {
            "priorityDestinations": [
                {
                    "destination": perceive_data["profile"]["destination"],
                    "score": round(
                        (reason_data["safetyScore"] * 0.35)
                        + (reason_data["popularityScore"] * 0.25)
                        + (reason_data["relevanceScore"] * 0.40),
                        2,
                    ),
                    "status": "primary",
                }
            ],
            "topAttractions": top_attractions,
            "foodAndCafes": top_food,
            "localFavorites": top_favorites,
            "itinerary": itinerary,
        }
        self.logger.info(
            "Reasoning step | traceId=%s | stage=plan | attractions=%s | food=%s | favorites=%s | days=%s",
            trace_id,
            len(top_attractions),
            len(top_food),
            len(top_favorites),
            len(itinerary),
        )
        return plan_data

    def _act(
        self,
        request: dict[str, Any],
        perceive_data: dict[str, Any],
        reason_data: dict[str, Any],
        plan_data: dict[str, Any],
        destination_landscape: dict[str, Any],
        trace_id: str,
    ) -> dict[str, Any]:
        recommendation = self.recommendation_engine.generate(request)
        grounding = self.grounding_engine.retrieve(
            destination=request["destination"],
            interests=request["interests"],
            travel_style=request["travelStyle"],
            pace=request["pace"],
            ranked_attractions=plan_data["topAttractions"],
            ranked_food=plan_data["foodAndCafes"],
            ranked_favorites=plan_data["localFavorites"],
        )
        engineered_features = self.feature_engineering_engine.build(
            request=request,
            profile=perceive_data["profile"],
            budget_per_day=perceive_data["budgetPerDay"],
            attraction_scores=reason_data["attractionScores"],
            food_scores=reason_data["foodScores"],
            favorite_scores=reason_data["favoriteScores"],
            grounding_metrics=grounding["metrics"],
        )
        features = self._assemble_feature_vector(
            destination_intelligence=float(recommendation.get("meta", {}).get("scores", {}).get("destinationIntelligence", 0)),
            budget_fit=float(recommendation.get("meta", {}).get("scores", {}).get("budgetFit", 0)),
            local_signal=float(recommendation.get("meta", {}).get("scores", {}).get("localSignal", 0)),
            safety_confidence=float(recommendation.get("meta", {}).get("scores", {}).get("safetyConfidence", 0)),
            popularity_score=float(reason_data["popularityScore"]),
            relevance_score=float(reason_data["relevanceScore"]),
            engineered_features=engineered_features["features"],
            grounding_metrics=grounding["metrics"],
        )
        with self._learning_lock:
            model_diagnostics = self.ranking_model.score(features)
            calibration = self.calibration_engine.calibrate(
                destination=request["destination"],
                raw_confidence=float(model_diagnostics["confidence"]),
                score=float(model_diagnostics["score"]),
            )
        model_diagnostics["rawConfidence"] = model_diagnostics["confidence"]
        model_diagnostics["confidence"] = calibration["calibratedConfidence"]
        model_diagnostics["calibrationDiagnostics"] = calibration

        reasoning_workflow = {
            "traceId": trace_id,
            "workflow": ["Perceive", "Reason", "Plan", "Act"],
            "perceive": {
                "recognizedDestination": perceive_data["recognized"],
                "budgetPerDay": perceive_data["budgetPerDay"],
                "currency": perceive_data["currency"],
                "riskLevel": perceive_data["safety"].get("riskLevel", "Moderate"),
                "sourcesUsed": perceive_data["sourcesUsed"],
            },
            "reason": {
                "safetyScore": reason_data["safetyScore"],
                "popularityScore": reason_data["popularityScore"],
                "relevanceScore": reason_data["relevanceScore"],
                "topSignals": reason_data["topSignals"],
            },
            "plan": {
                "priorityDestinations": plan_data["priorityDestinations"],
                "itineraryDays": len(plan_data["itinerary"]),
                "topAttractions": [item["name"] for item in plan_data["topAttractions"]],
                "foodAndCafes": [item["name"] for item in plan_data["foodAndCafes"]],
                "localFavorites": [item["name"] for item in plan_data["localFavorites"]],
            },
            "act": {
                "responseMode": recommendation["meta"].get("mode", "decision-engine"),
                "engineVersion": recommendation["meta"].get("engineVersion", "unknown"),
            },
        }

        social_references = recommendation.get("socialReferences", {})
        if social_references.get("overview"):
            reasoning_workflow["perceive"]["sourcesUsed"] = list(
                dict.fromkeys(
                    [
                        *reasoning_workflow["perceive"]["sourcesUsed"],
                        "youtube_public_search",
                        "reddit_public_search",
                    ]
                )
            )

        enriched = dict(recommendation)
        enriched["meta"] = {
            **recommendation.get("meta", {}),
            "decisionEngineVersion": self.VERSION,
            "traceId": trace_id,
        }
        enriched["reasoningWorkflow"] = reasoning_workflow
        enriched["grounding"] = grounding
        enriched["intentDiagnostics"] = engineered_features["diagnostics"]
        enriched["modelDiagnostics"] = model_diagnostics
        enriched["resultsSummary"] = {
            "topRankedDestination": destination_landscape["topRanked"]["destination"],
            "topPriorityLevel": destination_landscape["topRanked"]["priorityLevel"],
            "whyRankedFirst": destination_landscape["topRanked"]["why"],
            "totalDestinationsAnalyzed": destination_landscape["totalDestinationsAnalyzed"],
            "averageScore": destination_landscape["averageScore"],
            "averageConfidence": destination_landscape["averageConfidence"],
            "rankings": destination_landscape["rankings"],
        }
        enriched["agenticPositioning"] = {
            "workflow": ["Discover", "Verify", "Prioritize", "Explain"],
            "stageMap": [
                {
                    "label": "Discover",
                    "sourceStage": "Perceive",
                    "summary": f"{request['destination']} mapped to seeded intelligence and source signals.",
                    "detail": f"{perceive_data['profile']['destination']} | {perceive_data['budgetPerDay']} {request.get('currency', 'USD')} per day",
                },
                {
                    "label": "Verify",
                    "sourceStage": "Reason",
                    "summary": f"Safety and relevance validated at {round(reason_data['safetyScore'])}% and {round(reason_data['relevanceScore'])}%.",
                    "detail": f"Risk {perceive_data['safety'].get('riskLevel', 'Moderate')} | popularity {round(reason_data['popularityScore'])}",
                },
                {
                    "label": "Prioritize",
                    "sourceStage": "Plan",
                    "summary": f"{len(plan_data['topAttractions'])} attractions and {len(plan_data['localFavorites'])} local favorites ranked into the plan.",
                    "detail": f"{len(plan_data['itinerary'])} itinerary days assembled",
                },
                {
                    "label": "Explain",
                    "sourceStage": "Act",
                    "summary": "Decision score, priority, evidence, and traceability returned to the UI.",
                    "detail": f"traceId {trace_id}",
                },
            ],
        }
        enriched["decisionEngine"] = explain_recommendation(request["destination"], enriched)
        enriched["decisionEngine"]["historyStored"] = True
        enriched["decisionEngine"]["traceId"] = trace_id
        enriched["sourceVerification"] = self.source_verification_engine.verify(
            request=request,
            recommendation=enriched,
            destination_landscape=destination_landscape,
        )
        enriched["decisionEngine"]["verification_status"] = enriched["sourceVerification"]["verificationSummary"]["status"]
        enriched["agenticExperience"] = self.generative_experience_engine.generate(
            request=request,
            recommendation=enriched,
            destination_landscape=destination_landscape,
        )

        self._store_history(
            {
                "traceId": trace_id,
                "timestamp": datetime.now(UTC).isoformat(),
                "request": request,
                "decisionEngine": enriched["decisionEngine"],
                "sourceVerification": enriched["sourceVerification"],
                "agenticExperience": enriched["agenticExperience"],
                "reasoningWorkflow": reasoning_workflow,
            }
        )
        self.logger.info(
            "Reasoning step | traceId=%s | stage=act | priority=%s | confidence=%s | generatedMode=%s",
            trace_id,
            enriched["decisionEngine"]["priority_level"],
            enriched["decisionEngine"]["confidence"],
            enriched["agenticExperience"].get("mode", "unknown"),
        )
        return enriched

    def benchmark_landscape(self, payload: dict[str, Any]) -> dict[str, Any]:
        request = self._normalize_request(payload)
        return self._build_destination_landscape(
            request,
            trace_id="benchmark",
            prefer_selected_destination=False,
        )

    def benchmark_landscape_with_model(
        self,
        payload: dict[str, Any],
        *,
        ranking_model: RankingModel | None = None,
        calibration_engine: CalibrationEngine | None = None,
        feature_mask: set[str] | None = None,
    ) -> dict[str, Any]:
        request = self._normalize_request(payload)
        return self._build_destination_landscape(
            request,
            trace_id="benchmark",
            prefer_selected_destination=False,
            ranking_model=ranking_model,
            calibration_engine=calibration_engine,
            feature_mask=feature_mask,
        )

    def _build_destination_landscape(
        self,
        request: dict[str, Any],
        trace_id: str,
        prefer_selected_destination: bool = True,
        ranking_model: RankingModel | None = None,
        calibration_engine: CalibrationEngine | None = None,
        feature_mask: set[str] | None = None,
    ) -> dict[str, Any]:
        budget_per_day = round(request["budget"] / max(request["duration"], 1), 2)
        rankings = [
            self._evaluate_destination_candidate(
                profile,
                request,
                budget_per_day,
                ranking_model=ranking_model,
                calibration_engine=calibration_engine,
                feature_mask=feature_mask,
            )
            for profile in self.source_discovery.seed_profiles()
        ]
        rankings.sort(key=lambda item: item["score"], reverse=True)

        average_score = round(sum(item["score"] for item in rankings) / max(len(rankings), 1), 2)
        average_confidence = round(sum(item["confidence"] for item in rankings) / max(len(rankings), 1), 2)
        selected_candidate = (
            next(
                (item for item in rankings if item["destination"].lower() == request["destination"].lower()),
                None,
            )
            if prefer_selected_destination
            else None
        )
        top_ranked = selected_candidate or (rankings[0] if rankings else {
            "destination": request["destination"],
            "score": 0.0,
            "confidence": 0.0,
            "priorityLevel": "Medium",
            "why": "No seeded landscape was available.",
        })

        self.logger.info(
            "Reasoning landscape | traceId=%s | analyzed=%s | top=%s | averageScore=%s",
            trace_id,
            len(rankings),
            top_ranked["destination"],
            average_score,
        )
        return {
            "topRanked": top_ranked,
            "totalDestinationsAnalyzed": len(rankings),
            "averageScore": average_score,
            "averageConfidence": average_confidence,
            "rankings": rankings,
        }

    def _build_learning_dataset(
        self,
        *,
        cases: list[dict[str, Any]] | None = None,
        include_feedback: bool,
    ) -> dict[str, Any]:
        benchmark_samples: list[dict[str, Any]] = []
        feedback_samples: list[dict[str, Any]] = []

        for case in (cases or BENCHMARK_CASES):
            request = self._normalize_request(dict(case["request"]))
            budget_per_day = round(request["budget"] / max(request["duration"], 1), 2)
            accepted = {str(item).lower() for item in case.get("acceptedTop", [case["expectedTop"]])}
            expected = str(case["expectedTop"]).lower()

            for profile in self.source_discovery.seed_profiles():
                snapshot = self._candidate_snapshot(profile=profile, request=request, budget_per_day=budget_per_day)
                destination = str(profile.get("destination", "")).strip()
                destination_key = destination.lower()
                label = 1.0 if destination_key in accepted else 0.0
                sample_weight = 1.35 if destination_key == expected else 1.0 if label else 0.78
                benchmark_samples.append(
                    {
                        "features": snapshot["featureVector"],
                        "label": label,
                        "sampleWeight": sample_weight,
                        "source": "benchmark",
                        "destination": destination,
                        "caseId": case["id"],
                    }
                )

        if include_feedback:
            for event in self._feedback_training_events():
                request_payload = event.get("requestPayload")
                if not isinstance(request_payload, dict):
                    continue
                request = self._normalize_request(request_payload)
                profile, _ = self.source_discovery.discover(event.get("destination", request["destination"]))
                budget_per_day = round(request["budget"] / max(request["duration"], 1), 2)
                snapshot = self._candidate_snapshot(profile=profile, request=request, budget_per_day=budget_per_day)
                feedback_samples.append(
                    {
                        "features": snapshot["featureVector"],
                        "label": self._soft_label_from_feedback(
                            verdict=str(event.get("verdict", "")),
                            rating=int(event.get("rating", 3)),
                        ),
                        "sampleWeight": round(0.75 + (int(event.get("rating", 3)) * 0.15), 2),
                        "source": "feedback",
                        "destination": str(event.get("destination", "")).strip(),
                        "caseId": str(event.get("createdAt", "")).strip(),
                    }
                )

        return {
            "samples": [*benchmark_samples, *feedback_samples],
            "benchmarkSampleCount": len(benchmark_samples),
            "feedbackSampleCount": len(feedback_samples),
        }

    def _feedback_training_events(self) -> list[dict[str, Any]]:
        provider_events: list[dict[str, Any]] = []
        if self.feedback_training_provider:
            try:
                events = self.feedback_training_provider()
            except Exception as exc:  # noqa: BLE001
                self.logger.warning("Learning refresh skipped feedback events | %s", exc)
                events = []
            provider_events = events if isinstance(events, list) else []

        merged_events: list[dict[str, Any]] = []
        seen: set[str] = set()
        for event in [*list(self._runtime_feedback_events), *provider_events]:
            normalized = self._normalize_feedback_training_event(event)
            if not normalized:
                continue
            event_key = self._feedback_event_key(normalized)
            if event_key in seen:
                continue
            seen.add(event_key)
            merged_events.append(normalized)
        return merged_events

    def _candidate_snapshot(
        self,
        *,
        profile: dict[str, Any],
        request: dict[str, Any],
        budget_per_day: float,
    ) -> dict[str, Any]:
        safety = self.risk_analyzer.analyze(profile, request["pace"], budget_per_day)
        attraction_scores = self._rank_with_scores(profile.get("attractions", []), request, budget_per_day, limit=2)
        food_scores = self._rank_with_scores(profile.get("food", []), request, budget_per_day, limit=2)
        favorite_scores = self._rank_with_scores(profile.get("favorites", []), request, budget_per_day, limit=2)

        ranked_values = [entry["score"] for entry in attraction_scores + food_scores + favorite_scores]
        relevance_score = round(sum(ranked_values) / max(len(ranked_values), 1), 2)
        popularity_score = self._calculate_popularity(profile, True)
        score_inputs = profile.get("scoreInputs", {})
        destination_intelligence = float(score_inputs.get("destinationIntelligence", 82))
        budget_fit = float(score_inputs.get("budgetFit", self._budget_fit_proxy(budget_per_day)))
        local_signal = float(score_inputs.get("localSignal", min(94, 72 + len(profile.get("favorites", [])) * 5)))
        safety_confidence = float(score_inputs.get("safetyConfidence", safety.get("confidence", 82)))
        grounding = self.grounding_engine.retrieve(
            destination=str(profile.get("destination", request["destination"])),
            interests=request["interests"],
            travel_style=request["travelStyle"],
            pace=request["pace"],
            ranked_attractions=[entry["item"] for entry in attraction_scores],
            ranked_food=[entry["item"] for entry in food_scores],
            ranked_favorites=[entry["item"] for entry in favorite_scores],
        )
        engineered_features = self.feature_engineering_engine.build(
            request=request,
            profile=profile,
            budget_per_day=budget_per_day,
            attraction_scores=attraction_scores,
            food_scores=food_scores,
            favorite_scores=favorite_scores,
            grounding_metrics=grounding["metrics"],
        )
        feature_vector = self._assemble_feature_vector(
            destination_intelligence=destination_intelligence,
            budget_fit=budget_fit,
            local_signal=local_signal,
            safety_confidence=safety_confidence,
            popularity_score=popularity_score,
            relevance_score=relevance_score,
            engineered_features=engineered_features["features"],
            grounding_metrics=grounding["metrics"],
        )
        return {
            "featureVector": feature_vector,
            "engineeredFeatures": engineered_features,
            "grounding": grounding,
            "destinationIntelligence": destination_intelligence,
            "budgetFit": budget_fit,
            "localSignal": local_signal,
            "safetyConfidence": safety_confidence,
            "relevanceScore": relevance_score,
            "popularityScore": popularity_score,
        }

    def _assemble_feature_vector(
        self,
        *,
        destination_intelligence: float,
        budget_fit: float,
        local_signal: float,
        safety_confidence: float,
        popularity_score: float,
        relevance_score: float,
        engineered_features: dict[str, Any],
        grounding_metrics: dict[str, Any],
    ) -> dict[str, float]:
        return {
            "destination_intelligence": destination_intelligence,
            "budget_fit": budget_fit,
            "local_signal": local_signal,
            "safety_confidence": safety_confidence,
            "popularity_score": popularity_score,
            "relevance_score": relevance_score,
            "budget_realism": float(engineered_features["budget_realism"]),
            "intent_alignment": float(engineered_features["intent_alignment"]),
            "best_for_alignment": float(engineered_features["best_for_alignment"]),
            "style_alignment": float(engineered_features["style_alignment"]),
            "pace_alignment": float(engineered_features["pace_alignment"]),
            "grounding_coverage": float(grounding_metrics["coverageScore"]),
            "grounding_trust": float(grounding_metrics["trustScore"]),
            "grounding_recency": float(grounding_metrics["recencyScore"]),
            "evidence_density": min(99.0, float(grounding_metrics["documentsUsed"]) * 12.0),
            "evidence_support": float(engineered_features.get("evidence_support", 0.0)),
        }

    def _apply_feature_mask(
        self,
        features: dict[str, float],
        feature_mask: set[str] | None,
    ) -> dict[str, float]:
        if not feature_mask:
            return dict(features)
        masked = dict(features)
        for key in feature_mask:
            if key in masked:
                masked[key] = 0.0
        return masked

    def _soft_label_from_feedback(self, *, verdict: str, rating: int) -> float:
        normalized_verdict = str(verdict).strip().lower()
        rating_signal = max(0.0, min(1.0, rating / 5))
        if normalized_verdict == "accepted":
            return round(min(1.0, 0.72 + rating_signal * 0.28), 3)
        if normalized_verdict == "replanned":
            return round(0.32 + rating_signal * 0.24, 3)
        return round(max(0.0, 0.08 + rating_signal * 0.12), 3)

    def _evaluate_destination_candidate(
        self,
        profile: dict[str, Any],
        request: dict[str, Any],
        budget_per_day: float,
        ranking_model: RankingModel | None = None,
        calibration_engine: CalibrationEngine | None = None,
        feature_mask: set[str] | None = None,
    ) -> dict[str, Any]:
        snapshot = self._candidate_snapshot(profile=profile, request=request, budget_per_day=budget_per_day)
        model = ranking_model or self.ranking_model
        calibrator = calibration_engine or self.calibration_engine
        feature_vector = self._apply_feature_mask(snapshot["featureVector"], feature_mask)
        with self._learning_lock:
            diagnostics = model.score(feature_vector)
            calibration = calibrator.calibrate(
                destination=str(profile.get("destination", request["destination"])),
                raw_confidence=float(diagnostics["confidence"]),
                score=float(diagnostics["score"]),
            )
        diagnostics["rawConfidence"] = diagnostics["confidence"]
        diagnostics["confidence"] = calibration["calibratedConfidence"]
        diagnostics["calibrationDiagnostics"] = calibration
        decision_score = float(diagnostics["score"])
        confidence = float(diagnostics["confidence"])
        stage_contribution = {
            "Discover": round((snapshot["destinationIntelligence"] + snapshot["localSignal"] + snapshot["popularityScore"] + snapshot["grounding"]["metrics"]["coverageScore"]) / 4, 2),
            "Verify": round((snapshot["safetyConfidence"] + snapshot["grounding"]["metrics"]["trustScore"]) / 2, 2),
            "Prioritize": round((snapshot["budgetFit"] + snapshot["relevanceScore"] + snapshot["grounding"]["metrics"]["recencyScore"]) / 3, 2),
            "Explain": round((decision_score + (confidence * 100)) / 2, 2),
        }
        leading_stage = max(stage_contribution, key=stage_contribution.get)

        return {
            "destination": profile.get("destination", "Unknown"),
            "score": decision_score,
            "confidence": confidence,
            "priorityLevel": _priority_from_score(decision_score),
            "why": profile.get("explanationSummary", profile.get("whyNow", "High overall fit.")),
            "signals": profile.get("signals", [])[:3],
            "bestFor": profile.get("bestFor", [])[:3],
            "tripStyle": profile.get("styleIndicators", [])[:3],
            "budgetFit": snapshot["budgetFit"],
            "localSignal": snapshot["localSignal"],
            "safety": snapshot["safetyConfidence"],
            "groundingCoverage": snapshot["grounding"]["metrics"]["coverageScore"],
            "groundingTrust": snapshot["grounding"]["metrics"]["trustScore"],
            "leadingStage": leading_stage,
            "stageContribution": stage_contribution,
            "stageReason": self._stage_reason(leading_stage),
            "intentDiagnostics": snapshot["engineeredFeatures"]["diagnostics"],
            "featureBreakdown": diagnostics["featureBreakdown"],
        }

    def _normalize_feedback_event(self, *, record: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any] | None:
        if not isinstance(payload, dict):
            return None
        normalized = self._normalize_feedback_training_event(
            {
                "id": record.get("id", ""),
                "createdAt": record.get("createdAt", datetime.now(UTC).isoformat()),
                "traceId": payload.get("traceId", ""),
                "destination": payload.get("destination", ""),
                "verdict": payload.get("verdict", ""),
                "rating": payload.get("rating", 0),
                "requestPayload": payload.get("requestPayload", payload.get("request_payload")),
            }
        )
        return normalized

    def _normalize_feedback_training_event(self, event: dict[str, Any]) -> dict[str, Any] | None:
        if not isinstance(event, dict):
            return None
        request_payload = event.get("requestPayload", event.get("request_payload"))
        normalized_request_payload = request_payload if isinstance(request_payload, dict) else None
        return {
            "id": str(event.get("id", "")).strip(),
            "createdAt": str(event.get("createdAt", event.get("created_at", ""))).strip(),
            "traceId": str(event.get("traceId", event.get("trace_id", ""))).strip(),
            "destination": str(event.get("destination", "")).strip(),
            "verdict": str(event.get("verdict", "")).strip().lower(),
            "rating": int(event.get("rating", 0) or 0),
            "requestPayload": normalized_request_payload,
        }

    def _feedback_event_key(self, event: dict[str, Any]) -> str:
        explicit_id = str(event.get("id", "")).strip()
        if explicit_id:
            return explicit_id
        return "|".join(
            [
                str(event.get("traceId", "")).strip(),
                str(event.get("createdAt", "")).strip(),
                str(event.get("destination", "")).strip().lower(),
                str(event.get("verdict", "")).strip().lower(),
                str(event.get("rating", 0)).strip(),
            ]
        )

    def _upsert_runtime_feedback_event(self, event: dict[str, Any]) -> None:
        event_key = self._feedback_event_key(event)
        filtered = [item for item in self._runtime_feedback_events if self._feedback_event_key(item) != event_key]
        self._runtime_feedback_events = deque(filtered, maxlen=self._runtime_feedback_events.maxlen)
        self._runtime_feedback_events.appendleft(event)

    def _rank_with_scores(
        self,
        items: list[dict[str, Any]],
        request: dict[str, Any],
        budget_per_day: float,
        limit: int,
    ) -> list[dict[str, Any]]:
        ranked = sorted(
            (
                {
                    "item": item,
                    "score": self.prioritization_engine.score_item(
                        item,
                        request["interests"],
                        request["travelStyle"],
                        request["pace"],
                        budget_per_day,
                    ),
                }
                for item in items
            ),
            key=lambda entry: entry["score"],
            reverse=True,
        )
        return ranked[:limit]

    def _normalize_request(self, payload: dict[str, Any]) -> dict[str, Any]:
        interests = payload.get("interests", [])
        if isinstance(interests, str):
            interests = [item.strip() for item in interests.split(",") if item.strip()]

        return {
            "destination": str(payload.get("destination", "")).strip().title(),
            "budget": int(payload.get("budget", 0)),
            "currency": str(payload.get("currency", "USD")).strip().upper() or "USD",
            "duration": int(payload.get("duration", 1)),
            "interests": [str(item).strip().lower() for item in interests if str(item).strip()][:6],
            "travelStyle": str(payload.get("travelStyle", "Balanced Explorer")).strip() or "Balanced Explorer",
            "pace": str(payload.get("pace", "balanced")).strip().lower() or "balanced",
        }

    def _calculate_popularity(self, profile: dict[str, Any], recognized: bool) -> float:
        base = 80 if recognized else 68
        attractions = len(profile.get("attractions", [])) * 3
        food = len(profile.get("food", [])) * 2
        favorites = len(profile.get("favorites", [])) * 2
        signals = len(profile.get("signals", [])) * 1.5
        return round(min(96, base + attractions + food + favorites + signals), 2)

    def _budget_fit_proxy(self, budget_per_day: float) -> float:
        if budget_per_day < 100:
            return 82.0
        if budget_per_day <= 220:
            return 89.0
        if budget_per_day <= 320:
            return 92.0
        return 86.0

    def _top_reason_signals(
        self,
        attraction_scores: list[dict[str, Any]],
        food_scores: list[dict[str, Any]],
        favorite_scores: list[dict[str, Any]],
    ) -> list[str]:
        picks = []
        for bucket in (attraction_scores, food_scores, favorite_scores):
            if bucket:
                picks.append(f"{bucket[0]['item']['name']} scored {bucket[0]['score']}")
        return picks[:4]

    def _stage_reason(self, stage: str) -> str:
        reasons = {
            "Discover": "High destination fit and local signal lifted the candidate early.",
            "Verify": "Safety confidence and trustworthiness improved the rank.",
            "Prioritize": "Budget fit and route relevance made the plan more practical.",
            "Explain": "Overall score confidence made the result easier to defend.",
        }
        return reasons.get(stage, "Balanced performance across the workflow.")

    def _ensure_history_path(self) -> None:
        self.history_path.parent.mkdir(exist_ok=True)
        if not self.history_path.exists():
            self.history_path.write_text("", encoding="utf-8")

    def _store_history(self, record: dict[str, Any]) -> None:
        self._history.append(record)
        try:
            with self.history_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record) + "\n")
        except OSError as exc:
            self.logger.warning("Reasoning history persistence skipped | %s", exc)


def _normalize_risk_level(value: str) -> str:
    risk = value.lower()
    if "low" in risk or "relaxed" in risk:
        return "Low"
    if "high" in risk:
        return "High"
    return "Medium"


def _priority_from_score(score: float) -> str:
    if score >= 88:
        return "High"
    if score >= 76:
        return "Medium"
    return "Low"
