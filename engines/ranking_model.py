from __future__ import annotations

import math
from datetime import UTC, datetime
from dataclasses import dataclass
from typing import Any

from .model_artifact_store import ModelArtifactStore


@dataclass(slots=True)
class RankingModelConfig:
    weights: dict[str, float]
    bias: float = 0.0


class RankingModel:
    """Trainable interpretable ranking model persisted to local artifacts."""

    VERSION = "ranking-model-v3-blended-explainability"
    ARTIFACT_NAME = "ranking_model.json"
    LEARNED_BLEND_WEIGHT = 0.46
    PRIOR_BLEND_WEIGHT = 0.54
    PRIOR_WEIGHTS = {
        "destination_intelligence": 0.10,
        "budget_fit": 0.08,
        "budget_realism": 0.08,
        "local_signal": 0.07,
        "safety_confidence": 0.11,
        "popularity_score": 0.03,
        "relevance_score": 0.09,
        "intent_alignment": 0.16,
        "best_for_alignment": 0.06,
        "style_alignment": 0.09,
        "pace_alignment": 0.05,
        "grounding_coverage": 0.03,
        "grounding_trust": 0.03,
        "grounding_recency": 0.02,
        "evidence_density": 0.0,
        "evidence_support": 0.02,
    }

    def __init__(
        self,
        config: RankingModelConfig | None = None,
        artifact_store: ModelArtifactStore | None = None,
    ) -> None:
        self.artifact_store = artifact_store or ModelArtifactStore()
        self.config = config or RankingModelConfig(
            weights={
                "destination_intelligence": 1.6,
                "budget_fit": 1.2,
                "budget_realism": 1.1,
                "local_signal": 1.0,
                "safety_confidence": 1.8,
                "popularity_score": 0.7,
                "relevance_score": 1.5,
                "intent_alignment": 2.4,
                "best_for_alignment": 0.9,
                "style_alignment": 1.4,
                "pace_alignment": 0.8,
                "grounding_coverage": 0.85,
                "grounding_trust": 1.0,
                "grounding_recency": 0.55,
                "evidence_density": 0.35,
                "evidence_support": 1.1,
            }
        )
        self.training_summary: dict[str, Any] = {
            "status": "bootstrap-priors",
            "sampleCount": 0,
            "positiveRate": 0.0,
            "artifactPath": str(self.artifact_store.artifact_path(self.ARTIFACT_NAME)),
        }
        self._load_artifact()

    def score(self, features: dict[str, float]) -> dict[str, Any]:
        learned_layer = self._build_learned_layer(features)
        prior_layer = self._build_prior_layer(features)
        probability = round(
            (prior_layer["probability"] * self.PRIOR_BLEND_WEIGHT)
            + (learned_layer["probability"] * self.LEARNED_BLEND_WEIGHT),
            6,
        )
        contributions = self._build_blended_feature_breakdown(
            learned_breakdown=learned_layer["featureBreakdown"],
            prior_breakdown=prior_layer["featureBreakdown"],
        )

        score = round(max(0.0, min(99.0, probability * 100)), 2)
        confidence = round(max(0.38, min(0.985, probability * 0.92 + 0.05)), 3)
        calibration_band = self._calibration_band(confidence)

        return {
            "version": self.VERSION,
            "score": score,
            "confidence": confidence,
            "calibrationBand": calibration_band,
            "featureBreakdown": contributions,
            "scoringPipeline": {
                "mode": "blended-prior-plus-learned",
                "blendedProbability": probability,
                "prior": {
                    "weight": self.PRIOR_BLEND_WEIGHT,
                    "probability": prior_layer["probability"],
                    "referenceScore": prior_layer["referenceScore"],
                },
                "learned": {
                    "weight": self.LEARNED_BLEND_WEIGHT,
                    "probability": learned_layer["probability"],
                    "logit": learned_layer["logit"],
                    "bias": round(self.config.bias, 6),
                },
            },
            "layerBreakdown": {
                "priorFeatureBreakdown": prior_layer["featureBreakdown"],
                "learnedFeatureBreakdown": learned_layer["featureBreakdown"],
            },
            "trainingSummary": self.training_summary,
        }

    def predict_probability(self, features: dict[str, float]) -> float:
        learned_probability = self._predict_learned_probability(features)
        prior_probability = self._predict_prior_probability(features)
        return round(
            (prior_probability * self.PRIOR_BLEND_WEIGHT) + (learned_probability * self.LEARNED_BLEND_WEIGHT),
            6,
        )

    def _predict_learned_probability(self, features: dict[str, float]) -> float:
        return self._build_learned_layer(features)["probability"]

    def _predict_prior_probability(self, features: dict[str, float]) -> float:
        return self._build_prior_layer(features)["probability"]

    def fit(
        self,
        samples: list[dict[str, Any]],
        *,
        learning_rate: float = 0.08,
        epochs: int = 240,
        regularization: float = 0.08,
    ) -> dict[str, Any]:
        usable_samples = [sample for sample in samples if isinstance(sample.get("features"), dict)]
        if len(usable_samples) < 8:
            self.training_summary = {
                "status": "insufficient-training-data",
                "sampleCount": len(usable_samples),
                "positiveRate": 0.0,
                "artifactPath": str(self.artifact_store.artifact_path(self.ARTIFACT_NAME)),
            }
            return self.training_summary

        feature_names = list(dict.fromkeys([*self.config.weights.keys(), *self._sample_feature_names(usable_samples)]))
        weights = {name: float(self.config.weights.get(name, 0.0)) for name in feature_names}
        bias = float(self.config.bias)
        priors = dict(weights)
        positive_count = sum(1 for sample in usable_samples if float(sample.get("label", 0.0)) >= 0.5)
        negative_count = max(len(usable_samples) - positive_count, 1)
        positive_boost = max(1.0, (negative_count / max(positive_count, 1)) * 0.55)

        for _ in range(epochs):
            grad_bias = 0.0
            grad_weights = {name: 0.0 for name in feature_names}
            total_weight = 0.0

            for sample in usable_samples:
                label = float(sample.get("label", 0.0))
                sample_weight = float(sample.get("sampleWeight", 1.0))
                if label >= 0.5:
                    sample_weight *= positive_boost
                normalized = {
                    name: self._normalize(float(sample["features"].get(name, 0.0)))
                    for name in feature_names
                }
                logit = bias + sum(weights[name] * normalized[name] for name in feature_names)
                prediction = self._sigmoid(logit)
                error = prediction - label

                grad_bias += error * sample_weight
                for name in feature_names:
                    grad_weights[name] += error * normalized[name] * sample_weight
                total_weight += sample_weight

            if total_weight <= 0:
                continue

            grad_bias /= total_weight
            bias -= learning_rate * grad_bias

            for name in feature_names:
                grad = (grad_weights[name] / total_weight) + regularization * (weights[name] - priors.get(name, 0.0))
                floor = priors.get(name, 0.0) * 0.2
                weights[name] = max(floor, min(8.0, weights[name] - (learning_rate * grad)))

        self.config = RankingModelConfig(weights=weights, bias=bias)
        loss = self._weighted_log_loss(usable_samples)
        positive_rate = round(
            sum(float(sample.get("label", 0.0)) for sample in usable_samples) / max(len(usable_samples), 1),
            4,
        )
        source_mix = self._source_mix(usable_samples)

        artifact_payload = {
            "version": self.VERSION,
            "trainedAt": datetime.now(UTC).isoformat(),
            "bias": round(self.config.bias, 6),
            "weights": {name: round(value, 6) for name, value in self.config.weights.items()},
            "sampleCount": len(usable_samples),
            "positiveRate": positive_rate,
            "logLoss": loss,
            "sourceMix": source_mix,
            "featureNames": feature_names,
        }
        self.artifact_store.save_json(self.ARTIFACT_NAME, artifact_payload)
        self.training_summary = {
            "status": "trained",
            "sampleCount": len(usable_samples),
            "positiveRate": positive_rate,
            "logLoss": loss,
            "sourceMix": source_mix,
            "blendMode": "heuristic-prior-plus-learned-layer",
            "artifactPath": str(self.artifact_store.artifact_path(self.ARTIFACT_NAME)),
        }
        return self.training_summary

    def summary(self) -> dict[str, Any]:
        return {
            "version": self.VERSION,
            "bias": round(self.config.bias, 6),
            "featureCount": len(self.config.weights),
            "blendMode": "heuristic-prior-plus-learned-layer",
            **self.training_summary,
        }

    def _load_artifact(self) -> None:
        artifact = self.artifact_store.load_json(self.ARTIFACT_NAME)
        if not artifact:
            return

        weights = artifact.get("weights")
        bias = artifact.get("bias")
        if not isinstance(weights, dict) or bias is None:
            return

        self.config = RankingModelConfig(
            weights={str(name): float(value) for name, value in weights.items()},
            bias=float(bias),
        )
        self.training_summary = {
            "status": "loaded-artifact",
            "sampleCount": int(artifact.get("sampleCount", 0)),
            "positiveRate": float(artifact.get("positiveRate", 0.0)),
            "logLoss": float(artifact.get("logLoss", 0.0)),
            "sourceMix": artifact.get("sourceMix", {}),
            "trainedAt": str(artifact.get("trainedAt", "")).strip(),
            "artifactPath": str(self.artifact_store.artifact_path(self.ARTIFACT_NAME)),
        }

    def _calibration_band(self, confidence: float) -> str:
        if confidence >= 0.86:
            return "High"
        if confidence >= 0.72:
            return "Medium"
        return "Cautious"

    def _normalize(self, value: float) -> float:
        return max(0.0, min(1.0, value / 100))

    def _sigmoid(self, value: float) -> float:
        bounded = max(-30.0, min(30.0, value))
        return 1 / (1 + math.exp(-bounded))

    def _sample_feature_names(self, samples: list[dict[str, Any]]) -> list[str]:
        names: list[str] = []
        for sample in samples:
            for name in sample["features"].keys():
                if name not in names:
                    names.append(name)
        return names

    def _weighted_log_loss(self, samples: list[dict[str, Any]]) -> float:
        total_loss = 0.0
        total_weight = 0.0
        for sample in samples:
            label = float(sample.get("label", 0.0))
            sample_weight = float(sample.get("sampleWeight", 1.0))
            prediction = max(1e-6, min(1 - 1e-6, self._predict_learned_probability(sample["features"])))
            total_loss += sample_weight * (-(label * math.log(prediction) + (1 - label) * math.log(1 - prediction)))
            total_weight += sample_weight
        return round(total_loss / max(total_weight, 1.0), 4)

    def _source_mix(self, samples: list[dict[str, Any]]) -> dict[str, int]:
        counts: dict[str, int] = {}
        for sample in samples:
            source = str(sample.get("source", "unknown")).strip() or "unknown"
            counts[source] = counts.get(source, 0) + 1
        return counts

    def _build_learned_layer(self, features: dict[str, float]) -> dict[str, Any]:
        logit = self.config.bias
        contributions = []

        for key, weight in self.config.weights.items():
            value = float(features.get(key, 0.0))
            normalized_value = self._normalize(value)
            raw_contribution = normalized_value * weight
            logit += raw_contribution
            contributions.append(
                {
                    "feature": key,
                    "value": round(value, 2),
                    "normalizedValue": round(normalized_value, 4),
                    "weight": round(weight, 3),
                    "rawContribution": round(raw_contribution, 6),
                }
            )

        probability = round(self._sigmoid(logit), 6)
        scaled_contributions = self._scale_layer_contributions(
            contributions,
            total_contribution=probability * 100 * self.LEARNED_BLEND_WEIGHT,
            contribution_field="learnedContribution",
        )
        return {
            "probability": probability,
            "logit": round(logit, 6),
            "featureBreakdown": scaled_contributions,
        }

    def _build_prior_layer(self, features: dict[str, float]) -> dict[str, Any]:
        unclipped_reference_score = 0.0
        contributions = []

        for key, weight in self.PRIOR_WEIGHTS.items():
            value = float(features.get(key, 0.0))
            raw_contribution = value * weight
            unclipped_reference_score += raw_contribution
            contributions.append(
                {
                    "feature": key,
                    "value": round(value, 2),
                    "weight": round(weight, 3),
                    "rawContribution": round(raw_contribution, 6),
                }
            )

        reference_score = max(0.0, min(99.0, unclipped_reference_score))
        probability = round(self._sigmoid((reference_score - 74.0) / 8.0), 6)
        scaled_contributions = self._scale_layer_contributions(
            contributions,
            total_contribution=probability * 100 * self.PRIOR_BLEND_WEIGHT,
            contribution_field="priorContribution",
        )
        return {
            "probability": probability,
            "referenceScore": round(reference_score, 2),
            "featureBreakdown": scaled_contributions,
        }

    def _scale_layer_contributions(
        self,
        contributions: list[dict[str, Any]],
        *,
        total_contribution: float,
        contribution_field: str,
    ) -> list[dict[str, Any]]:
        positive_total = sum(max(float(item.get("rawContribution", 0.0)), 0.0) for item in contributions)
        scaled: list[dict[str, Any]] = []

        for item in contributions:
            raw_contribution = max(float(item.get("rawContribution", 0.0)), 0.0)
            share = (raw_contribution / positive_total) if positive_total > 0 else 0.0
            scaled.append(
                {
                    **item,
                    contribution_field: round(share * total_contribution, 2),
                }
            )

        scaled.sort(key=lambda entry: entry.get(contribution_field, 0.0), reverse=True)
        return scaled

    def _build_blended_feature_breakdown(
        self,
        *,
        learned_breakdown: list[dict[str, Any]],
        prior_breakdown: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        combined: dict[str, dict[str, Any]] = {}

        for item in prior_breakdown:
            feature = str(item.get("feature", "")).strip()
            if not feature:
                continue
            combined[feature] = {
                "feature": feature,
                "value": round(float(item.get("value", 0.0)), 2),
                "priorWeight": round(float(item.get("weight", 0.0)), 3),
                "learnedWeight": round(float(self.config.weights.get(feature, 0.0)), 3),
                "priorContribution": round(float(item.get("priorContribution", 0.0)), 2),
                "learnedContribution": 0.0,
                "contribution": round(float(item.get("priorContribution", 0.0)), 2),
                "dominantLayer": "prior",
            }

        for item in learned_breakdown:
            feature = str(item.get("feature", "")).strip()
            if not feature:
                continue
            entry = combined.setdefault(
                feature,
                {
                    "feature": feature,
                    "value": round(float(item.get("value", 0.0)), 2),
                    "priorWeight": round(float(self.PRIOR_WEIGHTS.get(feature, 0.0)), 3),
                    "learnedWeight": round(float(item.get("weight", 0.0)), 3),
                    "priorContribution": 0.0,
                    "learnedContribution": 0.0,
                    "contribution": 0.0,
                    "dominantLayer": "learned",
                },
            )
            entry["value"] = round(float(item.get("value", entry["value"])), 2)
            entry["learnedWeight"] = round(float(item.get("weight", entry["learnedWeight"])), 3)
            entry["learnedContribution"] = round(float(item.get("learnedContribution", 0.0)), 2)
            entry["contribution"] = round(entry["priorContribution"] + entry["learnedContribution"], 2)
            entry["dominantLayer"] = (
                "prior" if entry["priorContribution"] > entry["learnedContribution"] else "learned"
            )

        blended = sorted(combined.values(), key=lambda entry: entry["contribution"], reverse=True)
        return blended
