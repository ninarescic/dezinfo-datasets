from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict
import requests

from src.core.config import SETTINGS


@dataclass(frozen=True)
class FetchResult:
    url: str
    content: bytes
    content_type: Optional[str]


def resolve_url(url_or_path: str) -> str:
    """
    Accept either:
      - Full URL: https://server/path/file.csv
      - Relative path: /path/file.csv   (requires DATA_BASE_URL)
    """
    if url_or_path.startswith("http://") or url_or_path.startswith("https://"):
        return url_or_path

    if not SETTINGS.BASE_URL:
        raise ValueError("Relative path provided but DATA_BASE_URL is not set.")

    path = url_or_path if url_or_path.startswith("/") else "/" + url_or_path
    return f"{SETTINGS.BASE_URL}{path}"


def fetch_bytes(
    url_or_path: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    timeout_s: int = 60,
) -> FetchResult:
    """
    Download a remote resource and return the raw bytes + content type.
    Adds auth automatically if configured in environment variables.
    """
    full_url = resolve_url(url_or_path)
    hdrs = dict(headers or {})

    # Bearer token auth
    if SETTINGS.API_TOKEN and "Authorization" not in hdrs:
        hdrs["Authorization"] = f"Bearer {SETTINGS.API_TOKEN}"

    # Basic auth (optional)
    auth = None
    if SETTINGS.USERNAME and SETTINGS.PASSWORD:
        auth = (SETTINGS.USERNAME, SETTINGS.PASSWORD)

    resp = requests.get(full_url, headers=hdrs, auth=auth, timeout=timeout_s)
    resp.raise_for_status()

    return FetchResult(
        url=full_url,
        content=resp.content,
        content_type=resp.headers.get("Content-Type"),
    )
