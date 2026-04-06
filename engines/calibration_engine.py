from __future__ import annotations

import math
from datetime import UTC, datetime
from typing import Any, Callable

from .model_artifact_store import ModelArtifactStore


class CalibrationEngine:
    """Fits and applies local confidence calibration parameters."""

    VERSION = "platt-calibration-v2"
    ARTIFACT_NAME = "calibration_model.json"

    def __init__(
        self,
        feedback_summary_provider: Callable[[str | None], dict[str, Any]] | None = None,
        artifact_store: ModelArtifactStore | None = None,
    ) -> None:
        self.feedback_summary_provider = feedback_summary_provider
        self.artifact_store = artifact_store or ModelArtifactStore()
        self.alpha = 1.0
        self.beta = 0.0
        self.training_summary: dict[str, Any] = {
            "status": "identity",
            "sampleCount": 0,
            "artifactPath": str(self.artifact_store.artifact_path(self.ARTIFACT_NAME)),
        }
        self._load_artifact()

    def calibrate(
        self,
        *,
        destination: str,
        raw_confidence: float,
        score: float,
    ) -> dict[str, Any]:
        raw = float(raw_confidence)
        if raw > 1:
            raw = raw / 100

        transformed = self._sigmoid((self.alpha * self._logit(raw)) + self.beta)
        summary = self.feedback_summary_provider(destination) if self.feedback_summary_provider else {}
        destination_sample_count = int(summary.get("sampleCount", 0))
        global_sample_count = int(summary.get("globalSampleCount", 0))
        score_signal = min(0.99, max(0.01, score / 100))
        calibrated = round(max(0.02, min(0.985, (transformed * 0.92) + (score_signal * 0.08))), 3)

        return {
            "version": self.VERSION,
            "rawConfidence": round(raw, 3),
            "calibratedConfidence": calibrated,
            "sampleCount": destination_sample_count,
            "globalSampleCount": global_sample_count,
            "mode": self.training_summary.get("status", "identity"),
            "alpha": round(self.alpha, 5),
            "beta": round(self.beta, 5),
            "trainingSummary": self.training_summary,
        }

    def fit(
        self,
        samples: list[dict[str, Any]],
        *,
        learning_rate: float = 0.08,
        epochs: int = 220,
        regularization: float = 0.002,
    ) -> dict[str, Any]:
        usable_samples = [sample for sample in samples if sample.get("rawProbability") is not None]
        if len(usable_samples) < 10:
            self.training_summary = {
                "status": "insufficient-calibration-data",
                "sampleCount": len(usable_samples),
                "artifactPath": str(self.artifact_store.artifact_path(self.ARTIFACT_NAME)),
            }
            return self.training_summary

        alpha = float(self.alpha)
        beta = float(self.beta)

        for _ in range(epochs):
            grad_alpha = 0.0
            grad_beta = 0.0
            total_weight = 0.0
            for sample in usable_samples:
                probability = max(1e-5, min(1 - 1e-5, float(sample.get("rawProbability", 0.5))))
                label = float(sample.get("label", 0.0))
                sample_weight = float(sample.get("sampleWeight", 1.0))
                base_logit = self._logit(probability)
                calibrated = self._sigmoid((alpha * base_logit) + beta)
                error = calibrated - label

                grad_alpha += error * base_logit * sample_weight
                grad_beta += error * sample_weight
                total_weight += sample_weight

            if total_weight <= 0:
                continue

            grad_alpha = (grad_alpha / total_weight) + regularization * (alpha - 1.0)
            grad_beta = (grad_beta / total_weight) + regularization * beta
            alpha -= learning_rate * grad_alpha
            beta -= learning_rate * grad_beta

        self.alpha = alpha
        self.beta = beta
        log_loss = self._weighted_log_loss(usable_samples)
        artifact_payload = {
            "version": self.VERSION,
            "trainedAt": datetime.now(UTC).isoformat(),
            "alpha": round(self.alpha, 6),
            "beta": round(self.beta, 6),
            "sampleCount": len(usable_samples),
            "logLoss": log_loss,
            "sourceMix": self._source_mix(usable_samples),
        }
        self.artifact_store.save_json(self.ARTIFACT_NAME, artifact_payload)
        self.training_summary = {
            "status": "fitted-platt-scaling",
            "sampleCount": len(usable_samples),
            "logLoss": log_loss,
            "sourceMix": artifact_payload["sourceMix"],
            "artifactPath": str(self.artifact_store.artifact_path(self.ARTIFACT_NAME)),
        }
        return self.training_summary

    def summary(self) -> dict[str, Any]:
        return {
            "version": self.VERSION,
            "alpha": round(self.alpha, 6),
            "beta": round(self.beta, 6),
            **self.training_summary,
        }

    def _load_artifact(self) -> None:
        artifact = self.artifact_store.load_json(self.ARTIFACT_NAME)
        if not artifact:
            return
        try:
            self.alpha = float(artifact.get("alpha", 1.0))
            self.beta = float(artifact.get("beta", 0.0))
        except (TypeError, ValueError):
            self.alpha = 1.0
            self.beta = 0.0
            return

        self.training_summary = {
            "status": "loaded-artifact",
            "sampleCount": int(artifact.get("sampleCount", 0)),
            "logLoss": float(artifact.get("logLoss", 0.0)),
            "sourceMix": artifact.get("sourceMix", {}),
            "trainedAt": str(artifact.get("trainedAt", "")).strip(),
            "artifactPath": str(self.artifact_store.artifact_path(self.ARTIFACT_NAME)),
        }

    def _logit(self, value: float) -> float:
        clipped = max(1e-6, min(1 - 1e-6, value))
        return math.log(clipped / (1 - clipped))

    def _sigmoid(self, value: float) -> float:
        bounded = max(-30.0, min(30.0, value))
        return 1 / (1 + math.exp(-bounded))

    def _weighted_log_loss(self, samples: list[dict[str, Any]]) -> float:
        total_loss = 0.0
        total_weight = 0.0
        for sample in samples:
            probability = max(1e-5, min(1 - 1e-5, float(sample.get("rawProbability", 0.5))))
            label = float(sample.get("label", 0.0))
            sample_weight = float(sample.get("sampleWeight", 1.0))
            calibrated = max(1e-6, min(1 - 1e-6, self._sigmoid((self.alpha * self._logit(probability)) + self.beta)))
            total_loss += sample_weight * (-(label * math.log(calibrated) + (1 - label) * math.log(1 - calibrated)))
            total_weight += sample_weight
        return round(total_loss / max(total_weight, 1.0), 4)

    def _source_mix(self, samples: list[dict[str, Any]]) -> dict[str, int]:
        counts: dict[str, int] = {}
        for sample in samples:
            source = str(sample.get("source", "unknown")).strip() or "unknown"
            counts[source] = counts.get(source, 0) + 1
        return counts
