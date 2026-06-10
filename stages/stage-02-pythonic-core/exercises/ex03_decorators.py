"""Ex03: 装饰器。

涵盖：基础装饰器、`@wraps`、计时、参数化、装饰链、类装饰器。
"""
from __future__ import annotations

import time
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def timer(func: Callable[P, R]) -> Callable[P, R]:
    """装饰器：记录函数执行时间（秒）到 ``func.last_elapsed``，返回原结果。

    要求：保留函数元信息。
    """
    # TODO: 实现
    raise NotImplementedError


def logger(func: Callable[P, R]) -> Callable[P, R]:
    """装饰器：调用时打印 ``call <name>(<args>) -> <result>``。"""
    # TODO: 实现
    raise NotImplementedError


def retry(times: int = 3, delay: float = 0.0):
    """装饰器工厂：函数抛异常时重试 ``times`` 次，每次之间 sleep ``delay`` 秒。

    最后一次仍失败则把异常往上抛。
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        # TODO: 实现
        raise NotImplementedError

    return decorator


def validate_int(*expected: type) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """装饰器工厂：检查所有位置参数都是 ``expected`` 中某一种类型，否则抛 ``TypeError``。

    例：``@validate_int(int, float)`` 后，``f(1, 1.5)`` OK，``f("x", 1)`` 抛 TypeError。
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        # TODO: 实现
        raise NotImplementedError

    return decorator


class CountCalls:
    """类装饰器：记录函数被调用次数到 ``self.count``。"""

    def __init__(self, func: Callable[P, R]) -> None:
        # TODO: 实现
        ...

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        # TODO: 实现
        raise NotImplementedError


def slow(n: int = 1) -> int:
    """测试用：sleep ``n / 1000`` 秒后返回 ``n``。"""
    time.sleep(n / 1000)
    return n
