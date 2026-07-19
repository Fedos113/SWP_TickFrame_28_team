# Product Backlog

## Overview

This backlog tracks all PBIs (Product Backlog Items) for TickFrame. PBIs are organized by Sprint milestones and managed via GitHub Issues + Project Board.

---

## Labels

| Label | Meaning |
|-------|---------|
| `enhancement` | Feature PBI |
| `bug` | Bug fix |
| `documentation` | Documentation task |
| `good first issue` | Suitable for new contributors |

## Workflow States

A PBI moves through these states:

```
Backlog → Ready → In Progress → Review → Done
```

- **Backlog**: Not yet scheduled for a Sprint
- **Ready**: Refined, estimated, meets Definition of Ready
- **In Progress**: Someone is actively working on it
- **Review**: PR is open, needs code review
- **Done**: Merged to main, acceptance criteria satisfied

## Definition of Ready

A PBI is **Ready** when:
- Title and description are clear
- Acceptance criteria are defined
- Dependencies are identified and resolved
- Estimated in Story Points (SP)

## Definition of Done

A PBI is **Done** when:
- All acceptance criteria are satisfied
- Code is merged to `main` via PR with review
- CI (tests, linting) passes
- CHANGELOG.md is updated
- No secrets or credentials committed

---

## Sprint 3 — v1.1.0 (Previous)

**Milestone:** [Sprint 3 — Assignment 4 — v1.2.0](https://github.com/Fedos113/SWP_TickFrame_28_team/milestone/3)

**Goal:** Drawing toolbar with 13 tools, 50k candle support, SQLite persistence, WebSocket heartbeat, pattern analysis UI, coin sidebar enhancements, redact/undo system

| # | PBI | Title | SP | Status |
|---|-----|-------|----|--------|
| [#62](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/62) | PBI-101 | Drawing Toolbar Engine — 13-tool canvas overlay | 3 | Done |
| [#64](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/64) | PBI-102 | Advanced Drawing Tools — Fibonacci, Price Range %, Text tool | 2 | Done |
| [#63](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/63) | PBI-103 | Redact Mode + Selection + Drag-to-Move/Reshape | 1 | Done |
| [#66](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/66) | PBI-104 | Undo System — Add/Modify/Delete support | 1 | Done |
| [#65](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/65) | PBI-105 | Per-Drawing Settings Panel — Color, Width, Line Style, Font Size | 1 | Done |
| [#67](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/67) | PBI-106 | SQLite Persistence — Drawings, Settings, and Candles | 2 | Done |
| [#68](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/68) | PBI-107 | 50k Candle Support + Two-Phase Load + Pagination | 1 | Done |
| [#69](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/69) | PBI-108 | WebSocket Heartbeat + LIVE Status Indicator | 1 | Done |
| [#70](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/70) | PBI-109 | Pattern Analysis UI — Sliding Window + Visualization | 1 | Done |
| [#61](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/61) | PBI-110 | Coin Sidebar — Full Ticker, Trend Colors, 6-Digit Price Format | 1 | Done |
| [#71](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/71) | PBI-111 | Theme Persistence + Light Theme Fix + Theme-Aware Drawing Colors | 1 | Done |
| [#72](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/72) | — | Bug Fixes Batch (drag undo, delete undo, race condition, canvas leak, dead code, etc.) | — | Done |
| [#74](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/74) | PBI-112 | API Rate Limiting, DB Query Optimisation & Candle Performance | 2 | Done |
| [#75](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/75) | PBI-113 | Coin Switch Stability & Loading Overlay | 1 | Done |
| [#76](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/76) | PBI-114 | Frontend Candle Cache & Zoom-Out Lazy Loading | 1 | Done |

---

## Sprint 4 — MVP v2 (Previous)

**Milestone:** [Sprint 4](https://github.com/Fedos113/SWP_TickFrame_28_team/milestone/5)

**Goal:** Deliver MVP v2 by addressing critical customer feedback from Sprint 3 — WebSocket migration, DB caching, RSI/Volume sub-charts, multi-interval support, analysis range fix.

### Completed PBIs

| # | PBI | Title | SP | Status |
|---|-----|-------|----|--------|
| [#122](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/122) | PBI-121 | Multi-interval database caching with near-instant chart loading | 3 | Done |
| [#123](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/123) | PBI-122 | Configurable candle analysis limit for pattern detection | 1 | Done |
| [#124](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/124) | PBI-123 | ML pattern visualization with merged segments | 2 | Done |
| [#125](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/125) | PBI-124 | ML inference performance optimization (XGBoost) | 5 | Done |
| [#126](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/126) | PBI-125 | UI cleanup & sidebar resize with persistence | 2 | Done |
| [#158](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/158) | PBI-126 | UI redesign — coin icons, Fear & Greed Index, sidebar overhaul | 3 | Done |
| [#159](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/159) | PBI-127 | Drawing toolbar re-architecture with lightweight-charts-drawing library | 5 | Done |
| [#113](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/113) | PBI-118 | Volume sub-chart implementation | 3 | Done |
| [#110](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/110) | PBI-115 | WebSocket subscription migration | 5 | Done |

### Completed in Sprint 5

| # | PBI | Title | SP | Status |
|---|-----|-------|----|--------|
| [#112](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/112) | PBI-117 | RSI indicator sub-chart → delivered as 445+ indicators subsystem (PR #200) | 3 | Done |

### Superseded PBIs (folded into completed work above)

| # | PBI | Title | Reason |
|---|-----|-------|--------|
| ~~[#111](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/111)~~ | ~~PBI-116~~ | ~~SQLite-based candle caching~~ | Superseded by PBI-121 (multi-interval caching) |
| ~~[#114](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/114)~~ | ~~PBI-119~~ | ~~Reduce analysis range to 50k~~ | Superseded by PBI-122 (configurable limit) |
| ~~[#115](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/115)~~ | ~~PBI-120~~ | ~~Multi-interval support~~ | Superseded by PBI-121 (multi-interval caching) |

---

## Sprint 5 — Week 6 Trial Release (Previous)

**Milestone:** [Sprint 5](https://github.com/Fedos113/SWP_TickFrame_28_team/milestone/6)

**Release:** [v2.2.0](https://github.com/Fedos113/SWP_TickFrame_28_team/releases/tag/v2.2.0)

**Goal:** Produce stable trial/handover-candidate release — indicators subsystem, customer-facing documentation, handover prep, customer trial.

| # | PBI | Title | SP | Status |
|---|-----|-------|----|--------|
| [#112](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/112) | PBI-117 | RSI indicator sub-chart | 3 | Done |
| [#177](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/177) | PBI-129 | Customer-facing documentation review and update | — | Done |
| [#178](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/178) | — | Create/update CONTRIBUTING.md and AGENTS.md | — | Done |
| [#179](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/179) | — | Create/update docs/customer-handover.md | — | Done |
| [#180](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/180) | — | Week 6 trial release and deployment | — | Done |
| [#186](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/186) | — | DOC: Update localhost port references from 8000 to 8080 | — | Done |
| [#187](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/187) | — | DOC: Add Sprint 5 and Sprint 6 sections to backlog and roadmap | — | Done |
| [#188](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/188) | — | DOC: Create A6 scaffolding and team planning files | — | Done |
| [#189](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/189) | — | DOC: Create repo template files for A6 Part 3 and Part 4 | — | Done |
| [#190](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/190) | — | Course Task: Complete A6 Part 1 — Sprint 5 and Sprint 6 planning | — | Done |
| [#198](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/198) | PBI-118 | Add indicators subsystem with 445+ technical indicators | 5 | Done |
| [#199](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/199) | — | Drawing toolbar refinements, chart fixes, and WS race condition fix | — | Done |
| [#208](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/208) | PBI-135 | Train secondary Neural Network for DT & DB pattern classification | 5 | Done |
| [#209](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/209) | — | Assignment 6: Moodle PDF Template — Week 6 Submission | — | Done |
| [#212](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/212) | — | DOC: Update week 6 contributions.md | — | Done |

---

## Sprint 6 — MVP v3 (Completed)

**Milestone:** [Sprint 6 — MVP v3](https://github.com/Fedos113/SWP_TickFrame_28_team/milestone/7)

**Release:** [v3.0.0](https://github.com/TickFrame/SWP_TickFrame_28_team/releases/tag/v3.0.0)

**Goal:** Deliver final course version MVP v3 — follow-up maintenance, fixes from Week 6 trial, final transition, Demo Day preparation.

### PBIs

| # | PBI | Title | SP | Status |
|---|-----|-------|----|--------|
| [#201](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/201) | PBI-130 | PostgreSQL infrastructure migration — SQLite to PostgreSQL 16 | 5 | Done |
| [#202](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/202) | PBI-131 | Pattern filtering and confidence threshold controls | 3 | Done |
| [#216](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/216) | PBI-132 | Fix UI glitches on timeframe switch | 2 | Done |
| [#217](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/217) | PBI-133 | Implement scan results export | 3 | Done |
| [#225](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/225) | — | Sprint 6 maintenance and ML fixes | 3 | Done |
| [#226](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/226) | PBI-134 | DT/DB detector integration and dual-model inference optimization | 5 | Done |
| [#227](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/227) | — | DT/DB integration architecture and verification documentation | — | Done |

### Course Tasks & Documentation

| # | Title | Status |
|---|-------|--------|
| [#181](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/181) | DOC: Follow-up maintenance from Week 6 trial feedback | Done |
| [#182](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/182) | DOC: Final transition and MVP v3 release | Done |
| [#183](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/183) | DOC: Record public sanitized demo video for MVP v3 | Done — [Google Drive](https://drive.google.com/file/d/1Otmlahg1sAH8jTMJmSWi85pBt8RAX6lz/view?usp=sharing) |
| [#184](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/184) | DOC: Sprint 5 and Sprint 6 reports | Done |
| [#185](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/185) | DOC: Prepare presentation slides and rehearsal | Done |
| [#218](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/218) | Course Task: Conduct Sprint 6 Review meeting | Done |
| [#219](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/219) | Course Task: Conduct Sprint 6 Retrospective | Done |
| [#220](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/220) | Course Task: Write Week 7 reflection and LLM report | Done |
| [#221](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/221) | Course Task: Complete customer transition confirmation and update handover | Done |
| [#222](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/222) | Course Task: Final documentation maintenance for Sprint 6 | Done |

---

## Backlog (Future Work)

| PBI | Title | Notes |
|-----|-------|-------|
| US-09 | Coin search/filter | Search bar for coin list |
| US-14 | Real-time dashboard | Auto-refreshing dashboard |
| US-15 | UI polish pass | Layout, spacing, responsive fixes |

---

## How to Add a New PBI

1. Create a GitHub Issue using the appropriate template (`user_story.md`, `bug_report.md`, `other_pbi.md`)
2. Add the correct label (`enhancement`, `bug`, `documentation`)
3. Write clear acceptance criteria
4. Optionally assign Story Points in the description
5. When ready for a Sprint, assign to the milestone

## How to Close a Sprint

1. Verify all PBIs in the milestone are Done
2. Update CHANGELOG.md — move `[Unreleased]` to a dated version section
3. Create a SemVer release on GitHub
4. Update backlog.md — move completed PBIs to a "Previous Sprints" section
