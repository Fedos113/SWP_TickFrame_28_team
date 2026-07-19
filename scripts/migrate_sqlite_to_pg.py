from __future__ import annotations

import argparse
import asyncio
import os
import sqlite3
from pathlib import Path

import asyncpg

DEFAULT_SQLITE_PATH = Path(__file__).resolve().parent.parent / "tickframe" / "data" / "tickframe.db"

SCHEMA_PG = """
CREATE TABLE IF NOT EXISTS settings (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS drawings (
    id        BIGINT PRIMARY KEY,
    symbol    TEXT NOT NULL DEFAULT '',
    type      TEXT NOT NULL,
    points    TEXT NOT NULL,
    opts      TEXT NOT NULL DEFAULT '{}',
    selected  BIGINT NOT NULL DEFAULT 0,
    created   TEXT NOT NULL DEFAULT NOW()::TEXT
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
"""


def _sqlite_table_names(conn: sqlite3.Connection) -> set[str]:
    rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    return {r[0] for r in rows}


def _fetch_all(conn: sqlite3.Connection, table: str) -> list[sqlite3.Row]:
    return conn.execute(f"SELECT * FROM {table}").fetchall()


async def _migrate_settings(conn: sqlite3.Connection, pg: asyncpg.Connection) -> int:
    rows = _fetch_all(conn, "settings")
    records = [(r["key"], r["value"]) for r in rows]
    if records:
        await pg.executemany(
            "INSERT INTO settings (key, value) VALUES ($1, $2) "
            "ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value",
            records,
        )
    return len(records)


async def _migrate_drawings(conn: sqlite3.Connection, pg: asyncpg.Connection) -> int:
    rows = _fetch_all(conn, "drawings")
    records = [
        (r["id"], r["symbol"], r["type"], r["points"], r["opts"], r["selected"], r["created"])
        for r in rows
    ]
    if records:
        await pg.executemany(
            "INSERT INTO drawings (id, symbol, type, points, opts, selected, created) "
            "VALUES ($1, $2, $3, $4, $5, $6, $7) ON CONFLICT (id) DO NOTHING",
            records,
        )
    return len(records)


async def _migrate_drawings_blob(conn: sqlite3.Connection, pg: asyncpg.Connection) -> int:
    rows = _fetch_all(conn, "drawings_blob")
    records = [(r["symbol"], r["data"], r["updated"]) for r in rows]
    if records:
        await pg.executemany(
            "INSERT INTO drawings_blob (symbol, data, updated) VALUES ($1, $2, $3) "
            "ON CONFLICT (symbol) DO UPDATE SET data = EXCLUDED.data, updated = EXCLUDED.updated",
            records,
        )
    return len(records)


async def _migrate_toolbar_position(conn: sqlite3.Connection, pg: asyncpg.Connection) -> int:
    rows = _fetch_all(conn, "toolbar_position")
    records = [(r["id"], r["pos_left"], r["pos_top"]) for r in rows]
    if records:
        await pg.executemany(
            "INSERT INTO toolbar_position (id, pos_left, pos_top) VALUES ($1, $2, $3) "
            "ON CONFLICT (id) DO UPDATE SET pos_left = EXCLUDED.pos_left, pos_top = EXCLUDED.pos_top",
            records,
        )
    return len(records)


async def _migrate_coin_icons(conn: sqlite3.Connection, pg: asyncpg.Connection) -> int:
    rows = _fetch_all(conn, "coin_icons")
    records = [(r["symbol"], r["url"]) for r in rows]
    if records:
        await pg.executemany(
            "INSERT INTO coin_icons (symbol, url) VALUES ($1, $2) "
            "ON CONFLICT (symbol) DO UPDATE SET url = EXCLUDED.url",
            records,
        )
    return len(records)


async def _migrate_indicators_blob(conn: sqlite3.Connection, pg: asyncpg.Connection) -> int:
    rows = _fetch_all(conn, "indicators_blob")
    records = [(r["symbol"], r["data"], r["updated"]) for r in rows]
    if records:
        await pg.executemany(
            "INSERT INTO indicators_blob (symbol, data, updated) VALUES ($1, $2, $3) "
            "ON CONFLICT (symbol) DO UPDATE SET data = EXCLUDED.data, updated = EXCLUDED.updated",
            records,
        )
    return len(records)


async def _migrate_candles(conn: sqlite3.Connection, pg: asyncpg.Connection) -> int:
    rows = _fetch_all(conn, "candles")
    records = [
        (r["symbol"], r["interval"], r["time"], r["open"], r["high"], r["low"], r["close"], r["volume"], r["updated"])
        for r in rows
    ]
    if records:
        await pg.executemany(
            "INSERT INTO candles (symbol, interval, time, open, high, low, close, volume, updated) "
            "VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) "
            "ON CONFLICT (symbol, interval, time) DO UPDATE SET "
            "open = EXCLUDED.open, high = EXCLUDED.high, low = EXCLUDED.low, "
            "close = EXCLUDED.close, volume = EXCLUDED.volume, updated = EXCLUDED.updated",
            records,
        )
    return len(records)


MIGRATORS = {
    "settings": _migrate_settings,
    "drawings": _migrate_drawings,
    "drawings_blob": _migrate_drawings_blob,
    "toolbar_position": _migrate_toolbar_position,
    "coin_icons": _migrate_coin_icons,
    "indicators_blob": _migrate_indicators_blob,
    "candles": _migrate_candles,
}


async def migrate(sqlite_path: Path, database_url: str) -> None:
    conn = sqlite3.connect(str(sqlite_path))
    conn.row_factory = sqlite3.Row
    pg = await asyncpg.connect(database_url)
    try:
        await pg.execute(SCHEMA_PG)
        existing = _sqlite_table_names(conn)
        for table, migrator in MIGRATORS.items():
            if table not in existing:
                print(f"Skipping {table}: not present in SQLite database")
                continue
            count = await migrator(conn, pg)
            print(f"Migrated {count} rows from {table}")
    finally:
        conn.close()
        await pg.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Migrate TickFrame SQLite data to PostgreSQL")
    parser.add_argument("--sqlite", default=str(DEFAULT_SQLITE_PATH), help="Path to source SQLite database")
    parser.add_argument(
        "--database-url",
        default=os.environ.get("DATABASE_URL", "postgresql://tickframe:tickframe@localhost:5432/tickframe"),
        help="Target PostgreSQL connection URL",
    )
    args = parser.parse_args()

    sqlite_path = Path(args.sqlite)
    if not sqlite_path.exists():
        raise SystemExit(f"SQLite database not found: {sqlite_path}")

    asyncio.run(migrate(sqlite_path, args.database_url))


if __name__ == "__main__":
    main()
