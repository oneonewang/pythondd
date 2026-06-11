"""Ex03 测试。"""
import asyncio
import time

from .ex03_asyncio_basics import (
    fake_io,
    fetch_many,
    gather_with_exception,
    run_concurrent,
    run_sequential,
    schedule_with_delay,
)


class TestFakeIo:
    def test_returns_message(self) -> None:
        result = asyncio.run(fake_io(0.01))
        assert result == "done in 0.01s"


class TestSequential:
    def test_order(self) -> None:
        coros = [fake_io(0.01) for _ in range(3)]
        results = asyncio.run(run_sequential(coros))
        assert len(results) == 3

    def test_takes_sum_of_durations(self) -> None:
        start = time.perf_counter()
        asyncio.run(run_sequential([fake_io(0.02) for _ in range(3)]))
        elapsed = time.perf_counter() - start
        # 串行 3 × 0.02 = 0.06s
        assert elapsed >= 0.05


class TestConcurrent:
    def test_results_match(self) -> None:
        coros = [fake_io(0.01) for _ in range(3)]
        results = asyncio.run(run_concurrent(coros))
        assert len(results) == 3

    def test_actually_concurrent(self) -> None:
        start = time.perf_counter()
        asyncio.run(run_concurrent([fake_io(0.05) for _ in range(4)]))
        elapsed = time.perf_counter() - start
        # 4 × 0.05 并发应该 ≈ 0.05s，不是 0.2s
        assert elapsed < 0.15


class TestGatherException:
    def test_normal(self) -> None:
        async def good() -> int:
            return 1

        async def bad() -> int:
            raise ValueError("oops")

        result = asyncio.run(gather_with_exception(good(), bad(), good()))
        assert result[0] == 1
        assert isinstance(result[1], ValueError)
        assert result[2] == 1


class TestScheduleWithDelay:
    def test_delayed(self) -> None:
        async def immediate() -> str:
            return "hi"

        async def main() -> float:
            start = time.perf_counter()
            t = await schedule_with_delay(immediate(), 0.1)
            await t
            return time.perf_counter() - start

        elapsed = asyncio.run(main())
        assert elapsed >= 0.09


class TestFetchMany:
    def test_count(self) -> None:
        urls = [f"http://x/{i}" for i in range(5)]
        results = asyncio.run(fetch_many(urls))
        assert len(results) == 5

    def test_concurrent(self) -> None:
        urls = [f"http://x/{i}" for i in range(10)]
        start = time.perf_counter()
        asyncio.run(fetch_many(urls))
        elapsed = time.perf_counter() - start
        # 10 × 0.05 并发 ≈ 0.05s
        assert elapsed < 0.3
