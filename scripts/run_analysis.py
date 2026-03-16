from src.loader import load_transactions
from src.analyzer import analyze_transaction, analyze_dataset
from src.report_generator import generate_summary, generate_fraud_summary


def main():
    df = load_transactions("data/transactions.csv")

    # Dataset-level analysis
    transaction_flags, customer_flags = analyze_dataset(df)

    # Transaction-level summary (legacy)
    report = generate_summary(transaction_flags)
    print("=== Flagged Transactions ===")
    for txn, reason in report.items():
        print(f"  Transaction {txn}: {reason}")

    # Fraud summary report
    print("\n=== Fraud Summary Report ===")
    fraud_summary = generate_fraud_summary(df, transaction_flags, customer_flags)
    for entry in fraud_summary:
        print(f"  Customer {entry['customer_id']}: "
              f"Risk Score={entry['risk_score']}, "
              f"Level={entry['risk_level']}, "
              f"Behavioral Flags={entry['behavioral_flags']}")
        for tid, flags in entry["transaction_flags"].items():
            print(f"    Transaction {tid}: {', '.join(flags)}")


if __name__ == "__main__":
    main()
