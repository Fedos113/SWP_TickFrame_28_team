from __future__ import annotations

import json
import logging
import os as _os

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel

from ..models.schemas import CandleResponse, CoinSummary, IndicatorsPayload, PriceResponse
from ..services.cache import MemoryMarketCache
from ..services.database import DatabaseService
from ..services.coin_icons import coin_icons_client
from ..services.fng_client import fng_client
from ..services.ml_client import MlClient, MlUnsupportedTimeframe


router = APIRouter(prefix="/api", tags=["market"])
LOGGER = logging.getLogger("tickframe.api")


def get_cache(request: Request) -> MemoryMarketCache:
    cache = getattr(request.app.state, "cache", None)
    if cache is None:
        raise HTTPException(status_code=503, detail="Market cache is not ready")
    return cache


def get_ml_client(request: Request) -> MlClient:
    client = getattr(request.app.state, "ml_client", None)
    if client is None:
        raise HTTPException(status_code=503, detail="ML client is not ready")
    return client


def get_database(request: Request) -> DatabaseService:
    db = getattr(request.app.state, "database", None)
    if db is None:
        raise HTTPException(status_code=503, detail="Database is not ready")
    return db


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/sentiment")
async def get_market_sentiment() -> dict:
    return await fng_client.get_index()


@router.get("/coins/icons")
async def get_coin_icons(db: DatabaseService = Depends(get_database)) -> dict[str, str]:
    return await coin_icons_client.get_icons(db=db)


@router.get("/coins", response_model=list[CoinSummary])
async def list_coins(cache: MemoryMarketCache = Depends(get_cache)) -> list[dict]:
    return await cache.list_coins()


@router.get("/coins/{symbol}/price", response_model=PriceResponse)
async def get_price(symbol: str, cache: MemoryMarketCache = Depends(get_cache)) -> dict:
    return await cache.get_price(symbol)


MAX_CANDLES_LIMIT: int = 55000


@router.get("/coins/{symbol}/candles", response_model=CandleResponse)
async def get_candles(
    symbol: str,
    interval: str = Query(default="5m", pattern="^(1m|3m|5m|15m|30m|1h|2h|4h|1d|1w|1M)$"),
    limit: int = Query(default=200, ge=10, le=MAX_CANDLES_LIMIT),
    before: int | None = Query(default=None, description="Return candles older than this unix timestamp (seconds)"),
    cache: MemoryMarketCache = Depends(get_cache),
) -> dict:
    payload = await cache.get_candles(symbol, interval, limit, before=before)
    LOGGER.info(
        "Candles requested symbol=%s interval=%s limit=%s before=%s -> returned=%s source=%s",
        symbol,
        interval,
        limit,
        before,
        len(payload.get("candles", [])),
        payload.get("source", "unknown"),
    )
    return payload


@router.post("/analyze/{symbol}")
async def analyze_patterns(
    symbol: str,
    interval: str = Query(default="5m", pattern="^(5m)$"),
    confidence_threshold: float = Query(default=0.60, ge=0.0, le=1.0),
    cache: MemoryMarketCache = Depends(get_cache),
    ml: MlClient = Depends(get_ml_client),
    db: DatabaseService = Depends(get_database),
) -> dict:

    existing = await db.load_ml_scan(symbol, interval)
    if existing and existing["patterns"]:
        LOGGER.info(
            "Incremental analyze symbol=%s interval=%s last_scanned=%s",
            symbol, interval, existing["last_scanned_time"],
        )
        after = existing["last_scanned_time"]
        existing_patterns = existing["patterns"]
        existing_times = {p["timestamp"] for p in existing_patterns if "timestamp" in p}
    else:
        after = 0
        existing_patterns = []
        existing_times = set()

    if after > 0:
        candles = await db.load_candles_after(symbol, interval, after)
    else:
        db_count = await db.count_candles(symbol, interval)
        if db_count >= 50000:
            candles = await db.load_last_n_candles(symbol, interval, 50000)
        else:
            cache_result = await cache.get_candles(symbol, interval, 50000)
            candles = cache_result.get("candles", [])

    if after == 0 and not candles:
        raise HTTPException(status_code=400, detail="No candle data available for analysis")

    if not candles:
        LOGGER.info("No new candles since last scan for %s", symbol)
        return {
            "symbol": symbol, "interval": interval,
            "patterns": existing_patterns,
        }

    ml_candles = [
        {"timestamp": c["time"], "open": c["open"], "high": c["high"],
         "low": c["low"], "close": c["close"], "volume": c["volume"]}
        for c in candles
    ]

    try:
        result = await ml.analyze(symbol, interval, ml_candles, confidence_threshold)
    except MlUnsupportedTimeframe as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    new_patterns = result["patterns"]
    processing_ms = result["processing_ms"]

    for p in new_patterns:
        ts = p.get("timestamp")
        if ts is not None and ts not in existing_times:
            existing_patterns.append(p)
            existing_times.add(ts)

    last_time = candles[-1]["time"]
    try:
        await db.save_ml_scan(symbol, interval, last_time, existing_patterns)
    except Exception as exc:
        # Persistence failure should not crash the request with a non-JSON 500.
        LOGGER.error("Failed to persist ML scan for %s: %s", symbol, exc)
        raise HTTPException(status_code=500, detail="Failed to persist analysis results")

    LOGGER.info(
        "Analyze complete symbol=%s new=%d total=%d",
        symbol, len(new_patterns), len(existing_patterns),
    )


    return {
        "symbol": symbol, "interval": interval,
        "patterns": existing_patterns,
        "processing_ms": processing_ms,
    }



@router.get("/patterns/{symbol}")
async def get_patterns(
    symbol: str,
    interval: str = Query(default="5m", pattern="^(5m|15m|1h|4h|1d)$"),
    db: DatabaseService = Depends(get_database),
) -> dict:
    scan = await db.load_ml_scan(symbol, interval)
    return {
        "symbol": symbol,
        "interval": interval,
        "patterns": scan["patterns"] if scan else [],
    }


class DrawingsPayload(BaseModel):
    symbol: str = ""
    drawings: list = []
    drawings_data: list | dict | str | None = None


class ToolbarPositionPayload(BaseModel):
    left: int = 16
    top: int = 12


class SettingsPayload(BaseModel):
    settings: dict[str, str] = {}


@router.get("/toolbar-position")
async def get_toolbar_position(db: DatabaseService = Depends(get_database)) -> dict:
    pos = await db.load_toolbar_position()
    if pos:
        return pos
    return {"left": 16, "top": 12}


@router.post("/toolbar-position")
async def save_toolbar_position(
    payload: ToolbarPositionPayload, db: DatabaseService = Depends(get_database)
) -> dict:
    await db.save_toolbar_position(payload.left, payload.top)
    return {"status": "ok"}


@router.get("/drawings")
async def get_drawings(symbol: str = "", db: DatabaseService = Depends(get_database)) -> dict:
    blob = await db.load_drawings_blob(symbol)
    if blob:
        return {"drawings_data": blob}
    return {"drawings": []}


@router.post("/drawings")
async def save_drawings(payload: DrawingsPayload, db: DatabaseService = Depends(get_database)) -> dict:
    data = payload.drawings_data if payload.drawings_data is not None else payload.drawings
    await db.save_drawings_blob(payload.symbol, data)
    return {"status": "ok"}

@router.get("/indicators")
async def get_indicators(symbol: str = "", db: DatabaseService = Depends(get_database)) -> dict:
    blob = await db.load_indicators(symbol)
    if blob:
        return {"indicators": blob}
    return {"indicators": []}


@router.post("/indicators")
async def save_indicators(payload: IndicatorsPayload, db: DatabaseService = Depends(get_database)) -> dict:
    await db.save_indicators(payload.symbol, payload.indicators)
    return {"status": "ok"}


@router.get("/settings")
async def get_settings(db: DatabaseService = Depends(get_database)) -> dict:
    settings = await db.get_all_settings()
    return {"settings": settings}


@router.post("/settings")
async def save_settings(payload: SettingsPayload, db: DatabaseService = Depends(get_database)) -> dict:
    for key, value in payload.settings.items():
        await db.set_setting(key, value)
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Admin / DB Toolkit endpoints (dev-only, gated by ENABLE_DB_ADMIN_API)
# ---------------------------------------------------------------------------

if _os.environ.get("ENABLE_DB_ADMIN_API", "").lower() in ("1", "true", "yes"):

    from fastapi.responses import StreamingResponse as _StreamingResponse
    import csv as _csv
    import io as _io

    @router.get("/admin/db/candles/{symbol}/export")
    async def admin_db_export_candles(
        symbol: str,
        interval: str = Query(default="5m"),
        fmt: str = Query(default="csv", alias="format"),
        db: DatabaseService = Depends(get_database),
    ) -> _StreamingResponse:
        candles = await db.load_candles(symbol, interval)
        if fmt == "json":
            return _StreamingResponse(
                iter([json.dumps(candles, indent=2)]),
                media_type="application/json",
                headers={"Content-Disposition": f"attachment; filename={symbol}_{interval}.json"},
            )
        buf = _io.StringIO()
        writer = _csv.DictWriter(buf, fieldnames=["time", "open", "high", "low", "close", "volume"])
        writer.writeheader()
        writer.writerows(candles)
        buf.seek(0)
        return _StreamingResponse(
            iter([buf.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={symbol}_{interval}.csv"},
        )

    @router.post("/admin/db/candles/{symbol}/import")
    async def admin_db_import_candles(
        symbol: str,
        interval: str = Query(default="5m"),
        db: DatabaseService = Depends(get_database),
    ) -> dict:
        from fastapi import UploadFile, File as _File, HTTPException as _HTTPException
        file: UploadFile = _File(...)
        content = await file.read()
        raw = content.decode("utf-8")
        ext = file.filename.split(".")[-1].lower() if file.filename else "csv"
        if ext == "json" or raw.strip().startswith("["):
            candles = json.loads(raw)
        else:
            reader = _csv.DictReader(_io.StringIO(raw))
            candles = []
            row_num = 0
            for row in reader:
                row_num += 1
                try:
                    candles.append({
                        "time": int(row["time"]),
                        "open": float(row["open"]),
                        "high": float(row["high"]),
                        "low": float(row["low"]),
                        "close": float(row["close"]),
                        "volume": float(row.get("volume", 0)),
                    })
                except (ValueError, KeyError) as e:
                    raise _HTTPException(400, f"Row {row_num}: {e}")
        total = len(candles)
        await db.save_candles(symbol, interval, candles)
        return {"status": "ok", "rows_read": total, "rows_upserted": total}

    @router.get("/admin/db/patterns/{symbol}")
    async def admin_db_patterns(
        symbol: str,
        interval: str = Query(default="5m"),
        db: DatabaseService = Depends(get_database),
    ) -> dict:
        scan = await db.load_ml_scan(symbol, interval)
        if scan:
            return scan
        return {"symbol": symbol, "interval": interval, "last_scanned_time": 0, "patterns": []}
