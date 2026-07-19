# TickFrame Architecture

> **File:** `assignments/7/architecture.md` — comprehensive architecture of `/tickframe`.

---

## 1. Overview

TickFrame is a **cryptocurrency chart workstation** with a client-server architecture. A **FastAPI backend** serves a static **vanilla JS frontend** (Lightweight Charts v5), interfaces with cryptocurrency exchanges (Bybit primary, Binance fallback), and delegates ML pattern detection to a separate **dual-model microservice**.

- **Frontend:** Static HTML/CSS/JS served by the backend; single-page application with dual chart engine (Lightweight Charts v5 / TradingView Charting Library).
- **Backend:** FastAPI (Python 3.11+) with async REST + WebSocket endpoints, PostgreSQL persistence through asyncpg, 3-tier cache (memory → PostgreSQL → exchange).
- **ML Service:** Separate FastAPI microservice running XGBoost inference for H&S pattern detection (Classic + Inverse).
- **Deployment:** Docker Compose (3 containers: `postgres`, `tickframe`, `ml-service`).

### Technology Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11, FastAPI, Uvicorn, httpx, websockets, Pydantic v2, asyncpg |
| **Frontend** | Lightweight Charts v5, Canvas API, vanilla JS, TradingView Charting Library (vendored), Lucide icons, esbuild (drawing bundle, indicators bundle) |
| **Database** | PostgreSQL 16 (primary via asyncpg), SQLite (fallback for unit tests via `run_in_executor`) |
| **ML** | XGBoost (XGBClassifier), pandas, numpy, FastAPI microservice |
| **Exchange** | Bybit v5 API (HTTPS REST, primary), Binance API (HTTPS REST, fallback) |
| **External APIs** | CoinGecko (coin icons, 1h TTL), alternative.me (Fear & Greed Index, 6h TTL) |
| **CI** | GitHub Actions (ruff, mypy, pytest+cov, bandit, ESLint, Vitest, Lychee) |
| **Deployment** | Docker + Docker Compose (3 containers, default bridge network) |
| **Build** | esbuild (for drawing + indicators bundles) |

---

## 2. Directory Structure (`tickframe/`)

```
tickframe/
├── __init__.py                  # Package marker
├── __main__.py                  # CLI entry point: python -m tickframe
├── cli.py                       # CLI commands: scan, report, analyze, serve (legacy exchange/detection modules)
├── backend/                     # FastAPI backend (primary)
│   ├── __init__.py
│   ├── main.py                  # FastAPI app, lifespan, CORS, static mounts, background tasks
│   ├── api/
│   │   ├── __init__.py
│   │   ├── endpoints.py         # REST routes: health, coins, candles, analyze, patterns, drawings, indicators, settings, toolbar, sentiment
│   │   └── websocket.py         # WebSocket hub: /ws/market, /ws/candles/{symbol}
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py           # Pydantic models: CoinSummary, Candle, CandleResponse, PriceResponse, MarketSnapshot, Pattern, AnalyzeResponse, IndicatorConfig, IndicatorsResponse, IndicatorsPayload
│   └── services/
│       ├── __init__.py
│       ├── bybit_client.py      # Async Bybit v5 client + Binance fallback + pagination + RateLimiter (token-bucket 10 req/s, burst 5)
│       ├── cache.py             # MemoryMarketCache — 3-tier cache (memory → PostgreSQL → exchange), MAX_CANDLES=55000, warmup in 2 phases
│       ├── database.py          # PostgreSQL (asyncpg) primary + SQLite fallback; SCHEMA_PG + SCHEMA_SQLITE; CRUD for settings, drawings_blob, indicators_blob, toolbar_position, coin_icons, candles, ml_scans
│       ├── ml_client.py         # HTTP client for ML microservice (POST /predict), multi-URL fallback (ml-service:8001 → 127.0.0.1:8001), configurable confidence threshold
│       ├── coin_icons.py        # CoinGecko icon fetcher, 1h TTL cache, DB persistence
│       └── fng_client.py        # Fear & Greed Index fetcher (alternative.me), 6h TTL cache
├── frontend/                    # Frontend static files
│   ├── index.html               # Main SPA page: sidebar (logo, search, watchlist, FNG) | main (topbar, chart-container, analysis-stack, indicator-panel)
│   ├── package.json             # npm: devDependencies only (eslint ^9.0.0, vitest ^3.0.0, globals)
│   ├── eslint.config.js         # ESLint flat config
│   ├── css/
│   │   ├── styles.css           # Dark/light theme, layout, sidebar, FNG speedometer, analysis stack
│   │   ├── drawing-toolbar.css  # Floating toolbar styles (11 groups × 34 tools)
│   │   ├── drawing-properties.css # Properties panel styles
│   │   ├── indicators-panel.css # Indicators sidebar panel, panes, chips, toggle button
│   │   └── tradingview-custom.css # TradingView Charting Library overrides
│   ├── js/
│   │   ├── app.js               # DOM init: theme toggle, settings load/save, timeframe buttons, coin click, indicator subsystem init
│   │   ├── charts.js            # Chart engine: Lightweight Charts v5 + TV Charting Library wrapper, candlestick + volume histogram + volume SMA, infinite scroll, ML pattern markers, date-range drawings, in-memory candle cache, pattern filtering
│   │   ├── sidebar.js           # Coin list (10 coins), price updates (5s polling), FNG speedometer SVG, coin icons
│   │   ├── datafeed.js          # TradingView Charting Library datafeed adapter (REST + WS)
│   │   ├── websocket.js         # ManagedSocket class with auto-reconnect, event-based handlers; MarketSocket, CandleSocket
│   │   ├── drawing-overlay-src.js, drawing-bundle.js, drawing-events.js, drawing-state.js, drawing-settings.js, drawing-controller.js, drawing-toolbar.js, drawing-properties.js, drawing-overlay.js
│   │   ├── indicators-src.js, indicators-bundle.js, indicators-registry.js, indicators-state.js, indicators-panes.js, indicators-controller.js, indicators-panel.js, indicators-chips.js
│   ├── lib/
│   │   └── charting_library/    # TradingView Charting Library (vendored, optional)
│   └── tests/                   # Vitest JS tests
├── data/                        # SQLite DB (gitignored, used only in SQLite fallback mode)
├── detection/                   # Legacy pattern detection (deprecated, unused by backend)
├── exchange/                    # Legacy exchange client (deprecated, unused by backend)
└── web/                         # Legacy web server (deprecated, unused by backend)
```

### External: `ml_service/`

```
ml_service/
├── Dockerfile
├── requirements.txt            # xgboost, pandas, numpy, fastapi, uvicorn
├── logs/                       # App logs (gitignored)
└── app/
    ├── __init__.py
    ├── main.py                 # FastAPI ML API: /health, /predict (XGBoost H&S detection)
    ├── config.py               # MODEL_PATH, WINDOW_SIZE=101, FEATURE_ORDER
    ├── schemas.py              # CandleData, PredictRequest, PredictResponse, DetectedPattern
    └── services/
        ├── __init__.py
        ├── features.py         # Feature engineering: ATR, NATR, Trend, extremum search, geometry (slopes, dominance)
        └── inference.py        # Pattern thresholds, NMS clustering, business logic (Classic H&S class=1, Inverse H&S class=2)
```

---

## 3. Used Libraries

### Python (Backend)

| Library | Version | Usage |
|---|---|---|
| `fastapi` | — | Async web framework |
| `uvicorn` | — | ASGI server |
| `httpx` | — | Async HTTP client (exchanges, CoinGecko, alternative.me, ML service) |
| `pydantic` | v2 | Request/response validation |
| `asyncpg` | — | Async PostgreSQL driver |
| `websockets` | — | WebSocket protocol support |

### Python (ML Service)

| Library | Version | Usage |
|---|---|---|
| `xgboost` | — | XGBClassifier for H&S and DT/DB detection |
| `pandas` | — | DataFrame-based feature engineering |
| `numpy` | — | Vectorized feature calculations and model input arrays |
| `numba` | >=0.60.0 | Native-code acceleration for rolling extrema search |
| `fastapi` | — | ML inference API |
| `uvicorn` | — | ASGI server |

### JavaScript (Frontend)

| Library | Version | Source | Usage |
|---|---|---|---|
| `lightweight-charts` | 5.x | CDN | Candlestick chart, volume histogram, volume SMA |
| `lightweight-charts-drawing` | — | npm → esbuild bundle | 34+ drawing tools in 11 groups |
| `lightweight-charts-indicators` | 0.4.2 | npm → esbuild bundle | 446 TA indicators (Standard 82, Candlestick Patterns 44, Community 317) |
| `charting_library` | — | vendored | TradingView Advanced Charting (optional) |
| `lucide` | latest | CDN | SVG icons for drawing toolbar |
| `vitest` | ^3.0.0 | npm devDeps | JS unit testing |
| `eslint` | ^9.0.0 | npm devDeps | JS linting |
| `esbuild` | — | npm | Build drawing bundle + indicators bundle + oakscriptjs |

---

## 4. Code Structure & Module Responsibilities

### 4.1 Backend (`backend/`)

#### `main.py` — Application entry point

- Creates `FastAPI` with `lifespan` handler
- Lifespan: initializes `BybitClient`, `DatabaseService` (PostgreSQL via `DATABASE_URL` env or default `postgresql://tickframe:tickframe@postgres:5432/tickframe`), `MemoryMarketCache`, `MlClient`
- Starts background tasks:
  - `market_refresh_loop` (5s interval, broadcasts market snapshots over WebSocket)
  - `background_ml_scan` (silent scan for all 10 coins after warmup)
  - `cache.warm_up()` (Phase 1: load DB candles, Phase 2: fill gaps from exchange)
- Mounts `/css`, `/js`, `/lib`, `/static` as static directories
- Serves `index.html` at `/`
- CORS middleware (all origins allowed)
- Includes REST router (`/api`) and WebSocket router

#### `api/endpoints.py` — REST API

| Endpoint | Method | Description |
|---|---|---|
| `/api/health` | GET | Health check |
| `/api/coins` | GET | List 10 coins with price, 24h change, trend |
| `/api/coins/icons` | GET | Coin icon URLs (CoinGecko, 1h cache) |
| `/api/coins/{symbol}/price` | GET | Single coin price snapshot |
| `/api/coins/{symbol}/candles` | GET | OHLCV candles (limit, before, interval params); max 55000 |
| `/api/analyze/{symbol}` | POST | ML pattern analysis with incremental scan + configurable confidence threshold |
| `/api/patterns/{symbol}` | GET | Retrieve stored ML scan results |
| `/api/sentiment` | GET | Fear & Greed Index (alternative.me) |
| `/api/drawings` | GET/POST | Load/save drawings blob per symbol |
| `/api/indicators` | GET/POST | Load/save indicator configs per symbol |
| `/api/toolbar-position` | GET/POST | Load/save toolbar position |
| `/api/settings` | GET/POST | Load/save user settings (key-value) |

#### `api/websocket.py` — WebSocket

- `SocketHub` class: manages connected clients with `asyncio.Lock`, broadcast to all
- `/ws/market`: receives initial snapshot + continuous broadcast (5s market refresh loop)
- `/ws/candles/{symbol}`: sends snapshot on connect, then 1s polling with signature change detection (time, open, high, low, close, volume hash); sends `update`, `heartbeat`, or `snapshot` type messages

#### `services/bybit_client.py` — Exchange Client

- `BybitClient`: async HTTP client for Bybit v5 API
- Token-bucket `RateLimiter` (10 req/s, burst 5)
- Automatic fallback to Binance API on failure
- Pagination support (200 per request Bybit, 1000 per request Binance)
- `fetch_candles()`: paginated historical OHLCV fetch with deduplication
- `fetch_market_snapshot()`: 24hr ticker for all 10 coins
- `fetch_price()`: single coin price
- 10 default coins: BTC, ETH, SOL, XRP, DOGE, ADA, AVAX, DOT, LINK, BNB
- Fallback to hardcoded price hints + deterministic random when exchange unavailable

#### `services/cache.py` — Memory Cache

- `MemoryMarketCache`: 3-tier cache (memory → PostgreSQL → exchange)
- `MAX_CANDLES = 55000` per (symbol, interval) pair
- Intervals: 5m, 15m, 1h, 4h, 1d
- Warmup: Phase 1 loads DB candles for all coins/intervals concurrently; Phase 2 fills gaps from exchange sequentially respecting rate limits
- Thread-safe with `threading.Lock` for in-memory data
- `get_candles()`: returns from memory if fresh → DB lookup → exchange fetch + persist
- `_get_candles_before()`: pagination support for historical scroll
- Deduplication and merge logic for overlapping exchange/DB data

#### `services/database.py` — Database Service

- `DatabaseService`: dual-mode — PostgreSQL (`asyncpg`) primary, SQLite (`sqlite3` via `run_in_executor`) fallback for testing
- PostgreSQL schema (`SCHEMA_PG`): 7 tables
- SQLite schema (`SCHEMA_SQLITE`): 8 tables (adds legacy per-row `drawings` table)
- Key methods:
  - Settings: `get_setting`, `set_setting`, `get_all_settings`
  - Drawings: `save_drawings_blob`, `load_drawings_blob`
  - Indicators: `save_indicators`, `load_indicators`
  - Toolbar: `save_toolbar_position`, `load_toolbar_position`
  - Coin icons: `save_coin_icons`, `load_coin_icons`
  - Candles: `save_candles`, `load_candles`, `load_last_n_candles`, `load_candles_before`, `load_candles_after`, `get_candle_range`, `count_candles`
  - ML scans: `save_ml_scan`, `load_ml_scan`

#### `services/ml_client.py` — ML Service Client

- `MlClient`: HTTP client for ML microservice
- Multi-URL fallback: primary (`ml-service:8001/predict`) → localhost (`127.0.0.1:8001/predict`)
- Configurable via env: `ML_API_URL`, `ML_CONFIDENCE_THRESHOLD` (default 0.80), `ML_REQUEST_TIMEOUT` (default 30.0s)
- Filters results by confidence threshold
- Uses `httpx.AsyncClient`

#### `services/coin_icons.py` — Coin Icons

- `CoinIconsClient`: CoinGecko API (`/api/v3/coins/markets`), 1h TTL in-memory cache + DB persistence
- Maps 10 symbols to CoinGecko IDs (bitcoin, ethereum, solana, etc.)

#### `services/fng_client.py` — Fear & Greed

- `FearAndGreedClient`: alternative.me API (`/fng/?limit=1`), 6h TTL in-memory cache
- Fallback: returns neutral value 50 on failure with 5min retry

### 4.2 Frontend (`frontend/`)

#### `index.html` — SPA Shell

Layout: `sidebar` (logo, coin search, watchlist with 10 coins, FNG speedometer) | `main` (topbar with market stats, chart container, analysis stack, indicator panel)

Scripts loaded: `charts.js`, `app.js`, `sidebar.js`, `websocket.js`, drawing modules, indicator modules, `datafeed.js`

#### `js/app.js` — App Initialization

- Loads settings from backend, applies theme
- Inits indicator subsystem (`TFIndicatorController`, `TFIndicatorPanes`, `TFIndicatorPanel`, `TFIndicatorChips`)
- Wires symbol switch, timeframe buttons, indicators toggle, theme toggle, analyze button
- Handles candle update callbacks for indicator recompute
- Auto-selects first coin (BTC) after 300ms

#### `js/charts.js` — Chart Engine

- Dual-mode: Lightweight Charts v5 (primary, default) / TradingView Charting Library (advanced, optional)
- Candlestick series + Volume histogram + Volume SMA (20-period) line
- Infinite scroll pagination (`before` parameter) up to `_MAX_CANDLES = 55000`
- ML pattern markers (triangle shapes) with type-based coloring
- Pattern filtering: Classic H&S, Inverse H&S, Double Top, Double Bottom toggle
- In-memory candle cache (`_candleCache` dict) for fast symbol switching
- Date-range drawings support
- Matrix theme: dark bg `#02050a`, green text `#7fbf97`

#### `js/sidebar.js` — Watchlist & FNG

- 10 coins with names, icons, prices, 24h change
- 5s polling for price updates
- Fear & Greed SVG speedometer with colored zones and timer
- Auto-scroll to selected coin

#### `js/websocket.js` — WebSocket Manager

- `ManagedSocket`: auto-reconnect with exponential backoff, event-based handlers (`onMessage`, `onOpen`, `onClose`, `onError`)
- `MarketSocket`: connects to `/ws/market`, updates watchlist prices
- `CandleSocket`: connects to `/ws/candles/{symbol}`, handles snapshot/update/heartbeat

#### Indicator System (8 modules + bundle)

- **Registry:** `TFIndicators` — 446-indicator registry (Standard 82, Candlestick Patterns 44, Community 317) from `lightweight-charts-indicators`
- **State:** `TFIndicatorState` — reactive store with subscribe pattern
- **Panes:** `TFIndicatorPanes` — stacked `createChart` instances, timeScale sync, pane management (create, remove, resize)
- **Controller:** `TFIndicatorController` — apply/remove/recompute/persist lifecycle, volume pane init
- **Panel:** `TFIndicatorPanel` — right sidebar UI with search, grouping (All, Standard, Candlestick, Community), apply button
- **Chips:** `TFIndicatorChips` — applied indicator pill row with remove
- **Bundle:** esbuild-compiled `lightweight-charts-indicators` + `oakscriptjs`
- Triggered by `_onCandlesUpdated` callback for recompute on new data

#### Drawing System (9 modules + bundle)

- **Overlay:** `TFDraw` facade, keyboard shortcuts (delete, escape)
- **Controller:** Drawing lifecycle (add, select, move, resize), redact mode, auto-save to backend
- **Toolbar:** 11 groups × 34 tools, drag reposition, toggle visibility
- **Events/State/Settings/Properties:** modular support modules
- **Bundle:** esbuild-compiled `lightweight-charts-drawing`

### 4.3 CLI (`cli.py`)

Commands: `scan`, `report`, `analyze`, `serve`. Invoked via `python -m tickframe <command>`.
- **scan** — fetch candles from Bybit or use mock data, output to console or JSON
- **report** — generate Markdown report from scan results
- **analyze** — pattern analysis on cached candles (uses legacy detection module)
- **serve** — start FastAPI dev server via `uvicorn`

Note: `scan` and `report` reference deprecated `exchange.bybit` module; `analyze` references deprecated `data.cache` and `detection.mock` modules. These exist only for backward compatibility.

### 4.4 ML Microservice (`ml_service/`)

- `GET /health` — model loaded status (`"model_loaded": true/false`)
- `POST /predict` — OHLCV candles → smart features → XGBoost classifier → NMS clustering → detected patterns
- XGBoost `XGBClassifier`, `WINDOW_SIZE = 101` candles, `FEATURE_ORDER` strict ordering for inference
- Pattern classes: 1 = Classic H&S, 2 = Inverse H&S
- Pipeline: smart features (ATR, NATR, Trend_50, geometry slopes, dominance) → predict_proba → business thresholds → NMS → output
- Only `5m` timeframe supported
- Requires 50 context candles before analyzed window (WINDOW_SIZE - 1 = 100 cropped)
- Model file loaded from `MODEL_PATH` on startup, cleared on shutdown

---

## 5. Data Flow & Algorithmic Structure

### 5.1 Chart Loading Request Flow

```
Client                          Backend                         Exchange / DB
  │                                │                                │
  │── GET /api/coins/{s}/candles ──│                                │
  │                                │── Memory cache hit? ──────────→│
  │                                │   ├── Yes: return immediately  │
  │                                │   └── No: DB lookup ──────────→│
  │                                │       ├── Hit: return + cache  │
  │                                │       └── Miss: exchange fetch→│
  │                                │           └── persist to DB ──→│
  │←── CandleResponse JSON ───────│                                │
```

### 5.2 Pattern Analysis Flow

```
Client                          Backend                    ML Service
  │                                │                          │
  │── POST /api/analyze/{symbol} ──│                          │
  │   (confidence_threshold)       │── Check DB for existing  │
  │                                │   scan results           │
  │                                │── Load candles (increm.) │
  │                                │── POST /predict ────────→│
  │                                │   (OHLCV candles)        │
  │                                │                          │── Feature engineering
  │                                │                          │── XGBoost inference
  │                                │                          │── NMS clustering
  │                                │←── patterns_found ──────│
  │                                │── Merge + dedup patterns │
  │                                │── Save to DB (ml_scans)  │
  │←── patterns + metadata ───────│                          │
```

### 5.3 Market Broadcast Loop

```
market_refresh_loop (every 5s):
  1. cache.refresh_market_snapshot() → fetches 24hr tickers from Bybit
  2. market_hub.broadcast_json({ type: "market_snapshot", coins: [...] })
  → All /ws/market clients receive price updates
```

### 5.4 Background ML Scan (Startup)

```
background_ml_scan (after warmup):
  For each of 10 coins:
    1. db.load_ml_scan(pair) — skip if patterns already exist
    2. db.load_last_n_candles(pair, "5m", 50000)
    3. ml.analyze_candles() → POST /predict
    4. db.save_ml_scan(pair, interval, last_time, patterns)
```

### 5.5 3-Tier Cache Algorithm

```
get_candles(symbol, interval, limit, before?):
  1. Memory check: if cached payload exists, is fresh (< refresh_interval), and has ≥ limit candles → return cached slice
  2. DB check: load_last_n_candles from PostgreSQL, if ≥ limit → cache + return "db" source
  3. Exchange fetch: fetch from Bybit (with Binance fallback), merge with any DB candles, persist to DB, cache + return
```

### 5.6 Warmup Algorithm

```
warm_up():
  Phase 1: For all 10 × 5 intervals (50 total) concurrently:
    count_candles() → load_last_n_candles() → populate in-memory cache
  Phase 2: For each coin sequentially (respects rate limiter):
    For each interval (5m, 15m, 1h, 4h, 1d):
      if current < MAX_CANDLES:
        fetch missing older candles from exchange (paginated)
        merge + deduplicate + persist to DB
```

### 5.7 ML Feature Extraction (`ml_service/app/services/features.py`)

- Sliding window extremum search (pivot highs/lows)
- Geometric features: shoulder-head-shoulder slopes, neckline angles
- Dominance metrics: head dominance ratio
- Technical indicators: ATR, NATR, Trend_50 (50-period trend)
- All features aligned on WINDOW_SIZE=101 window

### 5.8 ML Inference & NMS (`ml_service/app/services/inference.py`)

- Business thresholds: minimum confidence, pattern-specific filters
- NMS (Non-Maximum Suppression) clustering: merge overlapping detections, keep highest confidence
- Class mapping: 1 → Classic H&S, 2 → Inverse H&S

### 5.9 WebSocket Candle Update

```
/ws/candles/{symbol}:
  1. Accept connection with interval and limit query params
  2. Send { type: "snapshot", candles: [...] }
  3. Every 1s:
     a. Fetch latest 2 candles from cache
     b. Compute signature = (time, O, H, L, C, V)
     c. If signature changed → send { type: "update", candle: last_candle }
     d. If unchanged → send { type: "heartbeat", timestamp }
```

### 5.10 Indicator Application

```
TFIndicatorController.apply(indicatorId, inputs):
  1. Find indicator in TFIndicators registry
  2. Create pane (if standalone) or overlay on main chart
  3. Compute indicator values using lightweight-charts-indicators
  4. Add series to pane with computed data
  5. Persist to backend via POST /api/indicators
```

### 5.11 Drawing Creation

```
TFDraw (drawing-overlay):
  1. User selects tool from toolbar (11 groups × 34 tools)
  2. Click on chart to place points
  3. Drawing rendered via lightweight-charts-drawing overlay
  4. Auto-save triggered → POST /api/drawings (JSON blob per symbol)
  5. Load on symbol switch → GET /api/drawings?symbol=X
```

---

## 6. Database Schema

### PostgreSQL (primary, `SCHEMA_PG`)

```sql
CREATE TABLE settings (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE drawings_blob (
    symbol  TEXT PRIMARY KEY,
    data    TEXT NOT NULL,
    updated TEXT NOT NULL DEFAULT NOW()::TEXT
);

CREATE TABLE toolbar_position (
    id        BIGINT PRIMARY KEY DEFAULT 1 CHECK (id = 1),
    pos_left  BIGINT NOT NULL DEFAULT 16,
    pos_top   BIGINT NOT NULL DEFAULT 40
);

CREATE TABLE coin_icons (
    symbol  TEXT PRIMARY KEY,
    url     TEXT NOT NULL
);

CREATE TABLE indicators_blob (
    symbol  TEXT PRIMARY KEY,
    data    TEXT NOT NULL,
    updated TEXT NOT NULL DEFAULT NOW()::TEXT
);

CREATE TABLE candles (
    symbol    TEXT NOT NULL,
    interval  TEXT NOT NULL,
    time      BIGINT NOT NULL,
    open      DOUBLE PRECISION NOT NULL,
    high      DOUBLE PRECISION NOT NULL,
    low       DOUBLE PRECISION NOT NULL,
    close     DOUBLE PRECISION NOT NULL,
    volume    DOUBLE PRECISION NOT NULL DEFAULT 0,
    updated   TEXT NOT NULL DEFAULT NOW()::TEXT,
    PRIMARY KEY (symbol, interval, time)
);

CREATE TABLE ml_scans (
    symbol   TEXT PRIMARY KEY,
    interval TEXT NOT NULL,
    last_scanned_time BIGINT NOT NULL DEFAULT 0,
    patterns TEXT NOT NULL DEFAULT '[]',
    updated  TEXT NOT NULL DEFAULT NOW()::TEXT
);
```

### SQLite (fallback for unit tests, `SCHEMA_SQLITE`)

Same as PostgreSQL but with:
- `INTEGER`/`REAL` instead of `BIGINT`/`DOUBLE PRECISION`
- `datetime('now')` instead of `NOW()::TEXT`
- Additional legacy `drawings` table (per-row drawings with id, symbol, type, points, opts, selected, created)
- Explicit `INSERT OR CONFLICT` for toolbar_position default row

---

## 7. API Surface

### REST Endpoints

| Method | Path | Query Params | Request Body | Response |
|---|---|---|---|---|
| GET | `/api/health` | — | — | `{"status": "ok"}` |
| GET | `/api/coins` | — | — | `[CoinSummary]` (10 coins with price, change, trend) |
| GET | `/api/coins/icons` | — | — | `{"symbol": "url", ...}` |
| GET | `/api/coins/{symbol}/price` | — | — | `PriceResponse` |
| GET | `/api/coins/{symbol}/candles` | `interval` (5m default), `limit` (200 default, max 55000), `before` (timestamp) | — | `CandleResponse` |
| POST | `/api/analyze/{symbol}` | `interval` (5m default), `confidence_threshold` (0.80 default) | — | `{symbol, interval, patterns}` |
| GET | `/api/patterns/{symbol}` | — | — | `{symbol, patterns}` |
| GET | `/api/sentiment` | — | — | `{value, classification, timestamp}` |
| GET | `/api/drawings` | `symbol` | — | `{drawings_data}` or `{drawings: []}` |
| POST | `/api/drawings` | — | `{symbol, drawings_data}` | `{"status": "ok"}` |
| GET | `/api/indicators` | `symbol` | — | `{indicators: [...]}` |
| POST | `/api/indicators` | — | `{symbol, indicators}` | `{"status": "ok"}` |
| GET | `/api/toolbar-position` | — | — | `{left, top}` |
| POST | `/api/toolbar-position` | — | `{left, top}` | `{"status": "ok"}` |
| GET | `/api/settings` | — | — | `{settings: {key: value, ...}}` |
| POST | `/api/settings` | — | `{settings: {key: value, ...}}` | `{"status": "ok"}` |

### WebSocket Endpoints

| Path | Direction | Message Types |
|---|---|---|
| `/ws/market` | Server → Client | `snapshot` (initial), `market_snapshot` (broadcast every 5s) |
| `/ws/candles/{symbol}` | Server → Client | `snapshot` (initial full), `update` (candle change), `heartbeat` (no change) |

### ML Microservice

| Method | Path | Request | Response |
|---|---|---|---|
| GET | `/health` | — | `{"status": "success", "model_loaded": true/false}` |
| POST | `/predict` | `{symbol, timeframe, candles: [CandleData]}` | `{symbol, timeframe, patterns_found: [DetectedPattern], processed_candles}` |

---

## 8. Configuration & Environment

| Variable | Default | Used By |
|---|---|---|
| `DATABASE_URL` | `postgresql://tickframe:tickframe@postgres:5432/tickframe` | `database.py` — PostgreSQL connection |
| `DB_PASSWORD` | `tickframe` | `docker-compose.yml` — PostgreSQL password |
| `ML_API_URL` | `http://ml-service:8001/predict` | `ml_client.py` — ML service endpoint |
| `ML_CONFIDENCE_THRESHOLD` | `0.80` | `ml_client.py` — pattern filter threshold |
| `ML_REQUEST_TIMEOUT` | `30.0` | `ml_client.py` — HTTP timeout |

---

## 9. Docker Deployment

### Docker Compose (3 services)

```yaml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: tickframe
      POSTGRES_USER: tickframe
      POSTGRES_PASSWORD: ${DB_PASSWORD:-tickframe}
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U tickframe -d tickframe"]
    restart: always
    # No host port exposed — accessible only within Docker network at postgres:5432

  tickframe:
    build: .
    ports:
      - "8080:8080"
    env_file: .env
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - ./tickframe/frontend:/app/tickframe/frontend  # live-reload
      - ./tickframe/backend:/app/tickframe/backend    # live-reload

  ml-service:
    build: ./ml_service
    ports:
      - "8001:8001"
    volumes:
      - ./ml_service/logs:/code/logs
    restart: always

volumes:
  pgdata:
```

### Port Mapping

| Container | Internal Port | Host Port | Notes |
|---|---|---|---|
| `postgres` | 5432 | — | Not exposed to host by default |
| `tickframe` | 8080 | 8080 | Main web UI + API |
| `ml-service` | 8001 | 8001 | ML inference API |

### Connecting to PostgreSQL from host

Add `ports: - "5432:5432"` to the `postgres` service, then connect with:
```
postgresql://tickframe:tickframe@localhost:5432/tickframe
```

---

## 10. Quality Requirements & Architecture Mapping

| QR | Metric | Architecture Support |
|---|---|---|
| QR-001 (Time Behaviour) | p95 ≤ 500ms | 3-tier cache (memory → DB → exchange), async I/O, background warmup, WebSocket push for live updates, paginated fetch |
| QR-002 (Confidentiality) | Zero secrets in commits | Env vars via `.env`, `.env.example` as template, secrets in `.gitignore`, Docker Compose `env_file` |
| QR-003 (Functional Correctness) | F2 ≥ 0.55, FPR ≤ 20% | ML microservice with XGBoost, smart feature engineering, NMS clustering, configurable confidence threshold |
| QRT-004 (WebSocket Reliability) | — | Auto-reconnect (ManagedSocket), heartbeat messages, signature-based change detection |
| QRT-005 (DB Cache Round-Trip) | — | PostgreSQL via asyncpg connection pool, transaction batching, `run_in_executor` for SQLite fallback |
