import argparse
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def generate(rows: int, seed: int = 42):
    rng = np.random.default_rng(seed)
    fraud = rng.binomial(1, 0.055, rows)

    customer_avg = np.exp(rng.normal(np.log(1800), 0.65, rows))
    amount_ratio = np.where(
        fraud,
        rng.lognormal(np.log(1.9), 0.55, rows),
        rng.lognormal(np.log(1.05), 0.55, rows),
    )
    amount = np.maximum(50, customer_avg * amount_ratio)

    hour = rng.integers(0, 24, rows)
    customer_txn = np.where(fraud, rng.poisson(5.0, rows), rng.poisson(2.8, rows))
    device_txn = np.where(fraud, rng.poisson(6.0, rows), rng.poisson(2.0, rows))
    device_customers = np.where(fraud, 1 + rng.poisson(2.0, rows), 1 + rng.poisson(0.55, rows))
    distance = np.where(fraud, rng.exponential(220, rows), rng.exponential(65, rows))
    new_device = np.where(fraud, rng.binomial(1, 0.55, rows), rng.binomial(1, 0.08, rows))
    new_location = np.where(fraud, rng.binomial(1, 0.60, rows), rng.binomial(1, 0.10, rows))
    merchant_rate = np.clip(
        np.where(fraud, rng.beta(2.2, 25, rows), rng.beta(1.3, 45, rows)), 0, 1
    )

    noise_mask = rng.random(rows) < 0.03
    amount[noise_mask] *= rng.uniform(0.7, 1.4, noise_mask.sum())
    distance[noise_mask] *= rng.uniform(0.6, 1.5, noise_mask.sum())

    df = pd.DataFrame({
        "amount": amount.round(2),
        "hour": hour,
        "customer_txn_count_24h": customer_txn,
        "customer_avg_amount": customer_avg.round(2),
        "device_txn_count_1h": device_txn,
        "device_customer_count": device_customers,
        "location_distance_km": distance.round(2),
        "is_new_device": new_device,
        "is_new_location": new_location,
        "merchant_fraud_rate_7d": merchant_rate.round(5),
        "is_fraud": fraud.astype(int),
    })

    out = ROOT / "data" / "transactions.csv"
    out.parent.mkdir(exist_ok=True)
    df.to_csv(out, index=False)
    print(f"Wrote {len(df):,} transactions to {out}")
    print(f"Fraud rate: {df.is_fraud.mean():.2%}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=50000)
    args = parser.parse_args()
    generate(args.rows)
