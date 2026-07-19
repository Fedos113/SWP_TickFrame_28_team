from __future__ import annotations

import asyncio
import json
import os
import sqlite3
from pathlib import Path

import asyncpg  # type: ignore[import-untyped]

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DB_PATH = DATA_DIR / "tickframe.db"

DEFAULT_DATABASE_URL = "postgresql://tickframe:tickframe@postgres:5432/tickframe"

SCHEMA_PG = """
CREATE TABLE IF NOT EXISTS settings (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS drawings_blob (
    symbol  TEXT PRIMARY KEY,
    data    TEXT NOT NULL,
    updated TEXT NOT NULL DEFAULT NOW()::TEXT
);
CREATE TABLE IF NOT EXISTS toolbar_position (
    id        BIGINT PRIMARY KEY DEFAULT 1 CHECK (id = 1),
    pos_left  BIGINT NOT NULL DEFAULT 16,
    pos_top   BIGINT NOT NULL DEFAULT 40
);
CREATE TABLE IF NOT EXISTS coin_icons (
    symbol  TEXT PRIMARY KEY,
    url     TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS indicators_blob (
    symbol  TEXT PRIMARY KEY,
    data    TEXT NOT NULL,
    updated TEXT NOT NULL DEFAULT NOW()::TEXT
);
CREATE TABLE IF NOT EXISTS candles (
    symbol    TEXT NOT NULL,
    interval  TEXT NOT NULL,
    time      BIGINT NOT NULL,
    open      DOUBLE PRECISION NOT NULL,
    high      DOUBLE PRECISION NOT NULL,
    low       DOUBLE PRECISION NOT NULL,
    close     DOUBLE PRECISION NOT NULL,
    volume    DOUBLE PRECISION NOT NULL DEFAULT 0,
    updated   TEXT NOT NULL DEFAULT NOW()::TEXT,
    PRIMARY KEY (symbol, interval, time)
);
CREATE TABLE IF NOT EXISTS ml_scans (
    symbol   TEXT NOT NULL,
    interval TEXT NOT NULL,
    last_scanned_time BIGINT NOT NULL DEFAULT 0,
    patterns TEXT NOT NULL DEFAULT '[]',
    updated  TEXT NOT NULL DEFAULT NOW()::TEXT,
    PRIMARY KEY (symbol, interval)
);
"""

SCHEMA_SQLITE = """
CREATE TABLE IF NOT EXISTS settings (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS drawings (
    id        INTEGER PRIMARY KEY,
    symbol    TEXT NOT NULL DEFAULT '',
    type      TEXT NOT NULL,
    points    TEXT NOT NULL,
    opts      TEXT NOT NULL DEFAULT '{}',
    selected  INTEGER NOT NULL DEFAULT 0,
    created   TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS drawings_blob (
    symbol TEXT PRIMARY KEY,
    data   TEXT NOT NULL,
    updated TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS toolbar_position (
    id        INTEGER PRIMARY KEY DEFAULT 1 CHECK (id = 1),
    pos_left  INTEGER NOT NULL DEFAULT 16,
    pos_top   INTEGER NOT NULL DEFAULT 40
);
INSERT INTO toolbar_position (id, pos_left, pos_top) VALUES (1, 16, 40)
    ON CONFLICT(id) DO NOTHING;
CREATE TABLE IF NOT EXISTS coin_icons (
    symbol  TEXT PRIMARY KEY,
    url     TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS indicators_blob (
    symbol  TEXT PRIMARY KEY,
    data    TEXT NOT NULL,
    updated TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS candles (
    symbol    TEXT NOT NULL,
    interval  TEXT NOT NULL,
    time      INTEGER NOT NULL,
    open      REAL NOT NULL,
    high      REAL NOT NULL,
    low       REAL NOT NULL,
    close     REAL NOT NULL,
    volume    REAL NOT NULL DEFAULT 0,
    updated   TEXT NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (symbol, interval, time)
);
CREATE TABLE IF NOT EXISTS ml_scans (
    symbol   TEXT NOT NULL,
    interval TEXT NOT NULL,
    last_scanned_time INTEGER NOT NULL DEFAULT 0,
    patterns TEXT NOT NULL DEFAULT '[]',
    updated  TEXT NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (symbol, interval)
);
"""


class DatabaseService:
    def __init__(self, database_url: str | None = None, use_sqlite: bool = False, db_path: str | Path | None = None):
        self.use_sqlite = use_sqlite
        self._pool: asyncpg.Pool | None = None
        if use_sqlite:
            self._db = str(db_path or DB_PATH)
            DATA_DIR.mkdir(parents=True, exist_ok=True)
        else:
            self._database_url = database_url or os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)

    async def init(self) -> None:
        if self.use_sqlite:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self._init_tables_sqlite)
            return
        self._pool = await asyncpg.create_pool(self._database_url)
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            await conn.execute(SCHEMA_PG)
            await self._migrate_pg(conn)
            await conn.execute(
                "INSERT INTO toolbar_position (id, pos_left, pos_top) VALUES (1, 16, 40) "
                "ON CONFLICT (id) DO NOTHING"
            )

    @staticmethod
    async def _migrate_pg(conn: asyncpg.Connection) -> None:
        """Idempotent migrations for databases created from an older schema.

        `CREATE TABLE IF NOT EXISTS` does not add a missing PRIMARY KEY to an
        already-existing table. Older `ml_scans` tables were created without the
        `(symbol, interval)` primary key, which makes the `ON CONFLICT
        (symbol, interval)` upsert in `save_ml_scan` fail. Ensure the constraint
        exists (de-duplicating any pre-existing rows first).
        """
        await conn.execute(
            """
            DO $$
            DECLARE
                pk_cols text;
            BEGIN
                SELECT string_agg(a.attname, ',' ORDER BY array_position(c.conkey, a.attnum))
                INTO pk_cols
                FROM pg_constraint c
                JOIN pg_attribute a
                     ON a.attrelid = c.conrelid AND a.attnum = ANY(c.conkey)
                WHERE c.conrelid = 'ml_scans'::regclass AND c.contype = 'p';

                -- Older schemas created the primary key on `symbol` only (or with
                -- some other shape), which breaks `ON CONFLICT (symbol, interval)`.
                -- Rebuild the PK on (symbol, interval) whenever it is not already so.
                IF pk_cols IS DISTINCT FROM 'symbol,interval' THEN
                    -- Drop the existing primary key (if any).
                    IF pk_cols IS NOT NULL THEN
                        EXECUTE 'ALTER TABLE ml_scans DROP CONSTRAINT '
                                || (SELECT conname FROM pg_constraint
                                    WHERE conrelid = 'ml_scans'::regclass AND contype = 'p');
                    END IF;
                    -- Remove duplicate (symbol, interval) rows, keeping the newest.
                    DELETE FROM ml_scans a USING ml_scans b
                    WHERE a.ctid < b.ctid
                      AND a.symbol = b.symbol
                      AND a.interval = b.interval;
                    ALTER TABLE ml_scans
                        ADD CONSTRAINT ml_scans_pkey PRIMARY KEY (symbol, interval);
                END IF;
            END
            $$;
            """
        )



    async def close(self) -> None:
        if self._pool is not None:
            await self._pool.close()
            self._pool = None

    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db, timeout=30.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_tables_sqlite(self) -> None:
        with self._conn() as conn:
            conn.executescript(SCHEMA_SQLITE)
            cols = [r[1] for r in conn.execute("PRAGMA table_info(drawings)").fetchall()]
            if "symbol" not in cols:
                conn.execute("ALTER TABLE drawings ADD COLUMN symbol TEXT NOT NULL DEFAULT ''")

    # --- Settings ---

    def _get_setting_sqlite(self, key: str) -> str | None:
        with self._conn() as conn:
            row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
            return row["value"] if row else None

    def _set_setting_sqlite(self, key: str, value: str) -> None:
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (key, value),
            )

    def _all_settings_sqlite(self) -> dict[str, str]:
        with self._conn() as conn:
            rows = conn.execute("SELECT key, value FROM settings").fetchall()
            return {r["key"]: r["value"] for r in rows}

    async def get_setting(self, key: str) -> str | None:
        if self.use_sqlite:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, self._get_setting_sqlite, key)
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow("SELECT value FROM settings WHERE key = $1", key)
            return row["value"] if row else None

    async def set_setting(self, key: str, value: str) -> None:
        if self.use_sqlite:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self._set_setting_sqlite, key, value)
            return
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO settings (key, value) VALUES ($1, $2) ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value",
                key,
                value,
            )

    async def get_all_settings(self) -> dict[str, str]:
        if self.use_sqlite:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, self._all_settings_sqlite)
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            rows = await conn.fetch("SELECT key, value FROM settings")
            return {r["key"]: r["value"] for r in rows}

    # --- Toolbar Position ---

    def _save_toolbar_position_sqlite(self, left: int, top: int) -> None:
        with self._conn() as conn:
            conn.execute(
                "UPDATE toolbar_position SET pos_left = ?, pos_top = ? WHERE id = 1",
                (left, top),
            )

    def _load_toolbar_position_sqlite(self) -> dict | None:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT pos_left, pos_top FROM toolbar_position WHERE id = 1"
            ).fetchone()
            if row:
                return {"left": row["pos_left"], "top": row["pos_top"]}
            return None

    async def save_toolbar_position(self, left: int, top: int) -> None:
        if self.use_sqlite:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self._save_toolbar_position_sqlite, left, top)
            return
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            await conn.execute(
                "UPDATE toolbar_position SET pos_left = $1, pos_top = $2 WHERE id = 1",
                left,
                top,
            )

    async def load_toolbar_position(self) -> dict | None:
        if self.use_sqlite:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, self._load_toolbar_position_sqlite)
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow("SELECT pos_left, pos_top FROM toolbar_position WHERE id = 1")
            if row:
                return {"left": row["pos_left"], "top": row["pos_top"]}
            return None

    # --- Coin Icons ---

    def _save_coin_icons_sqlite(self, icons: dict[str, str]) -> None:
        with self._conn() as conn:
            conn.execute("BEGIN")
            for sym, url in icons.items():
                conn.execute(
                    "INSERT INTO coin_icons (symbol, url) VALUES (?, ?) ON CONFLICT(symbol) DO UPDATE SET url = excluded.url",
                    (sym, url),
                )
            conn.execute("COMMIT")

    def _load_coin_icons_sqlite(self) -> dict[str, str]:
        with self._conn() as conn:
            rows = conn.execute("SELECT symbol, url FROM coin_icons").fetchall()
            return {r["symbol"]: r["url"] for r in rows}

    async def save_coin_icons(self, icons: dict[str, str]) -> None:
        if not icons:
            return
        if self.use_sqlite:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self._save_coin_icons_sqlite, icons)
            return
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            await conn.executemany(
                "INSERT INTO coin_icons (symbol, url) VALUES ($1, $2) ON CONFLICT (symbol) DO UPDATE SET url = EXCLUDED.url",
                list(icons.items()),
            )

    async def load_coin_icons(self) -> dict[str, str]:
        if self.use_sqlite:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, self._load_coin_icons_sqlite)
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            rows = await conn.fetch("SELECT symbol, url FROM coin_icons")
            return {r["symbol"]: r["url"] for r in rows}

    # --- Drawings (legacy sqlite-only) ---

    def _load_drawings_sqlite(self, symbol: str) -> list[dict]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT id, type, points, opts FROM drawings WHERE symbol = ? ORDER BY id",
                (symbol,),
            ).fetchall()
            result = []
            for r in rows:
                pts = json.loads(r["points"])
                d = {"id": r["id"], "type": r["type"], "points": pts}
                d["opts"] = json.loads(r["opts"])
                result.append(d)
            return result

    def _save_drawings_sqlite(self, symbol: str, drawings: list[dict]) -> None:
        with self._conn() as conn:
            conn.execute("DELETE FROM drawings WHERE symbol = ?", (symbol,))
            for d in drawings:
                conn.execute(
                    "INSERT INTO drawings (id, symbol, type, points, opts) VALUES (?, ?, ?, ?, ?)",
                    (d["id"], symbol, d["type"], json.dumps(d["points"]), json.dumps(d.get("opts", {}))),
                )

    async def load_drawings(self, symbol: str) -> list[dict]:
        if self.use_sqlite:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, self._load_drawings_sqlite, symbol)
        return []

    async def save_drawings(self, symbol: str, drawings: list[dict]) -> None:
        if self.use_sqlite:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self._save_drawings_sqlite, symbol, drawings)

    # --- Drawings Blob ---

    def _save_drawings_blob_sqlite(self, symbol: str, serialized: str) -> None:
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO drawings_blob (symbol, data, updated) VALUES (?, ?, datetime('now')) "
                "ON CONFLICT(symbol) DO UPDATE SET data = excluded.data, updated = excluded.updated",
                (symbol, serialized),
            )

    def _load_drawings_blob_sqlite(self, symbol: str) -> list | dict | None:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT data FROM drawings_blob WHERE symbol = ?", (symbol,)
            ).fetchone()
            if row:
                return json.loads(row["data"])
            return None

    async def save_drawings_blob(self, symbol: str, data: list | dict | str) -> None:
        serialized = json.dumps(data) if not isinstance(data, str) else data
        if self.use_sqlite:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self._save_drawings_blob_sqlite, symbol, serialized)
            return
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO drawings_blob (symbol, data, updated) VALUES ($1, $2, NOW()::TEXT) "
                "ON CONFLICT (symbol) DO UPDATE SET data = EXCLUDED.data, updated = EXCLUDED.updated",
                symbol,
                serialized,
            )

    async def load_drawings_blob(self, symbol: str) -> list | dict | None:
        if self.use_sqlite:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, self._load_drawings_blob_sqlite, symbol)
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow("SELECT data FROM drawings_blob WHERE symbol = $1", symbol)
            if row:
                return json.loads(row["data"])
            return None

    # --- Indicators ---

    def _save_indicators_sqlite(self, symbol: str, serialized: str) -> None:
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO indicators_blob (symbol, data, updated) VALUES (?, ?, datetime('now')) "
                "ON CONFLICT(symbol) DO UPDATE SET data = excluded.data, updated = excluded.updated",
                (symbol, serialized),
            )

    def _load_indicators_sqlite(self, symbol: str) -> list | dict | None:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT data FROM indicators_blob WHERE symbol = ?", (symbol,)
            ).fetchone()
            if row:
                return json.loads(row["data"])
            return None

    async def save_indicators(self, symbol: str, data: list | dict | str) -> None:
        serialized = json.dumps(data) if not isinstance(data, str) else data
        if self.use_sqlite:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self._save_indicators_sqlite, symbol, serialized)
            return
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO indicators_blob (symbol, data, updated) VALUES ($1, $2, NOW()::TEXT) "
                "ON CONFLICT (symbol) DO UPDATE SET data = EXCLUDED.data, updated = EXCLUDED.updated",
                symbol,
                serialized,
            )

    async def load_indicators(self, symbol: str) -> list | dict | None:
        if self.use_sqlite:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, self._load_indicators_sqlite, symbol)
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow("SELECT data FROM indicators_blob WHERE symbol = $1", symbol)
            if row:
                return json.loads(row["data"])
            return None

    # --- Candles ---

    def _save_candles_sqlite(self, symbol: str, interval: str, candles: list[dict]) -> None:
        with self._conn() as conn:
            conn.execute("BEGIN")
            conn.executemany(
                """INSERT OR REPLACE INTO candles (symbol, interval, time, open, high, low, close, volume, updated)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))""",
                [
                    (symbol, interval, c["time"], c["open"], c["high"], c["low"], c["close"], c.get("volume", 0))
                    for c in candles
                ],
            )
            conn.execute("COMMIT")

    def _load_candles_sqlite(self, symbol: str, interval: str) -> list[dict]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT time, open, high, low, close, volume FROM candles WHERE symbol = ? AND interval = ? ORDER BY time",
                (symbol, interval),
            ).fetchall()
            return [dict(r) for r in rows]

    def _load_last_n_candles_sqlite(self, symbol: str, interval: str, n: int) -> list[dict]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT time, open, high, low, close, volume FROM candles WHERE symbol = ? AND interval = ? ORDER BY time DESC LIMIT ?",
                (symbol, interval, n),
            ).fetchall()
            return [dict(r) for r in reversed(rows)]

    def _load_candles_before_sqlite(self, symbol: str, interval: str, n: int, before: int) -> list[dict]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT time, open, high, low, close, volume FROM candles WHERE symbol = ? AND interval = ? AND time < ? ORDER BY time DESC LIMIT ?",
                (symbol, interval, before, n),
            ).fetchall()
            return [dict(r) for r in reversed(rows)]

    def _get_candle_range_sqlite(self, symbol: str, interval: str) -> tuple[int, int] | None:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT MIN(time), MAX(time) FROM candles WHERE symbol = ? AND interval = ?",
                (symbol, interval),
            ).fetchone()
            if row and row[0] is not None:
                return (int(row[0]), int(row[1]))
            return None

    def _count_candles_sqlite(self, symbol: str, interval: str) -> int:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT COUNT(*) AS cnt FROM candles WHERE symbol = ? AND interval = ?",
                (symbol, interval),
            ).fetchone()
            return row["cnt"] if row else 0

    async def save_candles(self, symbol: str, interval: str, candles: list[dict]) -> None:
        if not candles:
            return
        if self.use_sqlite:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self._save_candles_sqlite, symbol, interval, candles)
            return
        assert self._pool is not None
        records = [
            (symbol, interval, c["time"], c["open"], c["high"], c["low"], c["close"], c.get("volume", 0))
            for c in candles
        ]
        async with self._pool.acquire() as conn:
            await conn.executemany(
                """INSERT INTO candles (symbol, interval, time, open, high, low, close, volume, updated)
                   VALUES ($1, $2, $3, $4, $5, $6, $7, $8, NOW()::TEXT)
                   ON CONFLICT (symbol, interval, time) DO UPDATE SET
                       open = EXCLUDED.open, high = EXCLUDED.high, low = EXCLUDED.low,
                       close = EXCLUDED.close, volume = EXCLUDED.volume, updated = EXCLUDED.updated""",
                records,
            )

    async def load_candles(self, symbol: str, interval: str) -> list[dict]:
        if self.use_sqlite:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, self._load_candles_sqlite, symbol, interval)
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT time, open, high, low, close, volume FROM candles WHERE symbol = $1 AND interval = $2 ORDER BY time",
                symbol,
                interval,
            )
            return [dict(r) for r in rows]

    async def load_last_n_candles(self, symbol: str, interval: str, n: int) -> list[dict]:
        if self.use_sqlite:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, self._load_last_n_candles_sqlite, symbol, interval, n)
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT time, open, high, low, close, volume FROM candles WHERE symbol = $1 AND interval = $2 ORDER BY time DESC LIMIT $3",
                symbol,
                interval,
                n,
            )
            return [dict(r) for r in reversed(rows)]

    async def load_candles_before(self, symbol: str, interval: str, n: int, before: int) -> list[dict]:
        if self.use_sqlite:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, self._load_candles_before_sqlite, symbol, interval, n, before)
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT time, open, high, low, close, volume FROM candles WHERE symbol = $1 AND interval = $2 AND time < $3 ORDER BY time DESC LIMIT $4",
                symbol,
                interval,
                before,
                n,
            )
            return [dict(r) for r in reversed(rows)]

    async def get_candle_range(self, symbol: str, interval: str) -> tuple[int, int] | None:
        if self.use_sqlite:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, self._get_candle_range_sqlite, symbol, interval)
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT MIN(time) AS lo, MAX(time) AS hi FROM candles WHERE symbol = $1 AND interval = $2",
                symbol,
                interval,
            )
            if row and row["lo"] is not None:
                return (int(row["lo"]), int(row["hi"]))
            return None

    async def clear_drawings(self) -> None:
        if self.use_sqlite:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, self._clear_drawings_sqlite)
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            await conn.execute("DELETE FROM drawings_blob")

    def _clear_drawings_sqlite(self) -> None:
        with self._conn() as conn:
            conn.execute("DELETE FROM drawings")
            conn.execute("DELETE FROM drawings_blob")

    async def clear_market_data(self) -> None:
        """Delete all volatile market data (candles + ML scans).
        The cache will re-fetch fresh data from the exchange on next request."""
        if self.use_sqlite:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, self._clear_market_data_sqlite)
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            await conn.execute("DELETE FROM candles")
            await conn.execute("DELETE FROM ml_scans")

    def _clear_market_data_sqlite(self) -> None:
        with self._conn() as conn:
            conn.execute("DELETE FROM candles")
            conn.execute("DELETE FROM ml_scans")

    async def count_candles(self, symbol: str, interval: str) -> int:
        if self.use_sqlite:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, self._count_candles_sqlite, symbol, interval)
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT COUNT(*) AS cnt FROM candles WHERE symbol = $1 AND interval = $2",
                symbol,
                interval,
            )
            return int(row["cnt"]) if row else 0

    # --- ML Scans ---

    def _save_ml_scan_sqlite(self, symbol: str, interval: str, last_scanned_time: int, patterns: list) -> None:
        serialized = json.dumps(patterns)
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO ml_scans (symbol, interval, last_scanned_time, patterns, updated) "
                "VALUES (?, ?, ?, ?, datetime('now')) "
                "ON CONFLICT(symbol, interval) DO UPDATE SET "
                "last_scanned_time = excluded.last_scanned_time, "
                "patterns = excluded.patterns, updated = excluded.updated",
                (symbol, interval, last_scanned_time, serialized),
            )

    def _load_ml_scan_sqlite(self, symbol: str, interval: str) -> dict | None:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT symbol, interval, last_scanned_time, patterns FROM ml_scans WHERE symbol = ? AND interval = ?",
                (symbol, interval),
            ).fetchone()
            if row:
                return {
                    "symbol": row["symbol"],
                    "interval": row["interval"],
                    "last_scanned_time": row["last_scanned_time"],
                    "patterns": json.loads(row["patterns"]),
                }
            return None

    def _load_candles_after_sqlite(self, symbol: str, interval: str, after_time: int) -> list[dict]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT time, open, high, low, close, volume FROM candles "
                "WHERE symbol = ? AND interval = ? AND time > ? ORDER BY time",
                (symbol, interval, after_time),
            ).fetchall()
            return [dict(r) for r in rows]

    async def save_ml_scan(self, symbol: str, interval: str, last_scanned_time: int, patterns: list) -> None:
        if self.use_sqlite:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self._save_ml_scan_sqlite, symbol, interval, last_scanned_time, patterns)
            return
        assert self._pool is not None
        serialized = json.dumps(patterns)
        async with self._pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO ml_scans (symbol, interval, last_scanned_time, patterns, updated) "
                "VALUES ($1, $2, $3, $4, NOW()::TEXT) "
                "ON CONFLICT (symbol, interval) DO UPDATE SET "
                "last_scanned_time = EXCLUDED.last_scanned_time, "
                "patterns = EXCLUDED.patterns, updated = EXCLUDED.updated",
                symbol, interval, last_scanned_time, serialized,
            )

    async def load_ml_scan(self, symbol: str, interval: str) -> dict | None:
        if self.use_sqlite:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, self._load_ml_scan_sqlite, symbol, interval)
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT symbol, interval, last_scanned_time, patterns FROM ml_scans WHERE symbol = $1 AND interval = $2",
                symbol, interval,
            )
            if row:
                return {
                    "symbol": row["symbol"],
                    "interval": row["interval"],
                    "last_scanned_time": row["last_scanned_time"],
                    "patterns": json.loads(row["patterns"]),
                }
            return None

    async def load_candles_after(self, symbol: str, interval: str, after_time: int) -> list[dict]:
        if self.use_sqlite:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, self._load_candles_after_sqlite, symbol, interval, after_time)
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT time, open, high, low, close, volume FROM candles "
                "WHERE symbol = $1 AND interval = $2 AND time > $3 ORDER BY time",
                symbol, interval, after_time,
            )
            return [dict(r) for r in rows]

