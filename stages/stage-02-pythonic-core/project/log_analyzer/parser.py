"""日志解析器：按行读取、解析为 LogRecord，全程用生成器。"""
from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path

from .models import LogRecord


@dataclass
class ParseStats:
    """解析过程中的统计。"""

    total_lines: int = 0
    parsed: int = 0
    errors: int = 0


def iter_lines(path: Path, encoding: str = "utf-8") -> Iterator[str]:
    """逐行读取文件，去掉换行符。空行跳过。"""
    with path.open(encoding=encoding) as f:
        for line in f:
            line = line.rstrip("\n").rstrip("\r")
            if line:
                yield line


def parse_line(line: str) -> LogRecord:
    """解析单行。失败抛 :class:`ValueError`。"""
    parts = line.split(" ", 2)
    if len(parts) < 3:
        raise ValueError(f"expected 3 fields, got {len(parts)}: {line!r}")
    ts, level, message = parts
    return LogRecord(timestamp=ts, level=level, message=message)


def iter_records(
    path: Path,
    stats: ParseStats | None = None,
    encoding: str = "utf-8",
) -> Iterator[LogRecord]:
    """流式产出 LogRecord，跳过无法解析的行（计入 ``stats.errors``）。

    用法：

    >>> stats = ParseStats()
    >>> for r in iter_records(path, stats):
    ...     process(r)
    >>> print(stats.errors)
    """
    # TODO: 实现
    raise NotImplementedError
    yield  # type: ignore  # 让 ruff 知道是生成器


def iter_records_or_raise(path: Path, encoding: str = "utf-8") -> Iterator[LogRecord]:
    """严格版：解析失败直接抛 :class:`ValueError`。"""
    for line in iter_lines(path, encoding=encoding):
        yield parse_line(line)
