from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, TextIO

import pandas as pd

from src.core.config import SETTINGS


# -----------------------
# Dataset configuration
# -----------------------
DATASET_DIRNAME = "higgs-twitter"  # folder name under DATA_ROOT

FILES = {
    "social_network": "higgs-social_network.edgelist",
    "retweet_network": "higgs-retweet_network.edgelist",
    "reply_network": "higgs-reply_network.edgelist",
    "mention_network": "higgs-mention_network.edgelist",
    "activity_time": "higgs-activity_time.txt",
}


def _require_data_root() -> Path:
    """
    DATA_ROOT should be the directory that contains `higgs-twitter/`.
    Example:
      DATA_ROOT=/mnt/DATA/Dezinfo-Social_nets
    """
    if SETTINGS.DATA_ROOT is None:
        raise RuntimeError(
            "DATA_ROOT is not set.\n"
            "Set it to the directory that contains the dataset folders.\n"
            "Example:\n"
            "  DATA_ROOT=/mnt/DATA/Dezinfo-Social_nets"
        )
    return SETTINGS.DATA_ROOT


def _dataset_path() -> Path:
    return _require_data_root() / DATASET_DIRNAME


def _read_head_whitespace(path: Path, nrows: int) -> pd.DataFrame:
    """
    Read whitespace-separated file and return first nrows.
    Supports both plain text and .gz automatically based on filename.
    """
    compression = "gzip" if path.name.endswith(".gz") else None
    return pd.read_csv(
        path,
        sep=r"\s+",
        header=None,
        nrows=nrows,
        compression=compression,
        engine="python",
    )


def load_network_head(key: str, nrows: int = 5) -> pd.DataFrame:
    """
    Load head of one of the edgelist network files.
    Some SNAP edgelists include a weight column; we infer based on column count.
    """
    dataset_dir = _dataset_path()
    path = dataset_dir / FILES[key]
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    df = _read_head_whitespace(path, nrows=nrows)

    if df.shape[1] == 2:
        df.columns = ["src", "dst"]
    elif df.shape[1] == 3:
        df.columns = ["src", "dst", "weight"]
    else:
        df.columns = [f"col{i}" for i in range(df.shape[1])]

    return df


def load_activity_head(nrows: int = 5) -> pd.DataFrame:
    """
    Load head of activity log file.
    Expected columns: userA userB timestamp interaction
    """
    dataset_dir = _dataset_path()
    path = dataset_dir / FILES["activity_time"]
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    df = _read_head_whitespace(path, nrows=nrows)

    if df.shape[1] == 4:
        df.columns = ["userA", "userB", "timestamp", "interaction"]
    else:
        df.columns = [f"col{i}" for i in range(df.shape[1])]

    return df


# -----------------------
# Reporting helpers
# -----------------------
def _writeln(out: TextIO, text: str = "") -> None:
    out.write(text + "\n")


def _print_and_write(out: TextIO, text: str = "") -> None:
    print(text)
    _writeln(out, text)


def _df_to_string(df: pd.DataFrame) -> str:
    # Make pandas output stable and readable
    return df.to_string(index=False)


def main(nrows: int = 5) -> None:
    dataset_dir = _dataset_path()

    # Write reports locally in the dataset folder (NOT the server folder)
    local_report_dir = Path(__file__).parent / "reports"
    local_report_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = local_report_dir / f"higgs_twitter_heads_{ts}.txt"

    with open(report_path, "w", encoding="utf-8") as out:
        _print_and_write(out, "Dataset: Higgs Twitter")
        _print_and_write(out, f"DATA_ROOT: {SETTINGS.DATA_ROOT}")
        _print_and_write(out, f"Dataset path: {dataset_dir}")
        _print_and_write(out, f"Rows shown per file: {nrows}")
        _print_and_write(out, f"Report file: {report_path}")
        _print_and_write(out, "-" * 80)

        # 4 network files
        for key in ["social_network", "retweet_network", "reply_network", "mention_network"]:
            _print_and_write(out, f"\n## {key}")
            df = load_network_head(key, nrows=nrows)
            _print_and_write(out, _df_to_string(df))

        # activity file
        _print_and_write(out, "\n## activity_time")
        df_act = load_activity_head(nrows=nrows)
        _print_and_write(out, _df_to_string(df_act))

        _print_and_write(out, "\nDone.")

    print(f"\nSaved report to: {report_path}")


if __name__ == "__main__":
    main(nrows=5)
