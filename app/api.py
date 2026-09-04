from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.model_service import predict
from app.investigator import investigate

app = FastAPI(
    title="Fraud-Spike Sentinel API",
    description="Defense-only fraud risk scoring and bounded investigation API.",
    version="1.0.0",
)

class Transaction(BaseModel):
    amount: float = Field(gt=0)
    hour: int = Field(ge=0, le=23)
    customer_txn_count_24h: int = Field(ge=0)
    customer_avg_amount: float = Field(gt=0)
    device_txn_count_1h: int = Field(ge=0)
    device_customer_count: int = Field(ge=0)
    location_distance_km: float = Field(ge=0)
    is_new_device: int = Field(ge=0, le=1)
    is_new_location: int = Field(ge=0, le=1)
    merchant_fraud_rate_7d: float = Field(ge=0, le=1)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/investigate")
def investigate_transaction(txn: Transaction):
    try:
        payload = txn.model_dump()
        score = predict(payload)
        return investigate(payload, score)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
