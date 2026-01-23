from __future__ import annotations

import pandas as pd
from src.core.fetch import fetch_bytes
from src.core.load import read_to_df

# Put the dataset path or full URL here later
DATASET_URL = "PUT_DATASET_URL_OR_PATH_HERE"


def load() -> pd.DataFrame:
    result = fetch_bytes(DATASET_URL)
    df = read_to_df(result.content, file_hint=DATASET_URL, content_type=result.content_type)
    return df


def main() -> None:
    df = load()
    print("Dataset: Twitter7")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))
    print(df.head())


if __name__ == "__main__":
    main()
