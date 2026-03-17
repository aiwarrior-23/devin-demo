from .rules import (
    is_high_value,
    is_high_risk_country,
    detect_multiple_high_value_transactions,
    detect_rapid_transactions,
    detect_geographic_anomalies,
)


def analyze_transaction(txn):
    flags = []

    if is_high_value(txn["amount"]):
        flags.append("HIGH_VALUE")

    if is_high_risk_country(txn["country"]):
        flags.append("HIGH_RISK_COUNTRY")

    return flags


def analyze_transactions(transactions):
    """Analyze a list of transactions for both per-transaction and behavioral fraud signals.

    Args:
        transactions: List of dicts with keys including 'transaction_id', 'customer_id',
            'amount', 'country', 'date'.

    Returns:
        Dict mapping transaction_id to a list of flag strings.
    """
    flagged = {}

    # Per-transaction rules
    for txn in transactions:
        flags = analyze_transaction(txn)
        if flags:
            flagged[txn["transaction_id"]] = flags

    # Behavioral rule: multiple high-value transactions within a rolling window
    burst_txn_ids = detect_multiple_high_value_transactions(transactions)
    for txn_id in burst_txn_ids:
        flagged.setdefault(txn_id, []).append("MULTIPLE_HIGH_VALUE")

    # Behavioral rule: rapid transaction velocity
    rapid_txn_ids = detect_rapid_transactions(transactions)
    for txn_id in rapid_txn_ids:
        flagged.setdefault(txn_id, []).append("RAPID_TRANSACTIONS")

    # Behavioral rule: geographic anomaly
    geo_txn_ids = detect_geographic_anomalies(transactions)
    for txn_id in geo_txn_ids:
        flagged.setdefault(txn_id, []).append("GEO_ANOMALY")

    return flagged
