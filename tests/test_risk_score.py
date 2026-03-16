import pandas as pd
from src.risk_score import calculate_customer_risk_score, get_risk_level


def _make_df(rows):
    return pd.DataFrame(rows, columns=["transaction_id", "customer_id", "amount", "country", "merchant_category", "date"])


def test_risk_score_high_risk_customer():
    """C101 has two high-value txns from Nigeria within 2 days -> high score."""
    df = _make_df([
        [1, "C101", 1600, "Nigeria", "Electronics", "2026-05-01"],
        [2, "C101", 1700, "Nigeria", "Electronics", "2026-05-02"],
    ])
    score = calculate_customer_risk_score(df, "C101")
    assert score >= 60
    assert get_risk_level(score) == "HIGH"


def test_risk_score_low_risk_customer():
    """C102 has one small domestic transaction -> low score."""
    df = _make_df([
        [3, "C102", 50, "USA", "Coffee", "2026-05-01"],
    ])
    score = calculate_customer_risk_score(df, "C102")
    assert score == 0
    assert get_risk_level(score) == "LOW"


def test_risk_score_medium_risk_customer():
    """Customer with two high-value txns from a safe country far apart -> medium."""
    df = _make_df([
        [4, "C103", 2000, "USA", "Travel", "2026-05-01"],
        [5, "C103", 1800, "USA", "Travel", "2026-05-20"],
    ])
    score = calculate_customer_risk_score(df, "C103")
    assert 30 <= score < 60
    assert get_risk_level(score) == "MEDIUM"


def test_risk_score_empty_customer():
    """Unknown customer should return 0."""
    df = _make_df([
        [1, "C101", 1600, "Nigeria", "Electronics", "2026-05-01"],
    ])
    score = calculate_customer_risk_score(df, "C999")
    assert score == 0


def test_get_risk_level_boundaries():
    assert get_risk_level(0) == "LOW"
    assert get_risk_level(29) == "LOW"
    assert get_risk_level(30) == "MEDIUM"
    assert get_risk_level(59) == "MEDIUM"
    assert get_risk_level(60) == "HIGH"
    assert get_risk_level(100) == "HIGH"
