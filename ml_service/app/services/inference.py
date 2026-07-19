import numpy as np
from app.config import (
    DTDB_THRESHOLD_DB,
    DTDB_THRESHOLD_DT,
    THRESHOLD_CLASSIC_HS,
    THRESHOLD_INVERSE_HS,
    TOLERANCE_WINDOW,
)

def apply_pattern_thresholds(probas: np.ndarray) -> np.ndarray:
    """
    Applies separate business probability thresholds for Classic and Inverse H&S.
    """
    y_pred_raw = np.zeros(len(probas), dtype=int)

    for i, proba in enumerate(probas):
        p_classic = proba[1]
        p_inverse = proba[2]

        if p_classic >= THRESHOLD_CLASSIC_HS and p_classic >= p_inverse:
            y_pred_raw[i] = 1
        elif p_inverse >= THRESHOLD_INVERSE_HS and p_inverse > p_classic:
            y_pred_raw[i] = 2

    return y_pred_raw


def apply_dtdb_thresholds(
    probas: np.ndarray,
    threshold_dt: float = DTDB_THRESHOLD_DT,
    threshold_db: float = DTDB_THRESHOLD_DB,
) -> np.ndarray:
    """Apply independent DT and DB confidence thresholds."""
    y_pred_raw = np.zeros(len(probas), dtype=int)
    prob_dt = probas[:, 1]
    prob_db = probas[:, 2]
    y_pred_raw[(prob_dt >= threshold_dt) & (prob_dt > prob_db)] = 1
    y_pred_raw[(prob_db >= threshold_db) & (prob_db > prob_dt)] = 2
    return y_pred_raw


def apply_nms_clustering(
    y_pred: np.ndarray,
    probas: np.ndarray,
    tolerance_window: int = TOLERANCE_WINDOW,
) -> np.ndarray:
    """
    Collapses multiple consecutive triggers into a single peak signal
    based on the highest model confidence.
    """
    y_pred = np.asarray(y_pred).astype(int)
    y_clean = np.zeros_like(y_pred)
    classes = np.unique(y_pred)
    classes = classes[classes != 0]

    for cls in classes:
        idxs = np.where(y_pred == cls)[0]
        if idxs.size == 0:
            continue

        k = 0
        while k < len(idxs):
            cluster = [idxs[k]]
            k += 1
            while k < len(idxs) and (idxs[k] - idxs[k-1]) <= tolerance_window:
                cluster.append(idxs[k])
                k += 1

            probs_cluster = probas[cluster, cls]
            best_rel = int(np.argmax(probs_cluster))
            best_idx = cluster[best_rel]
            y_clean[best_idx] = cls

    return y_clean
