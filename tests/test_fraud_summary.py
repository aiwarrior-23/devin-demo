import pandas as pd
from src.analyzer import analyze_dataset
from src.report_generator import generate_fraud_summary


def _make_df(rows):
    return pd.DataFrame(rows, columns=["transaction_id", "customer_id", "amount", "country", "merchant_category", "date"])


def test_fraud_summary_sorted_by_risk():
    """Fraud summary should list customers sorted by risk score descending."""
    df = _make_df([
        [4001, "C101", 120, "USA", "Grocery", "2026-05-01"],
        [4002, "C101", 1600, "Nigeria", "Electronics", "2026-05-02"],
        [4003, "C101", 1700, "Nigeria", "Electronics", "2026-05-03"],
        [4004, "C102", 50, "USA", "Coffee", "2026-05-01"],
    ])
    txn_flags, cust_flags = analyze_dataset(df)
    summary = generate_fraud_summary(df, txn_flags, cust_flags)

    assert len(summary) == 2
    assert summary[0]["customer_id"] == "C101"
    assert summary[0]["risk_score"] >= summary[1]["risk_score"]


def test_fraud_summary_contains_high_risk_customer():
    """Fraud summary should mark a high-risk customer as HIGH."""
    df = _make_df([
        [4002, "C101", 1600, "Nigeria", "Electronics", "2026-05-02"],
        [4003, "C101", 1700, "Nigeria", "Electronics", "2026-05-03"],
    ])
    txn_flags, cust_flags = analyze_dataset(df)
    summary = generate_fraud_summary(df, txn_flags, cust_flags)

    assert len(summary) == 1
    assert summary[0]["risk_level"] == "HIGH"
    assert len(summary[0]["behavioral_flags"]) > 0


def test_fraud_summary_low_risk_customer():
    """A safe customer should have a LOW risk level."""
    df = _make_df([
        [4004, "C102", 50, "USA", "Coffee", "2026-05-01"],
    ])
    txn_flags, cust_flags = analyze_dataset(df)
    summary = generate_fraud_summary(df, txn_flags, cust_flags)

    assert len(summary) == 1
    assert summary[0]["risk_level"] == "LOW"
    assert summary[0]["behavioral_flags"] == []
