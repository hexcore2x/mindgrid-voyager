from __future__ import annotations

from datetime import UTC, datetime
from typing import Any


class SourceVerificationEngine:
    """Creates traceable, source-aware verification data for the UI."""

    VERSION = "source-verification-v1"

    def verify(
        self,
        *,
        request: dict[str, Any],
        recommendation: dict[str, Any],
        destination_landscape: dict[str, Any],
    ) -> dict[str, Any]:
        meta = recommendation.get("meta", {})
        scores = meta.get("scores", {})
        supporting = recommendation.get("supportingSignals", {})
        workflow = recommendation.get("reasoningWorkflow", {})
        decision = recommendation.get("decisionEngine", {})
        social_references = recommendation.get("socialReferences", {})
        grounding = recommendation.get("grounding", {})
        grounding_metrics = grounding.get("metrics", {})
        destination_evidence = grounding.get("destinationEvidence", [])
        retrieval = grounding.get("retrieval", {})
        content_policy = retrieval.get("contentPolicy", {})

        sources = list(
            dict.fromkeys(
                [
                    *workflow.get("perceive", {}).get("sourcesUsed", []),
                    *decision.get("sources_used", []),
                    "destination_seed_profiles",
                    "local_reasoning_history",
                ]
            )
        )

        signal_ledger = [
            {
                "label": "Destination intelligence",
                "score": round(float(scores.get("destinationIntelligence", 0)), 2),
                "reason": "Measures how strongly the destination profile matched the trip brief.",
            },
            {
                "label": "Budget fit",
                "score": round(float(scores.get("budgetFit", 0)), 2),
                "reason": "Captures how realistic the destination is at the current daily budget.",
            },
            {
                "label": "Local signal",
                "score": round(float(scores.get("localSignal", 0)), 2),
                "reason": "Reflects local favorites, social pull, and destination texture.",
            },
            {
                "label": "Safety confidence",
                "score": round(float(scores.get("safetyConfidence", 0)), 2),
                "reason": "Combines seeded risk notes with the pace-aware safety model.",
            },
            {
                "label": "Decision confidence",
                "score": round(self._confidence_percent(decision.get("confidence", 0)), 2),
                "reason": "Shows how confidently the engine can defend the final recommendation.",
            },
            {
                "label": "Grounding coverage",
                "score": round(float(grounding_metrics.get("coverageScore", 0)), 2),
                "reason": "Measures how much retrieved evidence supports the destination-level claims.",
            },
            {
                "label": "Grounding trust",
                "score": round(float(grounding_metrics.get("trustScore", 0)), 2),
                "reason": "Reflects the average trust score of the evidence used in the final explanation.",
            },
        ]

        trust_score = round(sum(item["score"] for item in signal_ledger) / max(len(signal_ledger), 1), 2)
        if trust_score >= 88:
            status = "Verified"
        elif trust_score >= 78:
            status = "High-signal"
        else:
            status = "Partial verification"

        top_ranked = destination_landscape.get("topRanked", {})
        recognized = bool(meta.get("recognizedDestination"))
        cache_summary = retrieval.get("cache", {})
        if grounding.get("method") == "hybrid-live-cached-retrieval":
            freshness = (
                f"Hybrid seeded + cached live evidence ({int(cache_summary.get('cachedDocumentCount', 0))} cached docs)"
            )
        else:
            freshness = "Seeded intelligence + local runtime"
        content_grounded_count = int(grounding_metrics.get("contentGroundedDocuments", 0))
        reason = (
            f"{request['destination']} {'matched' if recognized else 'used'} the destination intelligence layer and "
            f"held a trust score of {trust_score:.2f}. Grounding coverage reached "
            f"{float(grounding_metrics.get('coverageScore', 0)):.2f}, with {content_grounded_count} passage-grounded evidence item(s). The top-ranked landscape candidate is "
            f"{top_ranked.get('destination', request['destination'])}."
        )

        citations = [
            {
                "label": self._humanize_source(source),
                "type": "engine",
                "confidence": max(70, min(98, round(trust_score))),
            }
            for source in sources[:5]
        ]
        for item in supporting.get("social", [])[:2]:
            citations.append(
                {
                    "label": str(item).strip(),
                    "type": "social-signal",
                    "confidence": max(72, min(94, round(float(scores.get("localSignal", 78))))),
                }
            )

        for item in social_references.get("overview", [])[:4]:
            citations.append(
                {
                    "label": str(item.get("title", item.get("platform", "Reference"))).strip(),
                    "type": str(item.get("platform", "reference")).strip().lower(),
                    "confidence": max(72, min(93, round(float(scores.get("localSignal", 78))))),
                    "url": str(item.get("url", "")).strip(),
                    "reason": str(item.get("reason", "")).strip(),
                }
            )
        for item in destination_evidence[:3]:
            citations.append(
                {
                    "label": str(item.get("title", "Evidence source")).strip(),
                    "type": str(item.get("sourceType", "grounding")).strip().lower(),
                    "confidence": round(float(item.get("trust", 0.75)) * 100),
                    "url": str(item.get("url", "")).strip(),
                    "reason": str(item.get("groundedClaim", item.get("excerpt", ""))).strip(),
                    "contentGrounded": bool(item.get("contentGrounded", False)),
                    "contentMode": str(item.get("contentMode", "")).strip(),
                    "legalBasis": str(item.get("legalBasis", "")).strip(),
                    "attribution": str(item.get("attribution", "")).strip(),
                }
            )

        return {
            "version": self.VERSION,
            "verificationSummary": {
                "status": status,
                "trustScore": trust_score,
                "freshness": freshness,
                "reason": reason,
                "checkedAt": datetime.now(UTC).isoformat(),
                "contentPolicy": content_policy.get("mode", "seeded-passages-plus-official-api-snippets"),
            },
            "sources": sources,
            "citations": citations[:6],
            "signalLedger": signal_ledger,
        }

    def _confidence_percent(self, value: Any) -> float:
        numeric = float(value or 0)
        if numeric <= 1:
            return numeric * 100
        return numeric

    def _humanize_source(self, value: str) -> str:
        return str(value).replace("_", " ").replace("-", " ").title()
