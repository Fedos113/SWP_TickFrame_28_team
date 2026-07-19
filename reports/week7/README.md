# Week 7 Public Report — Sprint 6 (Assignment 6)

**Project:** SWP TickFrame — cryptocurrency chart workstation with real-time Bybit market data, WebSocket streaming, Lightweight Charts v5 candlestick charts, modular drawing toolbar, 445+ technical indicators, ML pattern analysis (6 patterns), and PostgreSQL persistence.

**Team 28** · [GitHub Repository](https://github.com/Fedos113/SWP_TickFrame_28_team)

---

## 1. Week 6 Report

[reports/week6/README.md](../week6/README.md) — Sprint 5 trial release, customer feedback, transition-readiness status.

---

## 2. Product Backlog Board

[GitHub Projects — Tickframe Board](https://github.com/users/Fedos113/projects/1)

---

## 3. Sprint 6 Backlog

[Sprint 6 issues filtered view](https://github.com/Fedos113/SWP_TickFrame_28_team/issues?q=milestone%3A%22Sprint+6%22)

---

## 4. Sprint 6 Milestone

[Sprint 6 — MVP v3 Milestone](https://github.com/Fedos113/SWP_TickFrame_28_team/milestone/7)

---

## 5. Sprint 6 Overview

| Field | Value |
|---|---|
| **Sprint Goal** | Deliver final course version MVP v3 — follow-up maintenance, fixes from Week 6 trial, final transition, Demo Day preparation |
| **Sprint dates** | 2026-07-14 – 2026-07-20 |
| **Scope summary** | PostgreSQL migration (PBI-130), pattern filtering (PBI-131), ML DT/DB patterns, UI overhaul (coin search, market header, indicators fix), VM deployment, customer transition confirmation, final documentation |

---

## 6. Sprint 6 Size

**Total: 35 Story Points** (4 product PBIs + 8 course task PBIs)

- PBI-130 PostgreSQL migration: 5 SP
- PBI-131 Pattern filtering: 3 SP
- PBI-132 UI glitch fixes: 3 SP
- PBI-133 Scan results export: 2 SP
- Course tasks (#181–#185, #218–#222): 22 SP

---

## 7. Week 7 Follow-Up Maintenance and Final MVP v3 Changes

The following Sprint 6 work was delivered:

- **PostgreSQL migration (PBI-130):** SQLite replaced with PostgreSQL 16 container in Docker Compose. Database credentials via env vars. Schema initialisation via startup migrations. All data (candles, drawings, settings, indicators, ML patterns) persisted in PostgreSQL.
- **Pattern filtering (PBI-131):** Toggle checkboxes next to the patterns panel let users enable/disable pattern types. Filter state shared with chart renderer.
- **ML — Double Top / Double Bottom patterns:** Added DT/DB to existing H&S/InHS pipeline with backward-compatible API. 6 patterns operational.
- **UI overhaul:** Coin search bar in sidebar, market header (5m/1h/4h/24h change, market cap, supply), indicators now draggable without overlap.
- **Pre-computation architecture:** All coins pre-analysed on startup; "Analyze" retrieves from DB instantly.
- **Final VM deployment:** Updated deployment at university VM with all services (3 containers: ML, TickFrame, PostgreSQL).

---

## 8. Final Product Access

| Form | Link/Instructions |
|---|---|
| **Deployed VM** | http://10.93.26.164:8080/ |
| **Local via Docker** | `git clone` → `cp .env.example .env` → `docker compose up --build` |
| **Run instructions** | [README.md — Quick Start](https://github.com/Fedos113/SWP_TickFrame_28_team#docker-quick-start) |
| **Handover setup guide** | [docs/customer-handover.md — Setup and Deployment](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/docs/customer-handover.md#setup-and-deployment) |

---

## 9. Current Access / Run Instructions

[README.md](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/README.md)

---

## 10. README.md

[README.md](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/README.md)

---

## 11. CONTRIBUTING.md

[CONTRIBUTING.md](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/CONTRIBUTING.md)

---

## 12. AGENTS.md

[AGENTS.md](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/AGENTS.md)

---

## 13. Customer Handover

[docs/customer-handover.md](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/docs/customer-handover.md)

---

## 14. Hosted Documentation Site

[https://Fedos113.github.io/SWP_TickFrame_28_team/](https://Fedos113.github.io/SWP_TickFrame_28_team/)

---

## 15. Final Transition Outcome

| Status | Value |
|---|---|
| **Handover level reached** | `Ready for independent use` |
| **Customer-confirmation status** | `Accepted` |

The customer (Nikolay Kuzmin) confirmed during the Sprint 6 review (2026-07-17) that the product is ready for independent use and accepted the handover documentation. The customer explicitly stated the increment is approved as the final course delivery and no further changes are required before defense.

---

## 16. Transferred, Delegated, and Made Available Items

See [docs/customer-handover.md — Transition Scope](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/docs/customer-handover.md#transition-scope) for the full breakdown.

**Transferred:** Full source code (MIT), Docker Compose configuration, complete documentation set, changelog, contributor guidance, AI agent guidance.

**Delegated:** Docker-based deployment to customer infrastructure using provided Docker Compose setup.

**Made available:** Hosted documentation site, GitHub repository with issue/PR history, public demo video (see section 23).

---

## 17. Remaining Transition Blockers, Limitations, and Follow-Up Items

| Item | Status | Notes |
|---|---|---|
| Anomaly detection | Not delivered | Dropped due to insufficient research foundation and time constraints. Customer acknowledged complexity. |
| Multi-timeframe ML | Deferred | All 6 patterns only work on 5m timeframe. Annotated data for other intervals was unavailable. |
| Container architecture | MVP-accepted | Backend + frontend in same container is non-standard; accepted for course scope. |
| Concurrency | Not stress-tested | No locking for simultaneous "Analyze" clicks. Sub-second analysis makes risk low. |
| DT/DB precision | Low (17-18%) | Recall ~80%; post-course pipeline improvements planned by ML engineer. |
| Container dependencies | Noted | NPM must be pre-installed in TickFrame container; documented in setup. |

---

## 18. Customer Independent Use and Deployment Evidence

The customer:
- Attended the Sprint 5 review (2026-07-10) and reviewed progress, architecture, and configuration
- Attended the Sprint 6 review / final handover (2026-07-17) and confirmed acceptance
- Requested deployment of the final version to the VM, which was completed on 2026-07-17
- Expressed openness to future collaboration and post-course open-source contributions

The product was not independently deployed on the customer's own infrastructure — the university VM deployment was used throughout. This is consistent with the `Ready for independent use` handover level.

---

## 19. Customer Feedback Response Table (Sprint 6)

| Week 6 Feedback | Sprint 6 Action | Status |
|---|---|---|
| Migrate SQLite → PostgreSQL 17 container | PostgreSQL 16 container added to Docker Compose with env-var config | ✅ Done |
| Database credentials via env vars | DB_HOST, DB_PORT, DB_PASSWORD etc. configured in `.env` | ✅ Done |
| Database migrations instead of app-created tables | Startup migrations initialise schema | ✅ Done |
| Complete remaining 2 ML patterns (6 total) | DT/DB added; 6 patterns operational | ✅ Done |
| Pattern-type filtering + confidence threshold | Toggle checkboxes next to patterns panel | ✅ Done |
| Additional coin metrics (5m/1h/4h change, market cap) | Market header with CoinGecko-powered metrics | ✅ Done |
| Fix UI glitches on timeframe switch | Indicators fixed, draggable without overlap | ✅ Done |
| Deploy updated version to VM | Final version deployed 2026-07-17 | ✅ Done |

---

## 20. Week 7 UAT Results

UAT scenarios were executed during the Sprint 6 review (2026-07-17):

| Scenario | Result | Notes |
|---|---|---|
| UAT-001: Scan and view chart patterns | ✅ Pass | 6/6 patterns working; pre-analysed in DB, instant retrieval |
| UAT-002: Toggle chart timeframes | ⏳ Partial | Switching works; ML limited to 5m timeframe |
| UAT-003: Filter patterns by type | ✅ Pass | Toggle filter next to patterns panel |
| UAT-004: Real-time price sidebar | ✅ Pass | WebSocket live prices |
| UAT-005: Theme toggle | ✅ Pass | Unchanged, still passing |
| UAT-006: WebSocket real-time candles | ✅ Pass | Live updates from Bybit, DB cache fallback |
| UAT-007: Indicator sub-charts | ✅ Pass | Indicators now movable without overlap |
| UAT-008: Configure pattern analysis range | ✅ Pass | Slider with configurable range |
| UAT-009: Sidebar coin search and addition | ✅ Pass | Infinite coin addition with search |
| UAT-010: Coin metrics header | ✅ Pass | 5m/1h/4h change, market cap, supply from CoinGecko |

Full details: [docs/user-acceptance-tests.md](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/docs/user-acceptance-tests.md)

---

## 21. Final SemVer Release — MVP v3

[v3.0.0 — MVP v3 (Sprint 6 Final Release)](https://github.com/Fedos113/SWP_TickFrame_28_team/releases/tag/v3.0.0)

---

## 22. Changelog

[CHANGELOG.md](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/CHANGELOG.md)

---

## 23. Public Sanitized Demo Video

[Public sanitized demo video — MVP v3](https://drive.google.com/file/d/1Otmlahg1sAH8jTMJmSWi85pBt8RAX6lz/view?usp=sharing)

---

## 24. Demo Day Preparation Summary

- Slide deck prepared and refined for Week 7 lab rehearsal
- Week 7 lab rehearsal completed (2026-07-17): 5-min presentation + 3-min Q&A
- Each team member assigned slides to present
- Pre-recorded demo segment prepared for Week 8 Demo Day (under 2 minutes)
- Full presentation timing rehearsed to fit 7-min Demo Day limit

---

## 25. Sprint Review — Summary, Transcript, and Notes

| Artifact | Link |
|---|---|
| Sprint Review summary | [reports/week7/sprint-review-summary.md](sprint-review-summary.md) |
| Sprint Review transcript | [reports/week7/sprint-review-transcript.md](sprint-review-transcript.md) (published — recording/publication permitted) |
| Sprint Review notes | [reports/week7/sprint-review-notes.md](sprint-review-notes.md) |

**Recording and Publication Permissions:**
- Recording was permitted
- Public transcript publication was permitted
- The transcript is published in this repository

---

## 26. Reflection

[reports/week7/reflection.md](reflection.md)

---

## 27. Retrospective

[reports/week7/retrospective.md](retrospective.md)

---

## 28. LLM Report

[reports/week7/llm-report.md](llm-report.md)

---

## 29. Final Product Status

**MVP v3** (v3.0.0) is the final course version of SWP TickFrame. All planned PBIs for Sprint 6 have been delivered:

- PostgreSQL persistence with Docker Compose (3 containers)
- 6 ML patterns with pre-computation architecture (instant "Analyze")
- Pattern filtering by type
- UI overhaul: coin search, market header, draggable indicators
- VM deployment with latest version
- Complete documentation set maintained
- Customer handover accepted (`Ready for independent use` / `Accepted`)

**Known limitations:** Anomaly detection not delivered; ML only on 5m timeframe; DT/DB precision needs improvement; container architecture couples backend and frontend; concurrency not stress-tested.

---

## 30. Contribution Traceability

| Person | Role | Issues | PRs | Reviews | Testing | QA | Docs | Transition / Deployment | Demo Prep |
|---|---|---|---|---|---|---|---|---|---|
| F. Kozhevnikov ([Fedos113](https://github.com/Fedos113)) | Product Owner / Full-Stack | [#201](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/201), [#202](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/202), [#216](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/216), [#217](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/217), [#225](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/225) | [#228](https://github.com/Fedos113/SWP_TickFrame_28_team/pull/228), [#229](https://github.com/Fedos113/SWP_TickFrame_28_team/pull/229), [#231](https://github.com/Fedos113/SWP_TickFrame_28_team/pull/231) | [#230 ✅](https://github.com/Fedos113/SWP_TickFrame_28_team/pull/230) | Manual smoke tests | Automated checks passed | Sprint 6 docs, handover update | VM deployment | Slides, rehearsal |
| A. Gafarov ([omarichev](https://github.com/omarichev)) | Developer / Documentation | — | — | — | — | — | Week 6/7 reports, UAT update | — | Slide review |
| A. Mindubaev ([pug228](https://github.com/pug228)) | Developer / Quality & CI | [#203](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/203), [#204](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/204) | [#205](https://github.com/Fedos113/SWP_TickFrame_28_team/pull/205) | [#231 ✅](https://github.com/Fedos113/SWP_TickFrame_28_team/pull/231) | frontend-lint fix | Automated checks passed | CI/docs maintenance | — | — |
| D. Zhechev ([DaniilJechev](https://github.com/DaniilJechev)) | Scrum Master / ML Engineer | [#226](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/226), [#227](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/227) | [#230](https://github.com/Fedos113/SWP_TickFrame_28_team/pull/230) | [#228 ✅](https://github.com/Fedos113/SWP_TickFrame_28_team/pull/228), [#229 ✅](https://github.com/Fedos113/SWP_TickFrame_28_team/pull/229) | ML integration tests | — | DT/DB integration docs | — | ML segment slides |
| M. Bezborodov ([MikhailBezborodov024](https://github.com/MikhailBezborodov024)) | Developer / Frontend | — | — | — | Frontend testing | — | — | — | Frontend demo segment |

---

## 31. Screenshots

Screenshots evidence for inspectable Week 7 artifacts:

### Sprint 6 Milestone
![Sprint 6 milestone](images/sprint-6-milestone.png)
*Sprint 6 milestone with goal, dates, and issue list*

### MVP v3 Release (v3.0.0)
![MVP v3 release](images/mvp-v3-release.png)
*v3.0.0 MVP v3 Final Release on GitHub*

### Final Product Access — VM Deployment
![Final product access](images/final-product-access.png)
*SWP TickFrame running on university VM at http://10.93.26.164:8080/*

### Example Reviewed PR — Dual ML Model Integration
![Example reviewed PR](images/example-pr-week7.png)
*PR #230 — Dual ML model integration with reviewed approval*
