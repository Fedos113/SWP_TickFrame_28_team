# Project Roadmap

## Sprint 1 — Repository & Process Foundation

| Field | Value |
|---|---|
| **Milestone** | [Sprint 1](https://github.com/Fedos113/SWP_TickFrame_28_team/milestone/1) |
| **Dates** | Week 2 |
| **Goal** | Establish repository structure, licensing, and team workflow conventions. |
| **Focus** | Repo hygiene, environment scaffold, PR/issue process |

**Planned items:**

- [#007](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/7) US-03 — Public repo with MIT license
- [#010](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/10) US-04 — Reusable `.env` template
- [#012](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/12) US-05 — PR template for review consistency

---

## Sprint 2 — MVP v1 Core Features

| Field | Value |
|---|---|
| **Milestone** | [Sprint 2](https://github.com/Fedos113/SWP_TickFrame_28_team/milestone/2) |
| **Dates** | Week 3 |
| **Goal** | Deliver a working MVP v1 increment with real ML pattern detection and basic UI features. |
| **Focus** | XGBoost model integration, chart pattern detection, theme toggle |

**Planned items:**

- [#005](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/5) US-01 — Detect chart patterns with ML support
- [#016](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/16) US-13 — Toggle between day and night theme

---

## Sprint 3 — v1.1.0 Drawing Tools + Quality Gates

| Field | Value |
|---|---|
| **Milestone** | [Sprint 3 — Assignment 4 — v1.2.0](https://github.com/Fedos113/SWP_TickFrame_28_team/milestone/3) |
| **Dates** | Week 4 (2026-06-22 – 2026-06-29) |
| **Goal** | Replace mock pattern analyzer with real ML, deliver drawing toolbar, and establish quality foundations. |
| **Focus** | Drawing tools, SQLite persistence, pattern analysis UI, quality gates, CI, test coverage |

**Planned items:**

- [#62](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/62) PBI-101 — Drawing Toolbar Engine (13 tools)
- [#64](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/64) PBI-102 — Advanced Drawing Tools (Fibonacci, Price Range %, Text)
- [#63](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/63) PBI-103 — Redact Mode + Selection + Drag
- [#66](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/66) PBI-104 — Undo System
- [#65](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/65) PBI-105 — Per-Drawing Settings Panel
- [#67](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/67) PBI-106 — SQLite Persistence
- [#68](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/68) PBI-107 — 50k Candle Support
- [#69](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/69) PBI-108 — WebSocket Heartbeat
- [#70](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/70) PBI-109 — Pattern Analysis UI
- [#61](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/61) PBI-110 — Coin Sidebar Enhancements
- [#71](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/71) PBI-111 — Theme Persistence
- [#79](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/79) QR-001 — Performance Requirement
- [#80](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/80) QR-002 — Security Requirement
- [#81](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/81) QR-003 — Accuracy Requirement
- [#82](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/82) QRT-001 — Performance Test Automation
- [#83](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/83) QRT-002 — Security Test Automation
- [#84](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/84) QRT-003 — Accuracy Test Automation
- [#85](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/85) — Test Coverage ≥30%
- [#86](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/86) — CI Pipeline Setup
- [#72](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/72) — Bug Fixes Batch

---

## Sprint 4 — MVP v2 (Assignment 5)

| Field | Value |
|---|---|
| **Milestone** | [Sprint 4](https://github.com/Fedos113/SWP_TickFrame_28_team/milestone/5) |
| **Dates** | Week 5 (2026-06-30 – 2026-07-06) |
| **Goal** | Deliver MVP v2 by addressing all critical customer feedback from Sprint 3: DB caching, Volume sub-chart, UI redesign, drawing toolbar modernization, multi-interval support, analysis range fix, and WebSocket live data pipeline. RSI deferred to Sprint 5. |
| **Focus** | Customer-driven improvements, architecture hardening, real-time data pipeline, UI/UX overhaul |

**Completed PBIs:**

- [#122 PBI-121](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/122) — Multi-interval database caching & instant chart loading (Critical) ✅
- [#123 PBI-122](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/123) — Configurable candle analysis limit (Medium) ✅
- [#124 PBI-123](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/124) — ML pattern visualization with merged segments (High) ✅
- [#125 PBI-124](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/125) — ML inference performance optimization XGBoost (Critical) ✅
- [#126 PBI-125](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/126) — UI cleanup & sidebar resize (Medium) ✅
- [#158 PBI-126](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/158) — UI redesign: coin icons, Fear & Greed Index, sidebar overhaul (Medium) ✅
- [#159 PBI-127](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/159) — Drawing toolbar re-architecture with lightweight-charts-drawing library (High) ✅
- [#113 PBI-118](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/113) — Volume sub-chart implementation (High) ✅
- [#110 PBI-115](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/110) — WebSocket subscription migration (Critical) ✅

**Deferred to Sprint 5:**
- [#112 PBI-117](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/112) — RSI indicator sub-chart (High) — rendering complexity with current library

---

## Sprint 5 — Week 6 Trial Release (Assignment 6)

| Field | Value |
|---|---|
| **Milestone** | [Sprint 5](https://github.com/Fedos113/SWP_TickFrame_28_team/milestone/6) |
| **Dates** | Week 6 (2026-07-07 – 2026-07-13) |
| **Goal** | Produce stable trial/handover-candidate release with customer-facing documentation review and transition-readiness evidence. |
| **Focus** | RSI implementation, documentation polish, handover prep, customer trial |

**Planned items:**
- [#112 PBI-117](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/112) — RSI indicator sub-chart (High)
- [#177 PBI-129](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/177) — Customer-facing documentation review and update
- [#178](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/178) — Create/update CONTRIBUTING.md and AGENTS.md
- [#179](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/179) — Create/update docs/customer-handover.md
- [#180](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/180) — Week 6 trial release and deployment

---

## Sprint 6 — MVP v3 (Assignment 6 Week 7) ✅ Completed

| Field | Value |
|---|---|
| **Milestone** | [Sprint 6 — MVP v3](https://github.com/Fedos113/SWP_TickFrame_28_team/milestone/7) |
| **Dates** | Week 7 (2026-07-14 – 2026-07-20) |
| **Goal** | Deliver final course version MVP v3 — follow-up maintenance, fixes from Week 6 trial, final transition, Demo Day preparation. |
| **Focus** | Customer trial feedback, final transition, MVP v3 release, Demo Day |
| **Release** | [v3.0.0](https://github.com/Fedos113/SWP_TickFrame_28_team/releases/tag/v3.0.0) — MVP v3 |

**Delivered PBIs:**
- [#201 PBI-130](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/201) — PostgreSQL infrastructure migration — SQLite to PostgreSQL 16 ✅
- [#202 PBI-131](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/202) — Pattern filtering and confidence threshold controls ✅
- [#216 PBI-132](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/216) — Fix UI glitches on timeframe switch ✅
- [#217 PBI-133](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/217) — Implement scan results export ✅
- [#225](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/225) — Sprint 6 maintenance and ML fixes ✅
- [#226](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/226) — Dual ML model integration (DT/DB + H&S) ✅
- [#227](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/227) — DT/DB integration documentation ✅

**Course Tasks & Documentation (delivered):**
- [#181](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/181) — Follow-up maintenance from Week 6 trial feedback ✅
- [#182](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/182) — Final transition and MVP v3 release ✅
- [#183](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/183) — Record public sanitized demo video for MVP v3 ✅
- [#184](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/184) — Sprint 5 and Sprint 6 reports ✅
- [#185](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/185) — Prepare presentation slides and rehearsal for Demo Day ✅
- [#218](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/218) — Course Task: Conduct Sprint 6 Review meeting ✅
- [#219](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/219) — Course Task: Conduct Sprint 6 Retrospective ✅
- [#220](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/220) — Course Task: Write Week 7 reflection and LLM report ✅
- [#221](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/221) — Course Task: Complete customer transition confirmation and update handover ✅
- [#222](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/222) — Course Task: Final documentation maintenance for Sprint 6 ✅

---

## Backlog — Unscheduled

| Issue | Story | Priority |
|---|---|---|
| [#006](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/6) | US-02 — Scan results in report-friendly format | Must Have |
| [#009](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/9) | US-09 — View chart for different time periods | Should Have |
| [#022](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/22) | US-08-1 — Customizable figure colors | Could Have |
