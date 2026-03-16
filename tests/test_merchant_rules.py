from src.rules import is_high_risk_merchant, HIGH_RISK_MERCHANT_CATEGORIES


def test_high_risk_merchant_electronics():
    assert is_high_risk_merchant("Electronics") is True


def test_high_risk_merchant_travel():
    assert is_high_risk_merchant("Travel") is True


def test_high_risk_merchant_crypto():
    assert is_high_risk_merchant("Crypto") is True


def test_high_risk_merchant_gambling():
    assert is_high_risk_merchant("Gambling") is True


def test_safe_merchant_grocery():
    assert is_high_risk_merchant("Grocery") is False


def test_safe_merchant_coffee():
    assert is_high_risk_merchant("Coffee") is False


def test_high_risk_merchant_categories_list():
    assert "Electronics" in HIGH_RISK_MERCHANT_CATEGORIES
    assert "Travel" in HIGH_RISK_MERCHANT_CATEGORIES
    assert "Crypto" in HIGH_RISK_MERCHANT_CATEGORIES
    assert "Gambling" in HIGH_RISK_MERCHANT_CATEGORIES
