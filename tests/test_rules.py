from src.rules import is_high_value, is_high_risk_country

def test_high_value():
    assert is_high_value(2000) == True

def test_low_value():
    assert is_high_value(100) == False

def test_high_risk_country():
    assert is_high_risk_country("Nigeria") == True

def test_safe_country():
    assert is_high_risk_country("USA") == False
