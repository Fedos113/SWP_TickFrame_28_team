from __future__ import annotations

from pydantic import BaseModel, Field


class CoinSummary(BaseModel):
    class Config:
        allow_population_by_field_name = True

    symbol: str
    pair: str
    name: str
    icon: str = Field(default="")
    color: str = Field(default="#2962ff")
    price: float = 0.0
    change_24h: float = 0.0
    volume_24h: float = 0.0
    source: str = "cache"
    trend: str = "neutral"


class Candle(BaseModel):
    time: int
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0


class CandleResponse(BaseModel):
    symbol: str
    interval: str
    source: str = "bybit"
    updated_at: str
    candles: list[Candle]


class PriceResponse(BaseModel):
    symbol: str
    pair: str
    price: float
    change_24h: float
    volume_24h: float = 0.0
    updated_at: str
    source: str = "cache"


class MarketSnapshot(BaseModel):
    updated_at: str
    coins: list[CoinSummary]


class Pattern(BaseModel):
    timestamp: int
    pattern_type: str
    confidence: float
    detector: str = "hs"


class AnalyzeResponse(BaseModel):
    symbol: str
    interval: str
    limit: int
    patterns: list[Pattern]


class IndicatorConfig(BaseModel):
    uid: str
    indicatorId: str
    inputs: dict | None = None
    overlay: bool = True


class IndicatorsResponse(BaseModel):
    indicators: list[dict]


class IndicatorsPayload(BaseModel):
    symbol: str = ""
    indicators: list = []
