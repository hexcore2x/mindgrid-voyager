from __future__ import annotations

import json

from engines.llm_gateway import LLMGateway, LLMGatewayConfig


class _FakeResponse:
    def __init__(self, payload: dict) -> None:
        self._payload = payload

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None


def test_llm_gateway_status_defaults_to_local_fallback() -> None:
    gateway = LLMGateway(config=LLMGatewayConfig())

    status = gateway.status()

    assert status["provider"] == "local"
    assert status["liveReady"] is False
    assert status["mode"] == "local-fallback"


def test_llm_gateway_parses_openai_style_response(monkeypatch) -> None:
    gateway = LLMGateway(
        config=LLMGatewayConfig(
            provider="openai",
            endpoint="https://api.openai.com/v1/chat/completions",
            api_key="test-key",
            model="test-model",
        )
    )

    def fake_urlopen(request, timeout=0):  # noqa: ANN001
        return _FakeResponse(
            {
                "choices": [
                    {
                        "message": {
                            "content": json.dumps(
                                {
                                    "executiveBrief": "Live provider summary",
                                    "decisionMemo": "Live provider memo",
                                    "assistantReply": "Live provider reply",
                                    "nextPromptSuggestions": ["Prompt A", "Prompt B"],
                                }
                            )
                        }
                    }
                ]
            }
        )

    monkeypatch.setattr("engines.llm_gateway.urllib_request.urlopen", fake_urlopen)

    payload = gateway.generate_decision_layer(
        request={"destination": "Tokyo", "travelStyle": "Balanced Explorer", "duration": 4},
        recommendation={"decisionEngine": {"priority_level": "High", "confidence": 0.92, "decision_score": 91.8}},
        destination_landscape={"topRanked": {"destination": "Tokyo"}},
    )

    assert payload["provider"] == "openai"
    assert payload["model"] == "test-model"
    assert payload["assistantReply"] == "Live provider reply"
