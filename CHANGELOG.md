# Changelog

All notable user-visible changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] — 2026-07-19 (MVP v3 — Assignment 6 Sprint 6)

### Fixed
- **Double Top / Double Bottom patterns are now actually detected**: The `dtdb` detector's confidence on live 5m market data peaks around ~0.48, but the ML service required `0.75`/`0.80`, so no Double Top or Double Bottom was ever emitted. The `dtdb` thresholds are now calibrated to the current model so all four pattern types (Classic H&S, Inverse H&S, Double Top, Double Bottom) are detected, saved to the database on startup, and returned by `POST /api/analyze/{symbol}`.
- **Backend confidence filter no longer discards valid DT/DB detections**: The backend re-applied a single `confidence_threshold` (default `0.60`) to every pattern, silently dropping all Double Top / Double Bottom results (whose confidences are inherently lower than H&S). The filter now only applies to H&S patterns and trusts the ML model's own per-detector threshold for `dtdb`.
- **Pattern labels now include the confidence score**: The merged on-chart pattern label used the bare `pattern_type`; it now shows `pattern_type + confidence%` (e.g. `Double Top 47%`) consistently with the per-pattern markers.

- **Pattern filter checkboxes now actually filter the chart**: The pattern-filter toolbar wrote to `window._patternFilter`, but `charts.js` kept its filter state in a separate module-local object, so `renderPatterns()` never saw the checkbox state and all four pattern types were always shown. The module now exposes its filter on `window._patternFilter`, giving the toolbar and renderer a single shared source of truth.
- **ML `processing_ms` timings preserved**: `MlClient` discarded the ML service's `processing_ms` block (total / H&S / DT-DB timings). It is now kept and surfaced in the `POST /api/analyze/{symbol}` response.
- **Per-pattern `detector` field preserved**: The additive `detector` (`hs` / `dtdb`) field on each detected pattern is now carried through the backend and stored in the database, instead of being inferred from `pattern_type`.
- **Unsupported ML timeframes no longer look like "no patterns"**: The ML service only supports `5m`. `POST /api/analyze/{symbol}` is now restricted to `5m` and other timeframes raise an explicit HTTP 400 instead of silently returning an empty pattern list.

- **Charts render in Docker environments without internet**: `lightweight-charts` is now installed via npm (`^5.2.0`) and served as a local static file at `/lib/lightweight-charts/lightweight-charts.standalone.production.js`, replacing the `unpkg.com` CDN reference that was unreachable in isolated Docker containers.
- **CoinGecko API calls on cold boot eliminated**: Default coin icons for all 10 tracked coins are now hardcoded in `coin_icons.py`. On first boot with an empty database, the defaults are returned immediately and persisted to the DB — the external API is only called in the background and is never needed for the UI to work.
- **Safe fallback when LightweightCharts is missing**: `createChart` now guards against `typeof LightweightCharts === 'undefined'` and exits gracefully instead of throwing a ReferenceError.
- **`createChart()` is now actually called on DOMContentLoaded**: The `document.addEventListener('DOMContentLoaded', createChart)` line was accidentally dropped during the rewrite, meaning `createChart()` was defined but never invoked. The chart never initialized at all — this was the root cause of the blank screen.
- **Single-chart architecture replaces stacked per-coin instances**: The per-coin `CoinChartInstance`/`CoinChartManager` stacking approach introduced complexity, broke the drawing toolbar, and caused indicators to not initialize. Reverted to a single `Lightweight Charts` instance with per-coin data stored in a flat `_coinData` cache. On coin switch, the active coin's candles are swapped via `candleSeries.setData()`. Each coin maintains its own WebSocket connection and state independently.
- **Background preload reduced from 10 parallel API calls to 1**: `preloadAll()` (which fetched 10 000 candles from the REST API for all 10 coins simultaneously) is replaced by `preloadDefault()` which only preloads the first coin. Other coins load on-demand when the user clicks them, including their WebSocket connection.
- **WebSocket connected after initial candle load**: The promise chain that connects the WebSocket (`connectWs()`) after `loadCandles()` was restored. Without it, no real-time snapshot ever merged into the chart, causing stale candles and gaps.
- **Indicator subsystem now actually initializes**: `initIndicatorSubsystem()` was defined but never called. Now called from the `DOMContentLoaded` handler in `app.js`, which properly sets up `TFIndicatorController.init()` (with `getCurrentBarsFn`), `TFIndicatorPanes`, `TFIndicatorPanel`, `TFIndicatorChips`, and the `_onCandlesUpdated` callback that re-applies indicators on data changes.

### Changed
- **Unified "Matrix" design system**: The entire UI now shares one visual style — a black background with phosphor-green accents and monospace/code fonts for the dark theme, and a clean white background with muted-green accents for the light theme. Drawing toolbar, drawing properties, and the indicators panel now inherit the shared theme variables.
- **Redesigned indicators panel**: More user-friendly layout with a search field, collapsible groups with item counts, clearer applied-state indicators (`+`/`✓`), and consistent monospace styling.
- **Default drawing colors**: New drawings now default to the project's matrix-green palette, and the color swatches lead with the theme greens.
- **Refined Analyze / Pattern Filter UI**: The Analyze button and pattern filter popover were restyled for clarity; the filter now shows a live count badge, highlights when filtering is active, and offers "Select all" / "Clear all" bulk actions.

- **Themed chart & indicator panes**: The candlestick chart, volume bars, volume SMA, and pattern overlays now recolor to match the active theme (matrix-green on black, or muted green on white).
- **Unified chart & indicator grid (single-chart panes)**: Volume and oscillator indicators (RSI, MACD, …) now render as native panes *inside the main chart* instead of as separate chart widgets. All panes share one grid, one time axis and one crosshair, so columns and gridlines line up perfectly. The boundary between the price chart and each indicator is now a single thin separator line (draggable to resize) — the previous per-pane colored header bars, opaque backgrounds and box borders are gone.


### Added
- **Coin search bar**: The coins sidebar now has a search field and a scrollable watchlist, making it easier to find and (in future) add coins. The active coin is highlighted.
- **Market header**: The top bar now shows the selected coin's icon, ticker and name, live price with 24h change, multi-timeframe change readouts (5m / 1h / 4h / 24h), and market cap / circulating supply / 24h volume — all grouped on the left next to the coin identity. Timeframe buttons and the theme toggle sit on the right.

### Removed
- **Top bar clutter**: Removed the LIVE status indicator, the "Indicators" toggle button, and the indicators-panel close (X) button. The indicators panel is now permanently docked on the right of the chart. The theme toggle is now an icon-only button that shows a moon in dark mode and a sun in light mode.



## [2.2.0] — 2026-07-10


### Added
- **Indicators subsystem — 445+ technical indicators**: Integrated `lightweight-charts-indicators` v0.4.2 with `oakscriptjs` v0.2.8, providing 445+ built-in indicators including RSI, MACD, Bollinger Bands, moving averages, candlestick patterns, and community indicators. ([#198](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/198))
- **Indicator persistence API**: New `GET/POST /api/indicators` REST endpoints with SQLite `indicators_blob` table for per-symbol indicator state persistence across sessions.
- **Indicator panel UI**: Slide-out side panel with search input, collapsible groups (Standard / Candlestick Patterns / Community), pinned RSI row, volume toggle, and indicator rows that apply on click.
- **Indicator chips**: Chips bar below the top header showing all applied indicators; click a chip to remove the indicator.
- **Indicator pane system**: Dynamic pane creation for non-overlay indicators (e.g., MACD, Stochastic); volume sub-chart refactored as a pane.
- **RSI auto-apply**: RSI (14) automatically applied when switching to a new symbol if not already present. Closes [#112](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/112). ([#198](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/198))
- **esbuild indicators bundle**: New `npm run build:indicators` script bundles `indicators-src.js` → `indicators-bundle.js`.

### Changed
- **Drawing toolbar layout**: Grid changed from 2-column to 3-column; button size reduced (40→30px), icons 18→14px, border-radius 10→7px. Repositioned from top:12 to top:40, z-index 50→60.
- **Drawing z-order**: All drawing primitives (horizontal-line, vertical-line, cross-line, price-range, trend-line, etc.) set z-order to `"top"` to render above indicator overlays.
- **Drawing label precision**: Price labels use adaptive decimal places based on magnitude (e.g., 6 decimal places for small prices, 2 for large).
- **Drawing timestamp format**: Unix timestamps now display as human-readable `YYYY-MM-DD HH:mm`.
- **Bitmap-aware rendering**: Drawing primitives use `bitmapSize` instead of `viewport.width` for correct HiDPI/retina rendering.
- **Volume sub-chart refactored**: Volume pane integrated into indicator panes subsystem with toggle in the indicators panel.
- **Drawing toolbar default position**: Database default top changed from 12 to 40 in SQLite init.

### Fixed
- **WebSocket race condition**: Stale candle updates after symbol switch prevented by `_wsSymbol`/`_wsInterval` guards. ([#199](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/199))
- **Chart scale reset**: `resetChartScale()` called on cached data load and same-symbol re-request to maintain proper view.
- **Cached data re-render**: Series now clears with `setData([])` before `setData(data)` to force re-render on cache hit.
- **Sidebar async coin switching**: `onCoinClick` made async — properly awaits `loadCandles` before starting WebSocket.
- **Keyboard shortcut interference**: Keyboard shortcuts skip when focus is on `INPUT`/`TEXTAREA` elements; Backspace removed (Delete only).
- **Drawing settings merge**: `DrawingSettings.save()` properly deep-merges per-tool settings instead of full replace.
- **Drawing properties singleton**: Guard against duplicate `init()` calls.
- **Text annotation/callout removal**: Removed problematic tools (text-annotation, callout, brush, highlighter) from toolbar.

### Removed
- **Text annotation, Callout, Brush, Highlighter tools**: Removed from drawing toolbar due to rendering issues.
- **Keyboard shortcuts for individual tools**: Removed to prevent interference with text input; Escape/Delete retained.

## [2.0.0] — 2026-07-06 (MVP v2 — Sprint 4)

### Added
- **UI redesign — Coin icons, Fear & Greed Index, sidebar overhaul**: Coin rows now show icon images (CoinGecko), ticker symbol, full name, and 24h change %. Fear & Greed Index widget added to sidebar with SVG gauge. Lucide icons integrated for UI elements. Dynamic price precision based on magnitude. ([#158](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/158))
- **Drawing toolbar re-architecture with lightweight-charts-drawing library**: Complete modular rewrite of drawing system — 7 new JS modules (controller, events, state, settings, toolbar, properties, bundle). External `lightweight-charts-drawing` library integrated for advanced drawing capabilities. Toolbar moved to right side of chart. Dedicated CSS files (`drawing-toolbar.css`, `drawing-properties.css`). ([#158](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/158))
- **Lightweight Charts v5 upgrade**: Upgraded from v4 to v5.2.0, enabling new API features and improved rendering.
- **Volume sub-chart**: Dedicated volume pane below main chart with volume series (colored bars) and SMA overlay line. Configurable pane height ratios for main vs volume view. ([#113](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/113))
- **Coin icon service**: New `coin_icons.py` backend service fetches coin logos from CoinGecko API with 1-hour TTL cache. Exposed via `/api/coins/icons` endpoint.
- **Fear & Greed Index service**: New `fng_client.py` backend service fetches market sentiment index from alternative.me API with 6-hour TTL cache. Exposed via `/api/fng` endpoint.
- **esbuild bundling pipeline**: `package.json` with `npm run build:drawings` script that bundles `drawing-overlay-src.js` → `drawing-bundle.js` via esbuild for production.
- **Multi-interval database caching & warmup**: Backend warmup loads candles for all 5 intervals (5m, 15m, 1h, 4h, 1d) from SQLite into memory in parallel. Three-tier cache (mem → DB → exchange) with sub-millisecond cache hits on coin/interval switch. ([#122](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/122))
- **Configurable candle analysis limit**: Input field next to ANALYZE PATTERNS button lets users set 100–500000 candles for pattern detection. Passed as `limit` param to `/api/analyze/{symbol}`. ([#123](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/123))
- **ML pattern visualization with merged segments**: Pattern results rendered as merged, non-overlapping window segments (50-candle windows) with dotted red vertical boundary lines. Overlapping segments merged into contiguous blocks. ([#124](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/124))
- **ML inference performance optimization**: XGBoost-based pipeline replaces slow TensorFlow approach. Inference time reduced from >10s to <0.5s per 1k candles with NMS clustering and smart geometry features. ([#125](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/125))
- **Sidebar resize with persistence**: Draggable resize handle between sidebar and main area. Width constrained to 150–400px and persisted in localStorage (`tickframe_sidebar_width`). Touch event support included. ([#126](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/126))
- **Cache-busting for static assets**: `?v=1` query param appended to all CSS/JS links to force browser cache invalidation on deployment. ([#126](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/126))
- **Timeframe switching UI**: Working interval selector buttons (5m, 15m, 1h, 4h, 1d) in top bar trigger chart reload and WebSocket restart for selected interval.

### Changed
- **Lightweight Charts upgraded**: From v4 (unpkg `latest`) to v5.2.0 (pinned version) — improved performance and new drawing API.
- **Drawing toolbar architecture**: From monolithic inline HTML toolbar with single `drawing-overlay.js` to modular 7-file JavaScript system with esbuild bundling.
- **Coin sidebar design**: From simple badge+name+price to rich layout with coin icon, ticker, full name, price, and 24h change percentage.
- **Theme system**: Streamlined CSS variables; left-toolbar theme styles removed (toolbar moved to right side with dedicated CSS).
- **Timeframe warmup expanded**: From single 5m interval to all 5 intervals (5m, 15m, 1h, 4h, 1d) during cache warmup phase.
- **Analysis input default**: Default candle limit changed from hardcoded 50000 to configurable 10000 (range 100–500000).

### Fixed
- **Pattern segment collision**: Overlapping 50-candle window segments are now merged into contiguous blocks instead of rendering overlapping/double boundary lines.
- **V-line positioning**: `_visibleBottomPrice()` helper fixes v-line rendering at bottom of visible price range instead of hardcoded price=0.
- **Text tool 1-point commit logic**: Fixed to only auto-commit single-point tools that aren't the text tool (which requires label input).

### Removed
- **Old left-toolbar HTML**: Inline HTML for left drawing toolbar removed — replaced by modular right-side toolbar.
- **Legacy `toolbar.js`**: Replaced by new modular drawing system.
- **Old left-toolbar CSS**: All `.left-toolbar`, `.lt-btn`, `.lt-sep`, `.lt-group` styles removed from `styles.css`.
- **Search input**: Removed from sidebar (no backend search support).
- **Toolbar status bar** (`#tb-status`): Redundant status indicator removed.
- **Redact button** from left toolbar: Superfluous entry removed.

---

## [1.1.0] — 2026-06-26

### Added
- **API rate limiting**: Token-bucket `RateLimiter` (10 req/s, burst 5) on all Bybit/Binance candle requests — prevents 429 errors during warmup and zoom-out pagination.
- **DB query optimisation**: `load_last_n_candles()` with exact `ORDER BY time DESC LIMIT N` (sub-millisecond, no cooldown), `load_candles_before()`, `get_candle_range()`; indexed PK queries avoid loading 55k rows.
- **Frontend candle cache**: `_candleCache` map (keyed by `symbol|interval`) returns cached data instantly on coin re-switch, then refreshes in background.
- **Zoom-out lazy loading**: `before` query parameter on `/api/coins/{symbol}/candles`; `loadMoreBefore()` fetches older candles via pagination and appends to chart.
- **Coin switch loading overlay**: Animated spinner overlay (`<div id="chartLoading">`) for both lightweight and advanced (TradingView) modes; auto-hides via `window._hideChartLoading` callback when candles arrive; 5s fallback timeout.
- **`end_ms` pagination parameter**: `fetch_candles(end_ms)` and `_fetch_binance_candles(endTime)` support fetching candles before a timestamp — enables sequential per-coin fill up to 55000.
- **Drawing toolbar engine**: 13 drawing tools on canvas overlay (Trend Line, H-Line, V-Line, Ray, Cross Line, Fibonacci, Price Range %, Rectangle, Circle, Arrow, Text, Brush, Redact). ([#62](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/62))
- **Advanced drawing tools**: Fibonacci retracement, Price Range %, Text tool with custom modal. ([#64](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/64))
- **Redact mode**: Chart freeze, selection, drag-to-move/reshape for drawings. ([#63](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/63))
- **Undo system**: Full undo/redo stack for add, modify (drag), and delete operations. ([#66](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/66))
- **Per-drawing settings panel**: Color, width, line style, font size with SVG icons. ([#65](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/65))
- **SQLite persistence**: Drawings, settings, and candle data survive container restart. ([#67](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/67))
- **WebSocket heartbeat**: Backend sends heartbeat every 5s; frontend shows LIVE status indicator. ([#69](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/69))
- **Pattern Analysis UI**: Sliding window (50 candles, step 10), red dashed vertical lines + labels, confidence threshold slider. ([#70](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/70))
- **Coin sidebar enhancements**: Full ticker badges, trend-colored prices, 6-digit price formatting. ([#61](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/61))
- **Theme persistence**: Theme saved to SQLite, restored on reload, drawing colors adapt to theme. ([#71](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/71))
- **Quality requirements**: QR-001 (Performance), QR-002 (Security), QR-003 (Accuracy) documented in `docs/quality-requirements.md`.
- **Quality requirement tests**: Automated QRT-001 (performance), QRT-002 (security), QRT-003 (accuracy) in `tests/requirements/`.
- **CI pipeline**: GitHub Actions workflow with lint (ruff), type-check (mypy), test (pytest + coverage), QA (bandit). ([#86](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/86))
- **Testing strategy doc**: `docs/testing.md` covering unit, integration, and QRT testing.
- **Sprint 3 planning**: 20+ PBIs created and assigned to Sprint 3 milestone.

### Changed
- **Candle limit increased**: Maximum per request from 1000 to 50000 (all endpoints, datafeed, frontend).
- **Two-phase warmup**: Phase 1 loads DB candles for all 50 (coin×interval) combos in parallel; Phase 2 fills each coin sequentially to 55000 with rate-limited pagination via `end_ms`.
- **Removed exchange freshness check on DB hit**: `load_last_n_candles` now uses the exact `limit` (e.g. 10000) instead of hardcoded `MAX_CANDLES`; WS live updates keep data fresh without burning API calls on coin switch.
- **Warmup configurable**: Changed from hardcoded 50 to `max(50, min(limit // 4, 500))`.
- **DB transaction**: `_save_candles()` uses explicit `BEGIN`/`COMMIT` for 50k-row performance.
- **Definition of Done**: Restructured with CI check table, quality requirements, code quality criteria.
- **Roadmap**: Updated with Sprint 3 PBI list and Sprint 4 plan.

### Fixed
- **Coin switch race condition (chart stuck on BTC)**: `window.candleSeries` now used everywhere instead of local `candleSeries` variable — toolbar.js `switchChartType()` reassigns the global when user changes chart type, leaving local references stale.
- **AbortController race prevention**: Each `loadCandles()` call creates a new `AbortController`; stale in-flight fetches are aborted on rapid coin switch; `_currentLoadSymbol` guard discards stale responses after JSON parse.
- **Double-load on startup**: Removed redundant BTC load in app.js; `_initialLoadDone` flag prevents 300ms timeout override if user already clicked a coin.
- **Candle cache stale on zoom-out/WS**: `loadMoreBefore()` and WebSocket handlers update `_candleCache` so re-switch shows fresh data.
- **Drag undo**: Pre-capture `prevPoints` at drag start (not after mutation).
- **Delete undo**: Deleted drawings wrapped in `{action:'add'}` envelope for re-insert on undo.
- **Race condition**: `_loadDrawings()` sequence counter discards stale responses on rapid coin switch.
- **Canvas state leak**: Brush renderer wrapped in `ctx.save()`/`ctx.restore()`.
- **Document listener cleanup**: Global click listeners stored in `_listeners` array, removed on `destroy()`.
- **Per-drawing opts forwarding**: `opacity`, `fill`, `lineStyle`, `fontSize` now set on commit.
- **Empty catch blocks**: Replaced with `console.warn()`.
- **Dead code removed**: Unused `preview` variable, `textModalReject`, stray comment separators.
- **Dead conftest fixtures**: Removed stale fixtures that caused test warnings.
- Blank QRT test templates replaced with real tests.

---

## [1.0.0] (MVP v1) — 2026-06-21

### Added
- **FastAPI REST API**: New endpoints at `/api/health`, `/api/coins`, `/api/coins/{symbol}/price`, and `/api/coins/{symbol}/candles` with configurable candle limits up to 1000. ([#28])
- **WebSocket real-time streams**: Live market snapshot (`/ws/market`) and candle updates (`/ws/candles/{symbol}`) with 5-second polling interval. ([#28])
- **Interactive candlestick chart**: TradingView Lightweight Charts integration with dark/light theme toggle, time scale navigation, and responsive resize. ([#28], [#16])
- **Coin sidebar**: Live price list for all tracked trading pairs with real-time updates via WebSocket. ([#28])
- **Analysis window markers**: Vertical boundary lines on the chart highlighting the last 50 candles for pattern detection context. ([#28])
- **Docker deployment**: One-command startup via `docker compose up --build` with containerized FastAPI + Uvicorn stack. ([#8], [#37], [#39], [#40])
- **Candle data limit increased**: Maximum candles per request raised from 200 to 1000, enabling longer historical chart views. ([commit 165abde](https://github.com/Fedos113/SWP_TickFrame_28_team/commit/165abde29d9a906cee9b1b2f05df85cb84b7fee0))
- **Mock ML pattern detection**: Analyzes last 50 candles and returns pattern type (Bull Flag, Head & Shoulders, etc.) with randomized confidence score. ([#28])
- **Async Bybit v5 client**: Automatic fallback to Binance API when Bybit requests fail, with in-memory cache auto-refreshing every 5 seconds. ([#28])
- **CLI commands**: `scan` (fetch OHLCV data), `report` (generate Markdown reports), `analyze` (cache + pattern detection), and `serve` (legacy dashboard) with async backend support. ([#28])

### Changed
- **Architecture migration**: Backend rewritten from synchronous Python `http.server` (port 5000) to **FastAPI + Uvicorn** async stack (port 8000). Improved performance, scalability, and real-time capabilities. ([#28])
- **README restructured**: Docker-first setup instructions with VM-agnostic IP guidance, separated local development from deployment workflows. ([#40])
- **Data pipeline upgraded**: Legacy threaded Bybit client replaced with async `httpx`-based client; cache refresh interval reduced from 60s to 5s for fresher data. ([#28])
- **Project documentation**: User stories registry (`docs/user-stories.md`), roadmap (`docs/roadmap.md`), and Definition of Done (`docs/definition-of-done.md`) established and linked from README. ([#34], [#38])
- **CLI fallback preserved**: Legacy `--mock` flag retained for demo/offline usage — all CLI commands work with or without real API connectivity. ([#28])

### Fixed
- No fixes in this release (initial MVP v1 cut).

---

[3.0.0]: https://github.com/Fedos113/SWP_TickFrame_28_team/releases/tag/v3.0.0
[Unreleased]: https://github.com/Fedos113/SWP_TickFrame_28_team/compare/v3.0.0...HEAD
[2.2.0]: https://github.com/Fedos113/SWP_TickFrame_28_team/releases/tag/2.2.0
[2.0.0]: https://github.com/Fedos113/SWP_TickFrame_28_team/releases/tag/2.0.0
[1.1.0]: https://github.com/Fedos113/SWP_TickFrame_28_team/releases/tag/v1.1.0
[1.0.0]: https://github.com/Fedos113/SWP_TickFrame_28_team/releases/tag/SemVer

[#8]: https://github.com/Fedos113/SWP_TickFrame_28_team/issues/8
[#16]: https://github.com/Fedos113/SWP_TickFrame_28_team/issues/16
[#28]: https://github.com/Fedos113/SWP_TickFrame_28_team/pull/28
[#34]: https://github.com/Fedos113/SWP_TickFrame_28_team/pull/34
[#37]: https://github.com/Fedos113/SWP_TickFrame_28_team/pull/37
[#38]: https://github.com/Fedos113/SWP_TickFrame_28_team/pull/38
[#39]: https://github.com/Fedos113/SWP_TickFrame_28_team/pull/39
[#40]: https://github.com/Fedos113/SWP_TickFrame_28_team/pull/40
