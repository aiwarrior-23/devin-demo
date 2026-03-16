import pandas as pd
from src.rules import detect_repeated_high_value_transactions


def _make_df(rows):
    return pd.DataFrame(rows, columns=["transaction_id", "customer_id", "amount", "country", "merchant_category", "date"])


def test_repeated_high_value_true():
    """Customer with 3+ high-value transactions should be flagged."""
    df = _make_df([
        [1, "C101", 1600, "USA", "Electronics", "2026-05-01"],
        [2, "C101", 1700, "USA", "Electronics", "2026-05-10"],
        [3, "C101", 1800, "USA", "Travel", "2026-05-20"],
    ])
    assert detect_repeated_high_value_transactions(df, "C101") is True


def test_repeated_high_value_false_below_threshold():
    """Customer with only 2 high-value transactions (below default min_count=3) should not be flagged."""
    df = _make_df([
        [1, "C101", 1600, "USA", "Electronics", "2026-05-01"],
        [2, "C101", 1700, "USA", "Electronics", "2026-05-10"],
    ])
    assert detect_repeated_high_value_transactions(df, "C101") is False


def test_repeated_high_value_custom_min_count():
    """Custom min_count of 2 should flag a customer with exactly 2 high-value transactions."""
    df = _make_df([
        [1, "C101", 1600, "USA", "Electronics", "2026-05-01"],
        [2, "C101", 1700, "USA", "Electronics", "2026-05-10"],
    ])
    assert detect_repeated_high_value_transactions(df, "C101", min_count=2) is True


def test_repeated_high_value_no_high_value_txns():
    """Customer with no high-value transactions should not be flagged."""
    df = _make_df([
        [1, "C102", 50, "USA", "Coffee", "2026-05-01"],
        [2, "C102", 100, "USA", "Grocery", "2026-05-02"],
    ])
    assert detect_repeated_high_value_transactions(df, "C102") is False


def test_repeated_high_value_unknown_customer():
    """Unknown customer should not be flagged."""
    df = _make_df([
        [1, "C101", 1600, "USA", "Electronics", "2026-05-01"],
    ])
    assert detect_repeated_high_value_transactions(df, "C999") is False
