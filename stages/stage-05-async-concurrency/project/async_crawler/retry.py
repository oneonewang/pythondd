"""指数退避重试装饰器。"""
from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
):
    """异步指数退避装饰器。

    失败时按 ``base_delay * 2 ** (attempt - 1)`` 等待，最长 ``max_delay``。
    第 ``max_attempts`` 次仍失败则把异常往上抛。
    """

    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # TODO: 实现
            raise NotImplementedError

        return wrapper

    return decorator
