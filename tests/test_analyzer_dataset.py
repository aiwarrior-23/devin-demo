import pandas as pd
from src.analyzer import analyze_dataset


def _make_df(rows):
    return pd.DataFrame(rows, columns=["transaction_id", "customer_id", "amount", "country", "merchant_category", "date"])


def test_analyze_dataset_flags_transactions():
    """Dataset analysis should flag individual high-value and high-risk country transactions."""
    df = _make_df([
        [4001, "C101", 120, "USA", "Grocery", "2026-05-01"],
        [4002, "C101", 1600, "Nigeria", "Electronics", "2026-05-02"],
    ])
    txn_flags, _ = analyze_dataset(df)
    assert 4001 not in txn_flags
    assert "HIGH_VALUE" in txn_flags[4002]
    assert "HIGH_RISK_COUNTRY" in txn_flags[4002]


def test_analyze_dataset_customer_behavioral_flags():
    """Dataset analysis should detect behavioral patterns at customer level."""
    df = _make_df([
        [4002, "C101", 1600, "Nigeria", "Electronics", "2026-05-02"],
        [4003, "C101", 1700, "Nigeria", "Electronics", "2026-05-03"],
    ])
    _, customer_flags = analyze_dataset(df)
    assert "C101" in customer_flags
    assert "RAPID_HIGH_VALUE" in customer_flags["C101"]
    assert "REPEATED_HIGH_RISK_COUNTRY" in customer_flags["C101"]


def test_analyze_dataset_no_flags_for_safe_customer():
    """A customer with only low-value safe transactions should have no flags."""
    df = _make_df([
        [4004, "C102", 50, "USA", "Coffee", "2026-05-01"],
    ])
    txn_flags, customer_flags = analyze_dataset(df)
    assert 4004 not in txn_flags
    assert "C102" not in customer_flags
