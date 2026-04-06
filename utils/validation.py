from __future__ import annotations

import re
from typing import Any

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
ALLOWED_TRAVEL_STYLES = {
    "Balanced Explorer",
    "Food Scout",
    "Budget Hunter",
    "Luxury Escape",
    "Culture First",
}
ALLOWED_PACES = {"slow", "balanced", "fast"}
ALLOWED_CURRENCIES = {"USD", "EUR", "GBP", "INR", "JPY", "SGD", "AED", "THB", "IDR"}
ALLOWED_FEEDBACK_VERDICTS = {"accepted", "replanned", "rejected"}
CURRENCY_ALIASES = {
    "dollar": "USD",
    "dollars": "USD",
    "usd": "USD",
    "us dollar": "USD",
    "us dollars": "USD",
    "euro": "EUR",
    "euros": "EUR",
    "eur": "EUR",
    "pound": "GBP",
    "pounds": "GBP",
    "gbp": "GBP",
    "rupee": "INR",
    "rupees": "INR",
    "inr": "INR",
    "yen": "JPY",
    "jpy": "JPY",
    "sgd": "SGD",
    "singapore dollar": "SGD",
    "aed": "AED",
    "dirham": "AED",
    "thb": "THB",
    "baht": "THB",
    "idr": "IDR",
    "rupiah": "IDR",
}


class ValidationError(Exception):
    """Structured validation error used by the API layer."""

    def __init__(self, details: str, error: str = "Invalid input", status_code: int = 400) -> None:
        super().__init__(details)
        self.error = error
        self.details = details
        self.status_code = status_code


def build_success_response(**payload: Any) -> dict[str, Any]:
    """Keep existing fields while adding a consistent success flag."""
    return {"success": True, **payload}


def build_error_response(error: str, details: str) -> dict[str, Any]:
    return {
        "success": False,
        "error": error,
        "details": details,
    }


def validate_demo_request_payload(payload: dict[str, Any]) -> dict[str, str]:
    normalized = {
        "name": str(payload.get("name", "")).strip(),
        "email": str(payload.get("email", "")).strip(),
        "destination": str(payload.get("destination", "")).strip(),
        "travelStyle": str(payload.get("travelStyle", payload.get("travel_style", ""))).strip(),
        "notes": str(payload.get("notes", "")).strip(),
    }

    if not normalized["name"] or len(normalized["name"]) > 80:
        raise ValidationError("Name is required and must be 80 characters or fewer.")
    if not EMAIL_RE.match(normalized["email"]) or len(normalized["email"]) > 120:
        raise ValidationError("Email must be a valid address under 120 characters.")
    if len(normalized["destination"]) > 120:
        raise ValidationError("Destination must be 120 characters or fewer.")
    if len(normalized["travelStyle"]) > 60:
        raise ValidationError("Travel style must be 60 characters or fewer.")
    if len(normalized["notes"]) > 1200:
        raise ValidationError("Notes must be 1200 characters or fewer.")

    return normalized


def validate_recommendation_payload(payload: dict[str, Any]) -> dict[str, Any]:
    destination = _validate_destination(payload.get("destination"))
    budget = _validate_budget(payload.get("budget"))
    currency = _validate_currency(payload.get("currency"))
    duration = _validate_duration(payload.get("duration"))
    interests = _validate_interests(payload.get("interests"))
    travel_style = _validate_travel_style(payload.get("travelStyle", payload.get("travel_style")))
    pace = _validate_pace(payload.get("pace"))

    return {
        "destination": destination,
        "budget": budget,
        "currency": currency,
        "duration": duration,
        "interests": interests,
        "travelStyle": travel_style,
        "pace": pace,
    }


def validate_comparison_payload(payload: dict[str, Any]) -> dict[str, Any]:
    destinations = _validate_destinations(payload.get("destinations"))
    normalized = validate_recommendation_payload(
        {
            "destination": destinations[0],
            "budget": payload.get("budget"),
            "currency": payload.get("currency"),
            "duration": payload.get("duration"),
            "interests": payload.get("interests"),
            "travelStyle": payload.get("travelStyle", payload.get("travel_style")),
            "pace": payload.get("pace"),
        }
    )
    normalized.pop("destination", None)
    normalized["destinations"] = destinations
    return normalized


def validate_replan_payload(payload: dict[str, Any]) -> dict[str, Any]:
    base_request_raw = payload.get("baseRequest", payload.get("base_request"))
    if not isinstance(base_request_raw, dict):
        raise ValidationError("baseRequest must be a valid recommendation payload object.")

    instruction = str(payload.get("instruction", "")).strip()
    if not instruction:
        raise ValidationError("Instruction must be a non-empty string.")
    if len(instruction) > 500:
        raise ValidationError("Instruction must be 500 characters or fewer.")

    return {
        "baseRequest": validate_recommendation_payload(base_request_raw),
        "instruction": instruction,
    }


def validate_feedback_payload(payload: dict[str, Any]) -> dict[str, Any]:
    destination = _validate_destination(payload.get("destination"))
    verdict = str(payload.get("verdict", "")).strip().lower()
    if verdict not in ALLOWED_FEEDBACK_VERDICTS:
        allowed = ", ".join(sorted(ALLOWED_FEEDBACK_VERDICTS))
        raise ValidationError(f"Feedback verdict must be one of: {allowed}.")

    try:
        rating = int(payload.get("rating"))
    except (TypeError, ValueError) as exc:
        raise ValidationError("Feedback rating must be an integer between 1 and 5.") from exc

    if rating < 1 or rating > 5:
        raise ValidationError("Feedback rating must be an integer between 1 and 5.")

    notes = str(payload.get("notes", "")).strip()
    if len(notes) > 500:
        raise ValidationError("Feedback notes must be 500 characters or fewer.")

    trace_id = str(payload.get("traceId", payload.get("trace_id", ""))).strip()
    if trace_id and len(trace_id) > 64:
        raise ValidationError("traceId must be 64 characters or fewer.")

    request_payload = payload.get("requestPayload", payload.get("request_payload"))
    normalized_request_payload = None
    if request_payload is not None:
        if not isinstance(request_payload, dict):
            raise ValidationError("requestPayload must be a valid recommendation payload object.")
        normalized_request_payload = validate_recommendation_payload(request_payload)

    normalized = {
        "destination": destination,
        "verdict": verdict,
        "rating": rating,
        "notes": notes,
        "traceId": trace_id,
    }
    if normalized_request_payload is not None:
        normalized["requestPayload"] = normalized_request_payload
    return normalized


def validate_json_body_size(content_length: int) -> None:
    if content_length <= 0 or content_length > 32_000:
        raise ValidationError("Request body must be between 1 and 32000 bytes.")


def validate_json_payload_shape(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValidationError("Request body must be a JSON object.")
    return payload


def _validate_destination(value: Any) -> str:
    destination = str(value or "").strip()
    if not destination:
        raise ValidationError("Destination must be a non-empty string.")
    if len(destination) > 120:
        raise ValidationError("Destination must be 120 characters or fewer.")
    return destination


def _validate_budget(value: Any) -> float:
    try:
        budget = float(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError("Budget must be a positive number.") from exc

    if budget <= 0:
        raise ValidationError("Budget must be a positive number.")
    if budget > 100_000:
        raise ValidationError("Budget must be 100000 or less.")
    return int(budget) if budget.is_integer() else budget


def _validate_duration(value: Any) -> int:
    try:
        duration = int(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError("Duration must be an integer between 1 and 30.") from exc

    if duration < 1 or duration > 30:
        raise ValidationError("Duration must be an integer between 1 and 30.")
    return duration


def _validate_currency(value: Any) -> str:
    raw = str(value or "USD").strip().lower()
    currency = CURRENCY_ALIASES.get(raw, raw.upper())
    if currency not in ALLOWED_CURRENCIES:
        allowed = ", ".join(sorted(ALLOWED_CURRENCIES))
        raise ValidationError(f"Currency must be one of: {allowed}.")
    return currency


def _validate_interests(value: Any) -> list[str]:
    if isinstance(value, str):
        items = [item.strip().lower() for item in value.split(",") if item.strip()]
    elif isinstance(value, list):
        items = [str(item).strip().lower() for item in value if str(item).strip()]
    else:
        raise ValidationError("Interests must be a list or comma-separated string.")

    if not items:
        raise ValidationError("Interests must include at least one value.")
    return items[:6]


def _validate_travel_style(value: Any) -> str:
    travel_style = str(value or "Balanced Explorer").strip() or "Balanced Explorer"
    if travel_style not in ALLOWED_TRAVEL_STYLES:
        allowed = ", ".join(sorted(ALLOWED_TRAVEL_STYLES))
        raise ValidationError(f"Travel style must be one of: {allowed}.")
    return travel_style


def _validate_pace(value: Any) -> str:
    pace = str(value or "balanced").strip().lower() or "balanced"
    if pace not in ALLOWED_PACES:
        raise ValidationError("Pace must be one of: slow, balanced, fast.")
    return pace


def _validate_destinations(value: Any) -> list[str]:
    if isinstance(value, str):
        raw_items = value.split(",")
    elif isinstance(value, list):
        raw_items = value
    else:
        raise ValidationError("Destinations must be a list or comma-separated string.")

    seen: set[str] = set()
    destinations: list[str] = []
    for item in raw_items:
        destination = _validate_destination(item)
        normalized_key = destination.lower()
        if normalized_key in seen:
            continue
        seen.add(normalized_key)
        destinations.append(destination)

    if len(destinations) < 2 or len(destinations) > 4:
        raise ValidationError("Destinations must include between 2 and 4 unique values.")

    return destinations
