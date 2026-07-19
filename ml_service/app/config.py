# Model path config
MODEL_PATH = "models/xgb_hs_detector_MVP1.json"
DTDB_MODEL_PATH = "models/xgb_dtdb_detector.json"

# Sliding window size used during model training
WINDOW_SIZE = 50

# Post-processing configurations
TOLERANCE_WINDOW = 10  # NMS window size

# Model thresholds based on your business metric optimization
THRESHOLD_CLASSIC_HS = 0.60
THRESHOLD_INVERSE_HS = 0.65

# Strict feature ordering expected by the trained XGBoost model
FEATURE_ORDER = [
    "NATR_14",
    "Trend_50",
    "Range_Position",
    "H_Prc_2",
    "L_Prc_2",
    "Width_Left_H",
    "Width_Right_H",
    "Width_Left_L",
    "Width_Right_L",
    "Time_Sym_Classic",
    "Time_Sym_Inv",
    "Head_Dom_Classic",
    "Shoulder_Sym_Classic",
    "Neck_Slope_Classic",
    "Head_Dom_Inv",
    "Shoulder_Sym_Inv",
    "Neck_Slope_Inv"
]

# DT/DB model contract from temporal_pipeline_files pipeline.
DTDB_WINDOW_SIZE = 50
DTDB_MIN_CANDLES = DTDB_WINDOW_SIZE * 2 - 1
DTDB_NMS_WINDOW = 10
DTDB_TOLERANCE_WINDOW = 10
# NOTE: The dtdb XGBoost model's confidence distribution on live 5m market
# data peaks well below the original 0.75/0.80 targets (max ~0.48), so those
# thresholds never triggered and DT/DB were effectively never detected. These
# values are calibrated against the current model so Double Top / Double Bottom
# are surfaced while remaining selective after NMS clustering.
DTDB_THRESHOLD_DT = 0.45
DTDB_THRESHOLD_DB = 0.45

DTDB_FEATURE_ORDER = [
    "NATR_14",
    "Trend_50",
    "Range_Position",
    "H_Idx_1",
    "L_Idx_1",
    "H_Prc_1",
    "L_Prc_1",
    "H_Idx_2",
    "L_Idx_2",
    "H_Prc_2",
    "L_Prc_2",
    "DT_Width",
    "DB_Width",
    "DT_Symmetry_Prc",
    "DB_Symmetry_Prc",
    "DT_Peak_Dominance",
    "DB_Valley_Dominance",
    "Window_Range_ATR_Pct",
]