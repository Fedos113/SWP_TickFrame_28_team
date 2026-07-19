"""No-argument CLI smoke/load test for the dual-model ML API.

This intentionally repeats one fetched candle batch. It validates request size,
API availability, both detector labels, and response latency; it is not an
accuracy benchmark because repeated timestamps create synthetic boundaries.

Run from ``ml_service``:

    python app/test_dual_model_cli.py

Edit ``CONFIG`` below to change the default run settings. Command-line options
remain available as optional overrides.
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from collections import Counter
from dataclasses import dataclass
from typing import Any

import ccxt
import requests


@dataclass(frozen=True)
class DualModelCliConfig:
    """Default settings for a no-argument local CLI run."""

    api_url: str = os.getenv("ML_API_URL", "http://127.0.0.1:8001/predict")
    symbol: str = "BTC/USDT"
    timeframe: str = "5m"
    base_candles: int = 1000
    copies: int = 1
    timeout: float = 120.0


CONFIG = DualModelCliConfig()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch candles with CCXT and smoke-test both ML detectors."
    )
    parser.add_argument(
        "--api-url",
        default=CONFIG.api_url,
        help="ML /predict URL",
    )
    parser.add_argument("--symbol", default=CONFIG.symbol, help="CCXT symbol")
    parser.add_argument(
        "--timeframe",
        default=CONFIG.timeframe,
        help="Candle timeframe",
    )
    parser.add_argument(
        "--base-candles",
        type=int,
        default=CONFIG.base_candles,
        help="Number of candles fetched from the exchange",
    )
    parser.add_argument(
        "--copies",
        type=int,
        default=CONFIG.copies,
        help="Number of times to repeat the fetched candle batch",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=CONFIG.timeout,
        help="HTTP timeout in seconds",
    )
    return parser.parse_args()


def fetch_candles(symbol: str, timeframe: str, limit: int) -> list[dict[str, Any]]:
    exchange = ccxt.binance({"enableRateLimit": True})
    rows = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    if len(rows) < limit:
        raise RuntimeError(
            f"Exchange returned {len(rows)} candles, expected {limit}."
        )

    return [
        {
            "timestamp": int(timestamp),
            "open": float(open_price),
            "high": float(high),
            "low": float(low),
            "close": float(close),
            "volume": float(volume),
        }
        for timestamp, open_price, high, low, close, volume in rows
    ]


def main() -> int:
    args = parse_args()
    test_started = time.perf_counter()
    if args.base_candles < 1 or args.copies < 1:
        print("--base-candles and --copies must be positive.", file=sys.stderr)
        return 2

    try:
        fetch_started = time.perf_counter()
        base_candles = fetch_candles(
            symbol=args.symbol,
            timeframe=args.timeframe,
            limit=args.base_candles,
        )
        fetch_ms = (time.perf_counter() - fetch_started) * 1000
        candles = base_candles * args.copies
        payload = {
            "symbol": args.symbol.replace("/", ""),
            "timeframe": args.timeframe,
            "candles": candles,
        }

        print(
            f"Fetched {len(base_candles)} candles from Binance; "
            f"sending {len(candles)} candles ({args.copies} copies)."
        )
        request_started = time.perf_counter()
        response = requests.post(args.api_url, json=payload, timeout=args.timeout)
        round_trip_ms = (time.perf_counter() - request_started) * 1000
        response.raise_for_status()
        data = response.json()
    except (ccxt.BaseError, requests.RequestException, ValueError, RuntimeError) as exc:
        print(f"Dual-model CLI test failed: {exc}", file=sys.stderr)
        return 1

    patterns = data.get("patterns_found", [])
    processing_ms = data.get("processing_ms", {})
    full_wall_clock_ms = (time.perf_counter() - test_started) * 1000
    detector_counts = Counter(pattern.get("detector", "unknown") for pattern in patterns)
    type_counts = Counter(pattern.get("pattern_type", "unknown") for pattern in patterns)

    print(f"HTTP status: {response.status_code}")
    print(f"Exchange fetch time: {fetch_ms:.2f} ms")
    print(f"API round-trip time: {round_trip_ms:.2f} ms")
    print(f"Server total analysis time: {processing_ms.get('total_ms', 0.0):.2f} ms")
    print(f"H&S processing time (Classic + Inverse): {processing_ms.get('hs_ms', 0.0):.2f} ms")
    print(f"DT/DB processing time (Double Top + Double Bottom): {processing_ms.get('dtdb_ms', 0.0):.2f} ms")
    print(f"Full CLI wall-clock time: {full_wall_clock_ms:.2f} ms")
    print(f"Processed candles: {data.get('processed_candles')}")
    print(f"Patterns found: {len(patterns)}")
    print(f"By detector: {dict(detector_counts)}")
    print(f"By pattern: {dict(type_counts)}")

    for pattern in patterns[:5]:
        print(
            "  "
            f"{pattern.get('detector', 'unknown')}: "
            f"{pattern.get('pattern_type', 'unknown')} at "
            f"{pattern.get('timestamp')} "
            f"(confidence={pattern.get('confidence', 0.0):.4f})"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
