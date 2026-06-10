"""Ex04: 上下文管理器。

涵盖：``__enter__``/``__exit__``、``@contextmanager``、``ExitStack``。
"""
from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from types import TracebackType


class Indenter:
    """自动缩进打印。

    用法：

    >>> with Indenter() as ind:
    ...     ind.print("a")
    ...     with ind:
    ...         ind.print("b")
    a
      b
    """

    def __init__(self, indent_unit: str = "  ") -> None:
        self.indent_unit = indent_unit
        self.level = 0

    def __enter__(self) -> Indenter:
        # TODO: 缩进 +1，返回 self
        ...
        raise NotImplementedError

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        # TODO: 缩进 -1
        ...

    def print(self, *args: object) -> None:
        """按当前缩进打印。"""
        print(self.indent_unit * self.level, *args, sep="")


@contextmanager
def temp_file(content: str, suffix: str = ".txt") -> Iterator[Path]:
    """创建一个临时文件、写入 ``content``、yield 路径、退出时自动删除。

    要求：``@contextmanager``。
    """
    # TODO: 实现
    raise NotImplementedError
    yield  # type: ignore  # 让 ruff 知道这是生成器


@contextmanager
def swallow(type_: type[BaseException], message: str = "") -> Iterator[None]:
    """吞掉指定类型异常，打印 ``message``。其他异常正常抛出。"""
    # TODO: 实现
    raise NotImplementedError
    yield  # type: ignore


class atomic_counter:
    """线程不安全的学习示例。``with atomic_counter() as c: c.value += 1`` 演示：

    - ``__enter__`` 备份 ``self.value``
    - ``__exit__``：有异常则回滚到备份；无异常则提交（这里"提交"就是新值）
    """

    def __init__(self, initial: int = 0) -> None:
        self.value = initial

    def __enter__(self) -> atomic_counter:
        # TODO: 备份
        ...
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        # TODO: 异常时回滚
        ...
        return False
