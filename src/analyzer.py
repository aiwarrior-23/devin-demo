from .rules import (
    is_high_value,
    is_high_risk_country,
    is_high_risk_merchant,
    detect_multiple_high_value_transactions,
    detect_repeated_high_risk_country_purchases,
    detect_repeated_high_value_transactions,
)


def analyze_transaction(txn):
    """Analyze a single transaction and return a list of flags."""
    flags = []

    if is_high_value(txn["amount"]):
        flags.append("HIGH_VALUE")

    if is_high_risk_country(txn["country"]):
        flags.append("HIGH_RISK_COUNTRY")

    if is_high_risk_merchant(txn.get("merchant_category", "")):
        flags.append("HIGH_RISK_MERCHANT")

    return flags


def analyze_transactions(transactions):
    """Analyze a list of transactions for both per-transaction and behavioral fraud signals.

    Args:
        transactions: List of dicts with keys including 'transaction_id', 'customer_id',
            'amount', 'country', 'date', and optionally 'merchant_category'.

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

    # Per-customer behavioral rules
    customer_ids = set(txn["customer_id"] for txn in transactions)
    for cid in customer_ids:
        cflags = []

        if detect_repeated_high_risk_country_purchases(transactions, cid):
            cflags.append("REPEATED_HIGH_RISK_COUNTRY")

        if detect_repeated_high_value_transactions(transactions, cid):
            cflags.append("REPEATED_HIGH_VALUE")

        # Apply customer-level flags to all transactions for that customer
        if cflags:
            cust_txn_ids = [txn["transaction_id"] for txn in transactions if txn["customer_id"] == cid]
            for txn_id in cust_txn_ids:
                flagged.setdefault(txn_id, []).extend(cflags)

    return flagged
