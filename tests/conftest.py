from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request
from collections.abc import Iterator

import pytest

import app


@pytest.fixture
def api_server(monkeypatch: pytest.MonkeyPatch) -> Iterator[str]:
    """Run the local HTTP server on an ephemeral port with persistence stubbed out."""

    monkeypatch.setattr(
        app,
        "save_recommendation_request",
        lambda payload, response: {"requestId": "test-request", "resultId": "test-result"},
    )
    monkeypatch.setattr(
        app,
        "save_demo_request",
        lambda payload: {"id": "test-demo", "email": payload["email"]},
    )
    monkeypatch.setattr(
        app,
        "save_feedback",
        lambda payload: {"id": "test-feedback", "destination": payload["destination"]},
    )
    monkeypatch.setattr(app, "get_recent_requests", lambda kind, limit=3: [])
    monkeypatch.setattr(app, "get_request_count", lambda kind: 0)
    monkeypatch.setattr(
        app,
        "get_feedback_summary",
        lambda destination=None: {
            "sampleCount": 4 if destination else 6,
            "acceptanceRate": 0.75,
            "averageRating": 4.25,
            "verdictCounts": {"accepted": 3, "replanned": 1, "rejected": 0},
            "globalAcceptanceRate": 0.72,
            "globalSampleCount": 6,
        },
    )
    monkeypatch.setattr(
        app,
        "get_feedback_training_events",
        lambda: [
            {
                "createdAt": "2026-04-01T00:00:00+00:00",
                "destination": "Tokyo",
                "verdict": "accepted",
                "rating": 5,
                "requestPayload": {
                    "destination": "Tokyo",
                    "budget": 1800,
                    "currency": "USD",
                    "duration": 4,
                    "interests": ["food", "culture", "walkable"],
                    "travelStyle": "Balanced Explorer",
                    "pace": "balanced",
                },
            },
            {
                "createdAt": "2026-04-02T00:00:00+00:00",
                "destination": "Bangkok",
                "verdict": "accepted",
                "rating": 4,
                "requestPayload": {
                    "destination": "Bangkok",
                    "budget": 1400,
                    "currency": "USD",
                    "duration": 4,
                    "interests": ["food", "local", "nightlife"],
                    "travelStyle": "Food Scout",
                    "pace": "balanced",
                },
            },
        ],
    )
    app.REASONING_ENGINE.calibration_engine.feedback_summary_provider = app.get_feedback_summary
    app.REASONING_ENGINE.feedback_training_provider = app.get_feedback_training_events
    app.REASONING_ENGINE.refresh_learning_artifacts()

    server = app.ThreadingHTTPServer(("127.0.0.1", 0), app.MindGridHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        yield f"http://127.0.0.1:{port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def request_json(
    base_url: str,
    path: str,
    *,
    method: str = "GET",
    payload: dict | None = None,
    raw_body: bytes | None = None,
) -> tuple[int, dict]:
    body = raw_body if raw_body is not None else None
    headers = {"Accept": "application/json"}

    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(
        f"{base_url}{path}",
        data=body,
        headers=headers,
        method=method,
    )

    try:
        with urllib.request.urlopen(request) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode("utf-8"))
