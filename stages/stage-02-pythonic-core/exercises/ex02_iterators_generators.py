"""Ex02: 迭代器与生成器。

涵盖：自定义迭代器协议、`yield`、`yield from`、`itertools`。
"""
from __future__ import annotations

from collections.abc import Iterable, Iterator


def fibonacci(n: int) -> Iterator[int]:
    """生成前 n 个斐波那契数（0, 1, 1, 2, 3, 5, ...）。n=0 时不产出。

    要求：用 ``yield``。
    """
    # TODO: 实现
    raise NotImplementedError
    yield  # type: ignore  # 让 ruff 知道这是生成器


def take(n: int, iterable: Iterable[int]) -> list[int]:
    """取前 n 个元素。n=0 或 iterable 为空时返回 []。

    要求：用 ``itertools.islice``。
    """
    # TODO: 实现
    raise NotImplementedError


def chunked(iterable: Iterable[int], size: int) -> Iterator[list[int]]:
    """把 ``iterable`` 切成 ``size`` 大小的块，最后一块可能更短。

    要求：用 ``yield from`` 或 ``yield``。
    """
    # TODO: 实现
    raise NotImplementedError
    yield  # type: ignore


def flatten(nested: Iterable) -> Iterator:
    """递归展平任意嵌套的可迭代对象。

    例：``[1, [2, [3, 4], 5], 6]`` -> ``1 2 3 4 5 6``

    要求：生成器 + ``isinstance`` + 递归。
    """
    # TODO: 实现
    raise NotImplementedError
    yield  # type: ignore


def sliding_window(iterable: Iterable[int], k: int) -> Iterator[tuple[int, ...]]:
    """返回所有长度为 k 的滑动窗口。

    例：``sliding_window([1,2,3,4,5], 3)`` -> ``(1,2,3) (2,3,4) (3,4,5)``

    k <= 0 或 iterable 长度 < k 时不产出。

    要求：``itertools.tee`` 或纯生成器。
    """
    # TODO: 实现
    raise NotImplementedError
    yield  # type: ignore


def running_total(iterable: Iterable[int]) -> Iterator[int]:
    """产出累计和。

    例：``running_total([1, 2, 3, 4])`` -> ``1 3 6 10``
    """
    # TODO: 实现
    raise NotImplementedError
    yield  # type: ignore


class Cycle:
    """无限循环遍历 ``items``。

    例：``Cycle([1, 2, 3])`` -> 1 2 3 1 2 3 1 2 3 ...
    """

    def __init__(self, items: Iterable[int]) -> None:
        # TODO: 保存底层数据
        ...

    def __iter__(self) -> Iterator[int]:
        # TODO: 用 ``yield from`` + 循环实现无限序列
        ...
        raise NotImplementedError
        yield  # type: ignore
