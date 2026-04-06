from __future__ import annotations

from tests.conftest import request_json


def test_health_endpoint_returns_database_status_and_uptime(api_server: str) -> None:
    status, payload = request_json(api_server, "/health")

    assert status == 200
    assert payload["success"] is True
    assert payload["status"] == "ok"
    assert payload["database"] == "connected"
    assert payload["version"] == "1.0"
    assert "timestamp" in payload
    assert "uptimeSeconds" in payload
    assert "llmProvider" in payload
    assert "llmMode" in payload
    assert "llmReady" in payload
    assert "llmModel" in payload


def test_valid_recommendation_request_returns_success(api_server: str) -> None:
    status, payload = request_json(
        api_server,
        "/api/recommendations",
        method="POST",
        payload={
            "destination": "Tokyo",
            "budget": 1800,
            "currency": "EUR",
            "duration": 4,
            "interests": ["food", "culture"],
            "travelStyle": "Balanced Explorer",
            "pace": "balanced",
        },
    )

    assert status == 200
    assert payload["success"] is True
    assert payload["recommendation"]["request"]["destination"] == "Tokyo"
    assert payload["recommendation"]["request"]["currency"] == "EUR"
    assert payload["recommendation"]["budgetGuidance"]["currency"] == "EUR"
    assert payload["recommendation"]["agenticExperience"]["mode"] == "local-template-generation"
    assert payload["recommendation"]["agenticExperience"]["missionBrief"]["title"]
    assert payload["recommendation"]["agenticExperience"]["agentPlaybook"]["nextActions"]
    assert payload["recommendation"]["agenticExperience"]["memoryDraft"]["journalPreview"]
    assert payload["recommendation"]["agenticExperience"]["modelLayer"]["provider"]
    assert payload["recommendation"]["grounding"]["method"] == "seeded-evidence-retrieval"
    assert payload["recommendation"]["grounding"]["contentGroundingMode"] == "seeded-passages"
    assert payload["recommendation"]["grounding"]["destinationEvidence"]
    assert payload["recommendation"]["grounding"]["metrics"]["contentGroundedDocuments"] >= 1
    assert payload["recommendation"]["grounding"]["destinationEvidence"][0]["contentGrounded"] is True
    assert payload["recommendation"]["grounding"]["destinationEvidence"][0]["contentMode"] == "seeded-passage"
    assert payload["recommendation"]["modelDiagnostics"]["version"] == "ranking-model-v3-blended-explainability"
    assert payload["recommendation"]["modelDiagnostics"]["featureBreakdown"]
    assert payload["recommendation"]["modelDiagnostics"]["scoringPipeline"]["mode"] == "blended-prior-plus-learned"
    assert payload["recommendation"]["modelDiagnostics"]["scoringPipeline"]["prior"]["weight"] == 0.54
    assert payload["recommendation"]["modelDiagnostics"]["scoringPipeline"]["learned"]["weight"] == 0.46
    assert payload["recommendation"]["modelDiagnostics"]["layerBreakdown"]["priorFeatureBreakdown"]
    assert payload["recommendation"]["modelDiagnostics"]["layerBreakdown"]["learnedFeatureBreakdown"]
    assert "priorContribution" in payload["recommendation"]["modelDiagnostics"]["featureBreakdown"][0]
    assert "learnedContribution" in payload["recommendation"]["modelDiagnostics"]["featureBreakdown"][0]
    assert payload["recommendation"]["modelDiagnostics"]["trainingSummary"]["sampleCount"] >= 12
    assert payload["recommendation"]["intentDiagnostics"]["matchedInterestTokens"]
    assert payload["recommendation"]["sourceVerification"]["verificationSummary"]["status"]
    assert payload["recommendation"]["sourceVerification"]["verificationSummary"]["contentPolicy"] == "seeded-passages-plus-official-api-snippets"
    assert payload["recommendation"]["sourceVerification"]["citations"]
    assert payload["recommendation"]["socialReferences"]["overview"][0]["platform"] == "YouTube"
    assert payload["recommendation"]["topAttractions"][0]["references"]
    assert payload["recommendation"]["foodAndCafes"][0]["references"][0]["url"].startswith("https://")
    assert payload["recommendation"]["dayWiseItinerary"][0]["references"][0]["platform"] in {"YouTube", "Reddit"}


def test_invalid_budget_returns_error(api_server: str) -> None:
    status, payload = request_json(
        api_server,
        "/api/recommendations",
        method="POST",
        payload={
            "destination": "Tokyo",
            "budget": -50,
            "duration": 4,
            "interests": ["food"],
            "travelStyle": "Balanced Explorer",
            "pace": "balanced",
        },
    )

    assert status == 400
    assert payload == {
        "success": False,
        "error": "Invalid input",
        "details": "Budget must be a positive number.",
    }


def test_invalid_currency_returns_error(api_server: str) -> None:
    status, payload = request_json(
        api_server,
        "/api/recommendations",
        method="POST",
        payload={
            "destination": "Tokyo",
            "budget": 1800,
            "currency": "BTC",
            "duration": 4,
            "interests": ["food"],
            "travelStyle": "Balanced Explorer",
            "pace": "balanced",
        },
    )

    assert status == 400
    assert payload["success"] is False
    assert payload["error"] == "Invalid input"
    assert "Currency must be one of" in payload["details"]


def test_missing_destination_returns_error(api_server: str) -> None:
    status, payload = request_json(
        api_server,
        "/api/recommendations",
        method="POST",
        payload={
            "destination": "",
            "budget": 1800,
            "duration": 4,
            "interests": ["food"],
            "travelStyle": "Balanced Explorer",
            "pace": "balanced",
        },
    )

    assert status == 400
    assert payload["success"] is False
    assert payload["details"] == "Destination must be a non-empty string."


def test_comparison_with_multiple_destinations_works(api_server: str) -> None:
    status, payload = request_json(
        api_server,
        "/api/comparison",
        method="POST",
        payload={
            "destinations": ["Tokyo", "Bangkok", "Singapore"],
            "budget": 1800,
            "duration": 4,
            "interests": ["food", "culture"],
            "travelStyle": "Balanced Explorer",
            "pace": "balanced",
        },
    )

    assert status == 200
    assert payload["success"] is True
    assert payload["comparison"]["totalCompared"] == 3
    assert len(payload["comparison"]["results"]) == 3
    assert payload["comparison"]["results"][0]["decisionScore"] >= payload["comparison"]["results"][1]["decisionScore"]


def test_evaluation_endpoint_returns_benchmark_summary(api_server: str) -> None:
    status, payload = request_json(api_server, "/api/evaluation")

    assert status == 200
    assert payload["success"] is True
    assert payload["evaluation"]["version"] == "evaluation-engine-v3"
    assert payload["evaluation"]["headlineMode"] == "out-of-sample-temporal-backtest"
    assert payload["evaluation"]["summary"]["caseCount"] >= 12
    assert payload["evaluation"]["summary"]["benchmarkCaseCount"] >= 24
    assert payload["evaluation"]["summary"]["top1Accuracy"] >= 90
    assert payload["evaluation"]["summary"]["top3Coverage"] >= 95
    assert payload["evaluation"]["summary"]["averageGroundingCoverage"] >= 80
    assert payload["evaluation"]["learning"]["rankingModel"]["sampleCount"] >= 12
    assert payload["evaluation"]["summary"]["brierScore"] >= 0
    assert payload["evaluation"]["temporalValidation"]["status"] == "completed"
    assert payload["evaluation"]["temporalValidation"]["summary"]["top1Accuracy"] >= 85
    assert payload["evaluation"]["generalizationBacktest"]["status"] == "completed"
    assert payload["evaluation"]["ablationStudy"]
    assert payload["evaluation"]["sliceMetrics"]["difficulty"]


def test_feedback_endpoint_saves_local_calibration_signal(api_server: str) -> None:
    status, payload = request_json(
        api_server,
        "/api/feedback",
        method="POST",
        payload={
            "destination": "Tokyo",
            "traceId": "trace-123",
            "verdict": "accepted",
            "rating": 5,
            "notes": "Strong fit for the brief.",
            "requestPayload": {
                "destination": "Tokyo",
                "budget": 1800,
                "currency": "USD",
                "duration": 4,
                "interests": ["food", "culture"],
                "travelStyle": "Balanced Explorer",
                "pace": "balanced",
            },
        },
    )

    assert status == 201
    assert payload["success"] is True
    assert payload["feedbackId"] == "test-feedback"
    assert payload["feedbackSummary"]["sampleCount"] >= 4
    assert payload["feedbackSummary"]["acceptanceRate"] >= 0.7
    assert payload["learningRefresh"]["status"] == "refreshed"
    assert payload["learningRefresh"]["feedbackApplied"] is True
    assert payload["learningRefresh"]["feedbackTrainable"] is True
    assert payload["learningRefresh"]["feedbackSamples"] >= 3
    assert payload["learningRefresh"]["totalSamples"] >= payload["learningRefresh"]["benchmarkSamples"]


def test_replan_request_returns_updated_recommendation(api_server: str) -> None:
    status, payload = request_json(
        api_server,
        "/api/replan",
        method="POST",
        payload={
            "baseRequest": {
                "destination": "Tokyo",
                "budget": 1800,
                "duration": 4,
                "interests": ["food", "culture"],
                "travelStyle": "Balanced Explorer",
                "pace": "balanced",
            },
            "instruction": "make it cheaper and more food-focused",
        },
    )

    assert status == 200
    assert payload["success"] is True
    assert payload["replan"]["updatedRequest"]["travelStyle"] == "Food Scout"
    assert payload["replan"]["updatedRequest"]["budget"] < 1800
    assert payload["replan"]["recommendation"]["decisionEngine"]["traceId"]
    assert payload["replan"]["modelLayer"]["assistantReply"]


def test_malformed_input_does_not_crash_server(api_server: str) -> None:
    bad_status, bad_payload = request_json(
        api_server,
        "/api/recommendations",
        method="POST",
        raw_body=b'{"destination": "Tokyo", "budget": ',
    )

    good_status, good_payload = request_json(
        api_server,
        "/api/recommendations",
        method="POST",
        payload={
            "destination": "Paris",
            "budget": 1800,
            "duration": 4,
            "interests": ["culture"],
            "travelStyle": "Culture First",
            "pace": "balanced",
        },
    )

    assert bad_status == 400
    assert bad_payload["success"] is False
    assert bad_payload["details"] == "Request body must be valid JSON."
    assert good_status == 200
    assert good_payload["success"] is True
