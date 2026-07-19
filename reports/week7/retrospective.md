# Sprint 6 Retrospective — Assignment 6 (Week 7)

**Date:** 2026-07-17

---

## What Went Well

1. **All 6 ML patterns delivered.** Double Top and Double Bottom were added alongside existing Head and Shoulders and Inverse Head and Shoulders patterns. The backward-compatible API allowed integration without changing the frontend or existing pipeline ([PR on new branch]).

2. **PostgreSQL migration completed successfully.** SQLite was replaced with a dedicated PostgreSQL 16 container as part of Docker Compose. Database credentials are configurable via environment variables. Schema initialisation uses startup migrations instead of application-created tables — directly addressing the customer's critical feedback from Week 6.

3. **UI overhaul delivered.** Sidebar with coin search, draggable indicators without overlap, CoinGecko-powered metrics (5m/1h/4h change, market cap, supply), and pattern-type filtering — all customer requests from previous sprints were implemented.

4. **Pattern filtering implemented.** Toggle switches next to the patterns panel let users enable/disable specific pattern types — a feature the customer explicitly requested in the Week 6 review.

5. **Pre-computation architecture working.** All coins are analysed by the ML model before project initialisation. The "Analyze" button retrieves pre-calculated results from the database, making the user experience near-instant.

6. **Final deployment ready.** The fully completed version was scheduled for VM deployment the same evening as the review.

## What Did Not Go Well

1. **Anomaly detection not delivered.** Despite multiple approaches explored, no viable solution was found within sprint constraints. The lack of public research and labelled data made this infeasible. Should have been scoped as a risk-mitigation spike earlier.

2. **Concurrency handling not addressed.** The customer's question about simultaneous "Analyze" clicks exposed that no locking or idempotency mechanism exists. While analysis is sub-second, this is a quality gap for any multi-user scenario.

3. **Container dependency friction.** NPM missing from the TickFrame container caused setup issues. Dependency management was not fully accounted for in the Docker build process.

4. **DT/DB precision is low (17-18%).** While recall is acceptable at 80%, precision means many false positives. The team acknowledged this needs post-course refinement.

5. **No progress on multi-timeframe ML.** Only the 5-minute timeframe is supported. All 6 patterns are locked to a single interval. This was deferred across multiple sprints and never resolved.

## Changes from Previous Sprint

_Based on the previous Sprint retrospective (see [reports/week5/retrospective.md](../week5/retrospective.md)):_

- **Action point 1 (was: "Library capability validation before implementation"):** ✅ Addressed. The indicator library was validated before integration. No repeat of the RSI manual-implementation failure.

- **Action point 2 (was: "Anticipate complement features"):** ✅ Addressed. Pattern filtering was proactively implemented in Sprint 6 without needing a customer prompt.

- **Action point 3 (was: "Reserve capacity for UI polish"):** ✅ Addressed. UI polish (indicators, sidebar, metrics) was a major focus of Sprint 6 and delivered successfully.

- **Action point 4 (was: "Split documentation work into smaller PRs"):** ✅ Addressed. Documentation work was split into focused increments throughout the project.

- **New issue — Anomaly detection scoping:** The team learned that novel ML features without existing research require spike PBIs, not delivery PBIs.

## Process Improvements for Next Sprint

_(Not applicable — final course sprint. Recorded for future team reference.)_

1. **Spike PBIs for novel features.** When a feature has no established implementation path (e.g., anomaly detection), create a time-boxed spike PBI to assess feasibility before committing to delivery.

2. **Concurrency testing in Definition of Done.** Add a concurrency check to the DoD for any endpoint that modifies shared state — even if the current deployment is single-user.

3. **Container build validation.** Docker builds should validate that all expected tools and dependencies are available (e.g., NPM, Python packages) as part of CI.

4. **ML precision targets in PBI acceptance criteria.** Future ML PBIs should specify minimum precision and recall targets in the acceptance criteria to ensure models meet quality thresholds before merge.
