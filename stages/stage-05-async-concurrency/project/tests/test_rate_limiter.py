"""RateLimiter 测试。"""
import asyncio

from async_crawler.rate_limiter import RateLimiter


class TestRateLimiter:
    def test_all_complete(self) -> None:
        async def one(i: int) -> int:
            await asyncio.sleep(0.01)
            return i

        async def main() -> list[int]:
            limiter = RateLimiter(max_concurrent=3)
            tasks = [limiter.run(lambda i=i: one(i)) for i in range(10)]
            return await asyncio.gather(*tasks)

        results = asyncio.run(main())
        assert sorted(results) == list(range(10))

    def test_concurrency_limit(self) -> None:
        active = 0
        max_active = 0

        async def one() -> None:
            nonlocal active, max_active
            active += 1
            max_active = max(max_active, active)
            await asyncio.sleep(0.05)
            active -= 1

        async def main() -> int:
            limiter = RateLimiter(max_concurrent=2)
            tasks = [limiter.run(one) for _ in range(10)]
            await asyncio.gather(*tasks)
            return max_active

        result = asyncio.run(main())
        assert result <= 2
