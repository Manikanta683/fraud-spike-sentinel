# Fraud-Spike Sentinel

A defense-only AI/ML system for detecting unusual fraud activity and investigating high-risk transactions.

## What it demonstrates

- Synthetic transaction generation
- Leakage-safe train/test split
- Fraud classification with precision, recall, F1 and PR-AUC
- Risk scoring
- Explainable investigation reasons
- Bounded investigation workflow
- Audit trail
- FastAPI backend
- Streamlit dashboard

> This project uses synthetic data. It does not connect to live payment systems and does not perform offensive security activity.

## Project structure

```text
fraud-spike-sentinel/
├── app/
│   ├── api.py
│   ├── investigator.py
│   └── model_service.py
├── data/
├── models/
├── scripts/
│   ├── generate_data.py
│   └── train.py
├── tests/
│   └── test_investigator.py
├── dashboard.py
├── requirements.txt
└── .gitignore
```

## Quick start

### 1. Create an environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate synthetic transactions

```bash
python scripts/generate_data.py --rows 50000
```

### 4. Train the model

```bash
python scripts/train.py
```

This creates:

- `models/fraud_model.joblib`
- `models/metrics.json`

### 5. Quick launch on Windows

After installing Python, you can also run `run_project.bat` to install dependencies, prepare the model, and open the API/dashboard in separate terminals.

### 6. Start the API

```bash
uvicorn app.api:app --reload
```

API docs:

`http://127.0.0.1:8000/docs`

### 7. Start the dashboard

In another terminal:

```bash
streamlit run dashboard.py
```

Then open the local Streamlit URL shown in the terminal.

## Example API request

```json
{
  "amount": 12500,
  "hour": 2,
  "customer_txn_count_24h": 12,
  "customer_avg_amount": 1800,
  "device_txn_count_1h": 18,
  "device_customer_count": 7,
  "location_distance_km": 950,
  "is_new_device": 1,
  "is_new_location": 1,
  "merchant_fraud_rate_7d": 0.08
}
```

## Interview talking points

1. Why precision/recall matter more than raw accuracy for imbalanced fraud data.
2. Why the test set is held out from model training.
3. How false positives create merchant/customer friction.
4. Why the investigation workflow is bounded and auditable.
5. How the system could be extended with real payment-provider data without changing the core architecture.

## Important

Do not claim the example metrics in screenshots or presentations. Run the training script and use the metrics actually produced by the held-out test set.
