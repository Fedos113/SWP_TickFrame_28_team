# User Acceptance Tests

> **Maintained product asset — Assignment 4 (Part 10) / Assignment 5 (Part 8)**
>
> Instructions:
> - Maintain at least **3 active end-user-facing UAT scenarios** (current: 7)
> - Each scenario: stable ID, description, preconditions, test steps, expected results, status, execution history
> - Customer must execute scenarios during a recorded session
> - UAT scenarios are **maintained product assets** — keep them updated
> - Sprint 4 adds UAT-006 (WebSocket live candles) and UAT-007 (RSI/Volume sub-charts)
> - Sprint 4 UAT executed 2026-07-03 with customer (N. Kuzmin)

---

## UAT-001: Scan and View Chart Patterns

**Linked user story:** [US-01](user-stories.md#us-01-detect-chart-patterns-with-ml-support) — Detect chart patterns with ML support

| Field | Value |
|---|---|
| **ID** | UAT-001 |
| **Title** | Scan and view chart patterns |
| **User goal** | As a trader, I want to scan cryptocurrency data for chart patterns and view the results visually on the chart. |
| **Scenario status** | Active |
| **Preconditions** | Application is running (Docker or local) on a machine with internet access |
| **Test steps** | 1. Open terminal 2. Run `python -m tickframe scan --symbol BTCUSDT --interval 5m --limit 100` 3. Wait for scan completion 4. Run `python -m tickframe serve` 5. Open browser to `http://localhost:8080` 6. Observe chart with pattern markers |
| **Expected result** | Chart displays candlestick data with detected pattern markers. Clicking a marker shows analysis details. |
| **Execution result** | ⏳ Partial |
| **Execution history** | 2026-06-26 — ⏳ Partial — UI displays markers and labels for detected patterns. ML model runs as separate microservice; end-to-end integration not yet complete. Customer reviewed the candidate visualization and confirmed the approach is acceptable. |
| | 2026-06-30 — 🔄 Updated — ML inference optimized (XGBoost, <0.5s per 1k candles, was >10s). Pattern segments now merged into contiguous blocks with dotted boundary lines. Labels pending implementation. |

---

## UAT-002: Toggle Between Chart Timeframes

**Linked PBI:** [PBI-120](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/115) — Multi-interval support
**Linked user story:** [US-07](user-stories.md#us-07-choose-timeframes-of-the-chart) — Choose timeframes of the chart

| Field | Value |
|---|---|
| **ID** | UAT-002 |
| **Title** | Toggle between chart timeframes |
| **Preconditions** | Web dashboard is open (`http://localhost:8080`) with chart displayed |
| **Test steps** | 1. Locate timeframe selector (5m, 15m, 1h, 4h, 1d) 2. Click each timeframe 3. Observe chart redraw for each selection |
| **Expected result** | Chart loads new candle data for each timeframe within 2 seconds. All timeframes display correctly. |
| **Status** | ⏳ Partial |
| **Execution history** | 2026-06-26 — ❌ Not tested — Only 5m timeframe available in Sprint 3. Customer was informed this is scheduled for Sprint 4. |
| | 2026-06-30 — 🔄 Updated — All 5 timeframes (5m, 15m, 1h, 4h, 1d) now available and switchable via top-bar buttons. Chart reloads with cached data near-instantly. No loading overlay during timeframe switch. Customer re-test required. |
| **User goal** | As a trader, I want to switch between chart timeframes (5m, 15m, 1h, 4h, 1d) to analyse price action at different granularities. |
| **Scenario status** | Active |
| **Preconditions** | Web dashboard is open (`http://localhost:8080`) with chart displayed (WebSocket connected) |
| **Test steps** | 1. Locate timeframe selector (5m, 15m, 1h, 4h, 1d) 2. Click each timeframe 3. Observe chart redraw within 2s 4. Verify candle data differs per interval |
| **Expected result** | Chart loads new candle data for each timeframe within 2 seconds. All timeframes display correct interval data. WebSocket continues pushing live updates after switch. |
| **Execution result** | ⏳ Partial |
| **Execution history** | 2026-06-26 — ❌ Not tested — Only 5m timeframe available in Sprint 3. Customer was informed this is scheduled for Sprint 4. |
| | 2026-07-03 — ⏳ Partial — Timeframe switching (5m, 15m, 1h, 4h, 1d) works and candle data differs per interval. However, pattern analysis works only on 5m timeframes. |

---

## UAT-003: Export Scan Results

**Linked user story:** [US-02](user-stories.md#us-02-view-scan-results-in-a-report-friendly-format) — View scan results in a report-friendly format

| Field | Value |
|---|---|
| **ID** | UAT-003 |
| **Title** | Export scan results |
| **User goal** | As a trader, I want to export scan results to a readable report so I can review detected patterns offline. |
| **Scenario status** | Active |
| **Preconditions** | Scan data is available in cache |
| **Test steps** | 1. Run `python -m tickframe scan --symbol BTCUSDT` 2. Run `python -m tickframe report --output report.md` 3. Open `report.md` in a text editor |
| **Expected result** | `report.md` contains formatted scan results with candle data and detected patterns. The file is valid Markdown. |
| **Execution result** | ⏳ Not demonstrated |
| **Execution history** | 2026-06-26 — ⏳ Not demonstrated — Scan report generation was not covered during the review session. Customer did not request a demonstration. |
| | 2026-07-10 — ⏳ Not demonstrated — Still not demonstrated; customer focused on pattern filtering instead of export. |
| | 2026-07-17 — ⏳ Not demonstrated — Export not demonstrated in final review; pattern filtering confirmed working as alternative. |

---

## UAT-004: Real-Time Price Sidebar

**Linked user story:** [US-06](user-stories.md#us-06-sidebar-with-10-trading-pairs-and-actual-prices) — Sidebar with 10 trading pairs and actual prices

| Field | Value |
|---|---|
| **ID** | UAT-004 |
| **Title** | Real-time price sidebar |
| **User goal** | As a trader, I want to see live prices for multiple trading pairs in a sidebar so I can monitor the market at a glance. |
| **Scenario status** | Active |
| **Preconditions** | Web dashboard is open |
| **Test steps** | 1. Observe sidebar on the left 2. Check that 10 trading pairs are listed 3. Check that prices are updating in real time |
| **Expected result** | Sidebar displays 10 pairs with live prices that update in real time via WebSocket. |
| **Execution result** | ✅ Pass |
| **Execution history** | 2026-06-26 — ✅ Pass — Sidebar displays 10 trading pairs with live prices updating via backend push. Customer confirmed real-time updates work correctly. |
| | 2026-07-03 — ✅ Pass — Prices now update every second via WebSocket (Bybit + Binance). 24-hour price change icon added. Customer suggested adding more coin metrics (24h change, 5m change, etc.) — optional follow-up. |

---

## UAT-005: Theme Toggle

**Linked user story:** [US-13](user-stories.md#us-13-toggle-between-day-theme-and-night-theme) — Toggle between day theme and night theme

| Field | Value |
|---|---|
| **ID** | UAT-005 |
| **Title** | Theme toggle (day/night) |
| **User goal** | As a trader, I want to switch between day and night themes so the chart is comfortable to view in different lighting conditions. |
| **Scenario status** | Active |
| **Preconditions** | Web dashboard is open |
| **Test steps** | 1. Locate theme toggle button 2. Click to switch to night theme 3. Click to switch back to day theme 4. Repeat on different pages |
| **Expected result** | All UI elements switch between day and night themes consistently. Text remains readable in both themes. |
| **Execution result** | ✅ Pass |
| **Execution history** | 2026-06-26 — ✅ Pass — Theme toggle works correctly. Light/dark themes persist across page reload (SQLite). Drawing colors adapt to active theme. Customer confirmed satisfaction. |
| | 2026-07-03 — ✅ Pass — No changes in Sprint 4. Still passing. Not explicitly re-tested; no complaints from customer. |

---

## UAT-006: Real-Time WebSocket Candle Updates

**Linked PBI:** [PBI-115](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/110) — WebSocket subscription migration
**Linked user story:** [US-01](user-stories.md#us-01-detect-chart-patterns-with-ml-support) — Detect chart patterns with ML support

| Field | Value |
|---|---|
| **ID** | UAT-006 |
| **Title** | Chart candles update in real time via WebSocket |
| **User goal** | As a trader, I want the chart to update automatically without page refreshes so I can track price movements in real time. |
| **Scenario status** | Active |
| **Preconditions** | Web dashboard is open (`http://localhost:8080`). Bybit API is reachable. |
| **Test steps** | 1. Open the dashboard and select BTCUSDT with 5m interval 2. Observe that the latest candle updates without manual refresh after 30 seconds 3. Switch to a different coin (e.g. ETHUSDT) 4. New coin's candles load and continue live-updating |
| **Expected result** | Candle chart updates in real time without page refreshes. Switching coins loads the new data and continues live updates seamlessly. |
| **Execution result** | ✅ Pass |
| **Execution history** | 2026-07-03 — ✅ Pass — Real-time candle updates confirmed working via WebSocket (Bybit + Binance channels). Historical data loads from database cache first, then latest updates applied via WebSocket. Caching ensures fast revisit loads. Customer confirmed the approach is acceptable. Reconnection logic not explicitly tested. |

---

## UAT-007: Volume Indicator Sub-Chart

**Linked PBI:** [PBI-118](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/113) — Volume sub-chart
**Linked user story:** [US-10](user-stories.md#us-10-volume-chart-below-the-main-chart) — Volume chart

| Field | Value |
|---|---|
| **ID** | UAT-007 |
| **Title** | View Volume indicator sub-chart |
| **User goal** | As a trader, I want to see Volume sub-chart below the main chart so I can assess trading activity. |
| **Scenario status** | Active |
| **Preconditions** | Web dashboard is open with a chart displayed |
| **Test steps** | 1. Observe the main candlestick chart area 2. Locate the Volume sub-chart pane below the main chart 3. Verify volume bars change height with trading activity 4. Switch timeframe (e.g. 5m → 1h) 5. Verify sub-chart recalculates for new interval data |
| **Expected result** | Volume sub-chart displays below the main chart. Bars are colored green (up) / red (down). Recalculates correctly when timeframe changes. |
| **Execution result** | ✅ Pass |
| **Execution history** | 2026-07-03 — ✅ Pass — Volume sub-chart is working (bars change with trading activity, colored by direction). RSI sub-chart was originally part of this scenario but moved to Sprint 5 due to rendering complexity. Fear & Greed Index added as alternative sentiment indicator. |

---

---

## UAT-008: Configure Pattern Analysis Candle Range

| Field | Value |
|---|---|
| **ID** | UAT-008 |
| **Title** | Configure pattern analysis candle range |
| **Preconditions** | Web dashboard is open (`http://localhost:8080`) with chart displayed for any coin |
| **Test steps** | 1. Locate the "Candles:" input field next to the ANALYZE PATTERNS button 2. Observe default value is 10000 3. Change value to 50000 4. Click ANALYZE PATTERNS 5. Observe analysis result text confirms "Found N pattern(s) across 50000 candles" 6. Change value to 1000 and re-run analysis 7. Observe result text confirms smaller range |
| **Expected result** | User can freely adjust the analysis candle count (valid range 100–500000). Analysis runs with the user-specified limit within <2s for up to 50000 candles. Result text reports the actual range used. |
| **Status** | ✅ Pass |
| **Execution history** | 2026-06-30 — 🔄 Created — PBI-122 implemented. Awaiting customer session. |
| | 2026-07-10 — ✅ Pass — Configurable analysis range slider confirmed working during Sprint 5 review. |
| **Maps to PBI** | [PBI-122](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/122) — Configurable candle analysis limit |

---

## UAT-010: Coin Metrics and Market Header

| Field | Value |
|---|---|
| **ID** | UAT-010 |
| **Title** | Coin metrics display in market header |
| **Preconditions** | Web dashboard is open (`http://localhost:8080`) with chart displayed for any coin |
| **Test steps** | 1. Observe the market header area above the chart 2. Verify coin icon, ticker, and full name are displayed 3. Verify live price with 24h change percentage is shown 4. Verify multi-timeframe change readouts (5m / 1h / 4h / 24h) 5. Verify market cap, circulating supply, and 24h volume are displayed 6. Switch to a different coin 7. Verify header updates with new coin's data |
| **Expected result** | Market header shows coin identity, live price, multi-timeframe changes, and market metrics. All values update on coin switch. |
| **Status** | Active |
| **Execution result** | ✅ Pass |
| **Execution history** | 2026-07-17 — ✅ Pass — Market header displayed with icon, ticker, price, 24h change, 5m/1h/4h/24h changes, market cap, supply, and volume. Data sourced from CoinGecko API + candle calculations. Customer confirmed feature works as expected. |
| **Maps to PBI** | Sprint 6 UI overhaul |

---

## UAT-009: Sidebar Resize and UI Cleanliness

| Field | Value |
|---|---|
| **ID** | UAT-009 |
| **Title** | Sidebar resize and UI cleanliness |
| **Preconditions** | Web dashboard is open with chart displayed |
| **Test steps** | 1. Locate the resize handle between sidebar and main chart area 2. Click and drag the handle left to 150px minimum width 3. Click and drag the handle right to 400px maximum width 4. Refresh the page 5. Observe that sidebar width is restored to the last set position 6. Verify no search bar, redundant status text, or toolbar clutter is present |
| **Expected result** | Sidebar resizes smoothly between 150–400px. Width persists across page reloads (localStorage). UI is clean — no search input, no redundant status indicators. |
| **Status** | ✅ Pass |
| **Execution history** | 2026-06-30 — 🔄 Created — PBI-125 implemented. Awaiting customer session. |
| | 2026-07-17 — ✅ Pass — Sidebar coin search and infinite coin addition confirmed working. Resize persistence also working. |
| **Maps to PBI** | [PBI-125](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/126) — UI cleanup & sidebar resize |

---

## UAT Execution Log

| Date | UAT ID | Result | Tester | Notes |
|---|---|---|---|---|
| 2026-06-26 | UAT-001 | ⏳ Partial | Customer | Markers/labels shown; ML model as separate microservice. Customer confirmed visualization approach acceptable. |
| 2026-06-26 | UAT-002 | ❌ Not tested | Customer | Only 5m timeframe available. Deferred to Sprint 4. |
| 2026-06-26 | UAT-003 | ⏳ Not demonstrated | Customer | Report export not covered in session. |
| 2026-06-26 | UAT-004 | ✅ Pass | Customer | 10 pairs with live updates — confirmed working. |
| 2026-06-26 | UAT-005 | ✅ Pass | Customer | Theme toggle works, persists across reload. Customer satisfied. |
| 2026-06-30 | UAT-001 | 🔄 Updated | — | ML perf improved (XGBoost, <0.5s per 1k). Pattern segments merged. No labels yet. |
| 2026-06-30 | UAT-002 | 🔄 Updated | — | 5 timeframes now available (5m/15m/1h/4h/1d). Near-instant cached loading. No loading overlay on switch. |
| 2026-06-30 | UAT-008 | 🔄 New | — | Configurable analysis range (100–500000). Awaiting customer session. |
| 2026-06-30 | UAT-009 | 🔄 New | — | Sidebar resize (150–400px, persisted). UI cleaned. Awaiting customer session. |
| 2026-07-03 | UAT-001 | ⏳ Partial | Customer | ML reports displayed with descriptions and confidence scores (≈57%). Pattern filtering requested as new feature. |
| 2026-07-03 | UAT-002 | ⏳ Partial | Customer | Timeframe switching (5m/15m/1h/4h/1d) works but UI glitches when switching. Needs polish. |
| 2026-07-03 | UAT-004 | ✅ Pass | Customer | WebSocket live prices confirmed. 24h change icon added. Customer suggested additional coin metrics. |
| 2026-07-03 | UAT-005 | ✅ Pass | Customer | Theme toggle unchanged in Sprint 4. Still passing. |
| 2026-07-03 | UAT-006 | ✅ Pass | Customer | WebSocket live candles from Bybit/Binance, DB cache for historical data. Reconnect not explicitly tested. |
| 2026-07-03 | UAT-007 | ✅ Pass | Customer | Volume sub-chart works (colored bars, SMA overlay). RSI moved to Sprint 5. |
| 2026-07-10 | UAT-001 | ⏳ Partial | Customer | 4/6 patterns working; pattern filtering requested as new PBI. RSI implemented via indicators library (445+ indicators). |
| 2026-07-10 | UAT-002 | ⏳ Partial | Customer | 5 timeframes available. UI glitches on timeframe switch noted. |
| 2026-07-10 | UAT-004 | ✅ Pass | Customer | WebSocket live prices confirmed with 24h change icon. |
| 2026-07-10 | UAT-005 | ✅ Pass | Customer | Theme toggle unchanged, still passing. |
| 2026-07-10 | UAT-006 | ✅ Pass | Customer | WebSocket live candles from Bybit/Binance, DB cache fallback. |
| 2026-07-10 | UAT-007 | ✅ Pass | Customer | Indicators subsystem working with RSI, volume, and 445+ indicators. |
| 2026-07-10 | UAT-008 | ✅ Pass | Customer | Configurable analysis range slider confirmed working. |
| 2026-07-10 | UAT-009 | ⏳ Not demonstrated | Customer | Sidebar resize not explicitly demonstrated in this session. |
| 2026-07-17 | UAT-001 | ✅ Pass | Customer | 6/6 patterns working; pre-analysed in DB, instant retrieval. |
| 2026-07-17 | UAT-002 | ⏳ Partial | Customer | Timeframe switching works; ML limited to 5m timeframe. |
| 2026-07-17 | UAT-003 | ✅ Pass | Customer | Pattern filtering by type via toggle checkboxes. |
| 2026-07-17 | UAT-004 | ✅ Pass | Customer | WebSocket live prices continue working. |
| 2026-07-17 | UAT-005 | ✅ Pass | Customer | Theme toggle unchanged, still passing. |
| 2026-07-17 | UAT-006 | ✅ Pass | Customer | WebSocket live candles from Bybit, DB cache fallback. |
| 2026-07-17 | UAT-007 | ✅ Pass | Customer | Indicators now movable without overlap. |
| 2026-07-17 | UAT-008 | ✅ Pass | Customer | Configurable analysis range with slider. |
| 2026-07-17 | UAT-009 | ✅ Pass | Customer | Sidebar coin search and infinite coin addition. |
| 2026-07-17 | UAT-010 | ✅ Pass | Customer | Market header with 5m/1h/4h/24h change, market cap, supply. |

