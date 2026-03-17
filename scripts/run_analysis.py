from src.loader import load_transactions
from src.analyzer import analyze_transaction
from src.report_generator import generate_summary

def main():
    df = load_transactions("data/transactions.csv")
    flagged = {}

    for _, row in df.iterrows():
        flags = analyze_transaction(row)
        if flags:
            flagged[row["transaction_id"]] = flags

    report = generate_summary(flagged)

    for txn, reason in report.items():
        print(f"Transaction {txn}: {reason}")

if __name__ == "__main__":
    main()
