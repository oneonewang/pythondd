"""Crawler 端到端测试。"""
import asyncio

from async_crawler.crawler import AsyncCrawler, CrawlerConfig
from async_crawler.fetcher import MockFetcher
from async_crawler.models import FetchResult
from async_crawler.storage import SQLiteStorage


def make_mock_fetcher(responses: dict[str, FetchResult]) -> MockFetcher:
    return MockFetcher(responses)


class TestCrawler:
    def test_basic_crawl(self, tmp_path) -> None:
        urls = ["http://a", "http://b", "http://c"]
        responses = {
            u: FetchResult(url=u, status=200, content=f"body of {u}")
            for u in urls
        }
        fetcher = make_mock_fetcher(responses)
        storage = SQLiteStorage(tmp_path / "db.sqlite")
        config = CrawlerConfig(max_concurrent=3, max_retries=1, base_delay=0.01)
        crawler = AsyncCrawler(fetcher, storage, config)

        results = asyncio.run(crawler.crawl(urls))
        assert len(results) == 3
        assert all(r.ok for r in results)
        stats = storage.stats()
        assert stats["ok"] == 3

        storage.close()

    def test_handles_failures(self, tmp_path) -> None:
        urls = ["http://ok", "http://bad"]
        responses = {
            "http://ok": FetchResult(url="http://ok", status=200, content=""),
            "http://bad": FetchResult(url="http://bad", status=0, content="", error="timeout"),
        }
        fetcher = make_mock_fetcher(responses)
        storage = SQLiteStorage(tmp_path / "db.sqlite")
        config = CrawlerConfig(max_concurrent=2, max_retries=1, base_delay=0.01)
        crawler = AsyncCrawler(fetcher, storage, config)

        results = asyncio.run(crawler.crawl(urls))
        assert len(results) == 2
        assert sum(1 for r in results if r.ok) == 1
        stats = storage.stats()
        assert stats["ok"] == 1
        assert stats["failed"] == 1
        storage.close()

    def test_resume_finds_pending(self, tmp_path) -> None:
        storage = SQLiteStorage(tmp_path / "db.sqlite")
        # 模拟"上次没爬完"：标记一些为失败
        storage.save(FetchResult("http://x", status=500, content="", error="oops"))
        pending = storage.get_pending()
        failed = storage.get_failed()
        assert "http://x" in failed
        assert pending == []      # 之前失败的不会出现在 pending

        storage.close()
