"""Unit tests for db_toolkit.py using SQLite fallback mode."""

import json
import shutil
import tempfile
from pathlib import Path

import pytest
import pytest_asyncio

from tickframe.backend.services.db_toolkit import (
    count_candles,
    export_candles,
    get_candle_range,
    get_patterns,
    import_candles,
    list_all_scanned_symbols,
    run_readonly_query,
)
from tickframe.backend.services.database import DatabaseService


@pytest_asyncio.fixture
async def db():
    tmpdir = Path(tempfile.mkdtemp(prefix="tickframe-dbtk-", suffix="-test"))
    path = tmpdir / "test.db"
    svc = DatabaseService(use_sqlite=True, db_path=path)
    await svc.init()
    try:
        yield svc
    finally:
        await svc.close()
        shutil.rmtree(tmpdir, ignore_errors=True)


SAMPLE_CANDLES = [
    {"time": 1000, "open": 100.0, "high": 110.0, "low": 90.0, "close": 105.0, "volume": 1000},
    {"time": 2000, "open": 105.0, "high": 115.0, "low": 95.0, "close": 110.0, "volume": 2000},
    {"time": 3000, "open": 110.0, "high": 120.0, "low": 100.0, "close": 115.0, "volume": 3000},
]


@pytest.mark.asyncio
async def test_get_db_returns_connected_service(db):
    assert db._pool is None  # SQLite mode
    assert db.use_sqlite is True


@pytest.mark.asyncio
async def test_export_candles_csv(db):
    await db.save_candles("BTCUSDT", "5m", SAMPLE_CANDLES)
    tmpdir = Path(tempfile.mkdtemp())
    try:
        out = tmpdir / "test.csv"
        count = await export_candles(db, "BTCUSDT", "5m", out, fmt="csv")
        assert count == 3
        content = out.read_text()
        assert "time,open,high,low,close,volume" in content
        assert "1000,100.0,110.0,90.0,105.0,1000.0" in content
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.mark.asyncio
async def test_export_candles_json(db):
    await db.save_candles("BTCUSDT", "5m", SAMPLE_CANDLES)
    tmpdir = Path(tempfile.mkdtemp())
    try:
        out = tmpdir / "test.json"
        count = await export_candles(db, "BTCUSDT", "5m", out, fmt="json")
        assert count == 3
        data = json.loads(out.read_text())
        assert len(data) == 3
        assert data[0]["time"] == 1000
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.mark.asyncio
async def test_import_candles_csv(db):
    tmpdir = Path(tempfile.mkdtemp())
    try:
        csv_path = tmpdir / "in.csv"
        csv_path.write_text("time,open,high,low,close,volume\n100,10,12,8,11,500\n200,11,13,9,12,600\n")
        result = await import_candles(db, "ETHUSDT", "15m", csv_path, fmt="csv")
        assert result["rows_read"] == 2
        assert result["rows_upserted"] == 2
        loaded = await db.load_candles("ETHUSDT", "15m")
        assert len(loaded) == 2
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.mark.asyncio
async def test_import_candles_json(db):
    candles = [
        {"time": 10, "open": 1.0, "high": 2.0, "low": 0.5, "close": 1.5, "volume": 100},
    ]
    tmpdir = Path(tempfile.mkdtemp())
    try:
        json_path = tmpdir / "in.json"
        json_path.write_text(json.dumps(candles))
        result = await import_candles(db, "SOLUSDT", "1h", json_path, fmt="json")
        assert result["rows_read"] == 1
        loaded = await db.load_candles("SOLUSDT", "1h")
        assert len(loaded) == 1
        assert loaded[0]["close"] == 1.5
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.mark.asyncio
async def test_export_import_round_trip(db):
    await db.save_candles("XRPUSDT", "5m", SAMPLE_CANDLES)
    tmpdir = Path(tempfile.mkdtemp())
    try:
        out = tmpdir / "roundtrip.csv"
        await export_candles(db, "XRPUSDT", "5m", out, fmt="csv")
        await db.close()

        # New DB — import
        path2 = Path(tempfile.mkdtemp()) / "test2.db"
        db2 = DatabaseService(use_sqlite=True, db_path=path2)
        await db2.init()
        try:
            result = await import_candles(db2, "XRPUSDT", "5m", out, fmt="csv")
            assert result["rows_read"] == 3
            loaded = await db2.load_candles("XRPUSDT", "5m")
            assert len(loaded) == 3
            assert loaded[0]["time"] == 1000
            assert loaded[-1]["close"] == 115.0
        finally:
            await db2.close()
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.mark.asyncio
async def test_get_candle_range(db):
    rng = await get_candle_range(db, "BTCUSDT", "5m")
    assert rng is None
    await db.save_candles("BTCUSDT", "5m", SAMPLE_CANDLES)
    rng = await get_candle_range(db, "BTCUSDT", "5m")
    assert rng == (1000, 3000)


@pytest.mark.asyncio
async def test_count_candles(db):
    cnt = await count_candles(db, "BTCUSDT", "5m")
    assert cnt == 0
    await db.save_candles("BTCUSDT", "5m", SAMPLE_CANDLES)
    cnt = await count_candles(db, "BTCUSDT", "5m")
    assert cnt == 3


@pytest.mark.asyncio
async def test_get_patterns_no_scan(db):
    result = await get_patterns(db, "BTCUSDT")
    assert result is None


@pytest.mark.asyncio
async def test_get_patterns_with_data(db):
    patterns = [
        {"timestamp": 1000, "pattern_type": "Classic H&S", "confidence": 0.85},
        {"timestamp": 2000, "pattern_type": "Inverse H&S", "confidence": 0.72},
    ]
    await db.save_ml_scan("BTCUSDT", "5m", 3000, patterns)
    result = await get_patterns(db, "BTCUSDT")
    assert result is not None
    assert result["symbol"] == "BTCUSDT"
    assert result["interval"] == "5m"
    assert result["last_scanned_time"] == 3000
    assert len(result["patterns"]) == 2
    assert result["patterns"][0]["pattern_type"] == "Classic H&S"


@pytest.mark.asyncio
async def test_get_patterns_pretty_adds_datetime(db):
    patterns = [{"timestamp": 1000, "pattern_type": "Classic H&S", "confidence": 0.85}]
    await db.save_ml_scan("BTCUSDT", "5m", 2000, patterns)
    result = await get_patterns(db, "BTCUSDT", pretty=True)
    assert result is not None
    assert "datetime" in result["patterns"][0]


@pytest.mark.asyncio
async def test_list_all_scanned_symbols_empty(db):
    symbols = await list_all_scanned_symbols(db)
    assert symbols == []


@pytest.mark.asyncio
async def test_list_all_scanned_symbols(db):
    await db.save_ml_scan("BTCUSDT", "5m", 100, [])
    await db.save_ml_scan("ETHUSDT", "15m", 200, [])
    symbols = await list_all_scanned_symbols(db)
    assert symbols == ["BTCUSDT", "ETHUSDT"]


@pytest.mark.asyncio
async def test_run_readonly_query_select(db):
    await db.save_candles("BTCUSDT", "5m", SAMPLE_CANDLES)
    rows = await run_readonly_query(db, "SELECT COUNT(*) AS cnt FROM candles")
    assert len(rows) == 1
    assert rows[0]["cnt"] == 3


@pytest.mark.asyncio
async def test_run_readonly_query_rejects_insert(db):
    with pytest.raises(ValueError, match="read-only"):
        await run_readonly_query(db, "INSERT INTO settings (key, value) VALUES ('a', 'b')")


@pytest.mark.asyncio
async def test_run_readonly_query_rejects_drop(db):
    with pytest.raises(ValueError, match="read-only"):
        await run_readonly_query(db, "DROP TABLE candles")


@pytest.mark.asyncio
async def test_run_readonly_query_rejects_update(db):
    with pytest.raises(ValueError, match="read-only"):
        await run_readonly_query(db, "UPDATE settings SET value = 'x' WHERE key = 'y'")


@pytest.mark.asyncio
async def test_run_readonly_query_rejects_delete(db):
    with pytest.raises(ValueError, match="read-only"):
        await run_readonly_query(db, "DELETE FROM candles WHERE symbol = 'BTCUSDT'")


@pytest.mark.asyncio
async def test_run_readonly_query_rejects_empty(db):
    with pytest.raises(ValueError, match="empty"):
        await run_readonly_query(db, "")


@pytest.mark.asyncio
async def test_run_readonly_query_empty_result(db):
    rows = await run_readonly_query(db, "SELECT * FROM candles WHERE symbol = 'NONEXISTENT'")
    assert rows == []
