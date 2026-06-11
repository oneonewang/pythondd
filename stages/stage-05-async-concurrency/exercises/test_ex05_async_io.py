"""Ex05 测试。"""
import asyncio

from .ex05_async_io import AsyncFileReader, AsyncRange, read_files_concurrent, sum_async_range


class TestAsyncFileReader:
    def test_read(self, tmp_path) -> None:
        p = tmp_path / "x.txt"
        p.write_text("hello\nworld", encoding="utf-8")
        async def main() -> str:
            async with AsyncFileReader(p) as f:
                return await f.read()
        assert asyncio.run(main()) == "hello\nworld"

    def test_readlines(self, tmp_path) -> None:
        p = tmp_path / "x.txt"
        p.write_text("a\nb\nc", encoding="utf-8")
        async def main() -> list[str]:
            async with AsyncFileReader(p) as f:
                return await f.readlines()
        assert asyncio.run(main()) == ["a", "b", "c"]


class TestReadFilesConcurrent:
    def test_all_files(self, tmp_path) -> None:
        paths = []
        for i in range(5):
            p = tmp_path / f"f{i}.txt"
            p.write_text(f"content {i}", encoding="utf-8")
            paths.append(p)
        result = asyncio.run(read_files_concurrent(paths, max_concurrent=2))
        assert len(result) == 5
        for i, p in enumerate(paths):
            assert result[p] == f"content {i}"

    def test_empty(self, tmp_path) -> None:
        result = asyncio.run(read_files_concurrent([], max_concurrent=2))
        assert result == {}


class TestAsyncRange:
    def test_basic(self) -> None:
        async def main() -> list[int]:
            return [i async for i in AsyncRange(5)]
        assert asyncio.run(main()) == [0, 1, 2, 3, 4]

    def test_with_delay(self) -> None:
        import time
        async def main() -> float:
            start = time.perf_counter()
            async for _ in AsyncRange(5, step_delay=0.02):
                pass
            return time.perf_counter() - start
        elapsed = asyncio.run(main())
        # 5 步 × 0.02s 串行 = 0.1s
        assert elapsed >= 0.09


class TestSumAsyncRange:
    def test_zero(self) -> None:
        assert asyncio.run(sum_async_range(0)) == 0

    def test_basic(self) -> None:
        assert asyncio.run(sum_async_range(10)) == 45     # 0+1+...+9

    def test_large(self) -> None:
        assert asyncio.run(sum_async_range(101)) == 5050  # 0+...+100
