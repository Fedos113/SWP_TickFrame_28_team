from __future__ import annotations

import time
from typing import TYPE_CHECKING

import httpx

if TYPE_CHECKING:
    from .database import DatabaseService

COINGECKO_API = "https://api.coingecko.com/api/v3/coins/markets"
CACHE_TTL = 3600  # 1 hour — icons rarely change

SYMBOL_TO_ID: dict[str, str] = {
    "BTCUSDT": "bitcoin",
    "ETHUSDT": "ethereum",
    "SOLUSDT": "solana",
    "XRPUSDT": "ripple",
    "DOGEUSDT": "dogecoin",
    "ADAUSDT": "cardano",
    "AVAXUSDT": "avalanche-2",
    "DOTUSDT": "polkadot",
    "LINKUSDT": "chainlink",
    "BNBUSDT": "binancecoin",
}

# Hardcoded default icons to avoid CoinGecko API calls on cold boot.
# These are standard CoinGecko icon URLs that are stable.
DEFAULT_ICONS: dict[str, str] = {
    "BTCUSDT": "https://coin-images.coingecko.com/coins/images/1/large/bitcoin.png",
    "ETHUSDT": "https://coin-images.coingecko.com/coins/images/279/large/ethereum.png",
    "SOLUSDT": "https://coin-images.coingecko.com/coins/images/4128/large/solana.png",
    "XRPUSDT": "https://coin-images.coingecko.com/coins/images/44/large/xrp-symbol-white-01.png",
    "DOGEUSDT": "https://coin-images.coingecko.com/coins/images/5/large/dogecoin.png",
    "ADAUSDT": "https://coin-images.coingecko.com/coins/images/975/large/cardano.png",
    "AVAXUSDT": "https://coin-images.coingecko.com/coins/images/12559/large/Avalanche_Circle_RedWhite_Trans.png",
    "DOTUSDT": "https://coin-images.coingecko.com/coins/images/12171/large/polkadot.png",
    "LINKUSDT": "https://coin-images.coingecko.com/coins/images/877/large/chainlink-new-logo.png",
    "BNBUSDT": "https://coin-images.coingecko.com/coins/images/825/large/bnb-icon2_2x.png",
}


class CoinIconsClient:
    def __init__(self) -> None:
        self._cache: dict[str, str] | None = None
        self._cache_expiry: float = 0

    async def get_icons(self, db: DatabaseService | None = None) -> dict[str, str]:
        if self._cache is not None and time.time() < self._cache_expiry:
            return self._cache

        # Try DB first
        if db is not None:
            db_icons = await db.load_coin_icons()
            if db_icons:
                self._cache = db_icons
                self._cache_expiry = time.time() + CACHE_TTL
                return db_icons

        # Use hardcoded defaults to avoid API call on cold boot
        result = dict(DEFAULT_ICONS)
        self._cache = result
        self._cache_expiry = time.time() + CACHE_TTL

        # Persist defaults to DB so future boots use DB
        if db is not None:
            await db.save_coin_icons(result)

        # Refresh from CoinGecko in the background (best-effort)
        coin_ids = list(SYMBOL_TO_ID.values())
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    COINGECKO_API,
                    params={"vs_currency": "usd", "ids": ",".join(coin_ids), "order": "market_cap_desc", "per_page": "250", "sparkline": "false"},
                )
                resp.raise_for_status()
                for coin in resp.json():
                    sym = coin.get("symbol", "").upper() + "USDT"
                    img = coin.get("image", "")
                    if img:
                        result[sym] = img
                self._cache = result
                if db is not None:
                    await db.save_coin_icons(result)
        except Exception:
            pass  # default icons already set, no need to fail

        return result


coin_icons_client = CoinIconsClient()
