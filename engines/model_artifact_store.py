from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = ROOT / "data" / "model_artifacts"


class ModelArtifactStore:
    """Persists lightweight model artifacts for local-first training workflows."""

    def __init__(self, artifact_dir: Path | None = None) -> None:
        self.artifact_dir = artifact_dir or ARTIFACT_DIR
        self.artifact_dir.mkdir(parents=True, exist_ok=True)

    def artifact_path(self, name: str) -> Path:
        return self.artifact_dir / name

    def load_json(self, name: str) -> dict[str, Any] | None:
        path = self.artifact_path(name)
        if not path.exists():
            return None

        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None

        if not isinstance(payload, dict):
            return None
        return payload

    def save_json(self, name: str, payload: dict[str, Any]) -> None:
        path = self.artifact_path(name)
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
