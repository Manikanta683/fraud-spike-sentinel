#!/usr/bin/env bash
set -e
python3 -m venv .venv 2>/dev/null || true
source .venv/bin/activate
python -m pip install -r requirements.txt
[ -f data/transactions.csv ] || python scripts/generate_data.py --rows 50000
[ -f models/fraud_model.joblib ] || python scripts/train.py
uvicorn app.api:app --reload
