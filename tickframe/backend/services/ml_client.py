from __future__ import annotations

import logging
import os
from typing import Any

import httpx

LOGGER = logging.getLogger("tickframe.ml_client")

ML_API_URL = os.getenv("ML_API_URL", "http://ml-service:8001/predict")
ML_CONFIDENCE_THRESHOLD = float(os.getenv("ML_CONFIDENCE_THRESHOLD", "0.60"))
ML_REQUEST_TIMEOUT = float(os.getenv("ML_REQUEST_TIMEOUT", "30.0"))

# The ML service currently only supports the 5m timeframe (see ML API guide).
ML_SUPPORTED_TIMEFRAMES = {"5m"}


class MlUnsupportedTimeframe(Exception):
    """Raised when a timeframe not supported by the ML service is requested."""



class MlClient:
    def __init__(self, predict_url: str = ML_API_URL, timeout: float = ML_REQUEST_TIMEOUT):
        primary = predict_url.rstrip("/")
        self._urls = [primary]
        fallback = "http://127.0.0.1:8001/predict"
        if primary != fallback:
            self._urls.append(fallback)
        self._timeout = timeout
        self._client = httpx.AsyncClient(timeout=timeout)

    async def aclose(self) -> None:
        await self._client.aclose()

    async def analyze_candles(
        self,
        symbol: str,
        timeframe: str,
        candles: list[dict[str, Any]],
        threshold: float | None = None,
    ) -> list[dict[str, Any]]:
        result = await self.analyze(symbol, timeframe, candles, threshold)
        return result["patterns"]

    async def analyze(
        self,
        symbol: str,
        timeframe: str,
        candles: list[dict[str, Any]],
        threshold: float | None = None,
    ) -> dict[str, Any]:
        """Run ML analysis and return both patterns and server-side timings.

        Returns a dict: {"patterns": [...], "processing_ms": {...}}.
        Raises MlUnsupportedTimeframe if the timeframe is not supported by ML.
        """
        empty: dict[str, Any] = {"patterns": [], "processing_ms": {}}

        if timeframe not in ML_SUPPORTED_TIMEFRAMES:
            # The ML service only supports 5m; do not silently return "no patterns".
            raise MlUnsupportedTimeframe(
                f"Timeframe '{timeframe}' is not supported by the ML service "
                f"(supported: {sorted(ML_SUPPORTED_TIMEFRAMES)})"
            )

        if len(candles) < 99:
            LOGGER.warning("Not enough candles for ML analysis: %s (min 99)", len(candles))
            return empty

        threshold = threshold if threshold is not None else ML_CONFIDENCE_THRESHOLD


        payload = {
            "timeframe": timeframe,
            "symbol": symbol,
            "candles": candles,
        }

        for url in self._urls:
            try:
                response = await self._client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
            except httpx.ConnectError:
                LOGGER.warning("ML service unreachable at %s", url)
                continue
            except httpx.TimeoutException:
                LOGGER.warning("ML request timed out after %ss", self._timeout)
                return empty
            except httpx.HTTPStatusError as exc:
                LOGGER.warning("ML returned status %s: %s", exc.response.status_code, exc.response.text)
                return empty
            except Exception as exc:
                LOGGER.warning("ML request failed: %s", exc)
                return empty
            else:
                patterns = data.get("patterns_found", [])
                # Preserve the additive `detector` field on each pattern (see ML API guide).
                #
                # The ML service already applies its own tuned per-detector thresholds.
                # The backend's extra confidence filter is only meaningful for the H&S
                # detector, whose confidences run high (~0.8-0.99). The DT/DB detector's
                # confidences are inherently lower (peaking ~0.48), so applying the same
                # H&S-oriented threshold here would silently drop every valid Double
                # Top / Double Bottom. We therefore only threshold-filter H&S patterns
                # and trust the ML model's own DT/DB threshold. (See ML API guide.)
                filtered = [
                    p
                    for p in patterns
                    if p.get("detector") == "dtdb"
                    or p.get("confidence", 0) >= threshold
                ]

                processing_ms = data.get("processing_ms", {})
                LOGGER.info(
                    "ML analysis: %d patterns found, %d above threshold %.2f",
                    len(patterns),
                    len(filtered),
                    threshold,
                )
                return {"patterns": filtered, "processing_ms": processing_ms}

        LOGGER.warning("All ML URLs exhausted, service unavailable")
        return empty

