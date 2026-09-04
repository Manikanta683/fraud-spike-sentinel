from datetime import datetime, timezone

def investigate(txn: dict, risk_score: float) -> dict:
    """Bounded, defense-only investigation. No blocking or financial action is executed."""
    reasons = []

    if txn["device_txn_count_1h"] >= 10:
        reasons.append("High transaction velocity from the device")

    if txn["device_customer_count"] >= 4:
        reasons.append("Device is associated with multiple customers")

    if txn["is_new_device"]:
        reasons.append("New device for this customer")

    if txn["is_new_location"]:
        reasons.append("New location for this customer")

    if txn["location_distance_km"] >= 500:
        reasons.append("Unusual location distance from prior activity")

    if txn["customer_avg_amount"] > 0 and txn["amount"] >= 3 * txn["customer_avg_amount"]:
        reasons.append("Transaction amount is far above customer baseline")

    if txn["merchant_fraud_rate_7d"] >= 0.05:
        reasons.append("Merchant has elevated recent fraud rate")

    if txn["customer_txn_count_24h"] >= 10:
        reasons.append("Unusually high customer transaction count")

    if risk_score >= 0.80:
        decision = "ESCALATE_FOR_REVIEW"
    elif risk_score >= 0.50:
        decision = "VERIFY"
    else:
        decision = "ALLOW_MONITORING"

    return {
        "risk_score": round(risk_score, 4),
        "decision": decision,
        "reasons": reasons[:6],
        "stopping_rule": "No automated financial action is executed; high-risk cases are escalated for review.",
        "audit": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "workflow": "fraud_investigation_v1",
            "action": decision,
        },
    }
