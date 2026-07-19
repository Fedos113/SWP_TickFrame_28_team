# Week 6 Public Report — Sprint 5 (Assignment 6)

**Project:** SWP TickFrame — cryptocurrency chart workstation with real-time Bybit market data, WebSocket streaming, Lightweight Charts v5 candlestick charts, modular drawing toolbar, technical indicator library (445+ indicators), and ML pattern analysis.

**Team 28** · [GitHub Repository](https://github.com/Fedos113/SWP_TickFrame_28_team)

---

## 1. Product Backlog and Sprint 5 Backlog

| Artifact | Link |
|---|---|
| Product Backlog board | [GitHub Projects — Tickframe Board](https://github.com/users/Fedos113/projects/1) |
| Sprint 5 milestone | [Sprint 5 — Week 6 Trial Release](https://github.com/Fedos113/SWP_TickFrame_28_team/milestone/6) |
| Sprint 5 issues | [Sprint 5 filtered view](https://github.com/Fedos113/SWP_TickFrame_28_team/issues?q=milestone%3A%22Sprint+5%22) |

---

## 2. Sprint 5 Overview

| Field | Value |
|---|---|
| **Sprint Goal** | Produce stable trial/handover-candidate release — RSI implementation, customer-facing documentation, handover prep, customer trial |
| **Sprint dates** | 2026-07-07 – 2026-07-13 |
| **Total Story Points** | **10 SP** (3 delivered product PBIs: #112 PBI-117 RSI sub-chart [closed, superseded], #198 PBI-118 indicators subsystem [5 SP], #199 drawing refinements [2 SP]; plus documentation and course-task items) |
| **Completed PBIs (closed)** | #112 PBI-117 (superseded by #198), #186–#190, #193 |
| **Open PBIs (in progress)** | #177 PBI-129 (docs review), #178 (CONTRIBUTING/AGENTS), #179 (customer-handover), #180 (trial deployment), #194 (audit gap fixes), #198 PBI-118 (indicators), #199 (drawing refinements) |

---

## 3. Week 6 Trial Release Changes

The [v2.2.0 Sprint 5 trial release](https://github.com/Fedos113/SWP_TickFrame_28_team/releases/tag/v2.2.0) includes the following changes:

- **445+ technical indicators subsystem** — Integrated `lightweight-charts-indicators` library with searchable panel UI, grouped by category. RSI auto-applied on symbol switch.
- **Drawing toolbar refinements** — 3-column grid layout, smaller icons, z-order fixes for indicator overlay compatibility, adaptive price label precision, human-readable timestamps.
- **WebSocket race condition fix** — Stale candle messages no longer apply after switching trading pairs.
- **ML training pipeline** — XGBoost-based pattern detection with 4 trained models (Head & Shoulders, Double Top, Double Bottom, Flags). Inference time <0.5s per 1k candles.
- **Customer-handover documentation** — New `docs/customer-handover.md` with Transition Scope, env-var documentation, setup/deployment, known limitations.
- **Contributor and agent guidance** — `CONTRIBUTING.md` and `AGENTS.md` created.
- **Customer-facing documentation polish** — SVG architecture diagram, troubleshooting section, UI screenshot, relative link cleanup.
- **Assignment 6 scaffolding** — Context file, task breakdown, Sprint 5/6 planning, contribution tracking.

---

## 4. Product Access

| Form | Link/Instructions |
|---|---|
| **Deployed VM** | http://10.93.26.164:8080/ (university VM, may be unavailable when powered off) |
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

## 6. Customer-Facing Documentation Review Summary

The Sprint 5 review (2026-07-10) included an **architecture and configuration review** of the customer-facing documentation. The customer inspected:

- `.env.example` — Found DB_HOST/DB_PORT variables marked as "future" but missing DB_USER, DB_PASSWORD, DB_NAME. Customer requested PostgreSQL configuration with full credentials.
- `docker-compose.yml` — Found only tickframe + ml-service containers; no database container. Customer requested PostgreSQL 17 container added.
- `docs/customer-handover.md` — Not formally reviewed by the customer during this session.

**What was clear:** Project progress, indicator library approach, ML pattern detection limitations (5m timeframe only).
**What was unclear:** Why SQLite was used instead of PostgreSQL despite earlier architecture agreement.
**What was missing:** Database container, migration framework, full database env-var configuration, updated deployment with all services.

**Note:** The formal customer-facing documentation review (covering README.md, customer-handover.md, troubleshooting, known limitations as per A6 Part 3) has not yet taken place. This is scheduled for the Part 5 transition-readiness meeting in Sprint 6.

---

## 7. Transition-Readiness Summary

**Current handover level:** `Ready for independent use` (pending confirmation)

**What is ready for transition:**
- Full source code under MIT license
- Docker Compose (backend + ML service)
- Maintained customer-handover documentation
- CONTRIBUTING.md and AGENTS.md
- Hosted documentation site
- 4 ML patterns delivered
- 445+ technical indicators

**What blocks transition (must happen in Week 7):**
1. **PostgreSQL migration** (PBI-130) — SQLite → PostgreSQL 17 container with env-var credentials
2. **Pattern filtering** (PBI-131) — Type and confidence threshold controls
3. **Remaining 2 ML patterns** — Complete 6 total patterns
4. **Updated deployment** — Deploy latest version to VM with all services
5. **Part 5 transition-readiness meeting** — Formal session with customer to confirm handover
6. **Customer documentation review** — Ask customer to review full documentation set
7. **Customer-confirmation of handover** — Record acceptance status

---

## 8. Customer Feedback Response Table

| Feedback Point | Source | Resulting PBI/Issue | Status |
|---|---|---|---|
| Migrate SQLite → PostgreSQL 17 with dedicated container | Sprint 5 architecture review | [#201 PBI-130](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/201) — PostgreSQL infrastructure migration | Sprint 6 |
| Add database credentials to env vars (DB_USER, DB_PASSWORD, DB_NAME) | Sprint 5 architecture review | Part of PBI-130 | Sprint 6 |
| Implement database migrations instead of application-created tables | Sprint 5 architecture review | Part of PBI-130 | Sprint 6 |
| Add pattern-type filtering and confidence threshold controls | Sprint 4 UAT + Sprint 5 confirmation | [#202 PBI-131](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/202) — Pattern filtering and confidence threshold | Sprint 6 |
| Complete remaining 2 ML patterns (6 total) | Sprint 5 review | Suggested PBI-132 (not yet created) | Sprint 6 |
| Update VM deployment with latest version | Sprint 5 review | Part of [#180](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/180) — Week 6 trial release and deployment | Sprint 6 |
| Clear handover documentation with deployment prerequisites | Sprint 5 review | [#179](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/179) — docs/customer-handover.md | Sprint 6 |

## 9. Feedback Not Yet Addressed

- **Remaining 2 ML patterns** — No PBI created yet; suggested as PBI-132
- **Formal Part 5 transition-readiness session** — Not yet conducted; planned for Sprint 6
- **Independent customer trial** — Customer has not independently tried the trial release
- **Customer documentation review** — Customer has not reviewed the full documentation set
- **VM deployment update** — Pending PostgreSQL migration completion

---

## 10. UAT Results Summary

UAT scenarios were discussed during the Sprint 5 review. Results from the sprint-review-summary:

| Scenario | Result | Notes |
|---|---|---|
| UAT-001: Scan and view chart patterns | ⏳ Partial | 4/6 patterns working; filtering requested |
| UAT-002: Toggle chart timeframes | ⏳ Partial | 5 timeframes work; ML only on 5m |
| UAT-003: Export scan results | ⏳ Not demonstrated | — |
| UAT-004: Real-time price sidebar | ✅ Pass | WebSocket live prices |
| UAT-005: Theme toggle | ✅ Pass | Still passing |
| UAT-006: WebSocket real-time candles | ✅ Pass | Live updates from Bybit/Binance |
| UAT-007: Volume indicator sub-chart | ✅ Pass | Working with colored bars |
| UAT-008: Configure pattern analysis range | ✅ Pass | Configurable slider |
| UAT-009: Sidebar resize and UI cleanliness | ⏳ Not demonstrated | — |

Full details: [docs/user-acceptance-tests.md](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/docs/user-acceptance-tests.md)

---

## 11. Release and Changelog

| Artifact | Link |
|---|---|
| Week 6 SemVer trial release | [v2.2.0 — Sprint 5 Week 6 Trial Release](https://github.com/Fedos113/SWP_TickFrame_28_team/releases/tag/v2.2.0) |
| Changelog | [CHANGELOG.md](https://github.com/Fedos113/SWP_TickFrame_28_team/blob/main/CHANGELOG.md) |

---

## 12. Sprint Review Evidence

| Artifact | Link |
|---|---|
| Sprint Review transcript | [reports/week6/sprint-review-transcript.md](sprint-review-transcript.md) (published — recording/publication permitted) |
| Sprint Review summary | [reports/week6/sprint-review-summary.md](sprint-review-summary.md) |
| Sprint Retrospective | [reports/week6/retrospective.md](retrospective.md) |
| Reflection | [reports/week6/reflection.md](reflection.md) |
| LLM Report | [reports/week6/llm-report.md](llm-report.md) |

**Recording and Publication Permissions:**
- Recording was permitted
- Public transcript publication was permitted
- The transcript is published in this repository

---

## 13. Current Product Status and Expected Week 7 Follow-Up

**Current status:** The Sprint 5 trial release (v2.2.0) is deployed and functional. Key features delivered: 445+ indicators, 4 ML patterns, drawing toolbar refinements, WebSocket stability fixes, handover documentation.

**Expected Week 7 (Sprint 6) work:**
1. PostgreSQL migration (PBI-130) — SQLite → PostgreSQL 17 container, env-var credentials, migrations
2. Pattern filtering (PBI-131) — Type and confidence threshold UI controls
3. Complete remaining 2 ML patterns
4. Update VM deployment with all services
5. Conduct Part 5 transition-readiness meeting
6. Finalize customer-handover documentation
7. Record public sanitized demo video
8. Prepare and rehearse Demo Day presentation
9. Release MVP v3

---

## 14. Contribution Traceability

| Person | Role | Issues | PRs | Reviews | Testing | QA | Docs | Transition / Deployment | Demo Prep |
|---|---|---|---|---|---|---|---|---|---|
| F. Kozhevnikov ([Fedos113](https://github.com/Fedos113)) | Product Owner / Full-Stack | [#112](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/112) (closed), [#186](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/186), [#187](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/187), [#188](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/188), [#189](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/189), [#190](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/190), [#198](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/198), [#199](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/199) | [#191](https://github.com/Fedos113/SWP_TickFrame_28_team/pull/191), [#200](https://github.com/Fedos113/SWP_TickFrame_28_team/pull/200) | [#205 ✅](https://github.com/Fedos113/SWP_TickFrame_28_team/pull/205), [#211 ✅](https://github.com/Fedos113/SWP_TickFrame_28_team/pull/211) | Manual smoke tests | Automated checks passed | A6 scaffolding, repo templates, doc port fixes | — | — |
| A. Gafarov ([omarichev](https://github.com/omarichev)) | Developer / Documentation | [#212](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/212) | [#213](https://github.com/Fedos113/SWP_TickFrame_28_team/pull/213) | [#210 ✅](https://github.com/Fedos113/SWP_TickFrame_28_team/pull/210) | — | — | — | — | — |
| A. Mindubaev ([pug228](https://github.com/pug228)) | Developer / Quality & CI | [#203](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/203), [#204](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/204) | [#205](https://github.com/Fedos113/SWP_TickFrame_28_team/pull/205) | [#191 ✅](https://github.com/Fedos113/SWP_TickFrame_28_team/pull/191) | frontend-lint fix | Automated checks passed | Sprint 5 reports, CHANGELOG, README, arch docs, backlog, customer-handover | — | — |
| D. Zhechev ([DaniilJechev](https://github.com/DaniilJechev)) | Scrum Master / ML Engineer | [#208](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/208) | [#211](https://github.com/Fedos113/SWP_TickFrame_28_team/pull/211) | [#200 ✅](https://github.com/Fedos113/SWP_TickFrame_28_team/pull/200) | — | — | context.md ML update | — | — |
| M. Bezborodov ([MikhailBezborodov024](https://github.com/MikhailBezborodov024)) | Developer / Frontend | [#209](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/209) | [#210](https://github.com/Fedos113/SWP_TickFrame_28_team/pull/210) | [#213 ✅](https://github.com/Fedos113/SWP_TickFrame_28_team/pull/213) | — | — | A6 Moodle PDF template | — | — |

---

## 15. Screenshots

Screenshots evidence for inspectable Week 6 artifacts:

### Sprint 5 Milestone
![Sprint 5 milestone](images/sprint-5-milestone.png)
*Sprint 5 milestone with goal, dates, and issue list*

### Week 6 Trial Release (v2.2.0)
![Week 6 release](images/week6-release.png)
*v2.2.0 Sprint 5 Week 6 Trial Release on GitHub*

### Example Reviewed PR — Indicators Subsystem
![Example reviewed PR](images/example-pr.png)
*PR #200 — 445+ indicators subsystem, drawing fixes, and WS race condition fix*
