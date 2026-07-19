# Sprint 5 Retrospective — Assignment 6 (Week 6)

**Date:** 2026-07-13

---

## What Went Well

1. **Indicators subsystem delivered successfully.** The 445+ technical indicators library was integrated via npm with a searchable panel UI, collapsible groups, and RSI auto-apply on symbol switch. This was the largest single feature delivered in Sprint 5.

2. **Drawing toolbar refinements completed.** All customer feedback from Sprint 4 on drawing toolbar layout, icons, z-order, and HiDPI rendering was addressed.

3. **WebSocket race condition fixed.** Stale candle updates after symbol switch no longer occur, significantly improving real-time data reliability.

4. **Customer-facing documentation polished.** SVG architecture diagram, troubleshooting section, UI screenshot, and relative link cleanup — all A6 Part 3 requirements met.

5. **Customer-handover documentation created.** New `docs/customer-handover.md` with Transition Scope, env-var documentation, setup/deployment, known limitations, and sufficiency assessment.

6. **Sprint review and reports completed on time.** Week 6 report, sprint review transcript, summary, and documentation were delivered.

## What Did Not Go Well

1. **PostgreSQL migration deferred.** The customer explicitly requested PostgreSQL during the Sprint 5 architecture review, but the migration was pushed to Sprint 6 due to capacity constraints. This delayed the trial release's architecture readiness.

2. **Only 4 ML patterns delivered instead of 6.** Double Top and Double Bottom patterns were in development but not yet integrated into the trial release. The customer expected all 6 patterns.

3. **Pattern filtering not implemented.** The customer requested pattern-type filtering and confidence threshold controls, but this was deferred to Sprint 6.

4. **UI polish incomplete.** The indicators panel worked but the broader UI overhaul (coin search, market header, Matrix theme) was not started in Sprint 5 due to focus on core indicators functionality.

5. **Customer handover not formally accepted.** The Sprint 5 review covered progress and architecture, but the formal transition-readiness meeting was not conducted. Customer acceptance remained pending.

## Changes from Previous Sprint

_Based on the previous Sprint retrospective (see [reports/week5/retrospective.md](../week5/retrospective.md)):_

- **Action point 1 (was: "Vendor library capability validation before implementation"):** ✅ Addressed. The `lightweight-charts-indicators` library was validated before full integration. No repeat of the RSI manual-implementation failure.

- **Action point 2 (was: "Anticipate complementary features when planning"):** ⚠️ Partially addressed. Drawing toolbar refinements anticipated indicator overlay needs (z-order fixes), but pattern filtering was not anticipated despite customer feedback from Sprint 4.

- **Action point 3 (was: "Reserve story points for UI polish"):** ❌ Not addressed. UI polish (coin search, market header) was intentionally deferred to Sprint 6 to prioritise indicators. This was a conscious trade-off rather than a planning failure.

- **Action point 4 (was: "Split documentation work into smaller PRs"):** ✅ Addressed. Documentation was split across multiple focused PRs (customer-handover, AGENTS/CONTRIBUTING, entry-point docs, sprint reports).

## Process Improvements for Next Sprint

1. **Critical customer requests should not be deferred.** The PostgreSQL migration was a blocking request from the customer. When a customer explicitly requests an architecture change, it should be treated as a PBI in the current sprint, not the next.

2. **Track pattern completeness vs. delivery scope.** The team planned 4 ML patterns for Sprint 5 but the customer expected 6. Align expectations earlier in sprint planning.

3. **Reserve capacity for customer-requested UI features.** Pattern filtering and coin metrics were known requests from Sprint 4 UAT but were not scheduled. Proactively reserve capacity for known customer feedback items.
