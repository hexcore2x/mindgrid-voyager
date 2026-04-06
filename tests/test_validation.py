from __future__ import annotations

import pytest

from utils.validation import (
    ValidationError,
    validate_comparison_payload,
    validate_feedback_payload,
    validate_replan_payload,
    validate_recommendation_payload,
)


def test_validate_recommendation_payload_accepts_comma_separated_interests() -> None:
    payload = validate_recommendation_payload(
        {
            "destination": "Tokyo",
            "budget": 1800,
            "currency": "eur",
            "duration": 4,
            "interests": "food, culture, walkable",
            "travelStyle": "Balanced Explorer",
            "pace": "balanced",
        }
    )

    assert payload["destination"] == "Tokyo"
    assert payload["currency"] == "EUR"
    assert payload["interests"] == ["food", "culture", "walkable"]


def test_validate_recommendation_payload_rejects_invalid_budget() -> None:
    with pytest.raises(ValidationError, match="Budget must be a positive number"):
        validate_recommendation_payload(
            {
                "destination": "Tokyo",
                "budget": -1,
                "duration": 4,
                "interests": ["food"],
                "travelStyle": "Balanced Explorer",
                "pace": "balanced",
            }
        )


def test_validate_recommendation_payload_rejects_invalid_currency() -> None:
    with pytest.raises(ValidationError, match="Currency must be one of"):
        validate_recommendation_payload(
            {
                "destination": "Tokyo",
                "budget": 1800,
                "currency": "btc",
                "duration": 4,
                "interests": ["food"],
                "travelStyle": "Balanced Explorer",
                "pace": "balanced",
            }
        )


def test_validate_comparison_payload_accepts_multiple_destinations() -> None:
    payload = validate_comparison_payload(
        {
            "destinations": "Tokyo, Bangkok, Singapore",
            "budget": 1800,
            "duration": 4,
            "interests": ["food", "culture"],
            "travelStyle": "Balanced Explorer",
            "pace": "balanced",
        }
    )

    assert payload["destinations"] == ["Tokyo", "Bangkok", "Singapore"]
    assert payload["travelStyle"] == "Balanced Explorer"


def test_validate_replan_payload_rejects_missing_instruction() -> None:
    with pytest.raises(ValidationError, match="Instruction must be a non-empty string"):
        validate_replan_payload(
            {
                "baseRequest": {
                    "destination": "Tokyo",
                    "budget": 1800,
                    "duration": 4,
                    "interests": ["food"],
                    "travelStyle": "Balanced Explorer",
                    "pace": "balanced",
                },
                "instruction": "",
            }
        )


def test_validate_feedback_payload_accepts_supported_feedback_shape() -> None:
    payload = validate_feedback_payload(
        {
            "destination": "Tokyo",
            "traceId": "trace-123",
            "verdict": "accepted",
            "rating": 4,
            "notes": "Useful recommendation.",
            "requestPayload": {
                "destination": "Tokyo",
                "budget": 1800,
                "currency": "USD",
                "duration": 4,
                "interests": ["food"],
                "travelStyle": "Balanced Explorer",
                "pace": "balanced",
            },
        }
    )

    assert payload["destination"] == "Tokyo"
    assert payload["verdict"] == "accepted"
    assert payload["rating"] == 4
    assert payload["requestPayload"]["travelStyle"] == "Balanced Explorer"
