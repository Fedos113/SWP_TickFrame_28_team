from pydantic import BaseModel, Field
from typing import List

class CandleData(BaseModel):
    timestamp: int = Field(..., description="Unix timestamp of the candle")
    open: float = Field(..., description="Open price")
    high: float = Field(..., description="High price")
    low: float = Field(..., description="Low price")
    close: float = Field(..., description="Close price")
    volume: float = Field(..., description="Trading volume")

class PredictRequest(BaseModel):
    symbol: str = Field(..., example="BTCUSDT", description="Trading pair name")
    timeframe: str = Field(..., example="5m", description="Candle timeframe. Currently only '5m' is supported.")
    candles: List[CandleData] = Field(
        ...,
        min_length=99,
        description="At least 99 OHLCV candles, including historical context for both detectors",
    )

class DetectedPattern(BaseModel):
    timestamp: int = Field(..., description="Timestamp where the pattern peak was detected")
    pattern_type: str = Field(..., example="Classic H&S", description="Detected pattern type (Classic H&S or Inverse H&S)")
    confidence: float = Field(..., description="Model probability for this pattern in range [0, 1]")
    detector: str = Field(
        default="hs",
        example="hs",
        description="Detector that produced the signal: hs or dtdb",
    )


class ProcessingTimes(BaseModel):
    total_ms: float = Field(0.0, description="Total server-side analysis time")
    hs_ms: float = Field(
        0.0,
        description="H&S pipeline time for Classic H&S and Inverse H&S",
    )
    dtdb_ms: float = Field(
        0.0,
        description="DT/DB pipeline time for Double Top and Double Bottom",
    )


class PredictResponse(BaseModel):
    symbol: str = Field(..., example="BTCUSDT")
    timeframe: str = Field(..., example="5m", description="The timeframe of the analyzed candles") # <-- ДОБАВЛЕНО
    patterns_found: List[DetectedPattern] = Field(..., description="List of filtering-passed patterns")
    processed_candles: int = Field(..., description="Total candles analyzed after geometry crop")
    processing_ms: ProcessingTimes = Field(
        default_factory=ProcessingTimes,
        description="Server-side processing timings by detector",
    )