import pandas as pd


def load_dataset(path):
    df = pd.read_csv(path, quotechar='"', skipinitialspace=True)
    if len(df.columns) == 1 and "," in df.columns[0]:
        col_names = df.columns[0].split(",")
        df = df.iloc[:, 0].str.split(",", expand=True)
        df.columns = col_names
    df.columns = df.columns.str.strip()
    if "amount" in df.columns:
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    if "transaction_id" in df.columns:
        df["transaction_id"] = df["transaction_id"].str.strip()
    return df


def reconcile(bank_df, internal_df):
    bank_ids = set(bank_df["transaction_id"])
    internal_ids = set(internal_df["transaction_id"])

    results = []

    all_ids = bank_ids | internal_ids
    for txn_id in sorted(all_ids):
        in_bank = txn_id in bank_ids
        in_internal = txn_id in internal_ids

        if in_bank and in_internal:
            bank_amount = bank_df.loc[
                bank_df["transaction_id"] == txn_id, "amount"
            ].values[0]
            internal_amount = internal_df.loc[
                internal_df["transaction_id"] == txn_id, "amount"
            ].values[0]

            if bank_amount == internal_amount:
                status = "MATCHED"
            else:
                status = "AMOUNT_MISMATCH"
            results.append({
                "transaction_id": txn_id,
                "status": status,
                "bank_amount": bank_amount,
                "internal_amount": internal_amount,
            })
        elif in_bank and not in_internal:
            bank_amount = bank_df.loc[
                bank_df["transaction_id"] == txn_id, "amount"
            ].values[0]
            results.append({
                "transaction_id": txn_id,
                "status": "MISSING_IN_INTERNAL",
                "bank_amount": bank_amount,
                "internal_amount": None,
            })
        else:
            internal_amount = internal_df.loc[
                internal_df["transaction_id"] == txn_id, "amount"
            ].values[0]
            results.append({
                "transaction_id": txn_id,
                "status": "MISSING_IN_BANK",
                "bank_amount": None,
                "internal_amount": internal_amount,
            })

    return pd.DataFrame(results)


def generate_reconciliation_summary(results_df):
    summary = {
        "total_transactions": len(results_df),
        "matched": len(results_df[results_df["status"] == "MATCHED"]),
        "amount_mismatch": len(results_df[results_df["status"] == "AMOUNT_MISMATCH"]),
        "missing_in_bank": len(results_df[results_df["status"] == "MISSING_IN_BANK"]),
        "missing_in_internal": len(
            results_df[results_df["status"] == "MISSING_IN_INTERNAL"]
        ),
    }
    return summary
