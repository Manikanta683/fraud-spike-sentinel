@echo off
if not exist .venv (
  python -m venv .venv
)
call .venv\Scripts\activate
python -m pip install -r requirements.txt
if not exist data\transactions.csv python scripts\generate_data.py --rows 50000
if not exist models\fraud_model.joblib python scripts/train.py
start "Fraud API" cmd /k "uvicorn app.api:app --reload"
start "Fraud Dashboard" cmd /k "streamlit run dashboard.py"
