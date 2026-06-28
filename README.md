# SWP TickFrame — Team 28

FastAPI-based cryptocurrency chart workstation with real-time Bybit market data, live price streaming via WebSockets, candlestick charts (Lightweight Charts v4), a canvas-based drawing toolbar (13 tools), SQLite persistence, and ML pattern analysis.

---

## Quick Start (Docker)

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) + Docker Compose
- 2 CPU cores, 2 GB RAM recommended

### 1. Clone

```bash
git clone https://github.com/Fedos113/SWP_TickFrame_28_team.git
cd SWP_TickFrame_28_team
```

### 2. Build and run

```bash
docker compose up --build
```

### 3. Open in browser

```
http://localhost:8000
```

For a remote VM, replace `localhost` with the VM's IP address.

> The first load may take 10–30 seconds while historical candle data is fetched from the exchange. Once cached in SQLite, subsequent loads are instant.

---

## Architecture

```
tickframe/
├── backend/
│   ├── main.py                # FastAPI app, lifespan, static mounts
│   ├── api/
│   │   ├── endpoints.py       # REST: health, coins, candles, analyze, drawings, settings
│   │   └── websocket.py       # WS: market hub, candle streams + heartbeat
│   ├── services/
│   │   ├── bybit_client.py    # Async Bybit v5 client with Binance fallback + pagination
│   │   ├── cache.py           # MemoryMarketCache with DB fallback (3-tier: mem → DB → exchange)
│   │   ├── database.py        # SQLite service (settings, drawings, candle persistence)
│   │   └── ml_client.py       # HTTP client for ML pattern analysis service
│   └── models/
│       └── schemas.py         # Pydantic models
├── frontend/
│   ├── index.html             # Main page with left drawing toolbar
│   ├── css/styles.css         # Dark/light theme, toolbar, settings panel
│   └── js/
│       ├── app.js             # Init, theme toggle, settings load/save
│       ├── charts.js          # Lightweight Charts v4, candle loading, pattern analysis
│       ├── sidebar.js         # Coin list with full ticker badges, trend-colored prices
│       ├── datafeed.js        # TradingView Charting Library datafeed adapter
│       ├── drawing-overlay.js # Canvas drawing engine: 13 tools, redact mode, undo, per-drawing settings
│       ├── toolbar.js         # Chart type switching (candle/line/area)
│       └── websocket.js       # WebSocket connection management
├── ml_service/                # ML pattern detection microservice
├── data/tickframe.db          # SQLite database (auto-created, gitignored)
├── docker-compose.yml         # tickframe + ml-service containers
└── requirements.txt
```

### Data flow

```
Exchange (Bybit/Binance)
    ↓  (paginated fetch, max 50k candles)
MemoryMarketCache (in-memory, 5s refresh)
    ↓  (merge + dedup)
SQLite (data/tickframe.db) ← survives restarts
    ↓
Frontend chart (Lightweight Charts v4, last 10k candles default zoom)
    ↓  (sliding window, step 10)
ML service → pattern detections rendered as vertical lines + text labels
```

---

## Features

| Feature | Detail |
|---|---|
| **Chart** | Lightweight Charts v4, up to 50k candles, candlestick/line/area modes |
| **Drawing tools** | 13 tools: Trend Line, H-Line, V-Line, Ray, Cross Line, Fibonacci, Price Range %, Rectangle, Circle, Arrow, Text, Brush, Redact (select/move/edit) |
| **Per-drawing settings** | Color, width (1–4), line style (solid/dashed/dotted), font size |
| **Redact mode** | Freezes chart (no scroll/zoom), crosshair hidden, enables drag-to-move/reshape |
| **Undo** | Full undo stack for add, modify (drag), and delete operations |
| **Persistence** | All drawings saved per coin to SQLite; candle data cached in DB across restarts |
| **Real-time updates** | WebSocket streams with heartbeat (5s), candle updates pushed to chart |
| **Pattern analysis** | Sliding window (50 candles, step 10) sends to ML service; results rendered as red dashed vertical lines + labels |
| **Theme** | Dark/light toggle, persisted to DB |
| **Coin sidebar** | Full ticker badges, trend-colored prices (5m candle direction), 5s auto-refresh |
| **Price formatting** | Max 6 total digits, trailing zeros stripped |

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/health` | Health check |
| GET | `/api/coins` | List coins with prices and trend |
| GET | `/api/coins/{symbol}/price` | Current price |
| GET | `/api/coins/{symbol}/candles?interval=5m&limit=200` | Candlestick data (max 50000) |
| POST | `/api/analyze/{symbol}` | Pattern analysis (optional `{candles: [...]}` body) |
| GET | `/api/drawings?symbol=` | Load persisted drawings per coin |
| POST | `/api/drawings` | Save drawings per coin |
| GET | `/api/settings` | Load settings from DB |
| POST | `/api/settings` | Save settings to DB |
| WS | `/ws/market` | Market snapshot stream (5s) |
| WS | `/ws/candles/{symbol}?interval=5m` | Candle stream with heartbeat |

---

## Configuration

Bybit public endpoints work without authentication. For higher rate limits, create `.env`:

```bash
cp .env.example .env
```

Key variables:

| Variable | Default | Description |
|---|---|---|
| `ML_API_URL` | `http://ml-service:8001/predict` | ML analysis endpoint |
| `ML_CONFIDENCE_THRESHOLD` | `0.80` | Default confidence threshold |
| `ML_REQUEST_TIMEOUT` | `30.0` | ML request timeout (seconds) |

---

## Documentation & Reports

| Resource | Link |
|---|---|
| Definition of Done | [docs/definition-of-done.md](docs/definition-of-done.md) |
| Quality Requirements | [docs/quality-requirements.md](docs/quality-requirements.md) |
| Quality Requirement Tests | [docs/quality-requirement-tests.md](docs/quality-requirement-tests.md) |
| Testing Strategy | [docs/testing.md](docs/testing.md) |
| User Acceptance Tests | [docs/user-acceptance-tests.md](docs/user-acceptance-tests.md) |
| Roadmap | [docs/roadmap.md](docs/roadmap.md) |
| User Stories | [docs/user-stories.md](docs/user-stories.md) |
| Changelog | [CHANGELOG.md](CHANGELOG.md) |
| Week 2 Reports | [reports/week2/](reports/week2/README.md) |
| Week 3 Reports | [reports/week3/](reports/week3/README.md) |
| Week 4 Reports | [reports/week4/](reports/week4/README.md) |
| License | [MIT](LICENSE) |
