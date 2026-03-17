from datetime import datetime, timedelta


HIGH_VALUE_THRESHOLD = 1500
HIGH_VALUE_WINDOW_DAYS = 3
HIGH_VALUE_MIN_COUNT = 2

RAPID_VELOCITY_WINDOW_DAYS = 1
RAPID_VELOCITY_MIN_COUNT = 3

GEO_ANOMALY_WINDOW_DAYS = 2
GEO_ANOMALY_MIN_COUNTRIES = 2


def _parse_date(date):
    """Parse a date string in %Y-%m-%d format, or return as-is if already a datetime."""
    if isinstance(date, str):
        return datetime.strptime(date, "%Y-%m-%d")
    return date


def _group_transactions_by_customer(transactions):
    """Group transactions by customer_id, parsing dates along the way.

    Returns:
        Dict mapping customer_id to list of transaction dicts with parsed dates.
    """
    customer_txns = {}
    for txn in transactions:
        customer_id = txn["customer_id"]
        entry = {
            "transaction_id": txn["transaction_id"],
            "date": _parse_date(txn["date"]),
        }
        if "amount" in txn:
            entry["amount"] = txn["amount"]
        if "country" in txn:
            entry["country"] = txn["country"]
        customer_txns.setdefault(customer_id, []).append(entry)
    return customer_txns


def is_high_value(amount):
    return amount > HIGH_VALUE_THRESHOLD


def is_high_risk_country(country):
    return country in ["Nigeria", "Russia"]


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
        date = _parse_date(txn["date"])
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


def detect_rapid_transactions(transactions, window_days=RAPID_VELOCITY_WINDOW_DAYS, min_count=RAPID_VELOCITY_MIN_COUNT):
    """Detect customers with an unusually high number of transactions in a short period.

    Args:
        transactions: List of dicts with keys 'transaction_id', 'customer_id', 'date'.
        window_days: Rolling window size in days (default: 1).
        min_count: Minimum number of transactions within the window to flag (default: 3).

    Returns:
        Set of transaction IDs that are part of a rapid-velocity burst.
    """
    customer_txns = _group_transactions_by_customer(transactions)

    flagged_txn_ids = set()
    window = timedelta(days=window_days)

    for customer_id, txns in customer_txns.items():
        txns.sort(key=lambda t: t["date"])

        for i, txn in enumerate(txns):
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


def detect_geographic_anomalies(transactions, window_days=GEO_ANOMALY_WINDOW_DAYS, min_countries=GEO_ANOMALY_MIN_COUNTRIES):
    """Detect customers transacting from multiple countries within a short window.

    Args:
        transactions: List of dicts with keys 'transaction_id', 'customer_id', 'country', 'date'.
        window_days: Rolling window size in days (default: 2).
        min_countries: Minimum number of distinct countries within the window to flag (default: 2).

    Returns:
        Set of transaction IDs that are part of a geographic anomaly cluster.
    """
    customer_txns = _group_transactions_by_customer(transactions)

    flagged_txn_ids = set()
    window = timedelta(days=window_days)

    for customer_id, txns in customer_txns.items():
        txns.sort(key=lambda t: t["date"])

        for i, txn in enumerate(txns):
            cluster = [txn]
            for j in range(i + 1, len(txns)):
                if txns[j]["date"] - txn["date"] <= window:
                    cluster.append(txns[j])
                else:
                    break

            countries = {t["country"] for t in cluster}
            if len(countries) >= min_countries:
                for t in cluster:
                    flagged_txn_ids.add(t["transaction_id"])

    return flagged_txn_ids
