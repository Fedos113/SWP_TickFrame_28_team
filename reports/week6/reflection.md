# Reflection — Assignment 6 (Week 6)

## Learning Points

_What the team learned from:_

### Technical Indicator Library Integration

Integrating `lightweight-charts-indicators` with 445+ indicators taught the team how to evaluate and adopt third-party libraries effectively. The key lesson was validating library capability (indicator types, pane support, theming compatibility) before committing to integration. The previous sprint's RSI implementation attempt failed because the team assumed capability without verification — this sprint's indicators approach validated first, integrated second.

### Customer-Facing Documentation as a Product Asset

Creating `docs/customer-handover.md`, `CONTRIBUTING.md`, and `AGENTS.md` shifted the team's perspective from "documentation as a submission requirement" to "documentation as a product asset." The customer's ability to independently set up and understand the project from these documents demonstrated that well-structured documentation is as valuable as code for long-term product viability.

### Sprint Capacity Management

Sprint 5 had to balance indicators delivery (the largest single feature in the project) with documentation, trial release, and customer meeting preparation. The team learned that deferring known customer requests (PostgreSQL, pattern filtering) creates downstream risk — what seems like a reasonable deferral in sprint planning becomes a dependency blocker in the next sprint.

---

## Validated Assumptions

| Assumption | Status | Evidence |
|---|---|---|
| 445+ indicators can be integrated within one sprint | ✅ Confirmed | Indicators subsystem delivered with searchable panel, panes, chips, and persistence |
| Customer-facing docs can be created in parallel with feature work | ✅ Confirmed | AGENTS.md, CONTRIBUTING.md, customer-handover.md all delivered alongside indicators |
| Customer will review documentation during trial | ❌ Rejected | Sprint 5 review focused on architecture; documentation review did not occur as expected |
| Trial release will surface all remaining blockers | ⚠️ Partial | PostgreSQL and pattern filtering identified as blockers; other areas not surfaced |

---

## Friction and Gaps

- **PostgreSQL migration was deferred.** The customer explicitly requested it during the Sprint 5 architecture review, but it was pushed to Sprint 6 due to capacity constraints. This was the single biggest gap in the trial release.

- **Pattern filtering not delivered.** The customer requested pattern-type filtering in Sprint 4 UAT, confirmed it in Sprint 5 review, but it was not implemented in Sprint 5.

- **Only 4 of 6 ML patterns in the trial.** Double Top and Double Bottom were in development but not ready for the trial release.

- **No formal transition-readiness meeting.** The Sprint 5 review covered architecture and features but did not include a formal Part 5 transition-readiness discussion with the customer.

- **Missing independent customer trial.** The customer did not independently try the Week 6 trial release between the Sprint 5 and Sprint 6 reviews.

---

## Planned Response

| Issue | Planned Action | Links |
|---|---|---|
| PostgreSQL migration | Complete PBI-130 in Sprint 6 | [#201](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/201) |
| Pattern filtering | Complete PBI-131 in Sprint 6 | [#202](https://github.com/Fedos113/SWP_TickFrame_28_team/issues/202) |
| Remaining 2 ML patterns | Complete DT/DB integration in Sprint 6 | — |
| UI overhaul (coin search, metrics) | Implement in Sprint 6 maintenance work | — |
| Formal transition meeting | Schedule Part 5 meeting in Sprint 6 | — |
| Customer documentation review | Ask customer to review full doc set in Sprint 6 | — |
