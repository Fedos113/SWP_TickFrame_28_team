# Database Quick Guide

Quick reference for developers who need to interact with the TickFrame PostgreSQL database — whether through the CLI toolkit, REST admin endpoints, or direct Python calls.

---

## 1. Connection

### Default (Docker internal)

```
DATABASE_URL=postgresql://tickframe:tickframe@postgres:5432/tickframe
```

### From host machine

1. Add port mapping to `docker-compose.yml` under the `postgres` service:
   ```yaml
   ports:
     - "5432:5432"
   ```
2. Restart: `docker compose up -d`
3. Connect using:
   ```
   DATABASE_URL=postgresql://tickframe:tickframe@localhost:5432/tickframe
   ```

### SQLite fallback (for local dev / tests)

```bash
# The toolkit auto-detects via DatabaseService — no extra config needed.
# Use --sqlite flag with CLI commands to run against a local SQLite file.
```

---

## 2. CLI Toolkit

All commands use `python -m tickframe db <command>`.

```bash
# Show candle time range and count for a symbol/interval
python -m tickframe db candle-range BTCUSDT 5m

# Export candles to CSV file
python -m tickframe db export-candles BTCUSDT 5m --out btc_5m.csv

# Export candles to JSON
python -m tickframe db export-candles BTCUSDT 5m --out btc_5m.json --format json

# Import candles from CSV file (upserts on symbol+interval+time conflict)
python -m tickframe db import-candles BTCUSDT 5m --infile btc_5m.csv

# View ML scan patterns for a symbol
python -m tickframe db patterns BTCUSDT

# View patterns with human-readable timestamps
python -m tickframe db patterns BTCUSDT --pretty

# List patterns for ALL scanned symbols
python -m tickframe db patterns "*"

# Run an ad-hoc read-only SQL query
python -m tickframe db query "SELECT symbol, COUNT(*) as cnt FROM candles GROUP BY symbol ORDER BY cnt DESC"

# All commands accept --sqlite for local SQLite fallback
python -m tickframe db candle-range BTCUSDT 5m --sqlite
```

---

## 3. Python API

```python
import asyncio
from tickframe.backend.services.db_toolkit import get_db, export_candles, get_patterns, run_readonly_query

async def main():
    # Connect (reads DATABASE_URL from env)
    db = await get_db()

    try:
        # Load candles directly (wraps DatabaseService methods)
        candles = await db.load_last_n_candles("BTCUSDT", "5m", 500)
        print(f"Loaded {len(candles)} candles")

        # Export to file
        count = await export_candles(db, "BTCUSDT", "5m", "export.csv")
        print(f"Exported {count} candles")

        # Get ML scan results
        scan = await get_patterns(db, "BTCUSDT", pretty=True)
        if scan:
            print(f"Patterns: {scan['patterns']}")

        # Run a read-only query
        rows = await run_readonly_query(
            db,
            "SELECT symbol, COUNT(*) as cnt FROM candles WHERE interval = $1 GROUP BY symbol",
            "5m",
        )
        for row in rows:
            print(f"{row['symbol']}: {row['cnt']} candles")

        # Candle range / count
        rng = await db.get_candle_range("BTCUSDT", "5m")
        cnt = await db.count_candles("BTCUSDT", "5m")
        print(f"Range: {rng}, Count: {cnt}")

    finally:
        await db.close()

asyncio.run(main())
```

---

## 4. REST Admin Endpoints (dev-only)

Enable with environment variable: `ENABLE_DB_ADMIN_API=true`

```bash
# Export candles as CSV
curl -o btc_5m.csv "http://localhost:8080/api/admin/db/candles/BTCUSDT/export?interval=5m&format=csv"

# Export candles as JSON
curl -o btc_5m.json "http://localhost:8080/api/admin/db/candles/BTCUSDT/export?interval=5m&format=json"

# Import candles from CSV (multipart upload)
curl -X POST -F "file=@btc_5m.csv" "http://localhost:8080/api/admin/db/candles/BTCUSDT/import?interval=5m"

# Get ML scan patterns (includes raw ml_scans row)
curl "http://localhost:8080/api/admin/db/patterns/BTCUSDT"
```

---

## 5. Schema Reference

See [`assignments/7/architecture.md`](../assignments/7/architecture.md) §6 for full table definitions.

| Table | Primary Key | Contents |
|---|---|---|
| `candles` | `(symbol, interval, time)` | OHLCV price data |
| `settings` | `key` | Key-value app settings |
| `drawings_blob` | `symbol` | Chart drawings as JSON blob |
| `indicators_blob` | `symbol` | Technical indicator configs as JSON blob |
| `toolbar_position` | `id` (singleton) | Drawing toolbar position |
| `coin_icons` | `symbol` | Cryptocurrency icon URLs |
| `ml_scans` | `symbol` | ML pattern detection results |

---

## 6. Gotchas

- **Candle PK is `(symbol, interval, time)`** — imports upsert on conflict; no duplicates.
- **`MAX_CANDLES = 55000`** per `(symbol, interval)` — `cache.py` trims beyond this, but direct DB writes can exceed it. The toolkit does **not** enforce the cap.
- **`ml_scans`** is one row per symbol (latest scan only, not historical). Re-scanning overwrites.
- **Read-only guard** — `run_readonly_query` and the CLI `db query` command reject any non-`SELECT` SQL statement.
- **CSV format** — columns: `time,open,high,low,close,volume`. Symbol and interval are in the filename/args, not per-row.
- **SQLite fallback** — unit tests use this; no Docker/PostgreSQL needed for local testing.
