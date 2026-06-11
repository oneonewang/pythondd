"""Ex03: asyncio 基础。

涵盖：``async def``、``await``、``asyncio.gather``、``asyncio.create_task``、``asyncio.run``。
"""
from __future__ import annotations

import asyncio


async def fake_io(duration: float) -> str:
    """异步等待 ``duration`` 秒，返回 ``"done in {duration}s"``。"""
    # TODO
    raise NotImplementedError
    return ""  # type: ignore


async def run_sequential(coros: list) -> list:
    """按顺序 await 每个协程，返回结果列表。"""
    # TODO
    raise NotImplementedError


async def run_concurrent(coros: list) -> list:
    """用 ``asyncio.gather`` 并发跑所有协程。"""
    # TODO
    raise NotImplementedError


async def gather_with_exception(*coros) -> list:
    """``asyncio.gather`` 但 ``return_exceptions=True``，异常当结果返回。"""
    # TODO
    raise NotImplementedError


async def schedule_with_delay(coro, delay: float):
    """``delay`` 秒后调度执行 ``coro``，返回它的 Task。"""
    # TODO
    raise NotImplementedError


async def fetch_many(urls: list[str]) -> list[str]:
    """模拟对每个 URL fetch（用 ``fake_io``）。

    每个 URL 的延迟 = 0.05s。
    """
    # TODO
    raise NotImplementedError
