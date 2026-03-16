from src.analyzer import analyze_transaction


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
