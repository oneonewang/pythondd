"""Ex04: asyncio 进阶。

涵盖：超时、取消、``Semaphore``、``as_completed``、异步上下文管理器。
"""
from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager


async def with_timeout(coro, timeout: float):
    """``asyncio.wait_for(coro, timeout)`` 的便利包装。失败抛 ``asyncio.TimeoutError``。"""
    # TODO
    raise NotImplementedError


async def cancel_after(coro, delay: float):
    """``delay`` 秒后取消 ``coro``，返回其结果或抛 ``CancelledError``。"""
    # TODO
    raise NotImplementedError


async def gather_limited(coros: list, limit: int) -> list:
    """用 ``asyncio.Semaphore(limit)`` 控制同时最多 ``limit`` 个并发。

    - 输入 100 个协程、limit=10，应该分批跑（但总结果数仍是 100）
    - 返回结果列表（顺序与输入对应）
    """
    # TODO
    raise NotImplementedError


async def first_completed(coros: list):
    """返回第一个完成的协程的结果。"""
    # TODO
    raise NotImplementedError


@asynccontextmanager
async def async_timer() -> AsyncIterator[dict]:
    """异步上下文管理器：测代码块耗时。

    退出时把 ``elapsed`` 写到 ``yield`` 出去的 dict。
    """
    # TODO
    yield {}                  # type: ignore[unreachable]
    raise NotImplementedError


class AsyncCounter:
    """``__aenter__`` / ``__aexit__`` / ``increment``。

    - ``async with`` 时 ``self.value += 1``
    - ``__aexit__`` 时 ``self.value += 1``（无论是否异常）
    - ``increment`` 方法 ``self.value += 1``（async）
    """

    def __init__(self) -> None:
        # TODO
        ...

    async def __aenter__(self) -> AsyncCounter:
        # TODO
        ...

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        # TODO
        ...

    async def increment(self) -> None:
        # TODO
        ...
