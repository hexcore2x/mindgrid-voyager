# MindGrid Voyager Evaluation Report

## Snapshot

Representative out-of-sample temporal backtest snapshot after the current ranking, grounding, and calibration upgrades:

- Held-out case count: `16`
- Total benchmark case count: `24`
- Top-1 accuracy: `100%`
- Top-3 coverage: `100%`
- Average grounding coverage: `87.18`
- Calibration gap: `37.33`
- Brier score: `0.1477`

## What This Report Covers

The evaluation stack in MindGrid Voyager now includes:

- benchmark accuracy
- confidence quality
- grounding coverage
- slice-level performance
- temporal holdout validation
- feature ablation analysis

These metrics are exposed through `GET /api/evaluation`.

The evaluation response also includes an `inSampleReference` block, but that is intentionally secondary. The headline summary is now the out-of-sample temporal backtest.

## Temporal Holdout Validation

The benchmark suite is ordered by `benchmarkDate` and split into:

- Train window: `2025-01-12` to `2025-08-24`
- Holdout window: `2025-09-12` to `2025-12-21`

Current holdout snapshot:

- Holdout case count: `8`
- Holdout top-1 accuracy: `100%`
- Holdout top-3 coverage: `100%`
- Holdout Brier score: `0.1334`

This is not a substitute for production-scale temporal validation, but it is a stronger signal than evaluating only on the full benchmark set.

## Ablation Highlights

Current ablation study findings:

- Removing grounding features keeps rank order stable on this benchmark, but confidence quality drops sharply.
- Removing intent features causes the biggest performance collapse.
- Removing fitted calibration leaves ranking accuracy unchanged but worsens confidence quality.

Representative deltas:

- Grounding removed: calibration gap worsens by about `+22`
- Intent removed: top-1 accuracy drops by about `-45.83`
- Fitted calibration removed: calibration gap worsens by about `+8.99`

## Interpretation

This project now demonstrates more than UI polish and rule wiring. It shows:

- explicit feature engineering
- a learned local ranker with persisted artifacts
- fitted confidence calibration
- hybrid retrieval and grounding
- benchmark reporting with ablations and holdout checks

That makes it much stronger as an applied AI / decision-systems portfolio artifact, even though it is still local-first and intentionally lightweight.

## Remaining Gaps

The main remaining limitations are:

- the benchmark set is still handcrafted
- live retrieval remains optional and cache-dependent
- the learning loop is not yet backed by large organic outcome volume
- there is no notebook-style experiment history or large-scale offline dataset
