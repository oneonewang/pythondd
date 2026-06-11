"""Ex05: 异步 I/O（不引入第三方库，用 asyncio 原生模拟）。

涵盖：``asyncio.StreamReader``、异步迭代器、自实现 ``aiofiles`` 风格 API。
"""
from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from pathlib import Path


class AsyncFileReader:
    """最小 ``aiofiles`` 替代：用线程跑同步 ``open``，避免阻塞 loop。"""

    def __init__(self, path: Path) -> None:
        # TODO
        ...

    async def __aenter__(self) -> AsyncFileReader:
        # TODO: 用 asyncio.to_thread 打开文件
        ...

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        # TODO: 用 asyncio.to_thread 关闭
        ...

    async def read(self) -> str:
        # TODO: 用 asyncio.to_thread 读全文
        raise NotImplementedError

    async def readlines(self) -> list[str]:
        # TODO: 用 asyncio.to_thread 读所有行
        raise NotImplementedError


async def read_files_concurrent(paths: list[Path], max_concurrent: int = 5) -> dict[Path, str]:
    """并发读多个文件，返回 ``{path: content}``。

    限制同时最多 ``max_concurrent`` 个打开的文件（用 ``Semaphore``）。
    """
    # TODO
    raise NotImplementedError


class AsyncRange:
    """异步范围的异步迭代器。"""

    def __init__(self, stop: int, step_delay: float = 0.0) -> None:
        # TODO
        ...

    def __aiter__(self) -> AsyncRange:
        # TODO
        ...

    async def __anext__(self) -> int:
        # TODO
        raise NotImplementedError


async def sum_async_range(stop: int) -> int:
    """用 ``async for`` 遍历 ``AsyncRange`` 并求和。"""
    # TODO
    raise NotImplementedError
