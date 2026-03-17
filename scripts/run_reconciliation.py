import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.reconciler import load_dataset, reconcile, generate_reconciliation_summary


def main():
    bank_path = "data/Example2BankRecords.csv"
    internal_path = "data/Example2InternalRecords.csv"

    print("Loading datasets...")
    bank_df = load_dataset(bank_path)
    internal_df = load_dataset(internal_path)

    print(f"Bank records: {len(bank_df)} transactions")
    print(f"Internal records: {len(internal_df)} transactions")
    print()

    print("Running reconciliation...")
    results_df = reconcile(bank_df, internal_df)

    print("\n=== Reconciliation Report ===\n")
    print(results_df.to_string(index=False))

    summary = generate_reconciliation_summary(results_df)
    print("\n=== Summary ===\n")
    print(f"Total transactions:     {summary['total_transactions']}")
    print(f"Matched:                {summary['matched']}")
    print(f"Amount mismatches:      {summary['amount_mismatch']}")
    print(f"Missing in bank:        {summary['missing_in_bank']}")
    print(f"Missing in internal:    {summary['missing_in_internal']}")

    output_path = "data/reconciliation_report.csv"
    results_df.to_csv(output_path, index=False)
    print(f"\nReport saved to {output_path}")


if __name__ == "__main__":
    main()
