"""Ex04: 文件 I/O 与异常。

涵盖：with 语句、JSON、CSV、异常捕获、自定义异常。
"""
from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path


class StorageError(Exception):
    """存储层错误的基类。"""


def read_json_safely(path: Path, default: object = None) -> object:
    """读 JSON 文件。

    - 文件不存在 -> 返回 default
    - JSON 解析失败 -> 抛 :class:`StorageError`
    """
    # TODO: 实现
    raise NotImplementedError


def write_json(path: Path, data: object) -> None:
    """写 JSON 文件（utf-8, ensure_ascii=False, indent=2）。

    父目录不存在时创建。
    """
    # TODO: 实现
    raise NotImplementedError


def write_csv(path: Path, rows: Iterable[dict[str, object]], fieldnames: list[str]) -> None:
    """把 ``rows`` 写成 CSV，列顺序按 ``fieldnames``。"""
    # TODO: 实现
    raise NotImplementedError


def read_lines_stripped(path: Path) -> list[str]:
    """读取文件所有行，去掉首尾空白与空行。"""
    # TODO: 实现
    raise NotImplementedError


def safe_div(a: float, b: float) -> float | str:
    """a / b，b 为 0 时返回字符串 ``"inf"``。"""
    # TODO: 实现
    raise NotImplementedError
