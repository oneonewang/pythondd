"""数据模型。"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LogRecord:
    """一条解析后的日志。"""

    timestamp: str
    level: str
    message: str

    def is_level(self, level: str) -> bool:
        return self.level == level
