from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from app.config import WINDOW_SIZE

try:
    from numba import njit
except ImportError:  # pragma: no cover - only used without optional Numba
    njit = None


def _prepare_common_features(
    df: pd.DataFrame,
    window_size: int,
    natr_window: int,
) -> tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    """Build OHLC-derived columns shared by both detector pipelines."""
    data = df.copy()
    rename_dict = {
        col: col.capitalize()
        for col in data.columns
        if col.lower() in {"open", "high", "low", "close", "volume"}
    }
    data.rename(columns=rename_dict, inplace=True)

    prev_close = data["Close"].shift(1)
    true_range = pd.concat(
        [
            data["High"] - data["Low"],
            abs(data["High"] - prev_close),
            abs(data["Low"] - prev_close),
        ],
        axis=1,
    ).max(axis=1)
    data[f"NATR_{natr_window}"] = (
        true_range.rolling(natr_window).mean() / data["Close"]
    )
    data[f"Trend_{window_size}"] = (
        data["Close"] / data["Close"].shift(window_size) - 1
    )
    min_window = data["Low"].rolling(window_size).min()
    max_window = data["High"].rolling(window_size).max()
    data["Range_Position"] = (
        (data["Close"] - min_window) / (max_window - min_window + 1e-8)
    )
    return data, data["High"].to_numpy(), data["Low"].to_numpy()


def _find_extrema_python(
    high_prices: np.ndarray,
    low_prices: np.ndarray,
    window_size: int,
    min_dist: int,
    extrema_count: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Portable fallback that preserves the training-pipeline behavior."""
    n_windows = len(high_prices) - window_size + 1
    high_indices = np.zeros((n_windows, extrema_count))
    high_values = np.zeros((n_windows, extrema_count))
    low_indices = np.zeros((n_windows, extrema_count))
    low_values = np.zeros((n_windows, extrema_count))

    for i in range(n_windows):
        for prices, indices, values, choose_max in (
            (high_prices, high_indices, high_values, True),
            (low_prices, low_indices, low_values, False),
        ):
            available = np.ones(window_size, dtype=bool)
            window = prices[i : i + window_size]
            for step in range(extrema_count):
                if not np.any(available):
                    break
                index = (
                    int(np.argmax(np.where(available, window, -np.inf)))
                    if choose_max
                    else int(np.argmin(np.where(available, window, np.inf)))
                )
                indices[i, step] = window_size - index
                values[i, step] = window[index]
                available[
                    max(0, index - min_dist) : min(
                        window_size, index + min_dist + 1
                    )
                ] = False

    return high_indices, high_values, low_indices, low_values


if njit is not None:

    @njit(cache=True)
    def _find_extrema_numba(
        high_prices,
        low_prices,
        window_size,
        min_dist,
        extrema_count,
    ):
        """Compile the hot extrema loop to native code on Windows/Linux."""
        n_windows = len(high_prices) - window_size + 1
        high_indices = np.zeros((n_windows, extrema_count))
        high_values = np.zeros((n_windows, extrema_count))
        low_indices = np.zeros((n_windows, extrema_count))
        low_values = np.zeros((n_windows, extrema_count))

        for i in range(n_windows):
            high_available = np.ones(window_size, dtype=np.bool_)
            low_available = np.ones(window_size, dtype=np.bool_)
            for step in range(extrema_count):
                best_high_index = -1
                best_high_value = -np.inf
                best_low_index = -1
                best_low_value = np.inf

                for offset in range(window_size):
                    if high_available[offset]:
                        high_value = high_prices[i + offset]
                        if high_value > best_high_value:
                            best_high_value = high_value
                            best_high_index = offset
                    if low_available[offset]:
                        low_value = low_prices[i + offset]
                        if low_value < best_low_value:
                            best_low_value = low_value
                            best_low_index = offset

                high_indices[i, step] = window_size - best_high_index
                high_values[i, step] = best_high_value
                low_indices[i, step] = window_size - best_low_index
                low_values[i, step] = best_low_value

                high_start = max(0, best_high_index - min_dist)
                high_end = min(window_size, best_high_index + min_dist + 1)
                low_start = max(0, best_low_index - min_dist)
                low_end = min(window_size, best_low_index + min_dist + 1)
                for offset in range(high_start, high_end):
                    high_available[offset] = False
                for offset in range(low_start, low_end):
                    low_available[offset] = False

        return high_indices, high_values, low_indices, low_values


def _find_extrema(
    high_prices: np.ndarray,
    low_prices: np.ndarray,
    window_size: int,
    min_dist: int,
    extrema_count: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Use compiled extrema search, with a compatible fallback."""
    if njit is not None:
        return _find_extrema_numba(
            high_prices,
            low_prices,
            window_size,
            min_dist,
            extrema_count,
        )
    return _find_extrema_python(
        high_prices,
        low_prices,
        window_size,
        min_dist,
        extrema_count,
    )


def warmup_feature_engineering(window_size: int = WINDOW_SIZE) -> None:
    """Compile the Numba kernel during service startup, not the first request."""
    if njit is None:
        return
    sample_size = window_size + 2
    sample = np.linspace(100.0, 101.0, sample_size)
    _find_extrema(
        sample,
        sample,
        window_size=window_size,
        min_dist=max(2, window_size // 10),
        extrema_count=3,
    )


def _sort_extrema(
    high_indices: np.ndarray,
    high_values: np.ndarray,
    low_indices: np.ndarray,
    low_values: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Sort extrema chronologically, matching the training pipeline."""
    high_order = np.argsort(-high_indices, axis=1)
    low_order = np.argsort(-low_indices, axis=1)
    return (
        np.take_along_axis(high_indices, high_order, axis=1),
        np.take_along_axis(high_values, high_order, axis=1),
        np.take_along_axis(low_indices, low_order, axis=1),
        np.take_along_axis(low_values, low_order, axis=1),
    )


@dataclass(frozen=True)
class SharedFeatureSet:
    """Immutable-in-practice inputs reused by H&S and DT/DB builders."""

    data: pd.DataFrame
    high_indices: np.ndarray
    high_values: np.ndarray
    low_indices: np.ndarray
    low_values: np.ndarray


def prepare_shared_features(
    df: pd.DataFrame,
    window_size: int = WINDOW_SIZE,
) -> SharedFeatureSet:
    """Compute common metrics and three extrema once per API request."""
    natr_window = max(5, int(window_size * 0.28))
    data, high_prices, low_prices = _prepare_common_features(
        df,
        window_size=window_size,
        natr_window=natr_window,
    )
    extrema = _find_extrema(
        high_prices,
        low_prices,
        window_size=window_size,
        min_dist=max(2, window_size // 10),
        extrema_count=3,
    )
    high_indices, high_values, low_indices, low_values = _sort_extrema(*extrema)
    return SharedFeatureSet(
        data=data,
        high_indices=high_indices,
        high_values=high_values,
        low_indices=low_indices,
        low_values=low_values,
    )


def add_smart_features(
    df: pd.DataFrame,
    shared: SharedFeatureSet | None = None,
) -> pd.DataFrame:
    """Create the H&S feature contract without changing its formulas."""
    window_size = WINDOW_SIZE
    natr_window = max(5, int(window_size * 0.28))
    shared = shared or prepare_shared_features(df, window_size)
    data = shared.data.copy()
    high_indices = shared.high_indices
    high_values = shared.high_values
    low_indices = shared.low_indices
    low_values = shared.low_values

    data = data.iloc[window_size - 1 :].copy()
    current_closes = data["Close"].to_numpy()
    current_atr_usd = data[f"NATR_{natr_window}"].to_numpy() * current_closes + 1e-8
    for step in range(3):
        data[f"H_Idx_{step + 1}"] = high_indices[:, step].astype(int)
        data[f"L_Idx_{step + 1}"] = low_indices[:, step].astype(int)
        data[f"H_Prc_{step + 1}"] = (
            high_values[:, step] - current_closes
        ) / current_atr_usd
        data[f"L_Prc_{step + 1}"] = (
            current_closes - low_values[:, step]
        ) / current_atr_usd

    data["Width_Left_H"] = data["H_Idx_1"] - data["H_Idx_2"]
    data["Width_Right_H"] = data["H_Idx_2"] - data["H_Idx_3"]
    data["Width_Left_L"] = data["L_Idx_1"] - data["L_Idx_2"]
    data["Width_Right_L"] = data["L_Idx_2"] - data["L_Idx_3"]
    data["Time_Sym_Classic"] = abs(
        data["Width_Left_H"] - data["Width_Right_H"]
    ) / (data["Width_Left_H"] + data["Width_Right_H"] + 1e-8)
    data["Time_Sym_Inv"] = abs(
        data["Width_Left_L"] - data["Width_Right_L"]
    ) / (data["Width_Left_L"] + data["Width_Right_L"] + 1e-8)
    data["Head_Dom_Classic"] = data["H_Prc_2"] - data[
        ["H_Prc_1", "H_Prc_3"]
    ].max(axis=1)
    data["Shoulder_Sym_Classic"] = abs(data["H_Prc_1"] - data["H_Prc_3"])
    data["Neck_Slope_Classic"] = (
        data["L_Prc_2"] - data["L_Prc_1"]
    ) / (data["Width_Left_L"] + 1e-8)
    data["Head_Dom_Inv"] = data["L_Prc_2"] - data[
        ["L_Prc_1", "L_Prc_3"]
    ].max(axis=1)
    data["Shoulder_Sym_Inv"] = abs(data["L_Prc_1"] - data["L_Prc_3"])
    data["Neck_Slope_Inv"] = (
        data["H_Prc_2"] - data["H_Prc_1"]
    ) / (data["Width_Left_H"] + 1e-8)

    columns_to_drop = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "head_shoulder_format",
        "Target",
    ]
    for step in range(3):
        columns_to_drop.extend([f"H_Idx_{step + 1}", f"L_Idx_{step + 1}"])
    columns_to_drop.extend(["H_Prc_1", "H_Prc_3", "L_Prc_1", "L_Prc_3"])
    data.drop(
        columns=[column for column in columns_to_drop if column in data.columns],
        inplace=True,
    )
    data.dropna(inplace=True)
    return data


def add_dtdb_features(
    df: pd.DataFrame,
    window_size: int = 50,
    shared: SharedFeatureSet | None = None,
) -> pd.DataFrame:
    """Create the 18-column DT/DB contract from the training pipeline."""
    shared = shared or prepare_shared_features(df, window_size)
    data = shared.data.copy()
    high_indices = shared.high_indices
    high_values = shared.high_values
    low_indices = shared.low_indices
    low_values = shared.low_values

    # DT/DB needs only two extrema. The shared three-extrema result above
    # prevents the two detectors from repeating the same expensive search.
    high_indices = high_indices[:, :2]
    high_values = high_values[:, :2]
    low_indices = low_indices[:, :2]
    low_values = low_values[:, :2]

    data = data.iloc[window_size - 1 :].copy()
    current_closes = data["Close"].to_numpy()
    current_atr_usd = data["NATR_14"].to_numpy() * current_closes + 1e-8
    for step in range(2):
        data[f"H_Idx_{step + 1}"] = high_indices[:, step].astype(int)
        data[f"L_Idx_{step + 1}"] = low_indices[:, step].astype(int)
        data[f"H_Prc_{step + 1}"] = (
            high_values[:, step] - current_closes
        ) / current_atr_usd
        data[f"L_Prc_{step + 1}"] = (
            current_closes - low_values[:, step]
        ) / current_atr_usd

    data["DT_Width"] = (
        data["H_Idx_1"] - data["H_Idx_2"]
    ) / window_size
    data["DB_Width"] = (
        data["L_Idx_1"] - data["L_Idx_2"]
    ) / window_size
    data["DT_Symmetry_Prc"] = abs(data["H_Prc_1"] - data["H_Prc_2"])
    data["DB_Symmetry_Prc"] = abs(data["L_Prc_1"] - data["L_Prc_2"])
    data["DT_Peak_Dominance"] = (
        ((high_values[:, 0] + high_values[:, 1]) / 2 - current_closes)
        / current_atr_usd
    )
    data["DB_Valley_Dominance"] = (
        (current_closes - (low_values[:, 0] + low_values[:, 1]) / 2)
        / current_atr_usd
    )
    rolling_max = data["High"].rolling(window_size).max().to_numpy()
    rolling_min = data["Low"].rolling(window_size).min().to_numpy()
    data["Window_Range_ATR_Pct"] = (
        (rolling_max - rolling_min) / current_atr_usd
    ) * 100
    return data.dropna()
