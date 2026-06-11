"""抽象协议：Fetcher。"""
from __future__ import annotations

from typing import Protocol

from .models import FetchResult


class Fetcher(Protocol):
    """异步 fetch 接口。"""

    async def fetch(self, url: str) -> FetchResult: ...


class Storage(Protocol):
    """持久化接口。"""

    def save(self, result: FetchResult) -> None: ...
    def get_pending(self) -> list[str]: ...
    def get_failed(self) -> list[str]: ...
    def stats(self) -> dict[str, int]: ...
