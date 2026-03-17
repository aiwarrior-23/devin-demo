from src.loader import load_transactions
from src.analyzer import analyze_transactions
from src.report_generator import generate_summary


def main():
    df = load_transactions("data/transactions.csv")
    transactions = df.to_dict(orient="records")

    flagged = analyze_transactions(transactions)

    report = generate_summary(flagged)

    for txn, reason in report.items():
        print(f"Transaction {txn}: {reason}")


if __name__ == "__main__":
    main()
