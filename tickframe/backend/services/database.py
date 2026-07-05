from __future__ import annotations

import json
import sqlite3
import threading
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DB_PATH = DATA_DIR / "tickframe.db"


class DatabaseService:
    def __init__(self, db_path: str | Path | None = None):
        self._db = str(db_path or DB_PATH)
        self._lock = threading.RLock()
        self._conn_cache: sqlite3.Connection | None = None
        db_parent = Path(self._db).parent
        db_parent.mkdir(parents=True, exist_ok=True)

    def _conn(self) -> sqlite3.Connection:
        with self._lock:
            if self._conn_cache is None:
                conn = sqlite3.connect(self._db)
                conn.row_factory = sqlite3.Row
                conn.execute("PRAGMA journal_mode = DELETE")
                conn.execute("PRAGMA synchronous = NORMAL")
                self._conn_cache = conn
            return self._conn_cache

    def _init_tables(self) -> None:
        with self._conn() as conn:
            conn.executescript("""
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
                pos_top   INTEGER NOT NULL DEFAULT 12
            );
            INSERT INTO toolbar_position (id, pos_left, pos_top) VALUES (1, 16, 12)
                ON CONFLICT(id) DO NOTHING;
            CREATE TABLE IF NOT EXISTS coin_icons (
                symbol  TEXT PRIMARY KEY,
                url     TEXT NOT NULL
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
        """)
            # Add symbol column if missing (migration for existing DBs)
            cols = [r[1] for r in conn.execute("PRAGMA table_info(drawings)").fetchall()]
            if "symbol" not in cols:
                conn.execute("ALTER TABLE drawings ADD COLUMN symbol TEXT NOT NULL DEFAULT ''")

    async def init(self) -> None:
        self._init_tables()

    # --- Settings ---

    def _get_setting(self, key: str) -> str | None:
        with self._conn() as conn:
            row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
            return row["value"] if row else None

    def _set_setting(self, key: str, value: str) -> None:
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (key, value),
            )

    def _all_settings(self) -> dict[str, str]:
        with self._conn() as conn:
            rows = conn.execute("SELECT key, value FROM settings").fetchall()
            return {r["key"]: r["value"] for r in rows}

    async def get_setting(self, key: str) -> str | None:
        return self._get_setting(key)

    async def set_setting(self, key: str, value: str) -> None:
        self._set_setting(key, value)

    async def get_all_settings(self) -> dict[str, str]:
        return self._all_settings()

    # --- Toolbar Position ---

    def _save_toolbar_position(self, left: int, top: int) -> None:
        with self._conn() as conn:
            conn.execute(
                "UPDATE toolbar_position SET pos_left = ?, pos_top = ? WHERE id = 1",
                (left, top),
            )

    def _load_toolbar_position(self) -> dict | None:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT pos_left, pos_top FROM toolbar_position WHERE id = 1"
            ).fetchone()
            if row:
                return {"left": row["pos_left"], "top": row["pos_top"]}
            return None

    async def save_toolbar_position(self, left: int, top: int) -> None:
        self._save_toolbar_position(left, top)

    async def load_toolbar_position(self) -> dict | None:
        return self._load_toolbar_position()

    # --- Coin Icons ---

    def _save_coin_icons(self, icons: dict[str, str]) -> None:
        with self._conn() as conn:
            conn.execute("BEGIN")
            for sym, url in icons.items():
                conn.execute(
                    "INSERT INTO coin_icons (symbol, url) VALUES (?, ?) ON CONFLICT(symbol) DO UPDATE SET url = excluded.url",
                    (sym, url),
                )
            conn.execute("COMMIT")

    def _load_coin_icons(self) -> dict[str, str]:
        with self._conn() as conn:
            rows = conn.execute("SELECT symbol, url FROM coin_icons").fetchall()
            return {r["symbol"]: r["url"] for r in rows}

    async def save_coin_icons(self, icons: dict[str, str]) -> None:
        if not icons:
            return
        self._save_coin_icons(icons)

    async def load_coin_icons(self) -> dict[str, str]:
        return self._load_coin_icons()

    # --- Drawings ---

    def _load_drawings(self, symbol: str) -> list[dict]:
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

    def _save_drawings(self, symbol: str, drawings: list[dict]) -> None:
        with self._conn() as conn:
            conn.execute("DELETE FROM drawings WHERE symbol = ?", (symbol,))
            for d in drawings:
                conn.execute(
                    "INSERT INTO drawings (id, symbol, type, points, opts) VALUES (?, ?, ?, ?, ?)",
                    (d["id"], symbol, d["type"], json.dumps(d["points"]), json.dumps(d.get("opts", {}))),
                )

    async def load_drawings(self, symbol: str) -> list[dict]:
        return self._load_drawings(symbol)

    async def save_drawings(self, symbol: str, drawings: list[dict]) -> None:
        self._save_drawings(symbol, drawings)

    # --- Drawings Blob (new library format) ---

    def _save_drawings_blob(self, symbol: str, data: list | dict | str) -> None:
        serialized = json.dumps(data) if not isinstance(data, str) else data
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO drawings_blob (symbol, data, updated) VALUES (?, ?, datetime('now')) "
                "ON CONFLICT(symbol) DO UPDATE SET data = excluded.data, updated = excluded.updated",
                (symbol, serialized),
            )

    def _load_drawings_blob(self, symbol: str) -> list | dict | None:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT data FROM drawings_blob WHERE symbol = ?", (symbol,)
            ).fetchone()
            if row:
                return json.loads(row["data"])
            return None

    async def save_drawings_blob(self, symbol: str, data: list | dict | str) -> None:
        self._save_drawings_blob(symbol, data)

    async def load_drawings_blob(self, symbol: str) -> list | dict | None:
        return self._load_drawings_blob(symbol)

    # --- Candles ---

    def _save_candles(self, symbol: str, interval: str, candles: list[dict]) -> None:
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

    def _load_candles(self, symbol: str, interval: str) -> list[dict]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT time, open, high, low, close, volume FROM candles WHERE symbol = ? AND interval = ? ORDER BY time",
                (symbol, interval),
            ).fetchall()
            return [dict(r) for r in rows]

    def _load_last_n_candles(self, symbol: str, interval: str, n: int) -> list[dict]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT time, open, high, low, close, volume FROM candles WHERE symbol = ? AND interval = ? ORDER BY time DESC LIMIT ?",
                (symbol, interval, n),
            ).fetchall()
            return [dict(r) for r in reversed(rows)]

    def _load_candles_before(self, symbol: str, interval: str, n: int, before: int) -> list[dict]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT time, open, high, low, close, volume FROM candles WHERE symbol = ? AND interval = ? AND time < ? ORDER BY time DESC LIMIT ?",
                (symbol, interval, before, n),
            ).fetchall()
            return [dict(r) for r in reversed(rows)]

    def _get_candle_range(self, symbol: str, interval: str) -> tuple[int, int] | None:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT MIN(time), MAX(time) FROM candles WHERE symbol = ? AND interval = ?",
                (symbol, interval),
            ).fetchone()
            if row and row[0] is not None:
                return (int(row[0]), int(row[1]))
            return None

    def _count_candles(self, symbol: str, interval: str) -> int:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT COUNT(*) AS cnt FROM candles WHERE symbol = ? AND interval = ?",
                (symbol, interval),
            ).fetchone()
            return row["cnt"] if row else 0

    async def save_candles(self, symbol: str, interval: str, candles: list[dict]) -> None:
        if not candles:
            return
        self._save_candles(symbol, interval, candles)

    async def load_candles(self, symbol: str, interval: str) -> list[dict]:
        return self._load_candles(symbol, interval)

    async def load_last_n_candles(self, symbol: str, interval: str, n: int) -> list[dict]:
        return self._load_last_n_candles(symbol, interval, n)

    async def load_candles_before(self, symbol: str, interval: str, n: int, before: int) -> list[dict]:
        return self._load_candles_before(symbol, interval, n, before)

    async def get_candle_range(self, symbol: str, interval: str) -> tuple[int, int] | None:
        return self._get_candle_range(symbol, interval)

    async def count_candles(self, symbol: str, interval: str) -> int:
        return self._count_candles(symbol, interval)
