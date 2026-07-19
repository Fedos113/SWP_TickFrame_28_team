# Architecture Documentation — SWP TickFrame

> **Maintained artifact** — describes the current architecture of TickFrame using three architectural views (static, dynamic, deployment) and indexes the ADR set.

---

## 1. Introduction

TickFrame is a cryptocurrency chart workstation with a **client-server architecture**. The system consists of a **FastAPI backend** that serves a static **JavaScript frontend**, interfaces with cryptocurrency exchanges, and delegates ML pattern detection to a separate **microservice**.

### Technology Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11, FastAPI, Uvicorn, httpx, websockets |
| **Frontend** | Lightweight Charts v5, Canvas API, vanilla JS, lightweight-charts-drawing, lightweight-charts-indicators |
| **Database** | PostgreSQL 16 (via asyncpg); SQLite used as unit-test fallback |
| **Indicators** | 445+ technical indicators (lightweight-charts-indicators library, client-side computation) |
| **ML** | XGBoost, Numba, FastAPI microservice |
| **Exchange** | Bybit v5 API (primary), Binance API (fallback) |
| **Deployment** | Docker + Docker Compose (3 containers: tickframe, ml-service, postgres) |
| **Caching** | 3-tier: Memory → PostgreSQL → Exchange |

### Architecture Views

| View | Source | Rendered | Description |
|---|---|---|---|
| Static | [`diagram.puml`](static-view/diagram.puml) | [`diagram.svg`](static-view/diagram.svg) | Component diagram — system structure, components, and relations |
| Dynamic | [`diagram.puml`](dynamic-view/diagram.puml) | [`diagram.svg`](dynamic-view/diagram.svg) | Sequence diagram — chart loading flow and user interactions |
| Deployment | [`diagram.puml`](deployment-view/diagram.puml) | [`diagram.svg`](deployment-view/diagram.svg) | Deployment diagram — nodes, containers, and network boundaries |

### Supporting ML Architecture

The ML microservice now runs independent H&S and DT/DB XGBoost detectors in
one `/predict` request. Their feature contracts, thresholds, NMS behavior,
timing metrics, Numba warmup, fallback path, and verification evidence are
documented in [`dtdb-integration-decisions.md`](dtdb-integration-decisions.md).

---

## 2. Static View — Component Diagram

**Source:** [`static-view/diagram.puml`](static-view/diagram.puml)

![Static View — Component Diagram](static-view/diagram.svg)

### What the diagram shows

The static view decomposes TickFrame into four internal components and three external systems:

**Internal components:**
- **FastAPI Backend** (`tickframe/backend/`) — the central server that serves REST endpoints, manages WebSocket connections, caches market data in memory, persists data to PostgreSQL, and coordinates exchange and ML service calls.
- **Frontend** (`tickframe/frontend/`) — static HTML/CSS/JS served by the backend. Uses Lightweight Charts v5 for candlestick rendering, a modular drawing toolbar (lightweight-charts-drawing library), and the indicators subsystem (lightweight-charts-indicators library with 445+ indicators computed client-side).
- **ML Service** (`ml_service/`) — a separate FastAPI microservice running XGBoost inference for 6 pattern types: Head & Shoulders, Inverse H&S, Double Top, Double Bottom, Flags, Wedge.
- **PostgreSQL DB** — persistent storage for candles, drawings, settings, indicators, and ML results. Runs as a dedicated container via Docker Compose.

**External systems:**
- **Bybit API** — primary exchange data source via HTTPS REST.
- **Binance API** — fallback exchange when Bybit is unavailable.
- **Web Browser** — the client runtime environment.

**Relations and protocols:**
- Browser ↔ Backend: **HTTP REST** (JSON) + **WebSocket** (real-time streams)
- Backend → PostgreSQL: **SQL** via asyncpg
- Backend → Bybit/Binance: **HTTPS REST**
- Backend → ML Service: **HTTP POST** (Docker internal DNS)
- Frontend ↔ Indicators Library: **client-side** — indicators compute locally from candle data, no external API calls

### Coupling & Cohesion

- **Loose coupling** between frontend and backend — the frontend communicates only through REST/WebSocket APIs, so either can evolve independently as long as the API contract is preserved.
- **High cohesion** within the backend — the caching layer (`MemoryMarketCache`), database service (`DatabaseService`), and exchange client (`BybitClient`) are separated by responsibility and communicate through well-defined interfaces.
- **Microservice boundary** between backend and ML service — the ML service has its own codebase, dependencies, and Dockerfile. This enforces loose coupling and allows independent scaling and release cycles.

### Maintainability Implications

- The monorepo structure with a single Python package (`tickframe/`) simplifies local development and CI — one set of dependencies, one test runner, one lint/type-check config.
- The ML microservice avoids bloat in the main backend image — TensorFlow/XGBoost dependencies are isolated.
- The 3-tier cache (memory → DB → exchange) reduces external API dependency during development and testing.

### Quality Requirements Supported

| QR | How the architecture supports it |
|---|---|
| **QR-001 (Time Behaviour)** | FastAPI async handlers + MemoryMarketCache (in-process dict, TTL 5s) minimise latency. PostgreSQL provides persistent storage across restarts. Background warmup pre-loads data and pre-analyses ML patterns. |
| **QR-002 (Confidentiality)** | No secrets in code — all API configurations are environment variables via `.env`. Backend validates all inputs via Pydantic models before processing. |
| **QR-003 (Functional Correctness)** | ML service isolation enables focused accuracy testing (QRT-003). The caching layer preserves deterministic candle data for reproducible analysis. |

---

## 3. Dynamic View — Sequence Diagram

**Source:** [`dynamic-view/diagram.puml`](dynamic-view/diagram.puml)

![Dynamic View — Sequence Diagram](dynamic-view/diagram.svg)

### Scenario: Chart Loading & Pattern Analysis

The sequence diagram illustrates the **core user workflow**: a user opens the app, selects a coin, views the candlestick chart (with real-time updates), and requests ML pattern analysis.

### Why this scenario is important

This is the primary value proposition of TickFrame — a trader needs to see real-time candlestick data and ML-detected patterns in a single interface. The scenario exercises every architectural layer:
- Frontend rendering (Lightweight Charts)
- REST API for historical data
- 3-tier cache (memory → DB → exchange)
- WebSocket for live updates
- ML microservice for pattern detection

### Architecture decisions illustrated

1. **3-tier caching strategy** — the diagram shows how the backend checks memory first, falls back to PostgreSQL, then fetches from the exchange. This reduces exchange API calls and improves response time (QR-001).
2. **WebSocket for real-time updates** — after initial chart load, the frontend opens a WebSocket connection. The server pushes candle updates and heartbeats without polling (ADR-001).
3. **Microservice boundary** — ML analysis is a separate HTTP call to the ML service, keeping the backend free of heavy ML dependencies (ADR-003).

### Quality Requirements

| QR | How the dynamic flow supports it |
|---|---|
| **QR-001 (Time Behaviour)** | Cache-first strategy returns data in milliseconds on cache hit. WebSocket avoids polling overhead. Background warmup pre-fills caches before first user request. |
| **QR-003 (Functional Correctness)** | ML analysis runs on the same cached candle data the user sees, ensuring consistency between visual patterns and detected patterns. |

---

## 4. Deployment View — Deployment Diagram

**Source:** [`deployment-view/diagram.puml`](deployment-view/diagram.puml)

![Deployment View — Deployment Diagram](deployment-view/diagram.svg)

### What the diagram shows

The deployment view shows two deployment nodes:
- **Docker Host** — a single VM or development machine running Docker Engine. Three containers run inside a default bridge network:
  - `tickframe` container — exposes port `8000` (mapped to host `8080`). Runs the FastAPI backend and serves frontend static files.
  - `ml-service` container — exposes port `8001`. Runs the ML inference engine.
  - `postgres` container — exposes port `5432`. Runs PostgreSQL 16 with persistent volume storage.
- **Client Machine** — the user's web browser connecting via HTTP/WebSocket.

External dependencies (Bybit, Binance) are accessed over the internet.

### Why Docker Compose on a single VM

1. **Simplicity** — Docker Compose is the simplest reproducible deployment path. A single `docker compose up --build` starts all three containers with the correct networking, volume mounts, and environment variables.
2. **CI alignment** — the same Compose file is used in development and production, eliminating environment drift.
3. **Resource efficiency** — a single VM is sufficient for the expected load (single-user or small-team usage). Multi-node orchestration (Kubernetes, Swarm) would add operational complexity without proportional benefit.

### Constraints

- **Single point of failure** — if the Docker host goes down, the entire application is unavailable.
- **Horizontal scaling limited** — scaling requires moving to orchestration. The microservice architecture (`ml-service` as a separate container) makes this transition possible, but it is not implemented.
- **PostgreSQL concurrency** — PostgreSQL handles concurrent reads and writes efficiently. The migration from SQLite to PostgreSQL addressed the serialised-write bottleneck that could affect multi-user scenarios.

### Operations Considerations

- **Docker health checks** — both containers expose `/health` endpoints for monitoring and orchestration readiness probes.
- **Volume persistence** — the PostgreSQL database is stored on a named Docker volume (`pgdata`), surviving container restarts.
- **Secrets** — exchange API keys (optional) are supplied via `.env` file, which is listed in `.gitignore`. Only `.env.example` with placeholder values is committed.
- **Port mapping** — host port `8080` maps to container port `8000` to avoid conflicts with common development servers. Host port `8001` maps to `ml-service:8001`.
- **Logging** — ML service logs are written to `ml_service/logs/` via a mounted volume.

---

## 5. ADR Index

Architecture Decision Records (ADRs) document significant architecture decisions with context, rationale, and consequences. Each ADR links to the quality requirements it affects.

| ADR | Title | Status | Summary |
|---|---|---|---|
| [ADR-001](adr/ADR-001-websocket-migration.md) | WebSocket Migration | Accepted | Migrate REST polling to WebSocket for real-time market data. Reduces latency (QR-001). |
| [ADR-002](adr/ADR-002-sqlite-persistence.md) | SQLite Persistence | Accepted | Add SQLite as a persistent cache tier. Improves repeat-load performance (QR-001) and enables deterministic analysis (QR-003). |
| [ADR-003](adr/ADR-003-microservice-architecture.md) | Microservice Architecture | Accepted | Isolate ML detection as a separate microservice. Enables independent scaling, clean dependency isolation (QR-003), and focused accuracy testing. |

### Related Quality Requirements

| QR | Related ADRs |
|---|---|
| **QR-001** (Time Behaviour) | ADR-001 (WebSocket reduces latency), ADR-002 (SQLite cache reduces response time), ADR-003 (microservice network hop — mitigated by co-location) |
| **QR-002** (Confidentiality) | ADR-001 (WebSocket input validation), ADR-003 (service boundary enforces input sanitisation) |
| **QR-003** (Functional Correctness) | ADR-003 (ML isolation enables dedicated accuracy testing), ADR-002 (deterministic analysis on cached data) |
