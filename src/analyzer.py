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

    if is_high_risk_merchant(txn["merchant_category"]):
        flags.append("HIGH_RISK_MERCHANT")

    return flags


def analyze_dataset(df):
    """Analyze an entire dataset and return per-transaction flags and per-customer behavioral flags."""
    transaction_flags = {}
    customer_flags = {}

    for _, row in df.iterrows():
        flags = analyze_transaction(row)
        if flags:
            transaction_flags[row["transaction_id"]] = flags

    customer_ids = df["customer_id"].unique()
    for cid in customer_ids:
        cflags = []

        if detect_multiple_high_value_transactions(df, cid):
            cflags.append("RAPID_HIGH_VALUE")

        if detect_repeated_high_risk_country_purchases(df, cid):
            cflags.append("REPEATED_HIGH_RISK_COUNTRY")

        if detect_repeated_high_value_transactions(df, cid):
            cflags.append("REPEATED_HIGH_VALUE")

        if cflags:
            customer_flags[cid] = cflags

    return transaction_flags, customer_flags
