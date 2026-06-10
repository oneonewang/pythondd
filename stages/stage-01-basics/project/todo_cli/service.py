"""业务逻辑层。

只接受/返回内存数据，**不**做 I/O。I/O 由 storage 层负责。
这样 service 容易测——传 list 进去，断言返回的新 list 即可。
"""
from __future__ import annotations

from datetime import UTC, datetime

from .models import TodoDict


class TodoNotFoundError(Exception):
    """找不到对应 id 的任务。"""


def _now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def add(todos: list[TodoDict], title: str) -> TodoDict:
    """添加一条任务，返回新创建的任务（带 id）。

    id 生成规则：``max(existing_ids, default=0) + 1``。
    """
    # TODO: 实现
    raise NotImplementedError


def list_todos(todos: list[TodoDict], include_done: bool = True) -> list[TodoDict]:
    """列出任务，未完成在前、按 id 升序。

    ``include_done=False`` 时只返回未完成。
    """
    # TODO: 实现
    raise NotImplementedError


def complete(todos: list[TodoDict], todo_id: int) -> TodoDict:
    """把 ``todo_id`` 标记为完成，返回更新后的任务。

    不存在时抛 :class:`TodoNotFoundError`。
    """
    # TODO: 实现
    raise NotImplementedError


def remove(todos: list[TodoDict], todo_id: int) -> TodoDict:
    """从列表中删除 ``todo_id``，返回被删除的任务。

    不存在时抛 :class:`TodoNotFoundError`。
    """
    # TODO: 实现
    raise NotImplementedError


def clear_done(todos: list[TodoDict]) -> int:
    """清空所有已完成的任务，返回被清除的数量。"""
    # TODO: 实现
    raise NotImplementedError
