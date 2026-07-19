# SWP TickFrame — Customer Handover

**Team 28** · [GitHub Repository](https://github.com/Fedos113/SWP_TickFrame_28_team) · [Hosted Documentation](https://Fedos113.github.io/SWP_TickFrame_28_team/)

---

## Project Overview

TickFrame is a cryptocurrency chart workstation built with FastAPI. It provides real-time market data from Bybit (with Binance fallback), interactive candlestick charts via Lightweight Charts v5, a canvas-based drawing toolbar (13 tools), SQLite-persisted settings and drawings, a technical indicator library with 445+ indicators (including RSI, Volume, Fear & Greed), and ML-based pattern analysis (4 trading patterns via XGBoost microservice).

---

## Transition Scope

This section explains what has been transferred to the customer, what is delegated for the customer to operate on their own infrastructure, and what the team retains.

| Category | Items | Notes |
|---|---|---|
| **Transferred** | Full source code (MIT license), Docker Compose deployment configuration, maintained documentation set (`docs/`), contributor guidance (`CONTRIBUTING.md`), AI agent guidance (`AGENTS.md`), root README entry point, changelog (`CHANGELOG.md`) | All repository-resident assets are permanently available under the MIT open-source license. The customer may fork or copy without restriction. |
| **Delegated** | Docker-based deployment to the customer's own infrastructure, including the Docker Compose setup for `tickframe` + `ml-service` containers; environment configuration via `.env` file | The customer is expected to run the application on their own machines or VMs using the provided Docker Compose configuration. The university VM deployment used during development is a temporary convenience and may not persist after grading. |
| **Retained (team side)** | GitHub repository ownership and administration (team's university accounts), GitHub Actions CI pipeline configuration, GitHub Pages hosted documentation site | These are retained because they are tied to the team's university accounts and credentials. The customer can fork the repository to gain full control. CI secrets and workflow credentials remain with the team. |

---

## Configuration and Secrets

### Environment Variables

No API keys are required for basic operation — Bybit public endpoints work without authentication. For higher rate limits or custom configuration, create a `.env` file in the repository root:

```bash
cp .env.example .env
```

The following environment variables are used:

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `BYBIT_API_KEY` | No | — | Bybit API key for authenticated endpoints (higher rate limits). Leave empty for public-only access. |
| `BYBIT_API_SECRET` | No | — | Bybit API secret paired with the key. |
| `ML_API_URL` | No | `http://ml-service:8001/predict` | URL of the ML prediction endpoint. Change if running ML service on a different host/port. |
| `ML_CONFIDENCE_THRESHOLD` | No | `0.80` | Minimum confidence score (0.0–1.0) for pattern detection results to be shown. |
| `ML_REQUEST_TIMEOUT` | No | `30.0` | Timeout in seconds for ML service HTTP requests. |
| `DATABASE_URL` | No | `postgresql://tickframe:tickframe@postgres:5432/tickframe` | PostgreSQL connection string used by the backend. In Docker Compose it points to the bundled `postgres` service. |
| `DB_PASSWORD` | No | `tickframe` | Password for the PostgreSQL `tickframe` role, referenced by `DATABASE_URL` and the `postgres` container. |


### Secrets Handling Rules

- `.env` is listed in `.gitignore` — it must never be committed to the repository.
- `.env.example` is the committed sanitized template. Keep it updated if new variables are added.
- No real API keys, tokens, or passwords should ever appear in committed files, commit messages, CI logs, or public documentation.
- Store `.env` securely on the deployment machine and restrict file permissions (`chmod 600 .env`).

---

## Setup and Deployment

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) + Docker Compose (v2 or later)
- 2 CPU cores, 2 GB RAM recommended
- Network access to `api.bybit.com` (outbound HTTPS) and `api.binance.com` (fallback)

### Docker Quick Start

```bash
git clone https://github.com/Fedos113/SWP_TickFrame_28_team.git
cd SWP_TickFrame_28_team
cp .env.example .env   # optional — edit if using API keys
docker compose up --build
```

Open **http://localhost:8080** in your browser.

For a remote VM, replace `localhost` with the VM's IP address.

> The first load may take 10–30 seconds while historical candle data is fetched from the exchange. Once cached in PostgreSQL, subsequent loads are instant.

### PostgreSQL Setup

Docker Compose bundles a `postgres:16-alpine` service, so no manual database setup is required for containerised deployments. The backend connects using `DATABASE_URL` (see the environment variable table above) and creates its schema on startup. Data is stored in the named volume `pgdata` and survives container restarts.

To run the backend against an external PostgreSQL instance (for example, when developing without Docker):

```bash
export DATABASE_URL=postgresql://tickframe:tickframe@localhost:5432/tickframe
docker run --name tickframe-pg -e POSTGRES_DB=tickframe -e POSTGRES_USER=tickframe -e POSTGRES_PASSWORD=tickframe -p 5432:5432 -d postgres:16-alpine
uvicorn tickframe.backend.main:app --host 0.0.0.0 --port 8000
```

To migrate existing data from a legacy SQLite database (`tickframe/data/tickframe.db`) into PostgreSQL, run:

```bash
python scripts/migrate_sqlite_to_pg.py
```

The script reads every table (settings, drawings, drawings_blob, toolbar_position, coin_icons, indicators_blob, candles) from SQLite and transfers the rows into the configured `DATABASE_URL`.


### Local Development (No Docker)

For development or debugging without Docker:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
pip install -r tests/requirements.txt
uvicorn tickframe.backend.main:app --host 0.0.0.0 --port 8000
```

Open **http://localhost:8000**.

> Note: The ML microservice must be started separately for pattern analysis to work (`cd ml_service && uvicorn app.main:app --host 0.0.0.0 --port 8001`).

### Verification Steps

After starting the application, verify both services are healthy:

```bash
curl http://localhost:8080/api/health     # Backend — expected: {"status":"ok"}
curl http://localhost:8001/health          # ML service — expected: {"status":"success","model_loaded":true}
```

### Recovery and Clean Rebuild

If the application becomes unstable or changes are not reflected after a rebuild:

```bash
docker compose down
docker compose rm
docker compose build --no-cache
docker compose up -d
```

This forces Docker to rebuild all layers from scratch and start in detached mode.

### Updating from the Repository

```bash
git pull origin main
docker compose up --build
```

### Port Conflicts

The Docker host port is `8080` (mapped to container port `8000`). If another process is already using port `8080` or `8000`, check with:

```bash
netstat -ano | findstr ":8080"
```

Stop the conflicting process or change the host port in `docker-compose.yml`.

---

## Product Access

The application is deployed and accessible at:

> **http://10.93.26.164:8080/**

This is a university VM deployment used for development and trial access. Availability depends on the VM being powered on. If the VM is unreachable, use the Docker quick start above to run locally.

**Week 7 status:** The VM deployment was updated with the final MVP v3 version on 2026-07-17. The deployment now includes 3 Docker Compose services (ML Service, TickFrame, PostgreSQL) with database credentials configured via environment variables.

---

## Key Features

| Feature | Description |
|---|---|
| **Real-time charts** | WebSocket-powered live candlestick charts via Lightweight Charts v5 |
| **Drawing toolbar** | 13 modular tools: Trend Line, H-Line, V-Line, Ray, Cross Line, Fibonacci, Price Range %, Rectangle, Circle, Arrow, Text, Brush, Redact |
| **ML pattern analysis** | Sliding-window pattern detection (4 patterns: Head & Shoulders, Double Top, Double Bottom, Flags) with configurable candle limit and confidence scores |
| **Technical indicators** | 445+ indicators (RSI, Moving Averages, Bollinger Bands, etc.) via integrated open-source library; searchable panel UI |
| **Multi-interval** | 5m, 15m, 1h, 4h, 1d timeframes |
| **Volume sub-chart** | Volume pane with SMA overlay below main chart |
| **Fear & Greed Index** | Sentiment indicator displayed in sidebar |
| **WebSocket live data** | Real-time market snapshots and candle updates from Bybit/Binance (1s intervals) |
| **Persistence** | Drawings, settings, and candle data survive restarts via PostgreSQL |

| **Dark/light theme** | Toggle persisted to database |
| **Coin sidebar** | Live prices, ticker badges, 24h change, crypto icons |
| **Coin icons** | Auto-fetched from CoinGecko API |

---

## Architecture at a Glance

```
Exchange (Bybit/Binance)
    ↓
MemoryMarketCache (in-memory, 5s refresh)
    ↓
PostgreSQL (data persistence — candles, drawings, settings)
    ↓

FastAPI Backend (REST + WebSocket)
    ↓
Frontend (Lightweight Charts v5, Canvas drawing, JS)
```

The ML pattern detection runs as a separate microservice (`ml_service/`) for isolation and independent scaling. The technical indicator library runs client-side — it receives candle data from the backend and computes indicator values locally.

Full architecture documentation: [docs/architecture/README.md](architecture/README.md)

---

## Documentation Entry Points

The following documentation pages are the main entry points for normal use, operation, and troubleshooting:

| Resource | Link | Purpose |
|---|---|---|
| **README** | [../README.md](../README.md) | Project overview, quick start, API endpoints, configuration, troubleshooting |
| **Hosted Documentation Site** | https://Fedos113.github.io/SWP_TickFrame_28_team/ | Browsable rendered documentation set |
| **Architecture Docs** | [docs/architecture/README.md](architecture/README.md) | Static, dynamic, and deployment views; ADR index |
| **Customer Handover** | [docs/customer-handover.md](customer-handover.md) | This document — transition scope, setup, support |
| **Contributing Guide** | [../CONTRIBUTING.md](../CONTRIBUTING.md) | Workflow, coding standards, verification checklist |
| **AI Agent Guidance** | [../AGENTS.md](../AGENTS.md) | AI assistant safety rules and repository context |
| **Changelog** | [../CHANGELOG.md](../CHANGELOG.md) | All user-visible changes by release |
| **Roadmap** | [docs/roadmap.md](roadmap.md) | Sprint-by-Sprint delivery plan |
| **Testing Strategy** | [docs/testing.md](testing.md) | Test types, coverage, CI gates |
| **User Acceptance Tests** | [docs/user-acceptance-tests.md](user-acceptance-tests.md) | UAT scenarios and results |
| **Definition of Done** | [docs/definition-of-done.md](definition-of-done.md) | Minimum completion standard |
| **Quality Requirements** | [docs/quality-requirements.md](quality-requirements.md) | QR-001 through QR-003 |
| **Quality Requirement Tests** | [docs/quality-requirement-tests.md](quality-requirement-tests.md) | QRT-001 through QRT-005 |
| **Development Process** | [docs/development-process.md](development-process.md) | Git workflow, CI, configuration management |

### Documentation Sufficiency Assessment

**Current handover level:** `Ready for independent use`

**Customer-confirmation status:** `Accepted` (confirmed during Sprint 6 review, 2026-07-17)

**Sufficiency verdict:** The documentation set covers all areas needed for independent use — setup, deployment, configuration, operation, troubleshooting, architecture, testing, contribution, and handover. All gaps identified in Week 6 have been addressed:

- **Customer trial completed:** The Sprint 6 review (2026-07-17) served as the formal transition-readiness session. The customer reviewed the full documentation set and confirmed acceptance.
- **PostgreSQL migration completed:** PostgreSQL 16 container included in Docker Compose with env-var credentials. Handover docs updated with current architecture (database env-var table, deployment steps, migration script).
- **Final access details confirmed:** The university VM (http://10.93.26.164:8080/) continues to serve the latest deployment. Docker quick-start instructions remain the primary access path for local use.
- **Transition confirmed:** The customer accepted the handover documentation during the Sprint 6 review. No further changes were requested before defense.

---

## Known Limitations

| Area | Limitation |
|---|---|
| **Exchange dependency** | Only Bybit v5 (main) and Binance (fallback) are supported. Adding a new exchange requires a new client adapter. |
| **Single-user** | No authentication or multi-user support — all users share the same drawings and settings via SQLite. |
| **No order execution** | TickFrame is a charting/analysis workstation only. Trade placement is not supported. |
| **Historical depth** | Maximum 50 000 candles per request. Very long histories (years of 1m data) are not available. |
| **ML scope** | 4 patterns (Head & Shoulders, Double Top, Double Bottom, Flags) are detected; 2 more in development. Models were trained on synthetic data and accuracy varies by market conditions. |
| **ML timeframe** | Pattern detection is only available on the 5m timeframe. Chart switching to other intervals (15m, 1h, 4h, 1d) works, but pattern analysis does not run on them. |
| **WebSocket resilience** | Reconnect is automatic but a brief gap (1–3 s) may occur on network interruption. |
| **Browser support** | Developed and tested on Chromium-based browsers (Chrome, Edge). Other browsers may have minor rendering differences. |
| **Mobile** | No responsive layout. The UI is designed for desktop screens ≥ 1280 px wide. |

---

## Handover Status

### Current Week 7 State (Final)

| Status | Value |
|---|---|
| **Handover level reached** | `Ready for independent use` |
| **Customer-confirmation status** | `Accepted` |

**Explanation:** The product is functionally complete for independent use — the customer can run it locally or deploy it via Docker. The Sprint 6 review (2026-07-17) served as the final transition confirmation. All customer-requested changes from Week 6 were addressed (PostgreSQL migration, pattern filtering, coin metrics, UI fixes, 6 ML patterns). The customer explicitly approved the increment as the final course delivery and confirmed no further changes are required before defense.

### What Has Been Handed Over

- Full source code under MIT license in the public repository
- Docker Compose deployment configuration (`tickframe` + `ml-service`)
- Hosted documentation site at GitHub Pages
- Customer handover documentation (this file)
- Contributing guide (`CONTRIBUTING.md`) with workflow, setup, standards, CI, and PR process
- AI agent guidance (`AGENTS.md`) with safety rules, project context, and testing strategy
- Root `README.md` with project overview, quick start, API documentation, configuration, and troubleshooting
- Complete architecture documentation with static, dynamic, and deployment views plus ADRs
- Full testing documentation including unit, integration, QRT, and frontend test definitions
- Quality requirements and quality requirement tests (QR-001 through QR-003, QRT-001 through QRT-005)
- User acceptance tests, user stories, product backlog, and roadmap

### What the Customer Needs to Know

- No API keys are required for basic operation — Bybit public endpoints work without authentication
- For higher rate limits, create a `.env` file with Bybit API credentials (see [Configuration and Secrets](#configuration-and-secrets) above)
- The ML microservice uses XGBoost and starts alongside the main app via Docker Compose
- Data is stored in a PostgreSQL database that runs as a bundled Docker Compose service (`postgres:16-alpine`) — no manual database setup is needed. Persistence is backed by the `pgdata` named volume.

- The application is designed for desktop use on Chromium-based browsers
- The GitHub repository itself, CI pipelines, and GitHub Pages site are managed by the team's university accounts; fork the repository to gain full administrative control

### What Still Requires Team Support (Final State)

| Item | Status | Notes |
|---|---|---|
| Customer trial and documentation review | ✅ Completed | Sprint 6 review (2026-07-17) served as final transition confirmation. Customer reviewed and accepted. |
| Customer-confirmation of handover document | ✅ Completed | Customer accepted the handover documentation. Status: `Accepted`. |
| Final access arrangement for MVP v3 | ✅ Completed | PostgreSQL migration complete. VM deployment updated with all 3 services. |
| Known limitations | Documented | See [Known Limitations](#known-limitations) above. Anomaly detection not delivered; ML only on 5m; DT/DB precision low. |
| CI pipeline and GitHub Pages admin | Retained by team | Tied to university accounts. Customer can fork for independent CI/Pages control. |
| Post-course issues or feature requests | Post-course | File as GitHub issues (no guaranteed response after course ends). |

---

## License

This project is licensed under the MIT License — see [LICENSE](../LICENSE) for details.
