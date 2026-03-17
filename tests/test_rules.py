from src.rules import (
    is_high_value,
    is_high_risk_country,
    detect_multiple_high_value_transactions,
    detect_rapid_transactions,
    detect_geographic_anomalies,
)


def test_high_value():
    assert is_high_value(2000) == True


def test_low_value():
    assert is_high_value(100) == False


def test_high_value_boundary():
    assert is_high_value(1500) == False
    assert is_high_value(1501) == True


def test_high_risk_country():
    assert is_high_risk_country("Nigeria") == True


def test_safe_country():
    assert is_high_risk_country("USA") == False


# --- Tests for detect_multiple_high_value_transactions ---


def test_detect_multiple_high_value_within_window():
    """Two high-value transactions from the same customer within 3 days should be flagged."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 2000, "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C1", "amount": 1800, "date": "2026-05-03"},
    ]
    flagged = detect_multiple_high_value_transactions(transactions)
    assert flagged == {1, 2}


def test_no_flag_when_single_high_value():
    """A single high-value transaction should not be flagged."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 2000, "date": "2026-05-01"},
    ]
    flagged = detect_multiple_high_value_transactions(transactions)
    assert flagged == set()


def test_no_flag_when_outside_window():
    """High-value transactions more than 3 days apart should not be flagged."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 2000, "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C1", "amount": 1800, "date": "2026-05-05"},
    ]
    flagged = detect_multiple_high_value_transactions(transactions)
    assert flagged == set()


def test_no_flag_for_low_value_transactions():
    """Multiple low-value transactions within the window should not be flagged."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 100, "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C1", "amount": 200, "date": "2026-05-02"},
    ]
    flagged = detect_multiple_high_value_transactions(transactions)
    assert flagged == set()


def test_different_customers_not_grouped():
    """High-value transactions from different customers should not be grouped together."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 2000, "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C2", "amount": 1800, "date": "2026-05-02"},
    ]
    flagged = detect_multiple_high_value_transactions(transactions)
    assert flagged == set()


def test_multiple_customers_flagged_independently():
    """Two customers each with multiple high-value txns should both be flagged."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 2000, "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C1", "amount": 1800, "date": "2026-05-02"},
        {"transaction_id": 3, "customer_id": "C2", "amount": 2500, "date": "2026-05-01"},
        {"transaction_id": 4, "customer_id": "C2", "amount": 3000, "date": "2026-05-03"},
    ]
    flagged = detect_multiple_high_value_transactions(transactions)
    assert flagged == {1, 2, 3, 4}


def test_three_transactions_in_window():
    """Three high-value transactions within 3 days should all be flagged."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 2000, "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C1", "amount": 1800, "date": "2026-05-02"},
        {"transaction_id": 3, "customer_id": "C1", "amount": 1600, "date": "2026-05-03"},
    ]
    flagged = detect_multiple_high_value_transactions(transactions)
    assert flagged == {1, 2, 3}


def test_custom_window_and_min_count():
    """Custom window_days and min_count parameters should be respected."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 2000, "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C1", "amount": 1800, "date": "2026-05-02"},
        {"transaction_id": 3, "customer_id": "C1", "amount": 1600, "date": "2026-05-03"},
    ]
    # With min_count=3, all 3 within 3-day window should be flagged
    flagged = detect_multiple_high_value_transactions(transactions, window_days=3, min_count=3)
    assert flagged == {1, 2, 3}

    # With min_count=4, not enough transactions to trigger
    flagged = detect_multiple_high_value_transactions(transactions, window_days=3, min_count=4)
    assert flagged == set()


def test_boundary_exactly_three_days_apart():
    """Transactions exactly 3 days apart should be within the window (inclusive)."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 2000, "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C1", "amount": 1800, "date": "2026-05-04"},
    ]
    flagged = detect_multiple_high_value_transactions(transactions)
    assert flagged == {1, 2}


def test_empty_transactions():
    """Empty transaction list should return empty set."""
    flagged = detect_multiple_high_value_transactions([])
    assert flagged == set()


def test_mixed_high_and_low_value():
    """Only high-value transactions should be considered for the behavioral rule."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 2000, "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C1", "amount": 100, "date": "2026-05-02"},
        {"transaction_id": 3, "customer_id": "C1", "amount": 1800, "date": "2026-05-03"},
    ]
    flagged = detect_multiple_high_value_transactions(transactions)
    # Only txn 1 and 3 are high-value and within 3 days
    assert flagged == {1, 3}


# --- Tests for detect_rapid_transactions ---


def test_rapid_transactions_flagged():
    """3+ transactions from same customer within 1 day should be flagged."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 50, "country": "USA", "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C1", "amount": 60, "country": "USA", "date": "2026-05-01"},
        {"transaction_id": 3, "customer_id": "C1", "amount": 70, "country": "USA", "date": "2026-05-01"},
    ]
    flagged = detect_rapid_transactions(transactions)
    assert flagged == {1, 2, 3}


def test_rapid_transactions_not_flagged_below_threshold():
    """2 transactions within 1 day should NOT be flagged (min_count=3)."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 50, "country": "USA", "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C1", "amount": 60, "country": "USA", "date": "2026-05-01"},
    ]
    flagged = detect_rapid_transactions(transactions)
    assert flagged == set()


def test_rapid_transactions_different_customers():
    """Transactions from different customers should not be grouped."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 50, "country": "USA", "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C2", "amount": 60, "country": "USA", "date": "2026-05-01"},
        {"transaction_id": 3, "customer_id": "C3", "amount": 70, "country": "USA", "date": "2026-05-01"},
    ]
    flagged = detect_rapid_transactions(transactions)
    assert flagged == set()


def test_rapid_transactions_outside_window():
    """Transactions spread over multiple days should not be flagged."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 50, "country": "USA", "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C1", "amount": 60, "country": "USA", "date": "2026-05-03"},
        {"transaction_id": 3, "customer_id": "C1", "amount": 70, "country": "USA", "date": "2026-05-05"},
    ]
    flagged = detect_rapid_transactions(transactions)
    assert flagged == set()


def test_rapid_transactions_custom_params():
    """Custom window_days and min_count should be respected."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 50, "country": "USA", "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C1", "amount": 60, "country": "USA", "date": "2026-05-02"},
        {"transaction_id": 3, "customer_id": "C1", "amount": 70, "country": "USA", "date": "2026-05-03"},
    ]
    # With window_days=3, all 3 are within the window
    flagged = detect_rapid_transactions(transactions, window_days=3, min_count=3)
    assert flagged == {1, 2, 3}

    # With min_count=4, not enough to trigger
    flagged = detect_rapid_transactions(transactions, window_days=3, min_count=4)
    assert flagged == set()


def test_rapid_transactions_empty():
    """Empty transaction list should return empty set."""
    flagged = detect_rapid_transactions([])
    assert flagged == set()


# --- Tests for detect_geographic_anomalies ---


def test_geo_anomaly_multiple_countries():
    """Transactions from 2+ countries within 2 days should be flagged."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 50, "country": "USA", "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C1", "amount": 60, "country": "UK", "date": "2026-05-01"},
    ]
    flagged = detect_geographic_anomalies(transactions)
    assert flagged == {1, 2}


def test_geo_anomaly_same_country():
    """Transactions from the same country should NOT be flagged."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 50, "country": "USA", "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C1", "amount": 60, "country": "USA", "date": "2026-05-01"},
    ]
    flagged = detect_geographic_anomalies(transactions)
    assert flagged == set()


def test_geo_anomaly_different_customers():
    """Transactions from different customers in different countries should not trigger."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 50, "country": "USA", "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C2", "amount": 60, "country": "UK", "date": "2026-05-01"},
    ]
    flagged = detect_geographic_anomalies(transactions)
    assert flagged == set()


def test_geo_anomaly_outside_window():
    """Transactions from different countries beyond the window should not be flagged."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 50, "country": "USA", "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C1", "amount": 60, "country": "UK", "date": "2026-05-05"},
    ]
    flagged = detect_geographic_anomalies(transactions)
    assert flagged == set()


def test_geo_anomaly_three_countries():
    """Transactions from 3 countries within the window should all be flagged."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 50, "country": "USA", "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C1", "amount": 60, "country": "UK", "date": "2026-05-01"},
        {"transaction_id": 3, "customer_id": "C1", "amount": 70, "country": "Germany", "date": "2026-05-02"},
    ]
    flagged = detect_geographic_anomalies(transactions)
    assert flagged == {1, 2, 3}


def test_geo_anomaly_custom_params():
    """Custom window_days and min_countries should be respected."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 50, "country": "USA", "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C1", "amount": 60, "country": "UK", "date": "2026-05-02"},
        {"transaction_id": 3, "customer_id": "C1", "amount": 70, "country": "Germany", "date": "2026-05-03"},
    ]
    # With min_countries=3 and window_days=3, all 3 are within the window
    flagged = detect_geographic_anomalies(transactions, window_days=3, min_countries=3)
    assert flagged == {1, 2, 3}

    # With min_countries=4, not enough countries to trigger
    flagged = detect_geographic_anomalies(transactions, window_days=3, min_countries=4)
    assert flagged == set()


def test_geo_anomaly_empty():
    """Empty transaction list should return empty set."""
    flagged = detect_geographic_anomalies([])
    assert flagged == set()


def test_geo_anomaly_multiple_customers_independent():
    """Two customers each with multi-country txns should both be flagged independently."""
    transactions = [
        {"transaction_id": 1, "customer_id": "C1", "amount": 50, "country": "USA", "date": "2026-05-01"},
        {"transaction_id": 2, "customer_id": "C1", "amount": 60, "country": "UK", "date": "2026-05-01"},
        {"transaction_id": 3, "customer_id": "C2", "amount": 70, "country": "Japan", "date": "2026-05-01"},
        {"transaction_id": 4, "customer_id": "C2", "amount": 80, "country": "Brazil", "date": "2026-05-02"},
    ]
    flagged = detect_geographic_anomalies(transactions)
    assert flagged == {1, 2, 3, 4}
