"""JSON 持久化层。

阶段 1 用 dict + 简单序列化。阶段 4 会改用 ``dataclass`` + 自定义 ``to_dict`` / ``from_dict``。
"""
from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path

from .models import TodoDict


class StorageError(Exception):
    """存储层错误。"""


def load_todos(path: Path) -> list[TodoDict]:
    """从 JSON 文件加载任务列表。文件不存在返回空列表。"""
    # TODO: 实现
    # 提示：
    #   - path 不存在 -> 返回 []
    #   - 文件存在但内容不是合法 JSON -> raise StorageError
    raise NotImplementedError


def save_todos(path: Path, todos: Iterable[TodoDict]) -> None:
    """把任务列表写到 JSON 文件。父目录不存在时创建。"""
    # TODO: 实现
    raise NotImplementedError
