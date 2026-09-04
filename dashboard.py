import json
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "transactions.csv"
METRICS = ROOT / "models" / "metrics.json"

st.set_page_config(page_title="Fraud-Spike Sentinel", page_icon="🛡️", layout="wide")

st.title("🛡️ Fraud-Spike Sentinel")
st.caption("Defense-only fraud detection, bounded investigation and auditability.")

if not DATA.exists() or not METRICS.exists():
    st.warning("Run the data generation and training commands from README.md first.")
    st.stop()

df = pd.read_csv(DATA)
metrics = json.loads(METRICS.read_text())

c1, c2, c3, c4 = st.columns(4)
c1.metric("Transactions", f"{len(df):,}")
c2.metric("Fraud rate", f"{df.is_fraud.mean():.2%}")
c3.metric("Precision", f"{metrics['precision']:.2%}")
c4.metric("Recall", f"{metrics['recall']:.2%}")

st.subheader("Fraud activity overview")
hourly = df.groupby("hour").is_fraud.mean().reset_index()
st.line_chart(hourly.set_index("hour"))

st.subheader("Investigate a transaction")
with st.form("investigate"):
    amount = st.number_input("Amount", min_value=1.0, value=12500.0)
    hour = st.slider("Hour", 0, 23, 2)
    customer_txn_count_24h = st.number_input("Customer transactions / 24h", min_value=0, value=12)
    customer_avg_amount = st.number_input("Customer average amount", min_value=1.0, value=1800.0)
    device_txn_count_1h = st.number_input("Device transactions / 1h", min_value=0, value=18)
    device_customer_count = st.number_input("Customers using device", min_value=0, value=7)
    location_distance_km = st.number_input("Location distance (km)", min_value=0.0, value=950.0)
    is_new_device = st.checkbox("New device", value=True)
    is_new_location = st.checkbox("New location", value=True)
    merchant_fraud_rate_7d = st.number_input(
        "Merchant fraud rate (7d)", min_value=0.0, max_value=1.0, value=0.08, step=0.01
    )

    submitted = st.form_submit_button("Run investigation")

if submitted:
    payload = {
        "amount": amount,
        "hour": hour,
        "customer_txn_count_24h": customer_txn_count_24h,
        "customer_avg_amount": customer_avg_amount,
        "device_txn_count_1h": device_txn_count_1h,
        "device_customer_count": device_customer_count,
        "location_distance_km": location_distance_km,
        "is_new_device": int(is_new_device),
        "is_new_location": int(is_new_location),
        "merchant_fraud_rate_7d": merchant_fraud_rate_7d,
    }

    try:
        response = requests.post("http://127.0.0.1:8000/investigate", json=payload, timeout=5)
        response.raise_for_status()
        result = response.json()

        st.metric("Risk score", f"{result['risk_score']:.1%}")
        st.subheader(f"Decision: {result['decision']}")

        st.write("**Investigation reasons**")
        for reason in result["reasons"]:
            st.write(f"- {reason}")

        st.write("**Stopping rule**")
        st.info(result["stopping_rule"])

        st.write("**Audit event**")
        st.json(result["audit"])

    except requests.RequestException:
        st.error("API is not running. Start it with: uvicorn app.api:app --reload")
