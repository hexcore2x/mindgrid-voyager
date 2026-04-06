# MindGrid Voyager Model Card

## Overview

MindGrid Voyager uses a local, inspectable ranking stack rather than a hidden black-box model.

The current AI decision path is made of four layers:

1. `GroundingEngine`
   - retrieves hybrid seeded passages plus cached short snippets from official YouTube and Reddit endpoints
   - computes coverage, trust, and recency metrics
2. `FeatureEngineeringEngine`
   - converts traveler intent and destination profiles into explicit ranking features
3. `RankingModel`
   - fits a prior-regularized learned ranking layer over benchmark and feedback-aware samples
   - produces a decision score, confidence, calibration band, a blended scoring pipeline, and layer-aware feature contributions
4. `CalibrationEngine`
   - fits Platt-style confidence calibration over local benchmark and feedback-aware samples
5. `EvaluationEngine`
   - benchmarks the ranker against seeded travel scenarios and exposes calibration, slice, ablation, and temporal holdout metrics

Feedback submitted through the product can now refresh the live local ranking and calibration artifacts immediately at runtime, rather than only after a restart.

## Inputs

- destination
- budget
- currency
- duration
- interests
- travel style
- pace

## Feature Groups

- destination intelligence
- budget fit
- budget realism
- local signal
- safety confidence
- popularity score
- relevance score
- intent alignment
- style alignment
- pace alignment
- grounding coverage
- grounding trust
- grounding recency
- evidence density
- evidence support

## Outputs

- decision score
- confidence
- calibration band
- calibration diagnostics
- scoring pipeline with prior and learned layer probabilities
- blended feature breakdown with prior and learned contribution splits
- grounded evidence snippets
- verification summary

## Evaluation

The offline benchmark layer measures:

- top-1 accuracy
- top-3 coverage
- average confidence
- Brier score
- calibration gap
- average grounding coverage
- slice metrics by difficulty, season, region, and pace
- temporal holdout validation on later benchmark windows
- ablation deltas for intent, grounding, and calibration

These metrics are available from `GET /api/evaluation`.

The evaluation endpoint now separates:

- out-of-sample temporal backtest metrics used as the headline benchmark
- in-sample reference metrics used only as a secondary diagnostic

Live retrieval can be enabled with:

- `MINDGRID_YOUTUBE_API_KEY`
- `MINDGRID_ENABLE_LIVE_REDDIT=true`

## Intended Use

- portfolio demonstration of explainable travel recommendation architecture
- local-first AI product prototyping
- recruiter-facing showcase for ranking, grounding, calibration, and evaluation design

## Current Limitations

- default retrieval quality still depends on how much live evidence has been cached locally
- live social grounding uses short official API snippets and links, not full post/video transcripts
- evaluation set is larger now, but still handcrafted rather than mined from organic production traffic
- the learned ranker is trained on local benchmark and feedback data, not internet-scale outcome logs
- social references use safe public metadata and links rather than direct third-party content ingestion

## Upgrade Path

- expand hybrid retrieval into a larger indexed evidence store
- grow the benchmark set with harder negative cases and temporal drift checks
- collect more user outcome feedback with richer trip context
- replace or augment the ranker with a larger learned reranker when real volume exists
