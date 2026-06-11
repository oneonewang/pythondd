"""SQLite 持久化。"""
from __future__ import annotations

import sqlite3
from collections.abc import Iterable
from pathlib import Path

from .models import FetchResult

SCHEMA = """
CREATE TABLE IF NOT EXISTS results (
    url TEXT PRIMARY KEY,
    status INTEGER NOT NULL,
    content TEXT,
    error TEXT,
    duration_ms REAL NOT NULL,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_status ON results(status);
CREATE INDEX IF NOT EXISTS idx_error ON results(error);
"""


class SQLiteStorage:
    """同步 SQLite 存储（适合持久层；并发安全由 SQLite 自己保证）。"""

    def __init__(self, path: Path) -> None:
        # TODO
        ...

    def save(self, result: FetchResult) -> None:
        """upsert 一条结果。"""
        # TODO
        ...

    def get_pending(self) -> list[str]:
        """返回还没爬过 / 失败的 URL（用于断点续爬）。"""
        # TODO
        raise NotImplementedError

    def get_failed(self) -> list[str]:
        # TODO
        raise NotImplementedError

    def stats(self) -> dict[str, int]:
        """返回 ``{"total": n, "ok": n, "failed": n, "pending": n}``。"""
        # TODO
        raise NotImplementedError

    def close(self) -> None:
        # TODO
        ...
