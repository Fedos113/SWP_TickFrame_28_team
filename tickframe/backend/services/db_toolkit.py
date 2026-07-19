from __future__ import annotations

import csv
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .database import DatabaseService

__all__ = [
    "get_db",
    "export_candles",
    "import_candles",
    "get_candle_range",
    "count_candles",
    "get_patterns",
    "list_all_scanned_symbols",
    "run_readonly_query",
    "clear_market_data",
]

DEFAULT_DATABASE_URL = "postgresql://tickframe:tickframe@postgres:5432/tickframe"

_SELECT_RE = re.compile(r"^\s*SELECT\b", re.IGNORECASE)


def _default_database_url() -> str:
    return os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)


async def get_db(database_url: str | None = None, use_sqlite: bool = False, db_path: str | Path | None = None) -> DatabaseService:
    db = DatabaseService(
        database_url=database_url or _default_database_url(),
        use_sqlite=use_sqlite,
        db_path=db_path,
    )
    await db.init()
    return db


async def export_candles(
    db: DatabaseService,
    symbol: str,
    interval: str,
    path: str | Path,
    fmt: str = "csv",
) -> int:
    candles = await db.load_candles(symbol, interval)
    path = Path(path)
    if fmt == "csv":
        with path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["time", "open", "high", "low", "close", "volume"])
            writer.writeheader()
            writer.writerows(candles)
    elif fmt == "json":
        with path.open("w") as f:
            json.dump(candles, f, indent=2)
    else:
        raise ValueError(f"Unsupported format: {fmt}")
    return len(candles)


async def import_candles(
    db: DatabaseService,
    symbol: str,
    interval: str,
    path: str | Path,
    fmt: str = "csv",
) -> dict[str, int]:
    path = Path(path)
    if fmt == "csv":
        with path.open(newline="") as f:
            reader = csv.DictReader(f)
            candles = []
            for row in reader:
                candles.append({
                    "time": int(row["time"]),
                    "open": float(row["open"]),
                    "high": float(row["high"]),
                    "low": float(row["low"]),
                    "close": float(row["close"]),
                    "volume": float(row.get("volume", 0)),
                })
    elif fmt == "json":
        with path.open() as f:
            raw = json.load(f)
        candles = raw
    else:
        raise ValueError(f"Unsupported format: {fmt}")

    total = len(candles)
    await db.save_candles(symbol, interval, candles)
    return {"rows_read": total, "rows_upserted": total}


async def get_candle_range(db: DatabaseService, symbol: str, interval: str) -> tuple[int, int] | None:
    return await db.get_candle_range(symbol, interval)


async def count_candles(db: DatabaseService, symbol: str, interval: str) -> int:
    return await db.count_candles(symbol, interval)


async def get_patterns(db: DatabaseService, symbol: str, interval: str = "5m", pretty: bool = False) -> dict | None:
    scan = await db.load_ml_scan(symbol, interval)
    if scan is None:
        return None
    if pretty and scan.get("patterns"):
        for p in scan["patterns"]:
            ts = p.get("timestamp", 0)
            try:
                p["datetime"] = datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
            except Exception:
                pass
    return scan


async def list_all_scanned_symbols(db: DatabaseService) -> list[str]:
    if db.use_sqlite:
        return await _list_all_scanned_symbols_sqlite(db)
    assert db._pool is not None
    async with db._pool.acquire() as conn:
        rows = await conn.fetch("SELECT symbol FROM ml_scans ORDER BY symbol")
        return [r["symbol"] for r in rows]


async def _list_all_scanned_symbols_sqlite(db: DatabaseService) -> list[str]:
    def _query() -> list[str]:
        with db._conn() as conn:
            rows = conn.execute("SELECT symbol FROM ml_scans ORDER BY symbol").fetchall()
            return [r["symbol"] for r in rows]
    import asyncio
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _query)


def _validate_readonly(sql: str) -> None:
    stripped = sql.strip()
    if not stripped:
        raise ValueError("Query must not be empty")
    if not _SELECT_RE.match(stripped):
        raise ValueError("Only SELECT queries are allowed (read-only guard)")
    dangerous = re.search(r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|CREATE|REPLACE|EXECUTE|CALL|MERGE)\b", stripped, re.IGNORECASE)
    if dangerous:
        raise ValueError(f"Read-only guard rejected query containing '{dangerous.group(1)}'")


async def run_readonly_query(db: DatabaseService, sql: str, *params: Any) -> list[dict[str, Any]]:
    _validate_readonly(sql)
    if db.use_sqlite:
        return await _run_readonly_query_sqlite(db, sql, *params)
    assert db._pool is not None
    async with db._pool.acquire() as conn:
        rows = await conn.fetch(sql, *params)
        return [dict(r) for r in rows]


async def clear_market_data(
    database_url: str | None = None,
    use_sqlite: bool = False,
    db_path: str | Path | None = None,
) -> None:
    """Delete all candle and ML scan data. Next request for each coin/interval
    will re-fetch fresh data from the exchange API."""
    from . import cache as cache_module

    db = await get_db(database_url=database_url, use_sqlite=use_sqlite, db_path=db_path)
    try:
        await db.clear_market_data()
    finally:
        await db.close()
    # Clear in-memory cache so next access fetches from exchange
    client = cache_module.BybitClient()
    cache = cache_module.MemoryMarketCache(client=client, db=None)
    cache.clear_cache()


async def _run_readonly_query_sqlite(db: DatabaseService, sql: str, *params: Any) -> list[dict[str, Any]]:
    import asyncio
    def _query() -> list[dict[str, Any]]:
        with db._conn() as conn:
            rows = conn.execute(sql, params).fetchall()
            return [dict(r) for r in rows]
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _query)
