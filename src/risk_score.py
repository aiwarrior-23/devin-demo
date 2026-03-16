from .rules import (
    HIGH_VALUE_THRESHOLD,
    HIGH_RISK_COUNTRIES,
    HIGH_RISK_MERCHANT_CATEGORIES,
    detect_multiple_high_value_transactions,
    detect_repeated_high_risk_country_purchases,
    detect_repeated_high_value_transactions,
)


def calculate_customer_risk_score(df, customer_id):
    """Calculate a risk score (0-100) for a customer based on their transaction behavior."""
    score = 0
    customer_txns = df[df["customer_id"] == customer_id]

    if customer_txns.empty:
        return score

    # Points for high-value transactions
    high_value_count = len(customer_txns[customer_txns["amount"] > HIGH_VALUE_THRESHOLD])
    score += min(high_value_count * 15, 30)

    # Points for transactions from high-risk countries
    high_risk_count = len(customer_txns[customer_txns["country"].isin(HIGH_RISK_COUNTRIES)])
    score += min(high_risk_count * 15, 30)

    # Points for rapid high-value transactions within window
    if detect_multiple_high_value_transactions(df, customer_id):
        score += 20

    # Points for repeated high-risk country purchases
    if detect_repeated_high_risk_country_purchases(df, customer_id):
        score += 20

    # Points for high-risk merchant categories
    high_risk_merchant_count = len(
        customer_txns[customer_txns["merchant_category"].isin(HIGH_RISK_MERCHANT_CATEGORIES)]
    )
    score += min(high_risk_merchant_count * 10, 20)

    # Points for repeated high-value transactions
    if detect_repeated_high_value_transactions(df, customer_id):
        score += 10

    return min(score, 100)


def get_risk_level(score):
    """Return a human-readable risk level based on the score."""
    if score >= 60:
        return "HIGH"
    elif score >= 30:
        return "MEDIUM"
    return "LOW"
