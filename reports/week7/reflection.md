# Reflection — Assignment 6 (Week 7)

## Learning Points

_What the team learned from:_

### Database Integration and ML Persistence

Integrating ML pattern results into PostgreSQL taught the team how pre-computation with database caching eliminates perceived latency. By running ML analysis on all 10 coins before project initialisation, the "Analyze" button response becomes near-instant — only ≈50–150 unprocessed candles per click need live analysis (≈0.01s). The timestamp-based tracking of the last analysed candle, stored in the database, enables incremental analysis without redundant computation. First-time startup (≈2–3 min for candle fetch + ≈1 min for ML) is a one-time cost; subsequent starts are instant due to persistence.

### Container Architecture Trade-offs

Running backend and frontend from a single Docker container is non-standard but exposed practical trade-offs for an MVP: simplified orchestration vs. coupling of dependency lifecycles (e.g., NPM not pre-installed in the container). The team learned that while this works for a course project, production deployments should separate concerns. The customer acknowledged the compromise, reinforcing that architectural decisions must match project scope.

### Concurrency Awareness

The customer's questions about simultaneous "Analyze" clicks revealed a blind spot: the team had not explicitly tested or implemented locking for concurrent analysis requests. While the sub-second analysis time makes race conditions low-risk, the team recognised that production systems serving multiple concurrent users would need idempotency guarantees or request deduplication.

### ML Pattern Development Without Existing Research

Developing Double Top and Double Bottom detection without established public research or datasets was a significant challenge. The team learned that ML in niche domains often requires inventing pipelines from scratch — personal experimentation and iterative testing replace following tutorials. The experience validated that practical ML engineering is as much about data pipeline construction and feature engineering as it is about model architecture.

### Customer Handover Readiness

The final Sprint Review confirmed that meeting all customer-requested PBIs (PostgreSQL migration, pattern filtering, coin metrics, UI fixes, 6 ML patterns) does not guarantee a production-ready system. The anomaly detection PBI was dropped due to complexity — the team learned to better scope PBIs during planning rather than deferring discovery to the final sprint.

---

## Validated Assumptions

| Assumption | Status | Evidence |
|---|---|---|
| PostgreSQL migration achievable in one sprint | ✅ Confirmed | 3-container Docker Compose (ML, TickFrame, PostgreSQL) working with env-var credentials |
| Pattern filtering can be implemented as toggle next to patterns panel | ✅ Confirmed | Customer confirmed feature works as expected |
| DT/DB ML patterns can be added with backward-compatible API | ✅ Confirmed | New models integrated into existing pipeline without breaking changes |
| Pre-analysis at init eliminates perceived latency on "Analyze" | ✅ Confirmed | 50K candles pre-analysed; click retrieves from DB instantly |
| Anomaly detection can be delivered within course scope | ❌ Rejected | Insufficient research foundation and data — dropped after exploration |
| 6 ML patterns in one container architecture is acceptable for MVP | ✅ Confirmed | Customer accepted backend+frontend in same container as MVP compromise |

---

## Friction and Gaps

- **Anomaly detection was dropped.** The team explored multiple approaches but found no public research or datasets to build upon. Time constraints prevented developing a novel solution from scratch. This PBI should have been scoped as a spike earlier in the project rather than as a delivery item in the final sprint.

- **Concurrency not stress-tested.** The team never validated behaviour under simultaneous user requests. For a single-user/local deployment this is acceptable, but the customer's concern about concurrent "Analyze" clicks exposed an untested path.

- **Container dependency management.** NPM was not pre-installed in the TickFrame container, causing setup friction. Dependency installation should be part of the Docker build process, not assumed on the host.

- **Frontend + backend coupled in one container.** While accepted for MVP, this couples scaling (frontend and backend cannot be scaled independently) and complicates dependency management.

- **No multi-timeframe ML.** All 6 patterns only work on 5m candles. Multi-timeframe support was deferred throughout the project and never delivered — accepted trade-off given annotation costs.

---

## Planned Response

| Issue | Planned Action | Links |
|---|---|---|
| Anomaly detection not delivered | Document as known limitation in handover docs; future work if project continues post-course | — |
| Concurrency not tested | Add idempotency key or request deduplication if project moves to multi-user deployment | — |
| Container coupling | Separate frontend into nginx-based container in production architecture refactor | — |
| DT/DB accuracy (17-18% precision) | Danila to push improved training pipelines post-defense using refined labelling methodology | — |
| Multi-timeframe ML | Deferred — requires annotated datasets for each timeframe | — |
