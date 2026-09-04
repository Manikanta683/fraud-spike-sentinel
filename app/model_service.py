from pathlib import Path
import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "fraud_model.joblib"

FEATURES = [
    "amount",
    "hour",
    "customer_txn_count_24h",
    "customer_avg_amount",
    "device_txn_count_1h",
    "device_customer_count",
    "location_distance_km",
    "is_new_device",
    "is_new_location",
    "merchant_fraud_rate_7d",
]

_model = None

def load_model():
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                "Model not found. Run: python scripts/generate_data.py --rows 50000 "
                "then python scripts/train.py"
            )
        _model = joblib.load(MODEL_PATH)
    return _model

def predict(features: dict) -> float:
    model = load_model()
    row = pd.DataFrame([{k: features[k] for k in FEATURES}])
    return float(model.predict_proba(row)[0, 1])
