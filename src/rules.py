import pandas as pd

HIGH_VALUE_THRESHOLD = 1500
HIGH_RISK_COUNTRIES = ["Nigeria", "Russia"]
RAPID_TRANSACTION_WINDOW_DAYS = 3
RAPID_TRANSACTION_MIN_COUNT = 2


def is_high_value(amount):
    return amount > HIGH_VALUE_THRESHOLD


def is_high_risk_country(country):
    return country in HIGH_RISK_COUNTRIES


def detect_multiple_high_value_transactions(df, customer_id, window_days=RAPID_TRANSACTION_WINDOW_DAYS):
    """Detect if a customer has multiple high-value transactions within a given window of days."""
    customer_txns = df[df["customer_id"] == customer_id].copy()
    customer_txns["date"] = pd.to_datetime(customer_txns["date"])
    customer_txns = customer_txns.sort_values("date")

    high_value_txns = customer_txns[customer_txns["amount"] > HIGH_VALUE_THRESHOLD]

    if len(high_value_txns) < RAPID_TRANSACTION_MIN_COUNT:
        return False

    dates = high_value_txns["date"].tolist()
    for i in range(len(dates)):
        for j in range(i + 1, len(dates)):
            if (dates[j] - dates[i]).days <= window_days:
                return True

    return False


def detect_repeated_high_risk_country_purchases(df, customer_id):
    """Detect if a customer has repeated purchases from high-risk countries."""
    customer_txns = df[df["customer_id"] == customer_id]
    high_risk_txns = customer_txns[customer_txns["country"].isin(HIGH_RISK_COUNTRIES)]
    return len(high_risk_txns) >= 2
