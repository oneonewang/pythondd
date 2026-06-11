"""Ex05: functools。

涵盖：``lru_cache``、``partial``、``singledispatch``、``cached_property``、``total_ordering``。
"""
from __future__ import annotations

from collections.abc import Iterable
from functools import (
    cache,
    cached_property,
    lru_cache,
    partial,
    reduce,
    singledispatch,
    total_ordering,
)
from operator import add, mul


def cached_factorial(n: int) -> int:
    """带 ``@cache`` 的阶乘。"""
    # TODO
    raise NotImplementedError


def lru_power(base: float, exp: float) -> float:
    """带 ``@lru_cache(maxsize=...)`` 的幂函数。"""
    # TODO
    raise NotImplementedError


def make_doubler(factor: int):
    """返回 ``lambda x: x * factor``——但用 ``functools.partial`` 实现。

    ``make_doubler(2)`` 等价于 ``lambda x: x * 2``。
    """
    # TODO
    raise NotImplementedError


def factorial_via_reduce(n: int) -> int:
    """用 ``functools.reduce`` 计算阶乘。"""
    # TODO
    raise NotImplementedError


@singledispatch
def format_value(value) -> str:
    """通用 formatter，按类型分派。"""
    # TODO
    raise NotImplementedError


# TODO: 给 format_value 注册 int / float / str / list 的特化版本
#   - int -> 十进制
#   - float -> 保留 2 位小数
#   - str -> 加引号
#   - list -> "[a, b, c]" 形式（递归调用 format_value）


class SquareStats:
    """对一组数字缓存"平均"和"标准差"。

    - ``__init__(data: list[float])``
    - ``mean``、``stdev`` 用 ``@cached_property``
    """

    def __init__(self, data: list[float]) -> None:
        self.data = data

    @cached_property
    def mean(self) -> float:
        # TODO
        ...

    @cached_property
    def stdev(self) -> float:
        # TODO
        raise NotImplementedError


@total_ordering
class LetterGrade:
    """字母成绩，按 A > B > C > D > F 排序。"""

    order: dict[str, int] = {"A": 5, "B": 4, "C": 3, "D": 2, "F": 1}

    def __init__(self, letter: str) -> None:
        # TODO
        ...

    def __eq__(self, other) -> bool:
        # TODO
        ...

    def __lt__(self, other) -> bool:
        # TODO
        ...

    def __repr__(self) -> str:
        # TODO
        ...
