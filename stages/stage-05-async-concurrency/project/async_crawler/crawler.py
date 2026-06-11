"""爬虫主类。"""
from __future__ import annotations

import asyncio
import time
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from .fetcher import HttpxFetcher
from .models import FetchResult
from .protocols import Fetcher, Storage
from .rate_limiter import RateLimiter
from .retry import retry
from .storage import SQLiteStorage


@dataclass
class CrawlerConfig:
    """爬虫配置。"""

    max_concurrent: int = 10
    timeout: float = 10.0
    max_retries: int = 3
    base_delay: float = 1.0
    max_bytes: int = 1024 * 1024


class AsyncCrawler:
    """编排 fetch + 限速 + 重试 + 持久化。"""

    def __init__(
        self,
        fetcher: Fetcher,
        storage: Storage,
        config: CrawlerConfig | None = None,
    ) -> None:
        # TODO
        ...

    async def crawl(self, urls: Iterable[str]) -> list[FetchResult]:
        """并发爬取 ``urls``，返回所有结果。"""
        # TODO
        raise NotImplementedError

    async def _crawl_one(self, url: str) -> FetchResult:
        """爬单个 URL：限速 + 超时 + 重试。"""
        # TODO
        raise NotImplementedError
