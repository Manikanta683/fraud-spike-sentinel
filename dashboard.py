import json
from pathlib import Path

import pandas as pd
import streamlit as st

from app.investigator import investigate
from app.model_service import predict

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "transactions.csv"
MODEL = ROOT / "models" / "fraud_model.joblib"
METRICS = ROOT / "models" / "metrics.json"

st.set_page_config(page_title="Fraud-Spike Sentinel", page_icon="🛡️", layout="wide")

st.title("🛡️ Fraud-Spike Sentinel")
st.caption("Defense-only fraud detection, bounded investigation and auditability.")

# Streamlit Cloud does not retain generated files from the development machine.
# Bootstrap a small synthetic dataset and train the model on first launch.
if not DATA.exists() or not MODEL.exists() or not METRICS.exists():
    with st.spinner("Preparing the synthetic fraud-detection model for this demo..."):
        from scripts.generate_data import generate
        from scripts.train import main as train_model

        DATA.parent.mkdir(exist_ok=True)
        MODEL.parent.mkdir(exist_ok=True)
        if not DATA.exists():
            generate(50000)
        if not MODEL.exists() or not METRICS.exists():
            train_model()
    st.success("Demo model is ready.")

@st.cache_data

def load_demo_data():
    return pd.read_csv(DATA)

@st.cache_data

def load_metrics():
    return json.loads(METRICS.read_text())


df = load_demo_data()
metrics = load_metrics()

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
        risk_score = predict(payload)
        result = investigate(payload, risk_score)

        st.metric("Risk score", f"{result['risk_score']:.1%}")
        st.subheader(f"Decision: {result['decision']}")

        st.write("**Investigation reasons**")
        for reason in result["reasons"]:
            st.write(f"- {reason}")

        st.write("**Stopping rule**")
        st.info(result["stopping_rule"])

        st.write("**Audit event**")
        st.json(result["audit"])
    except Exception as exc:
        st.error(f"Investigation failed: {exc}")
