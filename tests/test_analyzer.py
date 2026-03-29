from src.analyzer import analyze_transaction, analyze_transactions


def test_analyze_transaction():
    txn = {
        "amount": 2000,
        "country": "Nigeria",
        "merchant_category": "Electronics",
    }
    flags = analyze_transaction(txn)
    assert "HIGH_VALUE" in flags
    assert "HIGH_RISK_COUNTRY" in flags
    assert "HIGH_RISK_MERCHANT" in flags


def test_analyze_transaction_safe_merchant():
    txn = {
        "amount": 2000,
        "country": "USA",
        "merchant_category": "Grocery",
    }
    flags = analyze_transaction(txn)
    assert "HIGH_VALUE" in flags
    assert "HIGH_RISK_MERCHANT" not in flags


def test_analyze_transaction_high_risk_merchant_only():
    txn = {
        "amount": 100,
        "country": "USA",
        "merchant_category": "Gambling",
    }
    flags = analyze_transaction(txn)
    assert "HIGH_RISK_MERCHANT" in flags
    assert "HIGH_VALUE" not in flags
    assert "HIGH_RISK_COUNTRY" not in flags


def test_analyze_transactions_flags_behavioral():
    """analyze_transactions should add MULTIPLE_HIGH_VALUE flag for burst behavior."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 2000, "country": "USA", "merchant_category": "Grocery", "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C1", "amount": 1800, "country": "USA", "merchant_category": "Grocery", "date": "2026-05-02"},
    ]
    flagged = analyze_transactions(transactions)
    assert "HIGH_VALUE" in flagged[1]
    assert "MULTIPLE_HIGH_VALUE" in flagged[1]
    assert "HIGH_VALUE" in flagged[2]
    assert "MULTIPLE_HIGH_VALUE" in flagged[2]


def test_analyze_transactions_no_behavioral_flag_for_single():
    """A single high-value transaction should not get MULTIPLE_HIGH_VALUE."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 2000, "country": "USA", "merchant_category": "Grocery", "date": "2026-05-01"},
    ]
    flagged = analyze_transactions(transactions)
    assert "HIGH_VALUE" in flagged[1]
    assert "MULTIPLE_HIGH_VALUE" not in flagged[1]


def test_analyze_transactions_combines_all_flags():
    """A transaction can have HIGH_VALUE, HIGH_RISK_COUNTRY, HIGH_RISK_MERCHANT, and MULTIPLE_HIGH_VALUE."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 2000, "country": "Nigeria", "merchant_category": "Electronics", "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C1", "amount": 1800, "country": "Nigeria", "merchant_category": "Electronics", "date": "2026-05-02"},
    ]
    flagged = analyze_transactions(transactions)
    assert "HIGH_VALUE" in flagged[1]
    assert "HIGH_RISK_COUNTRY" in flagged[1]
    assert "HIGH_RISK_MERCHANT" in flagged[1]
    assert "MULTIPLE_HIGH_VALUE" in flagged[1]


def test_analyze_transactions_low_value_not_flagged():
    """Low-value transactions from safe countries should not appear in results."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 50, "country": "USA", "merchant_category": "Coffee", "date": "2026-05-01"},
    ]
    flagged = analyze_transactions(transactions)
    assert 1 not in flagged


def test_analyze_transactions_repeated_high_risk_country():
    """Customers with 2+ high-risk country transactions should get REPEATED_HIGH_RISK_COUNTRY."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 2000, "country": "Nigeria", "merchant_category": "Electronics", "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C1", "amount": 1800, "country": "Nigeria", "merchant_category": "Electronics", "date": "2026-05-02"},
    ]
    flagged = analyze_transactions(transactions)
    assert "REPEATED_HIGH_RISK_COUNTRY" in flagged[1]
    assert "REPEATED_HIGH_RISK_COUNTRY" in flagged[2]


def test_analyze_transactions_repeated_high_value():
    """Customers with 3+ high-value transactions should get REPEATED_HIGH_VALUE."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 2000, "country": "USA", "merchant_category": "Grocery", "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C1", "amount": 1800, "country": "USA", "merchant_category": "Grocery", "date": "2026-05-10"},
        {"transaction_id": 3, "customer_id": "C1", "amount": 1600, "country": "USA", "merchant_category": "Grocery", "date": "2026-05-20"},
    ]
    flagged = analyze_transactions(transactions)
    assert "REPEATED_HIGH_VALUE" in flagged[1]
    assert "REPEATED_HIGH_VALUE" in flagged[2]
    assert "REPEATED_HIGH_VALUE" in flagged[3]
