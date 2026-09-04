# Fraud-Spike Sentinel

A defense-focused transaction fraud detection and investigation system for identifying unusual activity and routing high-risk transactions for review.

## 🚀 Live Demo

**Try the deployed dashboard:**

👉 https://fraud-spike-sentinel-xbmwp6dsojphyem2hjdgu5.streamlit.app/

The dashboard provides transaction-level risk scoring, investigation reasons, bounded decisions, and an audit event for each investigation.

### Example investigation

![Live investigation result](assets/demo-result.svg)

**Example result:** `100.0%` risk score → `ESCALATE_FOR_REVIEW`

> The example above uses synthetic benchmark data and is intended to demonstrate the project workflow.

## Project capabilities

- Synthetic transaction data generation
- Separate training and test data
- Fraud classification and performance measurement
- Transaction-level risk scoring
- Behavioral investigation reasons
- Three-level investigation workflow
- Audit trail for investigation decisions
- FastAPI backend
- Streamlit dashboard
- Automated tests with GitHub Actions CI

## How it works

1. Transaction and behavioral information is collected as input.
2. The detection model calculates the probability that the transaction is suspicious.
3. The investigation layer evaluates transaction behavior and identifies the strongest risk signals.
4. The system assigns one of three outcomes:
   - `ALLOW_MONITORING`
   - `VERIFY`
   - `ESCALATE_FOR_REVIEW`
5. High-risk cases are routed for human review instead of automatically taking a financial action.
6. An audit event records the workflow, decision, and timestamp.

## Detection signals

The investigation uses transaction and behavioral features such as:

- Transaction amount
- Transaction hour
- Customer transaction count in the last 24 hours
- Customer average transaction amount
- Device transaction count in the last hour
- Number of customers associated with a device
- Distance from previous customer activity
- New device indicator
- New location indicator
- Merchant fraud rate over the previous 7 days

## Example performance

The included synthetic benchmark contains **50,000 transactions** with a held-out test set of **10,000 transactions**.

| Metric | Result |
|---|---:|
| Fraud rate | 5.51% |
| Precision | 71.01% |
| Recall | 97.82% |
| F1 score | 82.29% |
| PR-AUC | 97.38% |

These results are from synthetic data and should not be interpreted as production fraud-detection performance.

## Project structure

```text
fraud-spike-sentinel/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── api.py
│   ├── investigator.py
│   └── model_service.py
├── assets/
│   └── demo-result.svg
├── data/
│   └── .gitkeep
├── models/
│   ├── .gitkeep
│   └── metrics.json
├── scripts/
│   ├── generate_data.py
│   └── train.py
├── tests/
│   └── test_investigator.py
├── dashboard.py
├── LICENSE
├── README.md
├── requirements.txt
├── pytest.ini
├── run_project.bat
└── run_project.sh
```

## Quick start

### 1. Create an environment

**Windows**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux**

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

### 4. Train the detection model

```bash
python scripts/train.py
```

This creates the local model file and benchmark metrics used by the application.

### 5. Start the API

```bash
uvicorn app.api:app --reload
```

API documentation:

`http://127.0.0.1:8000/docs`

### 6. Start the dashboard

In another terminal:

```bash
streamlit run dashboard.py
```

Then open the local Streamlit URL shown in the terminal.

### Windows shortcut

You can also run `run_project.bat` after installing Python. It prepares the project and launches the API and dashboard in separate terminals.

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

## Investigation decisions

| Risk score | Decision |
|---|---|
| `< 0.50` | `ALLOW_MONITORING` |
| `0.50 – 0.79` | `VERIFY` |
| `≥ 0.80` | `ESCALATE_FOR_REVIEW` |

The thresholds are intentionally simple and transparent so that the result can be reviewed alongside the underlying transaction signals.

## Design notes

- The test set is kept separate from training so reported performance is measured on unseen transactions.
- Precision, recall, F1, and PR-AUC are reported because fraudulent transactions are much less common than normal transactions in the synthetic dataset.
- Investigation results include specific behavioral reasons instead of returning only a score.
- The workflow is intentionally bounded: it does not block accounts, move money, or execute financial actions automatically.
- High-risk transactions are sent for review and recorded in an audit event.
- The project is designed for demonstration and development use with synthetic data.

## Safety and scope

This project uses synthetic transaction data only. It does not connect to live payment systems, process real financial transactions, or perform offensive security activity.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
