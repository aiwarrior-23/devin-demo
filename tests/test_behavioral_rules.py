from src.rules import (
    detect_repeated_high_risk_country_purchases,
)


def test_detect_repeated_high_risk_country_true():
    """Two transactions from high-risk countries should be detected."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C103", "amount": 2200, "country": "Russia", "merchant_category": "Travel", "date": "2026-05-04"},
        {"transaction_id": 2, "customer_id": "C103", "amount": 2100, "country": "Russia", "merchant_category": "Travel", "date": "2026-05-05"},
    ]
    assert detect_repeated_high_risk_country_purchases(transactions, "C103") is True


def test_detect_repeated_high_risk_country_false():
    """A single transaction from a high-risk country should not be detected."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C103", "amount": 2200, "country": "Russia", "merchant_category": "Travel", "date": "2026-05-04"},
        {"transaction_id": 2, "customer_id": "C103", "amount": 100, "country": "USA", "merchant_category": "Coffee", "date": "2026-05-05"},
    ]
    assert detect_repeated_high_risk_country_purchases(transactions, "C103") is False


def test_detect_repeated_high_risk_country_no_txns():
    """Customer with no transactions should not be flagged."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C101", "amount": 100, "country": "USA", "merchant_category": "Coffee", "date": "2026-05-01"},
    ]
    assert detect_repeated_high_risk_country_purchases(transactions, "C999") is False
