"""Storage 测试。"""
from pathlib import Path

from async_crawler.models import FetchResult
from async_crawler.storage import SQLiteStorage


def make_result(url: str, status: int = 200, error: str | None = None) -> FetchResult:
    return FetchResult(
        url=url,
        status=status,
        content="hello",
        error=error,
        duration_ms=10.0,
    )


class TestSQLiteStorage:
    def test_save_and_get_pending(self, tmp_path: Path) -> None:
        s = SQLiteStorage(tmp_path / "test.db")
        s.save(make_result("http://a"))
        assert "http://a" not in s.get_pending()     # 已成功
        s.save(make_result("http://b", status=500))
        assert "http://b" in s.get_failed()
        s.close()

    def test_upsert(self, tmp_path: Path) -> None:
        s = SQLiteStorage(tmp_path / "test.db")
        s.save(make_result("http://a", status=500))
        s.save(make_result("http://a", status=200))  # 覆盖
        stats = s.stats()
        assert stats["ok"] == 1
        assert stats["failed"] == 0
        s.close()

    def test_stats(self, tmp_path: Path) -> None:
        s = SQLiteStorage(tmp_path / "test.db")
        s.save(make_result("http://a", status=200))
        s.save(make_result("http://b", status=500, error="x"))
        stats = s.stats()
        assert stats["ok"] == 1
        assert stats["failed"] == 1
        assert stats["total"] == 2
        s.close()
