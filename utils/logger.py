from __future__ import annotations

import json
import logging
import logging.handlers
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "logs"
LOG_FILE = LOG_DIR / "app.log"


def get_app_logger(name: str = "mindgrid_voyager") -> logging.Logger:
    """Configure a rotating file logger once and fail safely if logging setup breaks."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        handler = logging.handlers.RotatingFileHandler(
            LOG_FILE,
            maxBytes=1_000_000,
            backupCount=3,
            encoding="utf-8",
        )
        handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        logger.propagate = False
    except OSError:
        # Logging should never prevent the server from starting.
        logger.addHandler(logging.NullHandler())

    return logger


def log_request(
    logger: logging.Logger,
    *,
    method: str,
    endpoint: str,
    status: int,
    duration_ms: float,
    error_message: str = "",
) -> None:
    level = logging.ERROR if status >= 500 else logging.WARNING if status >= 400 else logging.INFO
    _safe_log(
        logger,
        level,
        event="request",
        method=method,
        endpoint=endpoint,
        status=status,
        duration_ms=round(duration_ms, 2),
        error=error_message,
    )


def log_error(
    logger: logging.Logger,
    *,
    method: str,
    endpoint: str,
    status: int,
    duration_ms: float,
    error_message: str,
) -> None:
    _safe_log(
        logger,
        logging.ERROR if status >= 500 else logging.WARNING,
        event="error",
        method=method,
        endpoint=endpoint,
        status=status,
        duration_ms=round(duration_ms, 2),
        error=error_message,
    )


def log_decision_run(
    logger: logging.Logger,
    *,
    endpoint: str,
    status: int,
    duration_ms: float,
    destination: str,
    trace_id: str = "",
    request_id: str = "",
    decision_score: float | None = None,
    error_message: str = "",
) -> None:
    level = logging.ERROR if status >= 500 else logging.INFO
    _safe_log(
        logger,
        level,
        event="decision_run",
        endpoint=endpoint,
        status=status,
        duration_ms=round(duration_ms, 2),
        destination=destination,
        trace_id=trace_id,
        request_id=request_id,
        decision_score=decision_score,
        error=error_message,
    )


def _safe_log(logger: logging.Logger, level: int, **payload: Any) -> None:
    """Serialize structured log data without letting logging failures crash the server."""
    try:
        cleaned = {key: value for key, value in payload.items() if value not in (None, "")}
        logger.log(level, json.dumps(cleaned, ensure_ascii=True, default=str))
    except Exception:
        # Swallow logging failures intentionally so request handling stays safe.
        return
