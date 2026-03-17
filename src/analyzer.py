from .rules import is_high_value, is_high_risk_country

def analyze_transaction(txn):
    flags = []

    if is_high_value(txn["amount"]):
        flags.append("HIGH_VALUE")

    if is_high_risk_country(txn["country"]):
        flags.append("HIGH_RISK_COUNTRY")

    return flags
