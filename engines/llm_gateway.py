from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
import re
from typing import Any
from urllib import error as urllib_error
from urllib import request as urllib_request


@dataclass(slots=True)
class LLMGatewayConfig:
    provider: str = "local"
    endpoint: str = ""
    api_key: str = ""
    model: str = "mindgrid-local-copilot"
    timeout_ms: int = 5_000

    @classmethod
    def from_env(cls) -> "LLMGatewayConfig":
        timeout_raw = os.environ.get("MINDGRID_LLM_TIMEOUT_MS", "5000")
        try:
            timeout_ms = max(1_000, min(int(timeout_raw), 30_000))
        except ValueError:
            timeout_ms = 5_000

        api_key = os.environ.get("MINDGRID_LLM_API_KEY", "").strip() or os.environ.get("OPENAI_API_KEY", "").strip()
        configured_provider = os.environ.get("MINDGRID_LLM_PROVIDER", "").strip().lower()
        endpoint = os.environ.get("MINDGRID_LLM_ENDPOINT", "").strip()
        model = os.environ.get("MINDGRID_LLM_MODEL", "").strip() or os.environ.get("OPENAI_MODEL", "").strip()

        if configured_provider:
            provider = configured_provider
        elif api_key and not endpoint:
            provider = "openai"
        elif endpoint:
            provider = "custom"
        else:
            provider = "local"

        if provider == "openai" and not endpoint:
            endpoint = "https://api.openai.com/v1/chat/completions"

        return cls(
            provider=provider,
            endpoint=endpoint,
            api_key=api_key,
            model=model or ("gpt-4o-mini" if provider == "openai" else "mindgrid-local-copilot"),
            timeout_ms=timeout_ms,
        )


class LLMGateway:
    """Model-ready generation layer with a safe local fallback."""

    VERSION = "llm-gateway-v1"

    def __init__(
        self,
        *,
        config: LLMGatewayConfig | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        self.config = config or LLMGatewayConfig.from_env()
        self.logger = logger or logging.getLogger("mindgrid_voyager")

    def status(self) -> dict[str, Any]:
        provider = self.config.provider or "local"
        live_ready = provider != "local" and bool(self.config.endpoint)
        if provider == "openai":
            live_ready = live_ready and bool(self.config.api_key)

        return {
            "provider": provider,
            "liveReady": live_ready,
            "endpointConfigured": bool(self.config.endpoint),
            "model": self.config.model,
            "mode": "live-provider" if live_ready else "local-fallback",
        }

    def generate_decision_layer(
        self,
        *,
        request: dict[str, Any],
        recommendation: dict[str, Any],
        destination_landscape: dict[str, Any],
    ) -> dict[str, Any]:
        prompt_payload = {
            "task": "decision-layer",
            "request": request,
            "decisionEngine": recommendation.get("decisionEngine", {}),
            "summary": recommendation.get("destinationSummary", {}),
            "landscape": destination_landscape,
        }
        remote = self._call_remote(prompt_payload)
        if remote:
            return remote
        return self._build_local_decision_layer(request, recommendation, destination_landscape)

    def generate_replan_layer(
        self,
        *,
        base_request: dict[str, Any],
        updated_request: dict[str, Any],
        instruction: str,
        applied_adjustments: list[str],
        recommendation: dict[str, Any],
    ) -> dict[str, Any]:
        prompt_payload = {
            "task": "replan-layer",
            "baseRequest": base_request,
            "updatedRequest": updated_request,
            "instruction": instruction,
            "appliedAdjustments": applied_adjustments,
            "decisionEngine": recommendation.get("decisionEngine", {}),
        }
        remote = self._call_remote(prompt_payload)
        if remote:
            return remote
        return self._build_local_replan_layer(
            base_request=base_request,
            updated_request=updated_request,
            instruction=instruction,
            applied_adjustments=applied_adjustments,
            recommendation=recommendation,
        )

    def _call_remote(self, payload: dict[str, Any]) -> dict[str, Any] | None:
        provider = (self.config.provider or "local").lower()
        if provider == "local":
            return None
        if not self.config.endpoint:
            return None

        if provider == "openai":
            return self._call_openai(payload)

        return self._call_custom_endpoint(payload)

    def _call_openai(self, payload: dict[str, Any]) -> dict[str, Any] | None:
        if not self.config.api_key:
            return None

        request_body = {
            "model": self.config.model,
            "response_format": {"type": "json_object"},
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are MindGrid Voyager's decision copilot. Return JSON only with these keys: "
                        "executiveBrief, decisionMemo, assistantReply, nextPromptSuggestions. "
                        "nextPromptSuggestions must be an array of short strings."
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps(payload, ensure_ascii=True),
                },
            ],
        }

        remote_payload = self._post_json(self.config.endpoint, request_body)
        if not isinstance(remote_payload, dict):
            return None

        content = (
            remote_payload.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )
        extracted = self._extract_json_payload(content)
        if not extracted:
            return None

        return {
            "mode": "remote-llm",
            "provider": "openai",
            "model": self.config.model,
            **extracted,
        }

    def _call_custom_endpoint(self, payload: dict[str, Any]) -> dict[str, Any] | None:
        remote_payload = self._post_json(self.config.endpoint, payload)
        if not isinstance(remote_payload, dict):
            return None

        return {
            "mode": "remote-llm",
            "provider": "configured-endpoint",
            "model": self.config.model,
            **remote_payload,
        }

    def _post_json(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any] | None:
        try:
            request = urllib_request.Request(
                endpoint,
                data=json.dumps(payload).encode("utf-8"),
                headers=self._headers(),
                method="POST",
            )
            with urllib_request.urlopen(request, timeout=self.config.timeout_ms / 1000) as response:
                remote_payload = json.loads(response.read().decode("utf-8"))
        except (OSError, ValueError, json.JSONDecodeError, urllib_error.URLError) as exc:
            self.logger.warning("LLM gateway fallback engaged | provider=%s | endpoint=%s | error=%s", self.config.provider, endpoint, exc)
            return None

        return remote_payload if isinstance(remote_payload, dict) else None

    def _headers(self) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        return headers

    def _extract_json_payload(self, value: Any) -> dict[str, Any] | None:
        if isinstance(value, list):
            value = "".join(
                part.get("text", "")
                for part in value
                if isinstance(part, dict)
            )

        text = str(value or "").strip()
        if not text:
            return None

        try:
            parsed = json.loads(text)
            return parsed if isinstance(parsed, dict) else None
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", text, flags=re.DOTALL)
            if not match:
                return None
            try:
                parsed = json.loads(match.group(0))
            except json.JSONDecodeError:
                return None
            return parsed if isinstance(parsed, dict) else None

    def _build_local_decision_layer(
        self,
        request: dict[str, Any],
        recommendation: dict[str, Any],
        destination_landscape: dict[str, Any],
    ) -> dict[str, Any]:
        decision = recommendation.get("decisionEngine", {})
        summary = recommendation.get("destinationSummary", {})
        top_ranked = destination_landscape.get("topRanked", {})
        confidence_percent = self._confidence_percent(decision.get("confidence", 0))
        score = float(decision.get("decision_score", 0))
        best_for = recommendation.get("supportingSignals", {}).get("bestFor", [])

        executive_brief = (
            f"{request['destination']} stays at the top because score, safety, and route relevance all converge "
            f"around the same recommendation. The engine sees this as a {decision.get('priority_level', 'Medium').lower()}-priority "
            f"mission with {confidence_percent}% confidence."
        )
        decision_memo = (
            f"The current brief favors {request['travelStyle'].lower()} travel across {request['duration']} days. "
            f"{summary.get('whyThisWorks', 'The destination fit stayed strong.')} Compared with the seeded landscape, "
            f"{top_ranked.get('destination', request['destination'])} maintained the strongest defendable score at {score:.2f}."
        )
        assistant_reply = (
            f"If you want the engine to adapt this plan next, ask for a replan like 'make it cheaper', "
            f"'lean more into food', or 'shift toward a slower pace'."
        )
        next_prompts = [
            f"Make {request['destination']} more budget-friendly without losing the best food stops.",
            f"Rebuild {request['destination']} for a slower and safer version of the trip.",
            f"Push this plan further toward {best_for[0].lower()}." if best_for else f"Refine {request['destination']} for a more focused version.",
        ]

        return {
            "mode": "local-simulated-llm",
            "provider": "mindgrid-local",
            "model": self.config.model,
            "executiveBrief": executive_brief,
            "decisionMemo": decision_memo,
            "assistantReply": assistant_reply,
            "nextPromptSuggestions": next_prompts[:3],
        }

    def _build_local_replan_layer(
        self,
        *,
        base_request: dict[str, Any],
        updated_request: dict[str, Any],
        instruction: str,
        applied_adjustments: list[str],
        recommendation: dict[str, Any],
    ) -> dict[str, Any]:
        decision = recommendation.get("decisionEngine", {})
        confidence_percent = self._confidence_percent(decision.get("confidence", 0))
        destination_changed = base_request["destination"].lower() != updated_request["destination"].lower()
        destination_note = (
            f"The destination changed from {base_request['destination']} to {updated_request['destination']}."
            if destination_changed
            else f"The destination stayed on {updated_request['destination']} and the trip logic was retuned instead."
        )

        return {
            "mode": "local-simulated-llm",
            "provider": "mindgrid-local",
            "model": self.config.model,
            "executiveBrief": (
                f"The replan interpreted '{instruction}' and translated it into {len(applied_adjustments)} concrete trip adjustments."
            ),
            "decisionMemo": (
                f"{destination_note} The refreshed plan now targets a {updated_request['pace']} pace and "
                f"{updated_request['travelStyle'].lower()} positioning with {confidence_percent}% confidence."
            ),
            "assistantReply": (
                f"I adjusted the brief, reran the decision engine, and returned a cleaner version of the trip. "
                f"Ask again if you want it more premium, more local, safer, or more food-focused."
            ),
            "nextPromptSuggestions": [
                f"Make this even more local than the current {updated_request['destination']} plan.",
                "Reduce transit friction and protect only the highest-signal experiences.",
                "Generate a safety-first evening version of this trip.",
            ],
        }

    def _confidence_percent(self, value: Any) -> int:
        numeric = float(value or 0)
        if numeric <= 1:
            return round(numeric * 100)
        return round(numeric)
