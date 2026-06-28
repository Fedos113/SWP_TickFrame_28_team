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

## Sprint 3 — v1.1.0 (Current)

**Milestone:** [Sprint 3 — Assignment 4 — v1.1.0](https://github.com/Fedos113/SWP_TickFrame_28_team/milestone/3)

**Goal:** Drawing toolbar with 13 tools, 50k candle support, SQLite persistence, WebSocket heartbeat, pattern analysis UI, coin sidebar enhancements, redact/undo system

| # | PBI | Title | SP | Status |
|---|-----|-------|----|--------|
| [#62](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/62) | PBI-101 | Drawing Toolbar Engine — 13-tool canvas overlay | 13 | Done |
| [#64](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/64) | PBI-102 | Advanced Drawing Tools — Fibonacci, Price Range %, Text tool | 8 | Done |
| [#63](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/63) | PBI-103 | Redact Mode + Selection + Drag-to-Move/Reshape | 8 | Done |
| [#66](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/66) | PBI-104 | Undo System — Add/Modify/Delete support | 5 | Done |
| [#65](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/65) | PBI-105 | Per-Drawing Settings Panel — Color, Width, Line Style, Font Size | 8 | Done |
| [#67](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/67) | PBI-106 | SQLite Persistence — Drawings, Settings, and Candles | 8 | Done |
| [#68](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/68) | PBI-107 | 50k Candle Support + Two-Phase Load + Pagination | 5 | Done |
| [#69](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/69) | PBI-108 | WebSocket Heartbeat + LIVE Status Indicator | 3 | Done |
| [#70](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/70) | PBI-109 | Pattern Analysis UI — Sliding Window + Visualization | 8 | Done |
| [#61](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/61) | PBI-110 | Coin Sidebar — Full Ticker, Trend Colors, 6-Digit Price Format | 3 | Done |
| [#71](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/71) | PBI-111 | Theme Persistence + Light Theme Fix + Theme-Aware Drawing Colors | 3 | Done |
| [#72](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/72) | — | Bug Fixes Batch (drag undo, delete undo, race condition, canvas leak, dead code, etc.) | — | Done |
| [#74](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/74) | PBI-112 | API Rate Limiting, DB Query Optimisation & Candle Performance | 8 | Done |
| [#75](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/75) | PBI-113 | Coin Switch Stability & Loading Overlay | 5 | Done |
| [#76](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/76) | PBI-114 | Frontend Candle Cache & Zoom-Out Lazy Loading | 5 | Done |

---

## Backlog (Future Sprints)

| PBI | Title | Notes |
|-----|-------|-------|
| US-07 | Timeframe selector (5m, 15m, 1h, 4h, 1d) | Interval buttons exist, switching needs refinement |
| US-09 | Coin search/filter | Search bar for coin list |
| US-10 | Volume sub-chart | Volume bars below candles |
| US-11 | RSI indicator sub-chart | RSI line below candles |
| US-12 | Fear & Greed Index | Market sentiment widget |
| US-14 | Real-time dashboard | Auto-refreshing dashboard |
| US-15 | UI polish pass | Layout, spacing, responsive fixes |
| QR-001 | Performance (chart redraw <2s) | Requires QRT-001 test automation |
| QR-002 | Security (no secret leaks) | Requires QRT-002 test automation |
| QR-003 | Accuracy (candle data ~0.1%) | Requires QRT-003 test automation |

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
