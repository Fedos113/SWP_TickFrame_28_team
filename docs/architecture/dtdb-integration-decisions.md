# DT/DB Integration Architecture Report

## Scope

The ML service now supports two independent XGBoost detectors in one
`/predict` request:

- existing H&S detector: Classic H&S and Inverse H&S;
- new DT/DB detector: Double Top and Double Bottom.

The original H&S model artifact was not opened during this work.

## Source of the DT/DB contract

The authoritative source was:

`temporal_pipeline_files/doubleTop_DoubleBottom_detection.ipynb`

The model expects 18 features in this exact order:

1. `NATR_14`
2. `Trend_50`
3. `Range_Position`
4. `H_Idx_1`
5. `L_Idx_1`
6. `H_Prc_1`
7. `L_Prc_1`
8. `H_Idx_2`
9. `L_Idx_2`
10. `H_Prc_2`
11. `L_Prc_2`
12. `DT_Width`
13. `DB_Width`
14. `DT_Symmetry_Prc`
15. `DB_Symmetry_Prc`
16. `DT_Peak_Dominance`
17. `DB_Valley_Dominance`
18. `Window_Range_ATR_Pct`

The model metadata confirms three classes and 18 input features:

- class `0`: Noise;
- class `1`: Double Top;
- class `2`: Double Bottom.

## Feature pipeline isolation

H&S and DT/DB do not share a single feature builder. This prevents a
seemingly compatible column count from hiding an incompatible feature order or
normalization rule.

- H&S continues to use `add_smart_features`.
- DT/DB uses `add_dtdb_features`.
- DT/DB widths are normalized by the 50-candle window, as in training.
- DT/DB uses two extrema per side, not the three extrema used by H&S.
- DT/DB returns its first fully valid row after the second 50-candle rolling
  operation, which requires 99 input candles.

## Model lifecycle

Both models are loaded during FastAPI startup:

```text
startup
  ├── load H&S model
  └── load DT/DB model
```

Startup fails explicitly if either model artifact is missing. `/health`
reports the status of both detectors.

## Parallel inference

One `/predict` request creates two independent workers using
`ThreadPoolExecutor(max_workers=2)`. Each worker performs:

1. its own feature extraction;
2. strict feature-order selection;
3. `predict_proba`;
4. detector-specific thresholding;
5. NMS.

The results are combined only after both workers complete.

## Thresholds

H&S production thresholds remain:

- Classic H&S: `0.60`;
- Inverse H&S: `0.65`.

DT/DB currently uses the explicit values from its pipeline configuration:

- Double Top: `0.75`;
- Double Bottom: `0.80`.

The DT/DB notebook can also select thresholds through calibration when
`is_custom_threshold=False`. No calibration JSON artifact was found in the
repository, so runtime calibration was not introduced.

## NMS and tolerance

Runtime inference uses NMS:

- process each class separately;
- group predictions whose distance is at most 10 candles;
- keep the prediction with the highest class probability.

The training notebook's tolerance functions have a different purpose:

- `apply_label_tolerance` expands labels during training;
- `get_tolerant_indices` performs one-to-one TP/FP/FN matching;
- `evaluate_event_level` groups predictions into events and measures event
  precision/recall;
- `EVENT_GAP=35` is an evaluation grouping parameter.

These evaluation functions require ground-truth labels and therefore are not
applied to live API output. Applying them at runtime would be incorrect because
the API has no ground truth.

## API compatibility

The existing request shape remains OHLCV candles plus symbol and timeframe.

The response keeps:

- `timestamp`;
- `pattern_type`;
- `confidence`.

It adds:

```json
{
  "detector": "hs"
}
```

or:

```json
{
  "detector": "dtdb"
}
```

The backend preserves this field in `/api/analyze/{symbol}`. Existing clients
that ignore unknown fields remain compatible.

## Candle validation

The minimum request size is 99 candles. This is required by the DT/DB
pipeline's second rolling window. The backend client and `/api/analyze`
validation use the same minimum.

## CLI model test

`ml_service/app/test_dual_model_cli.py` provides a command-line smoke/load
test. It:

1. fetches 1000 candles through CCXT;
2. repeats that batch 10 times;
3. sends 10,000 candles to `/predict`;
4. reports latency, processed rows, detector counts, and pattern counts.

Example:

```powershell
cd ml_service
python -m app.test_dual_model_cli
```

The repeated candles intentionally create synthetic boundaries. This test
checks API availability, payload size, model execution, and response format;
it is not an accuracy benchmark.

## Feature-engineering performance

The main bottleneck was the Python loop that selected two or three extrema
inside every rolling window. XGBoost inference itself was not the dominant
cost.

The runtime implementation now:

- compiles the extrema loop with Numba when it is installed;
- keeps a pure Python/NumPy fallback for environments without Numba;
- computes `NATR`, `Trend`, `Range_Position`, and extrema once per request;
- shares those arrays between the parallel H&S and DT/DB builders;
- keeps `cache=True` so compiled Numba code can be reused after process warmup.
- warms the kernel during ML-service startup so the first API request avoids
  the JIT compilation delay.

On the Windows development environment, 10,000 synthetic candles required
approximately 42 ms for the shared feature pipeline after JIT warmup. The
first call in a fresh process can be slower because Numba compiles the kernel.
The API contract, feature order, thresholds, and model behavior are unchanged.

## Local-only project assets

- `temporal_pipeline_files/` remains excluded by `.gitignore`;
- `.cursor/` remains excluded by `.gitignore`;
- `.cursorignore` excludes generated and binary artifacts;
- no commits, pushes, or authorship metadata were created.

## Verification status

Passed:

- DT/DB feature contract test;
- DT/DB threshold test;
- direct prediction against the uploaded DT/DB model;
- Python AST parsing;
- IDE linter checks;
- whitespace validation.

Not run successfully in the current host environment:

- full FastAPI endpoint smoke test because `fastapi` is not installed locally;
- full repository pytest run because `pytest_asyncio` is not installed locally.

Both dependencies are declared in the project requirements and are expected
to be available in the Docker environment.
