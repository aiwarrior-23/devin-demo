from src.analyzer import analyze_transaction, analyze_transactions


def test_analyze_transaction():
    txn = {
        "amount": 2000,
        "country": "Nigeria"
    }
    flags = analyze_transaction(txn)
    assert "HIGH_VALUE" in flags
    assert "HIGH_RISK_COUNTRY" in flags


def test_analyze_transactions_flags_behavioral():
    """analyze_transactions should add MULTIPLE_HIGH_VALUE flag for burst behavior."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 2000, "country": "USA", "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C1", "amount": 1800, "country": "USA", "date": "2026-05-02"},
    ]
    flagged = analyze_transactions(transactions)
    assert "HIGH_VALUE" in flagged[1]
    assert "MULTIPLE_HIGH_VALUE" in flagged[1]
    assert "HIGH_VALUE" in flagged[2]
    assert "MULTIPLE_HIGH_VALUE" in flagged[2]


def test_analyze_transactions_no_behavioral_flag_for_single():
    """A single high-value transaction should not get MULTIPLE_HIGH_VALUE."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 2000, "country": "USA", "date": "2026-05-01"},
    ]
    flagged = analyze_transactions(transactions)
    assert "HIGH_VALUE" in flagged[1]
    assert "MULTIPLE_HIGH_VALUE" not in flagged[1]


def test_analyze_transactions_combines_all_flags():
    """A transaction can have HIGH_VALUE, HIGH_RISK_COUNTRY, and MULTIPLE_HIGH_VALUE."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 2000, "country": "Nigeria", "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C1", "amount": 1800, "country": "Nigeria", "date": "2026-05-02"},
    ]
    flagged = analyze_transactions(transactions)
    assert "HIGH_VALUE" in flagged[1]
    assert "HIGH_RISK_COUNTRY" in flagged[1]
    assert "MULTIPLE_HIGH_VALUE" in flagged[1]


def test_analyze_transactions_low_value_not_flagged():
    """Low-value transactions from safe countries should not appear in results."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 50, "country": "USA", "date": "2026-05-01"},
    ]
    flagged = analyze_transactions(transactions)
    assert 1 not in flagged
