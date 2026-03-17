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


def test_analyze_transactions_rapid_velocity():
    """3+ transactions from same customer within 1 day should get RAPID_TRANSACTIONS flag."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 50, "country": "USA", "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C1", "amount": 60, "country": "USA", "date": "2026-05-01"},
        {"transaction_id": 3, "customer_id": "C1", "amount": 70, "country": "USA", "date": "2026-05-01"},
    ]
    flagged = analyze_transactions(transactions)
    assert "RAPID_TRANSACTIONS" in flagged[1]
    assert "RAPID_TRANSACTIONS" in flagged[2]
    assert "RAPID_TRANSACTIONS" in flagged[3]


def test_analyze_transactions_geo_anomaly():
    """Transactions from multiple countries within 2 days should get GEO_ANOMALY flag."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 50, "country": "USA", "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C1", "amount": 60, "country": "UK", "date": "2026-05-01"},
    ]
    flagged = analyze_transactions(transactions)
    assert "GEO_ANOMALY" in flagged[1]
    assert "GEO_ANOMALY" in flagged[2]


def test_analyze_transactions_all_behavioral_flags():
    """A transaction can accumulate multiple behavioral flags simultaneously."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 2000, "country": "USA", "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C1", "amount": 1800, "country": "UK", "date": "2026-05-01"},
        {"transaction_id": 3, "customer_id": "C1", "amount": 1600, "country": "Germany", "date": "2026-05-01"},
    ]
    flagged = analyze_transactions(transactions)
    # All should have HIGH_VALUE, MULTIPLE_HIGH_VALUE, RAPID_TRANSACTIONS, GEO_ANOMALY
    for txn_id in [1, 2, 3]:
        assert "HIGH_VALUE" in flagged[txn_id]
        assert "MULTIPLE_HIGH_VALUE" in flagged[txn_id]
        assert "RAPID_TRANSACTIONS" in flagged[txn_id]
        assert "GEO_ANOMALY" in flagged[txn_id]
