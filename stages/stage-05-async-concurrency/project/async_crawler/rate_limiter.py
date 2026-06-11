"""基于 ``asyncio.Semaphore`` 的限速器。"""
from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


class RateLimiter:
    """``asyncio.Semaphore`` 包装的限速器。"""

    def __init__(self, max_concurrent: int) -> None:
        # TODO
        ...

    async def run[T](self, coro_factory: Callable[[], Awaitable[T]]) -> T:
        """在限速下跑协程工厂。"""
        # TODO
        raise NotImplementedError
