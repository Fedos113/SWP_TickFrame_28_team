# Week 7 Public Report — Sprint 6 / MVP v3 (Assignment 7)

**Project:** SWP TickFrame — cryptocurrency chart workstation with real-time Bybit market data, WebSocket streaming, Lightweight Charts v5 candlestick charts, modular drawing toolbar, 445+ technical indicators, and ML pattern analysis (6 patterns).

**Team 28** · [GitHub Repository](https://github.com/Fedos113/SWP_TickFrame_28_team)

---

## 1. Links to Previous Week and Backlog

| Artifact | Link |
|---|---|
| Week 6 report | [reports/week6/README.md](../week6/README.md) |
| Product Backlog board | [GitHub Projects — Tickframe Board](https://github.com/users/Fedos113/projects/1) |
| Sprint 6 Backlog board | [Sprint 6 filtered view](https://github.com/Fedos113/SWP_TickFrame_28_team/issues?q=milestone%3A%22Sprint+6+%E2%80%94+MVP+v3%22) |
| Sprint 6 milestone | [Sprint 6 — MVP v3](https://github.com/Fedos113/SWP_TickFrame_28_team/milestone/7) |

---

## 2. Sprint 6 Overview

| Field | Value |
|---|---|
| **Sprint Goal** | Deliver MVP v3 — follow-up maintenance, fixes from Week 6 trial, final transition, Demo Day preparation |
| **Sprint dates** | 2026-07-14 – 2026-07-20 |
| **Total Story Points** | **18 SP** (estimated across 4 product PBIs + 5 course-task issues) |
| **Completed PBIs** | PBI-130 PostgreSQL migration (#201), PBI-131 Pattern filtering (#202), PBI-132 UI glitch fixes (#216), PBI-133 Scan results export (#217), PBI-134 DT/DB dual-model ML detection (#226) |

---

## 3. Week 7 Follow-Up Maintenance and MVP v3 Changes

The following changes were delivered in Sprint 6 as follow-up to the Week 6 trial release and customer feedback:

- **PostgreSQL migration** (PBI-130) — SQLite replaced with PostgreSQL 16 as a dedicated Docker Compose container. Startup migrations initialize the schema. Database credentials via environment variables.
- **Pattern filtering** (PBI-131) — Toggle switches next to the patterns panel let users enable/disable specific pattern types (HS, InHS, DT, DB, Flags, Wedge).
- **UI overhaul** — Sidebar with coin search allows unlimited coin addition. Indicators are now draggable without overlap. Coin metrics (5m/1h/4h change, market cap, supply) from CoinGecko + candle calculations. Market header with multi-timeframe change readouts.
- **DT/DB dual-model ML detection** (PBI-134) — Double Top and Double Bottom XGBoost detectors added alongside existing H&S pipeline. Backward-compatible API. Numba-accelerated extrema selection.
- **Pre-computation architecture** — All coins analysed by ML before project initialisation. "Analyze" retrieves pre-calculated results from PostgreSQL. First-time startup ≈3–4 min; subsequent startups instant.
- **Pattern filter fix** — Shared `_patternFilter` state between toolbar and renderer so checkboxes actually filter chart markers.
- **Confidence threshold calibration** — DT/DB thresholds calibrated to actual model output (previously required 0.75/0.80, now matches model distribution).
- **Lightweight Charts local serving** — CDN reference replaced with local npm bundle to support isolated Docker environments.
- **CoinGecko cold-boot fix** — Default coin icons hardcoded; external API called in background only.
- **Single-chart architecture** — Per-coin stacked chart instances replaced with single shared instance for stability.
- **Unified "Matrix" design system** — Black + phosphor-green dark theme, white + muted-green light theme. Themed chart panes, indicators panel, drawing toolbar.

---

## 4. Product Access

| Form | Link/Instructions |
|---|---|
| **Deployed VM** | http://10.93.26.164:8080/ (university VM, deployed 2026-07-17 evening) |
| **Local via Docker** | `git clone` → `cp .env.example .env` → `docker compose up --build` |
| **Run instructions** | [README.md — Quick Start](https://github.com/Fedos113/SWP_TickFrame_28_team#docker-quick-start) |
| **Handover setup guide** | [docs/customer-handover.md — Setup and Deployment](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/docs/customer-handover.md#setup-and-deployment) |

---

## 5. Maintained Documentation Links

| Document | Link |
|---|---|
| README | [README.md](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/README.md) |
| Contributing Guide | [CONTRIBUTING.md](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/CONTRIBUTING.md) |
| AI Agent Guidance | [AGENTS.md](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/AGENTS.md) |
| Customer Handover | [docs/customer-handover.md](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/docs/customer-handover.md) |
| Hosted Documentation Site | https://Fedos113.github.io/SWP_TickFrame_28_team/ |
| Product Backlog | [docs/backlog.md](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/docs/backlog.md) |
| Roadmap | [docs/roadmap.md](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/docs/roadmap.md) |
| Quality Requirements | [docs/quality-requirements.md](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/docs/quality-requirements.md) |
| Quality Requirement Tests | [docs/quality-requirement-tests.md](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/docs/quality-requirement-tests.md) |
| Testing Strategy | [docs/testing.md](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/docs/testing.md) |
| Architecture Docs | [docs/architecture/README.md](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/docs/architecture/README.md) |
| Development Process | [docs/development-process.md](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/docs/development-process.md) |
| User Acceptance Tests | [docs/user-acceptance-tests.md](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/docs/user-acceptance-tests.md) |
| User Stories | [docs/user-stories.md](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/docs/user-stories.md) |
| Definition of Done | [docs/definition-of-done.md](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/docs/definition-of-done.md) |
| Changelog | [CHANGELOG.md](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/CHANGELOG.md) |

---

## 6. Final Transition Outcome

### Handover Level Reached

`Ready for independent use`

### Customer-Confirmation Status

`Accepted`

**Details:** The customer (Nikolay Kuzmin) reviewed and accepted the final increment during the Sprint 6 review on 2026-07-17. The increment was approved as the final course delivery with no further changes required before defence. The customer confirmed the Sprint 6 outcome was satisfactory and expressed openness to future collaboration and open-source contributions.

### What Was Transferred / Made Available

- Full source code under MIT license in the public repository
- Docker Compose deployment (3 containers: TickFrame, ML Service, PostgreSQL 16)
- Hosted documentation site at GitHub Pages
- Maintained customer handover documentation (`docs/customer-handover.md`)
- Contributing guide (`CONTRIBUTING.md`) and AI agent guidance (`AGENTS.md`)
- Complete architecture documentation with static, dynamic, and deployment views plus ADRs
- Full testing documentation, quality requirements, UAT scenarios, user stories, backlog, roadmap
- Final version deployed to university VM at http://10.93.26.164:8080/

### Remaining Blocker / Limitations

1. **Anomaly detection not delivered** — Dropped due to lack of public research and labelled data. Customer acknowledged the complexity.
2. **Single-timeframe ML (5m only)** — All 6 patterns only work on 5m candles. Multi-timeframe deferred — accepted trade-off.
3. **DT/DB precision 17–18%** — Recall ≈80% but high false-positive rate. Post-course pipeline improvement planned.
4. **Container coupling** — Frontend + backend in single container. Accepted for MVP but non-standard for production.
5. **Concurrency not stress-tested** — No locking for simultaneous "Analyze" clicks. Low risk given sub-second analysis time.
6. **NPM dependency in container** — Requires manual install, not pre-bundled in the Docker image.

### Customer Use / Deployment Evidence

The customer viewed a live demonstration of the final version during the Sprint 6 review on 2026-07-17. The fully completed version was deployed to the university VM the same evening for independent customer testing. The customer confirmed they would "run and check it" after deployment. No evidence of independent customer operation was obtained within the course period (deployment occurred at end of final review).

---

## 7. Customer Feedback Response Table — Sprint 6

| Feedback Point (from Week 6) | Source | Resulting PBI/Issue | Status |
|---|---|---|---|
| Migrate SQLite → PostgreSQL 17 with dedicated container | Sprint 5 architecture review | [#201 PBI-130](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/201) — PostgreSQL infrastructure migration | ✅ Done |
| Add database credentials to env vars (DB_USER, DB_PASSWORD, DB_NAME) | Sprint 5 architecture review | Part of PBI-130 | ✅ Done |
| Implement database migrations instead of app-created tables | Sprint 5 architecture review | Part of PBI-130 | ✅ Done |
| Add pattern-type filtering and confidence threshold controls | Sprint 4 UAT + Sprint 5 confirmation | [#202 PBI-131](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/202) — Pattern filtering | ✅ Done |
| Complete remaining 2 ML patterns (6 total) | Sprint 5 review | [#226 PBI-134](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/226) — DT/DB dual-model | ✅ Done |
| Update VM deployment with latest version | Sprint 5 review | Deployed 2026-07-17 evening | ✅ Done |
| Additional coin metrics (5m/1h/4h change, market cap, supply) | Sprint 4 UAT | Implemented via CoinGecko + candle calcs | ✅ Done |
| Fix UI glitches (chart switching, element movement) | Sprint 4 UAT | [#216 PBI-132](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/216) | ✅ Done |
| Scan results export | Sprint 4 UAT | [#217 PBI-133](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/217) | ✅ Done |

---

## 8. UAT Results Summary

Results from the Sprint 6 review (2026-07-17):

| Scenario | Result | Notes |
|---|---|---|
| UAT-001: Scan and view chart patterns | ✅ Pass | 6/6 patterns working; pre-analysed in DB, instant retrieval |
| UAT-002: Toggle chart timeframes | ⏳ Partial | Switching works; ML limited to 5m timeframe |
| UAT-003: Filter patterns by type | ✅ Pass | Toggle filter next to patterns panel |
| UAT-004: Real-time price sidebar | ✅ Pass | WebSocket live prices continue working |
| UAT-005: Theme toggle | ✅ Pass | Unchanged, still passing |
| UAT-006: WebSocket real-time candles | ✅ Pass | Live updates from Bybit, DB cache fallback |
| UAT-007: Indicator sub-charts | ✅ Pass | Indicators now movable without overlap |
| UAT-008: Configure pattern analysis range | ✅ Pass | Slider with configurable range |
| UAT-009: Sidebar coin search and addition | ✅ Pass | Infinite coin addition with search |
| UAT-010: Coin metrics (5m/1h/4h change, market cap, supply) | ✅ Pass | Displayed from CoinGecko + candle calculations |

Full details: [docs/user-acceptance-tests.md](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/docs/user-acceptance-tests.md)

---

## 9. Release and Changelog

| Artifact | Link |
|---|---|
| MVP v3 SemVer release | [v3.0.0](https://github.com/Fedos113/SWP_TickFrame_28_team/releases/tag/v3.0.0) |
| Changelog | [CHANGELOG.md](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/CHANGELOG.md) |
| Public sanitized demo video | [Demo](https://drive.google.com/file/d/1Otmlahg1sAH8jTMJmSWi85pBt8RAX6lz/view?usp=sharing) |

---

## 10. Demo Day Preparation Summary

- **Slide deck:** Refined based on Week 7 lab rehearsal feedback. Submitted as PDF alongside Week 7 Moodle PDF.
- **Presentation structure (7 min):** Project context and target users → Final product and key requirements → Pre-recorded demo (<2 min) → Customer usefulness and deployment status → Engineering, process, and quality evidence → Remaining limitations and handover status → Team contribution and reflection → Links to deployed product and repository.
- **Pre-recorded demo:** Under 2 minutes, covering final MVP v3 state including improvements added in Sprint 6.
- **Team attendance:** All 5 team members attending Demo Day.
- **Team presentation:** Each member presents at least one slide.
- **Q&A (7 min):** Person who worked on relevant part answers where possible.

---

## 11. Sprint Review Evidence

| Artifact | Link |
|---|---|
| Sprint Review summary | [reports/week7/sprint-review-summary.md](sprint-review-summary.md) |
| Sprint Review transcript | [reports/week7/sprint-review-transcript.md](sprint-review-transcript.md) |
| Sprint Review notes | [reports/week7/sprint-review-notes.md](sprint-review-notes.md) |
| Sprint Retrospective | [reports/week7/retrospective.md](retrospective.md) |
| Reflection | [reports/week7/reflection.md](reflection.md) |
| LLM Report | [reports/week7/llm-report.md](llm-report.md) |

**Recording and Publication Permissions:** Recording was permitted. Public transcript publication was permitted. The transcript is published in this repository.

---

## 12. Final Product Status

MVP v3 is the final course version delivered at the end of Sprint 6. The application is a fully functional cryptocurrency chart workstation with:

- **Real-time data:** WebSocket live candles and prices from Bybit (primary) and Binance (fallback)
- **Charting:** Lightweight Charts v5 with candlestick charts, 5 timeframes (5m, 15m, 1h, 4h, 1d)
- **Indicators:** 445+ technical indicators via `lightweight-charts-indicators` library
- **Drawing tools:** 13 drawing tools via `lightweight-charts-drawing` library
- **ML pattern detection:** 6 patterns (HS, InHS, DT, DB, Flags, Wedge) via XGBoost microservice
- **Database:** PostgreSQL 16 persistence with startup migrations
- **Deployment:** Docker Compose with 3 containers (TickFrame, ML Service, PostgreSQL)
- **UI:** Unified Matrix design system, coin search sidebar, market header with metrics, pattern filtering

**What was not delivered:** Anomaly detection (dropped due to infeasibility within scope), multi-timeframe ML (all patterns on 5m only), concurrency stress-testing.

---

## 13. Contribution Traceability

| Person | Role | Issues | PRs | Reviews | Testing | QA | Docs | Transition / Deployment | Demo Prep |
|---|---|---|---|---|---|---|---|---|---|
| F. Kozhevnikov ([Fedos113](https://github.com/Fedos113)) | Product Owner / Full-Stack | #201, #202, #216, #217 | PBI-130, PBI-131, PBI-132, PBI-133 PRs | Sprint 6 PRs | — | All CI passes | Architecture updates, README, CHANGELOG | VM deployment (2026-07-17) | Slide deck, demo |
| A. Gafarov ([omarichev](https://github.com/omarichev)) | Developer / Documentation | #218–#222, #236–#238 | `sprint-review-docs` branch | — | — | — | Week 7 reports (7 files), A7 scaffolding, customer-handover, DATABASE.md, architecture docs, Docker/config updates | — | — |
| A. Mindubaev ([pug228](https://github.com/pug228)) | Developer / Quality & CI | QRT maintenance | CI updates | Sprint 6 PRs | QRT execution | Automated checks | Testing docs, QRT updates | — | — |
| D. Zhechev ([DaniilJechev](https://github.com/DaniilJechev)) | Scrum Master / ML Engineer | #226, #227 | DT/DB Numba optimization | ML PRs | ML inference verification | — | DT/DB architecture report, ML docs | — | ML section slides |
| M. Bezborodov ([MikhailBezborodov024](https://github.com/MikhailBezborodov024)) | Developer / Frontend | UI polish issues | Frontend PRs | Frontend PRs | UI smoke tests | — | Frontend docs | — | Frontend demo |

---

## 14. Screenshots

Screenshots evidence for inspectable Week 7 artifacts:

### Sprint 6 Milestone
![Sprint 6 milestone](images/sprint-6-milestone.png)

### MVP v3 Release (v3.0.0)
![MVP v3 release](images/mvp-v3-release.png)

### Example Reviewed PR
![Example reviewed PR](images/example-pr.png)

### Product Access — Deployed VM
![Deployed VM](images/deployed-vm.png)
