def generate_summary(flagged_transactions):
    report = {}
    for txn_id, flags in flagged_transactions.items():
        report[txn_id] = ", ".join(flags)
    return report
