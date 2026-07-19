"""Unit tests for DatabaseService."""

import shutil
import tempfile
from pathlib import Path

import pytest
from tickframe.backend.services.database import DatabaseService


@pytest.fixture
def db():
    tmpdir = Path(tempfile.mkdtemp(prefix="tickframe-db-", suffix="-test"))
    path = tmpdir / "test.db"
    svc = DatabaseService(use_sqlite=True, db_path=path)

    try:
        yield svc
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.mark.asyncio
async def test_init_creates_tables(db):
    await db.init()
    with db._conn() as conn:
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        names = {r["name"] for r in tables}
    assert "settings" in names
    assert "drawings" in names
    assert "candles" in names


@pytest.mark.asyncio
async def test_setting_round_trip(db):
    await db.init()
    await db.set_setting("theme", "dark")
    value = await db.get_setting("theme")
    assert value == "dark"


@pytest.mark.asyncio
async def test_setting_overwrite(db):
    await db.init()
    await db.set_setting("theme", "dark")
    await db.set_setting("theme", "light")
    value = await db.get_setting("theme")
    assert value == "light"


@pytest.mark.asyncio
async def test_get_setting_missing_returns_none(db):
    await db.init()
    value = await db.get_setting("nonexistent")
    assert value is None


@pytest.mark.asyncio
async def test_get_all_settings(db):
    await db.init()
    await db.set_setting("theme", "dark")
    await db.set_setting("interval", "5m")
    all_settings = await db.get_all_settings()
    assert all_settings["theme"] == "dark"
    assert all_settings["interval"] == "5m"


@pytest.mark.asyncio
async def test_save_load_drawings(db):
    await db.init()
    drawings = [
        {"id": 1, "type": "trendline", "points": [{"x": 0, "y": 100}], "opts": {}},
        {"id": 2, "type": "rectangle", "points": [{"x": 0, "y": 0}], "opts": {"color": "red"}},
    ]
    await db.save_drawings("BTCUSDT", drawings)
    loaded = await db.load_drawings("BTCUSDT")
    assert len(loaded) == 2
    assert loaded[0]["type"] == "trendline"
    assert loaded[1]["type"] == "rectangle"


@pytest.mark.asyncio
async def test_load_drawings_empty_symbol(db):
    await db.init()
    loaded = await db.load_drawings("UNKNOWN")
    assert loaded == []


@pytest.mark.asyncio
async def test_save_load_candles(db):
    await db.init()
    candles = [
        {"time": 1000, "open": 100.0, "high": 110.0, "low": 90.0, "close": 105.0, "volume": 1000},
        {"time": 2000, "open": 105.0, "high": 115.0, "low": 95.0, "close": 110.0, "volume": 2000},
    ]
    await db.save_candles("BTCUSDT", "5m", candles)
    loaded = await db.load_candles("BTCUSDT", "5m")
    assert len(loaded) == 2
    assert loaded[0]["open"] == 100.0
    assert loaded[1]["close"] == 110.0


@pytest.mark.asyncio
async def test_load_candles_cache_miss(db):
    await db.init()
    loaded = await db.load_candles("BTCUSDT", "5m")
    assert loaded == []


@pytest.mark.asyncio
async def test_load_last_n_candles(db):
    await db.init()
    candles = [{"time": t, "open": 100.0, "high": 110.0, "low": 90.0, "close": 105.0, "volume": 1000} for t in range(0, 10000, 1000)]
    await db.save_candles("BTCUSDT", "5m", candles)
    loaded = await db.load_last_n_candles("BTCUSDT", "5m", 3)
    assert len(loaded) == 3


@pytest.mark.asyncio
async def test_candle_range(db):
    await db.init()
    candles = [
        {"time": 1000, "open": 100.0, "high": 110.0, "low": 90.0, "close": 105.0, "volume": 1000},
        {"time": 5000, "open": 105.0, "high": 115.0, "low": 95.0, "close": 110.0, "volume": 2000},
    ]
    await db.save_candles("BTCUSDT", "5m", candles)
    rng = await db.get_candle_range("BTCUSDT", "5m")
    assert rng == (1000, 5000)


@pytest.mark.asyncio
async def test_candle_range_no_data(db):
    await db.init()
    rng = await db.get_candle_range("BTCUSDT", "5m")
    assert rng is None


@pytest.mark.asyncio
async def test_count_candles(db):
    await db.init()
    candles = [{"time": t, "open": 100.0, "high": 110.0, "low": 90.0, "close": 105.0, "volume": 1000} for t in range(0, 5000, 1000)]
    await db.save_candles("BTCUSDT", "5m", candles)
    count = await db.count_candles("BTCUSDT", "5m")
    assert count == 5


@pytest.mark.asyncio
async def test_save_empty_candles_noop(db):
    await db.init()
    await db.save_candles("BTCUSDT", "5m", [])
    count = await db.count_candles("BTCUSDT", "5m")
    assert count == 0
