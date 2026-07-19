# Memory7 — SWP TickFrame Team 28 · Week 7 Context File

> **Purpose:** Comprehensive AI-assistant memory file for Week 7 (Sprint 6 / Assignment 7). Contains all project context, current status, remaining gaps, and links to every relevant artifact. Update this file as Sprint 6 work progresses.

---

## 1. Project Identity

| Field | Value |
|---|---|
| **Project Name** | SWP TickFrame |
| **Team** | 28 |
| **Repository** | https://github.com/Fedos113/SWP_TickFrame_28_team |
| **License** | MIT |
| **Description** | FastAPI-based cryptocurrency chart workstation with real-time Bybit market data, live WebSocket streaming, Lightweight Charts v5 candlestick charts, modular drawing toolbar, Fear & Greed Index, coin icons, PostgreSQL database, and ML pattern analysis (6 patterns). |
| **Default Branch** | `main` (protected) |
| **MVP v1** | [v1.0.0](https://github.com/Fedos113/SWP_TickFrame_28_team/releases/tag/SemVer) (Sprint 2) |
| **Sprint 3** | [v1.1.0](https://github.com/Fedos113/SWP_TickFrame_28_team/releases/tag/v1.1.0) |
| **MVP v2** | [v2.0.0](https://github.com/Fedos113/SWP_TickFrame_28_team/releases/tag/v2.0.0) (Sprint 4) |
| **Week 6 Trial** | [v2.2.0](https://github.com/Fedos113/SWP_TickFrame_28_team/releases/tag/v2.2.0) (Sprint 5) |
| **MVP v3** | [v3.0.0](https://github.com/Fedos113/SWP_TickFrame_28_team/releases/tag/v3.0.0) (Sprint 6 — Assignment 7) |

---

## 2. Team Members & GitHub Usernames

| Person | GitHub | Role | Technical Responsibilities |
|---|---|---|---|
| F. Kozhevnikov | [Fedos113](https://github.com/Fedos113) | Product Owner / Full-Stack | Backend, frontend, architecture, CI/CD |
| A. Gafarov | [omarichev](https://github.com/omarichev) | Developer / Documentation | Backend, documentation, reports |
| A. Mindubaev | [pug228](https://github.com/pug228) | Developer / Quality & CI | QRTs, testing strategy, CI pipeline |
| D. Zhechev | [DaniilJechev](https://github.com/DaniilJechev) | Scrum Master / ML Engineer | ML model training, ML microservice |
| M. Bezborodov | [MikhailBezborodov024](https://github.com/MikhailBezborodov024) | Developer / Frontend | Frontend UI, chart components |

---

## 3. Current Sprint Status

### Sprint 5 (Week 6) — Completed
- **Milestone:** [Sprint 5](https://github.com/Fedos113/SWP_TickFrame_28_team/milestone/6)
- **Dates:** 2026-07-07 – 2026-07-13
- **Goal:** Week 6 trial / handover-candidate release
- **Outcome:** Trial release with indicators subsystem (445+ indicators), drawing refinements, WebSocket fixes, customer-facing documentation polish

### Sprint 6 (Week 7) — Completed
- **Milestone:** [Sprint 6 — MVP v3](https://github.com/Fedos113/SWP_TickFrame_28_team/milestone/7)
- **Dates:** 2026-07-14 – 2026-07-20
- **Goal:** Deliver MVP v3 — follow-up maintenance, fixes from Week 6 trial, final transition, Demo Day preparation
- **Outcome:** MVP v3 delivered — DT/DB dual-model ML detection integrated, PostgreSQL migration completed, UI overhaul (sidebar, indicators, metrics, pattern filtering), Sprint 6 review documented, customer handover finalised, Demo Day preparation underway

---

## 4. Release Status

| Release | Tag | Date | Maps To |
|---|---|---|---|
| MVP v1 | `v1.0.0` | 2026-06-21 | Sprint 2 |
| Sprint 3 Increment | `v1.1.0` | 2026-06-26 | Sprint 3 |
| MVP v2 | `v2.0.0` | 2026-07-06 | Sprint 4 (A5) |
| Week 6 Trial | `v2.2.0-trial` | Week 6 | Sprint 5 (A6) |
| **MVP v3** | `v3.0.0` | 2026-07-17 | Sprint 6 (A7) |

---

## 5. Key Links

### Repository
| Resource | Link |
|---|---|
| Repository | https://github.com/Fedos113/SWP_TickFrame_28_team |
| Issues | https://github.com/Fedos113/SWP_TickFrame_28_team/issues |
| Projects Board | https://github.com/users/Fedos113/projects/1/views/1 |
| Pull Requests | https://github.com/Fedos113/SWP_TickFrame_28_team/pulls |
| Releases | https://github.com/Fedos113/SWP_TickFrame_28_team/releases |
| Actions (CI) | https://github.com/Fedos113/SWP_TickFrame_28_team/actions |

### Milestones
| Milestone | Link |
|---|---|
| Sprint 5 | https://github.com/Fedos113/SWP_TickFrame_28_team/milestone/6 |
| Sprint 6 — MVP v3 | https://github.com/Fedos113/SWP_TickFrame_28_team/milestone/7 |

### Maintained Docs
| Document | Path |
|---|---|
| Customer Handover | [`docs/customer-handover.md`](../../docs/customer-handover.md) |
| Contributing Guide | [`CONTRIBUTING.md`](../../CONTRIBUTING.md) |
| Agent Guidance | [`AGENTS.md`](../../AGENTS.md) |
| Roadmap | [`docs/roadmap.md`](../../docs/roadmap.md) |
| Product Backlog | [`docs/backlog.md`](../../docs/backlog.md) |
| Definition of Done | [`docs/definition-of-done.md`](../../docs/definition-of-done.md) |
| Quality Requirements | [`docs/quality-requirements.md`](../../docs/quality-requirements.md) |
| Quality Requirement Tests | [`docs/quality-requirement-tests.md`](../../docs/quality-requirement-tests.md) |
| Testing Strategy | [`docs/testing.md`](../../docs/testing.md) |
| User Acceptance Tests | [`docs/user-acceptance-tests.md`](../../docs/user-acceptance-tests.md) |
| User Stories | [`docs/user-stories.md`](../../docs/user-stories.md) |
| Architecture Docs | [`docs/architecture/README.md`](../../docs/architecture/README.md) |
| Development Process | [`docs/development-process.md`](../../docs/development-process.md) |
| Changelog | [`CHANGELOG.md`](../../CHANGELOG.md) |
| README | [`README.md`](../../README.md) |

### Reports
| Week | Path |
|---|---|
| Week 6 | [`reports/week6/README.md`](../../reports/week6/README.md) |
| Week 7 | [`reports/week7/README.md`](../../reports/week7/README.md) |

---

## 6. CI Pipeline

| Job | Tool | Runs On |
|---|---|---|
| lint | `ruff check .` | push/PR to main |
| type-check | `mypy tickframe/` | push/PR to main |
| test | `pytest --cov=tickframe --cov-report=xml tests/` | push/PR to main |
| qa-check | `bandit -r tickframe/ -ll` | push/PR to main |
| frontend-lint | `eslint tickframe/frontend/js/` | push/PR to main |
| frontend-test | `vitest run` (in `tickframe/frontend/`) | push/PR to main |
| link-check | `lychee` (all `.md` files) | push/PR to main |

---

## 7. Quality Requirements & Tests

| QR ID | Metric | QRT | Status |
|---|---|---|---|
| QR-001 | p95 ≤ 500ms | QRT-001 | Active |
| QR-002 | Zero secrets in commits | QRT-002 | Active |
| QR-003 | F2 ≥ 0.55, FPR ≤ 20% | QRT-003 | Active |
| — | WebSocket Reliability | QRT-004 | Active |
| — | DB Cache Round-Trip | QRT-005 | Active |

---

## 8. Testing Status

| Type | Scope | Location | Status |
|---|---|---|---|
| Unit | Backend services | `tests/unit/` | ✅ |
| Integration | API endpoints | `tests/integration/` | ✅ |
| QRTs | 5 requirement tests | `tests/requirements/` | ✅ |
| Frontend | JS unit tests | `tickframe/frontend/js/tests/` | ✅ |

---

## 9. Completed Week 7 Contributions (Branches `7-repo`, `feature/dtdb-numba-optimization`, and `sprint-review-docs`)

### A7 Scaffolding & Sprint 6 Planning

| Item | Detail | Status |
|---|---|---|
| `assignments/7/Assignment_07.md` | Week 7 spec — Sprint 6 completion, MVP v3, transition, Demo Day, 10 parts | ✅ Done |
| `assignments/7/architecture.md` | Architecture doc with updated paths for A7 | ✅ Done |
| `assignments/7/breakdown.md` | Task breakdown for Sprint 6 (30+ tasks) | ✅ Done |
| `assignments/7/context.md` | Memory7 AI context file (this file) | ✅ Done |
| `assignments/7/contributions.md` | Clean contribution tracking table for Week 7 | ✅ Done |
| `assignments/7/issue_template.md` | Issue template for A7 / Sprint 6 work | ✅ Done |

### Sprint 6 Milestone & Issue Tracking

| Item | Detail | Status |
|---|---|---|
| Sprint 6 milestone | 14 OPEN issues across 4 PBIs + 10 course tasks | ✅ Done |
| PBI-130 (#201) | PostgreSQL infrastructure migration — SQLite to PostgreSQL 17 | ✅ Done |
| PBI-131 (#202) | Pattern filtering and confidence threshold controls | ✅ Done |
| PBI-132 (#216) | Fix UI glitches on timeframe switch | ✅ Done |
| PBI-133 (#217) | Implement scan results export | ✅ Done |
| Course tasks (#218–#222) | Sprint 6 Review, Retrospective, Reflection, Transition, Docs | ✅ Done — all artifacts created |
| PBI-134 (#226) | DT/DB detector integration and dual-model inference optimization | ✅ Done |
| DOC (#227) | DT/DB integration architecture and verification documentation | ✅ Done |
| Sprint 5 milestone | Fully closed — 19 issues all marked Done | ✅ Done |
| `docs/backlog.md` | Updated Sprint 5 → Previous, Sprint 6 → Current with new PBIs | ✅ Done |
| `docs/roadmap.md` | Updated Sprint 6 planned items with new PBIs + course tasks | ✅ Done |

### Issue Creation from Customer Feedback

All issues follow `assignments/7/issue_template.md` format with AC, SP, roles, DoD checklist.

| Source | Issues Created |
|---|---|
| Sprint 4 customer feedback (Nikolay Kuzmin, 2026-07-03) | #216 PBI-132 (UI glitches), #217 PBI-133 (export) |
| Sprint 4 customer feedback (pattern filtering) | #202 PBI-131 (already existed) |
| Assignment 7 spec requirements | #218 (Sprint Review), #219 (Retro), #220 (Reflection/LLM), #221 (Transition), #222 (Docs) |

### DT/DB Dual-Model Contribution

The branch `feature/dtdb-numba-optimization` adds the DT/DB XGBoost detector
to the existing ML API while preserving the H&S detector. Both detectors run
from one `/predict` request with detector-specific feature contracts,
thresholds, NMS, and processing timings.

- **Implementation issue:** [#226](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/226)
- **Documentation issue:** [#227](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/227)
- **Architecture report:** [`docs/architecture/dtdb-integration-decisions.md`](../../docs/architecture/dtdb-integration-decisions.md)
- **Performance:** Numba accelerates extrema selection; shared base features
  are computed once per request and the kernel is warmed during startup.
- **Verification:** after warmup, the shared feature pipeline processed 10,000
  synthetic candles in approximately 49 ms on Windows. Full endpoint and CI
  verification remain pending in the Docker/CI environment.

### Sprint Review Documentation & Final Handover Reports (Branch `sprint-review-docs`)

The branch `sprint-review-docs` delivers the complete Sprint 6 (Week 7) review
documentation, retrospective, reflection, and LLM report — all based on the
2026-07-17 customer meeting.

| Artifact | Path | Description |
|---|---|---|
| Sprint Review Summary | [`reports/week7/sprint-review-summary.md`](../../reports/week7/sprint-review-summary.md) | PBI status table, UAT results, customer feedback, action points |
| Sprint Review Transcript | [`reports/week7/sprint-review-transcript.md`](../../reports/week7/sprint-review-transcript.md) | Full 28-min meeting transcript with timestamps and speaker labels |
| Sprint Review Notes | [`reports/week7/sprint-review-notes.md`](../../reports/week7/sprint-review-notes.md) | Condensed meeting notes with key decisions |
| Retrospective | [`reports/week7/retrospective.md`](../../reports/week7/retrospective.md) | What went well, what didn't, changes from previous sprint, process improvements |
| Reflection | [`reports/week7/reflection.md`](../../reports/week7/reflection.md) | Learning points, validated assumptions, friction/gaps, planned response |
| LLM Usage Report | [`reports/week7/llm-report.md`](../../reports/week7/llm-report.md) | OpenCode usage areas and limitations encountered |
| Week 7 Report Index | [`reports/week7/README.md`](../../reports/week7/README.md) | 31-section Week 7 report with transition outcome, UAT results, release, contribution traceability |

Key updates across the repository:
- **A7 scaffolding files:** All 6 `assignments/7/*.md` files updated with Sprint 6 completion state — context, architecture, breakdown, contributions, issue template, and assignment spec
- **Customer handover:** [`docs/customer-handover.md`](../../docs/customer-handover.md) updated with Sprint 6 final transition status
- **Database documentation:** [`docs/DATABASE.md`](../../docs/DATABASE.md) added with PostgreSQL schema, migration strategy, and connection configuration
- **Architecture documentation:** [`docs/architecture/README.md`](../../docs/architecture/README.md) and [`docs/architecture/dtdb-integration-decisions.md`](../../docs/architecture/dtdb-integration-decisions.md) updated for Sprint 6
- **CI/Config files:** Docker, Docker Compose, `.cursorignore`, `.gitignore`, `AGENTS.md`, `package.json`, `requirements.txt` updated to reflect MVP v3 state

These artifacts close Course Tasks #218 (Sprint Review), #219 (Retrospective),
#220 (Reflection/LLM), #221 (Transition/Handover), and #222 (Docs).

Corresponding documentation issues created on GitHub:
- [#236](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/236) — DOC: Sprint 6 review documentation (summary, transcript, notes)
- [#237](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/237) — DOC: Sprint 6 retrospective report
- [#238](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/238) — DOC: Update customer handover, database, and architecture docs for Sprint 6

> Note: The Week 7 reflection and LLM report issue could not be created due to network timeout (gh API rate limiting / connectivity). Create it manually: `gh issue create --title "DOC: Add Week 7 reflection and LLM usage report" --label "documentation" --milestone "Sprint 6 — MVP v3" --body-file /tmp/issue5.md`

### Final Week 7 Report & Maintained Documentation Alignment (Branch `assignment-6-parts-7-8-9-docs`)

The branch `assignment-6-parts-7-8-9-docs` delivers the final Assignment 6 Parts 7–9 documentation, Sprint 6 closure artifacts, and maintained documentation alignment for the MVP v3 release.

| Artifact | Path | Description |
|---|---|---|
| Week 7 Report Index | [`reports/week7/README.md`](../../reports/week7/README.md) | 31-section Week 7 report with 3 screenshots, transition outcome, UAT results |
| Screenshots | [`reports/week7/images/`](../../reports/week7/images/) | 3 screenshots: final product access, MVP v3 release, Sprint 6 milestone |
| Customer Handover | [`docs/customer-handover.md`](../../docs/customer-handover.md) | Status set to `Accepted` / `Ready for independent use` |
| UAT Log | [`docs/user-acceptance-tests.md`](../../docs/user-acceptance-tests.md) | UAT-010 defined, Week 6+7 execution log appended |
| Release Notes | [`CHANGELOG.md`](../../CHANGELOG.md) | v3.0.0 release entry (2026-07-19), Sprint 6 changes documented |
| Roadmap | [`docs/roadmap.md`](../../docs/roadmap.md) | Sprint 6 marked completed, v3.0.0 release noted |
| README | [`README.md`](../../README.md) | PostgreSQL, 3 containers, 6 patterns, v3.0.0, Matrix theme |
| Architecture Docs | [`docs/architecture/README.md`](../../docs/architecture/README.md) | PostgreSQL, 3 containers, 6 patterns, deployment view corrected |
| Development Process | [`docs/development-process.md`](../../docs/development-process.md) | PostgreSQL, 3 containers, Docker workflow updated |
| User Stories | [`docs/user-stories.md`](../../docs/user-stories.md) | All 16 stories marked Done |
| Product Backlog | [`docs/backlog.md`](../../docs/backlog.md) | Sprint 6 PBIs and course tasks all Done |
| A7 Context | [`assignments/7/context.md`](../../assignments/7/context.md) | Memory7 updated with final Sprint 6 / Week 7 state |

Corresponding documentation issues created on GitHub:
- [#242](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/242) — DOC: Finalise Week 7 report, release artifacts, and UAT for MVP v3
- [#243](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/243) — DOC: Align maintained documentation for Sprint 6 / MVP v3 final state
- [#244](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/244) — DOC: Update A7 context.md with final Sprint 6 / Week 7 status

---

## 10. Key Week 7 Deliverables — Updated Status

| # | Deliverable | Status |
|---|---|---|
| 1 | Complete Sprint 6 PBIs (PBI-130–133) | ✅ Done — all merged to main |
| 2 | Release MVP v3 (SemVer) | ✅ Done — integrated via `MVPv3` branch, merged to main |
| 3 | Finalize product transition | ✅ Done — customer handover updated for Sprint 6 |
| 4 | Customer handover confirmation | ✅ Done — confirmed in 2026-07-17 Sprint Review |
| 5 | Sprint 6 Review + Retrospective | ✅ Done — reports created in `reports/week7/` |
| 6 | Week 7 reports (README, review, reflection, retrospective, LLM) | ✅ Done — all 7 reports delivered |
| 7 | Updated slide deck + rehearsed presentation video | Issue #185 created |
| 8 | Public sanitized demo video | ✅ Done — [Google Drive](https://drive.google.com/file/d/1Otmlahg1sAH8jTMJmSWi85pBt8RAX6lz/view?usp=sharing) |
| 9 | Demo Day preparation (7-min presentation, <2-min demo) | Issue #185 created |
| 10 | Week 7 Moodle PDF submission | Pending |
| 11 | Final maintained documentation review | ✅ Done — customer-handover, DATABASE.md, architecture docs updated |
| 12 | A7 scaffolding and Sprint 6 planning | ✅ Done |
| 13 | DT/DB dual-model API integration and performance optimization | ✅ Done — merged via #228, #230 |
| 14 | Sprint review documentation and handover reports | ✅ Done — `sprint-review-docs` branch |
| 15 | Week 7 report images and final release artifacts | ✅ Done — 3 screenshots, v3.0.0 release, CHANGELOG |
| 16 | Maintained documentation alignment for MVP v3 | ✅ Done — README, architecture, dev-process, backlog, user-stories |
| 17 | A7 context.md final update with issue references | ✅ Done — #242, #243, #244 created |

---

## 11. Technology Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11, FastAPI, Uvicorn, httpx, websockets |
| **Frontend** | Lightweight Charts v5, Canvas API, vanilla JS, lightweight-charts-drawing, lightweight-charts-indicators, oakscriptjs, Lucide icons, esbuild |
| **Database** | PostgreSQL 16 (via asyncpg) |
| **ML** | XGBoost (6 patterns: H&S, Inverse H&S, Double Top, Double Bottom, Flags, Wedge), Numba, FastAPI microservice |
| **Exchange** | Bybit v5 API (primary), Binance API (fallback) |
| **Deployment** | Docker + Docker Compose (3 containers: ML, TickFrame, PostgreSQL) |
| **CI** | GitHub Actions (ruff, mypy, pytest+cov, bandit, ESLint, Vitest, Lychee) |
| **AI Tools** | OpenCode (deepseek-v4-flash-free) |

---

*Last updated: 2026-07-19 (Sprint 6 / Week 7 — finalised)*
*Generated by: OpenCode (deepseek-v4-flash-free)*
