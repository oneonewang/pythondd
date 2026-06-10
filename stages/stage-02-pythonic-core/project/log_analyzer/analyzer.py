"""流式统计：聚合、滑动窗口、异常检测。"""
from __future__ import annotations

from collections import Counter, deque
from collections.abc import Iterable, Iterator
from dataclasses import dataclass

from .models import LogRecord
from .parser import ParseStats, iter_records


def count_by_level(records: Iterable[LogRecord]) -> dict[str, int]:
    """按 level 计数。空输入返回空 dict。"""
    # TODO: 实现（用 collections.Counter）
    raise NotImplementedError


def take_errors(records: Iterable[LogRecord], limit: int) -> list[LogRecord]:
    """取前 ``limit`` 条 level == "ERROR" 的记录。"""
    # TODO: 实现
    raise NotImplementedError


@dataclass
class Anomaly:
    """异常报告。"""

    line_no: int
    error_rate: float
    window_size: int
    level: str


def sliding_rate(
    records: Iterable[LogRecord],
    window: int,
    level: str = "ERROR",
) -> Iterator[Anomaly]:
    """对每条记录，计算"前 window 条记录中 level 的占比"。

    产出每一条记录对应的窗口统计（不"只产出异常"——那是 :func:`find_anomalies` 的事）。

    例：window=3, level=ERROR，输入 [INFO, INFO, ERROR, INFO]：
    - 跳过前 window-1 条（窗口未填满）
    - 第 3 条触发窗口 [INFO, INFO, ERROR] -> 1/3
    - 第 4 条触发窗口 [INFO, ERROR, INFO] -> 1/3
    """
    # TODO: 用 collections.deque(maxlen=window) 实现
    raise NotImplementedError
    yield  # type: ignore


def find_anomalies(
    records: Iterable[LogRecord],
    window: int,
    threshold: float,
    level: str = "ERROR",
) -> Iterator[Anomaly]:
    """错误率超过 ``threshold`` 的窗口报警。

    等价于 ``(a for a in sliding_rate(...) if a.error_rate > threshold)``。
    """
    # TODO: 实现
    raise NotImplementedError
    yield  # type: ignore


# 便捷顶层 API：直接从文件路径分析
def analyze_file(
    path,
    *,
    stats: ParseStats | None = None,
) -> Iterator[LogRecord]:
    """``iter_records(path, stats)`` 的便捷包装。"""
    return iter_records(path, stats=stats)


__all__ = [
    "Anomaly",
    "ParseStats",
    "analyze_file",
    "count_by_level",
    "find_anomalies",
    "iter_records",
    "sliding_rate",
    "take_errors",
]
