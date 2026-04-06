from __future__ import annotations

import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .calibration_engine import CalibrationEngine
from .evaluation_benchmarks import BENCHMARK_CASES
from .model_artifact_store import ModelArtifactStore
from .ranking_model import RankingModel
from .reasoning_engine import ReasoningEngine


class EvaluationEngine:
    """Runs benchmark, slice, ablation, and holdout validation over the ranking stack."""

    VERSION = "evaluation-engine-v3"

    def __init__(self, reasoning_engine: ReasoningEngine) -> None:
        self.reasoning_engine = reasoning_engine

    def run(self) -> dict[str, Any]:
        baseline = self._evaluate_cases(BENCHMARK_CASES)
        generalization = self._temporal_backtest()
        learning = self.reasoning_engine.learning_diagnostics()

        return {
            "version": self.VERSION,
            "generatedAt": datetime.now(UTC).isoformat(),
            "summary": generalization["summary"],
            "headlineMode": "out-of-sample-temporal-backtest",
            "inSampleReference": baseline["summary"],
            "learning": learning,
            "datasetProfile": self._dataset_profile(BENCHMARK_CASES),
            "sliceMetrics": self._slice_metrics(BENCHMARK_CASES),
            "temporalValidation": self._temporal_holdout_validation(),
            "generalizationBacktest": generalization,
            "ablationStudy": self._ablation_study(generalization["summary"]),
            "cases": generalization["cases"],
        }

    def _evaluate_cases(
        self,
        cases: list[dict[str, Any]],
        *,
        ranking_model: RankingModel | None = None,
        calibration_engine: CalibrationEngine | None = None,
        feature_mask: set[str] | None = None,
    ) -> dict[str, Any]:
        case_results: list[dict[str, Any]] = []
        top1_hits = 0
        top3_hits = 0
        confidences: list[float] = []
        confidence_errors: list[float] = []
        grounding_scores: list[float] = []
        brier_terms: list[float] = []

        for case in cases:
            request = dict(case["request"])
            landscape = self.reasoning_engine.benchmark_landscape_with_model(
                request,
                ranking_model=ranking_model,
                calibration_engine=calibration_engine,
                feature_mask=feature_mask,
            )
            rankings = landscape.get("rankings", [])
            top_result = rankings[0] if rankings else {}
            top_destination = str(top_result.get("destination", ""))
            expected = str(case["expectedTop"])
            accepted = [str(item) for item in case.get("acceptedTop", [expected])]
            top_three = [str(item.get("destination", "")) for item in rankings[:3]]

            correct = top_destination in accepted
            top3_hit = any(item in accepted for item in top_three)
            top1_hits += int(correct)
            top3_hits += int(top3_hit)

            confidence = float(top_result.get("confidence", 0))
            confidences.append(confidence)
            confidence_errors.append(abs((1.0 if correct else 0.0) - confidence))
            brier_terms.append((confidence - (1.0 if correct else 0.0)) ** 2)
            grounding_scores.append(float(top_result.get("groundingCoverage", 0)))

            case_results.append(
                {
                    "id": case["id"],
                    "title": case["title"],
                    "expectedTop": expected,
                    "predictedTop": top_destination,
                    "correct": correct,
                    "top3Hit": top3_hit,
                    "score": round(float(top_result.get("score", 0)), 2),
                    "confidence": round(confidence, 3),
                    "groundingCoverage": round(float(top_result.get("groundingCoverage", 0)), 2),
                    "leadingStage": top_result.get("leadingStage", "Discover"),
                    "difficulty": str(case.get("difficulty", "unknown")),
                    "season": str(case.get("season", "unknown")),
                    "region": str(case.get("region", "unknown")),
                    "benchmarkDate": str(case.get("benchmarkDate", "")),
                }
            )

        return {"summary": self._summarize_case_results(case_results), "cases": case_results}

    def _summarize_case_results(self, case_results: list[dict[str, Any]]) -> dict[str, Any]:
        total = max(len(case_results), 1)
        confidences = [float(item.get("confidence", 0)) for item in case_results]
        confidence_errors = [abs((1.0 if item.get("correct") else 0.0) - float(item.get("confidence", 0))) for item in case_results]
        grounding_scores = [float(item.get("groundingCoverage", 0)) for item in case_results]
        brier_terms = [
            (float(item.get("confidence", 0)) - (1.0 if item.get("correct") else 0.0)) ** 2
            for item in case_results
        ]
        return {
            "caseCount": len(case_results),
            "top1Accuracy": round((sum(1 for item in case_results if item.get("correct")) / total) * 100, 2),
            "top3Coverage": round((sum(1 for item in case_results if item.get("top3Hit")) / total) * 100, 2),
            "averageConfidence": round((sum(confidences) / max(len(confidences), 1)) * 100, 2),
            "calibrationGap": round((sum(confidence_errors) / max(len(confidence_errors), 1)) * 100, 2),
            "averageGroundingCoverage": round(sum(grounding_scores) / max(len(grounding_scores), 1), 2),
            "brierScore": round(sum(brier_terms) / max(len(brier_terms), 1), 4),
        }

    def _dataset_profile(self, cases: list[dict[str, Any]]) -> dict[str, Any]:
        return {
            "caseCount": len(cases),
            "difficultyMix": self._count_by(cases, "difficulty"),
            "seasonMix": self._count_by(cases, "season"),
            "regionMix": self._count_by(cases, "region"),
            "travelStyleMix": self._count_by_request(cases, "travelStyle"),
            "paceMix": self._count_by_request(cases, "pace"),
        }

    def _slice_metrics(self, cases: list[dict[str, Any]]) -> dict[str, Any]:
        return {
            "difficulty": self._slice_report(cases, lambda item: str(item.get("difficulty", "unknown"))),
            "season": self._slice_report(cases, lambda item: str(item.get("season", "unknown"))),
            "region": self._slice_report(cases, lambda item: str(item.get("region", "unknown"))),
            "pace": self._slice_report(cases, lambda item: str(item.get("request", {}).get("pace", "unknown"))),
        }

    def _temporal_holdout_validation(self) -> dict[str, Any]:
        ordered = sorted(BENCHMARK_CASES, key=lambda item: str(item.get("benchmarkDate", "")))
        split_index = max(8, int(len(ordered) * 0.7))
        train_cases = ordered[:split_index]
        holdout_cases = ordered[split_index:]
        if not holdout_cases:
            return {
                "status": "insufficient-holdout-cases",
                "trainCaseCount": len(train_cases),
                "holdoutCaseCount": len(holdout_cases),
            }

        with tempfile.TemporaryDirectory() as temp_dir:
            store = ModelArtifactStore(Path(temp_dir))
            ranking_model = RankingModel(artifact_store=store)
            calibration_engine = CalibrationEngine(artifact_store=store)
            dataset = self.reasoning_engine.build_learning_dataset(cases=train_cases, include_feedback=False)
            ranking_model.fit(dataset["samples"])
            calibration_engine.fit(
                [
                    {
                        "rawProbability": ranking_model.predict_probability(sample["features"]),
                        "label": sample["label"],
                        "sampleWeight": sample["sampleWeight"],
                        "source": sample["source"],
                    }
                    for sample in dataset["samples"]
                ]
            )
            holdout = self._evaluate_cases(
                holdout_cases,
                ranking_model=ranking_model,
                calibration_engine=calibration_engine,
            )

        return {
            "status": "completed",
            "trainCaseCount": len(train_cases),
            "holdoutCaseCount": len(holdout_cases),
            "trainWindow": {
                "start": str(train_cases[0].get("benchmarkDate", "")),
                "end": str(train_cases[-1].get("benchmarkDate", "")),
            },
            "holdoutWindow": {
                "start": str(holdout_cases[0].get("benchmarkDate", "")),
                "end": str(holdout_cases[-1].get("benchmarkDate", "")),
            },
            "summary": holdout["summary"],
            "hardFailures": [case for case in holdout["cases"] if not case["correct"]][:3],
        }

    def _temporal_backtest(
        self,
        *,
        feature_mask: set[str] | None = None,
        fit_calibration: bool = True,
    ) -> dict[str, Any]:
        ordered = sorted(BENCHMARK_CASES, key=lambda item: str(item.get("benchmarkDate", "")))
        initial_train_size = max(8, len(ordered) // 3)
        fold_size = 4
        aggregate_cases: list[dict[str, Any]] = []
        folds: list[dict[str, Any]] = []

        for validation_start in range(initial_train_size, len(ordered), fold_size):
            train_cases = ordered[:validation_start]
            validation_cases = ordered[validation_start : validation_start + fold_size]
            if not validation_cases:
                continue

            ranking_model, calibration_engine, dataset = self._train_models_on_cases(
                train_cases,
                fit_calibration=fit_calibration,
            )
            fold_report = self._evaluate_cases(
                validation_cases,
                ranking_model=ranking_model,
                calibration_engine=calibration_engine,
                feature_mask=feature_mask,
            )
            aggregate_cases.extend(fold_report["cases"])
            folds.append(
                {
                    "trainCaseCount": len(train_cases),
                    "validationCaseCount": len(validation_cases),
                    "trainWindow": {
                        "start": str(train_cases[0].get("benchmarkDate", "")),
                        "end": str(train_cases[-1].get("benchmarkDate", "")),
                    },
                    "validationWindow": {
                        "start": str(validation_cases[0].get("benchmarkDate", "")),
                        "end": str(validation_cases[-1].get("benchmarkDate", "")),
                    },
                    "summary": fold_report["summary"],
                    "trainingSamples": len(dataset["samples"]),
                }
            )

        summary = self._summarize_case_results(aggregate_cases)
        summary["benchmarkCaseCount"] = len(ordered)
        summary["mode"] = "out-of-sample-temporal-backtest"
        return {
            "status": "completed",
            "summary": summary,
            "folds": folds,
            "cases": aggregate_cases,
        }

    def _train_models_on_cases(
        self,
        train_cases: list[dict[str, Any]],
        *,
        fit_calibration: bool,
    ) -> tuple[RankingModel, CalibrationEngine, dict[str, Any]]:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = ModelArtifactStore(Path(temp_dir))
            ranking_model = RankingModel(artifact_store=store)
            calibration_engine = CalibrationEngine(artifact_store=store)
            dataset = self.reasoning_engine.build_learning_dataset(cases=train_cases, include_feedback=False)
            ranking_model.fit(dataset["samples"])
            if fit_calibration:
                calibration_engine.fit(
                    [
                        {
                            "rawProbability": ranking_model.predict_probability(sample["features"]),
                            "label": sample["label"],
                            "sampleWeight": sample["sampleWeight"],
                            "source": sample["source"],
                        }
                        for sample in dataset["samples"]
                    ]
                )
        return ranking_model, calibration_engine, dataset

    def _ablation_study(self, baseline_summary: dict[str, Any]) -> list[dict[str, Any]]:
        ablations = [
            {
                "label": "Grounding features removed",
                "featureMask": {
                    "grounding_coverage",
                    "grounding_trust",
                    "grounding_recency",
                    "evidence_density",
                    "evidence_support",
                },
                "calibrationMode": "fitted",
            },
            {
                "label": "Intent features removed",
                "featureMask": {
                    "intent_alignment",
                    "best_for_alignment",
                    "style_alignment",
                    "pace_alignment",
                },
                "calibrationMode": "fitted",
            },
            {
                "label": "Fitted calibration removed",
                "featureMask": set(),
                "calibrationMode": "identity",
            },
        ]
        results: list[dict[str, Any]] = []
        for config in ablations:
            report = self._temporal_backtest(
                feature_mask=config["featureMask"],
                fit_calibration=config["calibrationMode"] == "fitted",
            )
            results.append(
                {
                    "label": config["label"],
                    "summary": report["summary"],
                    "deltaTop1Accuracy": round(
                        report["summary"]["top1Accuracy"] - baseline_summary["top1Accuracy"],
                        2,
                    ),
                    "deltaCalibrationGap": round(
                        report["summary"]["calibrationGap"] - baseline_summary["calibrationGap"],
                        2,
                    ),
                }
            )
        return results

    def _slice_report(self, cases: list[dict[str, Any]], key_fn: Any) -> dict[str, Any]:
        slices: dict[str, list[dict[str, Any]]] = {}
        for case in cases:
            key = key_fn(case)
            slices.setdefault(key, []).append(case)
        return {
            key: self._evaluate_cases(value)["summary"]
            for key, value in slices.items()
        }

    def _count_by(self, cases: list[dict[str, Any]], key: str) -> dict[str, int]:
        counts: dict[str, int] = {}
        for case in cases:
            label = str(case.get(key, "unknown"))
            counts[label] = counts.get(label, 0) + 1
        return counts

    def _count_by_request(self, cases: list[dict[str, Any]], key: str) -> dict[str, int]:
        counts: dict[str, int] = {}
        for case in cases:
            label = str(case.get("request", {}).get(key, "unknown"))
            counts[label] = counts.get(label, 0) + 1
        return counts
