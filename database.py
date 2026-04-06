from __future__ import annotations

import json
import sqlite3
from datetime import datetime, UTC
from pathlib import Path
from typing import Any
from uuid import uuid4

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "mindgrid_voyager.db"
DEMO_JSON_PATH = DATA_DIR / "demo_requests.json"


def _ensure_paths() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    if not DEMO_JSON_PATH.exists():
        DEMO_JSON_PATH.write_text("[]\n", encoding="utf-8")


def _connect() -> sqlite3.Connection:
    _ensure_paths()
    connection = sqlite3.connect(str(DB_PATH), timeout=30)
    connection.row_factory = sqlite3.Row
    # Memory-backed journaling behaves more reliably in constrained local environments
    # while still preserving the simple local persistence model we want here.
    connection.execute("PRAGMA journal_mode=MEMORY;")
    connection.execute("PRAGMA synchronous=NORMAL;")
    return connection


def init_db() -> None:
    with _connect() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS demo_requests (
                id TEXT PRIMARY KEY,
                submitted_at TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                destination TEXT,
                travel_style TEXT,
                notes TEXT
            );

            CREATE TABLE IF NOT EXISTS recommendation_requests (
                id TEXT PRIMARY KEY,
                submitted_at TEXT NOT NULL,
                destination TEXT NOT NULL,
                budget INTEGER NOT NULL,
                duration INTEGER NOT NULL,
                interests_json TEXT NOT NULL,
                travel_style TEXT NOT NULL,
                pace TEXT NOT NULL,
                request_payload_json TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS generated_results (
                id TEXT PRIMARY KEY,
                recommendation_request_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                engine_version TEXT NOT NULL,
                destination TEXT NOT NULL,
                response_json TEXT NOT NULL,
                FOREIGN KEY(recommendation_request_id) REFERENCES recommendation_requests(id)
            );

            CREATE TABLE IF NOT EXISTS feedback_events (
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                trace_id TEXT,
                destination TEXT NOT NULL,
                verdict TEXT NOT NULL,
                rating INTEGER NOT NULL,
                notes TEXT,
                payload_json TEXT NOT NULL
            );
            """
        )


def check_db_connection() -> bool:
    """Return True when SQLite accepts a simple query."""
    try:
        with _connect() as connection:
            connection.execute("SELECT 1").fetchone()
        return True
    except sqlite3.Error:
        return False


def _append_demo_json(record: dict[str, Any]) -> None:
    _ensure_paths()
    try:
        existing = json.loads(DEMO_JSON_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        existing = []

    existing.append(record)
    DEMO_JSON_PATH.write_text(json.dumps(existing, indent=2), encoding="utf-8")


def save_demo_request(payload: dict[str, Any]) -> dict[str, Any]:
    record = {
        "id": uuid4().hex[:10],
        "submittedAt": datetime.now(UTC).isoformat(),
        "name": payload["name"],
        "email": payload["email"],
        "destination": payload.get("destination", ""),
        "travelStyle": payload.get("travelStyle", ""),
        "notes": payload.get("notes", ""),
    }

    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO demo_requests (id, submitted_at, name, email, destination, travel_style, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["id"],
                record["submittedAt"],
                record["name"],
                record["email"],
                record["destination"],
                record["travelStyle"],
                record["notes"],
            ),
        )

    _append_demo_json(record)
    return record


def save_recommendation_request(payload: dict[str, Any], response: dict[str, Any]) -> dict[str, str]:
    request_id = uuid4().hex[:12]
    result_id = uuid4().hex[:12]
    submitted_at = datetime.now(UTC).isoformat()

    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO recommendation_requests (
                id, submitted_at, destination, budget, duration, interests_json, travel_style, pace, request_payload_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                request_id,
                submitted_at,
                payload["destination"],
                payload["budget"],
                payload["duration"],
                json.dumps(payload["interests"]),
                payload["travelStyle"],
                payload["pace"],
                json.dumps(payload),
            ),
        )
        connection.execute(
            """
            INSERT INTO generated_results (
                id, recommendation_request_id, created_at, engine_version, destination, response_json
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                result_id,
                request_id,
                submitted_at,
                response["meta"]["engineVersion"],
                response["request"]["destination"],
                json.dumps(response),
            ),
        )

    return {
        "requestId": request_id,
        "resultId": result_id,
    }


def get_request_count(kind: str) -> int:
    table_map = {
        "demo": "demo_requests",
        "recommendation": "recommendation_requests",
    }
    if kind not in table_map:
        raise ValueError("kind must be either 'demo' or 'recommendation'")

    with _connect() as connection:
        row = connection.execute(f"SELECT COUNT(*) AS count FROM {table_map[kind]}").fetchone()
    return int(row["count"])


def get_recent_requests(kind: str, limit: int = 5) -> list[dict[str, Any]]:
    query_map = {
        "demo": (
            "SELECT id, submitted_at, name, email, destination, travel_style, notes "
            "FROM demo_requests ORDER BY submitted_at DESC LIMIT ?"
        ),
        "recommendation": (
            "SELECT id, submitted_at, destination, budget, duration, interests_json, travel_style, pace "
            "FROM recommendation_requests ORDER BY submitted_at DESC LIMIT ?"
        ),
    }
    if kind not in query_map:
        raise ValueError("kind must be either 'demo' or 'recommendation'")

    with _connect() as connection:
        rows = connection.execute(query_map[kind], (limit,)).fetchall()

    results: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        if "interests_json" in item:
            item["interests"] = json.loads(item.pop("interests_json"))
        results.append(item)
    return results


def save_feedback(payload: dict[str, Any]) -> dict[str, Any]:
    record = {
        "id": uuid4().hex[:12],
        "createdAt": datetime.now(UTC).isoformat(),
        "traceId": payload.get("traceId", ""),
        "destination": payload["destination"],
        "verdict": payload["verdict"],
        "rating": int(payload["rating"]),
        "notes": payload.get("notes", ""),
    }

    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO feedback_events (id, created_at, trace_id, destination, verdict, rating, notes, payload_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["id"],
                record["createdAt"],
                record["traceId"],
                record["destination"],
                record["verdict"],
                record["rating"],
                record["notes"],
                json.dumps(payload),
            ),
        )

    return record


def get_feedback_summary(destination: str | None = None) -> dict[str, Any]:
    filters = []
    params: list[Any] = []
    if destination:
        filters.append("destination = ?")
        params.append(destination)

    where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

    with _connect() as connection:
        rows = connection.execute(
            f"""
            SELECT verdict, rating
            FROM feedback_events
            {where_clause}
            ORDER BY created_at DESC
            """,
            params,
        ).fetchall()
        global_rows = connection.execute(
            """
            SELECT verdict, rating
            FROM feedback_events
            ORDER BY created_at DESC
            """
        ).fetchall()

    summary = _summarize_feedback_rows(rows)
    global_summary = _summarize_feedback_rows(global_rows)
    return {
        **summary,
        "globalAcceptanceRate": global_summary["acceptanceRate"],
        "globalSampleCount": global_summary["sampleCount"],
    }


def get_feedback_training_events(limit: int = 200) -> list[dict[str, Any]]:
    with _connect() as connection:
        rows = connection.execute(
            """
            SELECT id, created_at, destination, verdict, rating, payload_json
            FROM feedback_events
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    results: list[dict[str, Any]] = []
    for row in rows:
        try:
            payload = json.loads(str(row["payload_json"]))
        except json.JSONDecodeError:
            payload = {}
        request_payload = payload.get("requestPayload") or payload.get("request_payload")
        results.append(
            {
                "id": row["id"],
                "createdAt": row["created_at"],
                "destination": row["destination"],
                "verdict": row["verdict"],
                "rating": int(row["rating"]),
                "requestPayload": request_payload if isinstance(request_payload, dict) else None,
            }
        )
    return results


def _summarize_feedback_rows(rows: list[sqlite3.Row]) -> dict[str, Any]:
    sample_count = len(rows)
    verdict_counts = {
        "accepted": 0,
        "replanned": 0,
        "rejected": 0,
    }
    ratings: list[int] = []
    for row in rows:
        verdict = str(row["verdict"])
        if verdict in verdict_counts:
            verdict_counts[verdict] += 1
        ratings.append(int(row["rating"]))

    acceptance_rate = round(
        ((verdict_counts["accepted"] + (verdict_counts["replanned"] * 0.5)) / sample_count),
        3,
    ) if sample_count else 0.0
    average_rating = round(sum(ratings) / sample_count, 2) if ratings else 0.0

    return {
        "sampleCount": sample_count,
        "acceptanceRate": acceptance_rate,
        "averageRating": average_rating,
        "verdictCounts": verdict_counts,
    }
