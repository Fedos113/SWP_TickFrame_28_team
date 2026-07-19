from __future__ import annotations

import logging
import time

import httpx

logger = logging.getLogger(__name__)

CACHE_TTL = 21600  # 6 hours — index updates daily


class FearAndGreedClient:
    def __init__(self) -> None:
        self.url = "https://api.alternative.me/fng/?limit=1"
        self._cache: dict | None = None
        self._cache_expiry: float = 0

    async def get_index(self) -> dict:
        if self._cache and time.time() < self._cache_expiry:
            return self._cache

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(self.url)
                resp.raise_for_status()
                data = resp.json()["data"][0]
                raw_value = int(data["value"])
                self._cache = {
                    "value": max(0, min(100, raw_value)),
                    "classification": data["value_classification"],
                    "timestamp": int(data["timestamp"]),
                }
                self._cache_expiry = time.time() + CACHE_TTL
        except Exception as exc:
            logger.warning("Fear & Greed fetch failed: %s", exc)
            if self._cache is None:
                self._cache = {
                    "value": 50,
                    "classification": "Neutral",
                    "timestamp": int(time.time()),
                }
                self._cache_expiry = time.time() + 300  # retry sooner on failure

        return self._cache


fng_client = FearAndGreedClient()
