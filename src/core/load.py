from __future__ import annotations

import io
import tarfile
import zipfile
from typing import Optional

import pandas as pd


def _read_single_file(content: bytes, *, filename: str) -> pd.DataFrame:
    """
    Read a single file (CSV, JSON, Parquet, Excel) into a DataFrame.
    filename is used to infer the format.
    """
    name = (filename or "").lower()

    if name.endswith(".parquet"):
        return pd.read_parquet(io.BytesIO(content))

    if name.endswith(".xlsx") or name.endswith(".xls"):
        return pd.read_excel(io.BytesIO(content))

    if name.endswith(".json"):
        return pd.read_json(io.BytesIO(content))

    # default: CSV
    return pd.read_csv(io.BytesIO(content))


def _read_tar_gz(content: bytes) -> pd.DataFrame:
    """
    Extract a .tar.gz/.tgz archive and load exactly one data file.
    If multiple files exist, we raise an error so the dataset script
    can implement dataset-specific logic.
    """
    with tarfile.open(fileobj=io.BytesIO(content), mode="r:gz") as tar:
        members = [m for m in tar.getmembers() if m.isfile()]

        if not members:
            raise ValueError("Archive contains no files.")

        if len(members) > 1:
            raise ValueError(
                f"Archive contains multiple files: {[m.name for m in members]}. "
                "Please customize this dataset's pull.py to choose the right file(s)."
            )

        member = members[0]
        extracted = tar.extractfile(member)
        if extracted is None:
            raise ValueError(f"Could not extract {member.name}")

        return _read_single_file(extracted.read(), filename=member.name)


def _read_zip(content: bytes) -> pd.DataFrame:
    """
    Extract a .zip archive and load exactly one data file.
    If multiple files exist, we raise an error for explicit handling.
    """
    with zipfile.ZipFile(io.BytesIO(content)) as zf:
        names = [n for n in zf.namelist() if not n.endswith("/")]

        if not names:
            raise ValueError("Zip archive is empty.")

        if len(names) > 1:
            raise ValueError(
                f"Zip archive contains multiple files: {names}. "
                "Please customize this dataset's pull.py to choose the right file(s)."
            )

        name = names[0]
        with zf.open(name) as f:
            return _read_single_file(f.read(), filename=name)


def read_to_df(
    content: bytes,
    *,
    file_hint: str = "",
    content_type: Optional[str] = None,
) -> pd.DataFrame:
    """
    Convert downloaded bytes into a pandas DataFrame.

    Supports:
      - CSV, JSON, Parquet, Excel
      - .tar.gz / .tgz archives (single file inside)
      - .zip archives (single file inside)

    file_hint: typically the URL or filename, used for extension detection.
    content_type: HTTP Content-Type, used as a secondary hint.
    """
    hint = (file_hint or "").lower()
    ctype = (content_type or "").lower()

    # tar.gz / tgz
    if hint.endswith(".tar.gz") or hint.endswith(".tgz") or ("gzip" in ctype and "tar" in ctype):
        return _read_tar_gz(content)

    # zip
    if hint.endswith(".zip") or "zip" in ctype:
        return _read_zip(content)

    # non-archive
    return _read_single_file(content, filename=hint)
