"""Resolve SQLite path for one-off scripts (new data/db + legacy fallbacks)."""
from __future__ import annotations

from pathlib import Path

import _bootstrap  # noqa: F401
from src.config.settings import BACKEND_DIR, SQLITE_PATH


def resolve_db_path() -> Path:
    candidates = [
        SQLITE_PATH,
        BACKEND_DIR / 'instance' / 'emotion_recognition.db',
        BACKEND_DIR / 'emotion_recognition.db',
    ]
    for path in candidates:
        if path.exists():
            return path
    return SQLITE_PATH
