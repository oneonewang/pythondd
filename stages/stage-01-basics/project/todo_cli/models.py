"""数据模型。

阶段 1 用普通 dict 表示，阶段 4 会升级为 :class:`dataclasses.dataclass`。
"""
from __future__ import annotations

from typing import TypedDict


class TodoDict(TypedDict):
    """一个 TODO 任务的字段。"""

    id: int
    title: str
    done: bool
    created_at: str  # ISO 8601 字符串
