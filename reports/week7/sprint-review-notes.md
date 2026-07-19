# Sprint Review Notes — Sprint 6 (Week 7)

## Meeting Info
- **Duration:** ~28 minutes
- **Type:** Sprint Review / Final Handover
- **Attendees:** Nikolay Kuzmin, Andrei Alekseev (Customers), Fedor Kozhevnikov (PO), Danila Zhechev (SM/ML), Amir Gafarov (Backend)

---

## 1. Deployment Status (00:00:20)
- VM not yet updated; latest version on GitHub
- Fedor to deploy final version same evening
- Demo running from Amir's local machine

## 2. Database & ML Integration (00:02:00)
- All 10 coins pre-analyzed before project initialization
- ML results persisted in PostgreSQL — instant retrieval on "Analyze" click
- Unprocessed candles (≈50–150) analyzed on-demand in ≈0.01s
- Timestamp-based tracking of last analyzed candle stored in DB

### Concurrency Discussion (00:03:00–00:06:15)
- Customer pressed on concurrent "Analyze" clicks from multiple users
- Team: analysis is near-instant, not explicitly stress-tested
- Customer concerned about race conditions; team acknowledged gap
- Pattern table schema stored in PostgreSQL; team demonstrated via container

### Data Flow (00:10:20–00:11:45)
- Initial startup: fetch 50K candles per coin from Bybit API (2–3 min)
- Then ML pre-analysis (≈1 min)
- Subsequent starts: instant — data already in DB
- WebSocket updates latest candles in real-time

## 3. New Features Demo (00:14:00–00:15:30)
- **Sidebar:** Add unlimited coins with search
- **Indicators:** Fixed overlap bug — now draggable like TradingView
- **Metrics:** 5m/1h/4h price change, market cap, supply (CoinGecko + candle calc)
- **Filter:** Toggle patterns on/off, located next to patterns panel

## 4. ML Update — Danila Zhechev (00:16:15)
- Double Top / Double Bottom patterns added via separate PR
- Backward-compatible API; integrates with existing HS/InHS pipeline
- **Accuracy:** Recall ≈80%, Precision ≈17–18% for DT/DB
- New models require only backend integration code — API unchanged
- Anomaly detection dropped: no public research/datasets to build on, time constraints

## 5. Container Setup Discussion (00:18:05–00:19:55)
- 3 Docker containers: ML Service, TickFrame, PostgreSQL
- TickFrame container serves both backend (FastAPI) and frontend (esbuild bundle)
- NPM not pre-installed in container — dependency issue flagged
- Andrei: non-standard practice but acceptable for MVP

## 6. Defense & Grading (00:22:05)
- Defense: Tuesday 2026-07-21, before 3 TAs
- Team prepared with presentation
- Grades to date: mostly 0.8 (80%), one 100%
- Marks reduced for documentation — customer acknowledged strict grading

## 7. Outstanding PBIs (00:24:20)
- Anomaly detection: dropped — lack of research foundation
- Team confirmed all other customer requests addressed

## 8. Team Reflections (00:25:45)
- Fedor: learned useful charting libraries, enjoyed project
- Danila: positive ML experience, worked without existing research to reference
- Customer: open to post-course collaboration and open-source contributions
- Danila to push improved DT/DB pipelines after defense

## 9. Key Decisions
- Final version deployed to VM same evening
- No further changes required before defense
- Higher-quality ML pipelines to be shared post-course (open-source)
- Container architecture (backend+frontend together) accepted as MVP compromise
