import pandas as pd
from src.rules import (
    detect_multiple_high_value_transactions,
    detect_repeated_high_risk_country_purchases,
)


def _make_df(rows):
    return pd.DataFrame(rows, columns=["transaction_id", "customer_id", "amount", "country", "merchant_category", "date"])


def test_detect_rapid_high_value_true():
    """Two high-value transactions within 2 days should be detected."""
    df = _make_df([
        [1, "C101", 1600, "Nigeria", "Electronics", "2026-05-01"],
        [2, "C101", 1700, "Nigeria", "Electronics", "2026-05-02"],
    ])
    assert detect_multiple_high_value_transactions(df, "C101") is True


def test_detect_rapid_high_value_false_only_one():
    """A single high-value transaction should not be detected."""
    df = _make_df([
        [1, "C101", 1600, "USA", "Electronics", "2026-05-01"],
        [2, "C101", 100, "USA", "Grocery", "2026-05-02"],
    ])
    assert detect_multiple_high_value_transactions(df, "C101") is False


def test_detect_rapid_high_value_false_outside_window():
    """Two high-value transactions more than 3 days apart should not be detected."""
    df = _make_df([
        [1, "C101", 1600, "USA", "Electronics", "2026-05-01"],
        [2, "C101", 1700, "USA", "Electronics", "2026-05-10"],
    ])
    assert detect_multiple_high_value_transactions(df, "C101") is False


def test_detect_rapid_high_value_custom_window():
    """Custom window of 1 day: transactions 2 days apart should not trigger."""
    df = _make_df([
        [1, "C101", 1600, "USA", "Electronics", "2026-05-01"],
        [2, "C101", 1700, "USA", "Electronics", "2026-05-03"],
    ])
    assert detect_multiple_high_value_transactions(df, "C101", window_days=1) is False


def test_detect_repeated_high_risk_country_true():
    """Two transactions from high-risk countries should be detected."""
    df = _make_df([
        [1, "C103", 2200, "Russia", "Travel", "2026-05-04"],
        [2, "C103", 2100, "Russia", "Travel", "2026-05-05"],
    ])
    assert detect_repeated_high_risk_country_purchases(df, "C103") is True


def test_detect_repeated_high_risk_country_false():
    """A single transaction from a high-risk country should not be detected."""
    df = _make_df([
        [1, "C103", 2200, "Russia", "Travel", "2026-05-04"],
        [2, "C103", 100, "USA", "Coffee", "2026-05-05"],
    ])
    assert detect_repeated_high_risk_country_purchases(df, "C103") is False


def test_detect_repeated_high_risk_country_no_txns():
    """Customer with no transactions should not be flagged."""
    df = _make_df([
        [1, "C101", 100, "USA", "Coffee", "2026-05-01"],
    ])
    assert detect_repeated_high_risk_country_purchases(df, "C999") is False
