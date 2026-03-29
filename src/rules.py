from datetime import datetime, timedelta

HIGH_VALUE_THRESHOLD = 1500
HIGH_RISK_COUNTRIES = ["Nigeria", "Russia"]
HIGH_RISK_MERCHANT_CATEGORIES = ["Electronics", "Travel", "Crypto", "Gambling"]
HIGH_VALUE_WINDOW_DAYS = 3
HIGH_VALUE_MIN_COUNT = 2
REPEATED_HIGH_VALUE_MIN_COUNT = 3


def is_high_value(amount):
    return amount > HIGH_VALUE_THRESHOLD


def is_high_risk_country(country):
    return country in HIGH_RISK_COUNTRIES


def is_high_risk_merchant(merchant_category):
    """Check if a merchant category is considered high risk."""
    return merchant_category in HIGH_RISK_MERCHANT_CATEGORIES


def detect_multiple_high_value_transactions(transactions, window_days=HIGH_VALUE_WINDOW_DAYS, min_count=HIGH_VALUE_MIN_COUNT):
    """Detect customers performing multiple high-value transactions within a given window.

    Args:
        transactions: List of dicts with keys 'transaction_id', 'customer_id', 'amount', 'date'.
            'date' should be a datetime object or date-parseable string.
        window_days: Number of days for the rolling window (default: 3).
        min_count: Minimum number of high-value transactions within the window to flag (default: 2).

    Returns:
        Set of transaction IDs that are part of a suspicious high-value burst.
    """
    # Group high-value transactions by customer
    customer_txns = {}
    for txn in transactions:
        if not is_high_value(txn["amount"]):
            continue
        customer_id = txn["customer_id"]
        date = txn["date"]
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d")
        customer_txns.setdefault(customer_id, []).append({
            "transaction_id": txn["transaction_id"],
            "date": date,
        })

    flagged_txn_ids = set()
    window = timedelta(days=window_days)

    for customer_id, txns in customer_txns.items():
        # Sort by date
        txns.sort(key=lambda t: t["date"])

        for i, txn in enumerate(txns):
            # Collect all transactions within the window starting from this transaction
            cluster = [txn]
            for j in range(i + 1, len(txns)):
                if txns[j]["date"] - txn["date"] <= window:
                    cluster.append(txns[j])
                else:
                    break

            if len(cluster) >= min_count:
                for t in cluster:
                    flagged_txn_ids.add(t["transaction_id"])

    return flagged_txn_ids


def detect_repeated_high_risk_country_purchases(transactions, customer_id):
    """Detect if a customer has repeated purchases from high-risk countries."""
    high_risk_count = sum(
        1 for txn in transactions
        if txn["customer_id"] == customer_id and is_high_risk_country(txn["country"])
    )
    return high_risk_count >= 2


def detect_repeated_high_value_transactions(transactions, customer_id, min_count=REPEATED_HIGH_VALUE_MIN_COUNT):
    """Detect if a customer has a pattern of repeated high-value transactions overall."""
    high_value_count = sum(
        1 for txn in transactions
        if txn["customer_id"] == customer_id and is_high_value(txn["amount"])
    )
    return high_value_count >= min_count
