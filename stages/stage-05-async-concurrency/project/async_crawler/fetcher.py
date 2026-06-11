"""HTTP Fetcher。"""
from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable
from typing import Any

import httpx

from .models import FetchResult


class HttpxFetcher:
    """真实 HTTP fetch（用 ``httpx.AsyncClient``）。"""

    def __init__(
        self,
        timeout: float = 10.0,
        max_bytes: int = 1024 * 1024,
        client_factory: Callable[[], httpx.AsyncClient] | None = None,
    ) -> None:
        # TODO
        ...

    async def fetch(self, url: str) -> FetchResult:
        # TODO: 测耗时，捕获异常，返回 FetchResult
        raise NotImplementedError


class MockFetcher:
    """测试用：可注入响应。"""

    def __init__(self, responses: dict[str, FetchResult]) -> None:
        # TODO
        ...

    async def fetch(self, url: str) -> FetchResult:
        # TODO
        ...
