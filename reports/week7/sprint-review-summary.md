# Sprint Review Summary — Sprint 6 (Assignment 6, Week 7)

---

**Date:** 2026-07-17
**Participants / Roles:** Nikolay Kuzmin (Customer), Andrei Alekseev (Customer), Fedor Kozhevnikov (Product Owner / Full-Stack), Danila Zhechev (Scrum Master / ML Engineer), Amir Gafarov (Backend Developer)
**Meeting type:** Sprint Review / Final Handover Review

---

## Sprint Goal Reviewed

Deliver MVP v3 — final course version with complete ML pattern detection, database persistence, UI polish, and reproducible deployment. ([Sprint 6 Milestone](https://github.com/Fedos113/SWP_TickFrame_28_team/milestone/7))

## Delivered Increment Discussed

| PBI | Issue | Status |
|---|---|---|
| ML pattern detection — Double Top / Double Bottom | — | Done — added DT/DB to existing HS/InHS pipeline; PR on new branch, backward-compatible API |
| Database integration — persist ML results in PostgreSQL | — | Done — all patterns saved in database; pre-analyzed on init, instant retrieval on user "Analyze" |
| UI overhaul — sidebar with coin search | — | Done — scalable coin addition with search |
| Indicators — fix overlapping, enable dragging | — | Done — now works correctly, similar to TradingView |
| Coin metrics — 5m/1h/4h changes, market cap, supply | — | Done — data from CoinGecko API + candle calculations |
| Pattern filtering — toggle on/off by type | — | Done — filter located next to patterns panel |
| PostgreSQL container in Docker Compose | — | Done — 3 containers: ML Service, TickFrame, PostgreSQL |
| Database schema and migrations | — | Done — tables created via startup migrations |
| Final VM deployment | — | Done — Final version is now available on VM |

## Addressed Customer Feedback (Sprint 5)

| Previous Feedback (Week 6) | How Addressed |
|---|---|
| Migrate SQLite → PostgreSQL 17 as dedicated container | Done — PostgreSQL 16 container included in Docker Compose with env-var credentials |
| Include all services in Docker Compose | Done — 3 containers: ML Service, TickFrame, PostgreSQL |
| Database credentials via environment variables | Done — configured via `.env` with `DB_HOST`, `DB_PORT`, etc. |
| Database migrations instead of app-created tables | Done — startup migrations initialize schema |
| Complete remaining 2 ML patterns (6 total) | Done — DT/DB added; 6 patterns operational (HS, InHS, DT, DB, Flags, Wedge) |
| Pattern-type filtering + confidence threshold controls | Done — toggle filter next to patterns panel |
| Additional coin metrics | Done — 5m/1h/4h change, market cap, supply via CoinGecko |
| Fix UI glitches (chart switching, element movement) | Done — indicators fixed, movable without overlap |
| Deploy updated version to VM | Done — Final version is now available on VM  |

## UAT Results

| Scenario | Result |
|---|---|
| UAT-001: Scan and view chart patterns | ✅ Pass — 6/6 patterns working; pre-analyzed in DB, instant retrieval |
| UAT-002: Toggle between chart timeframes | ⏳ Partial — switching works, but ML limited to 5m timeframe |
| UAT-003: Filter patterns by type | ✅ Pass — toggle filter next to patterns panel |
| UAT-004: Real-time price sidebar | ✅ Pass — WebSocket live prices continue working |
| UAT-005: Theme toggle | ✅ Pass — unchanged, still passing |
| UAT-006: WebSocket real-time candles | ✅ Pass — live updates from Bybit, DB cache fallback |
| UAT-007: Indicator sub-charts | ✅ Pass — indicators now movable without overlap |
| UAT-008: Configure pattern analysis range | ✅ Pass — slider with configurable range |
| UAT-009: Sidebar coin search and addition | ✅ Pass — infinite coin addition with search |
| UAT-010: Coin metrics (5m/1h/4h change, market cap, supply) | ✅ Pass — displayed from CoinGecko + candle calculations |

## Quality Evidence Discussed

- **Database Integration:** All ML patterns persisted in PostgreSQL before user init. 50,000 candles per coin pre-analyzed. On "Analyze" click, only unprocessed candles (≈50–150) are analyzed — takes ≈0.01s. First-time startup: ≈2–3 min for candle fetch (rate-limit safe) + ≈1 min for ML analysis. Subsequent startups instant due to DB persistence.
- **ML Pattern Detection:** 6 patterns operational (HS, InHS, DT, DB, Flags, Wedge). DT/DB added via separate branch with backward-compatible API. Recall ≈80%, precision ≈17–18% for DT/DB. All models trained on 5m timeframe only — multi-timeframe annotated data was unavailable within scope.
- **Anomaly Detection:** Dropped — complexity exceeded remaining sprint capacity. No public research or datasets available to build upon; team explored multiple approaches without viable results.
- **ML Architecture:** Separate microservice container; timestamp-based tracking of last analyzed candle stored in DB for incremental analysis.
- **Deployment:** Docker Compose starts 3 containers (ML Service, TickFrame, PostgreSQL). Backend + frontend served from single TickFrame container — acknowledged as non-standard but accepted for MVP scope. NPM availability in container identified as dependency issue during setup.
- **Concurrency:** Not explicitly tested for simultaneous "Analyze" clicks from multiple users. Team noted analysis is near-instant (sub-second) so race conditions are low-risk.

## Customer Feedback

**Positive:**
- Significant UI improvements — sidebar, indicators, metrics, filter all working well
- ML research and implementation praised — team worked without existing foundation or public research
- Project described as "cool" and "interesting" by team; customer acknowledged the learning value
- Overall direction and completeness satisfactory for course MVP
- Customer expressed openness to future collaboration and open-source contributions

**Critical:**
- Frontend + backend in same container is non-standard — acceptable for MVP but should be separated for production
- Container dependency management needs attention (NPM not pre-installed in container)
- Anomaly detection not delivered — customer acknowledged complexity but noted it was a PBI

**Requested:**
- Final version deployed to VM this evening for customer testing
- Higher-quality DT/DB training pipelines to be pushed to GitHub after course presentation
- Open-source contributions welcome post-course

## Approvals and Requested Changes

- Sprint increment approved as final course delivery
- Customer confirmed no further changes required before defense
- Team to deploy final version to VM and notify customer

## Remaining Gaps and Risks

- **Anomaly detection not delivered:** PBI dropped due to lack of research foundation and time constraints. Customer understood but noted the gap.
- **Single-timeframe ML:** Only 5m model available. Multi-timeframe deferred — accepted trade-off given annotation bottleneck.
- **Concurrency not stress-tested:** No locking mechanism validated for simultaneous "Analyze" clicks. Low risk given sub-second analysis time.
- **Container architecture:** Backend + frontend in single container; NPM dependency may cause setup friction. Not blocking for current deployment.
- **Defense readiness:** Team prepared with presentation; grades to date average ≈0.8 (80%).

## Action Points

| Action | Owner | Due |
|---|---|---|
| Deploy final version to VM | Fedor Kozhevnikov | 2026-07-17 (evening) |
| Notify customer once VM is updated | Fedor Kozhevnikov | 2026-07-17 |
| Push higher-quality DT/DB pipelines to GitHub post-defense | Danila Zhechev | After 2026-07-21 |
| Prepare and deliver course defense presentation | Team | 2026-07-21 |

## Product Backlog Updates

- **Anomaly detection PBI:** Removed from active scope — insufficient research foundation to deliver within sprint constraints
- **ML pipeline enhancement (DT/DB):** New PBI created for post-course quality improvements to training pipeline (Danila Zhechev, post-defense)
- **Container architecture refactor (backend/frontend separation):** Deferred — future work outside course scope
- **All other PBIs:** Closed as delivered in Sprint 6 final increment
