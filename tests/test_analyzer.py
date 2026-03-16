from src.analyzer import analyze_transaction

def test_analyze_transaction():
    txn = {
        "amount": 2000,
        "country": "Nigeria"
    }
    flags = analyze_transaction(txn)
    assert "HIGH_VALUE" in flags
    assert "HIGH_RISK_COUNTRY" in flags
