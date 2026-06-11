"""Ex04 测试。"""
import asyncio

import pytest

from .ex04_asyncio_advanced import (
    AsyncCounter,
    async_timer,
    cancel_after,
    first_completed,
    gather_limited,
    with_timeout,
)


class TestWithTimeout:
    def test_ok(self) -> None:
        async def fast() -> int:
            await asyncio.sleep(0.01)
            return 42

        assert asyncio.run(with_timeout(fast(), 0.1)) == 42

    def test_timeout(self) -> None:
        async def slow() -> int:
            await asyncio.sleep(1)
            return 42

        with pytest.raises(asyncio.TimeoutError):
            asyncio.run(with_timeout(slow(), 0.05))


class TestCancelAfter:
    def test_completes_first(self) -> None:
        async def fast() -> str:
            await asyncio.sleep(0.01)
            return "ok"

        assert asyncio.run(cancel_after(fast(), 0.1)) == "ok"

    def test_cancelled(self) -> None:
        async def slow() -> str:
            await asyncio.sleep(1)
            return "never"

        with pytest.raises(asyncio.CancelledError):
            asyncio.run(cancel_after(slow(), 0.05))


class TestGatherLimited:
    def test_results(self) -> None:
        async def one(i: int) -> int:
            await asyncio.sleep(0.01)
            return i * 2

        coros = [one(i) for i in range(20)]
        results = asyncio.run(gather_limited(coros, limit=5))
        assert sorted(results) == [i * 2 for i in range(20)]


class TestFirstCompleted:
    def test_returns_first(self) -> None:
        async def slow() -> int:
            await asyncio.sleep(0.1)
            return 1

        async def fast() -> int:
            await asyncio.sleep(0.01)
            return 2

        result = asyncio.run(first_completed([slow(), fast()]))
        assert result == 2


class TestAsyncTimer:
    def test_records_elapsed(self) -> None:
        async def main() -> None:
            async with async_timer() as info:
                await asyncio.sleep(0.05)
            assert info["elapsed"] >= 0.04

        asyncio.run(main())


class TestAsyncCounter:
    def test_enter_exit_increments(self) -> None:
        async def main() -> None:
            c = AsyncCounter()
            async with c:
                await c.increment()
                await c.increment()
            return c.value

        assert asyncio.run(main()) == 4   # enter +1, 2× inc, exit +1

    def test_enter_exit_on_exception(self) -> None:
        async def main() -> int:
            c = AsyncCounter()
            try:
                async with c:
                    raise ValueError()
            except ValueError:
                pass
            return c.value

        assert asyncio.run(main()) == 2   # enter +1, exit +1
