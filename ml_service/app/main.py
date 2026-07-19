import os
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
import numpy as np
import pandas as pd
import xgboost as xgb

from app.config import (
    DTDB_FEATURE_ORDER,
    DTDB_MIN_CANDLES,
    DTDB_MODEL_PATH,
    DTDB_NMS_WINDOW,
    DTDB_WINDOW_SIZE,
    FEATURE_ORDER,
    MODEL_PATH,
    WINDOW_SIZE,
)
from app.schemas import (
    DetectedPattern,
    PredictRequest,
    PredictResponse,
    ProcessingTimes,
)
from app.services.features import (
    SharedFeatureSet,
    add_dtdb_features,
    add_smart_features,
    prepare_shared_features,
    warmup_feature_engineering,
)
from app.services.inference import (
    apply_dtdb_thresholds,
    apply_nms_clustering,
    apply_pattern_thresholds,
)

# ==========================================
# Logger Configuration
# ==========================================
# setting up a basic logger to log messages to both console and a file

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] ML_API: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("logs/app.log", encoding="utf-8"), # Указана кодировка UTF-8
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the lifecycle of the FastAPI application.
    Loads the XGBoost model into memory on startup and clears it on shutdown.
    """
    model_paths = {
        "hs_detector": MODEL_PATH,
        "dtdb_detector": DTDB_MODEL_PATH,
    }
    for detector_name, model_path in model_paths.items():
        logger.info(
            "🚀 [STARTUP] Loading %s XGBoost model from %s...",
            detector_name,
            model_path,
        )
        if not os.path.exists(model_path):
            logger.error("❌ Model file not found at: %s", model_path)
            raise FileNotFoundError(f"Model file not found at: {model_path}")

        model = xgb.XGBClassifier()
        model.load_model(model_path)
        ml_models[detector_name] = model
        logger.info("✅ [STARTUP] %s model loaded successfully!", detector_name)
    warmup_feature_engineering(window_size=WINDOW_SIZE)
    logger.info("✅ [STARTUP] Feature-engineering kernel warmed up")
    yield
    logger.info("🛑 [SHUTDOWN] Clearing ML models...")
    ml_models.clear()

app = FastAPI(
    title="TickFrame ML API",
    description="Production REST API for real-time Head and Shoulders pattern detection.",
    version="1.1.0",
    lifespan=lifespan
)

@app.get("/health", tags=["Health"])
def health_check():
    """
    Basic health check endpoint to verify that the API is running
    and the ML model is successfully loaded into memory.
    """
    models = {
        "hs": "hs_detector" in ml_models,
        "dtdb": "dtdb_detector" in ml_models,
    }
    return {
        "status": "success" if all(models.values()) else "degraded",
        "model_loaded": all(models.values()),
        "models": models,
    }

def _run_detector(
    featured_df: pd.DataFrame,
    model: xgb.XGBClassifier,
    feature_order: list[str],
    detector: str,
    pattern_names: dict[int, str],
    original_timestamps: np.ndarray,
    use_dtdb_thresholds: bool = False,
    nms_window: int = 10,
) -> list[DetectedPattern]:
    missing_features = [
        feature for feature in feature_order if feature not in featured_df.columns
    ]
    if missing_features:
        raise ValueError(
            f"{detector} feature contract is missing columns: {missing_features}"
        )
    if featured_df.empty:
        return []

    X_inference = featured_df[feature_order].to_numpy()
    probas = model.predict_proba(X_inference)
    if use_dtdb_thresholds:
        y_pred_raw = apply_dtdb_thresholds(probas)
    else:
        y_pred_raw = apply_pattern_thresholds(probas)
    y_pred_clean = apply_nms_clustering(
        y_pred_raw,
        probas,
        tolerance_window=nms_window,
    )

    detected_patterns = []
    for row_idx, cls in enumerate(y_pred_clean):
        if cls <= 0:
            continue
        original_row_idx = int(featured_df.index[row_idx])
        timestamp = int(original_timestamps[original_row_idx])
        detected_patterns.append(
            DetectedPattern(
                timestamp=timestamp,
                pattern_type=pattern_names[int(cls)],
                confidence=float(probas[row_idx, cls]),
                detector=detector,
            )
        )
    return detected_patterns


def _analyze_hs(
    df: pd.DataFrame,
    model: xgb.XGBClassifier,
    original_timestamps: np.ndarray,
    shared: SharedFeatureSet,
) -> tuple[int, list[DetectedPattern], float]:
    started = time.perf_counter()
    featured_df = add_smart_features(df, shared=shared)
    patterns = _run_detector(
        featured_df,
        model,
        FEATURE_ORDER,
        detector="hs",
        pattern_names={1: "Classic H&S", 2: "Inverse H&S"},
        original_timestamps=original_timestamps,
        nms_window=WINDOW_SIZE // 5,
    )
    elapsed_ms = (time.perf_counter() - started) * 1000
    return len(featured_df), patterns, elapsed_ms


def _analyze_dtdb(
    df: pd.DataFrame,
    model: xgb.XGBClassifier,
    original_timestamps: np.ndarray,
    shared: SharedFeatureSet,
) -> tuple[int, list[DetectedPattern], float]:
    started = time.perf_counter()
    featured_df = add_dtdb_features(
        df,
        window_size=DTDB_WINDOW_SIZE,
        shared=shared,
    )
    patterns = _run_detector(
        featured_df,
        model,
        DTDB_FEATURE_ORDER,
        detector="dtdb",
        pattern_names={1: "Double Top", 2: "Double Bottom"},
        original_timestamps=original_timestamps,
        use_dtdb_thresholds=True,
        nms_window=DTDB_NMS_WINDOW,
    )
    elapsed_ms = (time.perf_counter() - started) * 1000
    return len(featured_df), patterns, elapsed_ms


@app.post(
    "/predict",
    response_model=PredictResponse,
    tags=["Inference"],
    summary="Analyze Candlestick Chart",
    response_description="""
    Returns a JSON object containing the requested symbol, timeframe, and a list of verified patterns.
    If patterns are found, `patterns_found` contains their timestamps and confidence scores.
    If no patterns are detected, `patterns_found` will be an empty array [].
    """,
    description="""
**Analyzes an array of OHLCV candles with both H&S and DT/DB detectors.**

⚠️ **DATA REQUIREMENT WARNING:**
The models require historical context to calculate market indicators (e.g., NATR, Trend_50).
You **MUST include an additional 50 historical candles** prior to the first candle you actually want to analyze.

*Example: To analyze the chart from 10:00 to 12:00, you must send an array of candles starting from 05:50 (50 previous 5-minute candles).*

**Pipeline Algorithm:**
1. Receives raw OHLCV data.
2. Calculates independent H&S and DT/DB feature sets.
3. Runs both XGBoost detectors on the same candle request.
4. Applies detector-specific Non-Maximum Suppression (NMS) and thresholds.
5. Returns the verified pattern peaks with their detector names.
"""
)
def predict_pattern(request: PredictRequest):
    """
    Main inference endpoint. Converts JSON request to DataFrame,
    extracts features, filters columns by strict order to drop metadata (like timestamp),
    predicts probabilities, and formats the output.
    """
    logger.info(f"📥 Received predict request for {request.symbol} | Timeframe: {request.timeframe} | Candles: {len(request.candles)}")

    # Validation constraint for timeframe
    if request.timeframe != "5m":
        logger.warning(f"⚠️ Invalid timeframe requested: {request.timeframe}")
        raise HTTPException(status_code=400, detail="Only '5m' timeframe candles are currently supported.")

    # Check if we have enough context candles to calculate geometry
    minimum_candles = max(WINDOW_SIZE, DTDB_MIN_CANDLES)
    if len(request.candles) < minimum_candles:
        logger.warning(
            "⚠️ Insufficient candles: %s. Required: %s",
            len(request.candles),
            minimum_candles,
        )
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient candles. Minimum required is {minimum_candles}.",
        )

    try:
        hs_model = ml_models.get("hs_detector")
        dtdb_model = ml_models.get("dtdb_detector")
        if hs_model is None or dtdb_model is None:
            logger.error("❌ Both ML models must be ready in memory.")
            raise RuntimeError("Both ML models must be ready in memory.")

        # 1. Convert Pydantic request to Pandas DataFrame
        raw_data = [c.model_dump() for c in request.candles]
        df = pd.DataFrame(raw_data)
        original_timestamps = df["timestamp"].to_numpy()
        analysis_started = time.perf_counter()

        # Both detectors use the same 50-candle window and NATR base metrics.
        # Build those arrays once, then run detector-specific work in parallel.
        shared_features = prepare_shared_features(df, window_size=WINDOW_SIZE)
        with ThreadPoolExecutor(max_workers=2) as executor:
            hs_future = executor.submit(
                _analyze_hs,
                df,
                hs_model,
                original_timestamps,
                shared_features,
            )
            dtdb_future = executor.submit(
                _analyze_dtdb,
                df,
                dtdb_model,
                original_timestamps,
                shared_features,
            )
            hs_processed, hs_patterns, hs_ms = hs_future.result()
            dtdb_processed, dtdb_patterns, dtdb_ms = dtdb_future.result()

        detected_patterns = hs_patterns + dtdb_patterns
        total_ms = (time.perf_counter() - analysis_started) * 1000

        logger.info(
            "✅ Prediction complete for %s. Found %s patterns "
            "(H&S=%s, DT/DB=%s).",
            request.symbol,
            len(detected_patterns),
            sum(pattern.detector == "hs" for pattern in detected_patterns),
            sum(pattern.detector == "dtdb" for pattern in detected_patterns),
        )

        return PredictResponse(
            symbol=request.symbol,
            timeframe=request.timeframe,
            patterns_found=detected_patterns,
            processed_candles=max(hs_processed, dtdb_processed),
            processing_ms=ProcessingTimes(
                total_ms=total_ms,
                hs_ms=hs_ms,
                dtdb_ms=dtdb_ms,
            ),
        )

    except Exception as e:
        logger.error(f"💥 Execution error during prediction: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Execution error: {str(e)}")
