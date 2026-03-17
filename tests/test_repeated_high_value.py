from src.rules import detect_repeated_high_value_transactions


def test_repeated_high_value_true():
    """Customer with 3+ high-value transactions should be flagged."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C101", "amount": 1600, "country": "USA", "merchant_category": "Electronics", "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C101", "amount": 1700, "country": "USA", "merchant_category": "Electronics", "date": "2026-05-10"},
        {"transaction_id": 3, "customer_id": "C101", "amount": 1800, "country": "USA", "merchant_category": "Travel", "date": "2026-05-20"},
    ]
    assert detect_repeated_high_value_transactions(transactions, "C101") is True


def test_repeated_high_value_false_below_threshold():
    """Customer with only 2 high-value transactions (below default min_count=3) should not be flagged."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C101", "amount": 1600, "country": "USA", "merchant_category": "Electronics", "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C101", "amount": 1700, "country": "USA", "merchant_category": "Electronics", "date": "2026-05-10"},
    ]
    assert detect_repeated_high_value_transactions(transactions, "C101") is False


def test_repeated_high_value_custom_min_count():
    """Custom min_count of 2 should flag a customer with exactly 2 high-value transactions."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C101", "amount": 1600, "country": "USA", "merchant_category": "Electronics", "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C101", "amount": 1700, "country": "USA", "merchant_category": "Electronics", "date": "2026-05-10"},
    ]
    assert detect_repeated_high_value_transactions(transactions, "C101", min_count=2) is True


def test_repeated_high_value_no_high_value_txns():
    """Customer with no high-value transactions should not be flagged."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C102", "amount": 50, "country": "USA", "merchant_category": "Coffee", "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C102", "amount": 100, "country": "USA", "merchant_category": "Grocery", "date": "2026-05-02"},
    ]
    assert detect_repeated_high_value_transactions(transactions, "C102") is False


def test_repeated_high_value_unknown_customer():
    """Unknown customer should not be flagged."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C101", "amount": 1600, "country": "USA", "merchant_category": "Electronics", "date": "2026-05-01"},
    ]
    assert detect_repeated_high_value_transactions(transactions, "C999") is False
