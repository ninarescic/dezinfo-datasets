import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
    # Load .env from project root (two levels above src/core/)
    project_root = Path(__file__).resolve().parents[2]
    load_dotenv(project_root / ".env")
except Exception:
    pass


@dataclass(frozen=True)
class Settings:
    DATA_ROOT: Path | None = (
        Path(os.getenv("DATA_ROOT")).expanduser()
        if os.getenv("DATA_ROOT")
        else None
    )


SETTINGS = Settings()
