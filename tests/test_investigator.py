from app.investigator import investigate

def test_high_risk_case_is_escalated():
    txn = {
        "amount": 12000,
        "hour": 2,
        "customer_txn_count_24h": 15,
        "customer_avg_amount": 1500,
        "device_txn_count_1h": 20,
        "device_customer_count": 7,
        "location_distance_km": 900,
        "is_new_device": 1,
        "is_new_location": 1,
        "merchant_fraud_rate_7d": 0.08,
    }
    result = investigate(txn, 0.94)
    assert result["decision"] == "ESCALATE_FOR_REVIEW"
    assert len(result["reasons"]) > 0
    assert "No automated financial action" in result["stopping_rule"]
