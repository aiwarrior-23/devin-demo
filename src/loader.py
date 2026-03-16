import pandas as pd

def load_transactions(path):
    return pd.read_csv(path)
