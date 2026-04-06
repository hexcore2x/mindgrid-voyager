# MindGrid Voyager

**One-line pitch**

MindGrid Voyager is a local-first agentic AI decision engine for real-world travel exploration, built with Python, HTML, CSS, and JavaScript.

## Product Overview

MindGrid Voyager turns a trip brief into structured destination intelligence.

Instead of behaving like a simple travel search page, it acts like a decision system:

- it evaluates destination fit
- it scores safety and budget alignment
- it prioritizes experiences
- it generates explainable recommendations
- it supports multi-destination comparison

The result is a portfolio-grade MVP that combines product thinking, backend design, recommendation logic, explainability, and premium frontend presentation in one local runnable project.

## Why This Project Exists

Most travel planning tools fragment the experience across multiple low-context surfaces:

- generic search results
- disconnected budgeting tools
- scattered blogs and social recommendations
- weak itinerary reasoning
- little transparency into why one option is better than another

MindGrid Voyager explores what a stronger interface could look like if travel planning were treated as an intelligence workflow instead of a list-rendering exercise.

## Key Features

- Local-first Python backend with no framework migration required
- Explainable recommendation engine with structured decision output
- Hybrid grounding layer that combines seeded passages with short, attributed snippets from official YouTube and Reddit APIs when enabled
- Prior-regularized learned ranking model with persisted local training artifacts and blended prior/learned feature contributions
- Offline evaluation harness with benchmark accuracy, top-3 coverage, slice metrics, temporal holdout validation, ablation studies, and calibration tracking
- Optional live-source-ready YouTube and Reddit adapters with safe local fallback
- Local feedback loop that stores outcome signals, reusable trip briefs, and calibration signals over time
- Live feedback refresh that retrains local ranking and calibration artifacts immediately after feedback submission
- Multi-destination comparison mode for 2-4 destinations
- Local recommendation history and restore flow in the UI
- SQLite-backed persistence for requests and generated results
- Structured logging with rotating log files
- Health check endpoint with database connectivity and uptime
- Validation layer for safe API input handling
- Premium dark UI with glassmorphism, responsive layouts, and polished states
- Automated pytest coverage for core backend flows

## Agentic Workflow

MindGrid Voyager is framed around a visible four-stage decision loop:

### Discover

Collect the user's brief, map it to seeded destination intelligence, and gather context signals.

### Verify

Check safety confidence, destination recognition, and trustworthiness of the result.

### Prioritize

Rank experiences, itinerary blocks, budget fit, and destination-level tradeoffs.

### Explain

Return a structured decision with score, priority, evidence, workflow trace, and reasoning summary.

Workflow label used across the product:

`Discover -> Verify -> Prioritize -> Explain`

## Architecture Overview

### Backend

- [`app.py`](./app.py)
  - local HTTP server
  - routing
  - response shaping
  - health checks
  - comparison, recommendation, replan, and evaluation endpoints
- [`database.py`](./database.py)
  - SQLite initialization
  - request persistence
  - generated result storage
  - database connectivity check
- [`engines/`](./engines)
  - destination intelligence
  - hybrid grounding and cached evidence retrieval
  - feature engineering
  - prior-regularized learned ranking model
  - recommendation assembly
  - prioritization
  - itinerary planning
  - risk analysis
  - reasoning orchestration
  - fitted calibration
  - offline benchmark evaluation
- [`utils/validation.py`](./utils/validation.py)
  - payload validation
  - structured API error helpers
- [`utils/logger.py`](./utils/logger.py)
  - structured request, error, and decision-run logging

### Frontend

- [`index.html`](./index.html)
  - landing page
  - live recommendation surface
  - comparison workflow
- [`styles.css`](./styles.css)
  - entry stylesheet that layers the final visual system
- [`app-theme.css`](./app-theme.css)
  - premium dark product styling layer
- [`theme-refresh.css`](./theme-refresh.css)
  - final release visual polish layer
- [`client_app.js`](./client_app.js)
  - API requests
  - rendering logic
  - comparison flow
  - local history

### Quality Layer

- [`tests/`](./tests)
  - endpoint tests
  - validation tests
- [`pytest.ini`](./pytest.ini)
  - local pytest configuration

### AI Credibility Layer

- `GroundingEngine`
  - retrieves seeded passages plus short official API snippets when enabled
  - exposes coverage, trust, recency, and content-grounding metrics
- `FeatureEngineeringEngine`
  - converts traveler intent and destination profiles into explicit ranking features
- `RankingModel`
  - trains a local monotonic ranker with persisted artifacts and layer-aware feature contributions from both the prior and learned score paths
- `CalibrationEngine`
  - fits confidence using benchmark and feedback samples rather than simple blending
- `SocialSignalEngine`
  - can fall back to safe outbound links or enrich results with optional live YouTube/Reddit metadata
- `EvaluationEngine`
  - runs an offline benchmark suite over seeded and feedback-aware scenarios
  - now uses out-of-sample temporal backtesting as the headline benchmark
  - reports top-1 accuracy, top-3 coverage, Brier score, average grounding coverage, calibration gap, slice metrics, ablations, and temporal holdout validation

See [`docs/model-card.md`](./docs/model-card.md) and [`docs/evaluation-report.md`](./docs/evaluation-report.md) for the current model and evaluation notes.

## Tech Stack

- Python 3.11+
- Standard library HTTP server
- SQLite
- Plain HTML
- Plain CSS
- Plain JavaScript
- Pytest

## Local Setup

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run Instructions

Start the local server:

```powershell
python app.py
```

Optional live-source enrichment:

```powershell
$env:MINDGRID_YOUTUBE_API_KEY="your-youtube-api-key"
$env:MINDGRID_ENABLE_LIVE_REDDIT="true"
python app.py
```

If no key is configured, the app keeps working with safe local fallback references.

Then open:

- [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Test Instructions

Run the backend test suite:

```powershell
python -m pytest -q
```

## Quick Demo

### Recommendation Input

Use this payload in the UI or against `POST /api/recommendations`:

```json
{
  "destination": "Tokyo",
  "budget": 1800,
  "duration": 4,
  "interests": ["food", "culture", "walkable", "local"],
  "travelStyle": "Balanced Explorer",
  "pace": "balanced"
}
```

### Comparison Input

Use this payload against `POST /api/comparison`:

```json
{
  "destinations": ["Tokyo", "Bangkok", "Singapore"],
  "budget": 1800,
  "duration": 4,
  "interests": ["food", "culture", "walkable"],
  "travelStyle": "Balanced Explorer",
  "pace": "balanced"
}
```

## Supported Demo Destinations

The seeded intelligence layer currently supports:

- Bangkok
- Tokyo
- Bali
- Dubai
- Singapore
- Paris
- Goa

Unknown destinations fall back to adaptive heuristic planning.

## API Endpoints

### `GET /health`

Returns service health, database connectivity, version, timestamp, and uptime.

Example response:

```json
{
  "success": true,
  "status": "ok",
  "database": "connected",
  "version": "1.0",
  "timestamp": "2026-04-03T00:00:00+00:00",
  "uptimeSeconds": 12.34
}
```

### `GET /api/demo-request`

Returns demo-request count and recent demo submissions.

### `POST /api/demo-request`

Example payload:

```json
{
  "name": "Alex",
  "email": "alex@example.com",
  "destination": "Paris",
  "travelStyle": "Balanced Explorer",
  "notes": "Optimize for food, safety, and walkability."
}
```

### `GET /api/recommendations`

Returns recommendation-request count and recent request metadata.

### `POST /api/recommendations`

Generates a structured recommendation with:

- destination summary
- decision score
- priority level
- reasoning workflow
- signals and evidence
- grounding evidence
- model diagnostics
- itinerary
- budget guidance
- safety notes

### `POST /api/comparison`

Generates ranked comparison results for 2-4 destinations under one shared trip brief.

Returns:

- top ranked destination
- average score and confidence
- ranked destination list
- comparison-ready reasoning data

### `POST /api/replan`

Applies a natural-language follow-up instruction, updates the trip brief, and reruns the decision engine.

### `GET /api/evaluation`

Returns the local offline benchmark report for the ranking system, including:

- out-of-sample temporal backtest summary used as the headline metric
- in-sample reference summary for comparison
- top-1 accuracy
- top-3 coverage
- average confidence
- Brier score
- calibration gap
- average grounding coverage
- learned model and calibration artifact summaries
- slice metrics by difficulty, season, region, and pace
- temporal holdout validation
- feature ablation comparisons

The current seeded suite covers 24 scenarios across value, safety, culture, premium, beach, nightlife, wellness, and business-style trip briefs.

### `GET /api/feedback`

Returns the local feedback summary used by the confidence calibration and learning layers.

### `POST /api/feedback`

Stores a local outcome signal for a recommendation, including:

- destination
- traceId
- verdict (`accepted`, `replanned`, `rejected`)
- rating (`1-5`)
- notes
- optional request payload for training-aware feedback reuse

## Screenshots

Suggested screenshot placeholders for the GitHub README:

- `docs/screenshots/hero-overview.png`
- `docs/screenshots/recommendation-results.png`
- `docs/screenshots/comparison-mode.png`
- `docs/screenshots/history-panel.png`
- `docs/screenshots/architecture-snapshot.png`

These can be captured after starting the app locally.

## Repository Structure

Current top-level structure:

```text
MindGrid Voyager/
|-- .gitignore
|-- LICENSE
|-- app.py
|-- app-theme.css
|-- client_app.js
|-- database.py
|-- docs/
|-- index.html
|-- pytest.ini
|-- README.md
|-- requirements.txt
|-- script.js
|-- styles.css
|-- theme-refresh.css
|-- data/
|-- engines/
|-- logs/
|-- static/
|-- templates/
|-- tests/
|-- utils/
```

Runtime notes:

- `data/` and `logs/` are local runtime directories and are ignored from Git except for placeholder files.
- `script.js` remains in the repo only as a compatibility artifact; the live page boots from `client_app.js`.

## Future Roadmap

- Integrate live travel and mapping data sources
- Add real social signal ingestion instead of seeded mock intelligence
- Add saved result browsing from backend history
- Add richer comparison analytics and destination filters
- Add user-level trip memory and journal persistence
- Expand hybrid retrieval into a larger indexed evidence store
- Expand feedback-aware calibration with larger local outcome sets and harder negatives
- Add CI automation for tests and release checks

## Engineering Value / Recruiter Value

MindGrid Voyager is useful as a hiring portfolio project because it demonstrates:

- backend API design
- structured validation and error handling
- local-first persistence
- recommendation engine architecture
- explainable AI-style orchestration
- premium frontend execution without heavy frameworks
- comparison-oriented product thinking
- test coverage and release hygiene

It shows the ability to evolve a working local app into something that feels product-shaped, technically credible, and ready for public review.
