from __future__ import annotations

import json
import logging
import mimetypes
import os
from datetime import datetime, UTC
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from time import perf_counter
from typing import Any
from urllib.parse import urlparse

from database import (
    DB_PATH,
    check_db_connection,
    get_feedback_training_events,
    get_feedback_summary,
    get_recent_requests,
    get_request_count,
    init_db,
    save_feedback,
    save_demo_request,
    save_recommendation_request,
)
from engines import CalibrationEngine, EvaluationEngine, ReasoningEngine, RecommendationEngine, ReplanEngine
from utils.logger import get_app_logger, log_decision_run, log_error, log_request
from utils.validation import (
    ValidationError,
    build_error_response,
    build_success_response,
    validate_comparison_payload,
    validate_demo_request_payload,
    validate_feedback_payload,
    validate_json_body_size,
    validate_json_payload_shape,
    validate_replan_payload,
    validate_recommendation_payload,
)

ROOT = Path(__file__).resolve().parent
LOG_DIR = ROOT / "logs"
APP_VERSION = "1.0"
SERVER_STARTED_AT = datetime.now(UTC)
SERVER_STARTED_MONOTONIC = perf_counter()
STATIC_ROUTES = {
    "/": ROOT / "index.html",
    "/index.html": ROOT / "index.html",
    "/styles.css": ROOT / "styles.css",
    "/app-theme.css": ROOT / "app-theme.css",
    "/theme-refresh.css": ROOT / "theme-refresh.css",
    "/script.js": ROOT / "script.js",
    "/client_app.js": ROOT / "client_app.js",
}
LOGGER = get_app_logger("mindgrid_voyager")
RECOMMENDATION_ENGINE = RecommendationEngine()
REASONING_ENGINE = ReasoningEngine(
    recommendation_engine=RECOMMENDATION_ENGINE,
    calibration_engine=CalibrationEngine(feedback_summary_provider=get_feedback_summary),
    feedback_training_provider=get_feedback_training_events,
    logger=LOGGER,
    history_path=LOG_DIR / "reasoning_history.jsonl",
)
EVALUATION_ENGINE = EvaluationEngine(REASONING_ENGINE)
REPLAN_ENGINE = ReplanEngine(
    source_discovery=RECOMMENDATION_ENGINE.source_discovery,
    logger=LOGGER,
)


class MindGridHandler(BaseHTTPRequestHandler):
    server_version = "MindGridVoyager/2.0"

    def do_GET(self) -> None:  # noqa: N802
        self._dispatch("GET")

    def do_POST(self) -> None:  # noqa: N802
        self._dispatch("POST")

    def _dispatch(self, method: str) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        request_started = perf_counter()
        self._response_status = HTTPStatus.INTERNAL_SERVER_ERROR
        error_message = ""

        try:
            if method == "GET" and path == "/health":
                self._handle_health()
                return
            if method == "GET" and path == "/api/demo-request":
                self._handle_demo_request_summary()
                return
            if method == "GET" and path == "/api/recommendations":
                self._handle_recommendation_summary()
                return
            if method == "GET" and path == "/api/evaluation":
                self._handle_evaluation_summary()
                return
            if method == "GET" and path == "/api/feedback":
                self._handle_feedback_summary()
                return
            if method == "POST" and path == "/api/comparison":
                self._handle_comparison_create()
                return
            if method == "POST" and path == "/api/demo-request":
                self._handle_demo_request_create()
                return
            if method == "POST" and path == "/api/recommendations":
                self._handle_recommendation_create()
                return
            if method == "POST" and path == "/api/replan":
                self._handle_replan_create()
                return
            if method == "POST" and path == "/api/feedback":
                self._handle_feedback_create()
                return

            file_path = STATIC_ROUTES.get(path)
            if file_path and file_path.exists():
                self._serve_file(file_path)
                return

            self._send_error(HTTPStatus.NOT_FOUND, "Not found", f"No route is registered for {path}.")
        except ValidationError as exc:
            error_message = exc.details
            self._send_error(HTTPStatus(exc.status_code), exc.error, exc.details)
        except json.JSONDecodeError:
            error_message = "Request body must be valid JSON."
            self._send_error(
                HTTPStatus.BAD_REQUEST,
                "Invalid input",
                "Request body must be valid JSON.",
            )
        except Exception as exc:  # noqa: BLE001
            error_message = str(exc)
            self._send_error(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                "Internal server error",
                "The server could not complete the request safely.",
            )
        finally:
            duration_ms = (perf_counter() - request_started) * 1000
            status_code = int(self._response_status)
            log_request(
                LOGGER,
                method=method,
                endpoint=path,
                status=status_code,
                duration_ms=duration_ms,
                error_message=error_message,
            )
            if error_message:
                log_error(
                    LOGGER,
                    method=method,
                    endpoint=path,
                    status=status_code,
                    duration_ms=duration_ms,
                    error_message=error_message,
                )

    def _handle_health(self) -> None:
        database_status = "connected" if check_db_connection() else "disconnected"
        uptime_seconds = round(perf_counter() - SERVER_STARTED_MONOTONIC, 2)
        llm_status = REASONING_ENGINE.generative_experience_engine.llm_gateway.status()
        self._send_json(
            HTTPStatus.OK,
            build_success_response(
                status="ok",
                database=database_status,
                version=APP_VERSION,
                uptimeSeconds=uptime_seconds,
                timestamp=datetime.now(UTC).isoformat(),
                llmProvider=llm_status["provider"],
                llmMode=llm_status["mode"],
                llmReady=llm_status["liveReady"],
                llmModel=llm_status["model"],
            ),
        )

    def _handle_demo_request_summary(self) -> None:
        recent = get_recent_requests("demo", limit=3)
        self._send_json(
            HTTPStatus.OK,
            build_success_response(count=get_request_count("demo"), recent=recent),
        )

    def _handle_recommendation_summary(self) -> None:
        recent = get_recent_requests("recommendation", limit=3)
        self._send_json(
            HTTPStatus.OK,
            build_success_response(count=get_request_count("recommendation"), recent=recent),
        )

    def _handle_evaluation_summary(self) -> None:
        evaluation = EVALUATION_ENGINE.run()
        self._send_json(
            HTTPStatus.OK,
            build_success_response(evaluation=evaluation),
        )

    def _handle_feedback_summary(self) -> None:
        summary = get_feedback_summary()
        self._send_json(
            HTTPStatus.OK,
            build_success_response(feedback=summary),
        )

    def _handle_demo_request_create(self) -> None:
        payload = validate_demo_request_payload(self._read_json_body())
        record = save_demo_request(payload)
        LOGGER.info("Demo request saved | id=%s | email=%s", record["id"], record["email"])
        self._send_json(
            HTTPStatus.CREATED,
            build_success_response(
                message="Demo request saved successfully.",
                requestId=record["id"],
            ),
        )

    def _handle_recommendation_create(self) -> None:
        payload = validate_recommendation_payload(self._read_json_body())
        decision_started = perf_counter()
        recommendation = None
        persistence_ids: dict[str, Any] = {}

        try:
            recommendation = REASONING_ENGINE.orchestrate(payload)
            persistence_ids = save_recommendation_request(payload, recommendation)
        except Exception as exc:  # noqa: BLE001
            duration_ms = (perf_counter() - decision_started) * 1000
            log_decision_run(
                LOGGER,
                endpoint="/api/recommendations",
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                duration_ms=duration_ms,
                destination=payload["destination"],
                error_message=str(exc),
            )
            raise

        duration_ms = (perf_counter() - decision_started) * 1000
        log_decision_run(
            LOGGER,
            endpoint="/api/recommendations",
            status=HTTPStatus.OK,
            duration_ms=duration_ms,
            destination=recommendation["request"]["destination"],
            trace_id=recommendation.get("meta", {}).get("traceId", ""),
            request_id=str(persistence_ids.get("requestId", "")),
            decision_score=recommendation.get("decisionEngine", {}).get("decision_score"),
        )
        self._send_json(
            HTTPStatus.OK,
            build_success_response(
                message="Recommendation generated successfully.",
                recommendation=recommendation,
                **persistence_ids,
            ),
        )

    def _handle_comparison_create(self) -> None:
        payload = validate_comparison_payload(self._read_json_body())
        comparison_started = perf_counter()
        recommendations = []

        try:
            for destination in payload["destinations"]:
                recommendation_input = {
                    "destination": destination,
                    "budget": payload["budget"],
                    "currency": payload["currency"],
                    "duration": payload["duration"],
                    "interests": payload["interests"],
                    "travelStyle": payload["travelStyle"],
                    "pace": payload["pace"],
                }
                recommendations.append(REASONING_ENGINE.orchestrate(recommendation_input))
        except Exception as exc:  # noqa: BLE001
            duration_ms = (perf_counter() - comparison_started) * 1000
            log_decision_run(
                LOGGER,
                endpoint="/api/comparison",
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                duration_ms=duration_ms,
                destination=",".join(payload["destinations"]),
                error_message=str(exc),
            )
            raise

        duration_ms = (perf_counter() - comparison_started) * 1000
        comparison = self._build_comparison_response(recommendations)
        log_decision_run(
            LOGGER,
            endpoint="/api/comparison",
            status=HTTPStatus.OK,
            duration_ms=duration_ms,
            destination=",".join(payload["destinations"]),
            trace_id=comparison["topResult"].get("traceId", ""),
            decision_score=comparison["topResult"].get("decisionScore"),
        )
        self._send_json(
            HTTPStatus.OK,
            build_success_response(
                message="Comparison generated successfully.",
                comparison=comparison,
            ),
        )

    def _handle_replan_create(self) -> None:
        payload = validate_replan_payload(self._read_json_body())
        replan_started = perf_counter()
        replan_result = None
        persistence_ids: dict[str, Any] = {}

        try:
            replan_result = REPLAN_ENGINE.replan(
                base_request=payload["baseRequest"],
                instruction=payload["instruction"],
                decision_runner=REASONING_ENGINE.orchestrate,
            )
            persistence_ids = save_recommendation_request(
                replan_result["updatedRequest"],
                replan_result["recommendation"],
            )
        except Exception as exc:  # noqa: BLE001
            duration_ms = (perf_counter() - replan_started) * 1000
            log_decision_run(
                LOGGER,
                endpoint="/api/replan",
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                duration_ms=duration_ms,
                destination=payload["baseRequest"]["destination"],
                error_message=str(exc),
            )
            raise

        duration_ms = (perf_counter() - replan_started) * 1000
        log_decision_run(
            LOGGER,
            endpoint="/api/replan",
            status=HTTPStatus.OK,
            duration_ms=duration_ms,
            destination=replan_result["updatedRequest"]["destination"],
            trace_id=replan_result["recommendation"].get("meta", {}).get("traceId", ""),
            request_id=str(persistence_ids.get("requestId", "")),
            decision_score=replan_result["recommendation"].get("decisionEngine", {}).get("decision_score"),
        )
        self._send_json(
            HTTPStatus.OK,
            build_success_response(
                message="Replan generated successfully.",
                replan=replan_result,
                **persistence_ids,
            ),
        )

    def _handle_feedback_create(self) -> None:
        payload = validate_feedback_payload(self._read_json_body())
        record = save_feedback(payload)
        learning_refresh = REASONING_ENGINE.apply_feedback_event(record=record, payload=payload)
        summary = get_feedback_summary(payload["destination"])
        LOGGER.info(
            "Feedback saved and live learning refreshed | destination=%s | feedbackId=%s | trainable=%s | totalSamples=%s",
            payload["destination"],
            record["id"],
            learning_refresh["feedbackTrainable"],
            learning_refresh["totalSamples"],
        )
        self._send_json(
            HTTPStatus.CREATED,
            build_success_response(
                message="Feedback saved successfully.",
                feedbackId=record["id"],
                feedbackSummary=summary,
                learningRefresh=learning_refresh,
            ),
        )

    def _build_comparison_response(self, recommendations: list[dict[str, Any]]) -> dict[str, Any]:
        results = []
        for item in recommendations:
            decision = item.get("decisionEngine", {})
            scores = item.get("meta", {}).get("scores", {})
            supporting_signals = item.get("supportingSignals", {})
            results.append(
                {
                    "destination": item["request"]["destination"],
                    "decisionScore": decision.get("decision_score", 0.0),
                    "confidence": decision.get("confidence", 0.0),
                    "priorityLevel": decision.get("priority_level", "Medium"),
                    "currency": item["request"].get("currency", "USD"),
                    "budgetFit": scores.get("budgetFit", 0),
                    "safety": scores.get("safetyConfidence", 0),
                    "localSignal": scores.get("localSignal", 0),
                    "tripStyle": item["request"].get("travelStyle", "Balanced Explorer"),
                    "bestFor": supporting_signals.get("bestFor", []),
                    "why": decision.get(
                        "reason_summary",
                        item.get("destinationSummary", {}).get("whyThisWorks", ""),
                    ),
                    "traceId": item.get("meta", {}).get("traceId", ""),
                }
            )

        ranked_results = sorted(results, key=lambda entry: entry["decisionScore"], reverse=True)
        average_score = round(
            sum(entry["decisionScore"] for entry in ranked_results) / max(len(ranked_results), 1),
            2,
        )
        average_confidence = round(
            sum(entry["confidence"] for entry in ranked_results) / max(len(ranked_results), 1),
            2,
        )

        return {
            "totalCompared": len(ranked_results),
            "topRankedDestination": ranked_results[0]["destination"],
            "averageScore": average_score,
            "averageConfidence": average_confidence,
            "topResult": ranked_results[0],
            "results": ranked_results,
        }

    def _read_json_body(self) -> dict[str, Any]:
        content_length = int(self.headers.get("Content-Length", "0"))
        validate_json_body_size(content_length)
        raw_body = self.rfile.read(content_length)
        # The API only accepts object payloads so route handlers can validate predictable keys.
        return validate_json_payload_shape(json.loads(raw_body.decode("utf-8")))

    def _serve_file(self, file_path: Path) -> None:
        data = file_path.read_bytes()
        mime_type, _ = mimetypes.guess_type(file_path.name)
        self._response_status = HTTPStatus.OK
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", mime_type or "application/octet-stream")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        data = json.dumps(payload).encode("utf-8")
        self._response_status = status
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_error(self, status: HTTPStatus, error: str, details: str) -> None:
        self._send_json(status, build_error_response(error=error, details=details))

    def log_message(self, format: str, *args: Any) -> None:
        return


def run() -> None:
    init_db()
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("127.0.0.1", port), MindGridHandler)
    LOGGER.info("MindGrid Voyager startup | port=%s", port)
    print(f"MindGrid Voyager running at http://127.0.0.1:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        LOGGER.info("MindGrid Voyager shutdown requested by user")
        print("\nShutting down MindGrid Voyager.")
    finally:
        server.server_close()
        LOGGER.info("MindGrid Voyager stopped")


if __name__ == "__main__":
    run()
