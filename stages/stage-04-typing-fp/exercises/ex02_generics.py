"""Ex02: 泛型。

涵盖：``TypeVar``、``Generic``、自定义泛型类、``ParamSpec``。
"""
from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Generic, ParamSpec, TypeVar

T = TypeVar("T")
U = TypeVar("U")
P = ParamSpec("P")
R = TypeVar("R")


class Stack(Generic[T]):
    """后进先出栈。

    - ``push(item)``
    - ``pop()`` -> T；空栈抛 IndexError
    - ``peek()`` -> T；空栈抛 IndexError
    - ``is_empty()`` -> bool
    - ``__len__`` -> int
    """

    def __init__(self) -> None:
        # TODO
        ...

    def push(self, item: T) -> None:
        # TODO
        ...

    def pop(self) -> T:
        # TODO
        raise NotImplementedError

    def peek(self) -> T:
        # TODO
        raise NotImplementedError

    def is_empty(self) -> bool:
        # TODO
        ...

    def __len__(self) -> int:
        # TODO
        ...


class Pair(Generic[T, U]):
    """``(key, value)`` 对，提供 ``swap``。"""

    def __init__(self, key: T, value: U) -> None:
        # TODO
        ...

    def swap(self) -> Pair[U, T]:
        # TODO
        raise NotImplementedError

    def __repr__(self) -> str:
        # TODO
        ...


def map_list(xs: list[T], f: Callable[[T], U]) -> list[U]:
    """内置 ``map`` 的列表版（更显式）。"""
    # TODO
    raise NotImplementedError


def first_or_default(xs: Iterable[T], default: T) -> T:
    """返回 ``xs`` 的第一个元素；空时返回 ``default``。"""
    # TODO
    raise NotImplementedError


def timer(func: Callable[P, R]) -> Callable[P, R]:
    """装饰器：保留签名。``ParamSpec`` 练习。

    （实际不做计时逻辑，只返回原函数；用于练 ParamSpec 类型。）
    """
    # TODO
    raise NotImplementedError
