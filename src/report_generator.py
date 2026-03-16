from .risk_score import calculate_customer_risk_score, get_risk_level


def generate_summary(flagged_transactions):
    """Generate a summary of flagged transactions."""
    report = {}
    for txn_id, flags in flagged_transactions.items():
        report[txn_id] = ", ".join(flags)
    return report


def generate_fraud_summary(df, transaction_flags, customer_flags):
    """Generate a fraud summary report listing high-risk customers with their risk scores."""
    customer_ids = df["customer_id"].unique()
    summary = []

    for cid in customer_ids:
        score = calculate_customer_risk_score(df, cid)
        level = get_risk_level(score)

        entry = {
            "customer_id": cid,
            "risk_score": score,
            "risk_level": level,
            "behavioral_flags": customer_flags.get(cid, []),
        }

        # Collect transaction-level flags for this customer
        cust_txn_ids = df[df["customer_id"] == cid]["transaction_id"].tolist()
        txn_flag_list = {
            tid: transaction_flags[tid]
            for tid in cust_txn_ids
            if tid in transaction_flags
        }
        entry["transaction_flags"] = txn_flag_list

        summary.append(entry)

    # Sort by risk score descending
    summary.sort(key=lambda x: x["risk_score"], reverse=True)
    return summary
