"""Runtime configuration helpers for environment-backed settings."""

import os

from dotenv import load_dotenv


def load_env() -> None:
    """Load .env values once for local runs; existing env vars win by default."""
    load_dotenv(override=False)


def env_flag(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    value = raw.strip().strip('"').strip("'").lower()
    return value in {"1", "true", "yes", "on"}


def is_mock_mode() -> bool:
    return env_flag("MOCK_MODE", default=True)
