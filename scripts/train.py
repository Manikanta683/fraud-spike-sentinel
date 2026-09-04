from pathlib import Path
import json
import joblib
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    average_precision_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "transactions.csv"
MODEL_DIR = ROOT / "models"

FEATURES = [
    "amount", "hour", "customer_txn_count_24h", "customer_avg_amount",
    "device_txn_count_1h", "device_customer_count", "location_distance_km",
    "is_new_device", "is_new_location", "merchant_fraud_rate_7d",
]

def main():
    if not DATA.exists():
        raise SystemExit("Dataset missing. Run scripts/generate_data.py first.")

    df = pd.read_csv(DATA)
    X = df[FEATURES]
    y = df["is_fraud"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)),
    ])
    model.fit(X_train, y_train)

    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= 0.50).astype(int)

    metrics = {
        "precision": precision_score(y_test, predictions, zero_division=0),
        "recall": recall_score(y_test, predictions, zero_division=0),
        "f1": f1_score(y_test, predictions, zero_division=0),
        "pr_auc": average_precision_score(y_test, probabilities),
        "confusion_matrix": confusion_matrix(y_test, predictions).tolist(),
        "classification_report": classification_report(y_test, predictions, output_dict=True, zero_division=0),
        "train_rows": len(X_train), "test_rows": len(X_test),
        "positive_rate_test": float(y_test.mean()),
    }

    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_DIR / "fraud_model.joblib")
    with open(MODEL_DIR / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print("\n=== Held-out test metrics ===")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall:    {metrics['recall']:.4f}")
    print(f"F1:        {metrics['f1']:.4f}")
    print(f"PR-AUC:    {metrics['pr_auc']:.4f}")
    print(f"Test rows: {metrics['test_rows']:,}")
    print("\nConfusion matrix:")
    print(metrics["confusion_matrix"])

if __name__ == "__main__":
    main()
